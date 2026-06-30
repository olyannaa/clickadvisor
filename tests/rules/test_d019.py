from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D019_set_zero_unlimited_skip_index import (
    D019SetZeroUnlimitedSkipIndex,
)


def test_d019_triggers_on_set_zero() -> None:
    rule = D019SetZeroUnlimitedSkipIndex()
    ctx = QueryContext(
        sql="CREATE TABLE t (status String, INDEX idx_status status TYPE set(0) GRANULARITY 4) ENGINE = MergeTree ORDER BY tuple()"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "D-019"
    assert finding.severity == "low"
    assert "set(0)" in finding.description


def test_d019_no_trigger_on_set_with_limit() -> None:
    rule = D019SetZeroUnlimitedSkipIndex()
    ctx = QueryContext(
        sql="CREATE TABLE t (status String, INDEX idx_status status TYPE set(100) GRANULARITY 4) ENGINE = MergeTree ORDER BY tuple()"
    )
    finding = rule.check(ctx)
    assert finding is None
