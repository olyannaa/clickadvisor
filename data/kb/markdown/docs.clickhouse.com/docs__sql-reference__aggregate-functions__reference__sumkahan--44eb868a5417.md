# sumKahan \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- sumKahan
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/sumKahan.md)# sumKahan

## sumKahan[​](#sumKahan "Direct link to sumKahan")


Introduced in: v1\.1\.0


Calculates the sum of the numbers with [Kahan compensated summation algorithm](https://en.wikipedia.org/wiki/Kahan_summation_algorithm).
Slower than [`sum`](/docs/sql-reference/aggregate-functions/reference/sum) function.
The compensation works only for [Float](/docs/sql-reference/data-types/float) types.


**Syntax**



```
sumKahan(x)

```

**Arguments**


- `x` — Input value. [`Integer`](/docs/sql-reference/data-types/int-uint) or [`Float`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the sum of numbers. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Examples**


**Demonstrating precision improvement with Kahan summation**



```
SELECT sum(0.1), sumKahan(0.1) FROM numbers(10);

```


```
┌───────────sum(0.1)─┬─sumKahan(0.1)─┐
│ 0.9999999999999999 │             1 │
└────────────────────┴───────────────┘

```
[PrevioussumCount](/docs/sql-reference/aggregate-functions/reference/sumcount)[NextsumMapWithOverflow](/docs/sql-reference/aggregate-functions/reference/summapwithoverflow)- [sumKahan](#sumKahan)
Was this page helpful?
