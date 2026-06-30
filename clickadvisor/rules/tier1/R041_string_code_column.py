from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_CREATE_TABLE_RE = re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE)
_STRING_COL_RE = re.compile(r"`?(\w+)`?\s+String\b", re.IGNORECASE)

_CODE_SUFFIXES = ("_code", "_iso", "_abbr", "_abbreviation")
_CODE_EXACT = frozenset(
    ["country_code", "currency_code", "language_code", "lang_code",
     "iso_code", "currency", "country", "lang", "region_code",
     "state_code", "status_code", "error_code"]
)


def _is_fixed_code_name(name: str) -> bool:
    low = name.lower()
    if low in _CODE_EXACT:
        return True
    return any(low.endswith(s) for s in _CODE_SUFFIXES)


class R041StringCodeColumn(Rule):
    rule_id = "R-041"
    name = "string_code_column_to_fixedstring"
    tier = "1B"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _CREATE_TABLE_RE.search(sql):
            return None
        for m in _STRING_COL_RE.finditer(sql):
            column = m.group(1)
            if _is_fixed_code_name(column):
                return Finding(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    tier=self.tier,
                    severity="low",
                    description=(
                        f"Колонка '{column}' объявлена как String, "
                        "но по имени предположительно хранит код фиксированной длины. "
                        "FixedString(N) хранит без length-prefix, эффективнее для фиксированных кодов."
                    ),
                    suggestion=(
                        f"Проверьте длину значений: "
                        f"country_code → FixedString(2), currency_code → FixedString(3). "
                        f"Замените String на FixedString(N) для '{column}'."
                    ),
                    example_before=f"CREATE TABLE t ({column} String) ENGINE = MergeTree ORDER BY tuple()",
                    example_after=f"CREATE TABLE t ({column} FixedString(2)) ENGINE = MergeTree ORDER BY tuple()",
                    explain_why=(
                        "FixedString(N) хранит ровно N байт без prefix длины. "
                        "Для ISO-кодов (2-3 символа) это ~30% экономия хранилища."
                    ),
                    confidence="advisory",
                    ch_version_introduced=self.ch_version_introduced,
                )
        return None
