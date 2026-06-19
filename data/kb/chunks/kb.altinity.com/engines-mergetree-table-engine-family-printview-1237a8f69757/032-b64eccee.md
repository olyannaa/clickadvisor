---
source: kb.altinity.com
url: https://github.com/ClickHouse/clickhouse\-presentations/blob/master/meetup41/merge\_tree.pdf](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup41/merge_tree.pdf
topic: mergetree-table-engine-family-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '192.168'
last_updated: '2026-06-12'
chunk_index: 32
total_chunks_in_doc: 32
---

split into several ones by using an expression like `cityHash64(id) % 50 = 0` as a sharding key. The ingesting app should calculate the shard number before sending data to internal buffers that will be flushed to INSERTs.

```
-- emulate insert into distributed table
INSERT INTO function remote('localhos{t,t,t}',default,Stage,id)
SELECT
    (rand() % 1E6)*100 AS id,
    --number AS id,
    ['HR', 'Finance', 'Engineering', 'Sales', 'Marketing'][rand() % 5 + 1] AS Department,
    rand() % 1000 AS metric1,
    (rand() % 10000) / 100.0 AS metric2,
    2 AS _version,
    1 AS sign
FROM numbers(1000)
settings prefer_localhost_replica=0;

```
