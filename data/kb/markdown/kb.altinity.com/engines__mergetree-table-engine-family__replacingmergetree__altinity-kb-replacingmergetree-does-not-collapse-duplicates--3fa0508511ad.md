# ReplacingMergeTree does not collapse duplicates \| Altinity® Knowledge Base for ClickHouse®


1. [Engines](/engines/)
2. [MergeTree table engine family](/engines/mergetree-table-engine-family/)
3. [ReplacingMergeTree](/engines/mergetree-table-engine-family/replacingmergetree/)
4. ReplacingMergeTree does not collapse duplicates
# ReplacingMergeTree does not collapse duplicates

**Hi there, I have a question about replacing merge trees. I have set up a
[Materialized View](https://www.youtube.com/watch?v=THDk625DGsQ)
with ReplacingMergeTree table, but even if I call optimize on it, the parts don’t get merged. I filled that table yesterday, nothing happened since then. What should I do?**

Merges are eventual and may never happen. It depends on the number of inserts that happened after, the number of parts in the partition, size of parts.
If the total size of input parts are greater than the maximum part size then they will never be merged.

[https://clickhouse.com/docs/en/operations/settings/merge\-tree\-settings\#max\-bytes\-to\-merge\-at\-max\-space\-in\-pool](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings#max-bytes-to-merge-at-max-space-in-pool)

[https://clickhouse.com/docs/en/engines/table\-engines/mergetree\-family/replacingmergetree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree)
*ReplacingMergeTree is suitable for clearing out duplicate data in the background in order to save space, but it doesn’t guarantee the absence of duplicates.*

Last modified 2024\.07\.29: [Site cleanup, mostly minor changes (3e41a19\)](https://github.com/Altinity/altinityknowledgebase/commit/3e41a19644b66d46db743db20321bd5b94b545df)
