from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches COALESCE(arg1, arg2) with exactly 2 arguments (no nested commas at top level)
_COALESCE_TWO_RE = re.compile(
    r"\bCOALESCE\s*\(\s*([^,()]+)\s*,\s*([^,()]+)\s*\)",
    re.IGNORECASE,
)


class R028CoalesceToIfNull(Rule):
    rule_id = "R-028"
    name = "coalesce_two_args_to_ifnull"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _COALESCE_TWO_RE.search(context.sql)
        if not m:
            return None
        arg1 = m.group(1).strip()
        arg2 = m.group(2).strip()
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                f"COALESCE({arg1}, {arg2}) с двумя аргументами полностью эквивалентен "
                f"ifNull({arg1}, {arg2})."
            ),
            suggestion=f"Замените на ifNull({arg1}, {arg2})",
            example_before=f"COALESCE({arg1}, {arg2})",
            example_after=f"ifNull({arg1}, {arg2})",
            explain_why=(
                "ifNull(x, y) — специализированная функция без overhead varargs-перебора. "
                "Семантически идентична COALESCE с двумя аргументами."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
