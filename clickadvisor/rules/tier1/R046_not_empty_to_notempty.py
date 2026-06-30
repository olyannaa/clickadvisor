from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches NOT empty(col)
_NOT_EMPTY_RE = re.compile(
    r"\bNOT\s+empty\s*\(\s*(\w+)\s*\)",
    re.IGNORECASE,
)


class R046NotEmptyToNotEmpty(Rule):
    rule_id = "R-046"
    name = "not_empty_to_notempty"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _NOT_EMPTY_RE.search(context.sql)
        if not m:
            return None
        col = m.group(1)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                f"NOT empty({col}) эквивалентно notEmpty({col}). "
                "notEmpty — нативная функция ClickHouse."
            ),
            suggestion=f"Замените NOT empty({col}) на notEmpty({col})",
            example_before=f"WHERE NOT empty({col})",
            example_after=f"WHERE notEmpty({col})",
            explain_why=(
                "notEmpty(x) ≡ NOT empty(x). "
                "Нативная функция устраняет оператор NOT и более читаема."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
