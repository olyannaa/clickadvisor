---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Change
topic: change-data-capture-cdc-with-postgresql-and-clickhouse-part-1-clickhouse
ch_version_introduced: '214354.531780374791'
last_updated: '2026-09-07'
chunk_index: 14
total_chunks_in_doc: 19
---

clause is also set to the same value if not specified.** This clause configures the associated [sparse primary index](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes#introduction). The `ORDER BY` must include the `PRIMARY KEY` as a prefix, as the latter assumes the data is sorted.

For performance, this primary index is held in memory with a [level of indirection using marks to minimize](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes#mark-files-are-used-for-locating-granules) size. The use of the `ORDER BY` key for deduplication in the ReplacingMergeTree can cause this to become long, increasing memory usage. If this becomes a concern, users can specify the `PRIMARY KEY` directly, restricting those columns loaded into memory while preserving the `ORDER BY` to maximize compression and enforce uniqueness.

Using this approach, the Postgres primary key columns can be omitted from the `PRIMARY KEY` \- saving memory without impacting query performance. We also apply this to our example above.

### Querying in ClickHouse \#

At [merge time](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree), the ReplacingMergeTree identifies duplicate rows, using the `ORDER BY` values as a unique identifier, and either retains only the highest version or removes all duplicates if the latest version indicates a delete (pending the resolution of the earlier [noted issue](https://github.com/ClickHouse/ClickHouse/issues/50346)\_. This, however, offers eventual correctness only \- it does not guarantee rows will be deduplicated, and you should not rely on it. Queries can therefore produce incorrect answers due to `update` and `delete` rows being considered in queries.

To obtain correct answers, users will need to complement background merges with query time deduplication and deletion removal. This can be achieved using the FINAL operator. Consider the following examples using the [UK property prices dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid).

```
1postgres=> select count(*) FROM uk_price_paid;
2  count
3----------
4 27735104
5(1 row)
6
7postgres=> SELECT avg(price) FROM uk_price_paid;
8     	avg
9---------------------
10 214354.531780374791
11(1 row)
12
13– no FINAL, incorrect result
14SELECT count()
15FROM uk_price_paid
16
17┌──count()─┐
18│ 27735966 │
19└──────────┘
20
21– FINAL, correct result
22SELECT count()
23FROM uk_price_paid
24FINAL
25
26┌──count()─┐
27│ 27735104 │
28└──────────┘
29
30
31– no FINAL, incorrect result
32SELECT avg(price)
33FROM uk_price_paid
34
35┌─────────avg(price)─┐
36│ 214353.94542901445 │
37└────────────────────┘
38
39
40– FINAL, correct result with some precision
41SELECT avg(price)
42FROM uk_price_paid
43FINAL
44
45┌────────avg(price)─┐
46│ 214354.5317803748 │
47└───────────────────┘
```
Copy command
#### FINAL performance \#
