# loop \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- loop
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/loop.md)# loop

## Syntax[​](#syntax "Direct link to Syntax")



```
SELECT ... FROM loop(database, table);
SELECT ... FROM loop(database.table);
SELECT ... FROM loop(table);
SELECT ... FROM loop(other_table_function(...));

```

## Arguments[​](#arguments "Direct link to Arguments")




| Argument Description| `database` database name.| `table` table name.| `other_table_function(...)` other table function. Example: `SELECT * FROM loop(numbers(10));` `other_table_function(...)` here is `numbers(10)`. | | | | | | | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- |


## Returned values[​](#returned_values "Direct link to Returned values")


Infinite loop to return query results.


## Examples[​](#examples "Direct link to Examples")


Selecting data from ClickHouse:



```
SELECT * FROM loop(test_database, test_table);
SELECT * FROM loop(test_database.test_table);
SELECT * FROM loop(test_table);

```

Or using other table functions:



```
SELECT * FROM loop(numbers(3)) LIMIT 7;
   ┌─number─┐
1. │      0 │
2. │      1 │
3. │      2 │
   └────────┘
   ┌─number─┐
4. │      0 │
5. │      1 │
6. │      2 │
   └────────┘
   ┌─number─┐
7. │      0 │
   └────────┘

```


```
SELECT * FROM loop(mysql('localhost:3306', 'test', 'test', 'user', 'password'));
...

```
[Previousview](/docs/sql-reference/table-functions/view)[NextWindow Functions](/docs/sql-reference/window-functions)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned values](#returned_values)- [Examples](#examples)
Was this page helpful?
