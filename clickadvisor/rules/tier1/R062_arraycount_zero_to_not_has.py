from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches arrayCount(x -> x = val, arr) = 0
_ARRAYCOUNT_ZERO_RE = re.compile(
    r"\barrayCount\s*\(\s*\w+\s*->\s*\w+\s*=\s*('[^']*'|\d+)\s*,\s*(\w+)\s*\)\s*=\s*0\b",
    re.IGNORECASE,
)


class R062ArrayCountZeroToNotHas(Rule):
    rule_id = "R-062"
    name = "arraycount_zero_to_not_has"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _ARRAYCOUNT_ZERO_RE.search(context.sql)
        if not m:
            return None
        val, arr = m.group(1), m.group(2)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=f"arrayCount(x -> x = {val}, {arr}) = 0 заменяется NOT has({arr}, {val}).",
            suggestion=f"Замените на NOT has({arr}, {val})",
            example_before=f"arrayCount(x -> x = {val}, {arr}) = 0",
            example_after=f"NOT has({arr}, {val})",
            explain_why="has() более эффективная функция поиска по значению в массиве.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
