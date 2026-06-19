# avg \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- avg
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/avg.md)# avg

## avg[​](#avg "Direct link to avg")


Introduced in: v1\.1\.0


Calculates the arithmetic mean.


**Syntax**



```
avg(x)

```

**Arguments**


- `x` — Input values. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the arithmetic mean, otherwise returns `NaN` if the input parameter `x` is empty. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
SELECT avg(x) FROM VALUES('x Int8', 0, 1, 2, 3, 4, 5);

```


```
┌─avg(x)─┐
│    2.5 │
└────────┘

```

**Empty table returns NaN**



```
CREATE TABLE test (t UInt8) ENGINE = Memory;

SELECT avg(t) FROM test;

```


```
┌─avg(x)─┐
│    nan │
└────────┘

```
[PreviousargMin](/docs/sql-reference/aggregate-functions/reference/argmin)[NextavgWeighted](/docs/sql-reference/aggregate-functions/reference/avgweighted)- [avg](#avg)
Was this page helpful?
