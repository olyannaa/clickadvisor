---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/quantilesExactInclusive.md)#
topic: quantilesexactinclusive-clickhouse-docs
ch_version_introduced: '0.01'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 1
---

# quantilesExactInclusive \| ClickHouse Docs

- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- quantilesExactInclusive
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/quantilesExactInclusive.md)# quantilesExactInclusive

## quantilesExactInclusive[​](#quantilesExactInclusive "Direct link to quantilesExactInclusive")

Introduced in: v20\.1\.0

Exactly computes multiple [quantiles](https://en.wikipedia.org/wiki/Quantile) of a numeric data sequence at different levels simultaneously using the inclusive method.

This function is equivalent to [`quantileExactInclusive`](/docs/sql-reference/aggregate-functions/reference/quantileExactInclusive) but allows computing multiple quantile levels in a single pass, which is more efficient than calling individual quantile functions.

This function uses the inclusive method for calculating quantiles, as described in the [R\-7 method](https://en.wikipedia.org/wiki/Quantile#Estimating_quantiles_from_a_sample).
This is equivalent to [PERCENTILE.INC](https://support.microsoft.com/en-us/office/percentile-inc-function-680f9539-45eb-410b-9a5e-c1355e5fe2ed) Excel function.

To get exact values, all the passed values are combined into an array, which is then partially sorted.
The sorting algorithm's complexity is `O(N·log(N))`, where `N = std::distance(first, last)` comparisons.

**Syntax**

```
quantilesExactInclusive(level1, level2, ...)(expr)

```

**Parameters**

- `level` — Levels of quantiles. Constant floating\-point numbers from 0 to 1 (inclusive). We recommend using `level` values in the range of `[0.01, 0.99]`. [`Float*`](/docs/sql-reference/data-types/float)

**Arguments**

- `expr` — Expression over the column values resulting in numeric data types, Date or DateTime. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)

**Returned value**

Array of quantiles of the specified levels in the same order as the levels were specified. [`Array(Float64)`](/docs/sql-reference/data-types/array)

**Examples**

**Computing multiple exact inclusive quantiles**

```
CREATE TABLE num AS numbers(1000);
SELECT quantilesExactInclusive(0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 0.999)(number) FROM num;

```

```
┌─quantilesExactInclusive(0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 0.999)(number)─┐
│ [249.75,499.5,749.25,899.1,949.05,989.01,998.001]                        │
└──────────────────────────────────────────────────────────────────────────┘

```
[PreviousquantilesExactExclusive](/docs/sql-reference/aggregate-functions/reference/quantilesExactExclusive)[NextquantilesGK](/docs/sql-reference/aggregate-functions/reference/quantilesGK)- [quantilesExactInclusive](#quantilesExactInclusive)
Was this page helpful?
