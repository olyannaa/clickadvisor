from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class D007FinalModifier(Rule):
    rule_id = "D-007"
    name = "final_modifier_usage"
    tier = "detector"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        ast = self.parser.parse(context.sql)
        if not self.parser.has_final_modifier(ast):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description="FINAL мержит parts на лету при чтении — дорогая операция. Альтернативы: argMax/argMin, ReplacingMergeTree.",
            suggestion="Избегайте FINAL в горячих запросах, если можно выразить актуальную строку через модель данных или агрегаты.",
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
