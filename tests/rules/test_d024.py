from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D024_mv_with_populate import D024MVWithPopulate


def test_d024_triggers_on_populate() -> None:
    rule = D024MVWithPopulate()
    ctx = QueryContext(
        sql="CREATE MATERIALIZED VIEW mv TO target AS SELECT user_id FROM events POPULATE"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "D-024"
    assert finding.severity == "medium"


def test_d024_no_trigger_without_populate() -> None:
    rule = D024MVWithPopulate()
    ctx = QueryContext(
        sql="CREATE MATERIALIZED VIEW mv TO target AS SELECT user_id FROM events"
    )
    finding = rule.check(ctx)
    assert finding is None
