# varPop \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- varPop
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/varPop.md)# varPop

## varPop[​](#varPop "Direct link to varPop")


Introduced in: v1\.1\.0


Calculates the population variance.


The population variance is calculated using the formula:


Σ(x−xˉ)2n\\frac{\\Sigma{(x \- \\bar{x})^2}}{n}nΣ(x−xˉ)2​
  

Where:


- xxx is each value in the population
- xˉ\\bar{x}xˉ is the population mean
- nnn is the population size


NoteThis function uses a numerically unstable algorithm. If you need [numerical stability](https://en.wikipedia.org/wiki/Numerical_stability) in calculations, use the [`varPopStable`](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/varpopstable) function. It works slower but provides a lower computational error.


**Syntax**



```
varPop(x)

```

**Aliases**: `VAR_POP`


**Arguments**


- `x` — Population of values to find the population variance of. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the population variance of `x`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Computing population variance**



```
DROP TABLE IF EXISTS test_data;
CREATE TABLE test_data
(
    x UInt8,
)
ENGINE = Memory;

INSERT INTO test_data VALUES (3), (3), (3), (4), (4), (5), (5), (7), (11), (15);

SELECT
    varPop(x) AS var_pop
FROM test_data;

```


```
┌─var_pop─┐
│    14.4 │
└─────────┘

```
[PreviousuniqTheta](/docs/sql-reference/aggregate-functions/reference/uniqthetasketch)[NextvarPopStable](/docs/sql-reference/aggregate-functions/reference/varpopstable)- [varPop](#varPop)
Was this page helpful?
