---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-joins-under-the-hood-hash-join-parallel-hash-join-grace-hash-join-clickhouse
ch_version_introduced: '1.00'
last_updated: '2026-09-07'
chunk_index: 15
total_chunks_in_doc: 17
---

asking ClickHouse to send trace\-level logs during the execution to the ClickHouse command line client. We execute the grace hash join query with a `max_threads` setting of 2 and a `grace_hash_join_initial_buckets` value of 3 (note the `send_logs_level='trace'` setting):

```

./clickhouse client --host ea3kq2u4fm.eu-west-1.aws.clickhouse.cloud --secure --password  --database=imdb_large --send_logs_level='trace' --query "
SELECT *
FROM actors AS a
JOIN roles AS r ON a.id = r.actor_id
FORMAT Null
SETTINGS max_threads = 2, join_algorithm = 'grace_hash', grace_hash_join_initial_buckets = 3;"

    ...
... GraceHashJoin: Initialize 4 buckets
... GraceHashJoin: Joining file bucket 0
    ...
... imdb_large.actors ...: Reading approx. 1000000 rows with 2 streams
    ...
... imdb_large.roles ...: Reading approx. 100000000 rows with 2 streams
    ...
... GraceHashJoin: Joining file bucket 1
... GraceHashJoin: Loaded bucket 1 with 250000(/25000823) rows
    ...
... GraceHashJoin: Joining file bucket 2
... GraceHashJoin: Loaded bucket 2 with 250000(/24996460) rows
    ...
... GraceHashJoin: Joining file bucket 3
... GraceHashJoin: Loaded bucket 3 with 250000(/25000742) rows
    ...
... GraceHashJoin: Finished loading all 4 buckets
    ...


```

We can now see that 4 (instead of 3\) initial buckets were created. Because, as mentioned before, ClickHouse always rounds the set value for `grace_hash_join_initial_buckets` up to the closest power of two. We also see how 2 parallel stream stages are used per table for reading the table’s rows. The first corresponding bucket (bucket 0 in the trace log messages above) of both tables gets immediately joined.

The other 3 buckets are written to disk, and later sequentially loaded for joining. We see that the 1 million, and the 100 million rows from both tables were evenly split \- 250 thousand rows, and \~25 million rows, respectively, per bucket.

For comparison, we execute the grace hash join query with a `max_threads` setting of 4 and a `grace_hash_join_initial_buckets` value of 8:
