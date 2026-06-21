from __future__ import annotations

from datetime import datetime, timedelta

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R005ToDateEquality(Rule):
    rule_id = "R-005"
    name = "to_date_eq_to_datetime_range"
    tier = "1A"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        ast = self.parser.parse(context.sql)
        match = self.parser.get_todate_equality(ast)
        if match is None:
            return None

        column, date_literal = match
        start = datetime.strptime(date_literal, "%Y-%m-%d")
        end = start + timedelta(days=1)
        suggestion = (
            f"Замените toDate({column}) = '{date_literal}' на "
            f"{column} >= '{start:%Y-%m-%d} 00:00:00' AND "
            f"{column} < '{end:%Y-%m-%d} 00:00:00'."
        )

        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description=(
                "Фильтр оборачивает колонку в toDate(), "
                "из-за чего predicate становится менее sargable."
            ),
            suggestion=suggestion,
            example_before=f"SELECT * FROM events WHERE toDate({column}) = '{date_literal}'",
            example_after=(
                f"SELECT * FROM events WHERE {column} >= '{start:%Y-%m-%d} 00:00:00' "
                f"AND {column} < '{end:%Y-%m-%d} 00:00:00'"
            ),
            explain_why=(
                "Range-предикат по исходной колонке "
                "лучше подходит для pruning в MergeTree."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
