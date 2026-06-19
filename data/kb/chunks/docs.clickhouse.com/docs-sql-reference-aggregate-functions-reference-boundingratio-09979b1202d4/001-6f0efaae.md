---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/boundingRatio.md)#
topic: boundingratio-clickhouse-docs
ch_version_introduced: '1.5'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 1
---

# boundingRatio \| ClickHouse Docs

- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- boundingRatio
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/boundingRatio.md)# boundingRatio

## boundingRatio[​](#boundingRatio "Direct link to boundingRatio")

Introduced in: v20\.1\.0

Calculates the slope between the leftmost and rightmost points across a group of values.

**Syntax**

```
boundingRatio(x, y)

```

**Arguments**

- `x` — X\-coordinate values. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `y` — Y\-coordinate values. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)

**Returned value**

Returns the slope of the line between the leftmost and rightmost points, otherwise returns `NaN` if the data is empty. [`Float64`](/docs/sql-reference/data-types/float)

**Examples**

**Sample data**

```
SELECT
    number,
    number * 1.5
FROM numbers(10)

```

```
┌─number─┬─multiply(number, 1.5)─┐
│      0 │                     0 │
│      1 │                   1.5 │
│      2 │                     3 │
│      3 │                   4.5 │
│      4 │                     6 │
│      5 │                   7.5 │
│      6 │                     9 │
│      7 │                  10.5 │
│      8 │                    12 │
│      9 │                  13.5 │
└────────┴───────────────────────┘

```

**Usage example**

```
SELECT boundingRatio(number, number * 1.5)
FROM numbers(10)

```

```
┌─boundingRatio(number, multiply(number, 1.5))─┐
│                                          1.5 │
└──────────────────────────────────────────────┘

```
[PreviousavgWeighted](/docs/sql-reference/aggregate-functions/reference/avgweighted)[NextcategoricalInformationValue](/docs/sql-reference/aggregate-functions/reference/categoricalinformationvalue)- [boundingRatio](#boundingRatio)
Was this page helpful?
