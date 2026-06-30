from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R060_has_and_has_to_hasall import R060HasAndHasToHasAll


def test_r060_triggers_on_has_and_has() -> None:
    rule = R060HasAndHasToHasAll()
    ctx = QueryContext(
        sql="SELECT * FROM events WHERE has(tags, 'error') AND has(tags, 'critical')"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-060"
    assert "hasAll" in finding.suggestion


def test_r060_no_trigger_on_different_arrays() -> None:
    rule = R060HasAndHasToHasAll()
    ctx = QueryContext(
        sql="SELECT * FROM events WHERE has(tags, 'error') AND has(labels, 'critical')"
    )
    finding = rule.check(ctx)
    assert finding is None
