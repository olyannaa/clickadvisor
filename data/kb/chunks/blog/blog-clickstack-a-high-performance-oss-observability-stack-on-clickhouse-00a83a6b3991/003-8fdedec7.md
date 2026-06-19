---
source: blog
url: https://clickhouse.com/o11y
topic: clickstack-a-high-performance-oss-observability-stack-on-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 7
---

slow tooling. ### Get started with ClickStack [\#](/blog/clickstack-a-high-performance-oss-observability-stack-on-clickhouse#test) Ready to explore the world's fastest and most scalable open source observability stack? Start locally in seconds. [Start exploring](https://clickhouse.com/docs/use-cases/observability/clickstack/getting-started?loc=blog-o11y-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) ### All you need is wide events…and a column store [\#](/blog/clickstack-a-high-performance-oss-observability-stack-on-clickhouse#all-you-need-is-wide-eventsand-a-column-store)

In our earlier post ["The State of SQL\-Based Observability"](https://clickhouse.com/blog/the-state-of-sql-based-observability) and subsequent [follow\-ups](https://clickhouse.com/blog/evolution-of-sql-based-observability-with-clickhouse), we explored this trend in depth \- though we didn't name it at the time, it aligns perfectly with today's Observability 2\.0 movement: a unified model [built around wide events](https://isburmistrov.substack.com/p/all-you-need-is-wide-events-not-metrics), not pillars. For too long, teams relied on separate stores for logs, metrics, and traces, which led to fragmentation, manual correlation, and unnecessary complexity. Wide events eliminate these silos by consolidating all observability signals into a single, queryable structure.

A wide event captures the full application context in a single record \- user, service, HTTP path, status code, cache result, and more. This unified structure is key to eliminating silos and enabling fast search and aggregation across high\-cardinality data \- provided you have a storage engine that can compress and store it efficiently!

While No\-SQL solutions, such as search engines, embraced this structure they lacked the aggregation performance to deliver on the promise \- great for search and "finding needles in galaxies", less so if you want to aggregate across wide ranges. ClickHouse's secret sauce to this problem remains unchanged: columnar storage, a rich codec library for deep compression, and a massively parallel engine optimized for analytical workloads.

### Resource efficient and scalable [\#](/blog/clickstack-a-high-performance-oss-observability-stack-on-clickhouse#resource-efficient-and-scalable)

In ClickHouse Cloud we went further and embraced object storage to deliver separation of storage and compute, essential if you're needing to scale your observability to PB and beyond and need to scale elastically. To support even more demanding use cases, we also introduced compute\-compute separation allowing users to dedicate compute to specific workloads while reading from the same data e.g. ingest and querying.

As observability needs became more complex, we recognized that native JSON support for semi\-structured events was table stakes. ClickHouse evolved to meet this need, adding first\-class support for semi\-structured data while preserving the benefits of column\-oriented processing. Columns are auto\-created as data arrives, and ClickHouse manages type promotion and column growth automatically. It's the schema\-on\-write you need for observability with the performance, compression, and flexibility expected from a modern analytical engine.
