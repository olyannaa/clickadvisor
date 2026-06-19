---
source: blog
url: https://benchmark.clickhouse.com/
topic: building-a-medallion-architecture-with-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 9
---

may have been composed of multiple tables from the previous silver stage. The focus here is on applying final transformations and ensuring the highest data quality for consumption by end\-users or applications, such as reporting and user\-facing dashboards.

This layered approach to data pipelines aims to efficiently address challenges like data quality, duplication and schema inconsistencies. By transforming raw data incrementally, the Medallion architecture aims to ensure a clear lineage and progressively refined datasets that are ready for analysis or operational use.

> While we find the naming of the medallion architecture could be better since it does not directly convey the contents of the layers, there are useful processes to extract from each layer and the discipline it helps enforce.

## Medallion architecture with ClickHouse [\#](/blog/building-a-medallion-architecture-with-clickhouse#medallion-architecture-with-clickhouse)

In this section, we propose how each layer of the Medallion architecture can be implemented using ClickHouse and how native features can be used to move data between them. This represents a flexible and evolving approach based on our internal experience and insights from our users, and we welcome feedback to refine these practices further.

### Bronze layer with ClickHouse [\#](/blog/building-a-medallion-architecture-with-clickhouse#bronze-layer-with-clickhouse)

The Bronze layer serves as the entry point for raw, unprocessed data, optimized for high\-throughput ingestion using ClickHouse’s flexible and performant constructs. Potentially acting as a historical archive, it can preserve raw data for lineage, debugging, or reprocessing without requiring complete cleansing or deduplication upfront. This focus on performance and flexibility establishes a robust foundation for downstream refinement and transformation in subsequent stages.

[![](/uploads/diagram_2_medallion_d8eba4506b.png)](/uploads/diagram_2_medallion_d8eba4506b.png)

Key features of the Bronze layer when implemented with ClickHouse include:

#### Ingestion from sources [\#](/blog/building-a-medallion-architecture-with-clickhouse#ingestion-from-sources)

Data can be ingested into this layer directly via clients, ELT tools like Fivetran, or by consuming streams from Kafka using ClickPipes or the ClickHouse Kafka connector. [S3Queue](https://clickhouse.com/docs/en/engines/table-engines/integrations/s3queue) and [ClickPipes](https://clickhouse.com/docs/en/integrations/clickpipes), in ClickHouse Cloud, provide additional options for reading data incrementally from S3 buckets in over 70 data formats (optionally compressed), including Parquet and lake formats such as Iceberg. This approach of using S3 as a staging area is particularly common when processing larger semi\-structured data whose schema is less consistent.

#### Optimization for fast inserts [\#](/blog/building-a-medallion-architecture-with-clickhouse#optimization-for-fast-inserts)
