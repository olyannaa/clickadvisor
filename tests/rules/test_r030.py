from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R030_not_in_singleton import R030NotInSingleton


def test_r030_triggers_on_not_in_single_value() -> None:
    rule = R030NotInSingleton()
    ctx = QueryContext(
        sql="SELECT * FROM events WHERE status NOT IN ('deleted')"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-030"
    assert "!=" in finding.suggestion


def test_r030_no_trigger_on_not_in_multiple() -> None:
    rule = R030NotInSingleton()
    ctx = QueryContext(
        sql="SELECT * FROM events WHERE status NOT IN ('deleted', 'archived')"
    )
    finding = rule.check(ctx)
    assert finding is None
