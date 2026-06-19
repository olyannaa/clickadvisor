# corr \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- corr
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/corr.md)# corr

## corr[​](#corr "Direct link to corr")


Introduced in: v1\.1\.0


Calculates the [Pearson correlation coefficient](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient):


Σ(x−xˉ)(y−yˉ)Σ(x−xˉ)2∗Σ(y−yˉ)2\\frac{\\Sigma{(x \- \\bar{x})(y \- \\bar{y})}}{\\sqrt{\\Sigma{(x \- \\bar{x})^2} \* \\Sigma{(y \- \\bar{y})^2}}}Σ(x−xˉ)2∗Σ(y−yˉ​)2​Σ(x−xˉ)(y−yˉ​)​
  

NoteThis function uses a numerically unstable algorithm. If you need [numerical stability](https://en.wikipedia.org/wiki/Numerical_stability) in calculations, use the [`corrStable`](/docs/sql-reference/aggregate-functions/reference/corrstable) function. It is slower but provides a more accurate result.


**Syntax**



```
corr(x, y)

```

**Arguments**


- `x` — First variable. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `y` — Second variable. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the Pearson correlation coefficient. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Basic correlation calculation**



```
DROP TABLE IF EXISTS series;
CREATE TABLE series
(
    i UInt32,
    x_value Float64,
    y_value Float64
)
ENGINE = Memory;
INSERT INTO series(i, x_value, y_value) VALUES (1, 5.6, -4.4),(2, -9.6, 3),(3, -1.3, -4),(4, 5.3, 9.7),(5, 4.4, 0.037),(6, -8.6, -7.8),(7, 5.1, 9.3),(8, 7.9, -3.6),(9, -8.2, 0.62),(10, -3, 7.3);

SELECT corr(x_value, y_value)
FROM series

```


```
┌─corr(x_value, y_value)─┐
│     0.1730265755453256 │
└────────────────────────┘

```
[Previouscontingency](/docs/sql-reference/aggregate-functions/reference/contingency)[NextcorrMatrix](/docs/sql-reference/aggregate-functions/reference/corrmatrix)- [corr](#corr)
Was this page helpful?
