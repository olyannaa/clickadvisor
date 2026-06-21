from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R010DisjunctionToIn(Rule):
    rule_id = "R-010"
    name = "disjunction_chain_to_in"
    tier = "1A"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        ast = self.parser.parse(context.sql)
        match = self.parser.get_disjunction_chain(ast)
        if match is None:
            return None

        column, values = match
        suggestion = f"Замените OR-цепочку на IN ({', '.join(values)})."
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description="Обнаружена длинная OR-цепочка равенств по одной и той же колонке.",
            suggestion=suggestion,
            example_before="SELECT * FROM events WHERE country = 'RU' OR country = 'BY' OR country = 'KZ'",
            example_after="SELECT * FROM events WHERE country IN ('RU', 'BY', 'KZ')",
            explain_why="IN выражает тот же смысл короче и даёт движку более каноничную форму фильтра.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
