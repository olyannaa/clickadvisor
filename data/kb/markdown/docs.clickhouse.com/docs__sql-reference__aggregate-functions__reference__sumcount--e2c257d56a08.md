# sumCount \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- sumCount
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/sumCount.md)# sumCount

## sumCount[​](#sumCount "Direct link to sumCount")


Introduced in: v21\.6\.0


Calculates the sum of the numbers and counts the number of rows at the same time. The function is used by ClickHouse query optimizer: if there are multiple `sum`, `count` or `avg` functions in a query, they can be replaced to single `sumCount` function to reuse the calculations. The function is rarely needed to use explicitly.


**See also**


- [`optimize_syntax_fuse_functions`](/docs/operations/settings/settings#optimize_syntax_fuse_functions) setting.


**Syntax**



```
sumCount(x)

```

**Arguments**


- `x` — Input value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns a tuple `(sum, count)`, where `sum` is the sum of numbers and `count` is the number of rows with not\-NULL values. [`Tuple`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
CREATE TABLE s_table (x Int8) ENGINE = Log;
INSERT INTO s_table SELECT number FROM numbers(0, 20);
INSERT INTO s_table VALUES (NULL);
SELECT sumCount(x) FROM s_table;

```


```
┌─sumCount(x)─┐
│ (190,20)    │
└─────────────┘

```

**See also**


- [optimize\_syntax\_fuse\_functions](/docs/operations/settings/settings#optimize_syntax_fuse_functions) setting.
[Previoussum](/docs/sql-reference/aggregate-functions/reference/sum)[NextsumKahan](/docs/sql-reference/aggregate-functions/reference/sumkahan)- [sumCount](#sumCount)
Was this page helpful?
