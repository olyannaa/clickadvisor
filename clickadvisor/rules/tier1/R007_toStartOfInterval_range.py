from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R007ToStartOfIntervalRange(Rule):
    rule_id = "R-007"
    name = "toStartOfInterval_eq_to_range"
    tier = "1A"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        match = self.parser.get_interval_start_equality(self.parser.parse(context.sql))
        if match is None:
            return None
        function_name, column, literal = match
        interval_range = self.parser.interval_range_from_literal(function_name, literal)
        if interval_range is None:
            return None
        start, end = interval_range
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description="Фильтр по toStartOf* блокирует прямое pruning по исходной колонке.",
            suggestion=(
                f"Замените {function_name}({column}) = '{literal}' на "
                f"{column} >= '{start}' AND {column} < '{end}'."
            ),
            example_before=f"SELECT * FROM logs WHERE {function_name}({column}) = '{literal}'",
            example_after=f"SELECT * FROM logs WHERE {column} >= '{start}' AND {column} < '{end}'",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
