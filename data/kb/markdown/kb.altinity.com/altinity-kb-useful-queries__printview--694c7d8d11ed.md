# Useful queries \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-useful-queries/).

# Useful queries

Access useful ClickHouse® queries, from finding database size, missing blocks, checking table metadata in Zookeeper, and more.- 1: [Check table metadata in zookeeper](#pg-07b94601e094c2af24d5cb38fd024f0a)
- 2: [Compare query\_log for 2 intervals](#pg-5704f78981a895262d6be648b83055ef)
- 3: [Debug hanging thing](#pg-cf943ceb9a63bdd48ef3b4fd52fba64e)
- 4: [Handy queries for system.query\_log](#pg-10f25820508d00c9e0650390a42361ea)
- 5: [Ingestion metrics from system.part\_log](#pg-c45e95d27689195552b92b57b6e44e8d)
- 6: [Remove block numbers from zookeeper for removed partitions](#pg-52ff6ae5cace35380f31225e9337f9db)
- 7: [Removing tasks in the replication queue related to empty partitions](#pg-48b5b2d5ec6823f5b4efbd375404d976)
- 8: [Can detached parts in ClickHouse® be dropped?](#pg-d513ecaa3a77a116065353cc360a57fc)
- 9: [Database Size \- Table \- Column size](#pg-d276b38fbf7a101890ac65681f9fc6ab)
- 10: [Notes on Various Errors with respect to replication and distributed connections](#pg-35d18dd8d848bd0bf334ae49489d8f1e)
- 11: [Number of active parts in a partition](#pg-adffc17f31e6074c402b6b2a4353932d)
- 12: [Parts consistency](#pg-db303ad1636093488b37a8d1b16311e4)

# 1 \- Check table metadata in zookeeper

Check table metadata in zookeeper.## Compare table metadata of different replicas in zookeeper


> Check if a table is consistent across all zookeeper replicas. From each replica, returns metdadata, columns, and is\_active nodes. Checks whether each replica’s value matches the previous replica’s value, and flags any mismatches (looks\_good \= 0\).


```
SELECT
    *,
    if(
        prev_name = name AND name != 'is_active',
        prev_value = value,
        1
    ) AS looks_good
FROM (
    SELECT
        name,
        path,
        ctime,
        mtime,
        value,
        lagInFrame(name)  OVER w AS prev_name,
        lagInFrame(value) OVER w AS prev_value
    FROM system.zookeeper
    WHERE (path IN (
        SELECT arrayJoin(groupUniqArray(if(path LIKE '%/replicas', concat(path, '/', name), path)))
        FROM system.zookeeper
        WHERE path IN (
            SELECT arrayJoin([zookeeper_path, concat(zookeeper_path, '/replicas')])
            FROM system.replicas
            WHERE table = 'test_repl'
        )
    )) AND (name IN ('metadata', 'columns', 'is_active'))
    WINDOW w AS (ORDER BY name = 'is_active', name ASC, path ASC
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
)

```

> Returns a table’s create\_table\_query, and the last time the table’s metadata was modified


```
SELECT metadata_modification_time, create_table_query
FROM system.tables
WHERE name = 'test_repl'

```
# 2 \- Compare query\_log for 2 intervals

Compare query performance across different time periods
> Looks at unique query shapes (by normalized\_query\_hash) which occurred within two different time intervals (“before” and “after”), and returns performance metrics for each query pattern which performed worse in the “after” interval.


```
WITH 
    toStartOfInterval(event_time, INTERVAL 5 MINUTE) = '2023-06-30 13:00:00' as before,
    toStartOfInterval(event_time, INTERVAL 5 MINUTE) = '2023-06-30 15:00:00' as after
SELECT
    normalized_query_hash,
    anyIf(query, before) AS QueryBefore,
    anyIf(query, after) AS QueryAfter,
    countIf(before) as CountBefore,
    sumIf(query_duration_ms, before) / 1000 AS QueriesDurationBefore,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'RealTimeMicroseconds')], before) / 1000000 AS RealTimeBefore,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'UserTimeMicroseconds')], before) / 1000000 AS UserTimeBefore,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'SystemTimeMicroseconds')], before) / 1000000 AS SystemTimeBefore,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'DiskReadElapsedMicroseconds')], before) / 1000000 AS DiskReadTimeBefore,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'DiskWriteElapsedMicroseconds')], before) / 1000000 AS DiskWriteTimeBefore,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'NetworkSendElapsedMicroseconds')], before) / 1000000 AS NetworkSendTimeBefore,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'NetworkReceiveElapsedMicroseconds')], before) / 1000000 AS NetworkReceiveTimeBefore,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'ZooKeeperWaitMicroseconds')], before) / 1000000 AS ZooKeeperWaitTimeBefore,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'OSIOWaitMicroseconds')], before) / 1000000 AS OSIOWaitTimeBefore,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'OSCPUWaitMicroseconds')], before) / 1000000 AS OSCPUWaitTimeBefore,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'OSCPUVirtualTimeMicroseconds')], before) / 1000000 AS OSCPUVirtualTimeBefore,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'SelectedBytes')], before)  AS SelectedBytesBefore, 
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'SelectedRanges')], before)  AS SelectedRangesBefore,
    sumIf(read_rows, before) AS ReadRowsBefore,
    formatReadableSize(sumIf(read_bytes, before) AS ReadBytesBefore),
    sumIf(written_rows, before) AS WrittenTowsBefore,
    formatReadableSize(sumIf(written_bytes, before)) AS WrittenBytesBefore,
    sumIf(result_rows, before) AS ResultRowsBefore,
    formatReadableSize(sumIf(result_bytes, before)) AS ResultBytesBefore,

    countIf(after) as CountAfter,
    sumIf(query_duration_ms, after) / 1000 AS QueriesDurationAfter,
   sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'RealTimeMicroseconds')], after) / 1000000 AS RealTimeAfter,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'UserTimeMicroseconds')], after) / 1000000 AS UserTimeAfter,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'SystemTimeMicroseconds')], after) / 1000000 AS SystemTimeAfter,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'DiskReadElapsedMicroseconds')], after) / 1000000 AS DiskReadTimeAfter,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'DiskWriteElapsedMicroseconds')], after) / 1000000 AS DiskWriteTimeAfter,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'NetworkSendElapsedMicroseconds')], after) / 1000000 AS NetworkSendTimeAfter,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'NetworkReceiveElapsedMicroseconds')], after) / 1000000 AS NetworkReceiveTimeAfter,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'ZooKeeperWaitMicroseconds')], after) / 1000000 AS ZooKeeperWaitTimeAfter,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'OSIOWaitMicroseconds')], after) / 1000000 AS OSIOWaitTimeAfter,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'OSCPUWaitMicroseconds')], after) / 1000000 AS OSCPUWaitTimeAfter,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'OSCPUVirtualTimeMicroseconds')], after) / 1000000 AS OSCPUVirtualTimeAfter,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'SelectedBytes')], after)  AS SelectedBytesAfter,
    sumIf(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'SelectedRanges')], after)  AS SelectedRangesAfter,

    sumIf(read_rows, after) AS ReadRowsAfter,
    formatReadableSize(sumIf(read_bytes, after) AS ReadBytesAfter),
    sumIf(written_rows, after) AS WrittenTowsAfter,
    formatReadableSize(sumIf(written_bytes, after)) AS WrittenBytesAfter,
    sumIf(result_rows, after) AS ResultRowsAfter,
    formatReadableSize(sumIf(result_bytes, after)) AS ResultBytesAfter

FROM system.query_log
WHERE (before OR after) AND type in (2,4) -- QueryFinish, ExceptionWhileProcessing
GROUP BY normalized_query_hash
    WITH TOTALS
ORDER BY SelectedRangesAfter- SelectedRangesBefore DESC
LIMIT 10
FORMAT Vertical

```

> Looks at the system.query\_log in a window (in this case, 3 days) prior to and following a specified timestamp of interest. Returns performance metrics for each query pattern which performed worse after that timestamp.


```
WITH 
    toDateTime('2024-02-09 00:00:00') as timestamp_of_issue,
    event_time < timestamp_of_issue as before,
    event_time >= timestamp_of_issue as after
select
    normalized_query_hash as h,
    any(query) as query_sample,
    round(quantileIf(0.9)(query_duration_ms, before)) as duration_q90_before,
    round(quantileIf(0.9)(query_duration_ms, after))  as duration_q90_after,
    countIf(before) as cnt_before,
    countIf(after) as cnt_after,
    sumIf(query_duration_ms,before) as duration_sum_before,
    sumIf(query_duration_ms,after) as duration_sum_after,
    sumIf(ProfileEvents['UserTimeMicroseconds'], before) as usertime_sum_before,
    sumIf(ProfileEvents['UserTimeMicroseconds'], after) as usertime_sum_after,
    sumIf(read_bytes,before) as sum_read_bytes_before,
    sumIf(read_bytes,after) as sum_read_bytes_after
from system.query_log
where event_time between timestamp_of_issue - INTERVAL 3 DAY and timestamp_of_issue + INTERVAL 3 DAY
group by h
HAVING cnt_after > 1.1 * cnt_before OR sum_read_bytes_after > 1.2 * sum_read_bytes_before OR usertime_sum_after > 1.2 * usertime_sum_before
ORDER BY sum_read_bytes_after - sum_read_bytes_before 
FORMAT Vertical

```
# 3 \- Debug hanging thing

Debug hanging / freezing things## Debug hanging / freezing things

If ClickHouse® is busy with something and you don’t know what’s happening, you can easily check the stacktraces of all the thread which are working


```
SELECT
 arrayStringConcat(arrayMap(x -> concat('0x', lower(hex(x)), '\t', demangle(addressToSymbol(x))), trace), '\n') as trace_functions,
 count()
FROM system.stack_trace
GROUP BY trace_functions
ORDER BY count()
DESC
SETTINGS allow_introspection_functions=1
FORMAT Vertical;

```
If you can’t start any queries, but you have access to the node, you can sent a signal


```
# older versions
for i in $(ls -1 /proc/$(pidof clickhouse-server)/task/); do kill -TSTP $i; done
# even older versions
for i in $(ls -1 /proc/$(pidof clickhouse-server)/task/); do kill -SIGPROF $i; done

```
# 4 \- Handy queries for system.query\_log

Useful queries for analyzing query performance, resource usage, and overall query statistics## Most resource\-intensive queries


> For each query (cluster\-wide, grouped by query hash and ordered by time), reports:

- Latency\-related metrics: CPU time categories, disk read and write time, network send and receive time, Zookeeper wait time
- Data size\-related metrics: counts of bytes and rows read/written, parts/ranges/marks read, files opened, and memory used
- Cache hit performance


```
SELECT 
    hostName() as host,
    normalized_query_hash,
    min(event_time),
    max(event_time),
    replace(substr(argMax(query, utime), 1, 80), '\n', ' ') AS query,
    argMax(query_id, utime) AS sample_query_id,
    count(),
    sum(query_duration_ms) / 1000 AS QueriesDuration, /* wall clock */
    sum(ProfileEvents['RealTimeMicroseconds']) / 1000000 AS RealTime,  /* same as above but x number of thread */
    sum(ProfileEvents['UserTimeMicroseconds'] as utime) / 1000000 AS UserTime,  /* time when our query was doin some cpu-insense work, creating cpu load */
    sum(ProfileEvents['SystemTimeMicroseconds']) / 1000000 AS SystemTime, /* time spend on waiting for some system operations */
    sum(ProfileEvents['DiskReadElapsedMicroseconds']) / 1000000 AS DiskReadTime,
    sum(ProfileEvents['DiskWriteElapsedMicroseconds']) / 1000000 AS DiskWriteTime,
    sum(ProfileEvents['NetworkSendElapsedMicroseconds']) / 1000000 AS NetworkSendTime, /* check the other side of the network! */
    sum(ProfileEvents['NetworkReceiveElapsedMicroseconds']) / 1000000 AS NetworkReceiveTime, /* check the other side of the network! */
    sum(ProfileEvents['ZooKeeperWaitMicroseconds']) / 1000000 AS ZooKeeperWaitTime,
    sum(ProfileEvents['OSIOWaitMicroseconds']) / 1000000 AS OSIOWaitTime, /* IO waits, usually disks - that metric is 'orthogonal' to other */ 
    sum(ProfileEvents['OSCPUWaitMicroseconds']) / 1000000 AS OSCPUWaitTime, /* waiting for a 'free' CPU - usually high when the other load on the server creates a lot of contention for cpu */ 
    sum(ProfileEvents['OSCPUVirtualTimeMicroseconds']) / 1000000 AS OSCPUVirtualTime, /* similar to usertime + system time */
    formatReadableSize(sum(ProfileEvents['NetworkReceiveBytes']) as network_receive_bytes) AS NetworkReceiveBytes,
    formatReadableSize(sum(ProfileEvents['NetworkSendBytes']) as network_send_bytes) AS NetworkSendBytes,
    sum(ProfileEvents['SelectedParts']) as SelectedParts,
    sum(ProfileEvents['SelectedRanges']) as SelectedRanges,
    sum(ProfileEvents['SelectedMarks']) as SelectedMarks,
    sum(ProfileEvents['SelectedRows']) as SelectedRows,  /* those may different from read_rows - here the number or rows potentially matching the where conditions, not neccessary all will be read */
    sum(ProfileEvents['SelectedBytes']) as SelectedBytes,
    sum(ProfileEvents['FileOpen']) as FileOpen,
    sum(ProfileEvents['ZooKeeperTransactions']) as ZooKeeperTransactions,
    formatReadableSize(sum(ProfileEvents['OSReadBytes'] ) as os_read_bytes ) as OSReadBytesExcludePageCache,
    formatReadableSize(sum(ProfileEvents['OSWriteBytes'] ) as os_write_bytes ) as OSWriteBytesExcludePageCache,
    formatReadableSize(sum(ProfileEvents['OSReadChars'] ) as os_read_chars ) as OSReadCharsIncludePageCache,
    formatReadableSize(sum(ProfileEvents['OSWriteChars'] ) as os_write_chars ) as OSWriteCharsIncludePageCache,
    formatReadableSize(quantile(0.97)(memory_usage) as memory_usage_q97) as MemoryUsageQ97 ,
    sum(read_rows) AS ReadRows,
    formatReadableSize(sum(read_bytes) as read_bytes_sum) AS ReadBytes,
    sum(written_rows) AS WrittenRows,
    formatReadableSize(sum(written_bytes) as written_bytes_sum) AS WrittenBytes, /* */
    sum(result_rows) AS ResultRows,
    formatReadableSize(sum(result_bytes) as result_bytes_sum) AS ResultBytes
FROM clusterAllReplicas('{cluster}', system.query_log)
WHERE event_date >= today() AND type in (2,4)-- QueryFinish, ExceptionWhileProcessing
GROUP BY
    GROUPING SETS (
        (normalized_query_hash, host),
        (host),
        ())
ORDER BY OSCPUVirtualTime DESC
LIMIT 30
FORMAT Vertical;

```

> Similar to above, for older ClickHouse versions (pre\-22\.4\). Returns the slowest queries from a single host along with elements of latency.


```
SELECT
    normalized_query_hash,
    any(query),
    count(),
    sum(query_duration_ms) / 1000 AS QueriesDuration,
    sum(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'RealTimeMicroseconds')]) / 1000000 AS RealTime,
    sum(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'UserTimeMicroseconds')]) / 1000000 AS UserTime,
    sum(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'SystemTimeMicroseconds')]) / 1000000 AS SystemTime,
    sum(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'DiskReadElapsedMicroseconds')]) / 1000000 AS DiskReadTime,
    sum(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'DiskWriteElapsedMicroseconds')]) / 1000000 AS DiskWriteTime,
    sum(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'NetworkSendElapsedMicroseconds')]) / 1000000 AS NetworkSendTime,
    sum(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'NetworkReceiveElapsedMicroseconds')]) / 1000000 AS NetworkReceiveTime,
    sum(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'ZooKeeperWaitMicroseconds')]) / 1000000 AS ZooKeeperWaitTime,
    sum(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'OSIOWaitMicroseconds')]) / 1000000 AS OSIOWaitTime,
    sum(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'OSCPUWaitMicroseconds')]) / 1000000 AS OSCPUWaitTime,
    sum(ProfileEvents.Values[indexOf(ProfileEvents.Names, 'OSCPUVirtualTimeMicroseconds')]) / 1000000 AS OSCPUVirtualTime,
    sum(read_rows) AS ReadRows,
    formatReadableSize(sum(read_bytes)) AS ReadBytes,
    sum(written_rows) AS WrittenTows,
    formatReadableSize(sum(written_bytes)) AS WrittenBytes,
    sum(result_rows) AS ResultRows,
    formatReadableSize(sum(result_bytes)) AS ResultBytes
FROM system.query_log
WHERE (event_date >= today()) AND (event_time > (now() - 3600)) AND type in (2,4) -- QueryFinish, ExceptionWhileProcessing
GROUP BY normalized_query_hash
    WITH TOTALS
ORDER BY UserTime DESC
LIMIT 30
FORMAT Vertical

```
## A/B tests of the same query


> Runs cluster\-wide, returns a side\-by\-side comparison of performance metrics, ordered by relative difference


```
WITH
	query_id='8c050082-428e-4523-847a-caf29511d6ba' AS first,
	query_id='618e0c55-e21d-4630-97e7-5f82e2475c32' AS second,
	arrayConcat(mapKeys(ProfileEvents), ['query_duration_ms', 'read_rows', 'read_bytes', 'written_rows', 'written_bytes', 'result_rows', 'result_bytes', 'memory_usage', 'normalized_query_hash', 'peak_threads_usage', 'query_cache_usage']) AS metrics,
	arrayConcat(mapValues(ProfileEvents), [query_duration_ms, read_rows, read_bytes, written_rows, written_bytes, result_rows, result_bytes, memory_usage, normalized_query_hash, peak_threads_usage, toUInt64(query_cache_usage)]) AS metrics_values
SELECT
	metrics[i] AS metric,
	anyIf(metrics_values[i], first) AS v1,
	anyIf(metrics_values[i], second) AS v2,
	formatReadableQuantity(v1 - v2)
FROM clusterAllReplicas(default, system.query_log)
ARRAY JOIN arrayEnumerate(metrics) AS i
WHERE (first OR second) AND (type = 2)
GROUP BY metric
HAVING v1 != v2
ORDER BY
	(v2 - v1) / (v1 + v2) DESC,
	v2 DESC,
	metric ASC

```

> Compares two queries run on the same host in the past day, returning the metrics highlighting the most significant performance differences between the faster and slower query


```
WITH
    'd18fb820-4075-49bf-8fa3-cd7e53b9d523' AS fast_query_id,
    '22ffbcc0-c62a-4895-8105-ee9d7447a643' AS slow_query_id,
    faster AS
    (
        SELECT pe.1 AS event_name, pe.2 AS event_value
        FROM
        (
            SELECT ProfileEvents.Names, ProfileEvents.Values
            FROM system.query_log
            WHERE (query_id = fast_query_id ) AND (type = 'QueryFinish') AND (event_date = today())
        )
        ARRAY JOIN arrayZip(ProfileEvents.Names, ProfileEvents.Values) AS pe
    ),
    slower AS
    (
        SELECT pe.1 AS event_name, pe.2 AS event_value
        FROM
        (
            SELECT ProfileEvents.Names, ProfileEvents.Values
            FROM system.query_log
            WHERE (query_id = slow_query_id) AND (type = 'QueryFinish') AND (event_date = today())
        )
        ARRAY JOIN arrayZip(ProfileEvents.Names, ProfileEvents.Values) AS pe
    )
SELECT
    event_name,
    formatReadableQuantity(slower.event_value) AS slower_value,
    formatReadableQuantity(faster.event_value) AS faster_value,
    round((slower.event_value - faster.event_value) / slower.event_value, 2) AS diff_q
FROM faster
LEFT JOIN slower USING (event_name)
WHERE diff_q > 0.05
ORDER BY event_name ASC
SETTINGS join_use_nulls = 1

```
## Queries which did not complete within specified timeframe


> For a given time range, returns queries which either did not complete, or did not complete within a configurable timeframe (100 seconds)


```
SELECT
  query_id,
  min(event_time) t,
  any(query)
FROM system.query_log
WHERE event_date = today() AND event_time > '2021-11-25 02:29:12'
GROUP BY query_id
HAVING countIf(type='QueryFinish') = 0 OR sum(query_duration_ms) > 100000
ORDER BY t;

```

> Returns queries which started within a specified timeframe but did not complete successfully (still running, crashed, threw exception)


```
SELECT
     query_id,
     any(query)
FROM system.query_log
WHERE event_time BETWEEN '2021-09-24 07:00:00' AND '2021-09-24 09:00:00'
GROUP BY query_id HAVING countIf(type=1) <> countIf(type!=1)

```
## Columns used in WHERE clauses


> Returns a list of columns which are used as filters against a table. Replace %target\_table% with the actual table name (or pattern) you want to inspect.


```
WITH
    any(query) AS q,
    any(tables) AS _tables,
    arrayJoin(extractAll(query, '\\b(?:PRE)?WHERE\\s+(.*?)\\s+(?:GROUP BY|ORDER BY|UNION|SETTINGS|FORMAT$)')) AS w,
    any(columns) AS cols,
    arrayFilter(x -> (position(w, extract(x, '\\.(`[^`]+`|[^\\.]+)$')) > 0), columns) AS c,
    arrayJoin(c) AS c2
SELECT
    c2,
    count()
FROM system.query_log
WHERE (event_time >= (now() - toIntervalDay(1)))
  AND arrayExists(x -> (x LIKE '%target_table%'), tables)
  AND (query ILIKE 'SELECT%')
GROUP BY c2
ORDER BY count() ASC;

```
## Most‑selected columns


> Over the past week, which columns have been accessed the most frequently in SELECT queries


```
SELECT
    col AS column,
    count() AS hits
FROM system.query_log
ARRAY JOIN columns AS col          -- expand the column list first
WHERE type = 'QueryFinish'
  AND query_kind = 'Select'
  AND event_time >= now() - INTERVAL 7 DAY
  AND notEmpty(columns)
GROUP BY col
ORDER BY hits DESC
LIMIT 50;

```
## Most‑used functions


> Over the past week, which functions have been used the most


```
SELECT
    f AS function,
    count() AS hits
FROM system.query_log
ARRAY JOIN used_functions AS f  -- used_aggregate_functions, used_aggregate_function_combinators
WHERE type = 'QueryFinish'
  AND event_time >= now() - INTERVAL 7 DAY
  AND notEmpty(used_functions)
GROUP BY f
ORDER BY hits DESC
LIMIT 50;

```
## “Worst offender” query ranks


> Over a specified time range, returns the query shapes which appear to be the worst performing based on a range of ranked criteria


```
SELECT *
FROM 
(
SELECT 
    *,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY cnt DESC) as rank_by_cnt,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY QueriesDuration DESC) as rank_by_duration,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY RealTime DESC) as rank_by_real_time,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY UserTime DESC) as rank_by_user_time,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY SystemTime DESC) as rank_by_system_time,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY DiskReadTime DESC) as rank_by_disk_read_time,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY DiskWriteTime DESC) as rank_by_disk_write_time,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY NetworkSendTime DESC) as rank_by_network_send_time,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY NetworkReceiveTime DESC) as rank_by_network_receive_time,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY OSIOWaitTime DESC) as rank_by_os_io_wait_time,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY OSCPUWaitTime DESC) as rank_by_os_cpu_wait_time,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY OSCPUVirtualTime DESC) as rank_by_os_cpu_virtual_time,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY NetworkReceiveBytes DESC) as rank_by_network_receive_bytes,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY NetworkSendBytes DESC) as rank_by_network_send_bytes,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY SelectedParts DESC) as rank_by_selected_parts,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY SelectedRanges DESC) as rank_by_selected_ranges,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY SelectedMarks DESC) as rank_by_selected_marks,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY SelectedRows DESC) as rank_by_selected_rows,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY SelectedBytes DESC) as rank_by_selected_bytes,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY FileOpen DESC) as rank_by_file_open,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY ZooKeeperTransactions DESC) as rank_by_zookeeper_transactions,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY OSReadBytesExcludePageCache DESC) as rank_by_os_read_bytes_exclude_page_cache,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY OSWriteBytesExcludePageCache DESC) as rank_by_os_write_bytes_exclude_page_cache,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY OSReadBytesIncludePageCache DESC) as rank_by_os_read_bytes_include_page_cache,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY OSWriteCharsIncludePageCache DESC) as rank_by_os_write_chars_include_page_cache,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY MemoryUsageQ97 DESC) as rank_by_memory_usage_q97,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY ReadRows DESC) as rank_by_read_rows,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY ReadBytes DESC) as rank_by_read_bytes,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY WrittenRows DESC) as rank_by_written_rows,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY WrittenBytes DESC) as rank_by_written_bytes,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY ResultRows DESC) as rank_by_result_rows,
    DENSE_RANK() OVER (PARTITION BY host ORDER BY ResultBytes DESC) as rank_by_result_bytes
