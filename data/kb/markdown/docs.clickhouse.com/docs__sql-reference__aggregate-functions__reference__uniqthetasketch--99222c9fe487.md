# uniqTheta \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- uniqTheta
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/uniqTheta.md)# uniqTheta

## uniqTheta[​](#uniqTheta "Direct link to uniqTheta")


Introduced in: v21\.6\.0


Calculates the approximate number of different argument values, using the [Theta Sketch Framework](https://datasketches.apache.org/docs/Theta/ThetaSketches.html#theta-sketch-framework).


Implementation detailsThis function calculates a hash for all parameters in the aggregate, then uses it in calculations.
It uses the [KMV](https://datasketches.apache.org/docs/Theta/InverseEstimate.html) algorithm to approximate the number of different argument values.4096(2^12\) 64\-bit sketch are used.
The size of the state is about 41 KB.The relative error is 3\.125% (95% confidence), see the [relative error table](https://datasketches.apache.org/docs/Theta/ThetaErrorTable.html) for detail.






**Syntax**



```
uniqTheta(x[, ...])

```

**Arguments**


- `x` — The function takes a variable number of parameters. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns a UInt64\-type number representing the approximate number of different argument values. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
CREATE TABLE example_theta
(
    id UInt32,
    category String
)
ENGINE = Memory;

INSERT INTO example_theta VALUES
(1, 'A'), (2, 'B'), (3, 'A'), (4, 'C'), (5, 'B'), (6, 'A');

SELECT uniqTheta(category) as theta_unique_categories
FROM example_theta;

```


```
┌─theta_unique_categories─┐
│                       3 │
└─────────────────────────┘

```

**See Also**


- [uniq](/docs/sql-reference/aggregate-functions/reference/uniq)
- [uniqCombined](/docs/sql-reference/aggregate-functions/reference/uniqcombined)
- [uniqCombined64](/docs/sql-reference/aggregate-functions/reference/uniqcombined64)
- [uniqHLL12](/docs/sql-reference/aggregate-functions/reference/uniqhll12)
- [uniqExact](/docs/sql-reference/aggregate-functions/reference/uniqexact)
[PreviousuniqHLL12](/docs/sql-reference/aggregate-functions/reference/uniqhll12)[NextvarPop](/docs/sql-reference/aggregate-functions/reference/varPop)- [uniqTheta](#uniqTheta)
Was this page helpful?
