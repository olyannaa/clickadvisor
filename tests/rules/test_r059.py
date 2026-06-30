from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R059_extract_hour import R059ExtractHourToHour


def test_r059_triggers_on_extract_hour() -> None:
    rule = R059ExtractHourToHour()
    ctx = QueryContext(sql="SELECT EXTRACT(HOUR FROM ts) AS hr FROM events")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-059"
    assert "toHour" in finding.suggestion


def test_r059_no_trigger_on_tohour() -> None:
    rule = R059ExtractHourToHour()
    ctx = QueryContext(sql="SELECT toHour(ts) AS hr FROM events")
    finding = rule.check(ctx)
    assert finding is None
