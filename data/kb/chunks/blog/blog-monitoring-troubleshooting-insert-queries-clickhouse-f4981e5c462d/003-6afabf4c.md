---
source: blog
url: https://clickhouse.com/blog/clickhouse-cloud-generally-available
topic: essential-monitoring-queries-part-1-insert-queries
ch_version_introduced: '0.25'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 8
---

process is visualized below, with an indication of the relevant log file at each stage. ![insert_logs.png](/uploads/insert_logs_c3f274c6c6.png) We can use the query below to review how many (and how often) new parts are created during the last two hours.

```

SELECT
    count() AS new_parts,
    toStartOfMinute(event_time) AS modification_time_m,
    table,
    sum(rows) AS total_written_rows,
    formatReadableSize(sum(size_in_bytes)) AS total_bytes_on_disk
FROM clusterAllReplicas(default, system.part_log)
WHERE (event_type = 'NewPart') AND (event_time > (now() - toIntervalHour(2)))
GROUP BY
    modification_time_m,
    table
ORDER BY
    modification_time_m ASC,
    table DESC


```

![part_log.png](/uploads/part_log_3121218d57.png)
**This first query also applies to synchronous inserts.**

We can also use the `system.asynchronous_insert_log` table to review each async insert's status. The result of the following query is ordered by `flush_time` with the results allowing us to determine when the data was inserted (multiple lines can belong to the same flush, you can group by flush\_query\_id in order to have one line per flush).

```

SELECT
    event_time,
    query,
    database,
    table,
    bytes,
    status,
    flush_time
FROM clusterAllReplicas(default, system.asynchronous_insert_log)
ORDER BY flush_time DESC


```

![async_query_log.png](/uploads/async_query_log_f39c1dc4eb.png)
### Monitoring Synchronous Inserts [\#](/blog/monitoring-troubleshooting-insert-queries-clickhouse#monitoring-synchronous-inserts)

While in most cases, asynchronous inserts are the most practical means of inserting data, users may not be using this approach if they can batch their insert requests client\-side or are performing a bulk load.

For synchronous inserts, in addition to watching the number of new parts created, users should monitor the **number of insert [bulk requests](https://clickhouse.com/docs/en/cloud/bestpractices/bulk-inserts/)** that have been processed and the **total written rows**. There should be a big difference between these metrics. If not, this means you are inserting a small number of rows on each INSERT SQL request which can produce errors such as [`DB::Exception: Too many parts`](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse).

We will use two different system tables to collect these two metrics.

1. The table `system.query_logs` will provide us with the metric about how many Insert [bulk requests](https://clickhouse.com/docs/en/cloud/bestpractices/bulk-inserts/) have been processed by the ClickHouse service \- specifically, for the query below, see the value of `nb_bulk_inserts`.

```

SELECT
    toStartOfMinute(event_time) AS event_time_m,
    count(*) AS nb_bulk_inserts
FROM clusterAllReplicas(default, system.query_log)
WHERE (query ILIKE '%insert%') AND (query_kind = 'Insert') AND (type = 'QueryFinish') AND (NOT (Settings['async_insert']) = '1') AND (event_time > (now() - toIntervalDay(3)))
GROUP BY event_time_m
ORDER BY event_time_m ASC


```
