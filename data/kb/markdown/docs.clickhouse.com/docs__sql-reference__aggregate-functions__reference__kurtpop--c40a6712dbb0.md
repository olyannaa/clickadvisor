# kurtPop \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- kurtPop
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/kurtPop.md)# kurtPop

## kurtPop[​](#kurtPop "Direct link to kurtPop")


Introduced in: v20\.1\.0


Computes the [kurtosis](https://en.wikipedia.org/wiki/Kurtosis) of a sequence.


**Syntax**



```
kurtPop(expr)

```

**Arguments**


- `expr` — [Expression](/docs/sql-reference/syntax#expressions) returning a number. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the kurtosis of the given distribution. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Computing kurtosis**



```
CREATE TABLE test_data (x Float64) ENGINE = Memory;
INSERT INTO test_data VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

SELECT kurtPop(x) FROM test_data;

```


```
┌─────────kurtPop(x)─┐
│ 1.7757575757575756 │
└────────────────────┘

```
[PreviouskolmogorovSmirnovTest](/docs/sql-reference/aggregate-functions/reference/kolmogorovsmirnovtest)[NextkurtSamp](/docs/sql-reference/aggregate-functions/reference/kurtsamp)- [kurtPop](#kurtPop)
Was this page helpful?
