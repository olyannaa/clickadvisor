from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D004_missing_limit import D004MissingLimit


def test_d004_matches_select_without_limit_and_without_top_level_agg() -> None:
    rule = D004MissingLimit()
    finding = rule.check(
        QueryContext(sql="SELECT user_id, event_type, created_at FROM events WHERE status = 'active'")
    )
    assert finding is not None
    assert finding.rule_id == "D-004"


def test_d004_does_not_match_top_level_aggregate() -> None:
    rule = D004MissingLimit()
    finding = rule.check(QueryContext(sql="SELECT COUNT(*) FROM events"))
    assert finding is None
