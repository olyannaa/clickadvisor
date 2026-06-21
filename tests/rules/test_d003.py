from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D003_select_star import D003SelectStar


def test_d003_matches_top_level_select_star() -> None:
    rule = D003SelectStar()
    context = QueryContext(sql="SELECT * FROM events WHERE user_id = 5")
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "D-003"


def test_d003_does_not_match_aggregate_without_select_star() -> None:
    rule = D003SelectStar()
    context = QueryContext(sql="SELECT user_id, COUNT(*) FROM events GROUP BY user_id")
    finding = rule.check(context)
    assert finding is None


def test_d003_does_not_match_nested_select_star_only() -> None:
    rule = D003SelectStar()
    context = QueryContext(sql="SELECT COUNT(*) FROM (SELECT * FROM events)")
    finding = rule.check(context)
    assert finding is None
