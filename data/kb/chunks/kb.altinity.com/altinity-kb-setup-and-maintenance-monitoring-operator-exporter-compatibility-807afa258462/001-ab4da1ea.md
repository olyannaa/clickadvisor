---
source: kb.altinity.com
url: http://localhost:8123/metrics
topic: compatibility-layer-for-the-altinity-kubernetes-operator-for-clickhouse-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 2
---

# Compatibility layer for the Altinity Kubernetes Operator for ClickHouse® \| Altinity® Knowledge Base for ClickHouse®

1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. Compatibility layer for the Altinity Kubernetes Operator for ClickHouse®
# Compatibility layer for the Altinity Kubernetes Operator for ClickHouse®

Page description for heading and indexes.It’s possible to expose `clickhouse-server` metrics in the style used by the Altinity Kubernetes Operator for ClickHouse®. It’s for the `clickhouse-operator` grafana dashboard.

```
CREATE VIEW system.operator_compatible_metrics
(
    `name` String,
    `value` Float64,
    `help` String,
    `labels` Map(String, String),
    `type` String
) AS
SELECT
    concat('chi_clickhouse_event_', event) AS name,
    CAST(value, 'Float64') AS value,
    description AS help,
    map('hostname', hostName()) AS labels,
    'counter' AS type
FROM system.events
UNION ALL
SELECT
    concat('chi_clickhouse_metric_', metric) AS name,
    CAST(value, 'Float64') AS value,
    description AS help,
    map('hostname', hostName()) AS labels,
    'gauge' AS type
FROM system.metrics
UNION ALL
SELECT
    concat('chi_clickhouse_metric_', metric) AS name,
    value,
    '' AS help,
    map('hostname', hostName()) AS labels,
    'gauge' AS type
FROM system.asynchronous_metrics
UNION ALL
SELECT
    'chi_clickhouse_metric_MemoryDictionaryBytesAllocated' AS name,
    CAST(sum(bytes_allocated), 'Float64') AS value,
    'Memory size allocated for dictionaries' AS help,
    map('hostname', hostName()) AS labels,
    'gauge' AS type
FROM system.dictionaries
UNION ALL
SELECT
    'chi_clickhouse_metric_LongestRunningQuery' AS name,
    CAST(max(elapsed), 'Float64') AS value,
    'Longest running query time' AS help,
    map('hostname', hostName()) AS labels,
    'gauge' AS type
FROM system.processes
UNION ALL
WITH
    ['chi_clickhouse_table_partitions', 'chi_clickhouse_table_parts', 'chi_clickhouse_table_parts_bytes', 'chi_clickhouse_table_parts_bytes_uncompressed', 'chi_clickhouse_table_parts_rows', 'chi_clickhouse_metric_DiskDataBytes', 'chi_clickhouse_metric_MemoryPrimaryKeyBytesAllocated'] AS names,
    [uniq(partition), count(), sum(bytes), sum(data_uncompressed_bytes), sum(rows), sum(bytes_on_disk), sum(primary_key_bytes_in_memory_allocated)] AS values,
    arrayJoin(arrayZip(names, values)) AS tpl
SELECT
    tpl.1 AS name,
    CAST(tpl.2, 'Float64') AS value,
    '' AS help,
    map('database', database, 'table', table, 'active', toString(active), 'hostname', hostName()) AS labels,
    'gauge' AS type
FROM system.parts
GROUP BY
    active,
    database,
    table
UNION ALL
WITH
    ['chi_clickhouse_table_mutations', 'chi_clickhouse_table_mutations_parts_to_do'] AS names,
    [CAST(count(), 'Float64'), CAST(sum(parts_to_do), 'Float64')] AS values,
    arrayJoin(arrayZip(names, values)) AS tpl
SELECT
    tpl.1 AS name,
    tpl.2 AS value,
    '' AS help,
    map('database', database, 'table', table, 'hostname', hostName()) AS labels,
    'gauge' AS type
FROM system.mutations
WHERE is_done = 0
GROUP BY
    database,
    table
UNION ALL
WITH if(coalesce(reason, 'unknown') = '', 'detached_by_user', coalesce(reason, 'unknown')) AS detach_reason
SELECT
    'chi_clickhouse_metric_DetachedParts' AS name,
    CAST(count(), 'Float64') AS value,
    '' AS help,
    map('database', database, 'table', table, 'disk', disk, 'hostname', hostName()) AS labels,
    'gauge' AS type
FROM system.detached_parts
GROUP BY
    database,
    table,
    disk,
    reason
ORDER BY name ASC

```
