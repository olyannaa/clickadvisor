from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R013LengthToEmpty(Rule):
    rule_id = "R-013"
    name = "length_zero_to_empty"
    tier = "1A"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        match = self.parser.get_length_empty_pattern(self.parser.parse(context.sql))
        if match is None:
            return None
        column, operator = match
        if operator == "eq":
            suggestion = f"Замените length({column}) = 0 на empty({column})."
        else:
            suggestion = f"Замените length({column}) {self._op(operator)} 0 на notEmpty({column})."
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description="Проверка length(...) на ноль выражается специализированными string predicates.",
            suggestion=suggestion,
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )

    def _op(self, key: str) -> str:
        return {"gt": ">", "neq": "!="}.get(key, key)
