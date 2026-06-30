from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R062_arraycount_zero_to_not_has import R062ArrayCountZeroToNotHas


def test_r062_triggers_on_arraycount_eq_zero() -> None:
    rule = R062ArrayCountZeroToNotHas()
    ctx = QueryContext(
        sql="SELECT * FROM events WHERE arrayCount(x -> x = 'error', tags) = 0"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-062"
    assert "NOT has" in finding.suggestion


def test_r062_no_trigger_on_arraycount_gt_zero() -> None:
    rule = R062ArrayCountZeroToNotHas()
    ctx = QueryContext(
        sql="SELECT * FROM events WHERE arrayCount(x -> x = 'error', tags) > 0"
    )
    finding = rule.check(ctx)
    assert finding is None
