from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_DATE_TRUNC_RE = re.compile(
    r"\bDATE_TRUNC\s*\(\s*'(day|hour|month|year|week|quarter)'\s*,\s*(\w+)\s*\)",
    re.IGNORECASE,
)

_UNIT_MAP = {
    "day": "toStartOfDay",
    "hour": "toStartOfHour",
    "month": "toStartOfMonth",
    "year": "toStartOfYear",
    "week": "toStartOfWeek",
    "quarter": "toStartOfQuarter",
}


class R051DateTruncToNative(Rule):
    rule_id = "R-051"
    name = "date_trunc_to_native"
    tier = "1A"
    ch_version_introduced = "21.4"

    def check(self, context: QueryContext) -> Finding | None:
        m = _DATE_TRUNC_RE.search(context.sql)
        if not m:
            return None
        unit, col = m.group(1).lower(), m.group(2)
        native_fn = _UNIT_MAP.get(unit, f"toStartOf{unit.capitalize()}")
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=f"DATE_TRUNC('{unit}', {col}) заменяется {native_fn}({col}).",
            suggestion=f"Замените на {native_fn}({col})",
            example_before=f"DATE_TRUNC('{unit}', {col})",
            example_after=f"{native_fn}({col})",
            explain_why="Нативные CH-функции более явны и идиоматичны.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
