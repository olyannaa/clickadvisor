---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-clickhouse-cloud-enabled-launchdarkly-to-build-and-ship-features-faster-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 4
total_chunks_in_doc: 9
---

“small experiment” turned into half a dozen teams adopting it within four months. “This dramatic drop in friction enabled us to ship features that would have previously taken months to develop.” ## How ClickHouse runs at LaunchDarkly \#

Today, LaunchDarkly runs ClickHouse as a fully hosted service using [ClickHouse Cloud](https://clickhouse.com/cloud). The decision to go with the managed service was “driven more by operational simplicity than by specific product features,” Matt says. “Spinning up clusters is easy, and the way ClickHouse scales in the cloud has been excellent for us.”

Raw events are sent directly into ClickHouse as they happen, and queries from the application layer are served straight from ClickHouse clusters. There’s no external pre\-aggregation pipeline to keep in sync just to power product features. [Materialized views](https://clickhouse.com/docs/materialized-views) are used where they make sense, but they live inside ClickHouse rather than a separate ETL system. The basic idea is simple: store raw events, query them directly, and introduce derived tables only when needed.

Ingestion follows a similar philosophy. Events arrive through an HTTP API, which batches them locally and writes them into S3 using an internal [protobuf](https://clickhouse.com/docs/interfaces/formats/Protobuf)\-based format. A [Lambda function](https://clickhouse.com/docs/use-cases/observability/clickstack/sdks/aws_lambda) converts each batch into standardized Parquet files, and ClickHouse is explicitly instructed to load that data into its own storage using [INSERT INTO SELECT](https://clickhouse.com/docs/sql-reference/statements/insert-into). Rather than querying S3 at runtime, ClickHouse pulls the data in and owns it. The ability to [import common file formats directly into ClickHouse](https://clickhouse.com/docs/integrations/data-formats) makes it easy to evolve ingestion over time without reworking everything upstream.

The platform ingests roughly six petabytes per month of uncompressed JSON events, covering feature evaluations, context metadata, and observability signals from production systems around the world. Once the data lands in ClickHouse, it compresses down to hundreds of terabytes while staying fully queryable. New data is typically available to product features in around 30 seconds, compared to several minutes in the previous warehouse, and retention has grown to roughly 100 days, a big step up from what was possible before.
