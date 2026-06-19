# jdbc \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- jdbc
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/jdbc.md)# jdbc

Noteclickhouse\-jdbc\-bridge contains experimental codes and is no longer supported. It may contain reliability issues and security vulnerabilities. Use it at your own risk.
ClickHouse recommend using built\-in table functions in ClickHouse which provide a better alternative for ad\-hoc querying scenarios (Postgres, MySQL, MongoDB, etc).


JDBC table function returns table that is connected via JDBC driver.


This table function requires separate [clickhouse\-jdbc\-bridge](https://github.com/ClickHouse/clickhouse-jdbc-bridge) program to be running.
It supports Nullable types (based on DDL of remote table that is queried).


## Syntax[​](#syntax "Direct link to Syntax")



```
jdbc(datasource, external_database, external_table)
jdbc(datasource, external_table)
jdbc(named_collection)

```

## Examples[​](#examples "Direct link to Examples")


Instead of an external database name, a schema can be specified:



```
SELECT * FROM jdbc('jdbc:mysql://localhost:3306/?user=root&password=root', 'schema', 'table')

```


```
SELECT * FROM jdbc('mysql://localhost:3306/?user=root&password=root', 'select * from schema.table')

```


```
SELECT * FROM jdbc('mysql-dev?p1=233', 'num Int32', 'select toInt32OrZero(''{{p1}}'') as num')

```


```
SELECT *
FROM jdbc('mysql-dev?p1=233', 'num Int32', 'select toInt32OrZero(''{{p1}}'') as num')

```


```
SELECT a.datasource AS server1, b.datasource AS server2, b.name AS db
FROM jdbc('mysql-dev?datasource_column', 'show databases') a
INNER JOIN jdbc('self?datasource_column', 'show databases') b ON a.Database = b.name

```
[Previousinput](/docs/sql-reference/table-functions/input)[Nextmerge](/docs/sql-reference/table-functions/merge)- [Syntax](#syntax)- [Examples](#examples)
Was this page helpful?
