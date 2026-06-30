from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_EXTRACT_MONTH_RE = re.compile(
    r"\bEXTRACT\s*\(\s*MONTH\s+FROM\s+(\w+)\s*\)",
    re.IGNORECASE,
)


class R057ExtractMonthToMonth(Rule):
    rule_id = "R-057"
    name = "extract_month_to_tomonth"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        match = _EXTRACT_MONTH_RE.search(context.sql)
        if not match:
            return None
        column = match.group(1)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=f"EXTRACT(MONTH FROM {column}) заменяется toMonth({column}).",
            suggestion=f"Замените на toMonth({column})",
            example_before=f"EXTRACT(MONTH FROM {column})",
            example_after=f"toMonth({column})",
            explain_why="Нативные CH-функции более читаемы и идиоматичны.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
