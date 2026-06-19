# avgWeighted \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- avgWeighted
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/avgWeighted.md)# avgWeighted

## avgWeighted[​](#avgWeighted "Direct link to avgWeighted")


Introduced in: v20\.1\.0


Calculates the [weighted arithmetic mean](https://en.wikipedia.org/wiki/Weighted_arithmetic_mean).


**Syntax**



```
avgWeighted(x, weight)

```

**Arguments**


- `x` — Values. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `weight` — Weights of the values. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns `NaN` if all the weights are equal to 0 or the supplied weights parameter is empty, or the weighted mean otherwise. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT avgWeighted(x, w)
FROM VALUES('x Int8, w Int8', (4, 1), (1, 0), (10, 2))

```


```
┌─avgWeighted(x, w)─┐
│                 8 │
└───────────────────┘

```

**Mixed integer and float weights**



```
SELECT avgWeighted(x, w)
FROM VALUES('x Int8, w Float64', (4, 1), (1, 0), (10, 2))

```


```
┌─avgWeighted(x, w)─┐
│                 8 │
└───────────────────┘

```

**All weights are zero returns NaN**



```
SELECT avgWeighted(x, w)
FROM VALUES('x Int8, w Int8', (0, 0), (1, 0), (10, 0))

```


```
┌─avgWeighted(x, w)─┐
│               nan │
└───────────────────┘

```

**Empty table returns NaN**



```
CREATE TABLE test (t UInt8) ENGINE = Memory;
SELECT avgWeighted(t, t) FROM test

```


```
┌─avgWeighted(t, t)─┐
│               nan │
└───────────────────┘

```
[Previousavg](/docs/sql-reference/aggregate-functions/reference/avg)[NextboundingRatio](/docs/sql-reference/aggregate-functions/reference/boundingRatio)- [avgWeighted](#avgWeighted)
Was this page helpful?
