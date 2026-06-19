---
source: blog
url: https://clickhouse.cloud/signUp?loc=blog-cta-header&utm_source=clickhouse&utm_medium=web&utm_campaign=blog
topic: clickhouse-joins-under-the-hood-full-sorting-merge-join-partial-merge-join-mergingsortedtransform
ch_version_introduced: '11.559'
last_updated: '2026-06-12'
chunk_index: 14
total_chunks_in_doc: 23
---

only show the first two and omit the rest) for the `FilterBySetOnTheFlyTransform` stage. 30, because ClickHouse streams rows from the right table with 30 parallel stream stages and uses 30 parallel `FilterBySetOnTheFlyTransform` stages for filtering the 30 streams.

#### Utilizing physical row order [\#](/blog/clickhouse-fully-supports-joins-full-sort-partial-merge-part3#utilizing-physical-row-order)

If the [physical row order](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes#data-is-stored-on-disk-ordered-by-primary-key-columns) of one or both joined tables matches the join key sort order, then the sorting phase of the full sorting merge join algorithm will be skipped for the corresponding table(s).

We can validate this by introspecting the query pipeline for a join query using join keys matching the sorting keys of both tables. First we check the sorting keys from the two joined tables:

```
SELECT
    name AS table,
    sorting_key
FROM system.tables
WHERE database = 'imdb_large';


┌─table───────┬─sorting_key───────────────────────┐
│ actors      │ id, first_name, last_name, gender │
│ roles       │ actor_id, movie_id                │
└─────────────┴───────────────────────────────────┘

```

We use a join query that finds all roles for each actor, by joining the two example tables by `id` for the `actors` table and by `actor_id` for the roles table. These join keys are prefixes of the sorting keys of the tables, allowing ClickHouse to skip the sorting stage of the full sorting merge algorithm by reading the rows from both tables in the order they are stored on disk.

We introspect the query pipeline for this query:

```
clickhouse client --host ekyyw56ard.us-west-2.aws.clickhouse.cloud --secure --port 9440 --password <PASSWORD> --database=imdb_large --query "
EXPLAIN pipeline graph=1, compact=0
SELECT *
FROM actors AS a
JOIN roles AS r ON a.id = r.actor_id
SETTINGS max_threads = 2, join_algorithm = 'full_sorting_merge', max_rows_in_set_to_optimize_join = 0, max_bytes_before_external_sort = '100M';" | dot -Tpdf > pipeline.pdf

```

![full_sorting_merge_5.png](/uploads/full_sorting_merge_5_735b527fb6.png)
We see that the query pipeline ① ② starts with two parallel stream stages per table (because max\_threads is set to 2\) that stream the rows block\-wise from the two tables **in order** into the query engine.

Note how sort and spill stages are missing. The already sorted blocks are merge\-sorted per table and ③ join matches are identified by merging (interleaved scanning) the two sorted streams.
