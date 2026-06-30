from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_MIN_CASE_RE = re.compile(
    r"\bMIN\s*\(\s*CASE\s+WHEN\s+(.+?)\s+THEN\s+([^\s)][^)]+?)\s+END\s*\)",
    re.IGNORECASE | re.DOTALL,
)


class R034MinCaseToMinIf(Rule):
    rule_id = "R-034"
    name = "min_case_to_minif"
    tier = "1A"
    ch_version_introduced = "1.23"

    def check(self, context: QueryContext) -> Finding | None:
        m = _MIN_CASE_RE.search(context.sql)
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
                f"MIN(CASE WHEN {cond} THEN {col} END) эквивалентен minIf({col}, {cond})."
            ),
            suggestion=f"Замените на minIf({col}, {cond})",
            example_before=f"MIN(CASE WHEN {cond} THEN {col} END)",
            example_after=f"minIf({col}, {cond})",
            explain_why=(
                "minIf — встроенный комбинатор ClickHouse. "
                "NULL из CASE игнорируется MIN — то же поведение minIf."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
