from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R025_order_by_tuple import R025OrderByTupleNoPK


def test_r025_triggers_on_order_by_tuple() -> None:
    rule = R025OrderByTupleNoPK()
    ctx = QueryContext(
        sql="CREATE TABLE events (user_id UInt64, ts DateTime) ENGINE = MergeTree ORDER BY tuple()"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-025"
    assert finding.severity == "medium"
    assert "primary key" in finding.description.lower() or "tuple()" in finding.description


def test_r025_no_trigger_on_proper_order_by() -> None:
    rule = R025OrderByTupleNoPK()
    ctx = QueryContext(
        sql="CREATE TABLE events (user_id UInt64, ts DateTime) ENGINE = MergeTree ORDER BY (user_id, ts)"
    )
    finding = rule.check(ctx)
    assert finding is None
