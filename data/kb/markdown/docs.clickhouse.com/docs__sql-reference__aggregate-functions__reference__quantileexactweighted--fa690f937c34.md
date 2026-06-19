# quantileExactWeighted \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- quantileExactWeighted
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/quantileExactWeighted.md)# quantileExactWeighted

## quantileExactWeighted[​](#quantileExactWeighted "Direct link to quantileExactWeighted")


Introduced in: v1\.1\.0


Exactly computes the [quantile](https://en.wikipedia.org/wiki/Quantile) of a numeric data sequence, taking into account the weight of each element.


To get the exact value, all the passed values are combined into an array, which is then partially sorted.
Each value is counted with its weight, as if it is present `weight` times.
A hash table is used in the algorithm.
Because of this, if the passed values are frequently repeated, the function consumes less RAM than [`quantileExact`](/docs/sql-reference/aggregate-functions/reference/quantileexact#quantileExact).
You can use this function instead of `quantileExact` and specify the weight 1\.


When using multiple `quantile*` functions with different levels in a query, the internal states are not combined (that is, the query works less efficiently than it could).
In this case, use the [quantiles](/docs/sql-reference/aggregate-functions/reference/quantiles#quantiles) function.


**Syntax**



```
quantileExactWeighted(level)(expr, weight)

```

**Aliases**: `medianExactWeighted`


**Parameters**


- `level` — Optional. Level of quantile. Constant floating\-point number from 0 to 1\. We recommend using a `level` value in the range of `[0.01, 0.99]`. Default value: 0\.5\. At `level=0.5` the function calculates median. [`Float*`](/docs/sql-reference/data-types/float)


**Arguments**


- `expr` — Expression over the column values resulting in numeric data types, Date or DateTime. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)
- `weight` — Column with weights of sequence members. Weight is a number of value occurrences. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Quantile of the specified level. [`Float64`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Computing exact weighted quantile**



```
CREATE TABLE t (
    n Int32,
    val Int32
) ENGINE = Memory;

-- Insert the sample data
INSERT INTO t VALUES
(0, 3),
(1, 2),
(2, 1),
(5, 4);

SELECT quantileExactWeighted(n, val) FROM t;

```


```
┌─quantileExactWeighted(n, val)─┐
│                             1 │
└───────────────────────────────┘

```

**See Also**


- [median](/docs/sql-reference/aggregate-functions/reference/median)
- [quantiles](/docs/sql-reference/aggregate-functions/reference/quantiles)
[PreviousquantileExactLow](/docs/sql-reference/aggregate-functions/reference/quantileExactLow)[NextquantileExactWeightedInterpolated](/docs/sql-reference/aggregate-functions/reference/quantileExactWeightedInterpolated)- [quantileExactWeighted](#quantileExactWeighted)
Was this page helpful?
