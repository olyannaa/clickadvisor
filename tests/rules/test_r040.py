from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R040_todate_comparison import R040TodateComparisonToDatetime


def test_r040_triggers_on_todate_gte_date() -> None:
    rule = R040TodateComparisonToDatetime()
    ctx = QueryContext(
        sql="SELECT * FROM events WHERE toDate(ts) >= '2024-01-01'"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-040"
    assert finding.severity == "high"
    assert "ts >=" in finding.suggestion


def test_r040_no_trigger_on_direct_datetime_comparison() -> None:
    rule = R040TodateComparisonToDatetime()
    ctx = QueryContext(
        sql="SELECT * FROM events WHERE ts >= '2024-01-01 00:00:00'"
    )
    finding = rule.check(ctx)
    assert finding is None
