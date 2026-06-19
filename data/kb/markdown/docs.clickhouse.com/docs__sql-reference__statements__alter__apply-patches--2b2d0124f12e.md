# Apply patches from lightweight updates \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [ALTER](/docs/sql-reference/statements/alter)- APPLY PATCHES
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/apply-patches.md)# Apply patches from lightweight updates

Beta feature. [Learn more.](/docs/beta-and-experimental-features#beta-features)

```
ALTER TABLE [db.]table [ON CLUSTER cluster] APPLY PATCHES [IN PARTITION partition_id]

```

The command manually triggers the physical materialization of patch parts created by [lightweight `UPDATE`](/docs/sql-reference/statements/update) statements. It forcefully applies pending patches to the data parts by rewriting only the affected columns.


Note- It only works for tables in the [`MergeTree`](/docs/engines/table-engines/mergetree-family/mergetree) family (including [replicated](/docs/engines/table-engines/mergetree-family/replication) tables).
- This is a mutation operation and executes asynchronously in the background.

## When to use APPLY PATCHES[​](#when-to-use "Direct link to When to use APPLY PATCHES")


TipGenerally, you should not need to use `APPLY PATCHES`


Patch parts are normally applied automatically during merges when the [`apply_patches_on_merge`](/docs/operations/settings/merge-tree-settings#apply_patches_on_merge) setting is enabled (default). However, you may want to manually trigger patch application in these scenarios:


- To reduce the overhead of applying patches during `SELECT` queries
- To consolidate multiple patch parts before they accumulate
- To prepare data for backup or export with patches already materialized
- When `apply_patches_on_merge` is disabled and you want to control when patches are applied


## Examples[​](#examples "Direct link to Examples")


Apply all pending patches for a table:



```
ALTER TABLE my_table APPLY PATCHES;

```

Apply patches only for a specific partition:



```
ALTER TABLE my_table APPLY PATCHES IN PARTITION '2024-01';

```

Combine with other operations:



```
ALTER TABLE my_table APPLY PATCHES, UPDATE column = value WHERE condition;

```

## Monitoring patch application[​](#monitor "Direct link to Monitoring patch application")


You can monitor the progress of patch application using the [`system.mutations`](/docs/operations/system-tables/mutations) table:



```
SELECT * FROM system.mutations
WHERE table = 'my_table' AND command LIKE '%APPLY PATCHES%';

```

## See also[​](#see-also "Direct link to See also")


- [Lightweight `UPDATE`](/docs/sql-reference/statements/update) \- Create patch parts with lightweight updates
- [`apply_patches_on_merge` setting](/docs/operations/settings/merge-tree-settings#apply_patches_on_merge) \- Control automatic patch application during merges
[PreviousROLE](/docs/sql-reference/statements/alter/role)[NextROW POLICY](/docs/sql-reference/statements/alter/row-policy)- [When to use APPLY PATCHES](#when-to-use)- [Examples](#examples)- [Monitoring patch application](#monitor)- [See also](#see-also)
Was this page helpful?
