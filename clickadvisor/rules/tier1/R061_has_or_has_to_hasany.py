from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_HAS_OR_HAS_RE = re.compile(
    r"\bhas\s*\(\s*(\w+)\s*,\s*('[^']*'|\d+)\s*\)\s+OR\s+has\s*\(\s*\1\s*,\s*('[^']*'|\d+)\s*\)",
    re.IGNORECASE,
)


class R061HasOrHasToHasAny(Rule):
    rule_id = "R-061"
    name = "has_or_has_to_hasany"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _HAS_OR_HAS_RE.search(context.sql)
        if not m:
            return None
        arr, v1, v2 = m.group(1), m.group(2), m.group(3)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=f"has({arr}, {v1}) OR has({arr}, {v2}) заменяется hasAny({arr}, [{v1}, {v2}]).",
            suggestion=f"Замените на hasAny({arr}, [{v1}, {v2}])",
            example_before=f"has({arr}, {v1}) OR has({arr}, {v2})",
            example_after=f"hasAny({arr}, [{v1}, {v2}])",
            explain_why="hasAny более читаем и легко расширяется для дополнительных значений.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
