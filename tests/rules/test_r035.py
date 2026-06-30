from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R035_avg_case_to_avgif import R035AvgCaseToAvgIf


def test_r035_triggers_on_avg_case() -> None:
    rule = R035AvgCaseToAvgIf()
    ctx = QueryContext(
        sql="SELECT AVG(CASE WHEN status = 'paid' THEN amount END) AS avg_paid FROM orders"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-035"
    assert "avgIf" in finding.suggestion


def test_r035_no_trigger_on_avg_without_case() -> None:
    rule = R035AvgCaseToAvgIf()
    ctx = QueryContext(sql="SELECT AVG(amount) FROM orders")
    finding = rule.check(ctx)
    assert finding is None
