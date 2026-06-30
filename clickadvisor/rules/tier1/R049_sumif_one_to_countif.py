from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_SUMIF_ONE_RE = re.compile(
    r"\bsumIf\s*\(\s*1\s*,\s*(.+?)\s*\)",
    re.IGNORECASE | re.DOTALL,
)


class R049SumIfOneToCountIf(Rule):
    rule_id = "R-049"
    name = "sumif_one_to_countif"
    tier = "1A"
    ch_version_introduced = "1.23"

    def check(self, context: QueryContext) -> Finding | None:
        m = _SUMIF_ONE_RE.search(context.sql)
        if not m:
            return None
        cond = m.group(1).strip()
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=f"sumIf(1, {cond}) эквивалентно countIf({cond}).",
            suggestion=f"Замените на countIf({cond})",
            example_before=f"sumIf(1, {cond})",
            example_after=f"countIf({cond})",
            explain_why="countIf — нативная функция подсчёта строк по условию; semantically identical.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
