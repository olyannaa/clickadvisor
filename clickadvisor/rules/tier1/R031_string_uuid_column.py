from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_CREATE_TABLE_RE = re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE)
_STRING_COL_RE = re.compile(
    r"`?(\w+)`?\s+String\b",
    re.IGNORECASE,
)
_UUID_NAME_PARTS = frozenset(["uuid", "guid", "uid"])
_UUID_EXACT_SUFFIXES = ("_uuid", "_guid", "_uid")
_UUID_COLUMN_NAMES = frozenset(
    ["trace_id", "span_id", "request_id", "correlation_id",
     "uuid", "guid", "uid", "object_id"]
)


def _is_uuid_name(name: str) -> bool:
    low = name.lower()
    if low in _UUID_COLUMN_NAMES:
        return True
    if any(low.endswith(s) for s in _UUID_EXACT_SUFFIXES):
        return True
    parts = set(low.split("_"))
    return bool(_UUID_NAME_PARTS.intersection(parts))


class R031StringUUIDColumn(Rule):
    rule_id = "R-031"
    name = "string_uuid_column_to_uuid_type"
    tier = "1B"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _CREATE_TABLE_RE.search(sql):
            return None
        for m in _STRING_COL_RE.finditer(sql):
            column = m.group(1)
            if _is_uuid_name(column):
                return Finding(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    tier=self.tier,
                    severity="low",
                    description=(
                        f"Колонка '{column}' объявлена как String, "
                        "но по имени предположительно хранит UUID. "
                        "UUID-тип хранит 16 байт вместо ~36 байт строки с дефисами."
                    ),
                    suggestion=(
                        f"Замените String на UUID для '{column}'. "
                        "Проверьте, что все значения — валидные UUID-строки."
                    ),
                    example_before=f"CREATE TABLE t ({column} String) ENGINE = MergeTree ORDER BY {column}",
                    example_after=f"CREATE TABLE t ({column} UUID) ENGINE = MergeTree ORDER BY {column}",
                    explain_why=(
                        "UUID хранит 128 бит (16 байт) в бинарном виде. "
                        "String UUID занимает ~36 байт. Экономия ~2.25x плюс нативные UUID-функции."
                    ),
                    confidence="advisory",
                    ch_version_introduced=self.ch_version_introduced,
                )
        return None
