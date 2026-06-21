from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R014_groupby_string_hash import R014GroupByStringHash


def test_r014_matches_groupby_candidate() -> None:
    rule = R014GroupByStringHash()
    finding = rule.check(QueryContext(sql="SELECT url, COUNT(*) FROM logs GROUP BY url"))
    assert finding is not None
    assert finding.rule_id == "R-014"


def test_r014_does_not_match_without_groupby() -> None:
    rule = R014GroupByStringHash()
    finding = rule.check(QueryContext(sql="SELECT url FROM logs"))
    assert finding is None
