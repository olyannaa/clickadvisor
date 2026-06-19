# ATTACH Statement \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- ATTACH
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/attach.md)# ATTACH Statement

Attaches a table or a dictionary, for example, when moving a database to another server.


**Syntax**



```
ATTACH TABLE|DICTIONARY|DATABASE [IF NOT EXISTS] [db.]name [ON CLUSTER cluster] ...

```

The query does not create data on disk, but assumes that data is already in the appropriate places, and just adds information about the specified table, dictionary or database to the server. After executing the `ATTACH` query, the server will know about the existence of the table, dictionary or database.


If a table was previously detached ([DETACH](/docs/sql-reference/statements/detach) query), meaning that its structure is known, you can use shorthand without defining the structure.


## Attach Existing Table[​](#attach-existing-table "Direct link to Attach Existing Table")


**Syntax**



```
ATTACH TABLE [IF NOT EXISTS] [db.]name [ON CLUSTER cluster]

```

This query is used when starting the server. The server stores table metadata as files with `ATTACH` queries, which it simply runs at launch (with the exception of some system tables, which are explicitly created on the server).


If the table was detached permanently, it won't be reattached at the server start, so you need to use `ATTACH` query explicitly.


## Create New Table And Attach Data[​](#create-new-table-and-attach-data "Direct link to Create New Table And Attach Data")


### With Specified Path to Table Data[​](#with-specified-path-to-table-data "Direct link to With Specified Path to Table Data")


The query creates a new table with provided structure and attaches table data from the provided directory in `user_files`.


**Syntax**



```
ATTACH TABLE name FROM 'path/to/data/' (col1 Type1, ...)

```

**Example**



```
DROP TABLE IF EXISTS test;
INSERT INTO TABLE FUNCTION file('01188_attach/test/data.TSV', 'TSV', 's String, n UInt8') VALUES ('test', 42);
ATTACH TABLE test FROM '01188_attach/test' (s String, n UInt8) ENGINE = File(TSV);
SELECT * FROM test;

```


```
┌─s────┬──n─┐
│ test │ 42 │
└──────┴────┘

```

### With Specified Table UUID[​](#with-specified-table-uuid "Direct link to With Specified Table UUID")


This query creates a new table with provided structure and attaches data from the table with the specified UUID.
It is supported by the [Atomic](/docs/engines/database-engines/atomic) database engine.


**Syntax**



```
ATTACH TABLE name UUID '<uuid>' (col1 Type1, ...)

```

## Attach MergeTree table as ReplicatedMergeTree[​](#attach-mergetree-table-as-replicatedmergetree "Direct link to Attach MergeTree table as ReplicatedMergeTree")


Allows to attach non\-replicated MergeTree table as ReplicatedMergeTree. ReplicatedMergeTree table will be created with values of `default_replica_path` and `default_replica_name` settings. It is also possible to attach a replicated table as a regular MergeTree.


Note that table's data in ZooKeeper is not affected in this query. This means you have to add metadata in ZooKeeper using `SYSTEM RESTORE REPLICA` or clear it with `SYSTEM DROP REPLICA ... FROM ZKPATH ...` after attach.


If you are trying to add a replica to an existing ReplicatedMergeTree table, keep in mind that all the local data in converted MergeTree table will be detached.


**Syntax**



```
ATTACH TABLE [db.]name AS [NOT] REPLICATED

```

**Convert table to replicated**



```
DETACH TABLE test;
ATTACH TABLE test AS REPLICATED;
SYSTEM RESTORE REPLICA test;

```

**Convert table to not replicated**


Get ZooKeeper path and replica name for table:



```
SELECT replica_name, zookeeper_path FROM system.replicas WHERE table='test';

```


```
┌─replica_name─┬─zookeeper_path─────────────────────────────────────────────┐
│ r1           │ /clickhouse/tables/401e6a1f-9bf2-41a3-a900-abb7e94dff98/s1 │
└──────────────┴────────────────────────────────────────────────────────────┘

```

Attach table as not replicated and delete replica's data from ZooKeeper:



```
DETACH TABLE test;
ATTACH TABLE test AS NOT REPLICATED;
SYSTEM DROP REPLICA 'r1' FROM ZKPATH '/clickhouse/tables/401e6a1f-9bf2-41a3-a900-abb7e94dff98/s1';

```

## Attach Existing Dictionary[​](#attach-existing-dictionary "Direct link to Attach Existing Dictionary")


Attaches a previously detached dictionary.


**Syntax**



```
ATTACH DICTIONARY [IF NOT EXISTS] [db.]name [ON CLUSTER cluster]

```

## Attach Existing Database[​](#attach-existing-database "Direct link to Attach Existing Database")


Attaches a previously detached database.


**Syntax**



```
ATTACH DATABASE [IF NOT EXISTS] name [ENGINE=<database engine>] [ON CLUSTER cluster]

```
[PreviousUPDATE](/docs/sql-reference/statements/update)[NextCHECK TABLE](/docs/sql-reference/statements/check-table)- [Attach Existing Table](#attach-existing-table)- [Create New Table And Attach Data](#create-new-table-and-attach-data)
	- [With Specified Path to Table Data](#with-specified-path-to-table-data)- [With Specified Table UUID](#with-specified-table-uuid)- [Attach MergeTree table as ReplicatedMergeTree](#attach-mergetree-table-as-replicatedmergetree)- [Attach Existing Dictionary](#attach-existing-dictionary)- [Attach Existing Database](#attach-existing-database)
Was this page helpful?
