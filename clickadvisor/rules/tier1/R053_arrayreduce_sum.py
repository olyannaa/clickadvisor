from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_ARRAYREDUCE_SUM_RE = re.compile(r"\barrayReduce\s*\(\s*'sum'\s*,\s*(\w+)\s*\)", re.IGNORECASE)


class R053ArrayReduceSum(Rule):
    rule_id = "R-053"
    name = "arrayreduce_sum_to_arraysum"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _ARRAYREDUCE_SUM_RE.search(context.sql)
        if not m:
            return None
        arr = m.group(1)
        return Finding(
            rule_id=self.rule_id, rule_name=self.name, tier=self.tier, severity="low",
            description=f"arrayReduce('sum', {arr}) заменяется arraySum({arr}).",
            suggestion=f"Замените на arraySum({arr})",
            example_before=f"arrayReduce('sum', {arr})", example_after=f"arraySum({arr})",
            explain_why="arraySum — специализированная функция, более читаемая.",
            confidence="provable", ch_version_introduced=self.ch_version_introduced,
        )
