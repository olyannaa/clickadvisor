from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R036_nested_if_to_multiif import R036NestedIfToMultiIf


def test_r036_triggers_on_nested_if() -> None:
    rule = R036NestedIfToMultiIf()
    ctx = QueryContext(
        sql="SELECT IF(score > 90, 'A', IF(score > 70, 'B', 'C')) AS grade FROM students"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-036"
    assert "multiIf" in finding.suggestion


def test_r036_no_trigger_on_simple_if() -> None:
    rule = R036NestedIfToMultiIf()
    ctx = QueryContext(
        sql="SELECT IF(score > 90, 'A', 'B') AS grade FROM students"
    )
    finding = rule.check(ctx)
    assert finding is None
