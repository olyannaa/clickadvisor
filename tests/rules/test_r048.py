from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R048_positionci_to_ilike import R048PositionCIToILike


def test_r048_triggers_on_positionci_gt_zero() -> None:
    rule = R048PositionCIToILike()
    ctx = QueryContext(sql="SELECT * FROM logs WHERE positionCaseInsensitive(message, 'error') > 0")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-048"
    assert "ILIKE" in finding.suggestion


def test_r048_no_trigger_on_positionci_eq_zero() -> None:
    rule = R048PositionCIToILike()
    ctx = QueryContext(sql="SELECT * FROM logs WHERE positionCaseInsensitive(message, 'error') = 0")
    finding = rule.check(ctx)
    assert finding is None
