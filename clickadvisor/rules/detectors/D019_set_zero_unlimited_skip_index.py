from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_SET_ZERO_RE = re.compile(
    r"\bINDEX\s+(\w+)\s+.*?\bTYPE\s+set\s*\(\s*0\s*\)",
    re.IGNORECASE | re.DOTALL,
)


class D019SetZeroUnlimitedSkipIndex(Rule):
    rule_id = "D-019"
    name = "set_zero_unlimited_skip_index"
    tier = "detector"
    ch_version_introduced = "0.720"

    def check(self, context: QueryContext) -> Finding | None:
        m = _SET_ZERO_RE.search(context.sql)
        if not m:
            return None
        index_name = m.group(1)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                f"Skip index '{index_name}' использует TYPE set(0) — неограниченный размер набора. "
                "На высококардинальных колонках индекс не сможет пропускать блоки "
                "и только замедлит слияния."
            ),
            suggestion=(
                f"Задайте явный лимит: INDEX {index_name} <column> TYPE set(100) GRANULARITY 4. "
                "Используйте set(N) только для колонок с малым числом уникальных значений в грануле."
            ),
            example_before=f"INDEX {index_name} status TYPE set(0) GRANULARITY 4",
            example_after=f"INDEX {index_name} status TYPE set(100) GRANULARITY 4",
            explain_why=(
                "set(0) означает неограниченный размер набора на гранулу. "
                "При высокой кардинальности набор содержит все значения "
                "и не может пропустить ни один блок, тратя память при слияниях."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
