from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R045_like_without_wildcards import R045LikeWithoutWildcardsToEq


def test_r045_triggers_on_like_without_wildcards() -> None:
    rule = R045LikeWithoutWildcardsToEq()
    ctx = QueryContext(
        sql="SELECT * FROM events WHERE event_type LIKE 'click'"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-045"
    assert "= 'click'" in finding.suggestion


def test_r045_no_trigger_on_like_with_wildcards() -> None:
    rule = R045LikeWithoutWildcardsToEq()
    ctx = QueryContext(
        sql="SELECT * FROM events WHERE event_type LIKE '%click%'"
    )
    finding = rule.check(ctx)
    assert finding is None
