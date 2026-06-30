from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_CREATE_TABLE_RE = re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE)
_STRING_COL_RE = re.compile(
    r"`?(\w+)`?\s+String\b",
    re.IGNORECASE,
)
_DATE_NAME_PARTS = frozenset(
    ["date", "datetime", "timestamp", "time", "created", "updated", "modified",
     "deleted", "occurred", "happened", "at", "on", "when", "dt", "ts"]
)


def _is_datetime_name(name: str) -> bool:
    parts = name.lower().split("_")
    # require at least one date-related word in name parts
    if _DATE_NAME_PARTS.intersection(parts):
        return True
    low = name.lower()
    # also catch names like 'created_at', 'event_date', 'event_time'
    return any(low.endswith(s) for s in ("_at", "_date", "_time", "_ts", "_dt", "_on"))


class R023StringDatetimeColumn(Rule):
    rule_id = "R-023"
    name = "string_datetime_column_to_date"
    tier = "1B"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _CREATE_TABLE_RE.search(sql):
            return None
        for m in _STRING_COL_RE.finditer(sql):
            column = m.group(1)
            if _is_datetime_name(column):
                return Finding(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    tier=self.tier,
                    severity="low",
                    description=(
                        f"Колонка '{column}' объявлена как String, "
                        "но по имени предположительно хранит дату или время. "
                        "Числовые типы дат сжимаются Delta-кодеком и допускают date-функции напрямую."
                    ),
                    suggestion=(
                        f"Замените String на Date (если только дата) или DateTime "
                        f"(если дата и время) для колонки '{column}'. "
                        "Проверьте реальный формат значений."
                    ),
                    example_before=f"CREATE TABLE t ({column} String) ENGINE = MergeTree ORDER BY {column}",
                    example_after=f"CREATE TABLE t ({column} DateTime) ENGINE = MergeTree ORDER BY {column}",
                    explain_why=(
                        "String хранит дату как UTF-8 (~10-19 байт). "
                        "Date — 2 байта, DateTime — 4 байта. "
                        "Числовые типы поддерживают Delta-сжатие и range-индексацию."
                    ),
                    confidence="advisory",
                    ch_version_introduced=self.ch_version_introduced,
                )
        return None
