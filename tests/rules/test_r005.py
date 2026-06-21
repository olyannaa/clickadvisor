from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R005_todate_equality import R005ToDateEquality


def test_r005_matches_todate_equality() -> None:
    rule = R005ToDateEquality()
    context = QueryContext(sql="SELECT * FROM events WHERE toDate(created_at) = '2024-01-15'")
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "R-005"
    assert "2024-01-16 00:00:00" in finding.suggestion
    assert "toDate(created_at)" in (finding.example_before or "")
    assert "created_at >=" in (finding.example_after or "")


def test_r005_does_not_match_plain_range_predicate() -> None:
    rule = R005ToDateEquality()
    context = QueryContext(
        sql=(
            "SELECT * FROM events WHERE created_at >= '2024-01-15 00:00:00' "
            "AND created_at < '2024-01-16 00:00:00'"
        )
    )
    finding = rule.check(context)
    assert finding is None
