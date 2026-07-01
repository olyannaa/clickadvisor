from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.pipeline import AnalysisPipeline
from clickadvisor.rules.registry import get_all_rules

STRING_LITERAL_RE = re.compile(r"'(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"")
NUMBER_LITERAL_RE = re.compile(r"\b\d+(?:\.\d+)?\b")
WHITESPACE_RE = re.compile(r"\s+")

QUERY_COLUMNS = ("query", "sql", "normalized_query")
DURATION_COLUMNS = ("query_duration_ms", "duration_ms", "elapsed_ms")
READ_ROWS_COLUMNS = ("read_rows", "rows_read", "rows")
READ_BYTES_COLUMNS = ("read_bytes", "bytes_read", "bytes")
MEMORY_COLUMNS = ("memory_usage", "peak_memory_usage", "memory_usage_bytes")
SEVERITY_WEIGHT = {"high": 100.0, "medium": 35.0, "low": 10.0}


@dataclass(slots=True)
class QueryGroup:
    fingerprint: str
    normalized_sql: str
    representative_sql: str
    executions: int = 0
    total_duration_ms: int = 0
    avg_duration_ms: float = 0.0
    p95_duration_ms: int = 0
    total_read_rows: int = 0
    total_read_bytes: int = 0
    max_memory_usage: int = 0
    findings_count: int = 0
    high_findings: int = 0
    medium_findings: int = 0
    low_findings: int = 0
    rule_ids: list[str] = field(default_factory=list)
    priority_score: float = 0.0
    priority_label: str = "low"


@dataclass(slots=True)
class WorkloadReport:
    source: str
    rows_read: int
    rows_used: int
    group_count: int
    top_n: int
    groups: list[QueryGroup]


@dataclass(slots=True)
class _GroupAccumulator:
    normalized_sql: str
    representative_sql: str
    durations_ms: list[int] = field(default_factory=list)
    read_rows: int = 0
    read_bytes: int = 0
    memory_values: list[int] = field(default_factory=list)


def _accumulate_rows(
    rows: list[dict[str, str]],
) -> tuple[int, int, dict[str, _GroupAccumulator]]:
    rows_read = 0
    rows_used = 0
    groups: dict[str, _GroupAccumulator] = {}
    for row in rows:
        rows_read += 1
        sql = first_text(row, QUERY_COLUMNS)
        if not sql:
            continue
        rows_used += 1
        normalized = normalize_sql(sql)
        fingerprint = fingerprint_sql(normalized)
        accumulator = groups.setdefault(
            fingerprint,
            _GroupAccumulator(
                normalized_sql=normalized,
                representative_sql=sql.strip(),
            ),
        )
        accumulator.durations_ms.append(first_int(row, DURATION_COLUMNS))
        accumulator.read_rows += first_int(row, READ_ROWS_COLUMNS)
        accumulator.read_bytes += first_int(row, READ_BYTES_COLUMNS)
        accumulator.memory_values.append(first_int(row, MEMORY_COLUMNS))
    return rows_read, rows_used, groups


def _build_report(
    source: str,
    rows_read: int,
    rows_used: int,
    groups: dict[str, _GroupAccumulator],
    *,
    top_n: int,
    ch_version: str | None,
) -> WorkloadReport:
    analyzed_groups = [
        build_query_group(fingerprint, accumulator, ch_version=ch_version)
        for fingerprint, accumulator in groups.items()
    ]
    analyzed_groups.sort(
        key=lambda group: (
            group.priority_score,
            group.total_duration_ms,
            group.total_read_bytes,
            group.executions,
        ),
        reverse=True,
    )
    return WorkloadReport(
        source=source,
        rows_read=rows_read,
        rows_used=rows_used,
        group_count=len(analyzed_groups),
        top_n=top_n,
        groups=analyzed_groups[:top_n],
    )


def analyze_query_log_csv(
    path: Path,
    *,
    top_n: int = 10,
    ch_version: str | None = None,
) -> WorkloadReport:
    """Analyze a sanitized ClickHouse query_log CSV export.

    The analyzer reads metadata and query text only. It does not connect to
    ClickHouse and does not execute user SQL.
    """
    with path.open(encoding="utf-8", newline="") as handle:
        raw_rows: list[dict[str, str]] = list(csv.DictReader(handle))
    rows_read, rows_used, groups = _accumulate_rows(raw_rows)
    return _build_report(
        str(path), rows_read, rows_used, groups, top_n=top_n, ch_version=ch_version
    )


def analyze_query_log_rows(
    rows: list[dict[str, str]],
    *,
    source: str,
    top_n: int = 10,
    ch_version: str | None = None,
) -> WorkloadReport:
    """Analyze query_log rows fetched from a live ClickHouse instance.

    Accepts the same row format as analyze_query_log_csv (list of dicts with
    string values), so ClickHouseLiveReader output can be passed directly.
    """
    rows_read, rows_used, groups = _accumulate_rows(rows)
    return _build_report(
        source, rows_read, rows_used, groups, top_n=top_n, ch_version=ch_version
    )


def normalize_sql(sql: str) -> str:
    text = STRING_LITERAL_RE.sub("?", sql)
    text = NUMBER_LITERAL_RE.sub("?", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = WHITESPACE_RE.sub(" ", text)
    return text.strip().lower()


def fingerprint_sql(normalized_sql: str) -> str:
    return hashlib.sha256(normalized_sql.encode("utf-8")).hexdigest()[:16]


def first_text(row: dict[str, str], columns: tuple[str, ...]) -> str:
    for column in columns:
        value = row.get(column)
        if value:
            return value
    return ""


def first_int(row: dict[str, str], columns: tuple[str, ...]) -> int:
    for column in columns:
        value = row.get(column)
        if value is not None and value != "":
            return parse_int(value)
    return 0


def parse_int(value: str) -> int:
    try:
        return max(0, int(float(value)))
    except ValueError:
        return 0


def build_query_group(
    fingerprint: str,
    accumulator: _GroupAccumulator,
    *,
    ch_version: str | None,
) -> QueryGroup:
    findings = rule_findings_for(accumulator.representative_sql, ch_version=ch_version)
    durations = sorted(accumulator.durations_ms)
    executions = len(durations)
    total_duration = sum(durations)
    high = sum(1 for finding in findings if finding.severity == "high")
    medium = sum(1 for finding in findings if finding.severity == "medium")
    low = sum(1 for finding in findings if finding.severity == "low")
    score = priority_score(
        findings,
        executions=executions,
        total_duration_ms=total_duration,
        total_read_bytes=accumulator.read_bytes,
        max_memory_usage=max(accumulator.memory_values, default=0),
    )
    return QueryGroup(
        fingerprint=fingerprint,
        normalized_sql=accumulator.normalized_sql,
        representative_sql=accumulator.representative_sql,
        executions=executions,
        total_duration_ms=total_duration,
        avg_duration_ms=(total_duration / executions) if executions else 0.0,
        p95_duration_ms=percentile(durations, 95),
        total_read_rows=accumulator.read_rows,
        total_read_bytes=accumulator.read_bytes,
        max_memory_usage=max(accumulator.memory_values, default=0),
        findings_count=len(findings),
        high_findings=high,
        medium_findings=medium,
        low_findings=low,
        rule_ids=[finding.rule_id for finding in findings],
        priority_score=score,
        priority_label=priority_label(score),
    )


def rule_findings_for(sql: str, *, ch_version: str | None) -> list[Finding]:
    pipeline = AnalysisPipeline(get_all_rules())
    report = pipeline.run(QueryContext(sql=sql, ch_version=ch_version))
    return [finding for finding in report.findings if finding.tier != "rag"]


def percentile(values: list[int], percentile_value: int) -> int:
    if not values:
        return 0
    if len(values) == 1:
        return values[0]
    position = (len(values) - 1) * percentile_value / 100
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return values[int(position)]
    fraction = position - lower
    return round(values[lower] * (1 - fraction) + values[upper] * fraction)


def priority_score(
    findings: list[Finding],
    *,
    executions: int,
    total_duration_ms: int,
    total_read_bytes: int,
    max_memory_usage: int,
) -> float:
    rule_score = sum(SEVERITY_WEIGHT.get(finding.severity, 0.0) for finding in findings)
    metric_score = (
        bounded_log_score(total_duration_ms, multiplier=6.0, cap=45.0)
        + bounded_log_score(total_read_bytes, multiplier=3.0, cap=35.0)
        + bounded_log_score(max_memory_usage, multiplier=3.0, cap=35.0)
        + bounded_log_score(executions, multiplier=4.0, cap=15.0)
    )
    return round(rule_score + metric_score, 3)


def bounded_log_score(value: int, *, multiplier: float, cap: float) -> float:
    if value <= 0:
        return 0.0
    return min(cap, math.log10(value + 1) * multiplier)


def priority_label(score: float) -> str:
    if score >= 120:
        return "high"
    if score >= 55:
        return "medium"
    return "low"


def workload_report_to_dict(report: WorkloadReport) -> dict[str, Any]:
    payload = asdict(report)
    payload["groups"] = [asdict(group) for group in report.groups]
    return payload


def render_workload_json(report: WorkloadReport) -> str:
    return json.dumps(workload_report_to_dict(report), ensure_ascii=False, indent=2)


def render_workload_markdown(report: WorkloadReport) -> str:
    lines = [
        "# ClickAdvisor Workload Report",
        "",
        f"- Source: `{report.source}`",
        f"- Rows read: `{report.rows_read}`",
        f"- Rows used: `{report.rows_used}`",
        f"- Normalized query groups: `{report.group_count}`",
        f"- Top groups shown: `{len(report.groups)}`",
        "",
        "## Top Performance Risks",
        "",
    ]
    if not report.groups:
        lines.append("No query groups found.")
        return "\n".join(lines)

    for index, group in enumerate(report.groups, start=1):
        rule_ids = ", ".join(group.rule_ids) if group.rule_ids else "none"
        lines.extend(
            [
                f"### {index}. Fingerprint `{group.fingerprint}`",
                "",
                f"- Priority: `{group.priority_label}` (`{group.priority_score:.3f}`)",
                f"- Executions: `{group.executions}`",
                f"- Total duration: `{group.total_duration_ms}` ms",
                f"- Avg / p95 duration: `{group.avg_duration_ms:.1f}` / `{group.p95_duration_ms}` ms",
                f"- Read rows / bytes: `{group.total_read_rows}` / `{group.total_read_bytes}`",
                f"- Max memory: `{group.max_memory_usage}`",
                f"- Findings: `{group.findings_count}` "
                f"({group.high_findings} high, {group.medium_findings} medium, {group.low_findings} low)",
                f"- Rule IDs: `{rule_ids}`",
                "- Normalized SQL:",
                "```sql",
                group.normalized_sql,
                "```",
                "",
            ]
        )
    return "\n".join(lines)
