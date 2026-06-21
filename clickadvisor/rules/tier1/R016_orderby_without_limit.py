from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R016OrderByWithoutLimit(Rule):
    rule_id = "R-016"
    name = "nested_orderby_without_limit_removal"
    tier = "1C"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        ast = self.parser.parse(context.sql)
        if self.parser.get_orderby_without_limit_subquery(ast) is None:
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description="Во внутреннем подзапросе есть ORDER BY без LIMIT.",
            suggestion="Уберите ORDER BY из подзапроса, если внешний запрос не зависит от порядка строк.",
            example_before="SELECT COUNT(*) FROM (SELECT * FROM events ORDER BY created_at)",
            example_after="SELECT COUNT(*) FROM events",
            explain_why="Сортировка во внутреннем подзапросе бесполезна, если результат далее не читается как упорядоченный поток.",
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
