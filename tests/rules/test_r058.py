from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R058_extract_day import R058ExtractDayToDayOfMonth


def test_r058_triggers_on_extract_day() -> None:
    rule = R058ExtractDayToDayOfMonth()
    ctx = QueryContext(sql="SELECT EXTRACT(DAY FROM ts) AS day_num FROM events")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-058"
    assert "toDayOfMonth" in finding.suggestion


def test_r058_no_trigger_on_todayofmonth() -> None:
    rule = R058ExtractDayToDayOfMonth()
    ctx = QueryContext(sql="SELECT toDayOfMonth(ts) AS day_num FROM events")
    finding = rule.check(ctx)
    assert finding is None
