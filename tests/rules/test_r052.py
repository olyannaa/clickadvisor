from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R052_formatdatetime_ymd import R052FormatDateTimeYMD


def test_r052_triggers_on_formatdatetime_ymd() -> None:
    rule = R052FormatDateTimeYMD()
    ctx = QueryContext(sql="SELECT formatDateTime(ts, '%Y-%m-%d') AS day FROM events")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-052"
    assert "toDate" in finding.suggestion


def test_r052_no_trigger_on_other_format() -> None:
    rule = R052FormatDateTimeYMD()
    ctx = QueryContext(sql="SELECT formatDateTime(ts, '%Y-%m') AS month FROM events")
    finding = rule.check(ctx)
    assert finding is None
