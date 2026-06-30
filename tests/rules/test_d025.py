from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D025_mv_with_join import D025MVWithJoin


def test_d025_triggers_on_mv_with_join() -> None:
    rule = D025MVWithJoin()
    ctx = QueryContext(
        sql="CREATE MATERIALIZED VIEW mv TO t AS SELECT e.uid, u.name FROM events e LEFT JOIN users u ON e.uid = u.uid"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "D-025"
    assert finding.severity == "medium"


def test_d025_no_trigger_on_mv_without_join() -> None:
    rule = D025MVWithJoin()
    ctx = QueryContext(
        sql="CREATE MATERIALIZED VIEW mv TO t AS SELECT user_id, count() FROM events GROUP BY user_id"
    )
    finding = rule.check(ctx)
    assert finding is None
