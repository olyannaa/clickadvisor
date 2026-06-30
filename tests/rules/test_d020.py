from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D020_partition_by_non_date import D020PartitionByNonDate


def test_d020_triggers_on_non_date_partition() -> None:
    rule = D020PartitionByNonDate()
    ctx = QueryContext(
        sql="CREATE TABLE events (user_id UInt64, ts DateTime) ENGINE = MergeTree PARTITION BY user_id ORDER BY ts"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "D-020"
    assert finding.severity == "medium"


def test_d020_no_trigger_on_date_function_partition() -> None:
    rule = D020PartitionByNonDate()
    ctx = QueryContext(
        sql="CREATE TABLE events (user_id UInt64, ts DateTime) ENGINE = MergeTree PARTITION BY toYYYYMM(ts) ORDER BY ts"
    )
    finding = rule.check(ctx)
    assert finding is None
