from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class D004MissingLimit(Rule):
    rule_id = "D-004"
    name = "missing_limit_on_unbounded_result"
    tier = "detector"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        if not self.parser.has_missing_limit(self.parser.parse(context.sql)):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description="Запрос может вернуть неограниченное число строк.",
            suggestion=(
                "Запрос может вернуть неограниченное число строк. "
                "Добавьте LIMIT или убедитесь что это намеренно."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
