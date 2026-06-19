# generate\_series (generateSeries) \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- generate\_series
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/generate_series.md)# generate\_series (generateSeries)

Alias: `generateSeries`


## Syntax[​](#syntax "Direct link to Syntax")


Returns a table with the single 'generate\_series' column (`UInt64`) that contains integers from start to stop inclusively:



```
generate_series(START, STOP)

```

Returns a table with the single 'generate\_series' column (`UInt64`) that contains integers from start to stop inclusively with spacing between values given by `STEP`:



```
generate_series(START, STOP, STEP)

```

`STEP` can be negative, in which case the series is generated in descending order from `START` down to `STOP`. If `STEP` is negative and `START < STOP`, the result is empty.


## Examples[​](#examples "Direct link to Examples")


The following queries return tables with the same content but different column names:



```
SELECT * FROM numbers(10, 5);

```


```
┌─number─┐
│     10 │
│     11 │
│     12 │
│     13 │
│     14 │
└────────┘

```


```
SELECT * FROM generate_series(10, 14);

```


```
┌─generate_series─┐
│              10 │
│              11 │
│              12 │
│              13 │
│              14 │
└─────────────────┘

```

And the following queries return tables with the same content but different column names (but the second option is more efficient):



```
SELECT * FROM numbers(10, 11) WHERE number % 3 == (10 % 3);

```


```
┌─number─┐
│     10 │
│     13 │
│     16 │
│     19 │
└────────┘

```


```
SELECT * FROM generate_series(10, 20, 3);

```


```
┌─generate_series─┐
│              10 │
│              13 │
│              16 │
│              19 │
└─────────────────┘

```

Generate a descending series:



```
SELECT * FROM generate_series(9, 0, -1);

```


```
┌─generate_series─┐
│               9 │
│               8 │
│               7 │
│               6 │
│               5 │
│               4 │
│               3 │
│               2 │
│               1 │
│               0 │
└─────────────────┘

```
[Previouszeros](/docs/sql-reference/table-functions/zeros)[Nextodbc](/docs/sql-reference/table-functions/odbc)- [Syntax](#syntax)- [Examples](#examples)
Was this page helpful?
