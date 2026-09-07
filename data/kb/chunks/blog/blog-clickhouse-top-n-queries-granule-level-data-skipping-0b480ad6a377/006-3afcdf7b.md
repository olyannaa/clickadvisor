---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-clickhouse-makes-top-n-queries-faster-with-granule-level-data-skipping-clickhouse
ch_version_introduced: '0.044'
last_updated: '2026-09-07'
chunk_index: 6
total_chunks_in_doc: 7
---

by enabling the new [use\_top\_k\_dynamic\_filtering](https://clickhouse.com/docs/operations/settings/settings#use_top_k_dynamic_filtering) setting. Note that the table has a [minmax data skipping index on the `EventTime` column](https://pastila.nl/?000d9e4d/048b6bdf283322bef6dc9bba561215c6#VWIpCGN9UO1RrWi2ilL5eA==GCM) and we disabled the [query condition cache](https://clickhouse.com/blog/introducing-the-clickhouse-query-condition-cache) for all runs to fully isolate the dynamic top\-N threshold filtering.

```
1SELECT URL,EventTime 
2FROM hits 
3WHERE URL LIKE '%google%'
4ORDER BY EventTime
5LIMIT 10
6SETTINGS
7  use_query_condition_cache = 0,
8  use_skip_indexes_on_data_read = 1,
9  use_skip_indexes_for_top_k = 1,
10  use_top_k_dynamic_filtering = 1;
```
Copy command
Now the fastest of three runs finished in 0\.033 seconds:

```
110 rows in set. Elapsed: 0.034 sec. Processed 7.66 million rows, 515.98 MB (227.36 million rows/s., 15.32 GB/s.)
2Peak memory usage: 51.30 MiB.
3
410 rows in set. Elapsed: 0.034 sec. Processed 7.59 million rows, 509.67 MB (224.45 million rows/s., 15.08 GB/s.)
5Peak memory usage: 51.29 MiB.
6
710 rows in set. Elapsed: 0.033 sec. Processed 7.67 million rows, 520.58 MB (234.95 million rows/s., 15.96 GB/s.)
8Peak memory usage: 47.28 MiB.
```
Copy command
This is roughly **10× faster than before**. Instead of processing the table’s full **\~100 million rows**, ClickHouse processed only about **7 million rows**, which reduced the amount of data read from roughly **9\.42 GB** to about **520\.58 MB**.

As in the previous example, this I/O benefit grows with table size: when tables run into billions or trillions of rows (and especially when the cache is cold), dynamically skipping granules that cannot improve the current Top\-N result becomes increasingly impactful.

As explained above, ClickHouse achieves this by continuously maintaining the current Top\-N threshold *during* query execution and using the minmax data skipping index to dynamically skip granules whose values cannot improve the Top\-10 result.

## Production\-scale validation \#

These mechanics have also been validated on very large production tables.

In [early testing](https://github.com/ClickHouse/ClickHouse/pull/89835#issuecomment-3566807610) on a table with **50 billion rows**, Top\-N queries using skip index filtering completed in under **0\.2 seconds**, confirming that granule\-level pruning remains effective even at extreme scale. Further improvements are expected to make this even faster.

## Turning Top\-N into a metadata problem \#

With data skipping–based Top\-N filtering, ClickHouse turns Top\-N queries into a **metadata\-driven pruning problem**.
