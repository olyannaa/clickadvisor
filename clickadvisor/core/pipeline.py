from __future__ import annotations

import logging
from typing import Protocol

from clickadvisor.core.models import Finding, QueryContext, Report
from clickadvisor.rules.base import Rule
from clickadvisor.rules.registry import get_all_rules

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
logger = logging.getLogger(__name__)


class RetrievalAdvisorProtocol(Protocol):
    def generate_advisory(
        self,
        context: QueryContext,
        existing_findings: list[Finding],
    ) -> list[Finding]: ...


class ImpactEstimateProtocol(Protocol):
    def format_summary(self) -> str: ...


class ExplainComparatorProtocol(Protocol):
    def compare(
        self,
        original_sql: str,
        rewritten_sql: str,
    ) -> ImpactEstimateProtocol | None: ...


class AnalysisPipeline:
    def __init__(
        self,
        rules: list[Rule],
        mode: str = "diagnose",
        retrieval_advisor: RetrievalAdvisorProtocol | None = None,
        explain_comparator: ExplainComparatorProtocol | None = None,
    ) -> None:
        self.rules = rules
        self.mode = mode
        self.retrieval_advisor = retrieval_advisor
        self.explain_comparator = explain_comparator

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
                if finding.example_after:
                    finding.rewritten_sql = finding.example_after
                if (
                    self.explain_comparator
                    and finding.example_after
                    and finding.tier in ("1A", "1B", "1C")
                ):
                    try:
                        impact = self.explain_comparator.compare(
                            context.sql,
                            finding.example_after,
                        )
                        if impact:
                            finding.impact_estimate = impact.format_summary()
                    except Exception as error:
                        logger.warning("EXPLAIN ESTIMATE comparison failed: %s", error)
                findings.append(finding)

        findings.sort(key=lambda finding: SEVERITY_ORDER.get(finding.severity, 99))

        rag_findings: list[Finding] = []
        if self.retrieval_advisor:
            try:
                rag_findings = self.retrieval_advisor.generate_advisory(context, findings)
            except Exception as error:
                logger.warning("Retrieval advisory failed: %s", error)

        return Report(
            query_context=context,
            findings=findings + rag_findings,
            rules_skipped_version=sorted(skipped),
        )


def analyze_query(context: QueryContext, mode: str = "diagnose") -> Report:
    return AnalysisPipeline(get_all_rules(), mode=mode).run(context)
