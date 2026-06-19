# EXCEPT modifier \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [SELECT](/docs/sql-reference/statements/select)- EXCEPT
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/select/except_modifier.md)# EXCEPT modifier


> Specifies the names of one or more columns to exclude from the result. All matching column names are omitted from the output.


## Syntax[​](#syntax "Direct link to Syntax")



```
SELECT <expr> EXCEPT ( col_name1 [, col_name2, col_name3, ...] ) FROM [db.]table_name

```

## Examples[​](#examples "Direct link to Examples")



```
SELECT * EXCEPT (i) from columns_transformers;

```


```
┌──j─┬───k─┐
│ 10 │ 324 │
│  8 │  23 │
└────┴─────┘

```
[PreviousEXCEPT](/docs/sql-reference/statements/select/except)[NextFORMAT](/docs/sql-reference/statements/select/format)- [Syntax](#syntax)- [Examples](#examples)
Was this page helpful?
