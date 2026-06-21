from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R001CountDistinct(Rule):
    rule_id = "R-001"
    name = "count_distinct_to_uniqExact"
    tier = "1A"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        ast = self.parser.parse(context.sql)
        if not self.parser.has_count_distinct(ast):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description="Обнаружен COUNT(DISTINCT x), который в ClickHouse лучше выражать через специализированный агрегат.",
            suggestion="Замените COUNT(DISTINCT x) на uniqExact(x).",
            example_before="SELECT COUNT(DISTINCT user_id) FROM events",
            example_after="SELECT uniqExact(user_id) FROM events",
            explain_why="ClickHouse имеет специализированный exact distinct-агрегат, который лучше соответствует этой задаче.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
