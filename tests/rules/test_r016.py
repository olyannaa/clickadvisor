from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R016_orderby_without_limit import R016OrderByWithoutLimit


def test_r016_matches_order_by_without_limit_in_subquery() -> None:
    rule = R016OrderByWithoutLimit()
    context = QueryContext(sql="SELECT COUNT(*) FROM (SELECT * FROM events ORDER BY created_at)")
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "R-016"


def test_r016_does_not_match_when_limit_present() -> None:
    rule = R016OrderByWithoutLimit()
    context = QueryContext(
        sql="SELECT COUNT(*) FROM (SELECT * FROM events ORDER BY created_at LIMIT 10)"
    )
    finding = rule.check(context)
    assert finding is None
