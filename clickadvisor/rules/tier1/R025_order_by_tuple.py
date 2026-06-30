from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_CREATE_TABLE_RE = re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE)
# Matches ORDER BY tuple() or ORDER BY ()
_ORDER_BY_TUPLE_RE = re.compile(
    r"\bORDER\s+BY\s+(?:tuple\s*\(\s*\)|\(\s*\))",
    re.IGNORECASE,
)


class R025OrderByTupleNoPK(Rule):
    rule_id = "R-025"
    name = "order_by_tuple_no_pk"
    tier = "1B"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _CREATE_TABLE_RE.search(sql):
            return None
        if not _ORDER_BY_TUPLE_RE.search(sql):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description=(
                "CREATE TABLE использует ORDER BY tuple() — без первичного ключа. "
                "Каждый SELECT с WHERE будет сканировать все данные без возможности "
                "использовать sparse primary index."
            ),
            suggestion=(
                "Выберите ORDER BY по колонкам, наиболее часто используемым в WHERE. "
                "Например: ORDER BY (user_id, ts) для аналитики по пользователям."
            ),
            example_before=(
                "CREATE TABLE events (user_id UInt64, ts DateTime) "
                "ENGINE = MergeTree ORDER BY tuple()"
            ),
            example_after=(
                "CREATE TABLE events (user_id UInt64, ts DateTime) "
                "ENGINE = MergeTree ORDER BY (user_id, ts)"
            ),
            explain_why=(
                "ORDER BY tuple() отключает сортировку и sparse primary index. "
                "Без primary key каждый SELECT выполняет полный скан — "
                "10-1000x медленнее по сравнению с правильным ORDER BY."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
