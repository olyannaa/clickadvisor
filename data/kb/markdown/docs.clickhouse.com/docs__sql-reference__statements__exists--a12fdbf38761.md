# EXISTS Statement \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- EXISTS
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/exists.md)# EXISTS Statement


```
EXISTS [TEMPORARY] [TABLE|DICTIONARY|DATABASE] [db.]name [INTO OUTFILE filename] [FORMAT format]

```

Returns a single `UInt8`\-type column, which contains the single value `0` if the table or database does not exist, or `1` if the table exists in the specified database.

[PreviousDROP](/docs/sql-reference/statements/drop)[NextKILL](/docs/sql-reference/statements/kill)Was this page helpful?
