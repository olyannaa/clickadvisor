---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/operators/in.md)#
topic: in-operators-clickhouse-docs
ch_version_introduced: '0.807696'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 7
---

┌──EventDate─┬────ratio─┐ │ 2014-03-17 │ 1 │ │ 2014-03-18 │ 0.807696 │ │ 2014-03-19 │ 0.755406 │ │ 2014-03-20 │ 0.723218 │ │ 2014-03-21 │ 0.697021 │ │ 2014-03-22 │ 0.647851 │ │ 2014-03-23 │ 0.648416 │ └────────────┴──────────┘ ```

For each day after March 17th, count the percentage of pageviews made by users who visited the site on March 17th.
A subquery in the `IN` clause is always run just one time on a single server. There are no dependent subqueries.

## NULL Processing[​](#null-processing "Direct link to NULL Processing")

During request processing, the `IN` operator assumes that the result of an operation with [NULL](/docs/operations/settings/formats#input_format_null_as_default) always equals `0`, regardless of whether `NULL` is on the right or left side of the operator. `NULL` values are not included in any dataset, do not correspond to each other and cannot be compared if [transform\_null\_in \= 0](/docs/operations/settings/settings#transform_null_in).

Here is an example with the `t_null` table:

```
┌─x─┬────y─┐
│ 1 │ ᴺᵁᴸᴸ │
│ 2 │    3 │
└───┴──────┘

```

Running the query `SELECT x FROM t_null WHERE y IN (NULL,3)` gives you the following result:

```
┌─x─┐
│ 2 │
└───┘

```

You can see that the row in which `y = NULL` is thrown out of the query results. This is because ClickHouse can't decide whether `NULL` is included in the `(NULL,3)` set, returns `0` as the result of the operation, and `SELECT` excludes this row from the final output.

```
SELECT y IN (NULL, 3)
FROM t_null

```

```
┌─in(y, tuple(NULL, 3))─┐
│                     0 │
│                     1 │
└───────────────────────┘

```

## Distributed Subqueries[​](#distributed-subqueries "Direct link to Distributed Subqueries")

There are two options for `IN` operators with subqueries (similar to `JOIN` operators): normal `IN` / `JOIN` and `GLOBAL IN` / `GLOBAL JOIN`. They differ in how they are run for distributed query processing.

NoteRemember that the algorithms described below may work differently depending on the [settings](/docs/operations/settings/settings) `distributed_product_mode` setting.

When using the regular `IN`, the query is sent to remote servers, and each of them runs the subqueries in the `IN` or `JOIN` clause.
