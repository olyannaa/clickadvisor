from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R015_distinct_after_groupby import R015DistinctAfterGroupBy


def test_r015_matches_distinct_after_groupby() -> None:
    rule = R015DistinctAfterGroupBy()
    finding = rule.check(
        QueryContext(
            sql="SELECT DISTINCT a, b FROM (SELECT a, b, COUNT(*) AS cnt FROM events GROUP BY a, b)"
        )
    )
    assert finding is not None
    assert finding.rule_id == "R-015"


def test_r015_does_not_match_different_projection() -> None:
    rule = R015DistinctAfterGroupBy()
    finding = rule.check(
        QueryContext(
            sql="SELECT DISTINCT a FROM (SELECT a, b, COUNT(*) AS cnt FROM events GROUP BY a, b)"
        )
    )
    assert finding is None
