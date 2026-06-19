# quantileExactHigh \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- quantileExactHigh
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/quantileExactHigh.md)# quantileExactHigh

## quantileExactHigh[​](#quantileExactHigh "Direct link to quantileExactHigh")


Introduced in: v20\.8\.0


Similar to [`quantileExact`](/docs/sql-reference/aggregate-functions/reference/quantileexact), this computes the exact [quantile](https://en.wikipedia.org/wiki/Quantile) of a numeric data sequence.


To get the exact value, all the passed values are combined into an array, which is then fully sorted.
The sorting algorithm's complexity is `O(N·log(N))`, where `N = std::distance(first, last)` comparisons.


The return value depends on the quantile level and the number of elements in the selection, i.e. if the level is 0\.5, then the function returns the higher median value for an even number of elements and the middle median value for an odd number of elements.
Median is calculated similarly to the [`median_high`](https://docs.python.org/3/library/statistics.html#statistics.median_high) implementation which is used in python.


For all other levels, the element at the index corresponding to the value of `level * size_of_array` is returned.


When using multiple `quantile*` functions with different levels in a query, the internal states are not combined (that is, the query works less efficiently than it could).
In this case, use the [quantiles](/docs/sql-reference/aggregate-functions/reference/quantiles) function.


**Syntax**



```
quantileExactHigh(level)(expr)

```

**Aliases**: `medianExactHigh`


**Parameters**


- `level` — Optional. Level of quantile. Constant floating\-point number from 0 to 1\. We recommend using a `level` value in the range of `[0.01, 0.99]`. Default value: 0\.5\. At `level=0.5` the function calculates median. [`Float*`](/docs/sql-reference/data-types/float)


**Arguments**


- `expr` — Expression over the column values resulting in numeric data types, Date or DateTime. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)


**Returned value**


Returns the quantile of the specified level. [`Float64`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Computing exact high quantile**



```
SELECT quantileExactHigh(number) FROM numbers(10);

```


```
┌─quantileExactHigh(number)─┐
│                         5 │
└───────────────────────────┘

```

**Computing specific quantile level**



```
SELECT quantileExactHigh(0.1)(number) FROM numbers(10);

```


```
┌─quantileExactHigh(0.1)(number)─┐
│                              1 │
└────────────────────────────────┘

```
[PreviousquantileExactExclusive](/docs/sql-reference/aggregate-functions/reference/quantileExactExclusive)[NextquantileExactInclusive](/docs/sql-reference/aggregate-functions/reference/quantileExactInclusive)- [quantileExactHigh](#quantileExactHigh)
Was this page helpful?