FROM
(
SELECT 
    hostName() as host,
    normalized_query_hash,
    min(event_time) as min_event_time,
    max(event_time) as max_event_time,
    replace(substr(argMax(query, utime), 1, 80), '\n', ' ') AS query,
    argMax(query_id, utime) AS sample_query_id,
    count() as cnt,
    sum(query_duration_ms) / 1000 AS QueriesDuration, /* wall clock */
    sum(ProfileEvents['RealTimeMicroseconds']) / 1000000 AS RealTime,  /* same as above but x number of thread */
    sum(ProfileEvents['UserTimeMicroseconds'] as utime) / 1000000 AS UserTime,  /* time when our query was doin some cpu-insense work, creating cpu load */
    sum(ProfileEvents['SystemTimeMicroseconds']) / 1000000 AS SystemTime, /* time spend on waiting for some system operations */
    sum(ProfileEvents['DiskReadElapsedMicroseconds']) / 1000000 AS DiskReadTime,
    sum(ProfileEvents['DiskWriteElapsedMicroseconds']) / 1000000 AS DiskWriteTime,
    sum(ProfileEvents['NetworkSendElapsedMicroseconds']) / 1000000 AS NetworkSendTime, /* check the other side of the network! */
    sum(ProfileEvents['NetworkReceiveElapsedMicroseconds']) / 1000000 AS NetworkReceiveTime, /* check the other side of the network! */
    sum(ProfileEvents['OSIOWaitMicroseconds']) / 1000000 AS OSIOWaitTime, /* IO waits, usually disks - that metric is 'orthogonal' to other */ 
    sum(ProfileEvents['OSCPUWaitMicroseconds']) / 1000000 AS OSCPUWaitTime, /* waiting for a 'free' CPU - usually high when the other load on the server creates a lot of contention for cpu */ 
    sum(ProfileEvents['OSCPUVirtualTimeMicroseconds']) / 1000000 AS OSCPUVirtualTime, /* similar to usertime + system time */
    sum(ProfileEvents['NetworkReceiveBytes']) AS NetworkReceiveBytes,
    sum(ProfileEvents['NetworkSendBytes']) AS NetworkSendBytes,
    sum(ProfileEvents['SelectedParts']) as SelectedParts,
    sum(ProfileEvents['SelectedRanges']) as SelectedRanges,
    sum(ProfileEvents['SelectedMarks']) as SelectedMarks,
    sum(ProfileEvents['SelectedRows']) as SelectedRows,  /* those may different from read_rows - here the number or rows potentially matching the where conditions, not neccessary all will be read */
    sum(ProfileEvents['SelectedBytes']) as SelectedBytes,
    sum(ProfileEvents['FileOpen']) as FileOpen,
    sum(ProfileEvents['ZooKeeperTransactions']) as ZooKeeperTransactions,
    sum(ProfileEvents['OSReadBytes'] )  as OSReadBytesExcludePageCache,
    sum(ProfileEvents['OSWriteBytes'] )  as OSWriteBytesExcludePageCache,
    sum(ProfileEvents['OSReadChars'] )  as OSReadBytesIncludePageCache,
    sum(ProfileEvents['OSWriteChars'] )  as OSWriteCharsIncludePageCache,
    quantile(0.97)(memory_usage)  as MemoryUsageQ97 ,
    sum(read_rows) AS ReadRows,
    sum(read_bytes) AS ReadBytes,
    sum(written_rows) AS WrittenRows,
    sum(written_bytes) AS WrittenBytes, /* */
    sum(result_rows) AS ResultRows,
    sum(result_bytes) AS ResultBytes
FROM clusterAllReplicas('{cluster}', system.query_log)
WHERE event_time BETWEEN '2024-04-04 11:31:10' and '2024-04-04 12:36:50' AND type in (2,4)-- QueryFinish, ExceptionWhileProcessing
GROUP BY normalized_query_hash, host
)
)
WHERE 
(rank_by_cnt <= 20 and cnt > 10)
OR (rank_by_duration <= 20 and QueriesDuration > 60)
OR (rank_by_real_time <= 20 and RealTime > 60)
OR (rank_by_user_time <= 20 and UserTime > 60)
OR (rank_by_system_time <= 20 and SystemTime > 60)
OR (rank_by_disk_read_time <= 20 and DiskReadTime > 60)
OR (rank_by_disk_write_time <= 20 and DiskWriteTime > 60)
OR (rank_by_network_send_time <= 20 and NetworkSendTime > 60)
OR (rank_by_network_receive_time <= 20 and NetworkReceiveTime > 60)
OR (rank_by_os_io_wait_time <= 20 and OSIOWaitTime > 60)
OR (rank_by_os_cpu_wait_time <= 20 and OSCPUWaitTime > 60)
OR (rank_by_os_cpu_virtual_time <= 20 and OSCPUVirtualTime > 60)
OR (rank_by_network_receive_bytes <= 20 and NetworkReceiveBytes > 500000000)
OR (rank_by_network_send_bytes <= 20 and NetworkSendBytes > 500000000)
OR (rank_by_selected_parts <= 20 and SelectedParts > 1000)
OR (rank_by_selected_ranges <= 20 and SelectedRanges > 1000)
OR (rank_by_selected_marks <= 20 and SelectedMarks > 1000)
OR (rank_by_selected_rows <= 20 and SelectedRows > 1000000)
OR (rank_by_selected_bytes <= 20 and SelectedBytes > 500000000)
OR (rank_by_file_open <= 20 and FileOpen > 1000)
OR (rank_by_zookeeper_transactions <= 20 and ZooKeeperTransactions > 10)
OR (rank_by_os_read_bytes_exclude_page_cache <= 20 and OSReadBytesExcludePageCache > 500000000)
OR (rank_by_os_write_bytes_exclude_page_cache <= 20 and OSWriteBytesExcludePageCache > 500000000)
OR (rank_by_os_read_bytes_include_page_cache <= 20 and OSReadBytesIncludePageCache > 500000000)
OR (rank_by_os_write_chars_include_page_cache <= 20 and OSWriteCharsIncludePageCache > 500000000)
OR (rank_by_memory_usage_q97 <= 20 and MemoryUsageQ97 > 500000000)
OR (rank_by_read_rows <= 20 and ReadRows > 100000)
OR (rank_by_read_bytes <= 20 and ReadBytes > 500000000)
OR (rank_by_written_rows <= 20 and WrittenRows > 100000)
OR (rank_by_written_bytes <= 20 and WrittenBytes > 500000000)
OR (rank_by_result_rows <= 20 and ResultRows > 100000)
OR (rank_by_result_bytes <= 20 and ResultBytes > 100000000)
ORDER BY rank_by_cnt*10 + rank_by_duration*10 + rank_by_real_time*10 + rank_by_user_time*10 + rank_by_system_time*10 + rank_by_disk_read_time*10 + rank_by_disk_write_time*5 + rank_by_network_send_time + rank_by_network_receive_time + rank_by_os_io_wait_time + rank_by_os_cpu_wait_time + rank_by_os_cpu_virtual_time*10 + rank_by_network_receive_bytes*8 + rank_by_network_send_bytes*8 + rank_by_selected_parts*5 + rank_by_selected_ranges*5 + rank_by_selected_marks*5 + rank_by_selected_rows*5 + rank_by_selected_bytes*5 + rank_by_file_open*5 + rank_by_zookeeper_transactions*5 + rank_by_os_read_bytes_exclude_page_cache*5 + rank_by_os_write_bytes_exclude_page_cache*5 + rank_by_os_read_bytes_include_page_cache*5 + rank_by_os_write_chars_include_page_cache*5 + rank_by_memory_usage_q97*10 + rank_by_read_rows*10 + rank_by_read_bytes*10 + rank_by_written_rows*8 + rank_by_written_bytes*8 + rank_by_result_rows*8 + rank_by_result_bytes*8 DESC

