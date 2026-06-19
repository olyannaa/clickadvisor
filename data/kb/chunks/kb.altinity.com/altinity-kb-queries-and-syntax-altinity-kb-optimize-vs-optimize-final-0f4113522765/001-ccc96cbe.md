---
source: kb.altinity.com
url: https://github.com/Altinity/altinityknowledgebase/commit/3e41a19644b66d46db743db20321bd5b94b545df
topic: optimize-vs-optimize-final-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 1
---

# OPTIMIZE vs OPTIMIZE FINAL \| Altinity® Knowledge Base for ClickHouse®

1. [Queries \& Syntax](/altinity-kb-queries-and-syntax/)
2. OPTIMIZE vs OPTIMIZE FINAL
# OPTIMIZE vs OPTIMIZE FINAL

`OPTIMIZE TABLE xyz` – this initiates an unscheduled merge.

## Example

You have 40 parts in 3 partitions. This unscheduled merge selects some partition (i.e. February) and selects 3 small parts to merge, then merge them into a single part. You get 38 parts in the result.

`OPTIMIZE TABLE xyz FINAL` – initiates a cycle of unscheduled merges.

ClickHouse® merges parts in this table until will remains 1 part in each partition (if a system has enough free disk space). As a result, you get 3 parts, 1 part per partition. In this case, ClickHouse rewrites parts even if they are already merged into a single part. It creates a huge CPU / Disk load if the table (XYZ) is huge. ClickHouse reads / uncompress / merge / compress / writes all data in the table.

If this table has size 1TB it could take around 3 hours to complete.

So we don’t recommend running `OPTIMIZE TABLE xyz FINAL` against tables with more than 10million rows.

Last modified 2024\.07\.29: [Site cleanup, mostly minor changes (3e41a19\)](https://github.com/Altinity/altinityknowledgebase/commit/3e41a19644b66d46db743db20321bd5b94b545df)
