from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R017SubqueryFilterPushdown(Rule):
    rule_id = "R-017"
    name = "subquery_filter_pushdown"
    tier = "1A"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        ast = self.parser.parse(context.sql)
        match = self.parser.get_subquery_filter_pushdown(ast)
        if match is None:
            return None
        table_name, inner_predicate, outer_predicate = match
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description="Внешний фильтр можно протолкнуть внутрь простого подзапроса.",
            suggestion=f"Слейте фильтры: SELECT * FROM {table_name} WHERE {inner_predicate} AND {outer_predicate}.",
            example_before="SELECT * FROM (SELECT * FROM events WHERE status = 'active') WHERE user_id = 42",
            example_after="SELECT * FROM events WHERE status = 'active' AND user_id = 42",
            explain_why="Чем раньше применяется фильтр, тем меньше строк проходит через последующие стадии плана.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
