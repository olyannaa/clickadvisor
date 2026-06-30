from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule


def _section(env: dict[str, Any] | None, name: str) -> Mapping[str, Any]:
    if not env:
        return {}
    value = env.get(name)
    return value if isinstance(value, Mapping) else {}


def _num(mapping: Mapping[str, Any], key: str) -> float | None:
    value = mapping.get(key)
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _bool(mapping: Mapping[str, Any], key: str) -> bool | None:
    value = mapping.get(key)
    return value if isinstance(value, bool) else None


def _str(mapping: Mapping[str, Any], key: str) -> str | None:
    value = mapping.get(key)
    return value if isinstance(value, str) else None


def _finding(rule: Rule, severity: str, description: str, suggestion: str) -> Finding:
    return Finding(
        rule_id=rule.rule_id,
        rule_name=rule.name,
        tier=rule.tier,
        severity=severity,
        description=description,
        suggestion=suggestion,
        confidence="advisory",
        ch_version_introduced=rule.ch_version_introduced,
    )


class E001MaxThreadsVsCpuCores(Rule):
    rule_id = "E-001"
    name = "max_threads_vs_cpu_cores"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        settings = _section(context.environment, "settings")
        hardware = _section(context.environment, "hardware")
        max_threads = _num(settings, "max_threads")
        cpu_cores = _num(hardware, "cpu_cores")
        if max_threads is None or cpu_cores is None or max_threads <= cpu_cores * 2:
            return None
        return _finding(self, "medium", "max_threads сильно превышает число CPU cores.", "Ограничьте max_threads ближе к CPU cores или профилю workload.")


class E002MaxMemoryUsageVsTotalRam(Rule):
    rule_id = "E-002"
    name = "max_memory_usage_vs_total_ram"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        settings = _section(context.environment, "settings")
        hardware = _section(context.environment, "hardware")
        memory = _num(settings, "max_memory_usage")
        ram = _num(hardware, "ram_bytes")
        if memory is None or ram is None or memory <= ram * 0.8:
            return None
        return _finding(self, "high", "max_memory_usage близок к общему RAM сервера.", "Оставьте запас памяти для merges, caches и параллельных запросов.")


class E003ExternalGroupByThreshold(Rule):
    rule_id = "E-003"
    name = "external_groupby_threshold"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        settings = _section(context.environment, "settings")
        max_memory = _num(settings, "max_memory_usage")
        external = _num(settings, "max_bytes_before_external_group_by")
        if max_memory is None or (external is not None and 0 < external <= max_memory * 0.7):
            return None
        return _finding(self, "medium", "external GROUP BY threshold отсутствует или слишком высок.", "Настройте max_bytes_before_external_group_by ниже max_memory_usage.")


class E004MarkCacheSizing(Rule):
    rule_id = "E-004"
    name = "mark_cache_sizing"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        caches = _section(context.environment, "caches")
        mark_cache = _num(caches, "mark_cache_size")
        active_marks = _num(caches, "active_marks_bytes")
        if mark_cache is None or active_marks is None or mark_cache >= active_marks * 0.5:
            return None
        return _finding(self, "medium", "mark_cache_size мал относительно активных marks.", "Увеличьте mark_cache_size или сократите hot working set.")


class E005UncompressedCacheSizing(Rule):
    rule_id = "E-005"
    name = "uncompressed_cache_sizing"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        caches = _section(context.environment, "caches")
        enabled = _bool(caches, "use_uncompressed_cache")
        cache_size = _num(caches, "uncompressed_cache_size")
        repeated = _bool(_section(context.environment, "workload"), "repeated_reads")
        if not repeated or (enabled and cache_size and cache_size > 0):
            return None
        return _finding(self, "low", "Повторяющийся workload без uncompressed cache.", "Включите и настройте uncompressed cache для повторных чтений.")


