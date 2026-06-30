from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R039_length_gte_one_to_notempty import R039LengthGteOneToNotEmpty


def test_r039_triggers_on_length_gte_one() -> None:
    rule = R039LengthGteOneToNotEmpty()
    ctx = QueryContext(sql="SELECT * FROM events WHERE length(tags) >= 1")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-039"
    assert "notEmpty" in finding.suggestion


def test_r039_no_trigger_on_length_gt_zero() -> None:
    rule = R039LengthGteOneToNotEmpty()
    ctx = QueryContext(sql="SELECT * FROM events WHERE length(tags) > 0")
    finding = rule.check(ctx)
    assert finding is None
