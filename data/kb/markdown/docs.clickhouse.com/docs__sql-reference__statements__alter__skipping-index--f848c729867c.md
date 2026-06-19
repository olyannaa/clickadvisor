# Manipulating Data Skipping Indices \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [ALTER](/docs/sql-reference/statements/alter)- INDEX
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/skipping-index.md)# Manipulating Data Skipping Indices

The following operations are available:


## ADD INDEX[​](#add-index "Direct link to ADD INDEX")


`ALTER TABLE [db.]table_name [ON CLUSTER cluster] ADD INDEX [IF NOT EXISTS] name expression TYPE type [GRANULARITY value] [FIRST|AFTER name]` \- Adds index description to tables metadata.


## DROP INDEX[​](#drop-index "Direct link to DROP INDEX")


`ALTER TABLE [db.]table_name [ON CLUSTER cluster] DROP INDEX [IF EXISTS] name` \- Removes index description from tables metadata and deletes index files from disk. Implemented as a [mutation](/docs/sql-reference/statements/alter#mutations).


## MATERIALIZE INDEX[​](#materialize-index "Direct link to MATERIALIZE INDEX")


`ALTER TABLE [db.]table_name [ON CLUSTER cluster] MATERIALIZE INDEX [IF EXISTS] name [IN PARTITION partition_name]` \- Rebuilds the secondary index `name` for the specified `partition_name`. Implemented as a [mutation](/docs/sql-reference/statements/alter#mutations). If `IN PARTITION` part is omitted then it rebuilds the index for the whole table data.


## CLEAR INDEX[​](#clear-index "Direct link to CLEAR INDEX")


`ALTER TABLE [db.]table_name [ON CLUSTER cluster] CLEAR INDEX [IF EXISTS] name [IN PARTITION partition_name]` \- Deletes the secondary index files from disk without removing description. Implemented as a [mutation](/docs/sql-reference/statements/alter#mutations).


The commands `ADD`, `DROP`, and `CLEAR` are lightweight in the sense that they only change metadata or remove files.
Also, they are replicated, syncing indices metadata via ClickHouse Keeper or ZooKeeper.


NoteIndex manipulation is supported only for tables with [`*MergeTree`](/docs/engines/table-engines/mergetree-family/mergetree) engine (including [replicated](/docs/engines/table-engines/mergetree-family/replication) variants).

[PreviousSAMPLE BY](/docs/sql-reference/statements/alter/sample-by)[NextCONSTRAINT](/docs/sql-reference/statements/alter/constraint)- [ADD INDEX](#add-index)- [DROP INDEX](#drop-index)- [MATERIALIZE INDEX](#materialize-index)- [CLEAR INDEX](#clear-index)
Was this page helpful?
