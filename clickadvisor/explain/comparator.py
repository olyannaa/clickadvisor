from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from clickadvisor.explain.parser import EstimateResult


class EstimateProvider(Protocol):
    def estimate(self, sql: str) -> EstimateResult | None: ...


@dataclass(slots=True)
class ImpactEstimate:
    before: EstimateResult
    after: EstimateResult
    rows_reduction_factor: float
    marks_reduction_factor: float
    rows_reduction_pct: float

    def has_significant_improvement(self) -> bool:
        return self.rows_reduction_factor >= 2.0

    def format_summary(self) -> str:
        if self.rows_reduction_factor >= 1000:
            factor_str = f"{self.rows_reduction_factor:.0f}×"
        elif self.rows_reduction_factor >= 10:
            factor_str = f"{self.rows_reduction_factor:.0f}×"
        else:
            factor_str = f"{self.rows_reduction_factor:.1f}×"

        return (
            f"Строк до: {self.before.rows:,} | "
            f"после: {self.after.rows:,} | "
            f"сокращение: {factor_str} "
            f"(оценка планировщика CH)"
        )


class ExplainComparator:
    def __init__(self, estimator: EstimateProvider) -> None:
        self.estimator = estimator

    def compare(self, original_sql: str, rewritten_sql: str) -> ImpactEstimate | None:
        """
        Сравнивает EXPLAIN ESTIMATE для оригинального и переписанного SQL.
        """
        before = self.estimator.estimate(original_sql)
        if before is None or before.is_empty():
            return None

        after = self.estimator.estimate(rewritten_sql)
        if after is None or after.is_empty():
            return None

        if after.rows == 0:
            return None

        rows_factor = before.rows / after.rows
        marks_factor = before.marks / after.marks if after.marks > 0 else 1.0
        rows_pct = (1 - after.rows / before.rows) * 100

        return ImpactEstimate(
            before=before,
            after=after,
            rows_reduction_factor=rows_factor,
            marks_reduction_factor=marks_factor,
            rows_reduction_pct=rows_pct,
        )
