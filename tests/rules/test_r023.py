from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R023_string_datetime_column import R023StringDatetimeColumn


def test_r023_triggers_on_string_created_at() -> None:
    rule = R023StringDatetimeColumn()
    ctx = QueryContext(
        sql="CREATE TABLE events (user_id UInt64, created_at String) ENGINE = MergeTree ORDER BY user_id"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-023"
    assert "created_at" in finding.description


def test_r023_no_trigger_on_string_name() -> None:
    rule = R023StringDatetimeColumn()
    ctx = QueryContext(
        sql="CREATE TABLE users (user_id UInt64, username String) ENGINE = MergeTree ORDER BY user_id"
    )
    finding = rule.check(ctx)
    assert finding is None
