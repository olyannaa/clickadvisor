from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches lower(col) LIKE 'pattern'
_LOWER_LIKE_RE = re.compile(
    r"\blower\s*\(\s*(\w+)\s*\)\s+LIKE\s+('[^']*')",
    re.IGNORECASE,
)


class R029LowerLikeToILike(Rule):
    rule_id = "R-029"
    name = "lower_col_like_to_ilike"
    tier = "1A"
    ch_version_introduced = "22.6"

    def check(self, context: QueryContext) -> Finding | None:
        m = _LOWER_LIKE_RE.search(context.sql)
        if not m:
            return None
        column = m.group(1)
        pattern = m.group(2)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                f"lower({column}) LIKE {pattern} эквивалентен "
                f"{column} ILIKE {pattern}. "
                "ILIKE — нативный оператор ClickHouse (с версии 22.6)."
            ),
            suggestion=f"Замените на {column} ILIKE {pattern}",
            example_before=f"lower({column}) LIKE {pattern}",
            example_after=f"{column} ILIKE {pattern}",
            explain_why=(
                "ILIKE выполняет регистронезависимое сравнение без явного вызова lower(). "
                "Упрощает план запроса и улучшает читаемость кода."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
