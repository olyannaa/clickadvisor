from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R043_having_count_gt_zero import R043HavingCountGtZero


def test_r043_triggers_on_having_count_gt_zero() -> None:
    rule = R043HavingCountGtZero()
    ctx = QueryContext(
        sql="SELECT user_id, count() FROM events GROUP BY user_id HAVING count() > 0"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-043"
    assert "тавтологи" in finding.description


def test_r043_no_trigger_on_having_count_gt_one() -> None:
    rule = R043HavingCountGtZero()
    ctx = QueryContext(
        sql="SELECT user_id, count() FROM events GROUP BY user_id HAVING count() > 1"
    )
    finding = rule.check(ctx)
    assert finding is None
