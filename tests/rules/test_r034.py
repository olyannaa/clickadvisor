from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R034_min_case_to_minif import R034MinCaseToMinIf


def test_r034_triggers_on_min_case() -> None:
    rule = R034MinCaseToMinIf()
    ctx = QueryContext(
        sql="SELECT MIN(CASE WHEN is_paid THEN amount END) AS min_paid FROM orders"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-034"
    assert "minIf" in finding.suggestion


def test_r034_no_trigger_on_min_without_case() -> None:
    rule = R034MinCaseToMinIf()
    ctx = QueryContext(sql="SELECT MIN(amount) FROM orders WHERE is_paid")
    finding = rule.check(ctx)
    assert finding is None
