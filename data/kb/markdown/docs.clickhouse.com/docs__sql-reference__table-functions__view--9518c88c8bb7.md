# view \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- view
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/view.md)# view

Turns a subquery into a table. The function implements views (see [CREATE VIEW](/docs/sql-reference/statements/create/view)). The resulting table does not store data, but only stores the specified `SELECT` query. When reading from the table, ClickHouse executes the query and deletes all unnecessary columns from the result.


## Syntax[​](#syntax "Direct link to Syntax")



```
view(subquery)

```

## Arguments[​](#arguments "Direct link to Arguments")


- `subquery` — `SELECT` query.


## Returned value[​](#returned_value "Direct link to Returned value")


- A table.


## Examples[​](#examples "Direct link to Examples")


Input table:



```
┌─id─┬─name─────┬─days─┐
│  1 │ January  │   31 │
│  2 │ February │   29 │
│  3 │ March    │   31 │
│  4 │ April    │   30 │
└────┴──────────┴──────┘

```


```
SELECT * FROM view(SELECT name FROM months);

```


```
┌─name─────┐
│ January  │
│ February │
│ March    │
│ April    │
└──────────┘

```

You can use the `view` function as a parameter of the [remote](/docs/sql-reference/table-functions/remote) and [cluster](/docs/sql-reference/table-functions/cluster) table functions:



```
SELECT * FROM remote(`127.0.0.1`, view(SELECT a, b, c FROM table_name));

```


```
SELECT * FROM cluster(`cluster_name`, view(SELECT a, b, c FROM table_name));

```

## Related[​](#related "Direct link to Related")


- [View Table Engine](/docs/engines/table-engines/special/view)
[Previousvalues](/docs/sql-reference/table-functions/values)[Nextloop](/docs/sql-reference/table-functions/loop)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned_value)- [Examples](#examples)- [Related](#related)
Was this page helpful?
