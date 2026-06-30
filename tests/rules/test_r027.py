from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R027_sum_case_col_to_sumif import R027SumCaseColToSumIf


def test_r027_triggers_on_sum_case_col() -> None:
    rule = R027SumCaseColToSumIf()
    ctx = QueryContext(
        sql="SELECT SUM(CASE WHEN is_paid THEN amount ELSE 0 END) AS paid_total FROM orders"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-027"
    assert "sumIf" in finding.suggestion


def test_r027_no_trigger_on_sum_without_case() -> None:
    rule = R027SumCaseColToSumIf()
    ctx = QueryContext(sql="SELECT SUM(amount) FROM orders")
    finding = rule.check(ctx)
    assert finding is None
