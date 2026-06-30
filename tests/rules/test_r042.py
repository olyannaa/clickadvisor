from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R042_grouparray_no_limit import R042GroupArrayNoLimit


def test_r042_triggers_on_grouparray_without_limit() -> None:
    rule = R042GroupArrayNoLimit()
    ctx = QueryContext(
        sql="SELECT user_id, groupArray(event_type) AS events FROM log GROUP BY user_id"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-042"
    assert "1000" in finding.suggestion


def test_r042_no_trigger_on_grouparray_with_limit() -> None:
    rule = R042GroupArrayNoLimit()
    ctx = QueryContext(
        sql="SELECT user_id, groupArray(1000)(event_type) AS events FROM log GROUP BY user_id"
    )
    finding = rule.check(ctx)
    assert finding is None
