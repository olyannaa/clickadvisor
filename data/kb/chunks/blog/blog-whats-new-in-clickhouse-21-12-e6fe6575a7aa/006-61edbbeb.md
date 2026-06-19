---
source: blog
url: https://zookeeper.apache.org/doc/r3.4.8/zookeeperAdmin.html#sc_zkCommands
topic: what-s-new-in-clickhouse-21-12
ch_version_introduced: '21.12'
last_updated: '2026-06-12'
chunk_index: 6
total_chunks_in_doc: 7
---

conditions and remove the conditions that are proved to be satisfied by constraints. It is controlled by the `convert_query_to_cnf` setting. You can also enable `optimize_append_index`. With this setting ClickHouse will derive more conditions on the table primary key.

The idea is so powerful that we cannot resist adding one more feature: *indices for hypothesis*.

```
INDEX my_index (a < b) TYPE hypothesis GRANULARITY 1

```

The expression is checked and the result (true/false) is written as an index for query optimization.

**How does this help you?**

Especially in large ClickHouse deployments with many complex tables it can be hard for users to always be up to date on the best way to query a given dataset. Constraints can help optimize queries without having to change the query structure itself. They can also make it easier to make changes to tables.

For example, let’s say you have a table containing web requests and it includes a URL column that contains the full URL of each request. Many times, users will want to know the top level domain (.com, .co.uk, etc.), something ClickHouse provides the `topLevelDomain` function to calculate. If you discover that many people are using this function you might decide to create a new materialized column that pre\-calculates the top level domain for each record.

Rather than tell all your users to change their queries you can use a table constraint to tell ClickHouse that each time a user tries to call the `topLevelDomain` function the request should be rewritten to use the new materialized column.

## **Read Large Remote Files In Chunks** [\#](/blog/whats-new-in-clickhouse-21-12#read-large-remote-files-in-chunks-)

ClickHouse combines a fast query engine and efficient data storage. It also allows to integrate external data sources for data import and export or even to process external datasets on the fly without the need for data import or preprocessing.

When reading large files in `Parquet`, `ORC`, and `Arrow` format using the `s3`, `url`, and `hdfs` table functions, ClickHouse will now automatically choose whether to read the entire file at once or read parts of it incrementally. This is now enabled by default and the setting `remote_read_min_bytes_for_seek` controls when to switch from reading it all to reading in chunks. The default is 1MiB.
