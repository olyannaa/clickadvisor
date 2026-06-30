from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_LOW_CARDINALITY_PARTS = frozenset(
    ["type", "status", "category", "flag", "level", "kind", "state", "mode", "priority", "rank", "class"]
)


def _has_low_cardinality_hint(column_name: str) -> bool:
    parts = column_name.lower().split("_")
    return bool(_LOW_CARDINALITY_PARTS.intersection(parts))

_CREATE_TABLE_RE = re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE)
_COLUMN_DEF_RE = re.compile(
    r"`?(\w+)`?\s+(UInt64|Int64)\b",
    re.IGNORECASE,
)


class R019UintNarrowing(Rule):
    rule_id = "R-019"
    name = "oversized_uint_type_narrowing"
    tier = "1B"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _CREATE_TABLE_RE.search(sql):
            return None

        for match in _COLUMN_DEF_RE.finditer(sql):
            column_name = match.group(1)
            col_type = match.group(2)
            if _has_low_cardinality_hint(column_name):
                return Finding(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    tier=self.tier,
                    severity="low",
                    description=(
                        f"Колонка '{column_name}' объявлена как {col_type}, "
                        "но по имени предполагается низкокардинальный домен. "
                        "Эвристика — требует проверки реального диапазона данных перед применением."
                    ),
                    suggestion=(
                        f"Проверьте MAX({column_name}) в таблице. "
                        "Если значения укладываются в UInt8 (0–255) или UInt16 (0–65535), "
                        "замените тип для экономии памяти и ускорения GROUP BY."
                    ),
                    example_before=f"CREATE TABLE t ({column_name} {col_type}) ENGINE = MergeTree();",
                    example_after=f"CREATE TABLE t ({column_name} UInt8) ENGINE = MergeTree();",
                    explain_why=(
                        "UInt8/UInt16/UInt32 занимают в 8/4/2 раза меньше памяти, чем UInt64. "
                        "ClickHouse хранит данные побlocно — меньший тип = меньше чтений с диска."
                    ),
                    confidence="advisory",
                    ch_version_introduced=self.ch_version_introduced,
                )
        return None
