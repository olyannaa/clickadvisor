# largestTriangleThreeBuckets \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- largestTriangleThreeBuckets
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/largestTriangleThreeBuckets.md)# largestTriangleThreeBuckets

## largestTriangleThreeBuckets[​](#largestTriangleThreeBuckets "Direct link to largestTriangleThreeBuckets")


Introduced in: v23\.10\.0


Applies the [Largest\-Triangle\-Three\-Buckets](https://skemman.is/bitstream/1946/15343/3/SS_MSthesis.pdf) algorithm to the input data.
The algorithm is used for downsampling time series data for visualization.
It is designed to operate on series sorted by x coordinate.
It works by dividing the sorted series into buckets and then finding the largest triangle in each bucket.
The number of buckets is equal to the number of points in the resulting series.
The function will sort data by `x` and then apply the downsampling algorithm to the sorted data.


NaNs are ignored in the provided series, meaning that any NaN values will be excluded from the analysis.
This ensures that the function operates only on valid numerical data.


**Syntax**



```
largestTriangleThreeBuckets(n)(x, y)

```

**Aliases**: `lttb`


**Parameters**


- `n` — Number of points in the resulting series. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Arguments**


- `x` — x coordinate. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal) or [`Date`](/docs/sql-reference/data-types/date) or [`Date32`](/docs/sql-reference/data-types/date32) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`DateTime64`](/docs/sql-reference/data-types/datetime64)
- `y` — y coordinate. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal) or [`Date`](/docs/sql-reference/data-types/date) or [`Date32`](/docs/sql-reference/data-types/date32) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Returned value**


Returns an array of tuples with two elements.. [`Array(Tuple(Float64, Float64))`](/docs/sql-reference/data-types/array)


**Examples**


**Downsampling time series data**



```
CREATE TABLE largestTriangleThreeBuckets_test (x Float64, y Float64) ENGINE = Memory;
INSERT INTO largestTriangleThreeBuckets_test VALUES
    (1.0, 10.0), (2.0, 20.0), (3.0, 15.0), (8.0, 60.0), (9.0, 55.0),
    (10.0, 70.0), (4.0, 30.0), (5.0, 40.0), (6.0, 35.0), (7.0, 50.0);

SELECT largestTriangleThreeBuckets(4)(x, y) FROM largestTriangleThreeBuckets_test;

```


```
┌────────largestTriangleThreeBuckets(4)(x, y)───────────┐
│           [(1,10),(3,15),(9,55),(10,70)]              │
└───────────────────────────────────────────────────────┘

```
[PreviouskurtSamp](/docs/sql-reference/aggregate-functions/reference/kurtsamp)[Nextlast\_value](/docs/sql-reference/aggregate-functions/reference/last_value)- [largestTriangleThreeBuckets](#largestTriangleThreeBuckets)
Was this page helpful?
