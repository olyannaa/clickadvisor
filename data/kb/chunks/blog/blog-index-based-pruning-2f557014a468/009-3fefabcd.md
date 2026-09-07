---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Index\-based
topic: index-based-pruning-in-clickhouse-clickhouse
ch_version_introduced: '5.366'
last_updated: '2026-09-07'
chunk_index: 9
total_chunks_in_doc: 17
---

optimize_use_projections = 1; ``` Copy command `optimize_use_projections` is enabled by default, but we included it here for completeness. If you turn it off, projections won’t be used. It’s useful for sanity checking that your projection is actually working!

The timings of running the above query are shown below:

```
110 rows in set. Elapsed: 0.023 sec.
2
310 rows in set. Elapsed: 0.056 sec.
4
510 rows in set. Elapsed: 0.046 sec.
```
Copy command
For the `BURNLEY` query, using a lightweight projection on the `district` column reduces the query time from 428 milliseconds to 23 milliseconds, a 94% improvement.

Let’s now have a look at what’s going on under the hood. I initially prefixed the query with the same explain clause that we used earlier:

```
1EXPLAIN indexes=1, pretty=1, compact= 1 
2SELECT town, count(), round(avg(price)) AS avgPrice, argAndMax(date, price)
3FROM uk_price_paid
4WHERE district = 'BURNLEY'
5GROUP BY ALL
6ORDER BY count() DESC LIMIT 10
7SETTINGS
8    use_query_condition_cache = 0,
9    optimize_use_projections = 1;
```
Copy command

```
1┌─explain─────────────────────────────────────────────────┐
2│ Output: town, count(), avgPrice, argAndMax(date, price) │
3│                                                         │
4│ Limit (preliminary LIMIT)                               │
5│ └──Sorting (Sorting for ORDER BY)                       │
6│    └──Aggregating                                       │
7│       └──ReadFromMergeTree (default.uk_price_paid)      │
8│             Indexes:                                    │
9│               PrimaryKey                                │
10│                 Condition: true                         │
11│                 Parts: 6/6                              │
12│                 Granules: 29741/29741                   │
13│               Ranges: 6                                 │
14└─────────────────────────────────────────────────────────┘
```
Copy command
This output doesn’t help us as it only includes the base query plan with the primary key index information. We need to also add `projections=1` so that projection analysis is included in the output:

```
1EXPLAIN indexes=1, projections=1, pretty=1, compact= 1 
2SELECT town, count(), round(avg(price)) AS avgPrice, argAndMax(date, price)
3FROM uk_price_paid
4WHERE district = 'BURNLEY'
5GROUP BY ALL
6ORDER BY count() DESC LIMIT 10
7SETTINGS
8    use_query_condition_cache = 0,
9    optimize_use_projections = 1,
10    output_format_pretty_max_value_width=65,
11    output_format_pretty_row_numbers=1;
```
Copy command
