# kurtSamp \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- kurtSamp
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/kurtSamp.md)# kurtSamp

## kurtSamp[​](#kurtSamp "Direct link to kurtSamp")


Introduced in: v20\.1\.0


Computes the [sample kurtosis](https://en.wikipedia.org/wiki/Kurtosis) of a sequence.


It represents an unbiased estimate of the kurtosis of a random variable if passed values form its sample.


**Syntax**



```
kurtSamp(expr)

```

**Arguments**


- `expr` — [Expression](/docs/sql-reference/syntax#expressions) returning a number. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the kurtosis of the given distribution. If `n <= 1` (`n` is a size of the sample), then the function returns `nan`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Computing sample kurtosis**



```
CREATE TABLE test_data (x Float64) ENGINE = Memory;
INSERT INTO test_data VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

SELECT kurtSamp(x) FROM test_data;

```


```
┌────────kurtSamp(x)─┐
│ 1.4383636363636365 │
└────────────────────┘

```
[PreviouskurtPop](/docs/sql-reference/aggregate-functions/reference/kurtpop)[NextlargestTriangleThreeBuckets](/docs/sql-reference/aggregate-functions/reference/largestTriangleThreeBuckets)- [kurtSamp](#kurtSamp)
Was this page helpful?
