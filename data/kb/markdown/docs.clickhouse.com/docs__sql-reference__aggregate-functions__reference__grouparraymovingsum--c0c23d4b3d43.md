# groupArrayMovingSum \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- groupArrayMovingSum
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/groupArrayMovingSum.md)# groupArrayMovingSum

## groupArrayMovingSum[​](#groupArrayMovingSum "Direct link to groupArrayMovingSum")


Introduced in: v20\.1\.0


Calculates the moving sum of input values.


The function can take the window size as a parameter. If left unspecified, the function takes the window size equal to the number of rows in the column.


**Syntax**



```
groupArrayMovingSum(numbers_for_summing)
groupArrayMovingSum(window_size)(numbers_for_summing)

```

**Parameters**


- `window_size` — Size of the calculation window. If left unspecified, the function takes the window size equal to the number of rows in the column. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Arguments**


- `numbers_for_summing` — Expression resulting in a numeric data type value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns an array of the same size and type as the input data. [`Array`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
CREATE TABLE t
(
    `int` UInt8,
    `float` Float32,
    `dec` Decimal32(2)
)
ENGINE = Memory;

INSERT INTO t VALUES (1, 1.1, 1.10), (2, 2.2, 2.20), (4, 4.4, 4.40), (7, 7.77, 7.77);

SELECT
    groupArrayMovingSum(int) AS I,
    groupArrayMovingSum(float) AS F,
    groupArrayMovingSum(dec) AS D
FROM t;

```


```
┌─I──────────┬─F───────────────────────────────┬─D──────────────────────┐
│ [1,3,7,14] │ [1.1,3.3000002,7.7000003,15.47] │ [1.10,3.30,7.70,15.47] │
└────────────┴─────────────────────────────────┴────────────────────────┘

```

**With window size**



```
SELECT
    groupArrayMovingSum(2)(int) AS I,
    groupArrayMovingSum(2)(float) AS F,
    groupArrayMovingSum(2)(dec) AS D
FROM t;

```


```
┌─I──────────┬─F───────────────────────────────┬─D──────────────────────┐
│ [1,3,6,11] │ [1.1,3.3000002,6.6000004,12.17] │ [1.10,3.30,6.60,12.17] │
└────────────┴─────────────────────────────────┴────────────────────────┘

```
[PreviousgroupArrayMovingAvg](/docs/sql-reference/aggregate-functions/reference/grouparraymovingavg)[NextgroupArraySample](/docs/sql-reference/aggregate-functions/reference/grouparraysample)- [groupArrayMovingSum](#groupArrayMovingSum)
Was this page helpful?
