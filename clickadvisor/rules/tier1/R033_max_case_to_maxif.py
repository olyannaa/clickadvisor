from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches MAX(CASE WHEN cond THEN col END) without ELSE
_MAX_CASE_RE = re.compile(
    r"\bMAX\s*\(\s*CASE\s+WHEN\s+(.+?)\s+THEN\s+([^\s)][^)]+?)\s+END\s*\)",
    re.IGNORECASE | re.DOTALL,
)


class R033MaxCaseToMaxIf(Rule):
    rule_id = "R-033"
    name = "max_case_to_maxif"
    tier = "1A"
    ch_version_introduced = "1.23"

    def check(self, context: QueryContext) -> Finding | None:
        m = _MAX_CASE_RE.search(context.sql)
        if not m:
            return None
        cond = m.group(1).strip()
        col = m.group(2).strip()
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                f"MAX(CASE WHEN {cond} THEN {col} END) эквивалентен maxIf({col}, {cond})."
            ),
            suggestion=f"Замените на maxIf({col}, {cond})",
            example_before=f"MAX(CASE WHEN {cond} THEN {col} END)",
            example_after=f"maxIf({col}, {cond})",
            explain_why=(
                "maxIf — встроенный комбинатор ClickHouse, семантически идентичный "
                "MAX(CASE WHEN cond THEN col END). NULL из CASE игнорируется MAX."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
