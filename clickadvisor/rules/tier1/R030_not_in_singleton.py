from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches col NOT IN (single_value) — one numeric or string literal, no comma
_NOT_IN_SINGLETON_RE = re.compile(
    r"(\w+)\s+NOT\s+IN\s*\(\s*('[^']*'|\d+(?:\.\d+)?)\s*\)",
    re.IGNORECASE,
)


class R030NotInSingleton(Rule):
    rule_id = "R-030"
    name = "not_in_singleton_to_not_equal"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _NOT_IN_SINGLETON_RE.search(context.sql)
        if not m:
            return None
        col = m.group(1)
        val = m.group(2)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                f"{col} NOT IN ({val}) с одним значением эквивалентен "
                f"{col} != {val} для не-Nullable колонок."
            ),
            suggestion=f"Замените на {col} != {val}",
            example_before=f"WHERE {col} NOT IN ({val})",
            example_after=f"WHERE {col} != {val}",
            explain_why=(
                "NOT IN с одним элементом строит hash set вместо прямого "
                "скалярного сравнения. Для не-Nullable колонок результат идентичен !=."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