```
## Other resources

- [Compare query\_log for 2 intervals](https://kb.altinity.com/altinity-kb-useful-queries/compare_query_log_for_2_intervals/)
- [Monitoring INSERT Queries](https://clickhouse.com/blog/monitoring-troubleshooting-insert-queries-clickhouse)
- [Monitoring SELECT Queries](https://clickhouse.com/blog/monitoring-troubleshooting-select-queries-clickhouse)
- [SYSTEM TABLES](https://clickhouse.com/blog/clickhouse-debugging-issues-with-system-tables)
- [Know Your Clickhouse](https://azat.sh/presentations/2022-know-your-clickhouse/)
# 5 \- Ingestion metrics from system.part\_log

Query to gather information about ingestion rate from system.part\_log.## Insert rate


> Returns aggregated insert metrics, per table, for the current day (by default), including parts per insert, rows/bytes per insert, and rows/bytes per part.


```
select database, table, time_bucket,
       max(number_of_parts_per_insert) max_parts_pi,
       median(number_of_parts_per_insert) median_parts_pi,
       min(min_rows_per_part) min_rows_pp, 
       max(max_rows_per_part) max_rows_pp, 
       median(median_rows_per_part) median_rows_pp,
       min(rows_per_insert) min_rows_pi, 
       median(rows_per_insert) median_rows_pi, 
       max(rows_per_insert) max_rows_pi, 
       sum(rows_per_insert) rows_inserted,
       sum(seconds_per_insert) parts_creation_seconds,
       count() inserts,
       sum(number_of_parts_per_insert) new_parts,
       max(last_part_pi) - min(first_part_pi) as insert_period,
       inserts*60/insert_period as inserts_per_minute
