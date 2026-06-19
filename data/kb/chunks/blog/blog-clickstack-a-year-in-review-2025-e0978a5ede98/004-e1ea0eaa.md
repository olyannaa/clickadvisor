---
source: blog
url: https://clickhouse.com/blog/clickstack-a-high-performance-oss-observability-stack-on-clickhouse
topic: clickstack-a-half-year-in-review
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 10
---

manage, companies migrating large workloads from proprietary observability vendors who needed a cost efficient alternative that didn’t compromise on performance, and application teams already using ClickHouse Cloud for analytics who could now add observability with a single click.

This Cloud integration also made our broader vision tangible, unified observability and analytics in one system. Instead of treating telemetry as a separate silo, ClickStack in Cloud allows teams to join traces, logs, and metrics directly with application data, product events, and operational KPIs. It shifts observability from after the fact diagnosis to a fully correlated analytical workflow where business impact, performance regressions, and customer behavior can all be understood through one engine. At the core of this belief is the principle we’ve stated throughout the year:

**We believe observability is just another data problem.** And that it belongs in the same database as your business\-critical analytics. With ClickHouse Cloud, you get the performance of a real\-time warehouse, the scale and flexibility of object storage, and now the visibility of a modern observability UI \- all in one stack.

![image9.png](/uploads/image9_3cb6c255b8.png)
Since launching in Cloud, we’ve continued onboarding customers steadily and have gathered feedback from some of the largest organizations using ClickHouse for observability today. These include deeply scaled teams such as [Anthropic](https://clickhouse.com/blog/how-anthropic-is-using-clickhouse-to-scale-observability-for-ai-era) and [character.AI](http://character.AI), whose input has shaped how the UI behaves under high volume, high cardinality workloads. Their use cases have pushed the product further, influencing everything from performance optimizations to workflow simplifications. August wasn’t just a feature release, it was the start of a new chapter where ClickStack became a native part of ClickHouse Cloud and a foundation for the unified observability experience we’ll continue building in 2026\.

Alongside this, we added further [performance improvements](https://clickhouse.com/blog/whats-new-in-clickstack-august#improved-query-efficiency-for-time-based-primary-keys) for scale as well as [early support](https://clickhouse.com/blog/whats-new-in-clickstack-august#inverted-indices-support) for ClickHouse’s [new inverted index](https://clickhouse.com/blog/clickhouse-full-text-search) \- an effort aimed at improving full text search over log bodies. While still experimental, it’s an area we’re actively still evaluating, and it will remain a focus as we move into January 2026\.

## September: Dashboard import/export, custom collector config, and smarter queries [\#](/blog/clickstack-a-year-in-review-2025#september-dashboard-importexport-custom-collector-config-and-smarter-queries)
