from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R049_sumif_one_to_countif import R049SumIfOneToCountIf


def test_r049_triggers_on_sumif_one() -> None:
    rule = R049SumIfOneToCountIf()
    ctx = QueryContext(sql="SELECT sumIf(1, status = 'active') AS active_cnt FROM users")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-049"
    assert "countIf" in finding.suggestion


def test_r049_no_trigger_on_sumif_col() -> None:
    rule = R049SumIfOneToCountIf()
    ctx = QueryContext(sql="SELECT sumIf(amount, is_paid) AS total FROM orders")
    finding = rule.check(ctx)
    assert finding is None
