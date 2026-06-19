# cramersVBiasCorrected \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- cramersVBiasCorrected
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/cramersVBiasCorrected.md)# cramersVBiasCorrected

## cramersVBiasCorrected[​](#cramersVBiasCorrected "Direct link to cramersVBiasCorrected")


Introduced in: v22\.1\.0


Cramer's V is a measure of association between two columns in a table.
The result of the [`cramersV` function](/docs/sql-reference/aggregate-functions/reference/cramersv) ranges from 0 (corresponding to no association between the variables) to 1 and can reach 1 only when each value is completely determined by the other.
The function can be heavily biased, so this version of Cramer's V uses the [bias correction](https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V#Bias_correction).


**Syntax**



```
cramersVBiasCorrected(column1, column2)

```

**Arguments**


- `column1` — First column to be compared. [`Any`](/docs/sql-reference/data-types)
- `column2` — Second column to be compared. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns a value between 0 (corresponding to no association between the columns' values) to 1 (complete association). [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Comparison with regular cramersV**



```
SELECT
    cramersV(a, b),
    cramersVBiasCorrected(a, b)
FROM
    (
        SELECT
            number % 10 AS a,
            number % 4 AS b
        FROM
            numbers(150)
    );

```


```
┌─────cramersV(a, b)─┬─cramersVBiasCorrected(a, b)─┐
│ 0.5798088336225178 │          0.5305112825189074 │
└────────────────────┴─────────────────────────────┘

```
[PreviouscramersV](/docs/sql-reference/aggregate-functions/reference/cramersv)[NextdeltaSum](/docs/sql-reference/aggregate-functions/reference/deltasum)- [cramersVBiasCorrected](#cramersVBiasCorrected)
Was this page helpful?
