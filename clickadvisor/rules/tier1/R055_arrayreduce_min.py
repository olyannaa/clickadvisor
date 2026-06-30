from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_ARRAYREDUCE_MIN_RE = re.compile(r"\barrayReduce\s*\(\s*'min'\s*,\s*(\w+)\s*\)", re.IGNORECASE)


class R055ArrayReduceMin(Rule):
    rule_id = "R-055"
    name = "arrayreduce_min_to_arraymin"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _ARRAYREDUCE_MIN_RE.search(context.sql)
        if not m:
            return None
        arr = m.group(1)
        return Finding(
            rule_id=self.rule_id, rule_name=self.name, tier=self.tier, severity="low",
            description=f"arrayReduce('min', {arr}) заменяется arrayMin({arr}).",
            suggestion=f"Замените на arrayMin({arr})",
            example_before=f"arrayReduce('min', {arr})", example_after=f"arrayMin({arr})",
            explain_why="arrayMin — специализированная нативная функция.",
            confidence="provable", ch_version_introduced=self.ch_version_introduced,
        )
