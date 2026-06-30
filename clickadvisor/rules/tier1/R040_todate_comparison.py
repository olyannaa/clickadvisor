from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches toDate(col) OP 'YYYY-MM-DD' where OP is >=, >, <=, <
_TODATE_CMP_RE = re.compile(
    r"\btoDate\s*\(\s*(\w+)\s*\)\s*(>=|>|<=|<)\s*'(\d{4}-\d{2}-\d{2})'",
    re.IGNORECASE,
)


class R040TodateComparisonToDatetime(Rule):
    rule_id = "R-040"
    name = "todate_comparison_to_datetime"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _TODATE_CMP_RE.search(context.sql)
        if not m:
            return None
        col = m.group(1)
        op = m.group(2)
        date = m.group(3)
        suggestion = self._build_suggestion(col, op, date)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description=(
                f"toDate({col}) {op} '{date}' оборачивает колонку в функцию, "
                "запрещая использование sparse primary index для DateTime-колонки."
            ),
            suggestion=suggestion,
            example_before=f"WHERE toDate({col}) {op} '{date}'",
            example_after=suggestion.replace("Замените на ", "WHERE "),
            explain_why=(
                "Применение toDate() к колонке делает predicate не-sargable: "
                "sparse index по DateTime не может быть использован. "
                "Прямое сравнение с DateTime-константой восстанавливает sargability."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )

    def _build_suggestion(self, col: str, op: str, date: str) -> str:
        if op == ">=":
            return f"Замените на {col} >= '{date} 00:00:00'"
        elif op == ">":
            return f"Замените на {col} >= (toDateTime('{date}') + toIntervalDay(1))"
        elif op == "<=":
            return f"Замените на {col} < (toDateTime('{date}') + toIntervalDay(1))"
        elif op == "<":
            return f"Замените на {col} < '{date} 00:00:00'"
        return f"Замените toDate({col}) {op} '{date}' на прямое DateTime-сравнение"