class E006MergeSettingsForDiskType(Rule):
    rule_id = "E-006"
    name = "merge_settings_for_disk_type"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        disk_type = (_str(_section(context.environment, "hardware"), "disk_type") or "").lower()
        merges = _num(_section(context.environment, "settings"), "background_pool_size")
        if disk_type != "hdd" or merges is None or merges <= 16:
            return None
        return _finding(self, "medium", "background_pool_size высок для HDD storage.", "Снизьте merge concurrency или перенесите hot tables на SSD/NVMe.")


class E007StoragePolicyRecommendation(Rule):
    rule_id = "E-007"
    name = "storage_policy_recommendation"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        storage = _section(context.environment, "storage")
        hot_cold = _bool(storage, "has_hot_cold_data")
        policy = _str(storage, "storage_policy")
        if not hot_cold or policy:
            return None
        return _finding(self, "low", "Есть hot/cold data без storage_policy.", "Добавьте storage policy с hot и cold volumes.")


class E008JitCompilationToggle(Rule):
    rule_id = "E-008"
    name = "jit_compilation_toggle"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        workload = _section(context.environment, "workload")
        settings = _section(context.environment, "settings")
        if not _bool(workload, "complex_expressions") or _bool(settings, "compile_expressions"):
            return None
        return _finding(self, "low", "Сложные выражения выполняются без JIT compilation.", "Проверьте compile_expressions для CPU-heavy workload.")


class E009QueryCacheForRepeatedWorkload(Rule):
    rule_id = "E-009"
    name = "query_cache_for_repeated_workload"
    tier = "env"
    ch_version_introduced = "23.1"

    def check(self, context: QueryContext) -> Finding | None:
        workload = _section(context.environment, "workload")
        settings = _section(context.environment, "settings")
        if not _bool(workload, "repeated_queries") or _bool(settings, "use_query_cache"):
            return None
        return _finding(self, "low", "Повторяющиеся запросы выполняются без query cache.", "Рассмотрите use_query_cache для стабильных повторных запросов.")


class E010PartsToThrowInsertTuning(Rule):
    rule_id = "E-010"
    name = "parts_to_throw_insert_tuning"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        metrics = _section(context.environment, "system_metrics")
        parts = _num(metrics, "active_parts")
        threshold = _num(_section(context.environment, "settings"), "parts_to_throw_insert")
        if parts is None or threshold is None or parts < threshold * 0.8:
            return None
        return _finding(self, "high", "active parts близки к parts_to_throw_insert.", "Укрупните inserts, проверьте partitioning и merge throughput.")


class E011DistributedConnectionsSizing(Rule):
    rule_id = "E-011"
    name = "distributed_connections_sizing"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        cluster = _section(context.environment, "cluster")
        shards = _num(cluster, "shards")
        replicas = _num(cluster, "replicas")
        connections = _num(_section(context.environment, "settings"), "max_distributed_connections")
        needed = (shards or 0) * (replicas or 1)
        if needed <= 0 or (connections is not None and connections >= needed):
            return None
        return _finding(self, "medium", "max_distributed_connections ниже размера fan-out.", "Увеличьте max_distributed_connections или уменьшите distributed fan-out.")


class E012JoinUseNullsOverhead(Rule):
    rule_id = "E-012"
    name = "join_use_nulls_overhead"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if not _bool(_section(context.environment, "settings"), "join_use_nulls"):
            return None
        return _finding(self, "medium", "join_use_nulls=1 добавляет Nullable overhead в JOIN results.", "Отключите join_use_nulls, если SQL-совместимость NULL не требуется.")


class E013AsyncInsertBusyTimeoutTuning(Rule):
    rule_id = "E-013"
    name = "async_insert_busy_timeout_tuning"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        settings = _section(context.environment, "settings")
        if not _bool(settings, "async_insert"):
            return None
        timeout = _num(settings, "async_insert_busy_timeout_ms")
        if timeout is not None and timeout >= 100:
            return None
        return _finding(self, "low", "async_insert включён с низким busy timeout.", "Увеличьте async_insert_busy_timeout_ms для лучшего batching.")


