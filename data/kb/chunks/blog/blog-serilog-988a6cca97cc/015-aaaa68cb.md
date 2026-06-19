---
source: blog
url: https://github.com/ClickHouse/clickhouse-serilog-demo/tree/main
topic: structured-logging-in-net-with-serilog-and-clickhouse
ch_version_introduced: '599.99'
last_updated: '2026-06-12'
chunk_index: 15
total_chunks_in_doc: 16
---

inserted, ClickHouse incrementally updates the aggregate. You can then query `error_counts_per_minute` for a real\-time error dashboard or alert when counts spike. These views can then be used inside ClickStack, which has [built\-in support for alerting](https://clickhouse.com/docs/use-cases/observability/clickstack/alerts). ## Resources [\#](/blog/serilog#resources)

- [Demo source code on GitHub](https://github.com/ClickHouse/clickhouse-serilog-demo/tree/main)
- [Serilog.Sinks.ClickHouse on GitHub](https://github.com/ClickHouse/Serilog.Sinks.ClickHouse)
- [ClickHouse Cloud](https://clickhouse.com/cloud) — Managed ClickHouse with a free tier
- [Serilog Documentation](https://serilog.net/)
- [ClickStack Performance Tuning](https://clickhouse.com/docs/use-cases/observability/clickstack/performance_tuning) — Optimizations for production observability workloads
- [Full\-Text Search in ClickHouse — Now GA](https://clickhouse.com/blog/full-text-search-ga-release) — Inverted indexes for sub\-second log search
- [How Trip.com Built a 50PB Logging Solution with ClickHouse](https://clickhouse.com/blog/how-trip.com-migrated-from-elasticsearch-and-built-a-50pb-logging-solution-with-clickhouse) — Migrating from Elasticsearch, 4x data capacity on same hardware
- [Building a Logging Platform with ClickHouse and Saving Millions over Datadog](https://clickhouse.com/blog/building-a-logging-platform-with-clickhouse-and-saving-millions-over-datadog) — 200x cost reduction vs SaaS, 17x compression ratio

## Conclusion [\#](/blog/serilog#conclusion)

We've built a .NET service that produces structured log events via Serilog, writes them directly to ClickHouse, and lets us query our logs using SQL.

The key takeaways:

- **Drop\-in for Serilog users**: If your .NET app already uses Serilog, the ClickHouse sink is one `WriteTo.ClickHouse()` call away.
- **Cost and performance**: ClickHouse handles log workloads at a fraction of the cost of traditional logging platforms, with 10–20x compression and sub\-second analytical queries over billions of rows.
- **Full schema control**: You decide how logs are stored. Typed columns, secondary indexes, partitioning, and compression codecs, all through the fluent schema builder in C\#.
- **Full\-text search**: ClickHouse's now\-GA inverted indexes bring sub\-second log search to your existing tables — no separate search engine required.
- **No frontend lock\-in**: Your logs are standard ClickHouse tables. Query them with SQL in the Play UI, connect [Grafana](https://clickhouse.com/docs/integrations/grafana) (via the ClickHouse data source plugin), [Metabase](https://www.metabase.com/data_sources/clickhouse), [ClickStack](https://clickhouse.com/docs/en/observability/clickstack), or any other tool that speaks SQL.

The entire demo runs with a single `docker compose up`. Clone the repo, generate some traffic, and see what structured logs look like in ClickHouse. When you're ready to try it with a managed deployment, get started with ClickHouse Cloud.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-267-get-started-today-sign-up&utm_blogctaid=267)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter
