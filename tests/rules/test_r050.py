from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R050_toyyyymm_comparison import R050ToYYYYMMComparison


def test_r050_triggers_on_toyyyymm_gte() -> None:
    rule = R050ToYYYYMMComparison()
    ctx = QueryContext(sql="SELECT * FROM events WHERE toYYYYMM(ts) >= 202401")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-050"
    assert finding.severity == "high"


def test_r050_no_trigger_on_direct_datetime() -> None:
    rule = R050ToYYYYMMComparison()
    ctx = QueryContext(sql="SELECT * FROM events WHERE ts >= '2024-01-01 00:00:00'")
    finding = rule.check(ctx)
    assert finding is None
