from __future__ import annotations

import json
import re
from urllib.parse import urlparse

from rich.console import Console, Group, RenderableType
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from clickadvisor.core.models import Finding, Report
from clickadvisor.rules.registry import get_registered_rule

SEVERITY_STYLES = {"high": "bold red", "medium": "bold yellow", "low": "bold blue"}


def _is_rag_finding(finding: Finding) -> bool:
    return finding.tier == "rag" or finding.rule_id.startswith("RAG-")


def _split_findings(findings: list[Finding]) -> tuple[list[Finding], list[Finding]]:
    rule_findings = [finding for finding in findings if not _is_rag_finding(finding)]
    rag_findings = [finding for finding in findings if _is_rag_finding(finding)]
    return rule_findings, rag_findings


def _summary_counts(report: Report) -> tuple[int, int, int]:
    high = sum(1 for finding in report.findings if finding.severity == "high")
    medium = sum(1 for finding in report.findings if finding.severity == "medium")
    low = sum(1 for finding in report.findings if finding.severity == "low")
    return high, medium, low


def _render_finding(finding: Finding, mode: str) -> Panel:
    body: list[RenderableType] = []
    severity_style = SEVERITY_STYLES.get(finding.severity, "bold white")

    header = Text()
    header.append("● ", style=severity_style)
    header.append(finding.severity.upper(), style=severity_style)
    header.append(f"  {finding.rule_id} · {finding.rule_name}", style="bold")
    body.append(header)
    body.append(Text(f"Найдено: {finding.description}", style="white"))
    body.append(Text(f"Решение: {finding.suggestion}", style="green"))

    if finding.example_before:
        body.append(Text("До:", style="bold"))
        body.append(Syntax(finding.example_before, "sql", theme="monokai", word_wrap=True))
    if finding.example_after:
        body.append(Text("После:", style="bold"))
        body.append(Syntax(finding.example_after, "sql", theme="monokai", word_wrap=True))
    if mode == "explain" and finding.explain_why:
        body.append(Text(f"Почему: {finding.explain_why}", style="cyan"))

    return Panel(
        Group(*body),
        border_style=SEVERITY_STYLES.get(finding.severity, "white"),
        padding=(0, 1),
    )


def _render_skipped_rules(skipped_rules: list[str]) -> str:
    if not skipped_rules:
        return "нет"

    rendered = []
    for rule_id in skipped_rules:
        rule = get_registered_rule(rule_id)
        if rule is None:
            rendered.append(rule_id)
            continue
        rendered.append(f"{rule_id} (requires {rule.ch_version_introduced}+)")
    return ", ".join(rendered)


def _extract_rag_score(finding: Finding) -> str:
    match = re.search(r"score:\s*([0-9.]+)", finding.description)
    return match.group(1) if match else "n/a"


def _extract_rag_url(finding: Finding) -> str:
    marker = "Источник:"
    if marker not in finding.suggestion:
        return ""
    return finding.suggestion.rsplit(marker, 1)[1].strip()


def _extract_rag_text(finding: Finding) -> str:
    marker = "Источник:"
    text = finding.suggestion.split(marker, 1)[0].strip()
    return text.replace("\n", " ")


def _source_label(url: str) -> str:
    if not url:
        return "knowledge base"
    host = urlparse(url).netloc
    return host or url


def _render_rag_findings(findings: list[Finding]) -> Panel:
    body: list[RenderableType] = []
    for index, finding in enumerate(findings, start=1):
        score = _extract_rag_score(finding)
        url = _extract_rag_url(finding)
        text = _extract_rag_text(finding)
        preview = text[:220] + ("..." if len(text) > 220 else "")

        body.append(Text(f"[{index}] (score: {score}) {_source_label(url)}", style="bold blue"))
        body.append(Text(f'    "{preview}"', style="white"))
        if url:
            body.append(Text(f"    → {url}", style="cyan"))

    return Panel(
        Group(*body),
        title="📚 Релевантная документация",
        border_style="blue",
        padding=(0, 1),
    )


def _finding_to_dict(finding: Finding) -> dict[str, object]:
    payload: dict[str, object] = {
        "rule_id": finding.rule_id,
        "tier": finding.tier,
        "severity": finding.severity,
        "description": finding.description,
        "suggestion": finding.suggestion,
        "confidence": finding.confidence,
    }
    if finding.example_before is not None:
        payload["example_before"] = finding.example_before
    if finding.example_after is not None:
        payload["example_after"] = finding.example_after
    if finding.explain_why is not None:
        payload["explain_why"] = finding.explain_why
    if finding.ch_version_introduced is not None:
        payload["ch_version_introduced"] = finding.ch_version_introduced
    return payload


