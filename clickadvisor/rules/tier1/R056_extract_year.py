from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_EXTRACT_RE = re.compile(
    r"\bEXTRACT\s*\(\s*YEAR\s+FROM\s+(\w+)\s*\)",
    re.IGNORECASE,
)


class R056ExtractToNative(Rule):
    rule_id = "R-056"
    name = "extract_year_to_toyear"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _EXTRACT_RE.search(context.sql)
        if not m:
            return None
        col = m.group(1)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=f"EXTRACT(YEAR FROM {col}) заменяется toYear({col}).",
            suggestion=f"Замените на toYear({col})",
            example_before=f"EXTRACT(YEAR FROM {col})",
            example_after=f"toYear({col})",
            explain_why="Нативные CH-функции более читаемы и идиоматичны.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
