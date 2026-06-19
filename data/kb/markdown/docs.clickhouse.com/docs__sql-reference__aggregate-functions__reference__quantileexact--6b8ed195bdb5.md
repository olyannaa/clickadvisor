# quantileExact Functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- quantileExact Functions
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/quantileExact.md)# quantileExact Functions

## quantileExact[​](#quantileExact "Direct link to quantileExact")


Introduced in: v1\.1\.0


Exactly computes the [quantile](https://en.wikipedia.org/wiki/Quantile) of a numeric data sequence.


To get exact value, all the passed values are combined into an array, which is then partially sorted.
Therefore, the function consumes `O(n)` memory, where `n` is a number of values that were passed.
However, for a small number of values, the function is very effective.


When using multiple `quantile*` functions with different levels in a query, the internal states are not combined (that is, the query works less efficiently than it could).
In this case, use the [`quantiles`](/docs/sql-reference/aggregate-functions/reference/quantiles#quantiles) function.


**Syntax**



```
quantileExact(level)(expr)

```

**Aliases**: `medianExact`


**Parameters**


- `level` — Optional. Level of quantile. Constant floating\-point number from 0 to 1\. We recommend using a `level` value in the range of `[0.01, 0.99]`. Default value: 0\.5\. At `level=0.5` the function calculates median. [`Float*`](/docs/sql-reference/data-types/float)


**Arguments**


- `expr` — Expression over the column values resulting in numeric data types, Date or DateTime. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)


**Returned value**


Quantile of the specified level. For numeric data types the output format will be the same as the input format. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Computing exact quantile**



```
SELECT quantileExact(number) FROM numbers(10);

```


```
┌─quantileExact(number)─┐
│                     5 │
└───────────────────────┘

```

**See Also**


- [median](/docs/sql-reference/aggregate-functions/reference/median)
- [quantiles](/docs/sql-reference/aggregate-functions/reference/quantiles)
[PreviousquantileDeterministic](/docs/sql-reference/aggregate-functions/reference/quantiledeterministic)[NextquantileExactExclusive](/docs/sql-reference/aggregate-functions/reference/quantileExactExclusive)- [quantileExact](#quantileExact)
Was this page helpful?
