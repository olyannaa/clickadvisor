from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R011HavingToWhere(Rule):
    rule_id = "R-011"
    name = "having_without_aggregate_to_where"
    tier = "1C"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        ast = self.parser.parse(context.sql)
        predicates = self.parser.get_having_without_agg_predicates(ast)
        if not predicates:
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description="В HAVING найдено условие без агрегатных функций.",
            suggestion=f"Перенесите условие в WHERE: {predicates[0]}.",
            example_before="... GROUP BY user_id HAVING country = 'RU' AND COUNT(*) > 100",
            example_after="... WHERE country = 'RU' GROUP BY user_id HAVING COUNT(*) > 100",
            explain_why="Неагрегатные условия выгоднее применять до GROUP BY, а не после агрегации.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
