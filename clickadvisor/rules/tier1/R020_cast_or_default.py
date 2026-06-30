from __future__ import annotations

import sqlglot.expressions as exp

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.rules.base import Rule

_OR_SAFE_SUFFIXES = ("orzero", "ornull", "ordefault")

_TO_TYPE_PREFIXES = (
    "touint",
    "toint",
    "tofloat",
    "tostring",
    "todecimal",
    "todate",
    "todatetime",
    "tofixedstring",
    "touuid",
)


def _is_safe_variant(name: str) -> bool:
    lower = name.lower()
    return any(lower.endswith(s) for s in _OR_SAFE_SUFFIXES)


def _is_to_type_function(name: str) -> bool:
    lower = name.lower()
    return any(lower.startswith(p) for p in _TO_TYPE_PREFIXES)


class R020CastOrDefault(Rule):
    rule_id = "R-020"
    name = "throwing_cast_to_or_default_cast"
    tier = "1B"
    ch_version_introduced = "21.7"

    def __init__(self, mode: str = "diagnose") -> None:
        super().__init__(mode=mode)
        self.parser = SQLParser()

    def check(self, context: QueryContext) -> Finding | None:
        ast = self.parser.parse(context.sql)

        for cast in ast.find_all(exp.Cast):
            if isinstance(cast.this, exp.Column) and cast.to is not None:
                column = cast.this.sql(dialect="clickhouse")
                target_type = cast.to.sql(dialect="clickhouse")
                return Finding(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    tier=self.tier,
                    severity="medium",
                    description=(
                        f"CAST({column} AS {target_type}) применён к колонке — "
                        "при грязных данных бросит исключение и прервёт запрос."
                    ),
                    suggestion=(
                        f"Используйте accurateCastOrDefault({column}, '{target_type}', <default>) "
                        "и явно выберите значение по умолчанию при ошибке конвертации."
                    ),
                    example_before=f"SELECT CAST({column} AS {target_type}) FROM t",
                    example_after=f"SELECT accurateCastOrDefault({column}, '{target_type}', 0) FROM t",
                    explain_why=(
                        "accurateCastOrDefault возвращает default вместо исключения, "
                        "запрос продолжает выполнение на грязных данных."
                    ),
                    confidence="advisory",
                    ch_version_introduced=self.ch_version_introduced,
                )

        for fn in ast.find_all(exp.Anonymous):
            name = fn.name
            if not _is_to_type_function(name):
                continue
            if _is_safe_variant(name):
                continue
            if not fn.expressions:
                continue
            if not isinstance(fn.expressions[0], exp.Column):
                continue
            column = fn.expressions[0].sql(dialect="clickhouse")
            return Finding(
                rule_id=self.rule_id,
                rule_name=self.name,
                tier=self.tier,
                severity="medium",
                description=(
                    f"{name}({column}) применён к колонке — "
                    "при грязных данных бросит исключение и прервёт запрос."
                ),
                suggestion=(
                    f"Используйте {name}OrDefault({column}) или "
                    f"accurateCastOrDefault({column}, '<Type>', <default>)."
                ),
                example_before=f"SELECT {name}({column}) FROM t",
                example_after=f"SELECT {name}OrDefault({column}) FROM t",
                explain_why=(
                    "OrDefault-варианты возвращают нулевое значение типа вместо исключения."
                ),
                confidence="advisory",
                ch_version_introduced=self.ch_version_introduced,
            )

        return None
