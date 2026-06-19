# Removing tasks in the replication queue related to empty partitions \| Altinity® Knowledge Base for ClickHouse®


1. [Useful queries](/altinity-kb-useful-queries/)
2. Removing tasks in the replication queue related to empty partitions
# Removing tasks in the replication queue related to empty partitions

## Removing tasks in the replication queue related to empty partitions


```
SELECT 'ALTER TABLE ' || database || '.' || table || ' DROP PARTITION ID \''|| partition_id || '\';'  FROM 
(SELECT DISTINCT database, table, extract(new_part_name, '^[^_]+')  as partition_id FROM clusterAllReplicas('{cluster}', system.replication_queue) ) as rq
LEFT JOIN 
(SELECT database, table, partition_id, sum(rows) as rows_count, count() as part_count 
FROM clusterAllReplicas('{cluster}', system.parts)
WHERE active GROUP BY database, table, partition_id
)  as p
USING (database, table, partition_id)
WHERE p.rows_count = 0 AND p.part_count = 0
FORMAT TSVRaw;

```
Last modified 2023\.08\.09: [Create remove\_empty\_partitions\_from\_rq.md (b99ad36\)](https://github.com/Altinity/altinityknowledgebase/commit/b99ad367a8cde08377885884e151d7daae4e06ae)
