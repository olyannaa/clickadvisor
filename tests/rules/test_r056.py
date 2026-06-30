from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R056_extract_year import R056ExtractToNative


def test_r056_triggers_on_extract_year() -> None:
    rule = R056ExtractToNative()
    ctx = QueryContext(sql="SELECT EXTRACT(YEAR FROM ts) AS yr FROM events")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-056"
    assert "toYear" in finding.suggestion


def test_r056_does_not_trigger_on_extract_month() -> None:
    rule = R056ExtractToNative()
    ctx = QueryContext(sql="SELECT EXTRACT(MONTH FROM ts) AS mon FROM events")
    finding = rule.check(ctx)
    assert finding is None


def test_r056_no_trigger_on_toyear() -> None:
    rule = R056ExtractToNative()
    ctx = QueryContext(sql="SELECT toYear(ts) AS yr FROM events")
    finding = rule.check(ctx)
    assert finding is None
