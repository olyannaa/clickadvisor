---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Getting
topic: getting-started-with-clickhouse-13-mistakes-and-how-to-avoid-them-clickhouse
ch_version_introduced: '335.39'
last_updated: '2026-09-07'
chunk_index: 16
total_chunks_in_doc: 20
---

allowed to spill over to disk. This setting is also helpful for cases where the user has an `ORDER BY` after a `GROUP BY` with a `LIMIT`, especially in cases where the query is distributed. ### JOINs \#

ClickHouse has [full JOIN support](https://clickhouse.com/blog/clickhouse-fully-supports-joins-part1) with all standard SQL join types, plus specialized variants like `ANY`, `ASOF`, `SEMI`, and `ANTI` joins that can significantly improve performance for common analytical patterns. That said, joins are inherently memory\-intensive operations, and understanding the tradeoffs between different approaches is key to avoiding memory issues.

The general principles for efficient joins in ClickHouse:

- **Choose the right algorithm for your data.** ClickHouse provides multiple [join algorithms](https://clickhouse.com/docs/guides/joining-tables) via the [`join_algorithm`](https://clickhouse.com/docs/operations/settings/settings#join_algorithm) setting, each trading off memory usage against performance. Hash joins are fast but memory\-bound. Grace hash partitions data into buckets and spills to disk when memory is exhausted. Sort\-merge variants (`partial_merge`, `full_sorting_merge`) work well for pre\-sorted data or when both sides are too large for memory. The `direct` algorithm acts as a fast key\-value lookup when the right table is backed by a dictionary or a small in\-memory table. Setting `join_algorithm = 'auto'` lets ClickHouse adaptively select the best algorithm at runtime based on available resources.
- **Use specialized join types.** `ANY JOIN` returns only the first matching row from the right table, making it much faster and more memory\-efficient for lookup\-style enrichment queries. `ASOF JOIN` is purpose\-built for time\-series data where you need the closest match rather than an exact one.
- **Filter early.** Apply WHERE conditions before the join wherever possible to reduce the volume of data entering the join operation.
- **Smaller table on the right.** For hash\-based joins (the default), ClickHouse builds an in\-memory hash table from the right\-hand side. Placing the smaller table on the right minimizes memory usage. [ClickHouse's query planner can automatically reorder join tables when it determines a better ordering](https://clickhouse.com/blog/clickhouse-release-25-12#join-reordering-primer), but understanding this principle remains important.

![sins-11-joins.png](/_next/image?url=%2Fdocs%2Fassets%2Fideal-img%2Fjoins-2.423394e.1600.png&w=2048&q=75)

### Rogue queries \#

Other causes for memory issues are unrestricted users. In these cases, we see users issuing rogue queries with no [quotas](https://clickhouse.com/docs/en/operations/quotas/) or [restrictions on query complexity](https://clickhouse.com/docs/en/operations/settings/query-complexity/). These controls are essential in providing a robust service if exposing a ClickHouse instance to a broad and diverse set of users. Our own [play.clickhouse.com](https://play.clickhouse.com/play?user=play) environment uses these effectively to restrict usage and provide a stable environment.
