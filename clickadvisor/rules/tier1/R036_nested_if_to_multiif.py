from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches IF(cond1, val1, IF(cond2, val2, val3))
# Simple regex for one level of nesting
_NESTED_IF_RE = re.compile(
    r"\bIF\s*\(\s*([^,()]+?)\s*,\s*([^,()]+?)\s*,\s*IF\s*\(",
    re.IGNORECASE,
)


class R036NestedIfToMultiIf(Rule):
    rule_id = "R-036"
    name = "nested_if_to_multiif"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if not _NESTED_IF_RE.search(context.sql):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                "Обнаружен вложенный IF(..., ..., IF(...)). "
                "multiIf(c1, v1, c2, v2, else_v) читаемее и избавляет от вложенности."
            ),
            suggestion="Замените IF(c1, v1, IF(c2, v2, v3)) на multiIf(c1, v1, c2, v2, v3)",
            example_before="IF(score > 90, 'A', IF(score > 70, 'B', 'C'))",
            example_after="multiIf(score > 90, 'A', score > 70, 'B', 'C')",
            explain_why=(
                "multiIf — нативная функция ClickHouse для множественных условий. "
                "Семантически идентична вложенным IF, но более читаема и устраняет вложенность."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
