# DESCRIBE TABLE \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- DESCRIBE TABLE
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/describe-table.md)# DESCRIBE TABLE

Returns information about table columns.


**Syntax**



```
DESC|DESCRIBE TABLE [db.]table [INTO OUTFILE filename] [FORMAT format]

```

The `DESCRIBE` statement returns a row for each table column with the following [String](/docs/sql-reference/data-types/string) values:


- `name` — A column name.
- `type` — A column type.
- `default_type` — A clause that is used in the column [default expression](/docs/sql-reference/statements/create/table): `DEFAULT`, `MATERIALIZED` or `ALIAS`. If there is no default expression, then empty string is returned.
- `default_expression` — An expression specified after the `DEFAULT` clause.
- `comment` — A [column comment](/docs/sql-reference/statements/alter/column#comment-column).
- `codec_expression` — A [codec](/docs/sql-reference/statements/create/table#column_compression_codec) that is applied to the column.
- `ttl_expression` — A [TTL](/docs/engines/table-engines/mergetree-family/mergetree#table_engine-mergetree-ttl) expression.
- `is_subcolumn` — A flag that equals `1` for internal subcolumns. It is included into the result only if subcolumn description is enabled by the [describe\_include\_subcolumns](/docs/operations/settings/settings#describe_include_subcolumns) setting.


All columns in [Nested](/docs/sql-reference/data-types/nested-data-structures/nested) data structures are described separately. The name of each column is prefixed with a parent column name and a dot.


To show internal subcolumns of other data types, use the [describe\_include\_subcolumns](/docs/operations/settings/settings#describe_include_subcolumns) setting.


**Example**



```
CREATE TABLE describe_example (
    id UInt64, text String DEFAULT 'unknown' CODEC(ZSTD),
    user Tuple (name String, age UInt8)
) ENGINE = MergeTree() ORDER BY id;

DESCRIBE TABLE describe_example;
DESCRIBE TABLE describe_example SETTINGS describe_include_subcolumns=1;

```


```
┌─name─┬─type──────────────────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
│ id   │ UInt64                        │              │                    │         │                  │                │
│ text │ String                        │ DEFAULT      │ 'unknown'          │         │ ZSTD(1)          │                │
│ user │ Tuple(name String, age UInt8) │              │                    │         │                  │                │
└──────┴───────────────────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

```

The second query additionally shows subcolumns:



```
┌─name──────┬─type──────────────────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┬─is_subcolumn─┐
│ id        │ UInt64                        │              │                    │         │                  │                │            0 │
│ text      │ String                        │ DEFAULT      │ 'unknown'          │         │ ZSTD(1)          │                │            0 │
│ user      │ Tuple(name String, age UInt8) │              │                    │         │                  │                │            0 │
│ user.name │ String                        │              │                    │         │                  │                │            1 │
│ user.age  │ UInt8                         │              │                    │         │                  │                │            1 │
└───────────┴───────────────────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┴──────────────┘

```

The DESCRIBE statement can also be used with subqueries or scalar expressions:



```
DESCRIBE SELECT 1 FORMAT TSV;

```

or



```
DESCRIBE (SELECT 1) FORMAT TSV;

```


```
1       UInt8

```

This usage returns metadata about the result columns of the specified query or subquery. It is useful for understanding the structure of complex queries before execution.


**See Also**


- [describe\_include\_subcolumns](/docs/operations/settings/settings#describe_include_subcolumns) setting.
[PreviousCHECK TABLE](/docs/sql-reference/statements/check-table)[NextDETACH](/docs/sql-reference/statements/detach)Was this page helpful?
