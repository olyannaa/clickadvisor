---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/projection.md)#
topic: projections-clickhouse-docs
ch_version_introduced: '1.5'
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 6
---

EXISTS] name [IN PARTITION partition_name] ``` The commands `ADD`, `DROP` and `CLEAR` are lightweight in the sense that they only change metadata or remove files. Additionally, they are replicated, and sync projection metadata via ClickHouse Keeper or ZooKeeper.

NoteProjection manipulation is supported only for tables with [`*MergeTree`](/docs/engines/table-engines/mergetree-family/mergetree) engine (including [replicated](/docs/engines/table-engines/mergetree-family/replication) variants).

### Controlling projection merge behavior[​](#control-projections-merges "Direct link to Controlling projection merge behavior")

When you execute a query, ClickHouse chooses between reading from the original table or one of its projections.
The decision to read from the original table or one of its projections is made individually per every table part.
ClickHouse generally aims to read as little data as possible and employs a couple of tricks to identify the best part to read from, for example, sampling the primary key of a part.
In some cases, source table parts have no corresponding projection parts.
This can happen, for example, because creating a projection for a table in SQL is “lazy” by default \- it only affects newly inserted data but keeps existing parts unaltered.

As one of the projections already contains the pre\-computed aggregate values, ClickHouse tries to read from the corresponding projection parts to avoid aggregating at query runtime again. If a specific part lacks the corresponding projection part, query execution falls back to the original part.

But what happens if the rows in the original table change in a non\-trivial way by non\-trivial data part background merges?
For example, assume the table is stored using the `ReplacingMergeTree` table engine.
If the same row is detected in multiple input parts during merge, only the most recent row version (from the most recently inserted part) will be kept, while all older versions will be discarded.

Similarly, if the table is stored using the `AggregatingMergeTree` table engine, the merge operation may fold the same rows in the input parts (based on the primary key values) into a single row to update partial aggregation states.

Before ClickHouse v24\.8, projection parts either silently got out of sync with the main data, or certain operations like updates and deletes could not be run at all as the database automatically threw an exception if the table had projections.
