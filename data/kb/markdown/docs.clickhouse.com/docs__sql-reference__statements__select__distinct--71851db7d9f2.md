# DISTINCT Clause \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [SELECT](/docs/sql-reference/statements/select)- DISTINCT
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/select/distinct.md)# DISTINCT Clause

If `SELECT DISTINCT` is specified, only unique rows will remain in a query result. Thus, only a single row will remain out of all the sets of fully matching rows in the result.


You can specify the list of columns that must have unique values: `SELECT DISTINCT ON (column1, column2,...)`. If the columns are not specified, all of them are taken into consideration.


Consider the table:



```
┌─a─┬─b─┬─c─┐
│ 1 │ 1 │ 1 │
│ 1 │ 1 │ 1 │
│ 2 │ 2 │ 2 │
│ 2 │ 2 │ 2 │
│ 1 │ 1 │ 2 │
│ 1 │ 2 │ 2 │
└───┴───┴───┘

```

Using `DISTINCT` without specifying columns:



```
SELECT DISTINCT * FROM t1;

```


```
┌─a─┬─b─┬─c─┐
│ 1 │ 1 │ 1 │
│ 2 │ 2 │ 2 │
│ 1 │ 1 │ 2 │
│ 1 │ 2 │ 2 │
└───┴───┴───┘

```

Using `DISTINCT` with specified columns:



```
SELECT DISTINCT ON (a,b) * FROM t1;

```


```
┌─a─┬─b─┬─c─┐
│ 1 │ 1 │ 1 │
│ 2 │ 2 │ 2 │
│ 1 │ 2 │ 2 │
└───┴───┴───┘

```

## DISTINCT and ORDER BY[​](#distinct-and-order-by "Direct link to DISTINCT and ORDER BY")


ClickHouse supports using the `DISTINCT` and `ORDER BY` clauses for different columns in one query. The `DISTINCT` clause is executed before the `ORDER BY` clause.


Consider the table:



```
┌─a─┬─b─┐
│ 2 │ 1 │
│ 1 │ 2 │
│ 3 │ 3 │
│ 2 │ 4 │
└───┴───┘

```

Selecting data:



```
SELECT DISTINCT a FROM t1 ORDER BY b ASC;

```


```
┌─a─┐
│ 2 │
│ 1 │
│ 3 │
└───┘

```

Selecting data with the different sorting direction:



```
SELECT DISTINCT a FROM t1 ORDER BY b DESC;

```


```
┌─a─┐
│ 3 │
│ 1 │
│ 2 │
└───┘

```

Row `2, 4` was cut before sorting.


Take this implementation specificity into account when programming queries.


## Null Processing[​](#null-processing "Direct link to Null Processing")


`DISTINCT` works with [NULL](/docs/sql-reference/syntax#null) as if `NULL` were a specific value, and `NULL==NULL`. In other words, in the `DISTINCT` results, different combinations with `NULL` occur only once. It differs from `NULL` processing in most other contexts.


## Alternatives[​](#alternatives "Direct link to Alternatives")


It is possible to obtain the same result by applying [GROUP BY](/docs/sql-reference/statements/select/group-by) across the same set of values as specified as `SELECT` clause, without using any aggregate functions. But there are few differences from `GROUP BY` approach:


- `DISTINCT` can be applied together with `GROUP BY`.
- When [ORDER BY](/docs/sql-reference/statements/select/order-by) is omitted and [LIMIT](/docs/sql-reference/statements/select/limit) is defined, the query stops running immediately after the required number of different rows has been read.
- Data blocks are output as they are processed, without waiting for the entire query to finish running.
[PreviousARRAY JOIN](/docs/sql-reference/statements/select/array-join)[NextEXCEPT](/docs/sql-reference/statements/select/except)- [DISTINCT and ORDER BY](#distinct-and-order-by)- [Null Processing](#null-processing)- [Alternatives](#alternatives)
Was this page helpful?
