# anyHeavy \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- anyHeavy
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/anyHeavy.md)# anyHeavy

## anyHeavy[​](#anyHeavy "Direct link to anyHeavy")


Introduced in: v1\.1\.0


Selects a frequently occurring value using the [heavy hitters](https://doi.org/10.1145/762471.762473) algorithm.
If there is a value that occurs more than in half the cases in each of the query's execution threads, this value is returned.
Normally, the result is nondeterministic.


**Syntax**



```
anyHeavy(column)

```

**Arguments**


- `column` — The column name. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a frequently occurring value. The result is nondeterministic. [`Any`](/docs/sql-reference/data-types)


**Examples**


**Usage example**



```
SELECT anyHeavy(AirlineID) AS res
FROM ontime;

```


```
┌───res─┐
│ 19690 │
└───────┘

```
[Previousany](/docs/sql-reference/aggregate-functions/reference/any)[NextanyLast](/docs/sql-reference/aggregate-functions/reference/anylast)- [anyHeavy](#anyHeavy)
Was this page helpful?
