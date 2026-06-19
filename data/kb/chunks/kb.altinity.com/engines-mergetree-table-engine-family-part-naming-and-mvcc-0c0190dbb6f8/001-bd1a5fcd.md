---
source: kb.altinity.com
url: https://github.com/Altinity/altinityknowledgebase/commit/3e41a19644b66d46db743db20321bd5b94b545df
topic: part-names-mvcc-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 2
---

# Part names \& MVCC \| Altinity® Knowledge Base for ClickHouse®

1. [Engines](/engines/)
2. [MergeTree table engine family](/engines/mergetree-table-engine-family/)
3. Part names \& MVCC
# Part names \& MVCC

Part names \& multiversion concurrency control.## Part names \& multiversion concurrency control

Part name format is:

```
<partitionid>_<min_block_number>_<max_block_number>_<level>_<data_version>

```
system.parts contains all the information parsed.

partitionid is quite simple (it just comes from your partitioning key).

What are block\_numbers?

```
DROP TABLE IF EXISTS part_names;
create table part_names (date Date, n UInt8, m UInt8) engine=MergeTree PARTITION BY toYYYYMM(date) ORDER BY n;

insert into part_names VALUES (now(), 0, 0);
select name, partition_id, min_block_number, max_block_number, level, data_version from system.parts where table = 'part_names' and active;
┌─name─────────┬─partition_id─┬─min_block_number─┬─max_block_number─┬─level─┬─data_version─┐
│ 202203_1_1_0 │ 202203       │                1 │                1 │     0 │            1 │
└──────────────┴──────────────┴──────────────────┴──────────────────┴───────┴──────────────┘

insert into part_names VALUES (now(), 0, 0);
select name, partition_id, min_block_number, max_block_number, level, data_version from system.parts where table = 'part_names' and active;
┌─name─────────┬─partition_id─┬─min_block_number─┬─max_block_number─┬─level─┬─data_version─┐
│ 202203_1_1_0 │ 202203       │                1 │                1 │     0 │            1 │
│ 202203_2_2_0 │ 202203       │                2 │                2 │     0 │            2 │
└──────────────┴──────────────┴──────────────────┴──────────────────┴───────┴──────────────┘

insert into part_names VALUES (now(), 0, 0);
select name, partition_id, min_block_number, max_block_number, level, data_version from system.parts where table = 'part_names' and active;
┌─name─────────┬─partition_id─┬─min_block_number─┬─max_block_number─┬─level─┬─data_version─┐
│ 202203_1_1_0 │ 202203       │                1 │                1 │     0 │            1 │
│ 202203_2_2_0 │ 202203       │                2 │                2 │     0 │            2 │
│ 202203_3_3_0 │ 202203       │                3 │                3 │     0 │            3 │
└──────────────┴──────────────┴──────────────────┴──────────────────┴───────┴──────────────┘

```
As you can see every insert creates a new incremental block\_number which is written in part names both as \<min\_block\_number\> and \<min\_block\_number\>
(and the level is 0 meaning that the part was never merged).

Those block numbering works in the scope of partition (for Replicated table) or globally across all partition (for plain MergeTree table).

ClickHouse® always merge only continuous blocks . And new part names always refer to the minimum and maximum block numbers.

```
OPTIMIZE TABLE part_names;

┌─name─────────┬─partition_id─┬─min_block_number─┬─max_block_number─┬─level─┬─data_version─┐
│ 202203_1_3_1 │ 202203       │                1 │                3 │     1 │            1 │
└──────────────┴──────────────┴──────────────────┴──────────────────┴───────┴──────────────┘

```
As you can see here \- three parts (with block number 1,2,3\) were merged and they formed the new part with name 1\_3 as min/max block size.
Level get incremented.
