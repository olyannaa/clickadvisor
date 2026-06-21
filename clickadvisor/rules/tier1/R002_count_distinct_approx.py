from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R002CountDistinctApprox(Rule):
    rule_id = "R-002"
    name = "count_distinct_to_uniq_approx"
    tier = "1B"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        column = self.parser.get_count_distinct(self.parser.parse(context.sql))
        if column is None:
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description="COUNT(DISTINCT x) допускает advisory-замену на approximate distinct.",
            suggestion=(
                "Для приблизительного подсчёта используйте uniq(x) "
                "(HyperLogLog, погрешность <1%). Требует явного согласия."
            ),
            example_before=f"SELECT COUNT(DISTINCT {column}) FROM events",
            example_after=f"SELECT uniq({column}) FROM events",
            explain_why="uniq даёт более дешёвую approximate-агрегацию ценой небольшой погрешности.",
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
