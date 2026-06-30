from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.backlog import (
    D001FullScanOnPartitionedTable,
    D002CrossJoinRisk,
    D005LeadingWildcardLike,
    D006ArrayJoinBeforeFilter,
    D008SampleWithoutSampleBy,
    D009NullableWithoutNeed,
    D010UnusedColumnsInSelect,
    D011ImplicitTypeCoercionInJoin,
    D012WindowFunctionWithoutPartition,
    D013DeeplyNestedSubqueries,
)


def test_d001_triggers_on_partitioned_table_without_partition_filter() -> None:
    rule = D001FullScanOnPartitionedTable()
    ctx = QueryContext(
        sql="SELECT count() FROM events WHERE user_id = 42",
        schema_ddl="CREATE TABLE events (ts DateTime, user_id UInt64) ENGINE = MergeTree PARTITION BY toYYYYMM(ts) ORDER BY user_id",
    )
    assert rule.check(ctx) is not None


def test_d001_requires_schema_context() -> None:
    assert D001FullScanOnPartitionedTable().check(QueryContext(sql="SELECT count() FROM events")) is None


def test_d002_triggers_on_cross_join() -> None:
    ctx = QueryContext(sql="SELECT * FROM events CROSS JOIN users")
    assert D002CrossJoinRisk().check(ctx) is not None


def test_d002_no_trigger_on_equality_join() -> None:
    ctx = QueryContext(sql="SELECT * FROM events e JOIN users u ON e.user_id = u.id")
    assert D002CrossJoinRisk().check(ctx) is None


def test_d005_triggers_on_leading_wildcard_like() -> None:
    assert D005LeadingWildcardLike().check(QueryContext(sql="SELECT * FROM logs WHERE msg LIKE '%error'")) is not None


def test_d005_no_trigger_on_prefix_like() -> None:
    assert D005LeadingWildcardLike().check(QueryContext(sql="SELECT * FROM logs WHERE msg LIKE 'error%'")) is None


def test_d006_triggers_when_arrayjoin_before_where() -> None:
    assert D006ArrayJoinBeforeFilter().check(QueryContext(sql="SELECT arrayJoin(tags) AS tag FROM events WHERE user_id = 1")) is not None


def test_d006_no_trigger_when_filter_before_arrayjoin() -> None:
    assert D006ArrayJoinBeforeFilter().check(QueryContext(sql="SELECT * FROM events WHERE id IN (SELECT arrayJoin(ids) FROM ids)")) is None


def test_d008_triggers_on_sample_without_sample_by() -> None:
    ctx = QueryContext(sql="SELECT * FROM events SAMPLE 0.1", schema_ddl="CREATE TABLE events (id UInt64) ENGINE = MergeTree ORDER BY id")
    assert D008SampleWithoutSampleBy().check(ctx) is not None


def test_d008_no_trigger_when_schema_has_sample_by() -> None:
    ctx = QueryContext(sql="SELECT * FROM events SAMPLE 0.1", schema_ddl="CREATE TABLE events (id UInt64) ENGINE = MergeTree ORDER BY id SAMPLE BY id")
    assert D008SampleWithoutSampleBy().check(ctx) is None


def test_d009_triggers_on_nullable_without_nulls() -> None:
    ctx = QueryContext(
        sql="SELECT count() FROM events",
        schema_ddl="CREATE TABLE events (status Nullable(String)) ENGINE = MergeTree ORDER BY tuple()",
        environment={"null_counts": {"status": 0}},
    )
    assert D009NullableWithoutNeed().check(ctx) is not None


def test_d009_no_trigger_when_nulls_are_present() -> None:
    ctx = QueryContext(sql="CREATE TABLE events (status Nullable(String))", environment={"null_counts": {"status": 12}})
    assert D009NullableWithoutNeed().check(ctx) is None


def test_d010_triggers_on_unused_inner_projection() -> None:
    ctx = QueryContext(sql="SELECT id FROM (SELECT id, payload FROM events)")
    assert D010UnusedColumnsInSelect().check(ctx) is not None


def test_d010_no_trigger_when_inner_projection_is_used() -> None:
    ctx = QueryContext(sql="SELECT id, payload FROM (SELECT id, payload FROM events)")
    assert D010UnusedColumnsInSelect().check(ctx) is None


def test_d011_triggers_on_join_cast() -> None:
    ctx = QueryContext(sql="SELECT * FROM events e JOIN users u ON toUInt64(e.user_id) = u.id")
    assert D011ImplicitTypeCoercionInJoin().check(ctx) is not None


def test_d011_no_trigger_without_join_cast() -> None:
    ctx = QueryContext(sql="SELECT * FROM events e JOIN users u ON e.user_id = u.id")
    assert D011ImplicitTypeCoercionInJoin().check(ctx) is None


def test_d012_triggers_on_window_without_partition() -> None:
    ctx = QueryContext(sql="SELECT row_number() OVER (ORDER BY ts) FROM events")
    assert D012WindowFunctionWithoutPartition().check(ctx) is not None


def test_d012_no_trigger_with_partition() -> None:
    ctx = QueryContext(sql="SELECT row_number() OVER (PARTITION BY user_id ORDER BY ts) FROM events")
    assert D012WindowFunctionWithoutPartition().check(ctx) is None


def test_d013_triggers_on_deeply_nested_subqueries() -> None:
    sql = "SELECT * FROM (SELECT * FROM (SELECT * FROM (SELECT * FROM (SELECT * FROM events))))"
    assert D013DeeplyNestedSubqueries().check(QueryContext(sql=sql)) is not None


def test_d013_no_trigger_on_shallow_query() -> None:
    assert D013DeeplyNestedSubqueries().check(QueryContext(sql="SELECT * FROM (SELECT * FROM events)")) is None
