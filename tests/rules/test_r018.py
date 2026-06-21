from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R018_union_to_union_all import R018UnionToUnionAll


def test_r018_matches_union_without_all() -> None:
    rule = R018UnionToUnionAll()
    finding = rule.check(
        QueryContext(sql="SELECT user_id FROM events_2023 UNION SELECT user_id FROM events_2024")
    )
    assert finding is not None
    assert finding.rule_id == "R-018"


def test_r018_does_not_match_union_all() -> None:
    rule = R018UnionToUnionAll()
    finding = rule.check(
        QueryContext(sql="SELECT user_id FROM events_2023 UNION ALL SELECT user_id FROM events_2024")
    )
    assert finding is None
