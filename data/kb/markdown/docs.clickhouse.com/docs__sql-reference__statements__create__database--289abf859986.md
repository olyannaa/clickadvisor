# CREATE DATABASE \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- DATABASE
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/database.md)# CREATE DATABASE

Creates a new database.



```
CREATE DATABASE [IF NOT EXISTS] db_name [ON CLUSTER cluster] [ENGINE = engine(...)] [SETTINGS ...] [COMMENT 'Comment']

```

## Clauses[​](#clauses "Direct link to Clauses")


### IF NOT EXISTS[​](#if-not-exists "Direct link to IF NOT EXISTS")


If the `db_name` database already exists, then ClickHouse does not create a new database and:


- Doesn't throw an exception if clause is specified.
- Throws an exception if clause isn't specified.


### ON CLUSTER[​](#on-cluster "Direct link to ON CLUSTER")


ClickHouse creates the `db_name` database on all the servers of a specified cluster. More details in a [Distributed DDL](/docs/sql-reference/distributed-ddl) article.


### ENGINE[​](#engine "Direct link to ENGINE")


By default, ClickHouse uses its own [Atomic](/docs/engines/database-engines/atomic) database engine. There are also [MySQL](/docs/engines/database-engines/mysql), [PostgresSQL](/docs/engines/database-engines/postgresql), [MaterializedPostgreSQL](/docs/engines/database-engines/materialized-postgresql), [Replicated](/docs/engines/database-engines/replicated), [SQLite](/docs/engines/database-engines/sqlite).


### COMMENT[​](#comment "Direct link to COMMENT")


You can add a comment to the database when you are creating it.


The comment is supported for all database engines.


**Syntax**



```
CREATE DATABASE db_name ENGINE = engine(...) COMMENT 'Comment'

```

**Example**



```
CREATE DATABASE db_comment ENGINE = Memory COMMENT 'The temporary database';
SELECT name, comment FROM system.databases WHERE name = 'db_comment';

```


```
┌─name───────┬─comment────────────────┐
│ db_comment │ The temporary database │
└────────────┴────────────────────────┘

```

### SETTINGS[​](#settings "Direct link to SETTINGS")


#### lazy\_load\_tables[​](#lazy-load-tables "Direct link to lazy_load_tables")


When enabled, tables are not fully loaded during database startup. Instead, a lightweight proxy is created for each table and the real table engine is materialized on first access. This reduces startup time and memory usage for databases with many tables where only a subset is actively queried.



```
CREATE DATABASE db_name ENGINE = Atomic SETTINGS lazy_load_tables = 1;

```

Applies to database engines that store table metadata on disk (e.g. `Atomic`, `Ordinary`). Views, materialized views, dictionaries, and tables backed by table functions are always loaded eagerly regardless of this setting.


**When to use:** This setting is useful for databases with a large number of tables (hundreds or thousands) where only a subset is actively queried. It reduces server startup time and memory usage by deferring the creation of table engine objects, scanning of data parts, and initialization of background threads until first access.


**Impact on `system.tables`:**


- Before a table is accessed, `system.tables` shows its engine as `TableProxy`. After first access, it shows the real engine name (e.g. `MergeTree`).
- Columns like `total_rows` and `total_bytes` return `NULL` for unloaded tables because the real storage has not been created yet.


**Interaction with DDL operations:**


- `SELECT`, `INSERT`, `ALTER`, `DROP` transparently trigger loading of the real table engine on first use.
- `RENAME TABLE` works without triggering a load.
- Once a table is loaded, it stays loaded for the lifetime of the server process.


**Limitations:**


- Monitoring tools that rely on `system.tables` metadata (e.g. `total_rows`, `engine`) may see incomplete information for unloaded tables.
- The first query to an unloaded table incurs a one\-time loading cost (parsing the stored `CREATE TABLE` statement and initializing the engine).


Default value: `0` (disabled).

[PreviousEmbedded dictionaries](/docs/sql-reference/statements/create/dictionary/embedded)[NextTABLE](/docs/sql-reference/statements/create/table)- [Clauses](#clauses)
	- [IF NOT EXISTS](#if-not-exists)- [ON CLUSTER](#on-cluster)- [ENGINE](#engine)- [COMMENT](#comment)- [SETTINGS](#settings)
Was this page helpful?