from
(SELECT 
	database, 
	table,
	toStartOfDay(event_time) AS time_bucket, 
	count() AS number_of_parts_per_insert,
	min(rows) AS min_rows_per_part,
	max(rows) AS max_rows_per_part, 
	median(rows) AS median_rows_per_part,
	sum(rows) AS rows_per_insert, 
	min(size_in_bytes) AS min_bytes_per_part, 
	max(size_in_bytes) AS max_bytes_per_part,
	median(size_in_bytes) AS median_bytes_per_part, 
	sum(size_in_bytes) AS bytes_per_insert, 
	median_bytes_per_part / median_rows_per_part AS avg_row_size,
	sum(duration_ms)/1000 as seconds_per_insert,
	max(event_time) as last_part_pi,  min(event_time) as first_part_pi
FROM 
	system.part_log
WHERE 
  -- Enum8('NewPart' = 1, 'MergeParts' = 2, 'DownloadPart' = 3, 'RemovePart' = 4, 'MutatePart' = 5, 'MovePart' = 6)
	event_type = 1 
	AND 
  -- change if another time period is desired
	event_date >= today()
GROUP BY query_id, database, table, time_bucket
)
GROUP BY database, table, time_bucket
ORDER BY time_bucket, database, table ASC

```
## New parts per partition


> Returns new part counts and average rows per table for the current day (by default)


```
select database, table, event_type, partition_id, count() c, round(avg(rows)) 
from system.part_log where event_date >= today() and event_type = 'NewPart'
group by database, table, event_type, partition_id
order by c desc

