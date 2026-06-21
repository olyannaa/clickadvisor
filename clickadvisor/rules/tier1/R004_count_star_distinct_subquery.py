from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R004CountStarDistinctSubquery(Rule):
    rule_id = "R-004"
    name = "count_star_in_distinct_subquery_collapse"
    tier = "1A"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        ast = self.parser.parse(context.sql)
        match = self.parser.get_count_star_distinct_subquery(ast)
        if match is None:
            return None
        column, table = match
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description="Обнаружен двухшаговый паттерн COUNT(*) поверх SELECT DISTINCT.",
            suggestion=f"Замените конструкцию на SELECT uniqExact({column}) FROM {table}.",
            example_before="SELECT COUNT(*) FROM (SELECT DISTINCT user_id FROM events)",
            example_after="SELECT uniqExact(user_id) FROM events",
            explain_why="Distinct-подзапрос и последующий count можно заменить на один специализированный агрегат.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
