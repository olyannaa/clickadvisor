from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R013_length_to_empty import R013LengthToEmpty


def test_r013_matches_length_zero_check() -> None:
    rule = R013LengthToEmpty()
    finding = rule.check(QueryContext(sql="SELECT * FROM comments WHERE length(body) > 0"))
    assert finding is not None
    assert finding.rule_id == "R-013"


def test_r013_does_not_match_other_numeric_filter() -> None:
    rule = R013LengthToEmpty()
    finding = rule.check(QueryContext(sql="SELECT * FROM comments WHERE score > 0"))
    assert finding is None
