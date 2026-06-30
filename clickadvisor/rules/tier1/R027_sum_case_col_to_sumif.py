from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches SUM(CASE WHEN cond THEN col_or_expr ELSE 0 END)
# Does NOT match THEN 1 (handled by R-026)
_SUM_CASE_COL_RE = re.compile(
    r"\bSUM\s*\(\s*CASE\s+WHEN\s+(.+?)\s+THEN\s+((?!1\b)[^\s][^)]+?)\s+ELSE\s+0\s*END\s*\)",
    re.IGNORECASE | re.DOTALL,
)


class R027SumCaseColToSumIf(Rule):
    rule_id = "R-027"
    name = "sum_case_col_to_sumif"
    tier = "1A"
    ch_version_introduced = "1.23"

    def check(self, context: QueryContext) -> Finding | None:
        m = _SUM_CASE_COL_RE.search(context.sql)
        if not m:
            return None
        cond = m.group(1).strip()
        col = m.group(2).strip()
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                "SUM(CASE WHEN cond THEN col ELSE 0 END) эквивалентно "
                "sumIf(col, cond) — встроенному комбинатору ClickHouse."
            ),
            suggestion=f"Замените на sumIf({col}, {cond})",
            example_before=f"SUM(CASE WHEN {cond} THEN {col} ELSE 0 END)",
            example_after=f"sumIf({col}, {cond})",
            explain_why=(
                "sumIf(col, cond) применяет сложение только к строкам где cond=true. "
                "Математически идентично SUM(CASE WHEN ... ELSE 0 END) при ELSE 0."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )
