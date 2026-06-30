from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R019_uint_narrowing import R019UintNarrowing


def test_r019_triggers_on_uint64_with_type_in_name() -> None:
    rule = R019UintNarrowing()
    context = QueryContext(
        sql="CREATE TABLE events (event_type UInt64, user_id UInt64) ENGINE = MergeTree() ORDER BY user_id"
    )
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "R-019"
    assert finding.severity == "low"
    assert "реального диапазона данных" in finding.description


def test_r019_triggers_on_int64_with_status_in_name() -> None:
    rule = R019UintNarrowing()
    context = QueryContext(
        sql="CREATE TABLE orders (order_status Int64, amount UInt64) ENGINE = MergeTree() ORDER BY order_status"
    )
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "R-019"


def test_r019_no_trigger_on_uint64_with_neutral_name() -> None:
    rule = R019UintNarrowing()
    context = QueryContext(
        sql="CREATE TABLE payments (amount UInt64) ENGINE = MergeTree() ORDER BY amount"
    )
    finding = rule.check(context)
    assert finding is None


def test_r019_no_trigger_on_select() -> None:
    rule = R019UintNarrowing()
    context = QueryContext(sql="SELECT event_type FROM events WHERE event_type = 1")
    finding = rule.check(context)
    assert finding is None
