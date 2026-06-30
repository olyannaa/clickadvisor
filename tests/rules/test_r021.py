from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R021_datetime64_zero import R021DateTime64ZeroToDateTime


def test_r021_triggers_on_datetime64_zero() -> None:
    rule = R021DateTime64ZeroToDateTime()
    ctx = QueryContext(
        sql="CREATE TABLE events (ts DateTime64(0), user_id UInt64) ENGINE = MergeTree ORDER BY ts"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-021"
    assert "DateTime64(0)" in finding.description


def test_r021_no_trigger_on_datetime64_with_precision() -> None:
    rule = R021DateTime64ZeroToDateTime()
    ctx = QueryContext(
        sql="CREATE TABLE events (ts DateTime64(3), user_id UInt64) ENGINE = MergeTree ORDER BY ts"
    )
    finding = rule.check(ctx)
    assert finding is None
