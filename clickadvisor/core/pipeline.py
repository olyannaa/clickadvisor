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


class AnalysisPipeline:
    def __init__(
        self,
        rules: list[Rule],
        mode: str = "diagnose",
        retrieval_advisor: RetrievalAdvisorProtocol | None = None,
    ) -> None:
        self.rules = rules
        self.mode = mode
        self.retrieval_advisor = retrieval_advisor

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
