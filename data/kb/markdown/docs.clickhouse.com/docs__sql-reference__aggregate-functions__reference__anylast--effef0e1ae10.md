# anyLast \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- anyLast
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/anyLast.md)# anyLast

## anyLast[​](#anyLast "Direct link to anyLast")


Introduced in: v1\.1\.0


Selects the last encountered value of a column.


NoteAs a query can be executed in arbitrary order, the result of this function is non\-deterministic.
If you need an arbitrary but deterministic result, use functions [min](/docs/sql-reference/aggregate-functions/reference/min) or [max](/docs/sql-reference/aggregate-functions/reference/max).


By default, the function never returns NULL, i.e. ignores NULL values in the input column.
However, if the function is used with the `RESPECT NULLS` modifier, it returns the last value reads no matter if NULL or not.


**Syntax**



```
anyLast(column) [RESPECT NULLS]

```

**Aliases**: `last_value`


**Arguments**


- `column` — The column name. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the last value encountered. [`Any`](/docs/sql-reference/data-types)


**Examples**


**Usage example**



```
CREATE TABLE tab(city Nullable(String)) ENGINE=Memory;
INSERT INTO tab (city) VALUES ('Amsterdam'), (NULL), ('New York'), ('Tokyo'), ('Valencia'), (NULL);
SELECT anyLast(city), anyLastRespectNulls(city) FROM tab;

```


```
┌─anyLast(city)─┬─anyLastRespectNulls(city)─┐
│ Valencia      │ ᴺᵁᴸᴸ                      │
└───────────────┴───────────────────────────┘

```
[PreviousanyHeavy](/docs/sql-reference/aggregate-functions/reference/anyheavy)[Nextapprox\_top\_k](/docs/sql-reference/aggregate-functions/reference/approxtopk)- [anyLast](#anyLast)
Was this page helpful?
