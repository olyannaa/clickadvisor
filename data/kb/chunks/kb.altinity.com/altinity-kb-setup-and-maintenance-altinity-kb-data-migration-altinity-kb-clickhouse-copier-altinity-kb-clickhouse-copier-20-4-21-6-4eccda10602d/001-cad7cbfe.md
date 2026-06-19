---
source: kb.altinity.com
url: https://github.com/Altinity/altinityknowledgebase/commit/3e41a19644b66d46db743db20321bd5b94b545df
topic: clickhouse-copier-20-4-21-6-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 5
---

# clickhouse\-copier 20\.4 \- 21\.6 \| Altinity® Knowledge Base for ClickHouse®

1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. [Data Migration](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/)
3. [clickhouse\-copier](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/altinity-kb-clickhouse-copier/)
4. clickhouse\-copier 20\.4 \- 21\.6
# clickhouse\-copier 20\.4 \- 21\.6

`clickhouse-copier` was created to move data between clusters.
It runs simple `INSERT…SELECT` queries and can copy data between tables with different engine parameters and between clusters with different number of shards.
In the task configuration file you need to describe the layout of the source and the target cluster, and list the tables that you need to copy. You can copy whole tables or specific partitions.
`clickhouse-copier` uses temporary distributed tables to select from the source cluster and insert into the target cluster.

The behavior of `clickhouse-copier` was changed in 20\.4:
