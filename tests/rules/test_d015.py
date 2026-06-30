from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D015_optimize_table_final import D015OptimizeTableFinal


def test_d015_triggers_on_optimize_final() -> None:
    rule = D015OptimizeTableFinal()
    ctx = QueryContext(sql="OPTIMIZE TABLE events FINAL")
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "D-015"
    assert finding.severity == "high"
    assert "FINAL" in finding.description


def test_d015_no_trigger_on_optimize_without_final() -> None:
    rule = D015OptimizeTableFinal()
    ctx = QueryContext(sql="OPTIMIZE TABLE events")
    finding = rule.check(ctx)
    assert finding is None
