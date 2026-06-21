from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R018UnionToUnionAll(Rule):
    rule_id = "R-018"
    name = "union_to_union_all_advisory"
    tier = "1C"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        if not self.parser.has_union_not_all(self.parser.parse(context.sql)):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description="UNION выполняет DISTINCT после объединения наборов.",
            suggestion=(
                "UNION выполняет DISTINCT после объединения. "
                "Если строки заведомо не пересекаются — используйте UNION ALL "
                "(значительно быстрее). Требует подтверждения."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
