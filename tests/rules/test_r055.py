from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R055_arrayreduce_min import R055ArrayReduceMin


def test_r055_triggers_on_arrayreduce_min() -> None:
    rule = R055ArrayReduceMin()
    ctx = QueryContext(sql="SELECT arrayReduce('min', scores) FROM results")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-055"
    assert "arrayMin" in finding.suggestion


def test_r055_no_trigger_on_arraymin() -> None:
    rule = R055ArrayReduceMin()
    ctx = QueryContext(sql="SELECT arrayMin(scores) FROM results")
    finding = rule.check(ctx)
    assert finding is None
