# RENAME Statement \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- RENAME
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/rename.md)# RENAME Statement

Renames databases, tables, or dictionaries. Several entities can be renamed in a single query.
Note that the `RENAME` query with several entities is non\-atomic operation. To swap entities names atomically, use the [EXCHANGE](/docs/sql-reference/statements/exchange) statement.


**Syntax**



```
RENAME [DATABASE|TABLE|DICTIONARY] name TO new_name [,...] [ON CLUSTER cluster]

```

## RENAME DATABASE[​](#rename-database "Direct link to RENAME DATABASE")


Renames databases.


**Syntax**



```
RENAME DATABASE atomic_database1 TO atomic_database2 [,...] [ON CLUSTER cluster]

```

## RENAME TABLE[​](#rename-table "Direct link to RENAME TABLE")


Renames one or more tables.


Renaming tables is a light operation. If you pass a different database after `TO`, the table will be moved to this database. However, the directories with databases must reside in the same file system. Otherwise, an error is returned.
If you rename multiple tables in one query, the operation is not atomic. It may be partially executed, and queries in other sessions may get `Table ... does not exist ...` error.


**Syntax**



```
RENAME TABLE [db1.]name1 TO [db2.]name2 [,...] [ON CLUSTER cluster]

```

**Example**



```
RENAME TABLE table_A TO table_A_bak, table_B TO table_B_bak;

```

And you can use a simpler sql:



```
RENAME table_A TO table_A_bak, table_B TO table_B_bak;

```

## RENAME DICTIONARY[​](#rename-dictionary "Direct link to RENAME DICTIONARY")


Renames one or several dictionaries. This query can be used to move dictionaries between databases.


**Syntax**



```
RENAME DICTIONARY [db0.]dict_A TO [db1.]dict_B [,...] [ON CLUSTER cluster]

```

**See Also**


- [Dictionaries](/docs/sql-reference/statements/create/dictionary)
[PreviousOPTIMIZE](/docs/sql-reference/statements/optimize)[NextEXCHANGE](/docs/sql-reference/statements/exchange)- [RENAME DATABASE](#rename-database)- [RENAME TABLE](#rename-table)- [RENAME DICTIONARY](#rename-dictionary)
Was this page helpful?
