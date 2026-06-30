from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R053_arrayreduce_sum import R053ArrayReduceSum


def test_r053_triggers_on_arrayreduce_sum() -> None:
    rule = R053ArrayReduceSum()
    ctx = QueryContext(sql="SELECT arrayReduce('sum', amounts) FROM orders")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-053"
    assert "arraySum" in finding.suggestion


def test_r053_no_trigger_on_arraysum() -> None:
    rule = R053ArrayReduceSum()
    ctx = QueryContext(sql="SELECT arraySum(amounts) FROM orders")
    finding = rule.check(ctx)
    assert finding is None
