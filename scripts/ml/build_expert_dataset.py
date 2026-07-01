from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import sqlglot
import yaml

from clickadvisor.ml.features import FeatureExtractor

DEFAULT_SOURCES_DIR = Path(".cache/dataset_sources")
DEFAULT_OUTPUT_DIR = Path("data/ml/expert_dataset")
DEFAULT_MAX_FUNCTIONAL_TEST_STATEMENTS = 3200
DEFAULT_MAX_BUG_REPRO_STATEMENTS = 500
MIN_SQL_CHARS = 8

SELECT_RE = re.compile(r"^\s*(?:WITH\b.+?\bSELECT\b|SELECT\b)", re.IGNORECASE | re.DOTALL)
FROM_TABLE_RE = re.compile(r"\bFROM\s+([`\"A-Za-z_][`\"A-Za-z0-9_.]*)\b", re.IGNORECASE)
LIMIT_RE = re.compile(r"\s+LIMIT\s+\d+(?:\s*,\s*\d+)?(?:\s+OFFSET\s+\d+)?\s*$", re.IGNORECASE)
COMMENT_RE = re.compile(r"^\s*(?:--|#)")
CONTROL_PREFIX_RE = re.compile(
    r"^\s*(?:SYSTEM|DROP|TRUNCATE|ATTACH|DETACH|KILL|CHECK|OPTIMIZE|EXPLAIN|DESC|DESCRIBE|ALTER|SHOW|SET|USE)\b",
    re.IGNORECASE,
)
QUERY_PREFIX_RE = re.compile(
    r"^\s*(?:WITH\b.+?\bSELECT\b|SELECT\b|INSERT\b|DELETE\b|CREATE\s+MATERIALIZED\s+VIEW\b)",
    re.IGNORECASE | re.DOTALL,
)


@dataclass(frozen=True, slots=True)
class SourceSpec:
    source: str
    family: str
    license_class: str
    path: Path


@dataclass(frozen=True, slots=True)
class RawQuery:
    sql: str
    source: str
    family: str
    license_class: str
    origin_path: str
    origin_index: int
    is_synthetic: bool = False
    synthesis_method: str | None = None
    parent_hash: str | None = None
    expected_rules: tuple[str, ...] = ()


