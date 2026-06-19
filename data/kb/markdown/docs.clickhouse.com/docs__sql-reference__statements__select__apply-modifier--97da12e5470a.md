# APPLY modifier \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [SELECT](/docs/sql-reference/statements/select)- APPLY
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/select/apply_modifier.md)# APPLY modifier


> Allows you to invoke some function for each row returned by an outer table expression of a query.


## Syntax[​](#syntax "Direct link to Syntax")



```
SELECT <expr> APPLY( <func> ) FROM [db.]table_name

```

## Example[​](#example "Direct link to Example")



```
CREATE TABLE columns_transformers (i Int64, j Int16, k Int64) ENGINE = MergeTree ORDER by (i);
INSERT INTO columns_transformers VALUES (100, 10, 324), (120, 8, 23);
SELECT * APPLY(sum) FROM columns_transformers;

```


```
┌─sum(i)─┬─sum(j)─┬─sum(k)─┐
│    220 │     18 │    347 │
└────────┴────────┴────────┘

```
[PreviousALL](/docs/sql-reference/statements/select/all)[NextARRAY JOIN](/docs/sql-reference/statements/select/array-join)- [Syntax](#syntax)- [Example](#example)
Was this page helpful?
