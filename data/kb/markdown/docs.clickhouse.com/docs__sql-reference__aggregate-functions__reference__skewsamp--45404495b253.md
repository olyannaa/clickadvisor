# skewSamp \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- skewSamp
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/skewSamp.md)# skewSamp

## skewSamp[​](#skewSamp "Direct link to skewSamp")


Introduced in: v20\.1\.0


Computes the [sample skewness](https://en.wikipedia.org/wiki/Skewness) of a sequence.


It represents an unbiased estimate of the skewness of a random variable if passed values form its sample.


**Syntax**



```
skewSamp(expr)

```

**Arguments**


- `expr` — An expression returning a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns the skewness of the given distribution. If `n <= 1` (`n` is the size of the sample), then the function returns `nan`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Symmetric distribution**



```
SELECT skewSamp(number) FROM numbers(100);

```


```
┌─skewSamp(number)─┐
│                0 │
└──────────────────┘

```

**Right\-skewed distribution**



```
SELECT skewSamp(x) FROM (SELECT pow(number, 2) AS x FROM numbers(10));

```


```
┌────────skewSamp(x)─┐
│ 0.5751042382747413 │
└────────────────────┘

```
[PreviousskewPop](/docs/sql-reference/aggregate-functions/reference/skewpop)[Nextsparkbar](/docs/sql-reference/aggregate-functions/reference/sparkbar)- [skewSamp](#skewSamp)
Was this page helpful?
