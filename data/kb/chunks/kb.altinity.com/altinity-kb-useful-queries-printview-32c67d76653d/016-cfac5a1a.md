---
source: kb.altinity.com
url: https://kb.altinity.com/altinity-kb-useful-queries/compare_query_log_for_2_intervals/
topic: useful-queries-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '0.9'
last_updated: '2026-06-12'
chunk_index: 16
total_chunks_in_doc: 19
---

1) AND (table LIKE 'ptest') GROUP BY database, table, column ORDER BY size DESC; ``` ## Understanding the columns data properties: > For each column in a table, unique value counts, min/max, and top 5 most frequent values

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
