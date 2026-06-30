from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D017_nullable_column_in_ddl import D017NullableColumnInDDL


def test_d017_triggers_on_nullable_in_ddl() -> None:
    rule = D017NullableColumnInDDL()
    ctx = QueryContext(
        sql="CREATE TABLE t (id UInt64, score Nullable(Float64)) ENGINE = MergeTree ORDER BY id"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "D-017"
    assert finding.severity == "medium"
    assert "Nullable" in finding.description


def test_d017_no_trigger_on_non_nullable_ddl() -> None:
    rule = D017NullableColumnInDDL()
    ctx = QueryContext(
        sql="CREATE TABLE t (id UInt64, score Float64) ENGINE = MergeTree ORDER BY id"
    )
    finding = rule.check(ctx)
    assert finding is None
