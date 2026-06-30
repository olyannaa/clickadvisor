from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_ARRAYREDUCE_MAX_RE = re.compile(r"\barrayReduce\s*\(\s*'max'\s*,\s*(\w+)\s*\)", re.IGNORECASE)


class R054ArrayReduceMax(Rule):
    rule_id = "R-054"
    name = "arrayreduce_max_to_arraymax"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _ARRAYREDUCE_MAX_RE.search(context.sql)
        if not m:
            return None
        arr = m.group(1)
        return Finding(
            rule_id=self.rule_id, rule_name=self.name, tier=self.tier, severity="low",
            description=f"arrayReduce('max', {arr}) заменяется arrayMax({arr}).",
            suggestion=f"Замените на arrayMax({arr})",
            example_before=f"arrayReduce('max', {arr})", example_after=f"arrayMax({arr})",
            explain_why="arrayMax — специализированная нативная функция.",
            confidence="provable", ch_version_introduced=self.ch_version_introduced,
        )
