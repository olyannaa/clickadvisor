# zeros \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- zeros
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/zeros.md)# zeros

- `zeros(N)` – Returns a table with the single 'zero' column (UInt8\) that contains the integer 0 `N` times
- `zeros_mt(N)` – The same as `zeros`, but uses multiple threads.


This function is used for test purposes as the fastest method to generate many rows. Similar to the `system.zeros` and `system.zeros_mt` system tables.


The following queries are equivalent:



```
SELECT * FROM zeros(10);
SELECT * FROM system.zeros LIMIT 10;
SELECT * FROM zeros_mt(10);
SELECT * FROM system.zeros_mt LIMIT 10;

```


```
┌─zero─┐
│    0 │
│    0 │
│    0 │
│    0 │
│    0 │
│    0 │
│    0 │
│    0 │
│    0 │
│    0 │
└──────┘

```
[PrevioustimeSeriesTags](/docs/sql-reference/table-functions/timeSeriesTags)[Nextgenerate\_series](/docs/sql-reference/table-functions/generate_series)Was this page helpful?
