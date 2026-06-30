from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R061_has_or_has_to_hasany import R061HasOrHasToHasAny


def test_r061_triggers_on_has_or_has() -> None:
    rule = R061HasOrHasToHasAny()
    ctx = QueryContext(
        sql="SELECT * FROM events WHERE has(tags, 'error') OR has(tags, 'warning')"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-061"
    assert "hasAny" in finding.suggestion


def test_r061_no_trigger_on_different_arrays() -> None:
    rule = R061HasOrHasToHasAny()
    ctx = QueryContext(
        sql="SELECT * FROM events WHERE has(tags, 'error') OR has(labels, 'warning')"
    )
    finding = rule.check(ctx)
    assert finding is None
