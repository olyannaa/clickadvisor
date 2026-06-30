from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D022_delete_without_where import D022DeleteWithoutWhere


def test_d022_triggers_on_delete_without_where() -> None:
    rule = D022DeleteWithoutWhere()
    ctx = QueryContext(sql="DELETE FROM events")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "D-022"
    assert finding.severity == "high"


def test_d022_no_trigger_on_delete_with_where() -> None:
    rule = D022DeleteWithoutWhere()
    ctx = QueryContext(sql="DELETE FROM events WHERE dt < '2023-01-01'")
    finding = rule.check(ctx)
    assert finding is None
