# covarPopStable \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- covarPopStable
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/covarPopStable.md)# covarPopStable

## covarPopStable[​](#covarPopStable "Direct link to covarPopStable")


Introduced in: v1\.1\.0


Calculates the population covariance:


Σ(x−xˉ)(y−yˉ)n\\frac{\\Sigma{(x \- \\bar{x})(y \- \\bar{y})}}{n}nΣ(x−xˉ)(y−yˉ​)​
  

It is similar to the [`covarPop`](/docs/sql-reference/aggregate-functions/reference/covarpop) function, but uses a numerically stable algorithm. As a result, `covarPopStable` is slower than `covarPop` but produces a more accurate result.


**Syntax**



```
covarPopStable(x, y)

```

**Arguments**


- `x` — First variable. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `y` — Second variable. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the population covariance between `x` and `y`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Basic population covariance calculation with stable algorithm**



```
DROP TABLE IF EXISTS series;
CREATE TABLE series(i UInt32, x_value Float64, y_value Float64) ENGINE = Memory;
INSERT INTO series(i, x_value, y_value) VALUES (1, 5.6,-4.4),(2, -9.6,3),(3, -1.3,-4),(4, 5.3,9.7),(5, 4.4,0.037),(6, -8.6,-7.8),(7, 5.1,9.3),(8, 7.9,-3.6),(9, -8.2,0.62),(10, -3,7.3);

SELECT covarPopStable(x_value, y_value)
FROM series

```


```
┌─covarPopStable(x_value, y_value)─┐
│                         6.485648 │
└──────────────────────────────────┘

```
[PreviouscovarPopMatrix](/docs/sql-reference/aggregate-functions/reference/covarpopmatrix)[NextcovarSamp](/docs/sql-reference/aggregate-functions/reference/covarsamp)- [covarPopStable](#covarPopStable)
Was this page helpful?
