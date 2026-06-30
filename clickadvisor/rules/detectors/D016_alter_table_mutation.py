from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_MUTATION_RE = re.compile(
    r"\bALTER\s+TABLE\s+[\w.`\"]+\s+(DELETE|UPDATE)\b",
    re.IGNORECASE,
)


class D016AlterTableMutation(Rule):
    rule_id = "D-016"
    name = "alter_table_mutation"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _MUTATION_RE.search(context.sql)
        if not m:
            return None
        op = m.group(1).upper()
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description=(
                f"ALTER TABLE ... {op} (мутация) перезаписывает весь затронутый data part. "
                "Даже изменение одной строки вызывает перезапись сотен ГБ. "
                "Нельзя откатить после запуска."
            ),
            suggestion=(
                "Для удаления данных используйте lightweight DELETE (CH >= 22.8) "
                "или DROP PARTITION. "
                "Для обновлений рассмотрите ReplacingMergeTree или CollapsingMergeTree."
            ),
            example_before="ALTER TABLE events DELETE WHERE dt < '2023-01-01'",
            example_after="DELETE FROM events WHERE dt < '2023-01-01'  -- CH >= 22.8",
            explain_why=(
                "Мутации в ClickHouse — асинхронные фоновые процессы, перезаписывающие "
                "целые data parts. Продолжают выполняться после рестарта сервера. "
                "При подзапросах (x IN (SELECT ...)) нагрузка на CPU/RAM многократно возрастает."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
