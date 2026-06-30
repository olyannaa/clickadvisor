from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R037_empty_string_eq_to_empty import R037EmptyStringEqToEmpty


def test_r037_triggers_on_eq_empty_string() -> None:
    rule = R037EmptyStringEqToEmpty()
    ctx = QueryContext(sql="SELECT * FROM events WHERE message = ''")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-037"
    assert "empty" in finding.suggestion


def test_r037_no_trigger_on_eq_nonempty_string() -> None:
    rule = R037EmptyStringEqToEmpty()
    ctx = QueryContext(sql="SELECT * FROM events WHERE message = 'hello'")
    finding = rule.check(ctx)
    assert finding is None
