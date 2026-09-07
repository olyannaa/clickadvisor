---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-joins-under-the-hood-full-sorting-merge-join-partial-merge-join-mergingsortedtransform-clickhouse
ch_version_introduced: '11.559'
last_updated: '2026-09-07'
chunk_index: 16
total_chunks_in_doc: 27
---

a `CreatingSetsOnTheFlyTransform` stage, indicating that the in\-memory set containing the (unique) join key column values of the right table couldn’t be built because the number of entries would exceed the configured threshold of 200000 for the `max_rows_in_set_to_optimize_join` setting.

Another entry for a `CreatingSetsOnTheFlyTransform` stage shows that the set containing the (unique) join key column values of the left table could be built successfully. This set is used for filtering rows from the right table as indicated by 30 entries (we only show the first two and omit the rest) for the `FilterBySetOnTheFlyTransform` stage. 30, because ClickHouse streams rows from the right table with 30 parallel stream stages and uses 30 parallel `FilterBySetOnTheFlyTransform` stages for filtering the 30 streams.

#### Utilizing physical row order \#

If the [physical row order](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes#data-is-stored-on-disk-ordered-by-primary-key-columns) of one or both joined tables matches the join key sort order, then the sorting phase of the full sorting merge join algorithm will be skipped for the corresponding table(s).

We can validate this by introspecting the query pipeline for a join query using join keys matching the sorting keys of both tables. First we check the sorting keys from the two joined tables:

```
1SELECT
2    name AS table,
3    sorting_key
4FROM system.tables
5WHERE database = 'imdb_large';
6
7
8┌─table───────┬─sorting_key───────────────────────┐
9│ actors      │ id, first_name, last_name, gender │
10│ roles       │ actor_id, movie_id                │
11└─────────────┴───────────────────────────────────┘
```
Copy command
We use a join query that finds all roles for each actor, by joining the two example tables by `id` for the `actors` table and by `actor_id` for the roles table. These join keys are prefixes of the sorting keys of the tables, allowing ClickHouse to skip the sorting stage of the full sorting merge algorithm by reading the rows from both tables in the order they are stored on disk.

We introspect the query pipeline for this query:

```
1clickhouse client --host ekyyw56ard.us-west-2.aws.clickhouse.cloud --secure --port 9440 --password <PASSWORD> --database=imdb_large --query "
2EXPLAIN pipeline graph=1, compact=0
3SELECT *
4FROM actors AS a
5JOIN roles AS r ON a.id = r.actor_id
6SETTINGS max_threads = 2, join_algorithm = 'full_sorting_merge', max_rows_in_set_to_optimize_join = 0, max_bytes_before_external_sort = '100M';" | dot -Tpdf > pipeline.pdf
```
Copy command
![full_sorting_merge_5.png](/_next/image?url=%2Fuploads%2Ffull_sorting_merge_5_735b527fb6.png&w=2048&q=75)