def main() -> None:
    args = parse_args()
    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_queries = collect_queries(args.sources_dir, args.max_functional, args.max_bugs)
    raw_queries.extend(generate_synthetic_variants(raw_queries, target_count=args.synthetic_target))
    records, skipped = build_records(raw_queries)

    dataset_path = output_dir / "queries.jsonl"
    with dataset_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    manifest = build_manifest(records, skipped, args)
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "README.md").write_text(render_readme(manifest), encoding="utf-8")
    print(f"Wrote {len(records)} expert dataset records to {dataset_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the ClickAdvisor expert SQL dataset.")
    parser.add_argument("--sources-dir", type=Path, default=DEFAULT_SOURCES_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-functional", type=int, default=DEFAULT_MAX_FUNCTIONAL_TEST_STATEMENTS)
    parser.add_argument("--max-bugs", type=int, default=DEFAULT_MAX_BUG_REPRO_STATEMENTS)
    parser.add_argument("--synthetic-target", type=int, default=1800)
    return parser.parse_args()


def collect_queries(sources_dir: Path, max_functional: int, max_bugs: int) -> list[RawQuery]:
    specs = source_specs(sources_dir)
    queries: list[RawQuery] = []
    for spec in specs:
        if not spec.path.exists():
            continue
        if spec.path.is_file() and spec.path.suffix == ".xml":
            queries.extend(read_performance_xml(spec))
        elif spec.path.is_file():
            queries.extend(read_sql_file(spec))
        else:
            paths = sorted(path for path in spec.path.rglob("*") if path.is_file())
            if spec.source == "clickhouse_functional_tests":
                paths = paths[:max_functional]
            if spec.source == "clickhouse_bug_reproducers":
                paths = paths[:max_bugs]
            for path in paths:
                child = SourceSpec(spec.source, spec.family, spec.license_class, path)
                if path.suffix == ".xml":
                    queries.extend(read_performance_xml(child))
                elif path.suffix == ".sql":
                    queries.extend(read_sql_file(child))

    benchmark_dir = Path("benchmark/cases")
    if benchmark_dir.exists():
        for index, path in enumerate(sorted(benchmark_dir.rglob("*.yaml")), start=1):
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
            if isinstance(payload, dict) and isinstance(payload.get("sql"), str):
                queries.append(
                    RawQuery(
                        sql=payload["sql"],
                        source="clickadvisor_benchmark",
                        family=str(payload.get("source") or "local_benchmark"),
                        license_class="project",
                        origin_path=str(path),
                        origin_index=index,
                        expected_rules=tuple(
                            item
                            for item in payload.get("expected_rules_to_fire", [])
                            if isinstance(item, str)
                        ),
                    )
                )
    return queries


def source_specs(sources_dir: Path) -> list[SourceSpec]:
    return [
        SourceSpec(
            "clickbench",
            "olap_flat_web_analytics",
            "permissive_or_project_upstream",
            sources_dir / "clickbench/clickhouse/queries.sql",
        ),
        SourceSpec(
            "clickbench_extended_latency",
            "olap_flat_web_analytics",
            "permissive_or_project_upstream",
            sources_dir / "clickbench/clickhouse/extended/queries_latency.sql",
        ),
        SourceSpec(
            "clickhouse_benchmarks_tpch",
            "tpch",
            "benchmark_kit_derived",
            sources_dir / "zghong-clickhouse-benchmarks/tpch/backup/queries",
        ),
        SourceSpec(
            "clickhouse_benchmarks_tpcds",
            "tpcds",
            "benchmark_kit_derived",
            sources_dir / "zghong-clickhouse-benchmarks/tpcds/backup/queries",
        ),
        SourceSpec(
            "job",
            "join_order_benchmark",
            "non_commercial_dataset_context",
            sources_dir / "job",
        ),
        SourceSpec(
            "clickhouse_performance_tests",
            "clickhouse_perf_xml",
            "apache-2.0",
            sources_dir / "clickhouse-src/tests/performance",
        ),
        SourceSpec(
            "clickhouse_functional_tests",
            "clickhouse_stateless",
            "apache-2.0",
            sources_dir / "clickhouse-src/tests/queries/0_stateless",
        ),
        SourceSpec(
            "clickhouse_bug_reproducers",
            "clickhouse_bugs",
            "apache-2.0",
            sources_dir / "clickhouse-src/tests/queries/bugs",
        ),
    ]


def read_sql_file(spec: SourceSpec) -> list[RawQuery]:
    try:
        text = spec.path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    result: list[RawQuery] = []
    for index, statement in enumerate(split_sql_statements(text), start=1):
        if keep_statement(statement):
            result.append(
                RawQuery(
                    sql=normalize_sql(statement),
                    source=spec.source,
                    family=spec.family,
                    license_class=spec.license_class,
                    origin_path=str(spec.path),
                    origin_index=index,
                )
            )
    return result


def read_performance_xml(spec: SourceSpec) -> list[RawQuery]:
    try:
        root = ET.fromstring(spec.path.read_text(encoding="utf-8", errors="ignore"))
    except (ET.ParseError, OSError):
        return []
    result: list[RawQuery] = []
    for index, node in enumerate(root.findall(".//query"), start=1):
        text = "".join(node.itertext()).strip()
        if keep_statement(text):
            result.append(
                RawQuery(
                    sql=normalize_sql(text),
                    source=spec.source,
                    family=spec.family,
                    license_class=spec.license_class,
                    origin_path=str(spec.path),
                    origin_index=index,
                )
            )
    return result


def split_sql_statements(text: str) -> Iterator[str]:
    buffer: list[str] = []
    quote: str | None = None
    escaped = False
    for char in text:
        buffer.append(char)
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {"'", '"', "`"}:
            quote = char
        elif char == ";":
            statement = "".join(buffer).strip().rstrip(";")
            buffer = []
            if statement:
                yield statement
    tail = "".join(buffer).strip()
    if tail:
        yield tail


def keep_statement(sql: str) -> bool:
    stripped = normalize_sql(sql)
    if len(stripped) < MIN_SQL_CHARS:
        return False
    if COMMENT_RE.match(stripped) or CONTROL_PREFIX_RE.match(stripped):
        return False
    if stripped.startswith(("$", "!", "echo ", "cat ", "grep ")):
        return False
    if "{" in stripped and "}" in stripped:
        return False
    if stripped.count("\n") > 80:
        return False
    return bool(QUERY_PREFIX_RE.match(stripped))


def normalize_sql(sql: str) -> str:
    lines = []
    for line in sql.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("--") or stripped.startswith("#!"):
            continue
        lines.append(line.rstrip())
    return "\n".join(lines).strip().rstrip(";")


def generate_synthetic_variants(seeds: Iterable[RawQuery], target_count: int) -> list[RawQuery]:
    variants: list[RawQuery] = []
    for seed in seeds:
        if len(variants) >= target_count:
            break
        for method, sql in synthesize(seed.sql):
            if len(variants) >= target_count:
                break
            variants.append(
                RawQuery(
                    sql=sql,
                    source="expert_synthetic_antipatterns",
                    family=seed.family,
                    license_class=seed.license_class,
                    origin_path=seed.origin_path,
                    origin_index=seed.origin_index,
                    is_synthetic=True,
                    synthesis_method=method,
                    parent_hash=sql_hash(seed.sql),
                )
            )
    return variants


def synthesize(sql: str) -> Iterator[tuple[str, str]]:
    normalized = normalize_sql(sql)
    if not SELECT_RE.match(normalized):
        return
    if "SELECT *" not in normalized.upper():
        star = replace_projection_with_star(normalized)
        if star and star != normalized:
            yield "replace_projection_with_select_star", star
    no_limit = LIMIT_RE.sub("", normalized)
    if no_limit != normalized and re.search(r"\bORDER\s+BY\b", normalized, re.IGNORECASE):
        yield "remove_limit_from_ordered_query", no_limit
    final = add_final_modifier(normalized)
    if final and final != normalized:
        yield "add_final_modifier_to_first_table", final


def replace_projection_with_star(sql: str) -> str | None:
    match = re.search(r"\bFROM\b", sql, re.IGNORECASE)
    select = re.match(r"\s*SELECT\b", sql, re.IGNORECASE)
    if not match or not select:
        return None
    return "SELECT * " + sql[match.start():]


def add_final_modifier(sql: str) -> str | None:
    match = FROM_TABLE_RE.search(sql)
    if not match:
        return None
    table_end = match.end(1)
    tail = sql[table_end: table_end + 16].upper()
    if " FINAL" in tail:
        return None
    return sql[:table_end] + " FINAL" + sql[table_end:]


def build_records(raw_queries: Iterable[RawQuery]) -> tuple[list[dict[str, Any]], Counter[str]]:
    extractor = FeatureExtractor()
    rule_meta = load_rule_metadata()
    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    skipped: Counter[str] = Counter()
    for raw in raw_queries:
        digest = sql_hash(raw.sql)
        if digest in seen:
            skipped["duplicate_sql"] += 1
            continue
        seen.add(digest)
        try:
            with quiet_sqlglot():
                parsed = sqlglot.parse_one(raw.sql, dialect="clickhouse")
        except sqlglot.errors.SqlglotError:
            skipped["parse_error"] += 1
            continue
        try:
            with quiet_sqlglot():
                features = extractor.extract(raw.sql).to_vector()
        except Exception:
            skipped["analysis_error"] += 1
            continue
        labels = infer_labels(raw, features, rule_meta)
        records.append(
            {
                "id": f"expert_{len(records) + 1:05d}",
                "sql_hash": digest,
                "sql": raw.sql,
                "sqlglot_expression": parsed.key,
                "source": raw.source,
                "family": raw.family,
                "license_class": raw.license_class,
                "origin": {
                    "path": raw.origin_path,
                    "statement_index": raw.origin_index,
                    "parent_sql_hash": raw.parent_hash,
                    "synthesis_method": raw.synthesis_method,
                },
                "is_synthetic": raw.is_synthetic,
                "labels": labels,
                "risk": risk_label(labels),
                "features": features,
                "measured_metrics": None,
                "label_method": "benchmark_expected_rules_plus_feature_weak_labels_v1",
            }
        )
    return records, skipped


@contextlib.contextmanager
def quiet_sqlglot() -> Iterator[None]:
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        yield


def infer_labels(
    raw: RawQuery,
    features: dict[str, float | int],
    rule_meta: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rule_ids = list(raw.expected_rules)
    if features.get("has_count_distinct"):
        rule_ids.extend(["R-001", "R-002"])
    if features.get("has_select_star"):
        rule_ids.append("D-003")
    if features.get("has_final_modifier"):
        rule_ids.append("D-007")
    if features.get("has_no_limit"):
        rule_ids.append("D-004")
    if features.get("has_union") and not features.get("has_union_all"):
        rule_ids.append("R-018")
    if features.get("has_quantile_exact"):
        rule_ids.append("R-003")
    if features.get("has_having_without_aggregate"):
        rule_ids.append("R-011")
    if features.get("has_or_chain_same_column"):
        rule_ids.append("R-010")
    if features.get("has_in_with_single_value"):
        rule_ids.append("R-009")
    if features.get("has_constant_predicate"):
        rule_ids.append("R-012")
    if features.get("has_length_zero_check"):
        rule_ids.append("R-013")
    if features.get("has_async_insert_without_wait"):
        rule_ids.append("D-014")
    if features.get("has_cast_without_default"):
        rule_ids.append("R-020")
    if features.get("has_subquery_with_orderby_no_limit"):
        rule_ids.append("R-016")
    if re.search(r"\bCROSS\s+JOIN\b", raw.sql, re.IGNORECASE):
        rule_ids.append("D-002")
    if re.search(r"\bLIKE\s+'%", raw.sql, re.IGNORECASE):
        rule_ids.append("D-005")
    if re.search(r"\bDELETE\s+FROM\b(?![\s\S]*\bWHERE\b)", raw.sql, re.IGNORECASE):
        rule_ids.append("D-022")
    if re.search(r"\bGROUP\s+BY\b", raw.sql, re.IGNORECASE) and not re.search(
        r"\bLIMIT\b", raw.sql, re.IGNORECASE
    ):
        rule_ids.append("R-112")

    labels: list[dict[str, str]] = []
    seen: set[str] = set()
    for rule_id in rule_ids:
        if rule_id in seen:
            continue
        seen.add(rule_id)
        meta = rule_meta.get(rule_id, {})
        labels.append(
            {
                "rule_id": rule_id,
                "tier": meta.get("tier", "weak"),
                "severity": meta.get("severity", default_severity(rule_id)),
                "confidence": "weak_static",
            }
        )
    return labels


def load_rule_metadata() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for path in Path("docs/rules/cards").glob("*.yaml"):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or not isinstance(payload.get("id"), str):
            continue
        result[payload["id"]] = {
            "tier": str(payload.get("tier") or "weak"),
            "severity": str(payload.get("severity") or default_severity(payload["id"])),
        }
    return result


def default_severity(rule_id: str) -> str:
    if rule_id in {"D-002", "D-014", "D-015", "D-022"}:
        return "high"
    if rule_id.startswith("D-"):
        return "medium"
    return "low"


def risk_label(labels: list[dict[str, str]]) -> dict[str, Any]:
    weights = {"low": 1, "medium": 3, "high": 6}
    score = sum(weights.get(label.get("severity", ""), 0) for label in labels)
    if score >= 9:
        label = "high"
    elif score >= 3:
        label = "medium"
    elif score > 0:
        label = "low"
    else:
        label = "no_known_risk"
    return {"label": label, "score": score}


def sql_hash(sql: str) -> str:
    return hashlib.sha256(normalize_sql(sql).encode("utf-8")).hexdigest()[:24]


def build_manifest(records: list[dict[str, Any]], skipped: Counter[str], args: argparse.Namespace) -> dict[str, Any]:
    sources = Counter(record["source"] for record in records)
    families = Counter(record["family"] for record in records)
    risks = Counter(record["risk"]["label"] for record in records)
    rules: Counter[str] = Counter()
    for record in records:
        rules.update(label["rule_id"] for label in record["labels"])
    return {
        "dataset": "clickadvisor_expert_sql_dataset",
        "version": "2026-07-01",
        "created_at": datetime.now(UTC).isoformat(),
        "builder": "scripts/ml/build_expert_dataset.py",
        "builder_args": {
            "sources_dir": str(args.sources_dir),
            "max_functional": args.max_functional,
            "max_bugs": args.max_bugs,
            "synthetic_target": args.synthetic_target,
        },
        "git_commit": current_git_commit(),
        "record_count": len(records),
        "real_record_count": sum(1 for record in records if not record["is_synthetic"]),
        "synthetic_record_count": sum(1 for record in records if record["is_synthetic"]),
        "source_counts": dict(sorted(sources.items())),
        "family_counts": dict(sorted(families.items())),
        "risk_counts": dict(sorted(risks.items())),
        "top_rule_counts": dict(rules.most_common(40)),
        "skipped_counts": dict(sorted(skipped.items())),
        "label_method": "Benchmark expected rules plus feature-derived static weak labels. measured_metrics is reserved for future query_log replay labels.",
    }


def current_git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def render_readme(manifest: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# ClickAdvisor Expert SQL Dataset",
            "",
            "Воспроизводимый JSONL-корпус из реальных ClickHouse SQL benchmark/test источников и контролируемых antipattern-вариантов.",
            "",
            f"- Записей: {manifest['record_count']}",
            f"- Реальных записей: {manifest['real_record_count']}",
            f"- Синтетических записей: {manifest['synthetic_record_count']}",
            f"- Метод разметки: {manifest['label_method']}",
            "",
            "Файлы:",
            "",
            "- `queries.jsonl` - одна нормализованная запись запроса на строку.",
            "- `manifest.json` - счетчики по источникам, risk-классам, правилам и metadata сборки.",
            "",
            "Поле `measured_metrics` намеренно остается `null`, пока локальный replay в ClickHouse не соберет метрики `system.query_log`.",
            "",
        ]
    )


if __name__ == "__main__":
    main()
