---
source: kb.altinity.com
url: http://s3.us-east-1.amazonaws.com/BUCKET_NAME/test_s3_disk/</endpoint>
topic: setup-maintenance-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '98.091'
last_updated: '2026-06-12'
chunk_index: 111
total_chunks_in_doc: 186
---

system.replicas SYSTEM DROP REPLICA 'replica_name' FROM ZKPATH '/table_path_in_zk/'; ``` ### Query to generate all the DDL: With this query you can generate the DDL script that will do the fetch and attach operations for each table and partition.

```
SELECT
    DISTINCT
    'alter table '||database||'.'||table||' FETCH PARTITION '''||partition_id||''' FROM '''||zookeeper_path||'''; '
    ||'alter table '||database||'.'||table||' ATTACH PARTITION '''||partition_id||''';'
FROM system.parts INNER JOIN system.replicas USING (database, table)
WHERE database IN ('db1','db2' ... 'dbn') AND active

```
You could add an ORDER BY to manually make the list in the order you need, or use ORDER BY rand() to randomize it. You will then need to split the commands between the shards.

# 44\.6 \- Remote table function

Remote table function## remote(…) table function

Suitable for moving up to hundreds of gigabytes of data.

With bigger tables recommended approach is to slice the original data by some `WHERE` condition, ideally \- apply the condition on partitioning key, to avoid writing data to many partitions at once.

```
INSERT INTO staging_table SELECT * FROM remote(...) WHERE date='2021-04-13';
INSERT INTO staging_table SELECT * FROM remote(...) WHERE date='2021-04-12';
INSERT INTO staging_table SELECT * FROM remote(...) WHERE date='2021-04-11';
....

OR 

INSERT INTO FUNCTION remote(...) SELECT * FROM staging_table WHERE date='2021-04-11';
....

```
### Q. Can it create a bigger load on the source system?

Yes, it may use disk read \& network write bandwidth. But typically write speed is worse than the read speed, so most probably the receiver side will be a bottleneck, and the sender side will not be overloaded.

While of course it should be checked, every case is different.

### Q. Can I tune INSERT speed to make it faster?

Yes, by the cost of extra memory usage (on the receiver side).

ClickHouse® tries to form blocks of data in memory and while one of limit: `min_insert_block_size_rows` or `min_insert_block_size_bytes` being hit, ClickHouse dump this block on disk. If ClickHouse tries to execute insert in parallel (`max_insert_threads > 1`), it would form multiple blocks at one time.  
So maximum memory usage can be calculated like this: `max_insert_threads * first(min_insert_block_size_rows OR min_insert_block_size_bytes)`

Default values:
