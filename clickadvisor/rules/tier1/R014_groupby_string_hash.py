from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R014GroupByStringHash(Rule):
    rule_id = "R-014"
    name = "groupby_long_string_to_hash"
    tier = "1B"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        column = self.parser.get_groupby_string_candidate(self.parser.parse(context.sql))
        if column is None:
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description="GROUP BY по колонке-кандидату на длинную строку может быть дорогим.",
            suggestion=(
                f"Если колонка {column} длинная строка (>20 символов), "
                "GROUP BY cityHash64(col) с any(col) в SELECT даёт 5-10× ускорение. "
                "Проверьте тип колонки."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
