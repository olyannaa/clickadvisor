---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Optimizing
topic: optimizing-analytical-workloads-comparing-redshift-vs-clickhouse-clickhouse
ch_version_introduced: '0.0005'
last_updated: '2026-09-07'
chunk_index: 7
total_chunks_in_doc: 33
---

the compressed size for both only. For the full table schemas and codecs used, see the below section Migrating Redshift Tables to ClickHouse. ### Measuring Redshift Table Size \# This information can be obtained with a simple query.

```
1SELECT "table", size, tbl_rows, unsorted, pct_used, diststyle  FROM SVV_TABLE_INFO WHERE "table" = 'blocks'
2
3?column?    size    tbl_rows    unsorted    pct_used
4blocks      11005   16629116    0           0.0005
```
Copy command
It is expected that the value of “unsorted” field is 0\. If not, users can run a [`VACUUM`](https://docs.aws.amazon.com/redshift/latest/dg/r_VACUUM_command.html) command to sort any unsorted rows in the background and achieve more optimal compression. The value returned for `size` is in MB and can be compared to compressed storage in ClickHouse. The distribution style is also returned since this can [impact total size](https://aws.amazon.com/premiumsupport/knowledge-center/redshift-cluster-storage-space/). Our tables have all been configured with an AUTO value, Redshift is free to assign an [optimal distribution style and adjust this based on table size.](https://docs.aws.amazon.com/redshift/latest/dg/c_choosing_dist_sort.html) Aside from our smallest table, blocks, the [EVEN](https://docs.aws.amazon.com/redshift/latest/dg/c_choosing_dist_sort.html) distribution style is selected, which means that the data is sent round\-robin across nodes. We applied the optimal compression algorithms for each column as identified by the [`ANALYZE COMPRESSION`](https://docs.aws.amazon.com/redshift/latest/dg/r_ANALYZE_COMPRESSION.html) (see “Compression” below).

Below we capture Redshift storage statistics from the serverless instance.

| **Table Name** | **Total Rows** | **Compressed size** | **Distribution style** |
| --- | --- | --- | --- |
| blocks | 16629116 | 10\.74GB | AUTO(KEY(number)) |
| contracts | 57394746 | 12\.51GB | AUTO(EVEN) |
| transactions | 1874052391 | 187\.53GB | AUTO(EVEN) |
| traces | 6377694114 | 615\.46GB | AUTO(EVEN) |


### Measuring ClickHouse Table Size \#

Compressed table sizes in ClickHouse can be found with a query to the `system.columns` table.

```
1SELECT
2    table,
3    formatReadableSize(sum(data_compressed_bytes)) AS compressed_size
4FROM system.columns
5WHERE database = 'ethereum'
6GROUP BY table
7ORDER BY sum(data_compressed_bytes) DESC
8
9┌─table───────────┬─compressed_size─┬
10│ traces          │ 339.95 GiB      │
11│ transactions    │ 139.94 GiB      │
12│ blocks          │ 5.37 GiB        │
13│ contracts       │ 2.73 GiB        │
14└─────────────────┴──────────────────
```
Copy command
### Comparison \#

Below we compare the above measurements, also comparing to Parquet and computing a ClickHouse to Redshift storage ratio.