```
## Too fast inserts


> Returns new part counts and average rows by minute by table

Should not be more often than 1 new part per table per second (60 inserts per minute)
One insert can create several parts because of partitioning and materialized views attached.


```
select toStartOfMinute(event_time) t, database, table, count() c, round(avg(rows)) 
from system.part_log
where event_date >= today()
  and event_type = 'NewPart'
  --and event_time > now() - 3600
group by database, table, t
order by t

```
# 6 \- Remove block numbers from zookeeper for removed partitions

## Remove block numbers from zookeeper for removed partitions


```
SELECT distinct concat('delete ', zk.block_numbers_path, zk.partition_id) FROM
(
    SELECT r.database, r.table, zk.block_numbers_path, zk.partition_id, p.partition_id
    FROM 
    (
        SELECT path as block_numbers_path, name as partition_id
        FROM system.zookeeper
        WHERE path IN (
            SELECT concat(zookeeper_path, '/block_numbers/') as block_numbers_path
            FROM clusterAllReplicas('{cluster}',system.replicas)
        )
    ) as zk 
    LEFT JOIN 
    (
            SELECT database, table, concat(zookeeper_path, '/block_numbers/') as block_numbers_path
            FROM clusterAllReplicas('{cluster}',system.replicas)
    )
    as r ON (r.block_numbers_path = zk.block_numbers_path) 
    LEFT JOIN 
    (
        SELECT DISTINCT partition_id, database, table
        FROM clusterAllReplicas('{cluster}',system.parts)
    )
    as p ON (p.partition_id = zk.partition_id AND p.database = r.database AND p.table = r.table)
    WHERE p.partition_id = ''  AND zk.partition_id <> 'all'
    ORDER BY r.database, r.table, zk.block_numbers_path, zk.partition_id, p.partition_id
) t
FORMAT TSVRaw;

```
## After 24\.3


```
WITH 
  now() - INTERVAL 120 DAY as retain_old_partitions,
  replicas AS (SELECT DISTINCT database, table, zookeeper_path || '/block_numbers' AS block_numbers_path FROM system.replicas),
  zk_data AS (SELECT DISTINCT name as partition_id, path as block_numbers_path FROM system.zookeeper WHERE path IN (SELECT block_numbers_path FROM replicas) AND mtime < retain_old_partitions AND partition_id <> 'all'),
  zk_partitions AS (SELECT DISTINCT database, table, partition_id FROM replicas JOIN zk_data USING block_numbers_path),
  partitions AS (SELECT DISTINCT database, table, partition_id FROM system.parts)
SELECT 
  format('ALTER TABLE `{}`.`{}` {};',database, table, arrayStringConcat( arraySort(groupArray('FORGET PARTITION ID \'' || partition_id || '\'')), ', ')) AS query
FROM zk_partitions
WHERE (database, table, partition_id) NOT IN (SELECT * FROM partitions) 
GROUP BY database, table
ORDER BY database, table
FORMAT TSVRaw;

```
## After fixing <https://github.com/ClickHouse/ClickHouse/issues/72807>


```
WITH 
  now() - INTERVAL 120 DAY as retain_old_partitions,
  replicas AS (SELECT DISTINCT database, table, zookeeper_path || '/block_numbers' AS block_numbers_path FROM clusterAllReplicas('{cluster}',system.replicas)),
  zk_data AS (SELECT DISTINCT name as partition_id, path as block_numbers_path FROM system.zookeeper WHERE path IN (SELECT block_numbers_path FROM replicas) AND mtime < retain_old_partitions AND partition_id <> 'all'),
  zk_partitions AS (SELECT DISTINCT database, table, partition_id FROM replicas JOIN zk_data USING block_numbers_path),
  partitions AS (SELECT DISTINCT database, table, partition_id FROM clusterAllReplicas('{cluster}',system.parts))
SELECT 
  format('ALTER TABLE `{}`.`{}` ON CLUSTER \'{{cluster}}\' {};',database, table, arrayStringConcat( arraySort(groupArray('FORGET PARTITION ID \'' || partition_id || '\'')), ', ')) AS query
FROM zk_partitions
WHERE (database, table, partition_id) NOT IN (SELECT * FROM partitions) 
GROUP BY database, table
ORDER BY database, table
FORMAT TSVRaw;

```
# 7 \- Removing tasks in the replication queue related to empty partitions

Removing tasks in the replication queue related to empty partitions## Removing tasks in the replication queue related to empty partitions


```
SELECT 'ALTER TABLE ' || database || '.' || table || ' DROP PARTITION ID \''|| partition_id || '\';'  FROM 
(SELECT DISTINCT database, table, extract(new_part_name, '^[^_]+')  as partition_id FROM clusterAllReplicas('{cluster}', system.replication_queue) ) as rq
LEFT JOIN 
(SELECT database, table, partition_id, sum(rows) as rows_count, count() as part_count 
FROM clusterAllReplicas('{cluster}', system.parts)
WHERE active GROUP BY database, table, partition_id
)  as p
USING (database, table, partition_id)
WHERE p.rows_count = 0 AND p.part_count = 0
FORMAT TSVRaw;