class E014MergeMaxBytesForLevel(Rule):
    rule_id = "E-014"
    name = "merge_max_bytes_for_level"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        settings = _section(context.environment, "settings")
        value = _num(settings, "max_bytes_to_merge_at_max_space_in_pool")
        large_parts = _bool(_section(context.environment, "workload"), "large_parts")
        if not large_parts or (value is not None and value > 0):
            return None
        return _finding(self, "medium", "Large parts workload без явной настройки merge max bytes.", "Проверьте max_bytes_to_merge_at_max_space_in_pool для merge throughput.")


class E015OptimizeAggregationInOrder(Rule):
    rule_id = "E-015"
    name = "optimize_aggregation_in_order"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        workload = _section(context.environment, "workload")
        settings = _section(context.environment, "settings")
        if not _bool(workload, "group_by_order_key_prefix") or _bool(settings, "optimize_aggregation_in_order"):
            return None
        return _finding(self, "medium", "GROUP BY совпадает с ORDER BY prefix, но optimize_aggregation_in_order выключен.", "Включите optimize_aggregation_in_order для streaming aggregation.")


class E016JoinAlgorithmForLargeTables(Rule):
    rule_id = "E-016"
    name = "join_algorithm_for_large_tables"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        workload = _section(context.environment, "workload")
        settings = _section(context.environment, "settings")
        algorithm = (_str(settings, "join_algorithm") or "").lower()
        if not _bool(workload, "large_join") or algorithm in {"partial_merge", "grace_hash", "auto"}:
            return None
        return _finding(self, "high", "Large JOIN использует неподходящий join_algorithm.", "Рассмотрите join_algorithm=auto, grace_hash или partial_merge.")


class E017DistributedAggregationMemoryEfficient(Rule):
    rule_id = "E-017"
    name = "distributed_aggregation_memory_efficient"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        workload = _section(context.environment, "workload")
        settings = _section(context.environment, "settings")
        if not _bool(workload, "distributed_aggregation") or _bool(settings, "distributed_aggregation_memory_efficient"):
            return None
        return _finding(self, "medium", "Distributed aggregation без memory efficient mode.", "Включите distributed_aggregation_memory_efficient для больших distributed GROUP BY.")


class E018InputFormatForBulkInserts(Rule):
    rule_id = "E-018"
    name = "input_format_for_bulk_inserts"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        workload = _section(context.environment, "workload")
        fmt = (_str(workload, "insert_format") or "").lower()
        if not _bool(workload, "bulk_inserts") or fmt in {"native", "parquet", "arrow", "rowbinary"}:
            return None
        return _finding(self, "medium", "Bulk inserts используют текстовый или неэффективный формат.", "Для bulk inserts используйте Native, RowBinary, Parquet или Arrow.")


class E019PreferLocalhostReplica(Rule):
    rule_id = "E-019"
    name = "prefer_localhost_replica"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        cluster = _section(context.environment, "cluster")
        settings = _section(context.environment, "settings")
        has_local = _bool(cluster, "has_local_replica") or _bool(cluster, "has_local_replicas")
        if not has_local or _bool(settings, "prefer_localhost_replica"):
            return None
        return _finding(self, "low", "Локальная replica доступна, но prefer_localhost_replica выключен.", "Включите prefer_localhost_replica для сокращения network hop.")


class E020MaxExecutionTimeForProtection(Rule):
    rule_id = "E-020"
    name = "max_execution_time_for_protection"
    tier = "env"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        workload = _section(context.environment, "workload")
        settings = _section(context.environment, "settings")
        max_time = _num(settings, "max_execution_time")
        protected_workload = _bool(workload, "interactive_queries") or _bool(workload, "user_facing")
        if not protected_workload or (max_time is not None and 0 < max_time <= 300):
            return None
        return _finding(self, "medium", "Interactive queries не защищены max_execution_time.", "Задайте max_execution_time в user profile или query settings.")
