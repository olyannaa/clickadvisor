# postgresql \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- postgresql
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/postgresql.md)# postgresql

Allows `SELECT` and `INSERT` queries to be performed on data that is stored on a remote PostgreSQL server.


## Syntax[​](#syntax "Direct link to Syntax")



```
postgresql({host:port, database, table, user, password[, schema, [, on_conflict]] | named_collection[, option=value [,..]]})

```

## Arguments[​](#arguments "Direct link to Arguments")




| Argument Description| `host:port` PostgreSQL server address.| `database` Remote database name.| `table` Remote table name.| `user` PostgreSQL user.| `password` User password.| `schema` Non\-default table schema. Optional.| `on_conflict` Conflict resolution strategy. Example: `ON CONFLICT DO NOTHING`. Optional. | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


Arguments also can be passed using [named collections](/docs/operations/named-collections). In this case `host` and `port` should be specified separately. This approach is recommended for production environment.


## Returned value[​](#returned_value "Direct link to Returned value")


A table object with the same columns as the original PostgreSQL table.


NoteIn the `INSERT` query to distinguish table function `postgresql(...)` from table name with column names list you must use keywords `FUNCTION` or `TABLE FUNCTION`. See examples below.


## Implementation Details[​](#implementation-details "Direct link to Implementation Details")


`SELECT` queries on PostgreSQL side run as `COPY (SELECT ...) TO STDOUT` inside read\-only PostgreSQL transaction with commit after each `SELECT` query.


Simple `WHERE` clauses such as `=`, `!=`, `>`, `>=`, `<`, `<=`, and `IN` are executed on the PostgreSQL server.


All joins, aggregations, sorting, `IN [ array ]` conditions and the `LIMIT` sampling constraint are executed in ClickHouse only after the query to PostgreSQL finishes.


`INSERT` queries on PostgreSQL side run as `COPY "table_name" (field1, field2, ... fieldN) FROM STDIN` inside PostgreSQL transaction with auto\-commit after each `INSERT` statement.


PostgreSQL Array types converts into ClickHouse arrays.


NoteBe careful, in PostgreSQL an array data type column like Integer\[] may contain arrays of different dimensions in different rows, but in ClickHouse it is only allowed to have multidimensional arrays of the same dimension in all rows.


Supports multiple replicas that must be listed by `|`. For example:



```
SELECT name FROM postgresql(`postgres{1|2|3}:5432`, 'postgres_database', 'postgres_table', 'user', 'password');

```

or



```
SELECT name FROM postgresql(`postgres1:5431|postgres2:5432`, 'postgres_database', 'postgres_table', 'user', 'password');

```

Supports replicas priority for PostgreSQL dictionary source. The bigger the number in map, the less the priority. The highest priority is `0`.


## Examples[​](#examples "Direct link to Examples")


Table in PostgreSQL:



```
postgres=# CREATE TABLE "public"."test" (
"int_id" SERIAL,
"int_nullable" INT NULL DEFAULT NULL,
"float" FLOAT NOT NULL,
"str" VARCHAR(100) NOT NULL DEFAULT '',
"float_nullable" FLOAT NULL DEFAULT NULL,
PRIMARY KEY (int_id));

CREATE TABLE

postgres=# INSERT INTO test (int_id, str, "float") VALUES (1,'test',2);
INSERT 0 1

postgresql> SELECT * FROM test;
  int_id | int_nullable | float | str  | float_nullable
 --------+--------------+-------+------+----------------
       1 |              |     2 | test |
(1 row)

```

Selecting data from ClickHouse using plain arguments:



```
SELECT * FROM postgresql('localhost:5432', 'test', 'test', 'postgresql_user', 'password') WHERE str IN ('test');

```

Or using [named collections](/docs/operations/named-collections):



```
CREATE NAMED COLLECTION mypg AS
        host = 'localhost',
        port = 5432,
        database = 'test',
        user = 'postgresql_user',
        password = 'password';
SELECT * FROM postgresql(mypg, table='test') WHERE str IN ('test');

```


```
┌─int_id─┬─int_nullable─┬─float─┬─str──┬─float_nullable─┐
│      1 │         ᴺᵁᴸᴸ │     2 │ test │           ᴺᵁᴸᴸ │
└────────┴──────────────┴───────┴──────┴────────────────┘

```

Inserting:



```
INSERT INTO TABLE FUNCTION postgresql('localhost:5432', 'test', 'test', 'postgrsql_user', 'password') (int_id, float) VALUES (2, 3);
SELECT * FROM postgresql('localhost:5432', 'test', 'test', 'postgresql_user', 'password');

```


```
┌─int_id─┬─int_nullable─┬─float─┬─str──┬─float_nullable─┐
│      1 │         ᴺᵁᴸᴸ │     2 │ test │           ᴺᵁᴸᴸ │
│      2 │         ᴺᵁᴸᴸ │     3 │      │           ᴺᵁᴸᴸ │
└────────┴──────────────┴───────┴──────┴────────────────┘

```

Using Non\-default Schema:



```
postgres=# CREATE SCHEMA "nice.schema";

postgres=# CREATE TABLE "nice.schema"."nice.table" (a integer);

postgres=# INSERT INTO "nice.schema"."nice.table" SELECT i FROM generate_series(0, 99) as t(i)

```


```
CREATE TABLE pg_table_schema_with_dots (a UInt32)
        ENGINE PostgreSQL('localhost:5432', 'clickhouse', 'nice.table', 'postgrsql_user', 'password', 'nice.schema');

```

## Related[​](#related "Direct link to Related")


- [The PostgreSQL table engine](/docs/engines/table-engines/integrations/postgresql)
- [Using PostgreSQL as a dictionary source](/docs/sql-reference/statements/create/dictionary/sources/postgresql)


### Replicating or migrating Postgres data with with PeerDB[​](#replicating-or-migrating-postgres-data-with-with-peerdb "Direct link to Replicating or migrating Postgres data with with PeerDB")



> In addition to table functions, you can always use [PeerDB](https://docs.peerdb.io/introduction) by ClickHouse to set up a continuous data pipeline from Postgres to ClickHouse. PeerDB is a tool designed specifically to replicate data from Postgres to ClickHouse using change data capture (CDC).

[Previousodbc](/docs/sql-reference/table-functions/odbc)[Nextredis](/docs/sql-reference/table-functions/redis)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned_value)- [Implementation Details](#implementation-details)- [Examples](#examples)- [Related](#related)
	- [Replicating or migrating Postgres data with with PeerDB](#replicating-or-migrating-postgres-data-with-with-peerdb)
Was this page helpful?
