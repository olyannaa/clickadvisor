from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_EXTRACT_HOUR_RE = re.compile(
    r"\bEXTRACT\s*\(\s*HOUR\s+FROM\s+(\w+)\s*\)",
    re.IGNORECASE,
)


class R059ExtractHourToHour(Rule):
    rule_id = "R-059"
    name = "extract_hour_to_tohour"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        match = _EXTRACT_HOUR_RE.search(context.sql)
        if not match:
            return None
        column = match.group(1)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=f"EXTRACT(HOUR FROM {column}) заменяется toHour({column}).",
            suggestion=f"Замените на toHour({column})",
            example_before=f"EXTRACT(HOUR FROM {column})",
            example_after=f"toHour({column})",
            explain_why="Нативные CH-функции более читаемы и идиоматичны.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
