# Apply mask of deleted rows \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [ALTER](/docs/sql-reference/statements/alter)- APPLY DELETED MASK
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/apply-deleted-mask.md)# Apply mask of deleted rows


```
ALTER TABLE [db].name [ON CLUSTER cluster] APPLY DELETED MASK [IN PARTITION partition_id]

```

The command applies mask created by [lightweight delete](/docs/sql-reference/statements/delete) and forcefully removes rows marked as deleted from disk. This command is a heavyweight mutation, and it semantically equals to query `ALTER TABLE [db].name DELETE WHERE _row_exists = 0`.


NoteIt only works for tables in the [`MergeTree`](/docs/engines/table-engines/mergetree-family/mergetree) family (including [replicated](/docs/engines/table-engines/mergetree-family/replication) tables).


**See also**


- [Lightweight deletes](/docs/sql-reference/statements/delete)
- [Heavyweight deletes](/docs/sql-reference/statements/alter/delete)
[PreviousUSER](/docs/sql-reference/statements/alter/user)[NextQUOTA](/docs/sql-reference/statements/alter/quota)Was this page helpful?
