---
source: kb.altinity.com
url: https://github.com/ClickHouse/ClickHouse/blob/8ab5270ded39c8b044f60f73c1de00c8117ab8f2/src/Interpreters/Aggregator.cpp#L382
topic: queries-syntax-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '8.888'
last_updated: '2026-06-12'
chunk_index: 50
total_chunks_in_doc: 117
---

[https://fiddle.clickhouse.com/7f331eb2\-9408\-4813\-9c67\-caef4cdd227d](https://fiddle.clickhouse.com/7f331eb2-9408-4813-9c67-caef4cdd227d) Explain result: ReadFromMergeTree (weekly\_projection) ``` Expression ((Project names + Projection)) Aggregating Expression ReadFromMergeTree (weekly_projection) Indexes: PrimaryKey Condition: true Parts: 9/9 Granules: 9/1223 ``` ## check parts - has the projection materialized - does not have lightweight deletes

```
SELECT
    p.database AS base_database,
    p.table AS base_table,
    p.name AS base_part_name,         -- Name of the part in the base table
    p.has_lightweight_delete,
    pp.active
FROM system.parts AS p  -- Alias for the base table's parts
LEFT JOIN system.projection_parts AS pp -- Alias for the projection's parts
ON    p.database = pp.database AND p.table = pp.table
  AND p.name = pp.parent_name
  AND pp.name = 'projection'
WHERE
    p.database = 'database'
    AND p.table = 'table'
    AND p.active  -- Consider only active parts of the base table
  -- and not pp.active          -- see only missed in the list
ORDER BY p.database, p.table, p.name;

```
## Recalculate on Merge

What happens in the case of non\-trivial background merges in ReplacingMergeTree, AggregatingMergeTree and similar, and OPTIMIZE table DEDUPLICATE queries?

- Before version 24\.8, projections became out of sync with the main data.
- Since version 24\.8, it is controlled by a new table\-level setting:  
[deduplicate\_merge\_projection\_mode](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings#deduplicate_merge_projection_mode)
\= `throw`/`drop`/`rebuild`
- Somewhere later (before 25\.3\) `ignore` option was introduced. It can be helpful for cases when SummingMergeTree is used with Projections and no DELETE operation in any flavor (Replacing/Collapsing/DELETE/ALTER DELETE) is executed over the table.

However, projection usage is still disabled for FINAL queries. So, you have to use OPTIMIZE FINAL or SELECT …GROUP BY instead of FINAL for fighting duplicates between parts

```
CREATE TABLE users (uid Int16, name String, version Int16,
  projection xx (
     select name,uid,version order by name
  )
) ENGINE=ReplacingMergeTree order by uid
settings deduplicate_merge_projection_mode='rebuild'
  ;

INSERT INTO users
SELECT 
    number AS uid,
    concat('User_', toString(uid)) AS name,
    1 AS version  
FROM numbers(100000);

INSERT INTO users
SELECT 
    number AS uid,
    concat('User_', toString(uid)) AS name,
    2 AS version  
FROM numbers(100000);

SELECT 'duplicate',name,uid,version FROM users 
where name ='User_98304' 
settings force_optimize_projection=1 ;

SELECT 'dedup by group by/limit 1 by',name,uid,version FROM users 
where name ='User_98304' 
order by version DESC
limit 1 by uid
settings force_optimize_projection=1
;

optimize table users final ;

SELECT 'dedup after optimize',name,uid,version FROM users 
where name ='User_98304' 
settings force_optimize_projection=1 ;

```
[https://fiddle.clickhouse.com/e1977a66\-09ce\-43c4\-aabc\-508c957d44d7](https://fiddle.clickhouse.com/e1977a66-09ce-43c4-aabc-508c957d44d7)

## System tables

- system.projections
- system.projection\_parts
- system.projection\_parts\_columns
