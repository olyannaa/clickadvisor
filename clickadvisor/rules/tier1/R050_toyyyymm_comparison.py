from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches toYYYYMM(col) OP YYYYMM_literal (6-digit number)
_TOYYYYMM_CMP_RE = re.compile(
    r"\btoYYYYMM\s*\(\s*(\w+)\s*\)\s*(>=|>|<=|<)\s*(\d{6})\b",
    re.IGNORECASE,
)


def _yyyymm_to_date(yyyymm: str) -> str:
    return f"{yyyymm[:4]}-{yyyymm[4:6]}-01"


class R050ToYYYYMMComparison(Rule):
    rule_id = "R-050"
    name = "toyyyymm_comparison_to_range"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        m = _TOYYYYMM_CMP_RE.search(context.sql)
        if not m:
            return None
        col, op, yyyymm = m.group(1), m.group(2), m.group(3)
        date_str = _yyyymm_to_date(yyyymm)
        suggestion = self._build_suggestion(col, op, date_str, yyyymm)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description=(
                f"toYYYYMM({col}) {op} {yyyymm} оборачивает колонку в функцию, "
                "запрещая использование sparse primary index."
            ),
            suggestion=suggestion,
            example_before=f"WHERE toYYYYMM({col}) {op} {yyyymm}",
            example_after=suggestion.replace("Замените на ", "WHERE "),
            explain_why=(
                "Применение toYYYYMM() к колонке делает predicate не-sargable. "
                "Прямое сравнение с DateTime-константой восстанавливает sargability."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )

    def _build_suggestion(self, col: str, op: str, date_str: str, yyyymm: str) -> str:
        if op == ">=":
            return f"Замените на {col} >= '{date_str} 00:00:00'"
        elif op == ">":
            yr, mo = int(yyyymm[:4]), int(yyyymm[4:6])
            mo += 1
            if mo > 12:
                mo, yr = 1, yr + 1
            return f"Замените на {col} >= '{yr}-{mo:02d}-01 00:00:00'"
        elif op == "<=":
            yr, mo = int(yyyymm[:4]), int(yyyymm[4:6])
            mo += 1
            if mo > 12:
                mo, yr = 1, yr + 1
            return f"Замените на {col} < '{yr}-{mo:02d}-01 00:00:00'"
        elif op == "<":
            return f"Замените на {col} < '{date_str} 00:00:00'"
        return f"Замените toYYYYMM({col}) {op} {yyyymm} на прямое сравнение"
