from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R007_toStartOfInterval_range import R007ToStartOfIntervalRange


def test_r007_matches_tostartofhour() -> None:
    rule = R007ToStartOfIntervalRange()
    finding = rule.check(
        QueryContext(sql="SELECT * FROM logs WHERE toStartOfHour(ts) = '2024-01-15 14:00:00'")
    )
    assert finding is not None
    assert finding.rule_id == "R-007"
    assert "toStartOfHour(ts)" in (finding.example_before or "")
    assert "ts >=" in (finding.example_after or "")


def test_r007_does_not_match_plain_hour_range() -> None:
    rule = R007ToStartOfIntervalRange()
    finding = rule.check(
        QueryContext(
            sql=(
                "SELECT * FROM logs WHERE ts >= '2024-01-15 14:00:00' "
                "AND ts < '2024-01-15 15:00:00'"
            )
        )
    )
    assert finding is None
