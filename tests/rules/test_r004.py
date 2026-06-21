from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R004_count_star_distinct_subquery import R004CountStarDistinctSubquery


def test_r004_matches_count_star_over_distinct_subquery() -> None:
    rule = R004CountStarDistinctSubquery()
    context = QueryContext(sql="SELECT COUNT(*) FROM (SELECT DISTINCT user_id FROM events)")
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "R-004"


def test_r004_does_not_match_plain_distinct_select() -> None:
    rule = R004CountStarDistinctSubquery()
    context = QueryContext(sql="SELECT DISTINCT user_id FROM events")
    finding = rule.check(context)
    assert finding is None
