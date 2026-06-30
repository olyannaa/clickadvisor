from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches groupArray(col) without a size argument: groupArray(col) but NOT groupArray(N)(col)
# groupArray with limit looks like: groupArray(N)(col) where N is a number
_GROUPARRAY_NO_LIMIT_RE = re.compile(
    r"\bgroupArray\s*\(\s*(?!\d)(\w+)\s*\)",
    re.IGNORECASE,
)


class R042GroupArrayNoLimit(Rule):
    rule_id = "R-042"
    name = "grouparray_without_limit"
    tier = "1B"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _GROUPARRAY_NO_LIMIT_RE.search(context.sql)
        if not m:
            return None
        col = m.group(1)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description=(
                f"groupArray({col}) без ограничения размера накапливает ВСЕ значения в памяти. "
                "На больших данных это может вызвать OOM."
            ),
            suggestion=(
                f"Добавьте лимит: groupArray(1000)({col}). "
                "Выберите N в зависимости от максимально ожидаемого размера группы."
            ),
            example_before=f"SELECT user_id, groupArray({col}) FROM log GROUP BY user_id",
            example_after=f"SELECT user_id, groupArray(1000)({col}) FROM log GROUP BY user_id",
            explain_why=(
                "groupArray без лимита накапливает все значения для каждой группы в RAM. "
                "groupArray(N)(col) безопасно ограничивает размер массива."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
