from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R006_toYYYYMM_range import R006ToYYYYMMRange


def test_r006_matches_toyyyymm() -> None:
    rule = R006ToYYYYMMRange()
    finding = rule.check(
        QueryContext(sql="SELECT * FROM events WHERE toYYYYMM(event_date) = 202401")
    )
    assert finding is not None
    assert finding.rule_id == "R-006"
    assert "toYYYYMM(event_date)" in (finding.example_before or "")
    assert "event_date >=" in (finding.example_after or "")


def test_r006_does_not_match_plain_range() -> None:
    rule = R006ToYYYYMMRange()
    finding = rule.check(
        QueryContext(
            sql=(
                "SELECT * FROM events WHERE event_date >= '2024-01-01' "
                "AND event_date < '2024-02-01'"
            )
        )
    )
    assert finding is None
