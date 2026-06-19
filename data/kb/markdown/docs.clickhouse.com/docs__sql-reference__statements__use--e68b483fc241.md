# USE Statement \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- USE
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/use.md)# USE Statement


```
USE [DATABASE] db

```

Lets you set the current database for the session.


The current database is used for searching for tables if the database is not explicitly defined in the query with a dot before the table name.


This query can't be made when using the HTTP protocol, since there is no concept of a session.

[PreviousPARALLEL WITH](/docs/sql-reference/statements/parallel_with)[NextWATCH](/docs/sql-reference/statements/watch)Was this page helpful?
