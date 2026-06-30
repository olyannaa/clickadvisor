from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R038_nonempty_string_neq import R038NonEmptyStringNeqToNotEmpty


def test_r038_triggers_on_neq_empty_string() -> None:
    rule = R038NonEmptyStringNeqToNotEmpty()
    ctx = QueryContext(sql="SELECT * FROM events WHERE message != ''")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-038"
    assert "notEmpty" in finding.suggestion


def test_r038_no_trigger_on_neq_nonempty_string() -> None:
    rule = R038NonEmptyStringNeqToNotEmpty()
    ctx = QueryContext(sql="SELECT * FROM events WHERE message != 'error'")
    finding = rule.check(ctx)
    assert finding is None
