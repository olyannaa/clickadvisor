---
source: blog
url: https://clickhouse.com/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse#proving-the-system-at-scale
topic: how-the-5-major-cloud-data-warehouses-compare-on-cost-performance
ch_version_introduced: '9.236'
last_updated: '2026-06-12'
chunk_index: 9
total_chunks_in_doc: 13
---

tiny by current standards. Today’s datasets are frequently in billions, trillions, even quadrillions. [Tesla ingested over one quadrillion rows into ClickHouse for a load test](https://clickhouse.com/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse#proving-the-system-at-scale), and [ClickPy](https://clickpy.clickhouse.com/), our Python client telemetry dataset, has already surpassed [two trillion rows](https://sql.clickhouse.com/?query=U0VMRUNUCiAgICAgICAgZm9ybWF0UmVhZGFibGVRdWFudGl0eShzdW0oY291bnQpKSBBUyB0b3RhbCwgdW5pcUV4YWN0KHByb2plY3QpIGFzIHByb2plY3RzIEZST00gcHlwaS5weXBpX2Rvd25sb2Fkcw&run_query=true).

To understand how cost and performance evolve as data grows, **we extended ClickBench to 1B, 10B, and 100B rows** and reran the full 43\-query benchmark at all three scales.

*To keep results fair and reproducible, we followed the standard [ClickBench rules](https://github.com/ClickHouse/ClickBench/?tab=readme-ov-file#overview): no tuning, no engine\-specific optimizations, and no changes to min/max compute settings. This ensures that all results reflect how each system behaves out of the box, without hand\-tuning or workload\-specific tricks (e.g., precalculating aggregations with materialized views).*

To make results comparable across systems with incompatible billing models, we used the [CostBench framework](/blog/how-cloud-data-warehouses-bill-you#before-we-dive-in-how-we-calculate-costs-with-costbench) from the companion post. It takes the raw per\-query runtimes, applies each vendor’s actual compute pricing model, and produces a unified dataset containing **runtime, and compute cost** for every query on every system, plus **storage cost, and system metadata**.

### What configurations we compare [\#](/blog/cloud-data-warehouses-cost-performance-comparison#what-configurations-we-compare)

While the interactive benchmark explorer lets you compare *all* tiers and cluster sizes, for this post, we keep the comparison simple and consistent:

- **[Snowflake](/blog/how-cloud-data-warehouses-bill-you#snowflake) and [Databricks](/blog/how-cloud-data-warehouses-bill-you#databricks-sql-serverless)**: we include three warehouse sizes each, the **smallest**, a **mid\-range size**, and the **largest** Enterprise\-tier size, to cover their full practical spectrum. *(For more Snowflake\-specific details, including Gen 2 warehouses, QAS, and new warehouse sizes, see the note below.)*
- **[ClickHouse Cloud](/blog/how-cloud-data-warehouses-bill-you#clickhouse-cloud)**: ClickHouse Cloud has no fixed warehouse shapes, so “small / medium / large” tiers don’t exist. Instead, we use **one fixed ClickHouse Cloud Enterprise\-tier configuration** per dataset size.
- **[BigQuery](/blog/how-cloud-data-warehouses-bill-you#bigquery)**: BigQuery appears twice in the charts because it is a fully serverless system with no concept of cluster sizes, but it offers two billing models. We run the workload once (with a base capacity of 2000 slots), then price the same runtimes using both Enterprise (used **slot capacity\-based**) pricing and **On\-demand** (per scanned TiB) pricing.
- **[Redshift Serverless](/blog/how-cloud-data-warehouses-bill-you#redshift-serverless)**: Redshift Serverless appears once, because it likewise has no warehouse sizes or tiers. We use the **default 128\-RPU base configuration**.

All pricing is taken for the same cloud provider and region (AWS us\-east) where applicable; BigQuery is the exception and uses GCP us\-east.
