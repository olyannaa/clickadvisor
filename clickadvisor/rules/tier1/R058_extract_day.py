from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_EXTRACT_DAY_RE = re.compile(
    r"\bEXTRACT\s*\(\s*DAY\s+FROM\s+(\w+)\s*\)",
    re.IGNORECASE,
)


class R058ExtractDayToDayOfMonth(Rule):
    rule_id = "R-058"
    name = "extract_day_to_todayofmonth"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        match = _EXTRACT_DAY_RE.search(context.sql)
        if not match:
            return None
        column = match.group(1)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=f"EXTRACT(DAY FROM {column}) заменяется toDayOfMonth({column}).",
            suggestion=f"Замените на toDayOfMonth({column})",
            example_before=f"EXTRACT(DAY FROM {column})",
            example_after=f"toDayOfMonth({column})",
            explain_why="Нативные CH-функции более читаемы и идиоматичны.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
