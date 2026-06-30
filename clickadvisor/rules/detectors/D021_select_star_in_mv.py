from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches CREATE MATERIALIZED VIEW ... AS SELECT *
_MV_SELECT_STAR_RE = re.compile(
    r"\bCREATE\s+MATERIALIZED\s+VIEW\b.*?\bAS\s+SELECT\s+\*",
    re.IGNORECASE | re.DOTALL,
)


class D021SelectStarInMV(Rule):
    rule_id = "D-021"
    name = "select_star_in_mv_create"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if not _MV_SELECT_STAR_RE.search(context.sql):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description=(
                "CREATE MATERIALIZED VIEW использует SELECT *, что делает MV хрупким: "
                "изменения схемы источника (добавление/удаление столбца) сломают MV."
            ),
            suggestion=(
                "Замените SELECT * на явный список нужных колонок. "
                "Используйте MIN набор колонок для целевой агрегации."
            ),
            example_before="CREATE MATERIALIZED VIEW mv AS SELECT * FROM source",
            example_after="CREATE MATERIALIZED VIEW mv AS SELECT user_id, count() AS cnt FROM source GROUP BY user_id",
            explain_why=(
                "SELECT * в MV фиксирует список столбцов на момент создания. "
                "Новые столбцы источника не попадут в MV; "
                "удалённые столбцы сломают MV при следующем INSERT."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
