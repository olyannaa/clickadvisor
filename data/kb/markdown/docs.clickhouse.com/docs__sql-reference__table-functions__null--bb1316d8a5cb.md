# null \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- null function
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/null.md)# null

Creates a temporary table of the specified structure with the [Null](/docs/engines/table-engines/special/null) table engine. According to the `Null`\-engine properties, the table data is ignored and the table itself is immediately dropped right after the query execution. The function is used for the convenience of test writing and demonstrations.


## Syntax[​](#syntax "Direct link to Syntax")



```
null('structure')

```

## Argument[​](#argument "Direct link to Argument")


- `structure` — A list of columns and column types. [String](/docs/sql-reference/data-types/string).


## Returned value[​](#returned_value "Direct link to Returned value")


A temporary `Null`\-engine table with the specified structure.


## Example[​](#example "Direct link to Example")


Query with the `null` function:



```
INSERT INTO function null('x UInt64') SELECT * FROM numbers_mt(1000000000);

```

can replace three queries:



```
CREATE TABLE t (x UInt64) ENGINE = Null;
INSERT INTO t SELECT * FROM numbers_mt(1000000000);
DROP TABLE IF EXISTS t;

```

## Related[​](#related "Direct link to Related")


- [Null table engine](/docs/engines/table-engines/special/null)
[Previousmysql](/docs/sql-reference/table-functions/mysql)[Nextnumbers](/docs/sql-reference/table-functions/numbers)- [Syntax](#syntax)- [Argument](#argument)- [Returned value](#returned_value)- [Example](#example)- [Related](#related)
Was this page helpful?
