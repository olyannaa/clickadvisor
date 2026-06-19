---
source: blog
url: https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9
topic: clickhouse-release-25-12
ch_version_introduced: '25.12'
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 13
---

25\.12 [\#](/blog/clickhouse-release-25-12#lazy-reading-in-2512) Rather than fetching 104 columns for each row individually, ClickHouse now performs a single join\-like pass to materialize all remaining columns for the Top\-100,000 rows at once. The fastest of three runs completed in **0\.513 seconds**:

```
100000 rows in set. Elapsed: 0.513 sec. Processed 104.87 million rows, 3.56 GB (204.62 million rows/s., 6.94 GB/s.)
Peak memory usage: 967.19 MiB.

100000 rows in set. Elapsed: 0.524 sec. Processed 104.87 million rows, 3.56 GB (200.13 million rows/s., 6.79 GB/s.)
Peak memory usage: 951.09 MiB.

100000 rows in set. Elapsed: 0.520 sec. Processed 104.87 million rows, 3.56 GB (201.77 million rows/s., 6.85 GB/s.)
Peak memory usage: 953.08 MiB.

```

This is roughly **75 times faster than with the previous lazy reading mechanics** (and 14 times faster than without lazy reading).

#### Looking under the hood [\#](/blog/clickhouse-release-25-12#looking-under-the-hood)

We can confirm the change in lazy reading mechanics by inspecting the logical query plans for the same query using EXPLAIN PLAN:

```

```
1EXPLAIN PLAN
2SELECT * 
3FROM hits 
4ORDER BY EventTime 
5Limit 100000
6SETTINGS query_plan_max_limit_for_lazy_materialization = 0;
```

```

On 25\.11, with the old mechanics for lazy reading the plan shows (read it from bottom to top) how ClickHouse plans to

1. Read data from the table ( only the ORDER BY column).
2. Sort the data
3. Apply the LIMIT
4. **Then lazily fetch the remaining non\-order columns row by row**.

```
LazilyRead
...
Limit
...
Sorting
...
ReadFromMergeTree (default.hits) 

```

On 25\.12, the plan changes in a fundamental way.

The engine still:

1. Reads only the ORDER BY column.
2. Sorts the data
3. Applies the LIMIT

But instead of row\-by\-row materialization, it now introduces a **dedicated join step** to fetch the remaining columns in bulk from the base table:

```
JoinLazyColumnsStep
    ...
    Limit
    ...
    Sorting
    ...
    ReadFromMergeTree (default.hits) 
LazilyReadFromMergeTree

```

## Faster Joins with a more powerful join reordering algorithm [\#](/blog/clickhouse-release-25-12#faster-joins-with-a-more-powerful-join-reordering-algorithm)

### Contributed by Alexander Gololobov [\#](/blog/clickhouse-release-25-12#contributed-by-alexander-gololobov)

Top\-N queries got faster. Lazy reading got faster. And, unsurprisingly for a ClickHouse release, joins got faster as well. ClickHouse 25\.12 ships with a simple (for now) but more powerful join reordering algorithm for INNER JOINs \- DPsize \- that explores more join orders than the existing greedy approach, often producing more efficient execution plans with less intermediate data.

### Join reordering primer [\#](/blog/clickhouse-release-25-12#join-reordering-primer)
