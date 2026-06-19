# stddevPop \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- stddevPop
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/stddevPop.md)# stddevPop

## stddevPop[​](#stddevPop "Direct link to stddevPop")


Introduced in: v1\.1\.0


Returns the population standard deviation of a numeric data sequence.
The result is equal to the square root of [`varPop`](/docs/sql-reference/aggregate-functions/reference/varPop).


NoteThis function uses a numerically unstable algorithm. If you need [numerical stability](https://en.wikipedia.org/wiki/Numerical_stability) in calculations, use the [`stddevPopStable`](/docs/sql-reference/aggregate-functions/reference/stddevpopstable) function. It works slower but provides a lower computational error.


**Syntax**



```
stddevPop(x)

```

**Aliases**: `STD`, `STDDEV_POP`


**Arguments**


- `x` — Population of values to find the standard deviation of. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the square root of population variance of `x`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Computing population standard deviation**



```
CREATE TABLE test_data (population UInt8) ENGINE = Log;
INSERT INTO test_data VALUES (3),(3),(3),(4),(4),(5),(5),(7),(11),(15);

SELECT stddevPop(population) AS stddev FROM test_data;

```


```
┌────────────stddev─┐
│ 3.794733192202055 │
└───────────────────┘

```
[Previoussparkbar](/docs/sql-reference/aggregate-functions/reference/sparkbar)[NextstddevPopStable](/docs/sql-reference/aggregate-functions/reference/stddevpopstable)- [stddevPop](#stddevPop)
Was this page helpful?
