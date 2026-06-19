# covarSampStable \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- covarSampStable
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/covarSampStable.md)# covarSampStable

## covarSampStable[​](#covarSampStable "Direct link to covarSampStable")


Introduced in: v1\.1\.0


Calculates the sample covariance:


Σ(x−xˉ)(y−yˉ)n−1\\frac{\\Sigma{(x \- \\bar{x})(y \- \\bar{y})}}{n \- 1}n−1Σ(x−xˉ)(y−yˉ​)​
  

It is similar to [`covarSamp`](/docs/sql-reference/aggregate-functions/reference/covarsamp) but uses a numerically stable algorithm.
As a result, `covarSampStable` is slower than `covarSamp` but provides a lower computational error.


**Syntax**



```
covarSampStable(x, y)

```

**Arguments**


- `x` — First variable. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `y` — Second variable. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the sample covariance between `x` and `y`. For `n <= 1`, `inf` is returned. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Basic sample covariance calculation with stable algorithm**



```
DROP TABLE IF EXISTS series;
CREATE TABLE series(i UInt32, x_value Float64, y_value Float64) ENGINE = Memory;
INSERT INTO series(i, x_value, y_value) VALUES (1, 5.6,-4.4),(2, -9.6,3),(3, -1.3,-4),(4, 5.3,9.7),(5, 4.4,0.037),(6, -8.6,-7.8),(7, 5.1,9.3),(8, 7.9,-3.6),(9, -8.2,0.62),(10, -3,7.3);

SELECT covarSampStable(x_value, y_value)
FROM
(
    SELECT
        x_value,
        y_value
    FROM series
);

```


```
┌─covarSampStable(x_value, y_value)─┐
│                 7.206275555555556 │
└───────────────────────────────────┘

```

**Single value returns inf**



```
SELECT covarSampStable(x_value, y_value)
FROM
(
    SELECT
        x_value,
        y_value
    FROM series LIMIT 1
);

```


```
┌─covarSampStable(x_value, y_value)─┐
│                               inf │
└───────────────────────────────────┘

```
[PreviouscovarSampMatrix](/docs/sql-reference/aggregate-functions/reference/covarsampmatrix)[NextcramersV](/docs/sql-reference/aggregate-functions/reference/cramersv)- [covarSampStable](#covarSampStable)
Was this page helpful?
