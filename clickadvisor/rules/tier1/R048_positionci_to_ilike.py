from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_POSITIONCI_GT_ZERO_RE = re.compile(
    r"\bpositionCaseInsensitive\s*\(\s*(\w+)\s*,\s*'([^']+)'\s*\)\s*>\s*0",
    re.IGNORECASE,
)


class R048PositionCIToILike(Rule):
    rule_id = "R-048"
    name = "positioncaseinsensitive_to_ilike"
    tier = "1A"
    ch_version_introduced = "22.6"

    def check(self, context: QueryContext) -> Finding | None:
        m = _POSITIONCI_GT_ZERO_RE.search(context.sql)
        if not m:
            return None
        col, pattern = m.group(1), m.group(2)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=f"positionCaseInsensitive({col}, '{pattern}') > 0 эквивалентно {col} ILIKE '%{pattern}%'.",
            suggestion=f"Замените на {col} ILIKE '%{pattern}%'",
            example_before=f"WHERE positionCaseInsensitive({col}, '{pattern}') > 0",
            example_after=f"WHERE {col} ILIKE '%{pattern}%'",
            explain_why="ILIKE более читаем и может использовать case-insensitive skip-индексы.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
