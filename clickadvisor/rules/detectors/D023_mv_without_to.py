from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_MV_RE = re.compile(r"\bCREATE\s+MATERIALIZED\s+VIEW\b", re.IGNORECASE)
_TO_RE = re.compile(r"\bTO\s+\w", re.IGNORECASE)


class D023MVWithoutTo(Rule):
    rule_id = "D-023"
    name = "mv_without_to_clause"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _MV_RE.search(sql):
            return None
        if _TO_RE.search(sql):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                "CREATE MATERIALIZED VIEW без TO создаёт скрытую целевую таблицу .inner.mvname. "
                "Управление схемой, ENGINE и индексами такой таблицы значительно сложнее."
            ),
            suggestion=(
                "Используйте явный TO-синтаксис: сначала создайте target table, "
                "затем CREATE MATERIALIZED VIEW mv TO target AS SELECT ..."
            ),
            example_before="CREATE MATERIALIZED VIEW mv AS SELECT user_id, count() FROM events GROUP BY user_id",
            example_after="CREATE TABLE mv_target ... ENGINE=...; CREATE MATERIALIZED VIEW mv TO mv_target AS ...",
            explain_why=(
                "TO-синтаксис позволяет явно управлять схемой target table: "
                "менять ENGINE, добавлять индексы, делать ALTER без пересоздания MV."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
