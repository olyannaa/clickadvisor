from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class D003SelectStar(Rule):
    rule_id = "D-003"
    name = "select_star_on_wide_table"
    tier = "detector"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        ast = self.parser.parse(context.sql)
        if not self.parser.has_top_level_select_star(ast):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description=(
                "SELECT * читает все колонки с диска. "
                "ClickHouse columnar — укажите нужные колонки явно."
            ),
            suggestion="Замените SELECT * на явный список нужных колонок.",
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
