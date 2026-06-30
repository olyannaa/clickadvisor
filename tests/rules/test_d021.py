from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D021_select_star_in_mv import D021SelectStarInMV


def test_d021_triggers_on_select_star_in_mv() -> None:
    rule = D021SelectStarInMV()
    ctx = QueryContext(
        sql="CREATE MATERIALIZED VIEW events_mv TO events_agg AS SELECT * FROM events"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "D-021"
    assert finding.severity == "medium"


def test_d021_no_trigger_on_explicit_columns() -> None:
    rule = D021SelectStarInMV()
    ctx = QueryContext(
        sql="CREATE MATERIALIZED VIEW events_mv TO events_agg AS SELECT user_id, count() FROM events GROUP BY user_id"
    )
    finding = rule.check(ctx)
    assert finding is None