def report_to_json_dict(report: Report) -> dict[str, object]:
    return {
        "ch_version": report.query_context.ch_version,
        "findings_count": len(report.findings),
        "findings": [_finding_to_dict(finding) for finding in report.findings],
        "rules_skipped_version": report.rules_skipped_version,
    }


def print_report_console(
    report: Report,
    mode: str = "diagnose",
    console: Console | None = None,
) -> None:
    active_console = console or Console()
    version = report.query_context.ch_version or "unknown"
    applied_count = len(report.findings)
    skipped_count = len(report.rules_skipped_version)
    header_stats = f"Rules applied: {applied_count} | Skipped: {skipped_count}"

    header = Table.grid(expand=True)
    header.add_row(Text("ClickAdvisor — Query Analysis Report", style="bold magenta"))
    header.add_row(Text(f"ClickHouse version: {version}", style="white"))
    header.add_row(Text(header_stats, style="white"))
    active_console.print(Panel(header, border_style="magenta", padding=(0, 2)))

    rule_findings, rag_findings = _split_findings(report.findings)

    if rule_findings:
        for finding in rule_findings:
            active_console.print(_render_finding(finding, mode))
    elif rag_findings:
        active_console.print(
            Panel(Text("Основных rule-находок не обнаружено.", style="green"), border_style="green")
        )
    else:
        active_console.print(
            Panel(Text("Находок не обнаружено.", style="green"), border_style="green")
        )

    if rag_findings:
        active_console.print(_render_rag_findings(rag_findings))

    high, medium, low = _summary_counts(report)
    summary = Text()
    summary.append(
        f"Итого: {len(report.findings)} находки ({high} high, {medium} medium, {low} low)",
        style="bold",
    )
    active_console.print(summary)
    active_console.print(
        Text(
            f"Пропущено по версии CH: {_render_skipped_rules(report.rules_skipped_version)}",
            style="dim",
        )
    )


def render_json(report: Report) -> str:
    return json.dumps(report_to_json_dict(report), ensure_ascii=False, indent=2)


def print_report_json(report: Report, console: Console | None = None) -> None:
    active_console = console or Console()
    active_console.print_json(render_json(report))


def render_markdown(report: Report, mode: str = "diagnose") -> str:
    version = report.query_context.ch_version or "unknown"
    rule_findings, rag_findings = _split_findings(report.findings)
    lines = [
        "# ClickAdvisor Report",
        "",
        f"- ClickHouse version: `{version}`",
        f"- Findings count: `{len(report.findings)}`",
        f"- Rules skipped by version: `{len(report.rules_skipped_version)}`",
        "",
    ]

    if not rule_findings and not rag_findings:
        lines.append("Находок не обнаружено.")
    else:
        for finding in rule_findings:
            lines.extend(
                [
                    f"## {finding.rule_id} — {finding.rule_name}",
                    f"- Severity: `{finding.severity}`",
                    f"- Tier: `{finding.tier}`",
                    f"- Найдено: {finding.description}",
                    f"- Решение: {finding.suggestion}",
                ]
            )
            if finding.example_before:
                lines.extend(["- До:", "```sql", finding.example_before, "```"])
            if finding.example_after:
                lines.extend(["- После:", "```sql", finding.example_after, "```"])
            if mode == "explain" and finding.explain_why:
                lines.append(f"- Почему: {finding.explain_why}")
            lines.append("")

        if rag_findings:
            lines.extend(["## 📚 Релевантная документация", ""])
            for index, finding in enumerate(rag_findings, start=1):
                score = _extract_rag_score(finding)
                url = _extract_rag_url(finding)
                text = _extract_rag_text(finding)
                lines.append(f"{index}. **(score: {score}) {_source_label(url)}**")
                lines.append(f"   > {text[:500]}")
                if url:
                    lines.append(f"   → {url}")
                lines.append("")

    lines.extend(
        [
            "## Summary",
            f"- Пропущено по версии CH: {_render_skipped_rules(report.rules_skipped_version)}",
        ]
    )
    return "\n".join(lines)


def print_report_markdown(
    report: Report,
    mode: str = "diagnose",
    console: Console | None = None,
) -> None:
    active_console = console or Console()
    active_console.print(render_markdown(report, mode=mode))