```
# 8 \- Can detached parts in ClickHouse® be dropped?

Cleaning up detached parts without data loss### Overview

This article explains detached parts in ClickHouse®: why they appear, what detached reasons mean, and how to clean up safely.

Use it when investigating:

You can perform two main operations with detached parts:

- **Recovery**: If you’re missing data due to misconfiguration or an error (such as connecting to the wrong ZooKeeper), check the detached parts. The missing data might be recoverable through manual intervention.
- **Cleanup**: Otherwise, clean up the detached parts periodically to free disk space.

### Version Scope

Primary scope: **ClickHouse 23\.10\+**.

Compatibility note:

- In **22\.6\-23\.9**, there was optional timeout\-based auto\-removal for some detached reasons.
- In **23\.10\+**, this option was removed; detached\-part cleanup is intentionally manual.

Important distinction for ReplicatedMergeTree: ClickHouse® tracks expected parts from ZooKeeper and unexpected parts found locally:

- Broken expected parts increment the `max_suspicious_broken_parts` counter (can block startup).
- Broken unexpected parts use a separate counter and do not block startup.

### Detailed actions based on the `status` of detached parts:

- **Safe to delete (after validation):**


	- ignored
	- clone.
- **Temporary, do not delete while in progress:**


	- attaching
	- deleting
	- tmp\-fetch.
- **Investigate before deleting:**


	- broken
	- broken\-on\-start
	- broken\-from\-backup
	- covered\-by\-broken
	- noquorum
	- merge\-not\-byte\-identical
	- mutate\-not\-byte\-identical

### Monitoring of detached parts

You can find information in `clickhouse-server.log`, for what happened when the parts were detached during startup. If `clickhouse-server.log` is lost it might be impossible to figure out what happened and why the parts were detached.

Another good source of information is `system.part_log` table, which can be used to investigate the history/timeline of specific parts involved in the detaching process:


```
SELECT
    event_time,
    event_type,
    database,
    `table`,
    part_name,
    partition_id,
    rows,
    size_in_bytes,
    merged_from,
    error,
    exception
FROM system.part_log
WHERE part_name IN ('all_1_5_0', 'all_6_10_1') -- example part names, replace with actual part names from detached_parts or clickhouse-server.log
ORDER BY
    part_name ASC,
    event_time ASC

```
Also `system.detached_parts` table contains useful information:


```
SELECT
    database,
    table,
    reason,
    count() AS parts
FROM system.detached_parts
GROUP BY database, table, reason
ORDER BY database ASC, table ASC, reason ASC

```
It is important to monitor for detached parts and act quickly when they appear. You can use `system.asynchronous_metric/metric_log` to track some metrics.

Use `system.asynchronous_metrics` for current values:


```
SELECT metric, value
FROM system.asynchronous_metrics
WHERE metric IN ('NumberOfDetachedParts', 'NumberOfDetachedByUserParts')
ORDER BY metric;

```
Use `system.asynchronous_metric_log` for history/trends:


```
SELECT
    event_time,
    metric,
    value
FROM system.asynchronous_metric_log
WHERE metric IN ('NumberOfDetachedParts', 'NumberOfDetachedByUserParts')
  AND event_time > now() - INTERVAL 24 HOUR
ORDER BY event_time DESC, metric;

```
### DROP DETACHED command

The DROP DETACHED command in ClickHouse® is used to remove parts or partitions that have previously been detached (i.e., moved to the detached directory and forgotten by the server). The syntax is:

#### Warning

Be careful before dropping any detached part or partition. Validate that data is no longer needed and keep a backup before running destructive commands.
```
ALTER TABLE table_name [ON CLUSTER cluster] DROP DETACHED PARTITION|PART ALL|partition_expr

