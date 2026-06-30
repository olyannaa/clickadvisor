from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_AVG_CASE_RE = re.compile(
    r"\bAVG\s*\(\s*CASE\s+WHEN\s+(.+?)\s+THEN\s+([^\s)][^)]+?)\s+END\s*\)",
    re.IGNORECASE | re.DOTALL,
)


class R035AvgCaseToAvgIf(Rule):
    rule_id = "R-035"
    name = "avg_case_to_avgif"
    tier = "1A"
    ch_version_introduced = "1.23"

    def check(self, context: QueryContext) -> Finding | None:
        m = _AVG_CASE_RE.search(context.sql)
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
                f"AVG(CASE WHEN {cond} THEN {col} END) эквивалентен avgIf({col}, {cond})."
            ),
            suggestion=f"Замените на avgIf({col}, {cond})",
            example_before=f"AVG(CASE WHEN {cond} THEN {col} END)",
            example_after=f"avgIf({col}, {cond})",
            explain_why=(
                "avgIf — встроенный комбинатор. "
                "AVG игнорирует NULL из CASE — то же поведение avgIf."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
