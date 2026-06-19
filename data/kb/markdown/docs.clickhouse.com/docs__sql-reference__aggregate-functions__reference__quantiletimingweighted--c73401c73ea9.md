# quantileTimingWeighted \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- quantileTimingWeighted
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/quantileTimingWeighted.md)# quantileTimingWeighted

## quantileTimingWeighted[​](#quantileTimingWeighted "Direct link to quantileTimingWeighted")


Introduced in: v1\.1\.0


With the determined precision computes the [quantile](https://en.wikipedia.org/wiki/Quantile) of a numeric data sequence according to the weight of each sequence member.


The result is deterministic (it does not depend on the query processing order). The function is optimized for working with sequences which describe distributions like loading web pages times or backend response times.


When using multiple `quantile*` functions with different levels in a query, the internal states are not combined (that is, the query works less efficiently than it could). In this case, use the [`quantiles`](/docs/sql-reference/aggregate-functions/reference/quantiles#quantiles) function.


**Accuracy**


The calculation is accurate if:


- Total number of values does not exceed 5670\.
- Total number of values exceeds 5670, but the page loading time is less than 1024ms.


Otherwise, the result of the calculation is rounded to the nearest multiple of 16 ms.


NoteFor calculating page loading time quantiles, this function is more effective and accurate than [`quantile`](/docs/sql-reference/aggregate-functions/reference/quantile).


NoteIf no values are passed to the function (when using `quantileTimingIf`), [NaN](/docs/sql-reference/data-types/float#nan-and-inf) is returned. The purpose of this is to differentiate these cases from cases that result in zero. See [ORDER BY clause](/docs/sql-reference/statements/select/order-by) for notes on sorting `NaN` values.


**Syntax**



```
quantileTimingWeighted(level)(expr, weight)

```

**Aliases**: `medianTimingWeighted`


**Parameters**


- `level` — Optional. Level of quantile. Constant floating\-point number from 0 to 1\. We recommend using a `level` value in the range of `[0.01, 0.99]`. Default value: 0\.5\. At `level=0.5` the function calculates median. [`Float*`](/docs/sql-reference/data-types/float)


**Arguments**


- `expr` — Expression over a column values returning a Float\*\-type number. If negative values are passed to the function, the behavior is undefined. If the value is greater than 30,000 (a page loading time of more than 30 seconds), it is assumed to be 30,000\. [`Float*`](/docs/sql-reference/data-types/float)
- `weight` — Column with weights of sequence elements. Weight is a number of value occurrences. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Quantile of the specified level. [`Float32`](/docs/sql-reference/data-types/float)


**Examples**


**Computing weighted timing quantile**



```
CREATE TABLE t (response_time UInt32, weight UInt32) ENGINE = Memory;
INSERT INTO t VALUES (68, 1), (104, 2), (112, 3), (126, 2), (138, 1), (162, 1);

SELECT quantileTimingWeighted(response_time, weight) FROM t;

```


```
┌─quantileTimingWeighted(response_time, weight)─┐
│                                           112 │
└───────────────────────────────────────────────┘

```
[PreviousquantileTiming](/docs/sql-reference/aggregate-functions/reference/quantiletiming)[Nextquantiles Functions](/docs/sql-reference/aggregate-functions/reference/quantiles)- [quantileTimingWeighted](#quantileTimingWeighted)
Was this page helpful?
