from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches col = '' or '' = col (empty string comparison)
_EQ_EMPTY_RE = re.compile(
    r"(\w+)\s*=\s*''|''\s*=\s*(\w+)",
    re.IGNORECASE,
)


class R037EmptyStringEqToEmpty(Rule):
    rule_id = "R-037"
    name = "empty_string_eq_to_empty"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _EQ_EMPTY_RE.search(context.sql)
        if not m:
            return None
        col = (m.group(1) or m.group(2)).strip()
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                f"'{col} = ''' можно заменить на empty({col}). "
                "empty() — специализированный предикат ClickHouse."
            ),
            suggestion=f"Замените на empty({col})",
            example_before=f"WHERE {col} = ''",
            example_after=f"WHERE empty({col})",
            explain_why=(
                "empty(s) ≡ s = '' для String типа. "
                "empty() более читаем и выражает намерение напрямую."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
