from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_CREATE_TABLE_RE = re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE)
_INT8_COL_RE = re.compile(
    r"`?(\w+)`?\s+(UInt8|Int8)\b",
    re.IGNORECASE,
)
_BOOL_PREFIXES = ("is_", "has_", "can_", "was_", "did_", "should_", "will_",
                  "allow_", "enable_", "disable_")
_BOOL_EXACT = frozenset(
    ["flag", "enabled", "disabled", "active", "inactive", "deleted", "archived",
     "published", "visible", "hidden", "locked", "verified", "confirmed",
     "approved", "rejected", "paid", "free", "premium", "suspended"]
)


def _is_boolean_name(name: str) -> bool:
    low = name.lower()
    if low in _BOOL_EXACT:
        return True
    return any(low.startswith(p) for p in _BOOL_PREFIXES)


class R032Int8BooleanColumn(Rule):
    rule_id = "R-032"
    name = "int8_boolean_column_to_bool"
    tier = "1B"
    ch_version_introduced = "22.1"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _CREATE_TABLE_RE.search(sql):
            return None
        for m in _INT8_COL_RE.finditer(sql):
            column = m.group(1)
            col_type = m.group(2)
            if _is_boolean_name(column):
                return Finding(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    tier=self.tier,
                    severity="low",
                    description=(
                        f"Колонка '{column}' объявлена как {col_type}, "
                        "но по имени предположительно хранит булево значение. "
                        "Тип Bool хранится идентично UInt8 (1 байт), "
                        "но документирует домен явно."
                    ),
                    suggestion=(
                        f"Замените {col_type} на Bool для '{column}'. "
                        "Требует CH >= 22.1. "
                        "Убедитесь, что значения только 0 и 1."
                    ),
                    example_before=f"CREATE TABLE t ({column} {col_type}) ENGINE = MergeTree ORDER BY tuple()",
                    example_after=f"CREATE TABLE t ({column} Bool) ENGINE = MergeTree ORDER BY tuple()",
                    explain_why=(
                        "Bool хранится как UInt8 (1 байт). "
                        "Замена семантически нейтральна для хранения, "
                        "но добавляет явное документирование домена в схеме."
                    ),
                    confidence="advisory",
                    ch_version_introduced=self.ch_version_introduced,
                )
        return None
