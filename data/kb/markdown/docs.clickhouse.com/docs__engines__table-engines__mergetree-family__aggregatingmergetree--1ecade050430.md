# AggregatingMergeTree table engine \| ClickHouse Docs


- - [Engines](/docs/engines)- [Table Engines](/docs/engines/table-engines)- [MergeTree Family](/docs/engines/table-engines/mergetree-family)- AggregatingMergeTree
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/engines/table-engines/mergetree-family/aggregatingmergetree.md)# AggregatingMergeTree table engine

The engine inherits from [MergeTree](/docs/engines/table-engines/mergetree-family/versionedcollapsingmergetree), altering the logic for data parts merging. ClickHouse replaces all rows with the same primary key (or more accurately, with the same [sorting key](/docs/engines/table-engines/mergetree-family/mergetree)) with a single row (within a single data part) that stores a combination of states of aggregate functions.


You can use `AggregatingMergeTree` tables for incremental data aggregation, including for aggregated materialized views.


You can see an example of how to use the AggregatingMergeTree and Aggregate functions in the below video:



The engine processes all columns with the following types:


- [`AggregateFunction`](/docs/sql-reference/data-types/aggregatefunction)
- [`SimpleAggregateFunction`](/docs/sql-reference/data-types/simpleaggregatefunction)


It is appropriate to use `AggregatingMergeTree` if it reduces the number of rows by orders.


## Creating a table[​](#creating-a-table "Direct link to Creating a table")



```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = AggregatingMergeTree()
[PARTITION BY expr]
[ORDER BY expr]
[SAMPLE BY expr]
[TTL expr]
[SETTINGS name=value, ...]

```

For a description of request parameters, see [request description](/docs/sql-reference/statements/create/table).


**Query clauses**


When creating an `AggregatingMergeTree` table, the same [clauses](/docs/engines/table-engines/mergetree-family/mergetree) are required as when creating a `MergeTree` table.


Deprecated Method for Creating a TableNoteDo not use this method in new projects and, if possible, switch the old projects to the method described above.


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE [=] AggregatingMergeTree(date-column [, sampling_expression], (primary, key), index_granularity)

```
All of the parameters have the same meaning as in `MergeTree`.


## SELECT and INSERT[​](#select-and-insert "Direct link to SELECT and INSERT")


To insert data, use [INSERT SELECT](/docs/sql-reference/statements/insert-into) query with aggregate \-State\- functions.
When selecting data from `AggregatingMergeTree` table, use `GROUP BY` clause and the same aggregate functions as when inserting data, but using the `-Merge` suffix.


In the results of `SELECT` query, the values of `AggregateFunction` type have implementation\-specific binary representation for all of the ClickHouse output formats. For example, if you dump data into `TabSeparated` format with a `SELECT` query, then this dump can be loaded back using an `INSERT` query.


## Example of an aggregated materialized view[​](#example-of-an-aggregated-materialized-view "Direct link to Example of an aggregated materialized view")


The following example assumes that you have a database named `test`. Create it if it doesn't already exist using the command below:



```
CREATE DATABASE test;

```

Now create the table `test.visits` that contains the raw data:



```
CREATE TABLE test.visits
 (
    StartDate DateTime64 NOT NULL,
    CounterID UInt64,
    Sign Nullable(Int32),
    UserID Nullable(Int32)
) ENGINE = MergeTree ORDER BY (StartDate, CounterID);

```

Next, you need an `AggregatingMergeTree` table that will store `AggregationFunction`s that keep track of the total number of visits and the number of unique users.


Create an `AggregatingMergeTree` materialized view that watches the `test.visits` table, and uses the [`AggregateFunction`](/docs/sql-reference/data-types/aggregatefunction) type:



```
CREATE TABLE test.agg_visits (
    StartDate DateTime64 NOT NULL,
    CounterID UInt64,
    Visits AggregateFunction(sum, Nullable(Int32)),
    Users AggregateFunction(uniq, Nullable(Int32))
)
ENGINE = AggregatingMergeTree() ORDER BY (StartDate, CounterID);

```

Create a materialized view that populates `test.agg_visits` from `test.visits`:



```
CREATE MATERIALIZED VIEW test.visits_mv TO test.agg_visits
AS SELECT
    StartDate,
    CounterID,
    sumState(Sign) AS Visits,
    uniqState(UserID) AS Users
FROM test.visits
GROUP BY StartDate, CounterID;

```

Insert data into the `test.visits` table:



```
INSERT INTO test.visits (StartDate, CounterID, Sign, UserID)
 VALUES (1667446031000, 1, 3, 4), (1667446031000, 1, 6, 3);

```

The data is inserted in both `test.visits` and `test.agg_visits`.


To get the aggregated data, execute a query such as `SELECT ... GROUP BY ...` from the materialized view `test.visits_mv`:



```
SELECT
    StartDate,
    sumMerge(Visits) AS Visits,
    uniqMerge(Users) AS Users
FROM test.visits_mv
GROUP BY StartDate
ORDER BY StartDate;

```


```
┌───────────────StartDate─┬─Visits─┬─Users─┐
│ 2022-11-03 03:27:11.000 │      9 │     2 │
└─────────────────────────┴────────┴───────┘

```

Add another couple of records to `test.visits`, but this time try using a different timestamp for one of the records:



```
INSERT INTO test.visits (StartDate, CounterID, Sign, UserID)
 VALUES (1669446031000, 2, 5, 10), (1667446031000, 3, 7, 5);

```

Run the `SELECT` query again, which will return the following output:



```
┌───────────────StartDate─┬─Visits─┬─Users─┐
│ 2022-11-03 03:27:11.000 │     16 │     3 │
│ 2022-11-26 07:00:31.000 │      5 │     1 │
└─────────────────────────┴────────┴───────┘

```

In some cases, you might want to avoid pre\-aggregating rows at insert time to shift the cost of aggregation from insert time
to merge time. Ordinarily, it is necessary to include the columns which are not part of the aggregation in the `GROUP BY`
clause of the materialized view definition to avoid an error. However, you can make use of the [`initializeAggregation`](/docs/sql-reference/functions/other-functions#initializeAggregation)
function with setting `optimize_on_insert = 0` (it is turned on by default) to achieve this. Use of `GROUP BY`
is no longer required in this case:



```
CREATE MATERIALIZED VIEW test.visits_mv TO test.agg_visits
AS SELECT
    StartDate,
    CounterID,
    initializeAggregation('sumState', Sign) AS Visits,
    initializeAggregation('uniqState', UserID) AS Users
FROM test.visits;

```

NoteWhen using `initializeAggregation`, an aggregate state is created for each individual row without grouping.
Each source row produces one row in the materialized view, and the actual aggregation happens later when the
`AggregatingMergeTree` merges parts. This is only true if `optimize_on_insert = 0`.


## Related content[​](#related-content "Direct link to Related content")


- Blog: [Using Aggregate Combinators in ClickHouse](https://clickhouse.com/blog/aggregate-functions-combinators-in-clickhouse-for-arrays-maps-and-states)
[PreviousSummingMergeTree](/docs/engines/table-engines/mergetree-family/summingmergetree)[NextCollapsingMergeTree](/docs/engines/table-engines/mergetree-family/collapsingmergetree)- [Creating a table](#creating-a-table)- [SELECT and INSERT](#select-and-insert)- [Example of an aggregated materialized view](#example-of-an-aggregated-materialized-view)- [Related content](#related-content)
Was this page helpful?
