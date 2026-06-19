# quantilePrometheusHistogram \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- quantilePrometheusHistogram
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/quantilePrometheusHistogram.md)# quantilePrometheusHistogram

## quantilePrometheusHistogram[​](#quantilePrometheusHistogram "Direct link to quantilePrometheusHistogram")


Introduced in: v25\.10\.0


Computes [quantile](https://en.wikipedia.org/wiki/Quantile) of a histogram using linear interpolation, taking into account the cumulative value and upper bounds of each histogram bucket.


To get the interpolated value, all the passed values are combined into an array, which are then sorted by their corresponding bucket upper bound values.
Quantile interpolation is then performed similarly to the PromQL [histogram\_quantile()](https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile) function on a classic histogram, performing a linear interpolation using the lower and upper bound of the bucket in which the quantile position is found.


**See Also**


- [median](/docs/sql-reference/aggregate-functions/reference/median)
- [quantiles](/docs/sql-reference/aggregate-functions/reference/quantiles)


**Syntax**



```
quantilePrometheusHistogram(level)(bucket_upper_bound, cumulative_bucket_value)

```

**Parameters**


- `level` — Optional. Level of quantile. Constant floating\-point number from 0 to 1\. We recommend using a `level` value in the range of `[0.01, 0.99]`. Default value: `0.5`. At `level=0.5` the function calculates [median](https://en.wikipedia.org/wiki/Median). [`Float64`](/docs/sql-reference/data-types/float)


**Arguments**


- `bucket_upper_bound` — Upper bounds of the histogram buckets. The highest bucket must have an upper bound of `+Inf`. [`Float64`](/docs/sql-reference/data-types/float)
- `cumulative_bucket_value` — Cumulative values of the histogram buckets. Values must be monotonically increasing as the bucket upper bound increases. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float64`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the quantile of the specified level. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT quantilePrometheusHistogram(bucket_upper_bound, cumulative_bucket_value)
FROM VALUES('bucket_upper_bound Float64, cumulative_bucket_value UInt64', (0, 6), (0.5, 11), (1, 14), (inf, 19));

```


```
┌─quantilePrometheusHistogram(bucket_upper_bound, cumulative_bucket_value)─┐
│                                                                     0.35 │
└──────────────────────────────────────────────────────────────────────────┘

```

**See Also**


- [median](/docs/sql-reference/aggregate-functions/reference/median)
- [quantiles](/docs/sql-reference/aggregate-functions/reference/quantiles)
[PreviousquantileInterpolatedWeighted](/docs/sql-reference/aggregate-functions/reference/quantileInterpolatedWeighted)[NextquantileTDigest](/docs/sql-reference/aggregate-functions/reference/quantiletdigest)- [quantilePrometheusHistogram](#quantilePrometheusHistogram)
Was this page helpful?
