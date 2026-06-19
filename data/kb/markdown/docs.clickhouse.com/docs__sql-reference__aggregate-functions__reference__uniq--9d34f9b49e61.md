# uniq \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- uniq
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/uniq.md)# uniq

## uniq[​](#uniq "Direct link to uniq")


Introduced in: v1\.1\.0


Calculates the approximate number of different values of the argument.


The function uses an adaptive sampling algorithm. For the calculation state, the function uses a sample of element hash values up to 65536\. This algorithm is very accurate and very efficient on the CPU. When the query contains several of these functions, using uniq is almost as fast as using other aggregate functions.


Implementation detailsThis function calculates a hash for all parameters in the aggregate, then uses it in calculations.
It uses an adaptive sampling algorithm.
For the calculation state, the function uses a sample of element hash values up to 65536\.
This algorithm is very accurate and very efficient on the CPU.
When the query contains several of these functions, using `uniq` is almost as fast as using other aggregate functions.


TipWe recommend using this function over other variants in almost all scenarios.


**Syntax**



```
uniq(x[, ...])

```

**Arguments**


- `x` — The function takes a variable number of parameters. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns a UInt64\-type number representing the approximate number of different values. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Example usage**



```
CREATE TABLE example_table (
    id UInt32,
    category String,
    value Float64
) ENGINE = Memory;

INSERT INTO example_table VALUES
(1, 'A', 10.5),
(2, 'B', 20.3),
(3, 'A', 15.7),
(4, 'C', 8.9),
(5, 'B', 12.1),
(6, 'A', 18.4);

SELECT uniq(category) as unique_categories
FROM example_table;

```


```
┌─unique_categories─┐
│                 3 │
└───────────────────┘

```

**Multiple arguments**



```
SELECT uniq(category, value) as unique_combinations
FROM example_table;

```


```
┌─unique_combinations─┐
│                   6 │
└─────────────────────┘

```

**See Also**


- [uniqCombined](/docs/sql-reference/aggregate-functions/reference/uniqcombined)
- [uniqCombined64](/docs/sql-reference/aggregate-functions/reference/uniqcombined64)
- [uniqHLL12](/docs/sql-reference/aggregate-functions/reference/uniqhll12)
- [uniqExact](/docs/sql-reference/aggregate-functions/reference/uniqexact)
- [uniqTheta](/docs/sql-reference/aggregate-functions/reference/uniqthetasketch)
[PrevioustopKWeighted](/docs/sql-reference/aggregate-functions/reference/topkweighted)[NextuniqCombined](/docs/sql-reference/aggregate-functions/reference/uniqcombined)- [uniq](#uniq)
Was this page helpful?
