# varPopStable \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- varPopStable
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/varPopStable.md)# varPopStable

## varPopStable[​](#varPopStable "Direct link to varPopStable")


Introduced in: v1\.1\.0


Returns the population variance.
Unlike [`varPop`](/docs/sql-reference/aggregate-functions/reference/varPop), this function uses a [numerically stable](https://en.wikipedia.org/wiki/Numerical_stability) algorithm.
It works slower but provides a lower computational error.


**Syntax**



```
varPopStable(x)

```

**Arguments**


- `x` — Population of values to find the population variance of. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the population variance of `x`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Computing stable population variance**



```
DROP TABLE IF EXISTS test_data;
CREATE TABLE test_data
(
    x UInt8,
)
ENGINE = Memory;

INSERT INTO test_data VALUES (3),(3),(3),(4),(4),(5),(5),(7),(11),(15);

SELECT
    varPopStable(x) AS var_pop_stable
FROM test_data;

```


```
┌─var_pop_stable─┐
│           14.4 │
└────────────────┘

```
[PreviousvarPop](/docs/sql-reference/aggregate-functions/reference/varPop)[NextvarSamp](/docs/sql-reference/aggregate-functions/reference/varSamp)- [varPopStable](#varPopStable)
Was this page helpful?
