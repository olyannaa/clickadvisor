from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier2 import (
    R101OrderByKeyRedesign,
    R102SkipIndexRecommendation,
    R103ProjectionRecommendation,
    R104PrimaryKeyRefinement,
    R105PartitionStrategyAdjustment,
    R106LowCardinalityConversion,
    R107CodecRecommendation,
    R108PrewhereInjection,
    R109JoinReorderSmallOnRight,
    R110JoinAlgorithmChoice,
    R111MaterializedViewRecommendation,
    R112GroupByMultipassSplit,
)


def assert_advisory(rule_id: str, ctx: QueryContext) -> None:
    rule = {
        "R-101": R101OrderByKeyRedesign,
        "R-102": R102SkipIndexRecommendation,
        "R-103": R103ProjectionRecommendation,
        "R-104": R104PrimaryKeyRefinement,
        "R-105": R105PartitionStrategyAdjustment,
        "R-106": R106LowCardinalityConversion,
        "R-107": R107CodecRecommendation,
        "R-108": R108PrewhereInjection,
        "R-109": R109JoinReorderSmallOnRight,
        "R-110": R110JoinAlgorithmChoice,
        "R-111": R111MaterializedViewRecommendation,
        "R-112": R112GroupByMultipassSplit,
    }[rule_id]()
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == rule_id
    assert finding.tier == "2"
    assert finding.confidence == "advisory"


def test_r101_order_by_tuple_schema() -> None:
    assert_advisory("R-101", QueryContext(sql="SELECT count() FROM events", schema_ddl="CREATE TABLE events (id UInt64) ENGINE = MergeTree ORDER BY tuple()"))
    assert R101OrderByKeyRedesign().check(QueryContext(sql="SELECT count() FROM events")) is None


def test_r102_skip_index_for_substring_search() -> None:
    assert_advisory("R-102", QueryContext(sql="SELECT * FROM logs WHERE msg LIKE '%timeout%'"))
    assert R102SkipIndexRecommendation().check(QueryContext(sql="SELECT * FROM logs WHERE msg LIKE 'timeout%'")) is None


def test_r103_projection_for_repeated_group_by() -> None:
    ctx = QueryContext(sql="SELECT user_id, count() FROM events GROUP BY user_id", environment={"workload": {"repeated_group_by": True}})
    assert_advisory("R-103", ctx)
    assert R103ProjectionRecommendation().check(QueryContext(sql="SELECT user_id, count() FROM events GROUP BY user_id")) is None


def test_r104_primary_key_refinement() -> None:
    ctx = QueryContext(sql="SELECT * FROM events WHERE user_id = 42", schema_ddl="CREATE TABLE events (user_id UInt64, ts DateTime) ENGINE = MergeTree ORDER BY (user_id, ts)")
    assert_advisory("R-104", ctx)
    assert R104PrimaryKeyRefinement().check(QueryContext(sql="SELECT * FROM events", schema_ddl=ctx.schema_ddl)) is None


def test_r105_partition_strategy_adjustment() -> None:
    assert_advisory("R-105", QueryContext(sql="SELECT count() FROM events", environment={"system_metrics": {"active_parts": 1000, "active_partitions": 5}}))
    assert R105PartitionStrategyAdjustment().check(QueryContext(sql="SELECT count() FROM events")) is None


def test_r106_lowcardinality_conversion() -> None:
    schema = "CREATE TABLE events (country String, ts DateTime) ENGINE = MergeTree ORDER BY ts"
    assert_advisory("R-106", QueryContext(sql="SELECT country FROM events", schema_ddl=schema))
    assert R106LowCardinalityConversion().check(QueryContext(sql="SELECT count() FROM events")) is None


def test_r107_codec_recommendation() -> None:
    schema = "CREATE TABLE events (ts DateTime, value UInt64) ENGINE = MergeTree ORDER BY ts"
    assert_advisory("R-107", QueryContext(sql="SELECT count() FROM events", schema_ddl=schema, environment={"workload": {"compression_sensitive": True}}))
    assert R107CodecRecommendation().check(QueryContext(sql="SELECT count() FROM events")) is None


def test_r108_prewhere_injection() -> None:
    assert_advisory("R-108", QueryContext(sql="SELECT * FROM events WHERE user_id = 42", environment={"workload": {"wide_table": True}}))
    assert R108PrewhereInjection().check(QueryContext(sql="SELECT * FROM events PREWHERE user_id = 42")) is None


def test_r109_join_reorder() -> None:
    ctx = QueryContext(sql="SELECT * FROM small s JOIN large l ON s.id = l.id", environment={"workload": {"right_table_larger_than_left": True}})
    assert_advisory("R-109", ctx)
    assert R109JoinReorderSmallOnRight().check(QueryContext(sql="SELECT * FROM a JOIN b ON a.id = b.id")) is None


def test_r110_join_algorithm_choice() -> None:
    assert_advisory("R-110", QueryContext(sql="SELECT * FROM a JOIN b ON a.id = b.id", environment={"workload": {"large_join": True}}))
    assert R110JoinAlgorithmChoice().check(QueryContext(sql="SELECT * FROM a")) is None


def test_r111_materialized_view_recommendation() -> None:
    ctx = QueryContext(sql="SELECT user_id, count() FROM events GROUP BY user_id", environment={"workload": {"repeated_expensive_query": True}})
    assert_advisory("R-111", ctx)
    assert R111MaterializedViewRecommendation().check(QueryContext(sql="SELECT count() FROM events")) is None


def test_r112_groupby_multipass_split() -> None:
    ctx = QueryContext(sql="SELECT user_id, count() FROM events GROUP BY user_id", environment={"workload": {"high_cardinality_group_by": True}})
    assert_advisory("R-112", ctx)
    assert R112GroupByMultipassSplit().check(QueryContext(sql="SELECT count() FROM events")) is None
