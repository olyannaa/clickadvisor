---
source: blog
url: https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9
topic: clickhouse-release-25-7
ch_version_introduced: '25.7'
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 10
---

key column. This reduces CPU instructions and speeds up one\-column JOINs. Each bar in the [PR](https://github.com/ClickHouse/ClickHouse/pull/82308)’s test screenshot compares old vs. new JOIN performance, showing \~1\.37× speedups across the board. ![Joins-01.png](/uploads/Joins_01_915a71fa40.png) ### 2\. Speed\-ups for multi\-OR\-condition JOINs [\#](/blog/clickhouse-release-25-07#2-speed-ups-for-multi-or-condition-joins)

Extended those single\-key optimizations to JOINs with multiple OR conditions in the ON clause. These now benefit from the same lower\-level improvements, making JOINs with multiple OR conditions more efficient.

Multi\-condition JOINs now run up to 1\.5× faster. Each bar in the [PR](https://github.com/ClickHouse/ClickHouse/pull/83041)’s performance test screenshot shows speedups for queries with OR conditions in the ON clause, thanks to reduced instruction overhead and tighter join loop execution.

![Joins-02.png](/uploads/Joins_02_002d7f7e23.png)
### 3\. Lower CPU overhead in join processing [\#](/blog/clickhouse-release-25-07#3-lower-cpu-overhead-in-join-processing)

Removed repeated hash computations during join tracking, cutting down on redundant work and boosting JOIN throughput.

Two join queries with large input tables show 1\.5× to 1\.8× speedups in the [PR](https://github.com/ClickHouse/ClickHouse/pull/83043)’s performance test screenshot after reducing hash recomputation overhead. These improvements target joins with high match cardinality, where redundant hashing previously dominated CPU cycles.

![Joins-03a.png](/uploads/Joins_03a_f75f788a04.png)
![Joins-03b.png](/uploads/Joins_03b_5d0f19d912.png)
### 4\. Reduced memory usage for join results [\#](/blog/clickhouse-release-25-07#4-reduced-memory-usage-for-join-results)

Result buffers are now sized precisely after determining the number of matches, avoiding waste and improving performance, especially for wide rows with repeated or padded columns, such as from JOIN ... USING queries or synthetic columns.

The [PR](https://github.com/ClickHouse/ClickHouse/pull/83304)’s performance test screenshot shows that JOINs with wide result rows now complete 1\.3× to 1\.4× faster due to more precise sizing of result buffers. These queries previously over\-allocated memory for joined rows, especially when many columns were repeated or padded. The optimization reduces memory usage and speeds up processing for sparse or wide joins.

![Joins-04a.png](/uploads/Joins_04a_bc2b7400ef.png)
![Joins-04b.png](/uploads/Joins_04b_a0cd927b2f.png)
We’re not done yet. JOIN performance remains a top priority, and we’ll continue optimizing the parallel hash join and other strategies in future releases.

**Coming soon**: We’re working on a technical deep dive that will walk through all of the JOIN improvements from the past few months, including benchmarks and practical examples. Stay tuned!

## Native support for Geo Parquet types [\#](/blog/clickhouse-release-25-07#native-support-for-geo-parquet-types)

### Contributed by Konstantin Vedernikov [\#](/blog/clickhouse-release-25-07#contributed-by-konstantin-vedernikov)

In ClickHouse 25\.5, ClickHouse [added support for reading Geo types in Parquet files](https://clickhouse.com/blog/clickhouse-release-25-05#geo-types-in-parquet). In that release, ClickHouse read Parquet’s Geo Types into other ClickHouse types, like tuples or lists.
