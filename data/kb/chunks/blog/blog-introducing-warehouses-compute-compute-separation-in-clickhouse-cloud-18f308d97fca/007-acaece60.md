---
source: blog
url: https://dv2fzne24g.us-east-1.aws.clickhouse.cloud:8443>`
topic: introducing-warehouses-compute-compute-separation-in-clickhouse-cloud
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 7
total_chunks_in_doc: 10
---

full compute\-compute isolation, we allowed only read\-write services to perform background operations. This means that when you dedicate a read\-only service for a critical read workload, you can be sure that reads will not be affected by merges.

However, with multiple read\-write (RW) services, any of them can perform background merges for INSERT queries initiated on any of the services. This is because merges are not directly tied to the queries that triggered them. As a result, in rare cases, heavy write operations may impact each other, even when executed on different services. In the future, we plan to introduce a specialized setting that will enable users to control which RW services handle background operations and distribute these operations among RW services based on the queries that caused them.

### Warehouses limitations [\#](/blog/introducing-warehouses-compute-compute-separation-in-clickhouse-cloud#warehouses-limitations)

Though warehouses bring a lot of flexibility to ClickHouse Cloud, there are a few limitations that are presented in the current implementation and that we plan to remove later:
