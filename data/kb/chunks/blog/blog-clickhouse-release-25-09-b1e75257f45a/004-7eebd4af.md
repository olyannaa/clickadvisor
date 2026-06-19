---
source: blog
url: https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9
topic: clickhouse-release-25-9
ch_version_introduced: '25.9'
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 8
---

21GROUP BY 22 n_name 23ORDER BY 24 revenue DESC; ``` ``` First, we executed the query on the tables **without statistics**: ``` ``` 1USE tpch_no_stats; 2SET query_plan_optimize_join_order_limit = 10; 3SET allow_statistics_optimize = 1; 4 5-- test_query ``` ```

```
   ┌─n_name────┬─────────revenue─┐
1. │ VIETNAM   │  5310749966.867 │
2. │ INDIA     │ 5296094837.7503 │
3. │ JAPAN     │ 5282184528.8254 │
4. │ CHINA     │ 5270934901.5602 │
5. │ INDONESIA │ 5270340980.4608 │
   └───────────┴─────────────────┘

5 rows in set. Elapsed: 3903.678 sec. Processed 766.04 million rows, 16.03 GB (196.23 thousand rows/s., 4.11 MB/s.)
Peak memory usage: 99.12 GiB.

```

That took over one hour! 🐌 And used 99 GiB of main memory.

Then we repeated the same query on the tables **with statistics**:

```

```
1USE tpch_stats;
2SET query_plan_optimize_join_order_limit = 10;
3SET allow_statistics_optimize = 1;
4
5-- test_query
```

```

```
Query id: 5c1db564-86d0-46c6-9bbd-e5559ccb0355

   ┌─n_name────┬─────────revenue─┐
1. │ VIETNAM   │  5310749966.867 │
2. │ INDIA     │ 5296094837.7503 │
3. │ JAPAN     │ 5282184528.8254 │
4. │ CHINA     │ 5270934901.5602 │
5. │ INDONESIA │ 5270340980.4608 │
   └───────────┴─────────────────┘

5 rows in set. Elapsed: 2.702 sec. Processed 638.85 million rows, 14.76 GB (236.44 million rows/s., 5.46 GB/s.)
Peak memory usage: 3.94 GiB.

```

Now it took 2\.7 seconds. **\~1,450× faster than before.** With \~25x less memory usage.

### What’s next for join reordering [\#](/blog/clickhouse-release-25-09#whats-next-for-join-reordering)

This is just the **first step** for global join reordering in ClickHouse. Today, it requires manually created statistics. The next steps will include:

- **Automatic statistics creation** — removing the need for manual setup.
- **Support more join types (like outer joins) and joins over subqueries**
- **More powerful join reordering algorithms** — handling larger join graphs and more complex scenarios.

Stay tuned.

## Streaming for secondary indices [\#](/blog/clickhouse-release-25-09#streaming-for-secondary-indices)

### Contributed by Amos Bird [\#](/blog/clickhouse-release-25-09#contributed-by-amos-bird)

Before ClickHouse 25\.9, **secondary indices** (e.g., minmax, set, bloom filter, vector, text) were evaluated *before* reading the underlying table data. This sequential process had several drawbacks:

- **Inefficient with LIMIT:** Even if a query stopped early, ClickHouse still had to scan the entire index upfront.
- **Startup delay:** Index analysis happened before query execution began.
- **Heavy index scans:** In some cases, scanning the index cost more than processing the actual data.
