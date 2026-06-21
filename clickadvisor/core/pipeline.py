from __future__ import annotations

from clickadvisor.core.models import QueryContext, Report
from clickadvisor.rules.base import Rule
from clickadvisor.rules.registry import get_all_rules

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class AnalysisPipeline:
    def __init__(self, rules: list[Rule], mode: str = "diagnose") -> None:
        self.rules = rules
        self.mode = mode

    def run(self, context: QueryContext) -> Report:
        findings = []
        skipped = []

        for rule in self.rules:
            if context.ch_version and not rule.is_applicable_for_version(context.ch_version):
                skipped.append(rule.rule_id)
                continue

            rule.mode = self.mode
            finding = rule.check(context)
            if finding:
                findings.append(finding)

        findings.sort(key=lambda finding: SEVERITY_ORDER.get(finding.severity, 99))

        return Report(
            query_context=context,
            findings=findings,
            rules_skipped_version=sorted(skipped),
        )


def analyze_query(context: QueryContext, mode: str = "diagnose") -> Report:
    return AnalysisPipeline(get_all_rules(), mode=mode).run(context)
