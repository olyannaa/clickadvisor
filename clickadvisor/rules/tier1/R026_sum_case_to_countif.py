from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches SUM(CASE WHEN ... THEN 1 ELSE 0 END) or COUNT(CASE WHEN ... THEN 1 END)
_SUM_CASE_ONE_RE = re.compile(
    r"\b(?:SUM|COUNT)\s*\(\s*CASE\s+WHEN\s+(.+?)\s+THEN\s+1\b(?:\s+ELSE\s+0\s*)?\s*END\s*\)",
    re.IGNORECASE | re.DOTALL,
)


class R026SumCaseToCountIf(Rule):
    rule_id = "R-026"
    name = "sum_case_to_countif"
    tier = "1A"
    ch_version_introduced = "1.23"

    def check(self, context: QueryContext) -> Finding | None:
        m = _SUM_CASE_ONE_RE.search(context.sql)
        if not m:
            return None
        cond = m.group(1).strip()
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                "SUM(CASE WHEN ... THEN 1 ELSE 0 END) или COUNT(CASE WHEN ... THEN 1 END) "
                "эквивалентно countIf(cond) — встроенному комбинатору ClickHouse."
            ),
            suggestion=f"Замените на countIf({cond})",
            example_before=f"SUM(CASE WHEN {cond} THEN 1 ELSE 0 END)",
            example_after=f"countIf({cond})",
            explain_why=(
                "countIf(cond) — синтаксический сахар, семантически идентичен "
                "COUNT(CASE WHEN cond THEN 1 END). Без материализации CASE-выражения."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
