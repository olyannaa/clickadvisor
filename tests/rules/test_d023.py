from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D023_mv_without_to import D023MVWithoutTo


def test_d023_triggers_on_mv_without_to() -> None:
    rule = D023MVWithoutTo()
    ctx = QueryContext(
        sql="CREATE MATERIALIZED VIEW events_mv AS SELECT user_id, count() FROM events GROUP BY user_id"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "D-023"


def test_d023_no_trigger_on_mv_with_to() -> None:
    rule = D023MVWithoutTo()
    ctx = QueryContext(
        sql="CREATE MATERIALIZED VIEW events_mv TO events_target AS SELECT user_id, count() FROM events GROUP BY user_id"
    )
    finding = rule.check(ctx)
    assert finding is None
