from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R015DistinctAfterGroupBy(Rule):
    rule_id = "R-015"
    name = "distinct_after_groupby_removal"
    tier = "1A"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        columns = self.parser.get_distinct_after_groupby(self.parser.parse(context.sql))
        if columns is None:
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description="DISTINCT после GROUP BY по тем же колонкам является noop.",
            suggestion="DISTINCT после GROUP BY по тем же колонкам — noop. Удалите DISTINCT.",
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
