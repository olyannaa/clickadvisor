# Projections \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [ALTER](/docs/sql-reference/statements/alter)- PROJECTION
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/projection.md)# Projections

This page discusses what projections are, how you can use them and various options for manipulating projections.


## Overview of projections[​](#overview "Direct link to Overview of projections")


Projections store data in a format that optimizes query execution, this feature is useful for:


- Running queries on a column that is not a part of the primary key
- Pre\-aggregating columns, it will reduce both computation and IO


You can define one or more projections for a table, and during the query analysis the projection with the least data to scan will be selected by ClickHouse without modifying the query provided by the user.


Disk usageProjections will create internally a new hidden table, this means that more IO and space on disk will be required.
For example, if the projection has defined a different primary key, all the data from the original table will be duplicated.


You can see more technical details about how projections work internally on this [page](/docs/guides/best-practices/sparse-primary-indexes#option-3-projections).


## Using projections[​](#examples "Direct link to Using projections")


### Example filtering without using primary keys[​](#example-filtering-without-using-primary-keys "Direct link to Example filtering without using primary keys")


Creating the table:



```
CREATE TABLE visits_order
(
   `user_id` UInt64,
   `user_name` String,
   `pages_visited` Nullable(Float64),
   `user_agent` String
)
ENGINE = MergeTree()
PRIMARY KEY user_agent

```

Using `ALTER TABLE`, we could add the Projection to an existing table:



```
ALTER TABLE visits_order ADD PROJECTION user_name_projection (
    SELECT *
    ORDER BY user_name
)

ALTER TABLE visits_order MATERIALIZE PROJECTION user_name_projection

```

Inserting the data:



```
INSERT INTO visits_order SELECT
    number,
    'test',
    1.5 * (number / 2),
    'Android'
FROM numbers(1, 100);

```

The Projection will allow us to filter by `user_name` fast even if in the original Table `user_name` was not defined as a `PRIMARY_KEY`.
At query time, ClickHouse determines that less data will be processed if the projection is used, as the data is ordered by `user_name`.



```
SELECT
    *
FROM visits_order
WHERE user_name='test'
LIMIT 2

```

To verify that a query is using the projection, we could review the `system.query_log` table. On the `projections` field we have the name of the projection used or empty if none has been used:



```
SELECT query, projections FROM system.query_log WHERE query_id='<query_id>'

```

### Example pre\-aggregation query[​](#example-pre-aggregation-query "Direct link to Example pre-aggregation query")


Create the table with projection `projection_visits_by_user`:



```
CREATE TABLE visits
(
   `user_id` UInt64,
   `user_name` String,
   `pages_visited` Nullable(Float64),
   `user_agent` String,
   PROJECTION projection_visits_by_user
   (
       SELECT
           user_agent,
           sum(pages_visited)
       GROUP BY user_id, user_agent
   )
)
ENGINE = MergeTree()
ORDER BY user_agent

```

Insert the data:



```
INSERT INTO visits SELECT
    number,
    'test',
    1.5 * (number / 2),
    'Android'
FROM numbers(1, 100);

```


```
INSERT INTO visits SELECT
    number,
    'test',
    1. * (number / 2),
   'IOS'
FROM numbers(100, 500);

```

Execute a first query with `GROUP BY` using the field `user_agent`.
This query will not use the projection defined as the pre\-aggregation does not match.



```
SELECT
    user_agent,
    count(DISTINCT user_id)
FROM visits
GROUP BY user_agent

```

To make use of the projection you can execute queries that select part of, or all of the pre\-aggregation and `GROUP BY` fields:



```
SELECT
    user_agent
FROM visits
WHERE user_id > 50 AND user_id < 150
GROUP BY user_agent

```


```
SELECT
    user_agent,
    sum(pages_visited)
FROM visits
GROUP BY user_agent

```

As previously mentioned, you can review the `system.query_log` table to understand if a projection was used.
The `projections` field shows the name of the projection used.
It will be empty if no projection has been used:



```
SELECT query, projections FROM system.query_log WHERE query_id='<query_id>'

```

### Creating and using projection indexes[​](#projection-indexes "Direct link to Creating and using projection indexes")


Creating a [projection index](/docs/engines/table-engines/mergetree-family/mergetree#projection-index):



```
CREATE TABLE events
(
    `event_time` DateTime,
    `event_id` UInt64,
    `user_id` UInt64,
    `huge_string` String,
    PROJECTION order_by_user_id INDEX user_id TYPE basic
)
ENGINE = MergeTree()
ORDER BY (event_id);

```

Creating a projection with explicit `_part_offset` fieldProjection indexes can alternatively be created using the following syntax (not recommended):
```
CREATE TABLE events
(
    `event_time` DateTime,
    `event_id` UInt64,
    `user_id` UInt64,
    `huge_string` String,
    PROJECTION order_by_user_id
    (
        SELECT
            _part_offset
        ORDER BY user_id
    )
)
ENGINE = MergeTree()
ORDER BY (event_id);

```



Inserting some sample data:



```
INSERT INTO events SELECT * FROM generateRandom() LIMIT 100000;

```

The `_part_offset` field preserves its value through merges and mutations, making it valuable for secondary indexing. We can leverage this in queries:



```
SELECT
    count()
FROM events
WHERE _part_starting_offset + _part_offset IN (
    SELECT _part_starting_offset + _part_offset
    FROM events
    WHERE user_id = 42
)
SETTINGS enable_shared_storage_snapshot_in_query = 1

```

## Manipulating projections[​](#manipulating-projections "Direct link to Manipulating projections")


The following operations with [projections](/docs/engines/table-engines/mergetree-family/mergetree#projections) are available:


### ADD PROJECTION[​](#add-projection "Direct link to ADD PROJECTION")


Use the statement below to add a projection description to a tables metadata:



```
ALTER TABLE [db.]name [ON CLUSTER cluster] ADD PROJECTION [IF NOT EXISTS] name ( SELECT <COLUMN LIST EXPR> [GROUP BY] [ORDER BY] ) [WITH SETTINGS ( setting_name1 = setting_value1, setting_name2 = setting_value2, ...)]

```

#### `WITH SETTINGS` Clause[​](#with-settings "Direct link to with-settings")


`WITH SETTINGS` defines **projection\-level settings**, which customize how the projection stores data (for example, `index_granularity` or `index_granularity_bytes`).
These correspond directly to **MergeTree table settings**, but apply **only to this projection**.


Example:



```
ALTER TABLE t
ADD PROJECTION p (
    SELECT x ORDER BY x
) WITH SETTINGS (
    index_granularity = 4096,
    index_granularity_bytes = 1048576
);

```

Projection settings override the effective table settings for the projection, subject to validation rules (e.g., invalid or incompatible overrides will be rejected).


### DROP PROJECTION[​](#drop-projection "Direct link to DROP PROJECTION")


Use the statement below to remove a projection description from a tables metadata and delete projection files from disk.
This is implemented as a [mutation](/docs/sql-reference/statements/alter#mutations).



```
ALTER TABLE [db.]name [ON CLUSTER cluster] DROP PROJECTION [IF EXISTS] name

```

### MATERIALIZE PROJECTION[​](#materialize-projection "Direct link to MATERIALIZE PROJECTION")


Use the statement below to rebuild the projection `name` in partition `partition_name`.
This is implemented as a [mutation](/docs/sql-reference/statements/alter#mutations).



```
ALTER TABLE [db.]table [ON CLUSTER cluster] MATERIALIZE PROJECTION [IF EXISTS] name [IN PARTITION partition_name]

```

### CLEAR PROJECTION[​](#clear-projection "Direct link to CLEAR PROJECTION")


Use the statement below to delete projection files from disk without removing description.
This is implemented as a [mutation](/docs/sql-reference/statements/alter#mutations).



```
ALTER TABLE [db.]table [ON CLUSTER cluster] CLEAR PROJECTION [IF EXISTS] name [IN PARTITION partition_name]

```

The commands `ADD`, `DROP` and `CLEAR` are lightweight in the sense that they only change metadata or remove files.
Additionally, they are replicated, and sync projection metadata via ClickHouse Keeper or ZooKeeper.


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


Since v24\.8, a new table\-level setting [`deduplicate_merge_projection_mode`](/docs/operations/settings/merge-tree-settings#deduplicate_merge_projection_mode) controls the behavior if the aforementioned non\-trivial background merge operations occur in parts of the original table.


Delete mutations are another example of part merge operations that drop rows in the parts of the original table. Since v24\.7, we also have a setting to control the behavior w.r.t. delete mutations triggered by lightweight deletes: [`lightweight_mutation_projection_mode`](/docs/operations/settings/merge-tree-settings#deduplicate_merge_projection_mode).


Below are the possible values for both `deduplicate_merge_projection_mode` and `lightweight_mutation_projection_mode`:


- `throw` (default): An exception is thrown, preventing projection parts from going out of sync.
- `drop`: Affected projection table parts are dropped. Queries will fall back to the original table part for affected projection parts.
- `rebuild`: The affected projection part is rebuilt to stay consistent with data in the original table part.


## Limitations[​](#limitations "Direct link to Limitations")


It is not possible to use an `ALIAS` column in a projection's `ORDER BY` clause. For example:



```
CREATE TABLE t
(
    id UInt64,
    a UInt32,
    ab_sum UInt64 ALIAS a + 1,
--highlight-next-line
    PROJECTION p (SELECT a ORDER BY ab_sum)
)
ENGINE = MergeTree ORDER BY id;
-- Fails with UNKNOWN_IDENTIFIER

```

`ALIAS` columns are not physically stored and are computed on\-the\-fly at query time, so they are unavailable during the projection part write path when the sorting expression is evaluated.


Instead, use `MATERIALIZED` columns or inline the expression directly:



```
-- using MATERIALIZED column
CREATE TABLE t
(
    id UInt64,
    a UInt32,
    ab_sum UInt64 MATERIALIZED a + 1,
    PROJECTION p (SELECT a ORDER BY ab_sum)
)
ENGINE = MergeTree ORDER BY id;

-- using an inline expression
CREATE TABLE t
(
    id UInt64,
    a UInt32,
    PROJECTION p (SELECT a ORDER BY a + 1)
)
ENGINE = MergeTree ORDER BY id;

```

## See also[​](#see-also "Direct link to See also")


- ["Control Of Projections During Merges" (blog post)](https://clickhouse.com/blog/clickhouse-release-24-08#control-of-projections-during-merges)
- ["Projections" (guide)](/docs/data-modeling/projections#using-projections-to-speed-up-UK-price-paid)
- ["Materialized Views versus Projections"](https://clickhouse.com/docs/managing-data/materialized-views-versus-projections)
[PreviousSETTINGS PROFILE](/docs/sql-reference/statements/alter/settings-profile)[NextVIEW](/docs/sql-reference/statements/alter/view)- [Overview of projections](#overview)- [Using projections](#examples)
	- [Example filtering without using primary keys](#example-filtering-without-using-primary-keys)- [Example pre\-aggregation query](#example-pre-aggregation-query)- [Creating and using projection indexes](#projection-indexes)- [Manipulating projections](#manipulating-projections)
	- [ADD PROJECTION](#add-projection)- [DROP PROJECTION](#drop-projection)- [MATERIALIZE PROJECTION](#materialize-projection)- [CLEAR PROJECTION](#clear-projection)- [Controlling projection merge behavior](#control-projections-merges)- [Limitations](#limitations)- [See also](#see-also)
Was this page helpful?
