from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R022_float_monetary import R022FloatMonetary


def test_r022_triggers_on_float_amount_column() -> None:
    rule = R022FloatMonetary()
    ctx = QueryContext(
        sql="CREATE TABLE orders (order_id UInt64, total_amount Float64) ENGINE = MergeTree ORDER BY order_id"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-022"
    assert "total_amount" in finding.description


def test_r022_no_trigger_on_float_non_monetary() -> None:
    rule = R022FloatMonetary()
    ctx = QueryContext(
        sql="CREATE TABLE metrics (ts DateTime, cpu_usage Float64) ENGINE = MergeTree ORDER BY ts"
    )
    finding = rule.check(ctx)
    assert finding is None
