from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_CREATE_TABLE_RE = re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE)
_NULLABLE_COL_RE = re.compile(
    r"`?(\w+)`?\s+Nullable\s*\(\s*(\w+)",
    re.IGNORECASE,
)


class D017NullableColumnInDDL(Rule):
    rule_id = "D-017"
    name = "nullable_column_in_ddl"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _CREATE_TABLE_RE.search(sql):
            return None
        m = _NULLABLE_COL_RE.search(sql)
        if not m:
            return None
        column = m.group(1)
        inner_type = m.group(2)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description=(
                f"Колонка '{column}' объявлена как Nullable({inner_type}). "
                "Nullable создаёт дополнительный файл UInt8-маски, увеличивая хранение "
                "и замедляя обработку. Nullable-колонки не могут быть в table indexes."
            ),
            suggestion=(
                f"Рассмотрите замену на {inner_type} DEFAULT 0 (для числовых) "
                f"или {inner_type} DEFAULT '' (для строк), если NULL не несёт "
                "семантической нагрузки."
            ),
            example_before=f"CREATE TABLE t ({column} Nullable({inner_type})) ENGINE = MergeTree ORDER BY tuple()",
            example_after=f"CREATE TABLE t ({column} {inner_type} DEFAULT 0) ENGINE = MergeTree ORDER BY tuple()",
            explain_why=(
                "Nullable column consumes additional storage space и almost always "
                "negatively affects performance (ClickHouse docs). "
                "Nullable type field cannot be included in table indexes."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
