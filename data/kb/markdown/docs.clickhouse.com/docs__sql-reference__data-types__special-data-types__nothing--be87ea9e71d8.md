# Nothing \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Data types](/docs/sql-reference/data-types)- [Special Data Types](/docs/sql-reference/data-types/special-data-types)- Nothing
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/special-data-types/nothing.md)# Nothing

The only purpose of this data type is to represent cases where a value is not expected. So you can't create a `Nothing` type value.


For example, literal [NULL](/docs/sql-reference/syntax#null) has type of `Nullable(Nothing)`. See more about [Nullable](/docs/sql-reference/data-types/nullable).


The `Nothing` type can also used to denote empty arrays:



```
SELECT toTypeName(array())

```


```
┌─toTypeName(array())─┐
│ Array(Nothing)      │
└─────────────────────┘

```
[PreviousSet](/docs/sql-reference/data-types/special-data-types/set)[NextInterval](/docs/sql-reference/data-types/special-data-types/interval)Was this page helpful?
