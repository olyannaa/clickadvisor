from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_CREATE_TABLE_RE = re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE)
# Matches PARTITION BY <expression>
_PARTITION_BY_RE = re.compile(
    r"\bPARTITION\s+BY\s+([^\n]+?)(?=\s*(?:ORDER\s+BY|PRIMARY\s+KEY|SETTINGS|ENGINE|\Z))",
    re.IGNORECASE | re.DOTALL,
)
# Date functions that are acceptable as PARTITION BY
_DATE_FUNCTIONS = frozenset([
    "toyyyymm", "tostartofmonth", "tostartofyear", "tostartofquarter",
    "tostartofweek", "tostartofday", "toyear", "todate", "todate32",
    "tostartofinterval",
])


def _has_date_function(expr: str) -> bool:
    low = expr.lower()
    return any(fn in low for fn in _DATE_FUNCTIONS)


class D020PartitionByNonDate(Rule):
    rule_id = "D-020"
    name = "partition_by_non_date_column"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _CREATE_TABLE_RE.search(sql):
            return None
        m = _PARTITION_BY_RE.search(sql)
        if not m:
            return None
        partition_expr = m.group(1).strip()
        if _has_date_function(partition_expr):
            return None
        # Skip tuple() — no partition
        if re.match(r"tuple\s*\(\s*\)", partition_expr, re.IGNORECASE):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description=(
                f"PARTITION BY '{partition_expr}' использует выражение без date-функции. "
                "Высококардинальные ключи партиционирования приводят к Part Explosion "
                "и деградации INSERT/мерджей."
            ),
            suggestion=(
                "Используйте date-функцию для партиционирования: PARTITION BY toYYYYMM(ts) "
                "или PARTITION BY toStartOfMonth(ts). "
                "Убедитесь, что кардинальность ключа не превышает сотни уникальных значений."
            ),
            example_before=f"PARTITION BY {partition_expr}",
            example_after="PARTITION BY toYYYYMM(ts)",
            explain_why=(
                "Partitioning primarily is a data management feature, not a query optimization tool. "
                "High-cardinality partition key leads to too many parts, "
                "degrading insert performance and merge operations."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )
