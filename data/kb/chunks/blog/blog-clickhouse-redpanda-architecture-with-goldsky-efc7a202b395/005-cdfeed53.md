---
source: blog
url: https://docs.goldsky.com/mirror/sources/subgraphs
topic: goldsky-a-gold-standard-architecture-with-clickhouse-and-redpanda
ch_version_introduced: '1.17'
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 8
---

with users exploiting its unrivaled query performance, cost efficiency and enhanced SQL for datasets, which often reach the TiB. Querying blockchain data with SQL is intuitive and popularized by services such as [dune](https://dune.com/docs/data-tables/raw/solana/blocks/). ### ClickHouse for backfills [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#clickhouse-for-backfills)

More recently, Goldsky has begun exploring using ClickHouse for backfilling data. This is often a requirement for customers who need a complete or filtered set of the data. In these cases, ClickHouse can be used to efficiently identify the subset and redirect to the Goldsky pipeline. Redpanda can be used for subsequent updates. This was implemented using a custom hybrid source, which is capable of consuming data from both sources: ClickHouse for the backfill and Redpanda for the incremental. Any aggregations defined in the pipeline would work across both ClickHouse and Redpanda without the user having to know where the data comes from.

## Challenges \& lessons [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#challenges--lessons)

Goldsky’s principal challenge with ClickHouse involved the use of the [ReplacingMergeTree](https://clickhouse.com/blog/clickhouse-postgresql-change-data-capture-cdc-part-1) engine type, and learning how to use it optimally. This engine choice ensures that updates (or duplicate events) can be efficiently handled. For optimization purposes, Goldsky specifically exploits:

- The ability to [emulate the PREWHERE condition](https://clickhouse.com/blog/clickhouse-postgresql-change-data-capture-cdc-part-1#final-performance) for the ReplacingMergeTree
- Utilizes partitions for [efficient querying](https://clickhouse.com/blog/clickhouse-postgresql-change-data-capture-cdc-part-1#exploiting-partitions)
- Recent abilities to [control the number of threads](https://clickhouse.com/docs/en/operations/settings/settings#max-final-threads) to use for the FINAL operator

Furthermore, Goldsky provides the ability for users to customize their `ORDER BY` key to align with their access patterns. This is typically a block timestamp or an address. In future, they hope to exploit the support for [projections for the ReplacingMergeTree engine](https://github.com/ClickHouse/ClickHouse/issues/33678).

### An example dataset [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#an-example-dataset)

At ClickHouse, we are always looking for large datasets to expose in our public instances. Keen to test the Goldsky service, we were excited by Goldsky’s offer to send a blockchain to one of our public instances. Looking for a well adopted chain with a significant number of transactions, we settled on Base.
