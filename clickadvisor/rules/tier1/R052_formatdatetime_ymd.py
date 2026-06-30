from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_FDATETIME_YMD_RE = re.compile(
    r"\bformatDateTime\s*\(\s*(\w+)\s*,\s*'%Y-%m-%d'\s*\)",
    re.IGNORECASE,
)


class R052FormatDateTimeYMD(Rule):
    rule_id = "R-052"
    name = "formatdatetime_ymd_to_toString"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _FDATETIME_YMD_RE.search(context.sql)
        if not m:
            return None
        col = m.group(1)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=f"formatDateTime({col}, '%Y-%m-%d') заменяется toString(toDate({col})).",
            suggestion=f"Замените на toString(toDate({col}))",
            example_before=f"formatDateTime({col}, '%Y-%m-%d')",
            example_after=f"toString(toDate({col}))",
            explain_why="toString(toDate()) более прямой без overhead парсинга format-строки.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
