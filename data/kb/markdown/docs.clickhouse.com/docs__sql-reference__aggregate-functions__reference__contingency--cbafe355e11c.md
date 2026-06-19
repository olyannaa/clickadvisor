# contingency \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- contingency
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/contingency.md)# contingency

## contingency[​](#contingency "Direct link to contingency")


Introduced in: v22\.1\.0


The `contingency` function calculates the [contingency coefficient](https://en.wikipedia.org/wiki/Contingency_table#Cram%C3%A9r's_V_and_the_contingency_coefficient_C), a value that measures the association between two columns in a table.
The computation is similar to the [`cramersV`](/docs/sql-reference/aggregate-functions/reference/cramersv) function but with a different denominator in the square root.


**Syntax**



```
contingency(column1, column2)

```

**Arguments**


- `column1` — First column to compare. [`Any`](/docs/sql-reference/data-types)
- `column2` — Second column to compare. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns a value between 0 and 1\. The larger the result, the closer the association of the two columns. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Comparison with cramersV**



```
SELECT
    cramersV(a, b),
    contingency(a, b)
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
┌─────cramersV(a, b)─┬──contingency(a, b)─┐
│ 0.5798088336225178 │ 0.708607540104077  │
└────────────────────┴────────────────────┘

```
[PreviouscategoricalInformationValue](/docs/sql-reference/aggregate-functions/reference/categoricalinformationvalue)[Nextcorr](/docs/sql-reference/aggregate-functions/reference/corr)- [contingency](#contingency)
Was this page helpful?
