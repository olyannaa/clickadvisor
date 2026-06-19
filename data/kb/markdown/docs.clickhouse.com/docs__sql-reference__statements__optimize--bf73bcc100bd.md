# OPTIMIZE Statement \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- OPTIMIZE
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/optimize.md)# OPTIMIZE Statement

This query tries to initialize an unscheduled merge of data parts for tables. Note that we generally recommend against using `OPTIMIZE TABLE ... FINAL` (see these [docs](/docs/optimize/avoidoptimizefinal)) as its use case is meant for administration, not for daily operations.


Note`OPTIMIZE` can't fix the `Too many parts` error.


**Syntax**



```
OPTIMIZE TABLE [db.]name [ON CLUSTER cluster] [PARTITION partition | PARTITION ID 'partition_id'] [FINAL | FORCE] [DEDUPLICATE [BY expression]]

```


```
OPTIMIZE TABLE [db.]name DRY RUN PARTS 'part_name1', 'part_name2' [, ...] [DEDUPLICATE [BY expression]] [CLEANUP]

```

The `OPTIMIZE` query is supported for [MergeTree](/docs/engines/table-engines/mergetree-family/mergetree) family (including [materialized views](/docs/sql-reference/statements/create/view#materialized-view)) and the [Buffer](/docs/engines/table-engines/special/buffer) engines. Other table engines aren't supported.


When `OPTIMIZE` is used with the [ReplicatedMergeTree](/docs/engines/table-engines/mergetree-family/replication) family of table engines, ClickHouse creates a task for merging and waits for execution on all replicas (if the [alter\_sync](/docs/operations/settings/settings#alter_sync) setting is set to `2`) or on current replica (if the [alter\_sync](/docs/operations/settings/settings#alter_sync) setting is set to `1`).


- If `OPTIMIZE` does not perform a merge for any reason, it does not notify the client. To enable notifications, use the [optimize\_throw\_if\_noop](/docs/operations/settings/settings#optimize_throw_if_noop) setting.
- If you specify a `PARTITION`, only the specified partition is optimized. [How to set partition expression](/docs/sql-reference/statements/alter/partition#how-to-set-partition-expression).
- If you specify `FINAL` or `FORCE`, optimization is performed even when all the data is already in one part. You can control this behaviour with [optimize\_skip\_merged\_partitions](/docs/operations/settings/settings#optimize_skip_merged_partitions). Also, the merge is forced even if concurrent merges are performed.
- If you specify `DEDUPLICATE`, then completely identical rows (unless by\-clause is specified) will be deduplicated (all columns are compared), it makes sense only for the MergeTree engine.


You can specify how long (in seconds) to wait for inactive replicas to execute `OPTIMIZE` queries by the [replication\_wait\_for\_inactive\_replica\_timeout](/docs/operations/settings/settings#replication_wait_for_inactive_replica_timeout) setting.


NoteIf the `alter_sync` is set to `2` and some replicas are not active for more than the time, specified by the `replication_wait_for_inactive_replica_timeout` setting, then an exception `UNFINISHED` is thrown.


## DRY RUN[​](#dry-run "Direct link to DRY RUN")


The `DRY RUN` clause simulates a merge of the specified parts without committing the result. The merged part is written to a temporary location, validated, and then discarded. The original parts and table data remain unchanged.


This is useful for:


- Testing merge correctness across ClickHouse versions.
- Reproducing merge\-related bugs deterministically.
- Benchmarking merge performance.


`DRY RUN` is only supported for [MergeTree](/docs/engines/table-engines/mergetree-family/mergetree) family tables. The `PARTS` keyword with a list of part names is required. All specified parts must exist, be active, and belong to the same partition.


`DRY RUN` is incompatible with `FINAL` and `PARTITION`. It can be combined with `DEDUPLICATE` (with optional column specification) and `CLEANUP` (for `ReplacingMergeTree` tables).


**Syntax**



```
OPTIMIZE TABLE [db.]name DRY RUN PARTS 'part_name1', 'part_name2' [, ...] [DEDUPLICATE [BY expression]] [CLEANUP]

```

By default, the resulting merged part is validated in a way similar to [`CHECK TABLE`](/docs/sql-reference/statements/check-table) query. This behavior is controlled by the [optimize\_dry\_run\_check\_part](/docs/operations/settings/settings#optimize_dry_run_check_part) setting (enabled by default). Disabling it skips validation, which can be useful for benchmarking the merge itself.


**Example**



```
CREATE TABLE dry_run_example (key UInt64, value String) ENGINE = MergeTree ORDER BY key;

INSERT INTO dry_run_example VALUES (1, 'a'), (2, 'b');
INSERT INTO dry_run_example VALUES (1, 'c'), (4, 'd');

-- Simulate merging using two parts
OPTIMIZE TABLE dry_run_example DRY RUN PARTS 'all_1_1_0', 'all_2_2_0';

-- Simulate merging with deduplication
OPTIMIZE TABLE dry_run_example DRY RUN PARTS 'all_1_1_0', 'all_2_2_0' DEDUPLICATE;

-- Parts and data remain unchanged after DRY RUN
SELECT name, rows FROM system.parts
WHERE database = currentDatabase() AND table = 'dry_run_example' AND active
ORDER BY name;

```


```
┌─name────────┬─rows─┐
│ all_1_1_0   │    2 │
│ all_2_2_0   │    2 │
└─────────────┴──────┘

```

## BY expression[​](#by-expression "Direct link to BY expression")


If you want to perform deduplication on custom set of columns rather than on all, you can specify list of columns explicitly or use any combination of [`*`](/docs/sql-reference/statements/select#asterisk), [`COLUMNS`](/docs/sql-reference/statements/select#select-clause) or [`EXCEPT`](/docs/sql-reference/statements/select/except-modifier) expressions. The explicitly written or implicitly expanded list of columns must include all columns specified in row ordering expression (both primary and sorting keys) and partitioning expression (partitioning key).


NoteNotice that `*` behaves just like in `SELECT`: [MATERIALIZED](/docs/sql-reference/statements/create/view#materialized-view) and [ALIAS](/docs/sql-reference/statements/create/table#alias) columns are not used for expansion.Also, it is an error to specify empty list of columns, or write an expression that results in an empty list of columns, or deduplicate by an `ALIAS` column.




**Syntax**



```
OPTIMIZE TABLE table DEDUPLICATE; -- all columns
OPTIMIZE TABLE table DEDUPLICATE BY *; -- excludes MATERIALIZED and ALIAS columns
OPTIMIZE TABLE table DEDUPLICATE BY colX,colY,colZ;
OPTIMIZE TABLE table DEDUPLICATE BY * EXCEPT colX;
OPTIMIZE TABLE table DEDUPLICATE BY * EXCEPT (colX, colY);
OPTIMIZE TABLE table DEDUPLICATE BY COLUMNS('column-matched-by-regex');
OPTIMIZE TABLE table DEDUPLICATE BY COLUMNS('column-matched-by-regex') EXCEPT colX;
OPTIMIZE TABLE table DEDUPLICATE BY COLUMNS('column-matched-by-regex') EXCEPT (colX, colY);

```

**Examples**


Consider the table:



```
CREATE TABLE example (
    primary_key Int32,
    secondary_key Int32,
    value UInt32,
    partition_key UInt32,
    materialized_value UInt32 MATERIALIZED 12345,
    aliased_value UInt32 ALIAS 2,
    PRIMARY KEY primary_key
) ENGINE=MergeTree
PARTITION BY partition_key
ORDER BY (primary_key, secondary_key);

```


```
INSERT INTO example (primary_key, secondary_key, value, partition_key)
VALUES (0, 0, 0, 0), (0, 0, 0, 0), (1, 1, 2, 2), (1, 1, 2, 3), (1, 1, 3, 3);

```


```
SELECT * FROM example;

```


```

┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           0 │             0 │     0 │             0 │
│           0 │             0 │     0 │             0 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             2 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             3 │
│           1 │             1 │     3 │             3 │
└─────────────┴───────────────┴───────┴───────────────┘

```

All following examples are executed against this state with 5 rows.


#### `DEDUPLICATE`[​](#deduplicate "Direct link to deduplicate")


When columns for deduplication are not specified, all of them are taken into account. The row is removed only if all values in all columns are equal to corresponding values in the previous row:



```
OPTIMIZE TABLE example FINAL DEDUPLICATE;

```


```
SELECT * FROM example;

```


```
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             2 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           0 │             0 │     0 │             0 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             3 │
│           1 │             1 │     3 │             3 │
└─────────────┴───────────────┴───────┴───────────────┘

```

#### `DEDUPLICATE BY *`[​](#deduplicate-by- "Direct link to deduplicate-by-")


When columns are specified implicitly, the table is deduplicated by all columns that are not `ALIAS` or `MATERIALIZED`. Considering the table above, these are `primary_key`, `secondary_key`, `value`, and `partition_key` columns:



```
OPTIMIZE TABLE example FINAL DEDUPLICATE BY *;

```


```
SELECT * FROM example;

```


```
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             2 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           0 │             0 │     0 │             0 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             3 │
│           1 │             1 │     3 │             3 │
└─────────────┴───────────────┴───────┴───────────────┘

```

#### `DEDUPLICATE BY * EXCEPT`[​](#deduplicate-by--except "Direct link to deduplicate-by--except")


Deduplicate by all columns that are not `ALIAS` or `MATERIALIZED` and explicitly not `value`: `primary_key`, `secondary_key`, and `partition_key` columns.



```
OPTIMIZE TABLE example FINAL DEDUPLICATE BY * EXCEPT value;

```


```
SELECT * FROM example;

```


```
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             2 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           0 │             0 │     0 │             0 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             3 │
└─────────────┴───────────────┴───────┴───────────────┘

```

#### `DEDUPLICATE BY <list of columns>`[​](#deduplicate-by-list-of-columns "Direct link to deduplicate-by-list-of-columns")


Deduplicate explicitly by `primary_key`, `secondary_key`, and `partition_key` columns:



```
OPTIMIZE TABLE example FINAL DEDUPLICATE BY primary_key, secondary_key, partition_key;

```


```
SELECT * FROM example;

```


```
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             2 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           0 │             0 │     0 │             0 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             3 │
└─────────────┴───────────────┴───────┴───────────────┘

```

#### `DEDUPLICATE BY COLUMNS(<regex>)`[​](#deduplicate-by-columnsregex "Direct link to deduplicate-by-columnsregex")


Deduplicate by all columns matching a regex: `primary_key`, `secondary_key`, and `partition_key` columns:



```
OPTIMIZE TABLE example FINAL DEDUPLICATE BY COLUMNS('.*_key');

```


```
SELECT * FROM example;

```


```
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           0 │             0 │     0 │             0 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             2 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             3 │
└─────────────┴───────────────┴───────┴───────────────┘

```
[PreviousKILL](/docs/sql-reference/statements/kill)[NextRENAME](/docs/sql-reference/statements/rename)- [DRY RUN](#dry-run)- [BY expression](#by-expression)
Was this page helpful?
