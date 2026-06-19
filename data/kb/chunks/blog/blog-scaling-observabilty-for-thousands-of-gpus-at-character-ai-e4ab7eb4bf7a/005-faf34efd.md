---
source: blog
url: https://clickhouse.com/docs/use-cases/observability/clickstack/getting-started?loc=blog-o11y-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog
topic: scaling-observability-at-character-ai-thousands-of-gpus-10x-logs-and-50-lower-cost-with-clickstack
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 8
---

also proved critical. Mustafa initially started with the smallest instance and gradually tuned auto\-scaling thresholds based on traffic patterns. Today, their cluster scales automatically between defined min/max bounds to handle variable load during the day while minimizing spend.

Even without exploiting ClickHouse Cloud's support for compute\-storage separation (to isolate read and writes), performance remained strong. Auto\-scaling, combined with fast S3\-backed storage and around 15x compression from raw, allowed them to keep costs low and query latency fast.

> "I was genuinely impressed by the compression we achieved with ClickHouse. Some columns gave us 10x, others 20x \- even up to 50x in some cases. On average, we're seeing 15–20x compression!"

## Lessons learned and advice for others [\#](/blog/scaling-observabilty-for-thousands-of-gpus-at-character-ai#lessons-learned-and-advice-for-others)

Once ingestion was stable, attention turned to schema and query optimization. The default schema, while functional, wasn't optimized for Character.AI's access patterns. This led to some queries being slower and less resource\-efficient. Working closely with the ClickHouse team, they:

- [**Optimized primary keys**](https://clickhouse.com/docs/primary-indexes) to align with common time\-range and service\-based queries.
- Added [**Materialized views**](https://clickhouse.com/docs/materialized-views) to extract key fields from JSON payloads, like cluster\_name, service\_name, and error\_type, into separate columns.
- Carefully evaluated and [**added skip indexes**](https://clickhouse.com/docs/optimize/skipping-indexes) (e.g., Bloom filters or min/max), while also **removing unused ones** to reduce memory overhead and complexity e.g. on `ScopeAttributes`.
- Reordered columns and tuned compression settings for better performance and storage efficiency.

Generally, Mustafa recommends performing optimizations early as small changes make huge differences at scale.

> "Even small optimizations make a huge impact at scale. The earlier you tune things, the better."

Despite the tremendous success, one persistent challenge stood out: **OpenTelemetry collector configuration**. Getting the collector config right took time \- especially around sampling, batching, and resilience. Early mistakes, like forgetting to batch or ingesting unsampled logs, triggered outages and forced them to reset pipelines. Today, things are stable, but Mustafa is clear: this is an area OpenTelemetry should improve and welcomes the opinionated distribution now available with ClickStack.

## Key ClickStack features [\#](/blog/scaling-observabilty-for-thousands-of-gpus-at-character-ai#key-clickstack-features)

Character.AI's infrastructure is massive \- but the ClickStack setup is surprisingly lean. What won Mustafa over was a combination of speed, simplicity, and several practical features that significantly help with day\-to\-day root cause analysis and issue resolution.
