from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D016_alter_table_mutation import D016AlterTableMutation


def test_d016_triggers_on_alter_delete() -> None:
    rule = D016AlterTableMutation()
    ctx = QueryContext(sql="ALTER TABLE events DELETE WHERE dt < '2023-01-01'")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "D-016"
    assert finding.severity == "high"
    assert "DELETE" in finding.description


def test_d016_no_trigger_on_select() -> None:
    rule = D016AlterTableMutation()
    ctx = QueryContext(sql="SELECT * FROM events WHERE dt > '2023-01-01'")
    finding = rule.check(ctx)
    assert finding is None
