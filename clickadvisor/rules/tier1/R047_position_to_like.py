from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_POSITION_GT_ZERO_RE = re.compile(
    r"\bposition\s*\(\s*(\w+)\s*,\s*'([^']+)'\s*\)\s*>\s*0",
    re.IGNORECASE,
)


class R047PositionToLike(Rule):
    rule_id = "R-047"
    name = "position_gt_zero_to_like"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _POSITION_GT_ZERO_RE.search(context.sql)
        if not m:
            return None
        col, pattern = m.group(1), m.group(2)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=f"position({col}, '{pattern}') > 0 эквивалентно {col} LIKE '%{pattern}%'.",
            suggestion=f"Замените на {col} LIKE '%{pattern}%'",
            example_before=f"WHERE position({col}, '{pattern}') > 0",
            example_after=f"WHERE {col} LIKE '%{pattern}%'",
            explain_why="LIKE может использовать skip-индекс (ngrambf_v1, text), position() — нет.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
