from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_MV_POPULATE_RE = re.compile(
    r"\bCREATE\s+MATERIALIZED\s+VIEW\b.*?\bPOPULATE\b",
    re.IGNORECASE | re.DOTALL,
)


class D024MVWithPopulate(Rule):
    rule_id = "D-024"
    name = "mv_with_populate"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if not _MV_POPULATE_RE.search(context.sql):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description=(
                "CREATE MATERIALIZED VIEW ... POPULATE создаёт окно потери данных: "
                "строки, вставленные ВО ВРЕМЯ backfill-а, не попадут в MV. "
                "POPULATE не атомарен."
            ),
            suggestion=(
                "Создайте MV без POPULATE, затем вручную залейте исторические данные: "
                "INSERT INTO target SELECT ... FROM source."
            ),
            example_before="CREATE MATERIALIZED VIEW mv TO target AS SELECT ... FROM src POPULATE",
            example_after=(
                "CREATE MATERIALIZED VIEW mv TO target AS SELECT ... FROM src;\n"
                "-- Затем: INSERT INTO target SELECT ... FROM src"
            ),
            explain_why=(
                "POPULATE читает данные из источника в фоне и одновременно "
                "начинает триггериться на новые INSERT. "
                "Данные, вставленные ВО ВРЕМЯ backfill-а, теряются."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
