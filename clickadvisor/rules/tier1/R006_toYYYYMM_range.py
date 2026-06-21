from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R006ToYYYYMMRange(Rule):
    rule_id = "R-006"
    name = "toYYYYMM_eq_to_date_range"
    tier = "1A"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        match = self.parser.get_date_part_equality(self.parser.parse(context.sql))
        if match is None:
            return None
        function_name, column, literal = match
        date_range = self.parser.monthly_range_from_literal(function_name, literal)
        example_after: str | None = None
        if date_range is None:
            suggestion = (
                f"Замените {function_name}({column}) = {literal!r} на range-предикат "
                f"по {column} с явными границами периода."
            )
        else:
            start, end = date_range
            suggestion = (
                f"Замените {function_name}({column}) = {literal!r} на "
                f"{column} >= '{start}' AND {column} < '{end}'."
            )
            example_after = (
                f"SELECT * FROM events WHERE {column} >= '{start}' AND {column} < '{end}'"
            )
        example_before = f"SELECT * FROM events WHERE {function_name}({column}) = {literal!r}"
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description="Фильтр вычисляет date-part от колонки и ухудшает sargability.",
            suggestion=suggestion,
            example_before=example_before,
            example_after=example_after,
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
