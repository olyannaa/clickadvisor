from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_MV_RE = re.compile(r"\bCREATE\s+MATERIALIZED\s+VIEW\b", re.IGNORECASE)
_JOIN_IN_BODY_RE = re.compile(r"\b(?:INNER|LEFT|RIGHT|FULL|CROSS)?\s*JOIN\b", re.IGNORECASE)


class D025MVWithJoin(Rule):
    rule_id = "D-025"
    name = "mv_with_join_in_select"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _MV_RE.search(sql):
            return None
        if not _JOIN_IN_BODY_RE.search(sql):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description=(
                "CREATE MATERIALIZED VIEW содержит JOIN в SELECT. "
                "При каждом INSERT в левую таблицу выполняется JOIN со всей правой таблицей. "
                "Это критически бьёт по производительности вставки."
            ),
            suggestion=(
                "Рассмотрите использование Dictionary, engine=Join или engine=Set для правой таблицы. "
                "Они хранятся в памяти и выполняют lookup намного быстрее полного JOIN-а."
            ),
            example_before="CREATE MATERIALIZED VIEW mv TO t AS SELECT e.uid, u.name FROM events e LEFT JOIN users u ON e.uid = u.uid",
            example_after="CREATE MATERIALIZED VIEW mv TO t AS SELECT uid, dictGet('users_dict', 'name', uid) FROM events",
            explain_why=(
                "MV срабатывает как AFTER INSERT TRIGGER на левую таблицу. "
                "JOIN выполняется со ВСЕЙ правой таблицей при каждом INSERT-е, "
                "что может увеличить latency вставки в разы."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
