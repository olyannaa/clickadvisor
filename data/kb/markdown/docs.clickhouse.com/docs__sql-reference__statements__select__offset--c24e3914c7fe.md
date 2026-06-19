# OFFSET FETCH Clause \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [SELECT](/docs/sql-reference/statements/select)- OFFSET
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/select/offset.md)# OFFSET FETCH Clause

`OFFSET` and `FETCH` allow you to retrieve data by portions. They specify a row block which you want to get by a single query.



```
-- SQL Standard style:
[OFFSET offset_row_count {ROW | ROWS}] [FETCH {FIRST | NEXT} fetch_row_count {ROW | ROWS} {ONLY | WITH TIES}]

-- MySQL/PostgreSQL style:
[LIMIT [n, ]m] [OFFSET offset_row_count]

```

The `offset_row_count` or `fetch_row_count` value can be a number or a literal constant. You can omit `fetch_row_count`; by default, it equals to 1\.


`OFFSET` specifies the number of rows to skip before starting to return rows from the query result set. `OFFSET n` skips the first `n` rows from the result.


Negative OFFSET is supported: `OFFSET -n` skips the last `n` rows from the result.


Fractional OFFSET is also supported: `OFFSET n` \- if 0 \< n \< 1, then the first n \* 100% of the result is skipped.


Example:  

• `OFFSET 0.1` \- skips the first 10% of the result.



> **Note**  
> 
> • The fraction must be a [Float64](/docs/sql-reference/data-types/float) number less than 1 and greater than zero.  
> 
> • If a fractional number of rows results from the calculation, it is rounded up to the next whole number.


The `FETCH` specifies the maximum number of rows that can be in the result of a query.


The `ONLY` option is used to return rows that immediately follow the rows omitted by the `OFFSET`. In this case the `FETCH` is an alternative to the [LIMIT](/docs/sql-reference/statements/select/limit) clause. For example, the following query



```
SELECT * FROM test_fetch ORDER BY a OFFSET 1 ROW FETCH FIRST 3 ROWS ONLY;

```

is identical to the query



```
SELECT * FROM test_fetch ORDER BY a LIMIT 3 OFFSET 1;

```

The `WITH TIES` option is used to return any additional rows that tie for the last place in the result set according to the `ORDER BY` clause. For example, if `fetch_row_count` is set to 5 but two additional rows match the values of the `ORDER BY` columns in the fifth row, the result set will contain seven rows.


NoteAccording to the standard, the `OFFSET` clause must come before the `FETCH` clause if both are present.


NoteThe real offset can also depend on the [offset](/docs/operations/settings/settings#offset) setting.


## Examples[​](#examples "Direct link to Examples")


Input table:



```
┌─a─┬─b─┐
│ 1 │ 1 │
│ 2 │ 1 │
│ 3 │ 4 │
│ 1 │ 3 │
│ 5 │ 4 │
│ 0 │ 6 │
│ 5 │ 7 │
└───┴───┘

```

Usage of the `ONLY` option:



```
SELECT * FROM test_fetch ORDER BY a OFFSET 3 ROW FETCH FIRST 3 ROWS ONLY;

```


```
┌─a─┬─b─┐
│ 2 │ 1 │
│ 3 │ 4 │
│ 5 │ 4 │
└───┴───┘

```

Usage of the `WITH TIES` option:



```
SELECT * FROM test_fetch ORDER BY a OFFSET 3 ROW FETCH FIRST 3 ROWS WITH TIES;

```


```
┌─a─┬─b─┐
│ 2 │ 1 │
│ 3 │ 4 │
│ 5 │ 4 │
│ 5 │ 7 │
└───┴───┘

```
[PreviousLIMIT](/docs/sql-reference/statements/select/limit)[NextORDER BY](/docs/sql-reference/statements/select/order-by)- [Examples](#examples)
Was this page helpful?
