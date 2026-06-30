from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R044_todatetime_todate import R044ToDateTimeToDateToStartOfDay


def test_r044_triggers_on_todatetime_todate() -> None:
    rule = R044ToDateTimeToDateToStartOfDay()
    ctx = QueryContext(
        sql="SELECT toDateTime(toDate(ts)) AS day_start FROM events"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-044"
    assert "toStartOfDay" in finding.suggestion


def test_r044_no_trigger_on_plain_todate() -> None:
    rule = R044ToDateTimeToDateToStartOfDay()
    ctx = QueryContext(sql="SELECT toDate(ts) AS day FROM events")
    finding = rule.check(ctx)
    assert finding is None
