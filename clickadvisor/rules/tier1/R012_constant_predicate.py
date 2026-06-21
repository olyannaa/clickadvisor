from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R012ConstantPredicate(Rule):
    rule_id = "R-012"
    name = "constant_predicate_elimination"
    tier = "1A"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        predicate = self.parser.get_constant_predicate(self.parser.parse(context.sql))
        if predicate is None:
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description="В WHERE найден избыточный константный предикат.",
            suggestion="Константный предикат избыточен, удалите его.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
