# quantile \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- quantile
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/quantile.md)# quantile

## quantile[​](#quantile "Direct link to quantile")


Introduced in: v1\.1\.0


Computes an approximate [`quantile`](https://en.wikipedia.org/wiki/Quantile) of a numeric data sequence.


This function applies [reservoir sampling](https://en.wikipedia.org/wiki/Reservoir_sampling) with a reservoir size up to 8192 and a random number generator for sampling.
The result is non\-deterministic.
To get an exact quantile, use the [`quantileExact`](/docs/sql-reference/aggregate-functions/reference/quantileexact#quantileExact) function.


When using multiple `quantile*` functions with different levels in a query, the internal states are not combined (that is, the query works less efficiently than it could).
In this case, use the [`quantiles`](/docs/sql-reference/aggregate-functions/reference/quantiles#quantiles) function.


Note that for an empty numeric sequence, `quantile` will return NaN, but its `quantile*` variants will return either NaN or a default value for the sequence type, depending on the variant.


**Syntax**



```
quantile(level)(expr)

```

**Aliases**: `median`


**Parameters**


- `level` — Optional. Level of quantile. Constant floating\-point number from 0 to 1\. We recommend using a `level` value in the range of `[0.01, 0.99]`. Default value: 0\.5\. At `level=0.5` the function calculates median. [`Float`](/docs/sql-reference/data-types/float)


**Arguments**


- `expr` — Expression over the column values resulting in numeric data types, Date or DateTime. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)


**Returned value**


Approximate quantile of the specified level. [`Float64`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Computing quantile**



```
CREATE TABLE t (val UInt32) ENGINE = Memory;
INSERT INTO t VALUES (1), (1), (2), (3);

SELECT quantile(val) FROM t;

```


```
┌─quantile(val)─┐
│           1.5 │
└───────────────┘

```

**See Also**


- [median](/docs/sql-reference/aggregate-functions/reference/median)
- [quantiles](/docs/sql-reference/aggregate-functions/reference/quantiles)
[PreviousminMap](/docs/sql-reference/aggregate-functions/reference/minmap)[NextquantileBFloat16](/docs/sql-reference/aggregate-functions/reference/quantilebfloat16)- [quantile](#quantile)
Was this page helpful?
