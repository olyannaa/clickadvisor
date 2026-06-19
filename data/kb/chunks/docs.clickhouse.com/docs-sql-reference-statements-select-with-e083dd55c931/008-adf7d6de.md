---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/select/with.md)#
topic: with-clause-clickhouse-docs
ch_version_introduced: '24.3'
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 8
---

[(1,4),(4,5),(5,1),(1,4)] │ │ 4 │ 5 │ 4 -> 5 │ true │ [(4,5),(5,1),(1,4),(4,5)] │ │ 5 │ 1 │ 5 -> 1 │ true │ [(5,1),(1,4),(4,5),(5,1)] │ └──────┴────┴────────┴──────────┴───────────────────────────┘ ``` ### Infinite queries[​](#infinite-queries "Direct link to Infinite queries")

It is also possible to use infinite recursive CTE queries if `LIMIT` is used in outer query:

**Example:** Infinite recursive CTE query

```
WITH RECURSIVE test_table AS (
    SELECT 1 AS number
UNION ALL
    SELECT number + 1 FROM test_table
)
SELECT sum(number) FROM (SELECT number FROM test_table LIMIT 100);

```

```
┌─sum(number)─┐
│        5050 │
└─────────────┘

```

## Trailing Comma[​](#trailing-comma "Direct link to Trailing Comma")

A comma is allowed after the last element in the `WITH` clause:

```
WITH
    (SELECT sum(number) FROM numbers(10)) AS total,
    total * 2 AS doubled,
SELECT total, doubled;

```
[PreviousWHERE](/docs/sql-reference/statements/select/where)[NextINSERT INTO](/docs/sql-reference/statements/insert-into)- [Common Table Expressions](#common-table-expressions)
	- [Syntax](#common-table-expressions-syntax)- [Example](#common-table-expressions-example)- [Materialized Common Table Expressions](#materialized-common-table-expressions)
	- [Syntax](#materialized-common-table-expressions-syntax)- [When to use](#materialized-cte-when-to-use)- [Examples](#materialized-common-table-expressions-examples)- [Restrictions](#materialized-cte-restrictions)- [Common Scalar Expressions](#common-scalar-expressions)
	- [Syntax](#common-scalar-expressions-syntax)- [Examples](#common-scalar-expressions-examples)- [Recursive Queries](#recursive-queries)
	- [Search order](#search-order)- [Cycle detection](#cycle-detection)- [Infinite queries](#infinite-queries)- [Trailing Comma](#trailing-comma)
Was this page helpful?