```
This command removes the specified part or all parts of the specified partition from the detached directory. For more details on how to specify the partition expression, see the documentation on how to set the partition expression DROP DETACHED PARTITION\|PART.

Note: You must have the `allow_drop_detached` setting enabled to use this command.

#### DROP DML

#### Warning

Review generated `DROP DETACHED` commands carefully before executing them. They can cause data loss if used incorrectly. Ensure you have a valid backup before destructive operations. Treat generated commands as candidates for manual review, not as commands to run blindly.Here is a query that can help with investigations. It looks for active parts containing the same data blocks as the detached parts and generates commands to drop the detached parts.


```
SELECT a.*,
    concat('ALTER TABLE ',a.database,'.',a.table,' DROP DETACHED PART ''',a.name,''' SETTINGS allow_drop_detached=1;',
           ' -- db=',a.database,' table=',a.table,' reason=',a.reason,' partition_id=',a.partition_id,
           ' min_block=',toString(a.min_block_number),' max_block=',toString(a.max_block_number)) AS drop_command
FROM system.detached_parts AS a
LEFT JOIN (
    SELECT database, table, partition_id, name, active, min_block_number, max_block_number
    FROM system.parts
    WHERE active
) b
ON a.database = b.database AND a.table = b.table AND a.partition_id = b.partition_id
WHERE a.min_block_number IS NOT NULL
  AND a.max_block_number IS NOT NULL
  AND a.min_block_number >= b.min_block_number
  AND a.max_block_number <= b.max_block_number
ORDER BY a.table, a.min_block_number, a.max_block_number
SETTINGS join_use_nulls=1

```
The list of `DETACH_REASONS`: [MergeTreePartInfo.h\#L163](https://github.com/ClickHouse/ClickHouse/blob/master/src/Storages/MergeTree/MergeTreePartInfo.h#L163)

### Rare but Important Edge Cases

1. **Invalid detached part names with `_tryN` suffixes** can produce `NULL` parsing metadata in `system.detached_parts`; treat these as a separate cleanup track.
2. **Older versions had DROP DETACHED issues on ReplicatedMergeTree over S3 (without zero\-copy)**; this was fixed in 2023\.
3. **Startup handling of unexpected parts was improved** to restore closer ancestors instead of random covered parts.
4. **Downgrade workflows may fail to ATTACH `broken-on-start_*` directly** in some versions. Workaround is manual rename then attach:


```
SELECT
    concat('mv ', path, ' ', replace(path, 'broken-on-start_', '')) AS mv_cmd
FROM system.detached_parts
WHERE startsWith(name, 'broken-on-start_')

```


| Detached part type | Source code reference |
| --- | --- |
| `broken` | [StorageReplicatedMergeTree.cpp](https://github.com/ClickHouse/ClickHouse/blob/53e451c70f33f167efe57dbf455ff9776d6e880f/src/Storages/StorageReplicatedMergeTree.cpp#L2306-L2334) |
| `unexpected` | [MergeTreeData.cpp](https://github.com/ClickHouse/ClickHouse/blob/53e451c70f33f167efe57dbf455ff9776d6e880f/src/Storages/MergeTree/MergeTreeData.cpp#L5389-L5393) |
| `ignored` | [MergeTreeSettings.cpp](https://github.com/ClickHouse/ClickHouse/blob/53e451c70f33f167efe57dbf455ff9776d6e880f/src/Storages/MergeTree/MergeTreeSettings.cpp#L507-L512) |
| `noquorum` | [ReplicatedMergeTreeRestartingThread.cpp](https://github.com/ClickHouse/ClickHouse/blob/53e451c70f33f167efe57dbf455ff9776d6e880f/src/Storages/MergeTree/ReplicatedMergeTreeRestartingThread.cpp#L264-L284) |
| `broken-on-start` | [MergeTreeData.cpp](https://github.com/ClickHouse/ClickHouse/blob/53e451c70f33f167efe57dbf455ff9776d6e880f/src/Storages/MergeTree/MergeTreeData.cpp#L2301-L2399) |
| `clone` | [StorageReplicatedMergeTree.cpp](https://github.com/ClickHouse/ClickHouse/blob/53e451c70f33f167efe57dbf455ff9776d6e880f/src/Storages/StorageReplicatedMergeTree.cpp#L3510-L3518) |
| `attaching` | [MergeTreeData.cpp](https://github.com/ClickHouse/ClickHouse/blob/53e451c70f33f167efe57dbf455ff9776d6e880f/src/Storages/MergeTree/MergeTreeData.cpp#L7541-L7671) |
| `deleting` | [MergeTreeData.cpp](https://github.com/ClickHouse/ClickHouse/blob/53e451c70f33f167efe57dbf455ff9776d6e880f/src/Storages/MergeTree/MergeTreeData.cpp#L7541-L7583) |
| `tmp-fetch` | [DataPartsExchange.cpp](https://github.com/ClickHouse/ClickHouse/blob/53e451c70f33f167efe57dbf455ff9776d6e880f/src/Storages/MergeTree/DataPartsExchange.cpp#L408-L413) |
| `covered-by-broken` | [StorageReplicatedMergeTree.cpp](https://github.com/ClickHouse/ClickHouse/blob/53e451c70f33f167efe57dbf455ff9776d6e880f/src/Storages/StorageReplicatedMergeTree.cpp#L4571-L4588) |
| `merge-not-byte-identical` | [MergeFromLogEntryTask.cpp](https://github.com/ClickHouse/ClickHouse/blob/53e451c70f33f167efe57dbf455ff9776d6e880f/src/Storages/MergeTree/MergeFromLogEntryTask.cpp#L441-L443) |
| `mutate-not-byte-identical` | [MutateFromLogEntryTask.cpp](https://github.com/ClickHouse/ClickHouse/blob/53e451c70f33f167efe57dbf455ff9776d6e880f/src/Storages/MergeTree/MutateFromLogEntryTask.cpp#L278-L280) |
| `broken-from-backup` | [MergeTreeData.cpp](https://github.com/ClickHouse/ClickHouse/blob/53e451c70f33f167efe57dbf455ff9776d6e880f/src/Storages/MergeTree/MergeTreeData.cpp#L6919-L6934) |

# 9 \- Database Size \- Table \- Column size

Queries to analyze size and compression rates across tables and columns## Tables

### Table size


> Returns table size, compression rates, and row and part counts, by table


```
SELECT
    database,
    table,
    formatReadableSize(sum(data_compressed_bytes) AS size) AS compressed,
    formatReadableSize(sum(data_uncompressed_bytes) AS usize) AS uncompressed,
    round(usize / size, 2) AS compr_rate,
    sum(rows) AS rows,
    count() AS part_count
FROM system.parts
WHERE (active = 1) AND (database LIKE '%') AND (table LIKE '%')
GROUP BY
    database,
    table
ORDER BY size DESC;

```
### Table size \+ inner MatView (Atomic)


> As above, but resolves Materialized View inner table names (for Materialized Views created using implicit inner table)


```
SELECT
      p.database,
      if(t.name = '', p.table, p.table||' ('||t.name||')') tbl,
      formatReadableSize(sum(p.data_compressed_bytes) AS size) AS compressed,
      formatReadableSize(sum(p.data_uncompressed_bytes) AS usize) AS uncompressed,
      round(usize / size, 2) AS compr_rate,
      sum(p.rows) AS rows,
      count() AS part_count
FROM system.parts p left join system.tables t on p.database = t.database and p.table = '.inner_id.'||toString(t.uuid)
WHERE (active = 1) AND (tbl LIKE '%') AND (database LIKE '%')
GROUP BY
    p.database,
    tbl
ORDER BY size DESC;

```
### Column size


> Returns size, compression rate, row counts, and average row size for each column (by db and table)


```
SELECT
    database,
    table,
    column,
    formatReadableSize(sum(column_data_compressed_bytes) AS size) AS compressed,
    formatReadableSize(sum(column_data_uncompressed_bytes) AS usize) AS uncompressed,
    round(usize / size, 2) AS compr_ratio,
    sum(rows) rows_cnt,
    round(usize / rows_cnt, 2) avg_row_size
FROM system.parts_columns
WHERE (active = 1) AND (database LIKE '%') AND (table LIKE '%')
GROUP BY
    database,
    table,
    column
ORDER BY size DESC;

```
## Projections

### Projection size


> Returns size, compression rate, row counts, and average row size for each projection (“name”), by db and table


```
SELECT
    database,
    table,
    name,
    formatReadableSize(sum(data_compressed_bytes) AS size) AS compressed,
    formatReadableSize(sum(data_uncompressed_bytes) AS usize) AS uncompressed,
    round(usize / size, 2) AS compr_rate,
    sum(rows) AS rows,
    count() AS part_count
FROM system.projection_parts
WHERE (table = 'ptest') AND active
GROUP BY
    database,
    table,
    name
ORDER BY size DESC;

```
### Projection column size


> Returns size, compression rate, row counts, and average row size for each projection (“name”), by db and table, and column


```
SELECT
    database,
    table,
    column,
    formatReadableSize(sum(column_data_compressed_bytes) AS size) AS compressed,
    formatReadableSize(sum(column_data_uncompressed_bytes) AS usize) AS uncompressed,
    round(usize / size, 2) AS compr_rate
FROM system.projection_parts_columns
WHERE (active = 1) AND (table LIKE 'ptest')
GROUP BY
    database,
    table,
    column
ORDER BY size DESC;

```
## Understanding the columns data properties:


> For each column in a table, unique value counts, min/max, and top 5 most frequent values


```
SELECT
   count(),
   * APPLY (uniq),
   * APPLY (max),
   * APPLY (min),
   * APPLY(topK(5))
FROM table_name 
FORMAT Vertical;

-- also you can add * APPLY (entropy) to show entropy (i.e. 'randomness' of the column).
-- if the table is huge add some WHERE condition to slice some 'representative' data range, for example single month / week / day of data.

```
## Understanding the ingest pattern:


> For parts which are recently created and are unmerged, returns row, size, and count information by db and table.

- High count, low rows: lots of small parts
- High countif(NOT active) relative to count(): merges are keeping up
- Low countIf(NOT active) relative to count(): merges may be falling behind
- uniqExact(partition): how many partitions are being written to


```
SELECT
    database,
    table,
    median(rows),
    median(bytes_on_disk),
    sum(rows),
    max(bytes_on_disk),
    min(bytes_on_disk),
    round(quantile(0.95)(bytes_on_disk), 0),
    sum(bytes_on_disk),
    count(),
    countIf(NOT active),
    uniqExact(partition)
FROM system.parts
WHERE (modification_time > (now() - 480)) AND (level = 0)
GROUP BY
    database,
    table
ORDER BY count() DESC

```
## part\_log


> For the past day, returns per\-second part lifecycle metrics over 30 minute buckets


```
WITH 30 * 60 AS frame_size
SELECT
    toStartOfInterval(event_time, toIntervalSecond(frame_size)) AS m,
    database,
    table,
    ROUND(countIf(event_type = 'NewPart') / frame_size, 2) AS new,
    ROUND(countIf(event_type = 'MergeParts') / frame_size, 2) AS merge,
    ROUND(countIf(event_type = 'DownloadPart') / frame_size, 2) AS dl,
    ROUND(countIf(event_type = 'RemovePart') / frame_size, 2) AS rm,
    ROUND(countIf(event_type = 'MutatePart') / frame_size, 2) AS mut,
    ROUND(countIf(event_type = 'MovePart') / frame_size, 2) AS mv
FROM system.part_log
WHERE event_time > (now() - toIntervalHour(24))
GROUP BY
    m,
    database,
    table
ORDER BY
    database ASC,
    table ASC,
    m ASC

```

> For the past day, returns per\-second insert throughput metrics, by db and table, over 30 minute buckets


```
WITH 30 * 60 AS frame_size
SELECT
    toStartOfInterval(event_time, toIntervalSecond(frame_size)) AS m,
    database,
    table,
    ROUND(countIf(event_type = 'NewPart') / frame_size, 2) AS inserts_per_sec,
    ROUND(sumIf(rows, event_type = 'NewPart') / frame_size, 2) AS rows_per_sec,
    ROUND(sumIf(size_in_bytes, event_type = 'NewPart') / frame_size, 2) AS bytes_per_sec
FROM system.part_log
WHERE event_time > (now() - toIntervalHour(24))
GROUP BY
    m,
    database,
    table
ORDER BY
    database ASC,
    table ASC,
    m ASC

```
## Understanding partitioning


> Partition distribution analysis, aggregating system.parts metrics by partition. The quantiles results can indicate whether there is skewed distribution of data between partitions.


```
SELECT
    database,
    table,
    count(),
    topK(5)(partition),
    COLUMNS('metric.*') APPLY(quantiles(0.005, 0.05, 0.10, 0.25, 0.5, 0.75, 0.9, 0.95, 0.995))
FROM
(
    SELECT
        database,
        table,
        partition,
        sum(bytes_on_disk) AS metric_bytes,
        sum(data_uncompressed_bytes) AS metric_uncompressed_bytes,
        sum(rows) AS metric_rows,
        sum(primary_key_bytes_in_memory) AS metric_pk_size,
        count() AS metric_count,
        countIf(part_type = 'Wide') AS metric_wide_count,
        countIf(part_type = 'Compact') AS metric_compact_count,
        countIf(part_type = 'Memory') AS metric_memory_count
    FROM system.parts
    GROUP BY
        database,
        table,
        partition
)
GROUP BY
    database,
    table
FORMAT Vertical

```
## Subcolumns sizes


> Returns column\-level storage metrics, including subcolumns (JSON, tuples, maps, etc \- if present)


```
WITH 
     if(
          length(subcolumns.names) > 0, 
          arrayMap( (sc_n,sc_t,sc_s, sc_bod, sc_dcb, sc_dub) -> tuple(sc_n,sc_t,sc_s, sc_bod, sc_dcb, sc_dub), subcolumns.names, subcolumns.types, subcolumns.serializations, subcolumns.bytes_on_disk, subcolumns.data_compressed_bytes, subcolumns.data_uncompressed_bytes),
          [tuple('',type,serialization_kind,column_bytes_on_disk,column_data_compressed_bytes,column_data_uncompressed_bytes)]) as _subcolumns_data,
     arrayJoin(_subcolumns_data) as _subcolumn,
     _subcolumn.1 as _sc_name, 
     _subcolumn.2 as _sc_type,
     _subcolumn.3 as _sc_serialization,
     _subcolumn.4 as _sc_bytes_on_disk,
     _subcolumn.5 as _sc_data_compressed_bytes,
     _subcolumn.6 as _sc_uncompressed_bytes
SELECT
    database || '.' || table as table_,
    column as colunm_, 
    _sc_name as subcolumn_,
    any(_sc_type),
    formatReadableSize(sum(_sc_data_compressed_bytes) AS size) AS compressed,
    formatReadableSize(sum(_sc_uncompressed_bytes) AS usize) AS uncompressed,
    round(usize / size, 2) AS compr_ratio,
    sum(rows) AS rows_cnt,
    round(usize / rows_cnt, 2) AS avg_row_size
FROM system.parts_columns
WHERE (active = 1) AND (database LIKE '%') AND (`table` LIKE '%')
GROUP BY  
     table_,
     colunm_,
     subcolumn_
ORDER BY size DESC ;

```
# 10 \- Notes on Various Errors with respect to replication and distributed connections

Notes on errors related to replication and distributed connections## `ClickHouseDistributedConnectionExceptions`

This alert usually indicates that one of the nodes isn’t responding or that there’s an interconnectivity issue. Debug steps:

## 1\. Check Cluster Connectivity

Verify connectivity inside the cluster by running:


```
SELECT count() FROM clusterAllReplicas('{cluster}', cluster('{cluster}', system.one))

```
## 2\. Check for Errors

Run the following queries to see if any nodes report errors:


```
SELECT hostName(), * FROM clusterAllReplicas('{cluster}', system.clusters) WHERE errors_count > 0;
SELECT hostName(), * FROM clusterAllReplicas('{cluster}', system.errors) WHERE last_error_time > now() - 3600 ORDER BY value;

```
Depending on the results, ensure that the affected node is up and responding to queries. Also, verify that connectivity (DNS, routes, delays) is functioning correctly.

### `ClickHouseReplicatedPartChecksFailed` \& `ClickHouseReplicatedPartFailedFetches`

Unless you’re seeing huge numbers, these alerts can generally be ignored. They’re often a sign of temporary replication issues that ClickHouse resolves on its own. However, if the issue persists or increases rapidly, follow the steps to debug replication issues:

- Check the replication status using tables such as system.replicas and system.replication\_queue.
- Examine server logs, system.errors, and system load for any clues.
- Try to restart the replica (`SYSTEM RESTART REPLICA db_name.table_name` command) and, if necessary, contact Altinity support.
# 11 \- Number of active parts in a partition

Number of active parts in a partition## Q: Why do I have several active parts in a partition? Why ClickHouse® does not merge them immediately?

### A: CH does not merge parts by time

Merge scheduler selects parts by own algorithm based on the current node workload / number of parts / size of parts.

CH merge scheduler balances between a big number of parts and a wasting resources on merges.

Merges are CPU/DISK IO expensive. If CH will merge every new part then all resources will be spend on merges and will no resources remain on queries (selects ).

CH will not merge parts with a combined size greater than 150 GB [max\_bytes\_to\_merge\_at\_max\_space\_in\_pool](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings#max-bytes-to-merge-at-max-space-in-pool)
.


```
SELECT
    database,
    table,
    partition,
    sum(rows) AS rows,
    count() AS part_count
FROM system.parts
WHERE (active = 1) AND (table LIKE '%') AND (database LIKE '%')
GROUP BY
    database,
    table,
    partition
ORDER BY part_count DESC
limit 20

```
# 12 \- Parts consistency

## Check if there are blocks missing


```
SELECT
    database,
    table,
    partition_id,
    ranges.1 AS previous_part,
    ranges.2 AS next_part,
    ranges.3 AS previous_block_number,
    ranges.4 AS next_block_number,
    range(toUInt64(previous_block_number + 1), toUInt64(next_block_number)) AS missing_block_numbers
FROM
(
    WITH
        arrayPopFront(groupArray(min_block_number) AS min) AS min_adj,
        arrayPopBack(groupArray(max_block_number) AS max) AS max_adj,
        arrayFilter((x, y, z) -> (y != (z + 1)), arrayZip(arrayPopBack(groupArray(name) AS name_arr), arrayPopFront(name_arr), max_adj, min_adj), min_adj, max_adj) AS missing_ranges
    SELECT
        database,
        table,
        partition_id,
        missing_ranges
    FROM
    (
        SELECT *
        FROM system.parts
        WHERE active AND (table = 'query_thread_log') AND (partition_id = '202108') AND active
        ORDER BY min_block_number ASC
    )
    GROUP BY
        database,
        table,
        partition_id
)
ARRAY JOIN missing_ranges AS ranges

┌─database─┬─table────────────┬─partition_id─┬─previous_part───────┬─next_part──────────┬─previous_block_number─┬─next_block_number─┬─missing_block_numbers─┐
│ system   │ query_thread_log │ 202108       │ 202108_864_1637_556 │ 202108_1639_1639_0 │                  1637 │              1639 │ [1638]                │
└──────────┴──────────────────┴──────────────┴─────────────────────┴────────────────────┴───────────────────────┴───────────────────┴───────────────────────┘

```
## Find the number of blocks in a table


```
SELECT
    database,
    table,
    partition_id,
    sum(max_block_number - min_block_number) AS blocks_count
FROM system.parts
WHERE active AND (table = 'query_thread_log') AND (partition_id = '202108') AND active
GROUP BY
    database,
    table,
    partition_id

┌─database─┬─table────────────┬─partition_id─┬─blocks_count─┐
│ system   │ query_thread_log │ 202108       │         1635 │
└──────────┴──────────────────┴──────────────┴──────────────┘

```
## Compare the list of parts in ZooKeeper with the list of parts on disk


```
select zoo.p_path as part_zoo, zoo.ctime, zoo.mtime, disk.p_path as part_disk
from
(
  select concat(path,'/',name) as p_path, ctime, mtime
  from system.zookeeper where path in (select concat(replica_path,'/parts') from system.replicas)
) zoo
left join 
(
  select concat(replica_path,'/parts/',name) as p_path
  from system.parts inner join system.replicas using (database, table)
) disk on zoo.p_path = disk.p_path
where part_disk='' and zoo.mtime <= now() - interval 1 hour
order by part_zoo;

```
You can clean that orphan zk records (need to execute using `delete` in zkCli, `rm` in zk\-shell):


```
select 'delete '||part_zoo
from (
select zoo.p_path as part_zoo, zoo.ctime, zoo.mtime, disk.p_path as part_disk
from
(
  select concat(path,'/',name) as p_path, ctime, mtime
  from system.zookeeper where path in (select concat(replica_path,'/parts') from system.replicas)
) zoo
left join 
(
  select concat(replica_path,'/parts/',name) as p_path
  from system.parts inner join system.replicas using (database, table)
) disk on zoo.p_path = disk.p_path
where part_disk='' and zoo.mtime <= now() - interval 1 day
order by part_zoo) format TSVRaw;

```
