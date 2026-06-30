from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches length(col) >= 1
_LENGTH_GTE_ONE_RE = re.compile(
    r"\blength\s*\(\s*(\w+)\s*\)\s*>=\s*1\b",
    re.IGNORECASE,
)


class R039LengthGteOneToNotEmpty(Rule):
    rule_id = "R-039"
    name = "length_gte_one_to_notempty"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _LENGTH_GTE_ONE_RE.search(context.sql)
        if not m:
            return None
        col = m.group(1)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                f"length({col}) >= 1 эквивалентно notEmpty({col}). "
                "notEmpty() — специализированный предикат ClickHouse."
            ),
            suggestion=f"Замените length({col}) >= 1 на notEmpty({col})",
            example_before=f"WHERE length({col}) >= 1",
            example_after=f"WHERE notEmpty({col})",
            explain_why=(
                "length(x) >= 1 ≡ length(x) > 0 ≡ notEmpty(x). "
                "notEmpty более читаем и выражает намерение напрямую."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
