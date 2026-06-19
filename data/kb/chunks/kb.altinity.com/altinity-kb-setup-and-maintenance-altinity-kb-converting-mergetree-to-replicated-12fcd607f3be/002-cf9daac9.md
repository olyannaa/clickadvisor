---
source: kb.altinity.com
url: https://clickhouse.tech/docs/en/engines/table\-engines/mergetree\-family/replication/\#converting\-from\-mergetree\-to\-replicatedmergetree](https://clickhouse.tech/docs/en/engines/table-engines/mergetree-family/replication/#converting-from-mergetree-to-replicatedmergetree
topic: converting-mergetree-to-replicated-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 2
---

free from a compute and disk space perspective. This feature utilizes filesystem hard\-links and the fact that files are immutable in ClickHouse® (it’s the core of the ClickHouse design, filesystem hard\-links and such file manipulations are widely used).

```
create table foo( A Int64, D Date, S String ) 
Engine MergeTree 
partition by toYYYYMM(D) order by A;

insert into foo select number, today(), '' from numbers(1e8);
insert into foo select number, today()-60, '' from numbers(1e8);

select count() from foo;
┌───count()─┐
│ 200000000 │
└───────────┘

create table foo_replicated as foo 
Engine ReplicatedMergeTree('/clickhouse/{cluster}/tables/{database}/{table}/{shard}','{replica}')
partition by toYYYYMM(D) order by A;

SYSTEM STOP MERGES;

SELECT DISTINCT 'ALTER TABLE foo_replicated ATTACH PARTITION ID \'' || partition_id || '\' FROM foo;' from system.parts WHERE table = 'foo' AND active;
┌─concat('ALTER TABLE foo_replicated ATTACH PARTITION ID \'', partition_id, '\' FROM foo;')─┐
│ ALTER TABLE foo_replicated ATTACH PARTITION ID '202111' FROM foo;                         │
│ ALTER TABLE foo_replicated ATTACH PARTITION ID '202201' FROM foo;                         │
└───────────────────────────────────────────────────────────────────────────────────────────┘

clickhouse-client -q "SELECT DISTINCT 'ALTER TABLE foo_replicated ATTACH PARTITION ID \'' || partition_id || '\' FROM foo;' from system.parts WHERE table = 'foo' format TabSeparatedRaw" |clickhouse-client -mn

SYSTEM START MERGES;

SELECT count() FROM foo_replicated;
┌───count()─┐
│ 200000000 │
└───────────┘

rename table foo to foo_old, foo_replicated to foo;

-- you can drop foo_old any time later, it's kinda a cheap backup, 
-- it cost nothing until you insert a lot of additional data into foo_replicated

```
Last modified 2025\.04\.09: [SEO improvements to make content easier to find (3b6158c)](https://github.com/Altinity/altinityknowledgebase/commit/3b6158c2a22100a97198a07184f2bce18e189d37)
