from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R017_subquery_filter_pushdown import R017SubqueryFilterPushdown


def test_r017_matches_simple_filter_pushdown() -> None:
    rule = R017SubqueryFilterPushdown()
    context = QueryContext(
        sql="SELECT * FROM (SELECT * FROM events WHERE status = 'active') WHERE user_id = 42"
    )
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "R-017"


def test_r017_does_not_match_subquery_with_distinct() -> None:
    rule = R017SubqueryFilterPushdown()
    context = QueryContext(
        sql="SELECT * FROM (SELECT DISTINCT user_id FROM events WHERE status = 'active') WHERE user_id = 42"
    )
    finding = rule.check(context)
    assert finding is None
