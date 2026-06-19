# analysisOfVariance \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- analysisOfVariance
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/analysisOfVariance.md)# analysisOfVariance

## analysisOfVariance[​](#analysisOfVariance "Direct link to analysisOfVariance")


Introduced in: v22\.10\.0


Provides a statistical test for one\-way analysis of variance (ANOVA test). It is a test over several groups of normally distributed observations to find out whether all groups have the same mean or not.


NoteGroups are enumerated starting from 0 and there should be at least two groups to perform a test.
There should be at least one group with the number of observations greater than one.


**Syntax**



```
analysisOfVariance(val, group_no)

```

**Aliases**: `anova`


**Arguments**


- `val` — Value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `group_no` — Group number that `val` belongs to. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns a tuple with the F\-statistic and p\-value. [`Tuple(Float64, Float64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT analysisOfVariance(number, number % 2) FROM numbers(1048575);

```


```
┌─analysisOfVariance(number, modulo(number, 2))─┐
│ (0,1)                                         │
└───────────────────────────────────────────────┘

```
[PreviousaggThrow](/docs/sql-reference/aggregate-functions/reference/aggthrow)[Nextany](/docs/sql-reference/aggregate-functions/reference/any)- [analysisOfVariance](#analysisOfVariance)
Was this page helpful?
