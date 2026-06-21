from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R008RedundantCast(Rule):
    rule_id = "R-008"
    name = "redundant_cast_on_filter_removal"
    tier = "1C"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        match = self.parser.get_redundant_cast(self.parser.parse(context.sql))
        if match is None:
            return None
        column, cast_type = match
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description="Фильтр содержит CAST/toType вокруг колонки.",
            suggestion=(
                f"Если колонка уже имеет тип {cast_type}, CAST избыточен "
                "и блокирует использование primary key index."
            ),
            confidence="conditional",
            ch_version_introduced=self.ch_version_introduced,
        )
