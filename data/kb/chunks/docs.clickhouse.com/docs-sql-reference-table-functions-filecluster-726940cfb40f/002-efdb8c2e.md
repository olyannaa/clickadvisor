---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/fileCluster.md)#
topic: filecluster-clickhouse-docs
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 2
---

cluster node, and their content is identical across different nodes: ``` $ cat /var/lib/clickhouse/user_files/test1.csv 1,"file1" 11,"file11" $ cat /var/lib/clickhouse/user_files/test2.csv 2,"file2" 22,"file22" ``` For example, one can create these files by executing these two queries on every cluster node:

```
INSERT INTO TABLE FUNCTION file('file1.csv', 'CSV', 'i UInt32, s String') VALUES (1,'file1'), (11,'file11');
INSERT INTO TABLE FUNCTION file('file2.csv', 'CSV', 'i UInt32, s String') VALUES (2,'file2'), (22,'file22');

```

Now, read data contents of `test1.csv` and `test2.csv` via `fileCluster` table function:

```
SELECT * FROM fileCluster('my_cluster', 'file{1,2}.csv', 'CSV', 'i UInt32, s String') ORDER BY i, s

```

```
┌──i─┬─s──────┐
│  1 │ file1  │
│ 11 │ file11 │
└────┴────────┘
┌──i─┬─s──────┐
│  2 │ file2  │
│ 22 │ file22 │
└────┴────────┘

```

## Globs in Path[​](#globs-in-path "Direct link to Globs in Path")

All patterns supported by [File](/docs/sql-reference/table-functions/file#globs-in-path) table function are supported by FileCluster.

## Related[​](#related "Direct link to Related")

- [File table function](/docs/sql-reference/table-functions/file)
[Previousfile](/docs/sql-reference/table-functions/file)[Nextfilesystem](/docs/sql-reference/table-functions/filesystem)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned_value)- [Globs in Path](#globs-in-path)- [Related](#related)
Was this page helpful?
