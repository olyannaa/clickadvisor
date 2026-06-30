from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches toDateTime(toDate(col))
_TODATETIME_TODATE_RE = re.compile(
    r"\btoDateTime\s*\(\s*toDate\s*\(\s*(\w+)\s*\)\s*\)",
    re.IGNORECASE,
)


class R044ToDateTimeToDateToStartOfDay(Rule):
    rule_id = "R-044"
    name = "todatetime_todate_to_startofday"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _TODATETIME_TODATE_RE.search(context.sql)
        if not m:
            return None
        col = m.group(1)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                f"toDateTime(toDate({col})) вычисляет начало дня через двойное преобразование. "
                f"toStartOfDay({col}) — нативная функция для той же операции."
            ),
            suggestion=f"Замените toDateTime(toDate({col})) на toStartOfDay({col})",
            example_before=f"toDateTime(toDate({col}))",
            example_after=f"toStartOfDay({col})",
            explain_why=(
                "toDate(ts) = дата без времени. toDateTime(date) = date + 00:00:00. "
                "toStartOfDay(ts) = ts отсечённый до полуночи текущего дня. Всё это одно."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
