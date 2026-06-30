from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches col LIKE 'literal' where literal has no % or _
_LIKE_NO_WILDCARD_RE = re.compile(
    r"(\w+)\s+LIKE\s+'([^%_']+)'",
    re.IGNORECASE,
)


class R045LikeWithoutWildcardsToEq(Rule):
    rule_id = "R-045"
    name = "like_without_wildcards_to_eq"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _LIKE_NO_WILDCARD_RE.search(context.sql)
        if not m:
            return None
        col = m.group(1)
        pattern = m.group(2)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                f"{col} LIKE '{pattern}' без шаблонов (% и _) эквивалентен "
                f"{col} = '{pattern}'. "
                "LIKE без шаблонов компилируется в regexp, что избыточно."
            ),
            suggestion=f"Замените на {col} = '{pattern}'",
            example_before=f"WHERE {col} LIKE '{pattern}'",
            example_after=f"WHERE {col} = '{pattern}'",
            explain_why=(
                "LIKE 'pattern' без % и _ = exact match = = 'pattern'. "
                "= выполняет прямое сравнение без regexp overhead."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
