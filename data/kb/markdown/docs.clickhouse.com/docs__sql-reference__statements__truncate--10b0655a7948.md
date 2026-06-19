# TRUNCATE Statements \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- TRUNCATE
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/truncate.md)# TRUNCATE Statements

The `TRUNCATE` statement in ClickHouse is used to quickly remove all data from a table or database while preserving their structure.


## TRUNCATE TABLE[​](#truncate-table "Direct link to TRUNCATE TABLE")



```
TRUNCATE TABLE [IF EXISTS] [db.]name [ON CLUSTER cluster] [SYNC]

```

  



| Parameter Description| `IF EXISTS` Prevents an error if the table does not exist. If omitted, the query returns an error.| `db.name` Optional database name.| `ON CLUSTER cluster` Runs the command across a specified cluster.| `SYNC` Makes the truncation synchronous across replicas when using replicated tables. If omitted, truncation happens asynchronously by default. | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


You can use the [alter\_sync](/docs/operations/settings/settings#alter_sync) setting to set up waiting for actions to be executed on replicas.


You can specify how long (in seconds) to wait for inactive replicas to execute `TRUNCATE` queries with the [replication\_wait\_for\_inactive\_replica\_timeout](/docs/operations/settings/settings#replication_wait_for_inactive_replica_timeout) setting.


NoteIf the `alter_sync` is set to `2` and some replicas are not active for more than the time, specified by the `replication_wait_for_inactive_replica_timeout` setting, then an exception `UNFINISHED` is thrown.


The `TRUNCATE TABLE` query is **not supported** for the following table engines:


- [`View`](/docs/engines/table-engines/special/view)
- [`File`](/docs/engines/table-engines/special/file)
- [`URL`](/docs/engines/table-engines/special/url)
- [`Buffer`](/docs/engines/table-engines/special/buffer)
- [`Null`](/docs/engines/table-engines/special/null)


## TRUNCATE ALL TABLES[​](#truncate-all-tables "Direct link to TRUNCATE ALL TABLES")



```
TRUNCATE [ALL] TABLES FROM [IF EXISTS] db [LIKE | ILIKE | NOT LIKE '<pattern>'] [ON CLUSTER cluster]

```

  



| Parameter Description| `ALL` Removes data from all tables in the database.| `IF EXISTS` Prevents an error if the database does not exist.| `db` The database name.| `LIKE | ILIKE | NOT LIKE '<pattern>'` Filters tables by pattern.| `ON CLUSTER cluster` Runs the command across a cluster. | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


Removes all data from all tables in a database.


## TRUNCATE DATABASE[​](#truncate-database "Direct link to TRUNCATE DATABASE")



```
TRUNCATE DATABASE [IF EXISTS] db [ON CLUSTER cluster]

```

  



| Parameter Description| `IF EXISTS` Prevents an error if the database does not exist.| `db` The database name.| `ON CLUSTER cluster` Runs the command across a specified cluster. | | | | | | | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- |


Removes all tables from a database but keeps the database itself. When the clause `IF EXISTS` is omitted, the query returns an error if the database does not exist.


Note`TRUNCATE DATABASE` is not supported for `Replicated` databases. Instead, just `DROP` and `CREATE` the database.

[PreviousSET ROLE](/docs/sql-reference/statements/set-role)[NextEXECUTE AS](/docs/sql-reference/statements/execute_as)- [TRUNCATE TABLE](#truncate-table)- [TRUNCATE ALL TABLES](#truncate-all-tables)- [TRUNCATE DATABASE](#truncate-database)
Was this page helpful?
