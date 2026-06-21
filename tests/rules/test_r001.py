from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R001_count_distinct import R001CountDistinct


def test_r001_matches_count_distinct() -> None:
    rule = R001CountDistinct()
    context = QueryContext(sql="SELECT COUNT(DISTINCT user_id) FROM events")
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "R-001"


def test_r001_does_not_match_plain_count() -> None:
    rule = R001CountDistinct()
    context = QueryContext(sql="SELECT COUNT(user_id) FROM events")
    finding = rule.check(context)
    assert finding is None
