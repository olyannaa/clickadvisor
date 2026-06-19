# last\_value \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- last\_value
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/last_value.md)# last\_value

Selects the last encountered value, similar to `anyLast`, but could accept NULL.
Mostly it should be used with [Window Functions](/docs/sql-reference/window-functions).
Without Window Functions the result will be random if the source stream is not ordered.


## examples[​](#examples "Direct link to examples")



```
CREATE TABLE test_data
(
    a Int64,
    b Nullable(Int64)
)
ENGINE = Memory;

INSERT INTO test_data (a, b) VALUES (1,null), (2,3), (4, 5), (6,null)

```

### Example 1[​](#example1 "Direct link to Example 1")


The NULL value is ignored at default.



```
SELECT last_value(b) FROM test_data

```


```
┌─last_value_ignore_nulls(b)─┐
│                          5 │
└────────────────────────────┘

```

### Example 2[​](#example2 "Direct link to Example 2")


The NULL value is ignored.



```
SELECT last_value(b) ignore nulls FROM test_data

```


```
┌─last_value_ignore_nulls(b)─┐
│                          5 │
└────────────────────────────┘

```

### Example 3[​](#example3 "Direct link to Example 3")


The NULL value is accepted.



```
SELECT last_value(b) respect nulls FROM test_data

```


```
┌─last_value_respect_nulls(b)─┐
│                        ᴺᵁᴸᴸ │
└─────────────────────────────┘

```

### Example 4[​](#example4 "Direct link to Example 4")


Stabilized result using the sub\-query with `ORDER BY`.



```
SELECT
    last_value_respect_nulls(b),
    last_value(b)
FROM
(
    SELECT *
    FROM test_data
    ORDER BY a ASC
)

```


```
┌─last_value_respect_nulls(b)─┬─last_value(b)─┐
│                        ᴺᵁᴸᴸ │             5 │
└─────────────────────────────┴───────────────┘

```
[PreviouslargestTriangleThreeBuckets](/docs/sql-reference/aggregate-functions/reference/largestTriangleThreeBuckets)[NextmannWhitneyUTest](/docs/sql-reference/aggregate-functions/reference/mannwhitneyutest)- [examples](#examples)
	- [Example 1](#example1)- [Example 2](#example2)- [Example 3](#example3)- [Example 4](#example4)
Was this page helpful?
