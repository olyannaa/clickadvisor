# Number of active parts in a partition \| Altinity® Knowledge Base for ClickHouse®


1. [Useful queries](/altinity-kb-useful-queries/)
2. Number of active parts in a partition
# Number of active parts in a partition

## Q: Why do I have several active parts in a partition? Why ClickHouse® does not merge them immediately?

### A: CH does not merge parts by time

Merge scheduler selects parts by own algorithm based on the current node workload / number of parts / size of parts.

CH merge scheduler balances between a big number of parts and a wasting resources on merges.

Merges are CPU/DISK IO expensive. If CH will merge every new part then all resources will be spend on merges and will no resources remain on queries (selects ).

CH will not merge parts with a combined size greater than 150 GB [max\_bytes\_to\_merge\_at\_max\_space\_in\_pool](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings#max-bytes-to-merge-at-max-space-in-pool)
.


```
SELECT
    database,
    table,
    partition,
    sum(rows) AS rows,
    count() AS part_count
FROM system.parts
WHERE (active = 1) AND (table LIKE '%') AND (database LIKE '%')
GROUP BY
    database,
    table,
    partition
ORDER BY part_count DESC
limit 20

```
Last modified 2024\.12\.27: [Update altinity\-kb\-number\-of\-active\-parts\-in\-a\-partition.md (fc2aa89\)](https://github.com/Altinity/altinityknowledgebase/commit/fc2aa896de278d0f7df5fd41f384347882119708)
