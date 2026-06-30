from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R028_coalesce_to_ifnull import R028CoalesceToIfNull


def test_r028_triggers_on_coalesce_two_args() -> None:
    rule = R028CoalesceToIfNull()
    ctx = QueryContext(
        sql="SELECT COALESCE(user_name, 'anonymous') AS name FROM users"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-028"
    assert "ifNull" in finding.suggestion


def test_r028_no_trigger_on_coalesce_three_args() -> None:
    rule = R028CoalesceToIfNull()
    ctx = QueryContext(
        sql="SELECT COALESCE(a, b, c) FROM t"
    )
    finding = rule.check(ctx)
    assert finding is None
