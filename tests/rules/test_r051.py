from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R051_date_trunc_to_native import R051DateTruncToNative


def test_r051_triggers_on_date_trunc_day() -> None:
    rule = R051DateTruncToNative()
    ctx = QueryContext(sql="SELECT DATE_TRUNC('day', ts) AS day FROM events")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-051"
    assert "toStartOfDay" in finding.suggestion


def test_r051_no_trigger_on_native_function() -> None:
    rule = R051DateTruncToNative()
    ctx = QueryContext(sql="SELECT toStartOfDay(ts) AS day FROM events")
    finding = rule.check(ctx)
    assert finding is None
