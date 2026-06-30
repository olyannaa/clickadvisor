from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R026_sum_case_to_countif import R026SumCaseToCountIf


def test_r026_triggers_on_sum_case_one() -> None:
    rule = R026SumCaseToCountIf()
    ctx = QueryContext(
        sql="SELECT SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active_cnt FROM users"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-026"
    assert "countIf" in finding.suggestion


def test_r026_no_trigger_on_sum_col() -> None:
    rule = R026SumCaseToCountIf()
    ctx = QueryContext(
        sql="SELECT SUM(CASE WHEN is_paid THEN amount ELSE 0 END) AS total FROM orders"
    )
    finding = rule.check(ctx)
    assert finding is None
