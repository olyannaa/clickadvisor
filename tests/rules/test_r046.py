from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R046_not_empty_to_notempty import R046NotEmptyToNotEmpty


def test_r046_triggers_on_not_empty() -> None:
    rule = R046NotEmptyToNotEmpty()
    ctx = QueryContext(sql="SELECT * FROM events WHERE NOT empty(message)")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-046"
    assert "notEmpty" in finding.suggestion


def test_r046_no_trigger_on_notempty() -> None:
    rule = R046NotEmptyToNotEmpty()
    ctx = QueryContext(sql="SELECT * FROM events WHERE notEmpty(message)")
    finding = rule.check(ctx)
    assert finding is None
