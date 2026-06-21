from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R009InSingleton(Rule):
    rule_id = "R-009"
    name = "in_singleton_to_equality"
    tier = "1A"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        match = self.parser.get_in_singleton(self.parser.parse(context.sql))
        if match is None:
            return None
        column, value = match
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description="IN со списком из одного значения можно упростить до equality.",
            suggestion=f"Замените {column} IN ({value}) на {column} = {value}.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
