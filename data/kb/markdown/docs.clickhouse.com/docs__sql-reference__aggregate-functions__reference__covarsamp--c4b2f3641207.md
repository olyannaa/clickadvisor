# covarSamp \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- covarSamp
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/covarSamp.md)# covarSamp

## covarSamp[​](#covarSamp "Direct link to covarSamp")


Introduced in: v1\.1\.0


Calculates the sample covariance:


Σ(x−xˉ)(y−yˉ)n−1\\frac{\\Sigma{(x \- \\bar{x})(y \- \\bar{y})}}{n \- 1}n−1Σ(x−xˉ)(y−yˉ​)​
NoteThis function uses a numerically unstable algorithm. If you need [numerical stability](https://en.wikipedia.org/wiki/Numerical_stability) in calculations, use the [`covarSampStable`](/docs/sql-reference/aggregate-functions/reference/covarsampstable) function.
It works slower but provides a lower computational error.


**Syntax**



```
covarSamp(x, y)

```

**Aliases**: `COVAR_SAMP`


**Arguments**


- `x` — First variable. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `y` — Second variable. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the sample covariance between `x` and `y`. For `n <= 1`, `nan` is returned. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Basic sample covariance calculation**



```
DROP TABLE IF EXISTS series;
CREATE TABLE series(i UInt32, x_value Float64, y_value Float64) ENGINE = Memory;
INSERT INTO series(i, x_value, y_value) VALUES (1, 5.6,-4.4),(2, -9.6,3),(3, -1.3,-4),(4, 5.3,9.7),(5, 4.4,0.037),(6, -8.6,-7.8),(7, 5.1,9.3),(8, 7.9,-3.6),(9, -8.2,0.62),(10, -3,7.3);

SELECT covarSamp(x_value, y_value)
FROM series

```


```
┌─covarSamp(x_value, y_value)─┐
│           7.206275555555556 │
└─────────────────────────────┘

```

**Single value returns NaN**



```
SELECT covarSamp(x_value, y_value)
FROM series LIMIT 1

```


```
┌─covarSamp(x_value, y_value)─┐
│                         nan │
└─────────────────────────────┘

```
[PreviouscovarPopStable](/docs/sql-reference/aggregate-functions/reference/covarpopstable)[NextcovarSampMatrix](/docs/sql-reference/aggregate-functions/reference/covarsampmatrix)- [covarSamp](#covarSamp)
Was this page helpful?
