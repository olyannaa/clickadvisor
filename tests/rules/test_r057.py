from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R057_extract_month import R057ExtractMonthToMonth


def test_r057_triggers_on_extract_month() -> None:
    rule = R057ExtractMonthToMonth()
    ctx = QueryContext(sql="SELECT EXTRACT(MONTH FROM ts) AS mon FROM events")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-057"
    assert "toMonth" in finding.suggestion


def test_r057_no_trigger_on_tomonth() -> None:
    rule = R057ExtractMonthToMonth()
    ctx = QueryContext(sql="SELECT toMonth(ts) AS mon FROM events")
    finding = rule.check(ctx)
    assert finding is None
