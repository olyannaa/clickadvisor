from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R008_redundant_cast import R008RedundantCast


def test_r008_matches_cast_on_column() -> None:
    rule = R008RedundantCast()
    finding = rule.check(QueryContext(sql="SELECT * FROM users WHERE CAST(user_id AS UInt64) = 12345"))
    assert finding is not None
    assert finding.rule_id == "R-008"


def test_r008_does_not_match_expression_cast() -> None:
    rule = R008RedundantCast()
    finding = rule.check(QueryContext(sql="SELECT * FROM users WHERE CAST(user_id + 1 AS UInt64) = 12345"))
    assert finding is None
