# uniqExact \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- uniqExact
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/uniqExact.md)# uniqExact

## uniqExact[​](#uniqExact "Direct link to uniqExact")


Introduced in: v1\.1\.0


Calculates the exact number of different argument values.


NoteThe `uniqExact` function uses more memory than `uniq`, because the size of the state has unbounded growth as the number of different values increases.
Use the `uniqExact` function if you absolutely need an exact result.
Otherwise use the [`uniq`](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/uniq) function.


**Syntax**



```
uniqExact(x[, ...])

```

**Arguments**


- `x` — The function takes a variable number of parameters. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the exact number of different argument values as a UInt64\. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
CREATE TABLE example_data
(
    id UInt32,
    category String
)
ENGINE = Memory;

INSERT INTO example_data VALUES
(1, 'A'), (2, 'B'), (3, 'A'), (4, 'C'), (5, 'B'), (6, 'A');

SELECT uniqExact(category) as exact_unique_categories
FROM example_data;

```


```
┌─exact_unique_categories─┐
│                       3 │
└─────────────────────────┘

```

**Multiple arguments**



```
SELECT uniqExact(id, category) as exact_unique_combinations
FROM example_data;

```


```
┌─exact_unique_combinations─┐
│                         6 │
└───────────────────────────┘

```

**See Also**


- [uniq](/docs/sql-reference/aggregate-functions/reference/uniq)
- [uniqCombined](/docs/sql-reference/aggregate-functions/reference/uniqcombined)
- [uniqHLL12](/docs/sql-reference/aggregate-functions/reference/uniqhll12)
- [uniqTheta](/docs/sql-reference/aggregate-functions/reference/uniqthetasketch)
[PreviousuniqCombined64](/docs/sql-reference/aggregate-functions/reference/uniqcombined64)[NextuniqHLL12](/docs/sql-reference/aggregate-functions/reference/uniqhll12)- [uniqExact](#uniqExact)
Was this page helpful?
