# stddevSampStable \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- stddevSampStable
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/stddevSampStable.md)# stddevSampStable

## stddevSampStable[​](#stddevSampStable "Direct link to stddevSampStable")


Introduced in: v1\.1\.0


The result is equal to the square root of [varSamp](/docs/sql-reference/aggregate-functions/reference/varSamp). Unlike [stddevSamp](/docs/sql-reference/aggregate-functions/reference/stddevsamp) this function uses a numerically stable algorithm. It works slower but provides a lower computational error.


**Syntax**



```
stddevSampStable(x)

```

**Arguments**


- `x` — Values for which to find the square root of sample variance. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the square root of sample variance of `x`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
DROP TABLE IF EXISTS test_data;
CREATE TABLE test_data
(
    population UInt8,
)
ENGINE = Log;

INSERT INTO test_data VALUES (3),(3),(3),(4),(4),(5),(5),(7),(11),(15);

SELECT
    stddevSampStable(population)
FROM test_data;

```


```
┌─stddevSampStable(population)─┐
│                            4 │
└──────────────────────────────┘

```
[PreviousstddevSamp](/docs/sql-reference/aggregate-functions/reference/stddevsamp)[NextstochasticLinearRegression](/docs/sql-reference/aggregate-functions/reference/stochasticlinearregression)- [stddevSampStable](#stddevSampStable)
Was this page helpful?
