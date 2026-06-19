# mysql \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- mysql
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/mysql.md)# mysql

Allows `SELECT` and `INSERT` queries to be performed on data that are stored on a remote MySQL server.


## Syntax[​](#syntax "Direct link to Syntax")



```
mysql({host:port, database, table, user, password[, replace_query, on_duplicate_clause] | named_collection[, option=value [,..]]})

```

## Arguments[​](#arguments "Direct link to Arguments")




| Argument Description| `host:port` MySQL server address.| `database` Remote database name.| `table` Remote table name.| `user` MySQL user.| `password` User password.| `replace_query` Flag that converts `INSERT INTO` queries to `REPLACE INTO`. Possible values: \- `0` \- The query is executed as `INSERT INTO`. \- `1` \- The query is executed as `REPLACE INTO`.| `on_duplicate_clause` The `ON DUPLICATE KEY on_duplicate_clause` expression that is added to the `INSERT` query. Can be specified only with `replace_query = 0` (if you simultaneously pass `replace_query = 1` and `on_duplicate_clause`, ClickHouse generates an exception). Example: `INSERT INTO t (c1,c2) VALUES ('a', 2) ON DUPLICATE KEY UPDATE c2 = c2 + 1;` `on_duplicate_clause` here is `UPDATE c2 = c2 + 1`. See the MySQL documentation to find which `on_duplicate_clause` you can use with the `ON DUPLICATE KEY` clause. | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


Arguments also can be passed using [named collections](/docs/operations/named-collections). In this case `host` and `port` should be specified separately. This approach is recommended for production environment.


Simple `WHERE` clauses such as `=, !=, >, >=, <, <=` are currently executed on the MySQL server.


The rest of the conditions and the `LIMIT` sampling constraint are executed in ClickHouse only after the query to MySQL finishes.


Supports multiple replicas that must be listed by `|`. For example:



```
SELECT name FROM mysql(`mysql{1|2|3}:3306`, 'mysql_database', 'mysql_table', 'user', 'password');

```

or



```
SELECT name FROM mysql(`mysql1:3306|mysql2:3306|mysql3:3306`, 'mysql_database', 'mysql_table', 'user', 'password');

```

## Returned value[​](#returned_value "Direct link to Returned value")


A table object with the same columns as the original MySQL table.


NoteSome data types of MySQL can be mapped to different ClickHouse types \- this is addressed by query\-level setting [mysql\_datatypes\_support\_level](/docs/operations/settings/settings#mysql_datatypes_support_level)


NoteIn the `INSERT` query to distinguish table function `mysql(...)` from table name with column names list, you must use keywords `FUNCTION` or `TABLE FUNCTION`. See examples below.


## Examples[​](#examples "Direct link to Examples")


Table in MySQL:



```
mysql> CREATE TABLE `test`.`test` (
    ->   `int_id` INT NOT NULL AUTO_INCREMENT,
    ->   `float` FLOAT NOT NULL,
    ->   PRIMARY KEY (`int_id`));

mysql> INSERT INTO test (`int_id`, `float`) VALUES (1,2);

mysql> SELECT * FROM test;
+--------+-------+
| int_id | float |
+--------+-------+
|      1 |     2 |
+--------+-------+

```

Selecting data from ClickHouse:



```
SELECT * FROM mysql('localhost:3306', 'test', 'test', 'bayonet', '123');

```

Or using [named collections](/docs/operations/named-collections):



```
CREATE NAMED COLLECTION creds AS
        host = 'localhost',
        port = 3306,
        database = 'test',
        user = 'bayonet',
        password = '123';
SELECT * FROM mysql(creds, table='test');

```


```
┌─int_id─┬─float─┐
│      1 │     2 │
└────────┴───────┘

```

Replacing and inserting:



```
INSERT INTO FUNCTION mysql('localhost:3306', 'test', 'test', 'bayonet', '123', 1) (int_id, float) VALUES (1, 3);
INSERT INTO TABLE FUNCTION mysql('localhost:3306', 'test', 'test', 'bayonet', '123', 0, 'UPDATE int_id = int_id + 1') (int_id, float) VALUES (1, 4);
SELECT * FROM mysql('localhost:3306', 'test', 'test', 'bayonet', '123');

```


```
┌─int_id─┬─float─┐
│      1 │     3 │
│      2 │     4 │
└────────┴───────┘

```

Copying data from MySQL table into ClickHouse table:



```
CREATE TABLE mysql_copy
(
   `id` UInt64,
   `datetime` DateTime('UTC'),
   `description` String,
)
ENGINE = MergeTree
ORDER BY (id,datetime);

INSERT INTO mysql_copy
SELECT * FROM mysql('host:port', 'database', 'table', 'user', 'password');

```

Or if copying only an incremental batch from MySQL based on the max current id:



```
INSERT INTO mysql_copy
SELECT * FROM mysql('host:port', 'database', 'table', 'user', 'password')
WHERE id > (SELECT max(id) FROM mysql_copy);

```

## Related[​](#related "Direct link to Related")


- [The 'MySQL' table engine](/docs/engines/table-engines/integrations/mysql)
- [Using MySQL as a dictionary source](/docs/sql-reference/statements/create/dictionary/sources/mysql)
- [mysql\_datatypes\_support\_level](/docs/operations/settings/settings#mysql_datatypes_support_level)
- [mysql\_map\_fixed\_string\_to\_text\_in\_show\_columns](/docs/operations/settings/settings#mysql_map_fixed_string_to_text_in_show_columns)
- [mysql\_map\_string\_to\_text\_in\_show\_columns](/docs/operations/settings/settings#mysql_map_string_to_text_in_show_columns)
- [mysql\_max\_rows\_to\_insert](/docs/operations/settings/settings#mysql_max_rows_to_insert)
[Previousmongodb](/docs/sql-reference/table-functions/mongodb)[Nextnull function](/docs/sql-reference/table-functions/null)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned_value)- [Examples](#examples)- [Related](#related)
Was this page helpful?
