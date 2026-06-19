---
source: blog
url: https://docs.goldsky.com/mirror/sources/subgraphs
topic: goldsky-a-gold-standard-architecture-with-clickhouse-and-redpanda
ch_version_introduced: '1.17'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 8
---

this presented a challenge from a data engineering perspective \- how to efficiently stream the same TiB datasets to potentially 10s of thousands of ClickHouse instances while providing customer\-independent processing that may target only subsets. ## Architecture [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#architecture)

![gold_sky_architecture.png](/uploads/gold_sky_architecture_8455529196.png)
The Goldsky architecture consists of Redpanda, Apache Flink and ClickHouse. Data is pushed into Redpanda via direct indexers which can extract structures such as blocks, transactions, traces and logs. Each blockchain exists as multiple topics on Redpanda (one for each data type), from which Apache Flink can consume and transform events. Users write FlinkSQL to transform specific datasets, potentially starting from a specific position on the topic to time limit the data. Transformations are applied in stream before the data is delivered to ClickHouse for analytics. This multi\-tenant architecture allows Goldsky to efficiently process and deliver any crypto dataset to potentially thousands of ClickHouse clusters. All of this is exposed through a simple interface or API, abstracting the complexity and allowing the users to simply write transformations naturally in SQL.

> Readers may notice the subgraph module above. Subgraphs are a single\-threaded method of indexing that allows for users to write webassembly logic that process the blockchain sequentially using typescript. This allows for custom aggregations by reading and writing state, which can be an easier paradigm to start with. This also allows for additional HTTP calls to the ethereum network to pull contract state during the indexing process. These subgraphs can in turn be used to expose an API or inserted to ClickHouse for analytics. Further details [here](https://docs.goldsky.com/mirror/sources/subgraphs).

We explore each of these technology choices below.

### Redpanda as a backing store [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#redpanda-as-a-backing-store)

Goldsky expended significant effort ensuring all popular blockchains are transformed into a format which can realistically be easily consumed by other services such as ClickHouse. The schema\-driven Avro format represents their current preferred format. Once a blockchain has been transformed, there are several primary challenges:

- Efficient storage of the transformed data for later consumption by customers. The retention period here is infinite
- Keeping this data up\-to\-date such that users can enjoy access to the latest transactions and blocks
- Ensuring the data can be delivered with minimal end\-to\-end latency to any number of destinations, including ClickHouse
