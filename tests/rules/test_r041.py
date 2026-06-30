from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R041_string_code_column import R041StringCodeColumn


def test_r041_triggers_on_string_country_code() -> None:
    rule = R041StringCodeColumn()
    ctx = QueryContext(
        sql="CREATE TABLE orders (order_id UInt64, country_code String) ENGINE = MergeTree ORDER BY order_id"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-041"
    assert "FixedString" in finding.suggestion


def test_r041_no_trigger_on_string_description() -> None:
    rule = R041StringCodeColumn()
    ctx = QueryContext(
        sql="CREATE TABLE products (product_id UInt64, description String) ENGINE = MergeTree ORDER BY product_id"
    )
    finding = rule.check(ctx)
    assert finding is None
