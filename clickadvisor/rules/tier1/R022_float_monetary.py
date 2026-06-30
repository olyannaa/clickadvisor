from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_CREATE_TABLE_RE = re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE)
_FLOAT_COL_RE = re.compile(
    r"`?(\w+)`?\s+(Float32|Float64)\b",
    re.IGNORECASE,
)
_MONETARY_PARTS = frozenset(
    ["amount", "price", "cost", "revenue", "fee", "total", "balance", "tax",
     "payment", "charge", "salary", "income", "expense", "profit", "discount",
     "rate", "value"]
)


def _is_monetary_name(name: str) -> bool:
    parts = name.lower().split("_")
    return bool(_MONETARY_PARTS.intersection(parts))


class R022FloatMonetary(Rule):
    rule_id = "R-022"
    name = "float_monetary_column_to_decimal"
    tier = "1B"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _CREATE_TABLE_RE.search(sql):
            return None
        for m in _FLOAT_COL_RE.finditer(sql):
            column = m.group(1)
            col_type = m.group(2)
            if _is_monetary_name(column):
                return Finding(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    tier=self.tier,
                    severity="low",
                    description=(
                        f"Колонка '{column}' объявлена как {col_type}, "
                        "но по имени предположительно хранит монетарное значение. "
                        "Float-арифметика не ассоциативна и даёт неточные финансовые расчёты."
                    ),
                    suggestion=(
                        f"Замените {col_type} на Decimal64(2) для '{column}'. "
                        "Decimal даёт точные результаты для SUM/AVG денежных сумм."
                    ),
                    example_before=f"CREATE TABLE t ({column} {col_type}) ENGINE = MergeTree ORDER BY tuple()",
                    example_after=f"CREATE TABLE t ({column} Decimal64(2)) ENGINE = MergeTree ORDER BY tuple()",
                    explain_why=(
                        "(a + b) - a может не равняться b при Float64 из-за рounding. "
                        "Decimal(p, s) даёт точные целочисленные вычисления со смещённой точкой."
                    ),
                    confidence="advisory",
                    ch_version_introduced=self.ch_version_introduced,
                )
        return None
