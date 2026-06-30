from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R047_position_to_like import R047PositionToLike


def test_r047_triggers_on_position_gt_zero() -> None:
    rule = R047PositionToLike()
    ctx = QueryContext(sql="SELECT * FROM logs WHERE position(message, 'error') > 0")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-047"
    assert "LIKE" in finding.suggestion


def test_r047_no_trigger_on_position_eq_zero() -> None:
    rule = R047PositionToLike()
    ctx = QueryContext(sql="SELECT * FROM logs WHERE position(message, 'error') = 0")
    finding = rule.check(ctx)
    assert finding is None
