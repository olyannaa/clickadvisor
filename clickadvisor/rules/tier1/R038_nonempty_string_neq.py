from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches col != '' or col <> '' (not-empty string comparison)
_NEQ_EMPTY_RE = re.compile(
    r"(\w+)\s*(?:!=|<>)\s*''|''\s*(?:!=|<>)\s*(\w+)",
    re.IGNORECASE,
)


class R038NonEmptyStringNeqToNotEmpty(Rule):
    rule_id = "R-038"
    name = "nonempty_string_neq_to_notempty"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _NEQ_EMPTY_RE.search(context.sql)
        if not m:
            return None
        col = (m.group(1) or m.group(2)).strip()
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                f"'{col} != ''' можно заменить на notEmpty({col}). "
                "notEmpty() — специализированный предикат ClickHouse."
            ),
            suggestion=f"Замените на notEmpty({col})",
            example_before=f"WHERE {col} != ''",
            example_after=f"WHERE notEmpty({col})",
            explain_why=(
                "notEmpty(s) ≡ s != '' для String типа. "
                "notEmpty() более читаем и выражает намерение напрямую."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
