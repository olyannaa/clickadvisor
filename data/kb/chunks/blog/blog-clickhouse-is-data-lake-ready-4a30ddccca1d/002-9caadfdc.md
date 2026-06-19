---
source: blog
url: https://clickhouse.com/clickhouse-for-data-lakes
topic: clickhouse-is-data-lake-ready
ch_version_introduced: '0.5'
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 12
---

well: process Parquet files quickly, work with open table formats like Iceberg and Delta Lake, and integrate with the catalogs that sit on top. Here's how we've built out each of these capabilities over the past two years.

We started by shipping initial support for the Apache Iceberg format ([23\.3](https://clickhouse.com/blog/clickhouse-release-23-02#iceberg-right-ahead---support-for-apache-iceberg-ucasfl)), allowing the data to be read natively on object storage and giving users their first way to use **ClickHouse as a query engine for lake data**. We followed that with Parallel Replicas ([25\.8](https://clickhouse.com/blog/clickhouse-release-25-08)), enabling query execution to be distributed across multiple nodes for lake\-scale workloads.

From there, we invested heavily in [Parquet](https://clickhouse.com/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics), the foundational file format underneath Iceberg and Delta Lake tables. We added row group skipping using Parquet metadata [(23\.8\)](https://clickhouse.com/blog/clickhouse-release-23-08), enabled fast counts, and allowed file name metadata to be used in filters to avoid unnecessary file reads. In ([23\.7](https://clickhouse.com/blog/clickhouse-release-23-07#parquet-writing-improvements-michael-kolupaev))we improved Parquet write performance. On the storage side, we extended support to Azure Blob Storage ([23\.5](https://clickhouse.com/blog/clickhouse-release-23-05)), so ClickHouse wasn't limited to S3 and GCS.

In [24\.12](https://clickhouse.com/blog/clickhouse-release-24-12), we introduced our first catalog support with Unity Catalog, along with schema evolution. Users could now query Iceberg data from a catalog managed by an external service, with ClickHouse automatically detecting when columns were added, removed, renamed, or their types changed. The Polaris catalog was supported as well.

We also put significant effort in integrating the Delta Rust Kernel into ClickHouse, replacing our original Delta Lake reader. Rather than reinventing the wheel, we built on the community's open\-source kernel, and in doing so unlocked Delta Lake reads, writes, changed data feed support, schema evolution, time travel, partition pruning, and statistic\-based pruning.

Catalog support kept expanding in [25\.3](https://clickhouse.com/blog/clickhouse-release-25-03) where we added AWS Glue and Delta Lake support for the Unity Catalog. Since then we've added support for Microsoft OneLake, Iceberg REST Catalog, and AWS Glue, providing a truly catalog\-agnostic solution, letting users decide how they wish to manage their tables. In [25\.4](https://clickhouse.com/blog/clickhouse-release-25-04), we added time travel for Iceberg, letting users query previous snapshots of their data. This is especially important for data warehouse\-style workloads where auditability and point\-in\-time queries matter. In [25\.6](https://clickhouse.com/blog/clickhouse-release-25-06), we shipped JSON in Parquet support and deeper Iceberg history introspection, giving users more visibility into how their tables evolve over time.
