# FROM Clause \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [SELECT](/docs/sql-reference/statements/select)- FROM
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/select/from.md)# FROM Clause

The `FROM` clause specifies the source to read data from:


- [Table](/docs/engines/table-engines)
- [Subquery](/docs/sql-reference/statements/select)
- [Table function](/docs/sql-reference/table-functions)


[JOIN](/docs/sql-reference/statements/select/join) and [ARRAY JOIN](/docs/sql-reference/statements/select/array-join) clauses may also be used to extend the functionality of the `FROM` clause.


Subquery is another `SELECT` query that may be specified in parenthesis inside `FROM` clause.


A SQL standard `VALUES` clause can also be used as a table expression:



```
SELECT * FROM (VALUES (1, 'a'), (2, 'b'), (3, 'c')) AS t(id, val);

```

See [Values table function](/docs/sql-reference/table-functions/values#sql-standard-values-clause) for more details.


The `FROM` can contain multiple data sources, separated by commas, which is equivalent of performing [CROSS JOIN](/docs/sql-reference/statements/select/join) on them.


`FROM` can optionally appear before a `SELECT` clause. This is a ClickHouse\-specific extension of standard SQL which makes `SELECT` statements easier to read. Example:



```
FROM table
SELECT *

```

## FINAL Modifier[​](#final-modifier "Direct link to FINAL Modifier")


When `FINAL` is specified, ClickHouse fully merges the data before returning the result. This also performs all data transformations that happen during merges for the given table engine.


It is applicable when selecting data from tables using the following table engines:


- `ReplacingMergeTree`
- `SummingMergeTree`
- `AggregatingMergeTree`
- `CollapsingMergeTree`
- `VersionedCollapsingMergeTree`


`SELECT` queries with `FINAL` are executed in parallel. The [max\_final\_threads](/docs/operations/settings/settings#max_final_threads) setting limits the number of threads used.


### Drawbacks[​](#drawbacks "Direct link to Drawbacks")


Queries that use `FINAL` execute slightly slower than similar queries that do not use `FINAL` because:


- Data is merged during query execution.
- Queries with `FINAL` may read primary key columns in addition to the columns specified in the query.


`FINAL` requires additional compute and memory resources because the processing that normally would occur at merge time must occur in memory at the time of the query. However, using FINAL is sometimes necessary in order to produce accurate results (as data may not yet be fully merged). It is less expensive than running `OPTIMIZE` to force a merge.


As an alternative to using `FINAL`, it is sometimes possible to use different queries that assume the background processes of the `MergeTree` engine have not yet occurred and deal with it by applying an aggregation (for example, to discard duplicates). If you need to use `FINAL` in your queries in order to get the required results, it is okay to do so but be aware of the additional processing required.


`FINAL` can be applied automatically using [FINAL](/docs/operations/settings/settings#final) setting to all tables in a query using a session or a user profile.


### Example Usage[​](#example-usage "Direct link to Example Usage")


Using the `FINAL` keyword



```
SELECT x, y FROM mytable FINAL WHERE x > 1;

```

Using `FINAL` as a query\-level setting



```
SELECT x, y FROM mytable WHERE x > 1 SETTINGS final = 1;

```

Using `FINAL` as a session\-level setting



```
SET final = 1;
SELECT x, y FROM mytable WHERE x > 1;

```

## Implementation Details[​](#implementation-details "Direct link to Implementation Details")


If the `FROM` clause is omitted, data will be read from the `system.one` table.
The `system.one` table contains exactly one row (this table fulfills the same purpose as the DUAL table found in other DBMSs).


To execute a query, all the columns listed in the query are extracted from the appropriate table. Any columns not needed for the external query are thrown out of the subqueries.
If a query does not list any columns (for example, `SELECT count() FROM t`), some column is extracted from the table anyway (the smallest one is preferred), in order to calculate the number of rows.

[PreviousFORMAT](/docs/sql-reference/statements/select/format)[NextGROUP BY](/docs/sql-reference/statements/select/group-by)- [FINAL Modifier](#final-modifier)
	- [Drawbacks](#drawbacks)- [Example Usage](#example-usage)- [Implementation Details](#implementation-details)
Was this page helpful?
