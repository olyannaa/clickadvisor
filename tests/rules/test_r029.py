from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R029_lower_like_to_ilike import R029LowerLikeToILike


def test_r029_triggers_on_lower_like() -> None:
    rule = R029LowerLikeToILike()
    ctx = QueryContext(
        sql="SELECT * FROM logs WHERE lower(message) LIKE '%error%'"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-029"
    assert "ILIKE" in finding.suggestion


def test_r029_no_trigger_on_plain_like() -> None:
    rule = R029LowerLikeToILike()
    ctx = QueryContext(
        sql="SELECT * FROM logs WHERE message LIKE '%error%'"
    )
    finding = rule.check(ctx)
    assert finding is None
