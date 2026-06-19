# Null dictionary source \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- DICTIONARY- SOURCE- Null
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/dictionary/sources/null.md)# Null dictionary source

A special source that can be used to create dummy (empty) dictionaries.
Dummy dictionaries can be useful for testing purposes or for setups with separate data and query nodes with distributed tables.



```
CREATE DICTIONARY null_dict (
    id              UInt64,
    val             UInt8,
    default_val     UInt8 DEFAULT 123,
    nullable_val    Nullable(UInt8)
)
PRIMARY KEY id
SOURCE(NULL())
LAYOUT(FLAT())
LIFETIME(0);

```
[PreviousYTsaurus](/docs/sql-reference/statements/create/dictionary/sources/ytsaurus)[NextYAMLRegExpTree](/docs/sql-reference/statements/create/dictionary/sources/yamlregexptree)Was this page helpful?
