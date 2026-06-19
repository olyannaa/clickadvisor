# merge \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- merge
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/merge.md)# merge

Creates a temporary [Merge](/docs/engines/table-engines/special/merge) table.
The table schema is derived from underlying tables by using a union of their columns and by deriving common types.
The same virtual columns are available as for the [Merge](/docs/engines/table-engines/special/merge) table engine.


## Syntax[​](#syntax "Direct link to Syntax")



```
merge(['db_name',] 'tables_regexp')

```

## Arguments[​](#arguments "Direct link to Arguments")




| Argument Description| `db_name` Possible values (optional, default is `currentDatabase()`): \- database name, \- constant expression that returns a string with a database name, for example, `currentDatabase()`, \- `REGEXP(expression)`, where `expression` is a regular expression to match the DB names.| `tables_regexp` A regular expression to match the table names in the specified DB or DBs. | | | | | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- |


## Related[​](#related "Direct link to Related")


- [Merge](/docs/engines/table-engines/special/merge) table engine
[Previousjdbc](/docs/sql-reference/table-functions/jdbc)[Nextmongodb](/docs/sql-reference/table-functions/mongodb)- [Syntax](#syntax)- [Arguments](#arguments)- [Related](#related)
Was this page helpful?
