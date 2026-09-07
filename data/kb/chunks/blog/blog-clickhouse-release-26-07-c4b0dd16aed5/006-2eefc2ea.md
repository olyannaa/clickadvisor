---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-26-7-clickhouse
ch_version_introduced: '26.7'
last_updated: '2026-09-07'
chunk_index: 6
total_chunks_in_doc: 24
---

and the same AWS EC2 `m6i.8xlarge` instance as in the previous section, with 32 vCPUs and 128 GiB of RAM. As a reminder, our example query calculates revenue from `lineitem` rows belonging to orders with `o_totalprice > 500000`:

```
SELECT
    sum(l.l_extendedprice * (1 - l.l_discount)) AS revenue
FROM lineitem AS l
INNER JOIN orders AS o
    ON l.l_orderkey = o.o_orderkey
WHERE o.o_totalprice > 500000;
```
Copy command

We compared the three relevant join and index optimizations disabled versus enabled. The query condition cache remained disabled in both configurations so that it could not influence the results:

| Setting | Disabled | Enabled |
| --- | --- | --- |
| `enable_join_runtime_filters` | `0` | `1` |
| `enable_join_runtime_filters_index_analysis` | `0` | `1` |
| `use_skip_indexes_on_data_read` | `0` | `1` |
| `use_query_condition_cache` | `0` | `0` |


First, we ran the query three consecutive times with all three optimizations disabled:

```
1 row in set. Elapsed: 0.600 sec. Processed 750.04 million rows, 13.23 GB (1.25 billion rows/s., 22.03 GB/s.)
Peak memory usage: 19.70 MiB.

1 row in set. Elapsed: 0.597 sec. Processed 750.04 million rows, 13.23 GB (1.26 billion rows/s., 22.14 GB/s.)
Peak memory usage: 29.58 MiB.

1 row in set. Elapsed: 0.599 sec. Processed 750.04 million rows, 13.23 GB (1.25 billion rows/s., 22.10 GB/s.)
Peak memory usage: 25.74 MiB.
```
Copy command
Next, we enabled all three optimizations and repeated the same three\-run test:

```
1 row in set. Elapsed: 0.099 sec. Processed 162.98 million rows, 1.41 GB (1.65 billion rows/s., 14.29 GB/s.)
Peak memory usage: 3.90 MiB.

1 row in set. Elapsed: 0.097 sec. Processed 162.98 million rows, 1.41 GB (1.68 billion rows/s., 14.51 GB/s.)
Peak memory usage: 6.84 MiB.

1 row in set. Elapsed: 0.097 sec. Processed 162.98 million rows, 1.41 GB (1.67 billion rows/s., 14.48 GB/s.)
Peak memory usage: 3.38 MiB.
```
Copy command
Using the fastest run from each configuration:
