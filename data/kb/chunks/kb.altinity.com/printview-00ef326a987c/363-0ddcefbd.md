---
source: kb.altinity.com
url: http://altinity.com/
topic: altinity-knowledge-base-for-clickhouse
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 363
total_chunks_in_doc: 478
---

│ │ background_fetches_pool_size │ 8 │ │ background_schedule_pool_size │ 16 │ │ background_message_broker_schedule_pool_size │ 16 │ │ background_distributed_schedule_pool_size │ 16 │ │ postgresql_connection_pool_size │ 16 │ │ postgresql_connection_pool_wait_timeout │ -1 │ │ odbc_bridge_connection_pool_size │ 16 │ └──────────────────────────────────────────────┴───────┘ ```

```
SELECT
    metric,
    value
FROM system.metrics
WHERE metric LIKE 'Background%'

┌─metric──────────────────────────────────┬─value─┐
│ BackgroundPoolTask                      │     0 │
│ BackgroundFetchesPoolTask               │     0 │
│ BackgroundMovePoolTask                  │     0 │
│ BackgroundSchedulePoolTask              │     0 │
│ BackgroundBufferFlushSchedulePoolTask   │     0 │
│ BackgroundDistributedSchedulePoolTask   │     0 │
│ BackgroundMessageBrokerSchedulePoolTask │     0 │
└─────────────────────────────────────────┴───────┘


SELECT *
FROM system.asynchronous_metrics
WHERE lower(metric) LIKE '%thread%'
ORDER BY metric ASC

┌─metric───────────────────────────────────┬─value─┐
│ HTTPThreads                              │     0 │
│ InterserverThreads                       │     0 │
│ MySQLThreads                             │     0 │
│ OSThreadsRunnable                        │     2 │
│ OSThreadsTotal                           │  2910 │
│ PostgreSQLThreads                        │     0 │
│ TCPThreads                               │     1 │
│ jemalloc.background_thread.num_runs      │     0 │
│ jemalloc.background_thread.num_threads   │     0 │
│ jemalloc.background_thread.run_intervals │     0 │
└──────────────────────────────────────────┴───────┘


SELECT *
FROM system.metrics
WHERE lower(metric) LIKE '%thread%'
ORDER BY metric ASC

Query id: 6acbb596-e28f-4f89-94b2-27dccfe88ee9

┌─metric─────────────┬─value─┬─description───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ GlobalThread       │   151 │ Number of threads in global thread pool.                                                                          │
│ GlobalThreadActive │   144 │ Number of threads in global thread pool running a task.                                                           │
│ LocalThread        │     0 │ Number of threads in local thread pools. The threads in local thread pools are taken from the global thread pool. │
│ LocalThreadActive  │     0 │ Number of threads in local thread pools running a task.                                                           │
│ QueryThread        │     0 │ Number of query processing threads                                                                                │
└────────────────────┴───────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```
### Stack traces of the working threads from the pools

```
SET allow_introspection_functions = 1;

WITH arrayMap(x -> demangle(addressToSymbol(x)), trace) AS all
SELECT
    thread_id,
    query_id,
    arrayStringConcat(all, '\n') AS res
FROM system.stack_trace
WHERE res ILIKE '%Pool%'
FORMAT Vertical;

```
# 5\.65 \- Who ate my ClickHouse® memory?
