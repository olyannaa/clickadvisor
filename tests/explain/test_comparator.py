from __future__ import annotations

from clickadvisor.explain.comparator import ExplainComparator
from clickadvisor.explain.parser import EstimateResult


class FakeEstimator:
    def __init__(self, estimates: list[EstimateResult | None]) -> None:
        self.estimates = estimates

    def estimate(self, sql: str) -> EstimateResult | None:
        return self.estimates.pop(0)


def test_compare_computes_reduction_factors() -> None:
    comparator = ExplainComparator(
        FakeEstimator(
            [
                EstimateResult(rows=1000, marks=100),
                EstimateResult(rows=10, marks=5),
            ]
        )
    )

    impact = comparator.compare("SELECT before", "SELECT after")

    assert impact is not None
    assert impact.rows_reduction_factor == 100.0
    assert impact.marks_reduction_factor == 20.0
    assert impact.rows_reduction_pct == 99.0


def test_compare_returns_none_when_after_rows_is_zero() -> None:
    comparator = ExplainComparator(
        FakeEstimator(
            [
                EstimateResult(rows=1000, marks=100),
                EstimateResult(rows=0, marks=5),
            ]
        )
    )

    assert comparator.compare("SELECT before", "SELECT after") is None
