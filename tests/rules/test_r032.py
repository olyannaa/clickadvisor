from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R032_int8_boolean_column import R032Int8BooleanColumn


def test_r032_triggers_on_uint8_is_active() -> None:
    rule = R032Int8BooleanColumn()
    ctx = QueryContext(
        sql="CREATE TABLE users (user_id UInt64, is_active UInt8) ENGINE = MergeTree ORDER BY user_id"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-032"
    assert "Bool" in finding.suggestion


def test_r032_no_trigger_on_uint8_non_boolean_name() -> None:
    rule = R032Int8BooleanColumn()
    ctx = QueryContext(
        sql="CREATE TABLE events (user_id UInt64, event_count UInt8) ENGINE = MergeTree ORDER BY user_id"
    )
    finding = rule.check(ctx)
    assert finding is None
