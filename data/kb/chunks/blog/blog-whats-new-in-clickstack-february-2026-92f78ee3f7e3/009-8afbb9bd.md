---
source: blog
url: https://github.com/AdityaPimpalkar
topic: what-s-new-in-clickstack-february-26
ch_version_introduced: '0.99'
last_updated: '2026-06-12'
chunk_index: 9
total_chunks_in_doc: 10
---

OR logic. This behavior is controlled by `use_skip_indexes_for_disjunctions`, which is enabled by default. As a result, ClickStack automatically benefits from improved pruning and reduced data scans for a wider range of real\-world query patterns. ### Lazy materializations [\#](/blog/whats-new-in-clickstack-february-2026#lazy-materializations)

ClickHouse has long relied on layered I/O optimizations such as columnar storage, primary and secondary indexes, projections, and PREWHERE to reduce the amount of data read from disk. Traditionally, once rows passed the WHERE clause, all referenced columns for those rows would be loaded before operations such as sorting, aggregation, or LIMIT were applied. In many analytical queries, especially Top\-N patterns, this meant reading large columns that were ultimately unnecessary for producing the final result.

Lazy materialization, introduced in ClickHouse 25\.4 and enabled by default, changes this behavior. Instead of eagerly loading all selected columns, ClickHouse defers reading columns until they are actually required by the execution plan. For example, when a query performs an `ORDER BY … LIMIT`, the engine can first determine the top rows using only the ordering column, and only then read the remaining columns for those final rows. This reduces I/O, memory usage, and latency, particularly for wide tables or queries returning a small number of rows from very large datasets. If you're curious as to the internals and looking for a deep dive, we recommend the excellent blog post [“ClickHouse gets lazier (and faster): Introducing lazy materialization”](https://clickhouse.com/blog/clickhouse-gets-lazier-and-faster-introducing-lazy-materialization#speed-without-filters-lazy-materialization-in-isolation).

Since this optimization was default since 25\.4, users have been enjoying this for some time. However, this optimization is only applied if the limit is below a specified threshold [`query_plan_max_limit_for_lazy_materialization`](https://clickhouse.com/docs/operations/settings/settings#query_plan_max_limit_for_lazy_materialization). By default, this has a value of 10,000\.

In our own testing against typical ClickStack access patterns for log and trace search, we observed that result sets up to 100,000 rows still benefit significantly from lazy materialization \- in large part to [recent changes which make further optimizations to this feature](https://clickhouse.com/blog/clickhouse-release-25-12#what-changed-in-2512). As a result, in the latest version of ClickStack, we increase this threshold to 100,000 to extend the performance gains to a broader range of real\-world queries.

## Alerts on number charts [\#](/blog/whats-new-in-clickstack-february-2026#alerts-on-number-charts)

We continue to expand alerting capabilities in ClickStack. Last year, we introduced [alerts on saved searches and charts](https://clickhouse.com/docs/use-cases/observability/clickstack/alerts). In the latest release, users can now create alerts directly on number charts as well.
