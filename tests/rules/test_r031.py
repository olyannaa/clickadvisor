from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R031_string_uuid_column import R031StringUUIDColumn


def test_r031_triggers_on_string_trace_id() -> None:
    rule = R031StringUUIDColumn()
    ctx = QueryContext(
        sql="CREATE TABLE spans (trace_id String, span_id String, ts DateTime) ENGINE = MergeTree ORDER BY ts"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-031"
    assert "UUID" in finding.suggestion


def test_r031_no_trigger_on_string_name() -> None:
    rule = R031StringUUIDColumn()
    ctx = QueryContext(
        sql="CREATE TABLE users (user_id UInt64, full_name String) ENGINE = MergeTree ORDER BY user_id"
    )
    finding = rule.check(ctx)
    assert finding is None
