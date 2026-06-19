---
source: blog
url: https://github.com/ClickHouse/clickhouse_vs_snowflake>
topic: clickhouse-vs-snowflake-for-real-time-analytics-benchmarks-and-cost-analysis
ch_version_introduced: '3.6'
last_updated: '2026-06-12'
chunk_index: 10
total_chunks_in_doc: 34
---

impact SELECT performance, so we report the total time taken for merges to reduce the part count to under 3000 (default recommended total) \- queries for this [here](https://github.com/ClickHouse/clickhouse_vs_snowflake/tree/main/insert_performance#misc). This is the value compared to Snowflake’s total load time.

| Database | Specification | Number of nodes | Memory per node (GiB) | vCPUs per node | Total vCPUs | Total memory (GiB) | Insert threads | Total time (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Snowflake | 2X\-LARGE | 32 | 16 | 8 | 256 | 512 | NA | 11410 |
| Snowflake | 4X\-LARGE | 128 | 16 | 8 | 1024 | 2048 | NA | 2901 |
| ClickHouse | 708GB | 3 | 236 | 59 | 177 | 708 | 4 | 15370 |
| ClickHouse | 708GB | 3 | 236 | 59 | 177 | 708 | 8 | 10400 |
| ClickHouse | 708GB | 3 | 236 | 59 | 177 | 708 | 16 | 11400 |
| ClickHouse | 1024GB | 16 | 64 | 16 | 256 | 1024 | 1\* | 9459 |
| ClickHouse | 1024GB | 16 | 64 | 16 | 256 | 1024 | 2 | 5730 |
| ClickHouse | 960GB | 8 | 120 | 30 | 240 | 960 | 4 | 6110 |
| ClickHouse | 960GB | 8 | 120 | 30 | 240 | 960 | 8 | 5391 |
| ClickHouse | 960GB | 8 | 120 | 30 | 240 | 960 | 16 | 6133 |



If we compare the best results for a 2X\-LARGE (256 vCPUs) vs. 960GB (240 vCPUs), which have similar resources, **ClickHouse delivers over 2x the insert performance of Snowflake for the same number of vCPUs**.

Other observations from this test:
