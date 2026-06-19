# Replace modifier \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [SELECT](/docs/sql-reference/statements/select)- REPLACE
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/select/replace_modifier.md)# Replace modifier


> Allows you to specify one or more [expression aliases](/docs/sql-reference/syntax#expression-aliases).


Each alias must match a column name from the `SELECT *` statement. In the output column list, the column that matches
the alias is replaced by the expression in that `REPLACE`.


This modifier does not change the names or order of columns. However, it can change the value and the value type.


**Syntax:**



```
SELECT <expr> REPLACE( <expr> AS col_name) from [db.]table_name

```

**Example:**



```
SELECT * REPLACE(i + 1 AS i) from columns_transformers;

```


```
┌───i─┬──j─┬───k─┐
│ 101 │ 10 │ 324 │
│ 121 │  8 │  23 │
└─────┴────┴─────┘

```
[PreviousQUALIFY](/docs/sql-reference/statements/select/qualify)[NextSAMPLE](/docs/sql-reference/statements/select/sample)Was this page helpful?
