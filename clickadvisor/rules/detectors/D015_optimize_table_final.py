from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_OPTIMIZE_FINAL_RE = re.compile(
    r"\bOPTIMIZE\s+TABLE\s+[\w.`\"]+.*?\bFINAL\b",
    re.IGNORECASE | re.DOTALL,
)


class D015OptimizeTableFinal(Rule):
    rule_id = "D-015"
    name = "optimize_table_final"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if not _OPTIMIZE_FINAL_RE.search(context.sql):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description=(
                "OPTIMIZE TABLE ... FINAL перезаписывает все data parts в один, "
                "игнорируя лимиты слияния. На больших таблицах — часы I/O и риск OOM."
            ),
            suggestion=(
                "Используйте FINAL в SELECT вместо OPTIMIZE FINAL: "
                "SELECT ... FROM t FINAL WHERE ... "
                "Не запускайте OPTIMIZE FINAL в продакшене."
            ),
            example_before="OPTIMIZE TABLE events FINAL",
            example_after="SELECT event_id FROM events FINAL WHERE dt >= today() - 7",
            explain_why=(
                "OPTIMIZE FINAL игнорирует max_bytes_to_merge_at_max_space_in_pool "
                "и сливает части в один. Может создать часть в сотни ГБ, "
                "которую невозможно разбить обратно."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
