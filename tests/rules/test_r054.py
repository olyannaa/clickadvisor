from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R054_arrayreduce_max import R054ArrayReduceMax


def test_r054_triggers_on_arrayreduce_max() -> None:
    rule = R054ArrayReduceMax()
    ctx = QueryContext(sql="SELECT arrayReduce('max', scores) FROM results")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-054"
    assert "arrayMax" in finding.suggestion


def test_r054_no_trigger_on_arraymax() -> None:
    rule = R054ArrayReduceMax()
    ctx = QueryContext(sql="SELECT arrayMax(scores) FROM results")
    finding = rule.check(ctx)
    assert finding is None
