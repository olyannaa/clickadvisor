# quantilesTimingWeighted \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- quantilesTimingWeighted
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/quantilesTimingWeighted.md)# quantilesTimingWeighted

## quantilesTimingWeighted[​](#quantilesTimingWeighted "Direct link to quantilesTimingWeighted")


Introduced in: v1\.1\.0


Computes multiple [quantiles](https://en.wikipedia.org/wiki/Quantile) of a numeric data sequence at different levels simultaneously with determined precision, taking into account the weight of each sequence member.


This function is equivalent to [`quantileTimingWeighted`](/docs/sql-reference/aggregate-functions/reference/quantiletimingweighted) but allows computing multiple quantile levels in a single pass, which is more efficient than calling individual quantile functions.


The result is deterministic (it does not depend on the query processing order). The function is optimized for working with sequences which describe distributions like loading web pages times or backend response times.


**Accuracy**


The calculation is accurate if:


- Total number of values does not exceed 5670\.
- Total number of values exceeds 5670, but the page loading time is less than 1024ms.


Otherwise, the result of the calculation is rounded to the nearest multiple of 16 ms.


NoteFor calculating page loading time quantiles, this function is more effective and accurate than [`quantiles`](/docs/sql-reference/aggregate-functions/reference/quantiles).


**Syntax**



```
quantilesTimingWeighted(level1, level2, ...)(expr, weight)

```

**Parameters**


- `level` — Levels of quantiles. One or more constant floating\-point numbers from 0 to 1\. We recommend using `level` values in the range of `[0.01, 0.99]`. [`Float*`](/docs/sql-reference/data-types/float)


**Arguments**


- `expr` — Expression over a column values returning a Float\*\-type number. If negative values are passed to the function, the behavior is undefined. If the value is greater than 30,000 (a page loading time of more than 30 seconds), it is assumed to be 30,000\. [`Float*`](/docs/sql-reference/data-types/float)
- `weight` — Column with weights of sequence elements. Weight is a number of value occurrences. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Array of quantiles of the specified levels in the same order as the levels were specified. [`Array(Float32)`](/docs/sql-reference/data-types/array)


**Examples**


**Computing multiple weighted timing quantiles**



```
SELECT quantilesTimingWeighted(0.5, 0.99)(response_time, weight) FROM t;

```


```
┌─quantilesTimingWeighted(0.5, 0.99)(response_time, weight)─┐
│ [112, 162]                                                │
└───────────────────────────────────────────────────────────┘

```

**See Also**


- [median](/docs/sql-reference/aggregate-functions/reference/median)
- [quantiles](/docs/sql-reference/aggregate-functions/reference/quantiles)
[PreviousquantilesGK](/docs/sql-reference/aggregate-functions/reference/quantilesGK)[NextrankCorr](/docs/sql-reference/aggregate-functions/reference/rankCorr)- [quantilesTimingWeighted](#quantilesTimingWeighted)
Was this page helpful?
