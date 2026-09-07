---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Streaming
topic: streaming-secondary-indices-incremental-demand-driven-index-evaluation-clickhouse
ch_version_introduced: '25.9'
last_updated: '2026-09-07'
chunk_index: 3
total_chunks_in_doc: 4
---

can check that the bloom filter index has a size of over 2 GiB now: ``` 1SELECT 2 name, 3 type_full, 4 formatReadableSize(data_uncompressed_bytes) AS size 5FROM system.data_skipping_indices 6WHERE database = 'default' AND table = 'test'; ``` Copy command

```
1┌─name──┬─type_full────────────┬─size─────┐
21. │ s_idx │ bloom_filter(0.0001) │ 2.21 GiB │
3   └───────┴──────────────────────┴──────────┘
```
Copy command
To make the comparison fair, we cleared the OS page cache before each of the two test query runs below.

```
1echo 3 | sudo tee /proc/sys/vm/drop_caches >/dev/null
```
Copy command
**Without streaming indices** (use\_skip\_indexes\_on\_data\_read \= 0\), finding a single row with LIMIT 1 took \~10 seconds.

*Note that we set max\_threads \= 1 and disabled the [query condition cache](https://clickhouse.com/blog/introducing-the-clickhouse-query-condition-cache) to isolate and highlight the effect of secondary index processing.*

```
1SELECT * FROM test WHERE s = 'needle' LIMIT 1 
2SETTINGS 
3  max_threads = 1, 
4  use_query_condition_cache = 0,  use_skip_indexes_on_data_read = 0;
```
Copy command

```
1┌─s──────┐
21. │ needle │
3   └────────┘
4
51 row in set. Elapsed: 10.173 sec. Processed 29.70 thousand rows, 2.14 MB (2.92 thousand rows/s., 210.00 KB/s.)
6Peak memory usage: 8.90 MiB.
```
Copy command
**With streaming indices** (use\_skip\_indexes\_on\_data\_read \= 1\), the same query returned in \~2\.4 seconds — over 4× faster with less memory used.

```
1SELECT * FROM test WHERE s = 'needle' LIMIT 1 
2SETTINGS 
3  max_threads = 1, 
4  use_query_condition_cache = 0,  use_skip_indexes_on_data_read = 1;
```
Copy command

```
1┌─s──────┐
21. │ needle │
3   └────────┘
4
51 row in set. Elapsed: 2.471 sec. Processed 29.70 thousand rows, 2.14 MB (12.02 thousand rows/s., 864.57 KB/s.)
6Peak memory usage: 4.48 MiB.
```
Copy command
## Why this is faster in practice \#

As a reminder, the observed speedup comes from two (① and ②) mechanisms:

- **Without streaming indices**: Before query processing even begins, ClickHouse must fully scan and process the index to identify all matching granules.
- **With streaming indices**:  

① ClickHouse concurrently scans the index and processes matching granules in the query engine.  

② And as soon as the first matching row (LIMIT 1\) is found, it immediately stops scanning further index entries and granules, eliminating wasted work.

## Key takeaway \#
