# skewPop \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- skewPop
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/skewPop.md)# skewPop

## skewPop[​](#skewPop "Direct link to skewPop")


Introduced in: v20\.1\.0


Computes the [skewness](https://en.wikipedia.org/wiki/Skewness) of a sequence.


**Syntax**



```
skewPop(expr)

```

**Arguments**


- `expr` — An expression returning a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns the skewness of the given distribution. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Symmetric distribution**



```
SELECT skewPop(number) FROM numbers(100);

```


```
┌─skewPop(number)─┐
│               0 │
└─────────────────┘

```

**Right\-skewed distribution**



```
SELECT skewPop(x) FROM (SELECT pow(number, 2) AS x FROM numbers(10));

```


```
┌─────────skewPop(x)─┐
│ 0.6735701055423582 │
└────────────────────┘

```
[PrevioussingleValueOrNull](/docs/sql-reference/aggregate-functions/reference/singlevalueornull)[NextskewSamp](/docs/sql-reference/aggregate-functions/reference/skewsamp)- [skewPop](#skewPop)
Was this page helpful?
