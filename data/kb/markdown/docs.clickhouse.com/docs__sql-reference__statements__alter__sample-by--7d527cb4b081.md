# Manipulating Sampling\-Key Expressions \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [ALTER](/docs/sql-reference/statements/alter)- SAMPLE BY
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/sample-by.md)# Manipulating Sampling\-Key Expressions

The following operations are available:


## MODIFY[​](#modify "Direct link to MODIFY")



```
ALTER TABLE [db].name [ON CLUSTER cluster] MODIFY SAMPLE BY new_expression

```

The command changes the [sampling key](/docs/engines/table-engines/mergetree-family/mergetree) of the table to `new_expression` (an expression or a tuple of expressions). The primary key must contain the new sample key.


## REMOVE[​](#remove "Direct link to REMOVE")



```
ALTER TABLE [db].name [ON CLUSTER cluster] REMOVE SAMPLE BY

```

The command removes the [sampling key](/docs/engines/table-engines/mergetree-family/mergetree) of the table.


The commands `MODIFY` and `REMOVE` are lightweight in the sense that they only change metadata or remove files.


NoteIt only works for tables in the [MergeTree](/docs/engines/table-engines/mergetree-family/mergetree) family (including [replicated](/docs/engines/table-engines/mergetree-family/replication) tables).

[PreviousORDER BY](/docs/sql-reference/statements/alter/order-by)[NextINDEX](/docs/sql-reference/statements/alter/skipping-index)- [MODIFY](#modify)- [REMOVE](#remove)
Was this page helpful?
