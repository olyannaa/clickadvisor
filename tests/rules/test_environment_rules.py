from collections.abc import Callable

import pytest

from clickadvisor.core.models import QueryContext
from clickadvisor.rules.base import Rule
from clickadvisor.rules.environment import (
    E001MaxThreadsVsCpuCores,
    E002MaxMemoryUsageVsTotalRam,
    E003ExternalGroupByThreshold,
    E004MarkCacheSizing,
    E005UncompressedCacheSizing,
    E006MergeSettingsForDiskType,
    E007StoragePolicyRecommendation,
    E008JitCompilationToggle,
    E009QueryCacheForRepeatedWorkload,
    E010PartsToThrowInsertTuning,
    E011DistributedConnectionsSizing,
    E012JoinUseNullsOverhead,
    E013AsyncInsertBusyTimeoutTuning,
    E014MergeMaxBytesForLevel,
    E015OptimizeAggregationInOrder,
    E016JoinAlgorithmForLargeTables,
    E017DistributedAggregationMemoryEfficient,
    E018InputFormatForBulkInserts,
    E019PreferLocalhostReplica,
    E020MaxExecutionTimeForProtection,
)

RuleFactory = Callable[[], Rule]


@pytest.mark.parametrize(
    ("factory", "environment"),
    [
        (E001MaxThreadsVsCpuCores, {"settings": {"max_threads": 64}, "hardware": {"cpu_cores": 8}}),
        (E002MaxMemoryUsageVsTotalRam, {"settings": {"max_memory_usage": 90}, "hardware": {"ram_bytes": 100}}),
        (E003ExternalGroupByThreshold, {"settings": {"max_memory_usage": 1000}}),
        (E004MarkCacheSizing, {"caches": {"mark_cache_size": 100, "active_marks_bytes": 1000}}),
        (E005UncompressedCacheSizing, {"workload": {"repeated_reads": True}, "caches": {"use_uncompressed_cache": False}}),
        (E006MergeSettingsForDiskType, {"hardware": {"disk_type": "hdd"}, "settings": {"background_pool_size": 32}}),
        (E007StoragePolicyRecommendation, {"storage": {"has_hot_cold_data": True}}),
        (E008JitCompilationToggle, {"workload": {"complex_expressions": True}, "settings": {"compile_expressions": False}}),
        (E009QueryCacheForRepeatedWorkload, {"workload": {"repeated_queries": True}, "settings": {"use_query_cache": False}}),
        (E010PartsToThrowInsertTuning, {"system_metrics": {"active_parts": 900}, "settings": {"parts_to_throw_insert": 1000}}),
        (E011DistributedConnectionsSizing, {"cluster": {"shards": 4, "replicas": 2}, "settings": {"max_distributed_connections": 4}}),
        (E012JoinUseNullsOverhead, {"settings": {"join_use_nulls": True}}),
        (E013AsyncInsertBusyTimeoutTuning, {"settings": {"async_insert": True, "async_insert_busy_timeout_ms": 10}}),
        (E014MergeMaxBytesForLevel, {"workload": {"large_parts": True}, "settings": {"max_bytes_to_merge_at_max_space_in_pool": 0}}),
        (E015OptimizeAggregationInOrder, {"workload": {"group_by_order_key_prefix": True}, "settings": {"optimize_aggregation_in_order": False}}),
        (E016JoinAlgorithmForLargeTables, {"workload": {"large_join": True}, "settings": {"join_algorithm": "hash"}}),
        (E017DistributedAggregationMemoryEfficient, {"workload": {"distributed_aggregation": True}, "settings": {"distributed_aggregation_memory_efficient": False}}),
        (E018InputFormatForBulkInserts, {"workload": {"bulk_inserts": True, "insert_format": "jsonEachRow"}}),
        (E019PreferLocalhostReplica, {"cluster": {"has_local_replicas": True}, "settings": {"prefer_localhost_replica": False}}),
        (E020MaxExecutionTimeForProtection, {"workload": {"user_facing": True}, "settings": {"max_execution_time": 0}}),
    ],
)
def test_environment_rules_trigger_with_required_context(factory: RuleFactory, environment: dict[str, object]) -> None:
    rule = factory()
    finding = rule.check(QueryContext(sql="SELECT count() FROM events", environment=environment))
    assert finding is not None
    assert finding.rule_id == rule.rule_id
    assert finding.confidence == "advisory"


@pytest.mark.parametrize(
    "factory",
    [
        E001MaxThreadsVsCpuCores,
        E002MaxMemoryUsageVsTotalRam,
        E003ExternalGroupByThreshold,
        E004MarkCacheSizing,
        E005UncompressedCacheSizing,
        E006MergeSettingsForDiskType,
        E007StoragePolicyRecommendation,
        E008JitCompilationToggle,
        E009QueryCacheForRepeatedWorkload,
        E010PartsToThrowInsertTuning,
        E011DistributedConnectionsSizing,
        E012JoinUseNullsOverhead,
        E013AsyncInsertBusyTimeoutTuning,
        E014MergeMaxBytesForLevel,
        E015OptimizeAggregationInOrder,
        E016JoinAlgorithmForLargeTables,
        E017DistributedAggregationMemoryEfficient,
        E018InputFormatForBulkInserts,
        E019PreferLocalhostReplica,
        E020MaxExecutionTimeForProtection,
    ],
)
def test_environment_rules_do_not_fire_without_environment(factory: RuleFactory) -> None:
    assert factory().check(QueryContext(sql="SELECT count() FROM events")) is None
