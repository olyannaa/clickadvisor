from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule


class R003QuantileExact(Rule):
    rule_id = "R-003"
    name = "quantileExact_to_quantileTDigest"
    tier = "1B"
    ch_version_introduced = "1.0"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        match = self.parser.get_quantile_exact(self.parser.parse(context.sql))
        if match is None:
            return None
        level, column = match
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description="quantileExact хранит больше состояния и дороже approximate quantile-агрегатов.",
            suggestion=(
                "Для приблизительных квантилей используйте "
                "quantileTDigest(level)(x) — погрешность <0.1%."
            ),
            example_before=f"SELECT quantileExact({level})({column}) FROM requests",
            example_after=f"SELECT quantileTDigest({level})({column}) FROM requests",
            explain_why="TDigest обычно даёт очень близкий результат при заметно меньшей цене.",
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
