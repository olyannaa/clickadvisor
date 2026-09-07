---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-vs-snowflake-for-real-time-analytics-benchmarks-and-cost-analysis-clickhouse
ch_version_introduced: '3.6'
last_updated: '2026-09-07'
chunk_index: 6
total_chunks_in_doc: 35
---

Snowflake states that query acceleration service depends on server availability and performance improvements might fluctuate over time, making it not a great fit for reproducible benchmarks. ### Schemas \# #### ClickHouse \# Our ClickHouse schema is shown below:

```
1CREATE TABLE default.pypi
2(
3   `timestamp` DateTime64(6),
4   `date` Date MATERIALIZED timestamp,
5   `country_code` LowCardinality(String),
6   `url` String,
7   `project` String,
8   `file` Tuple(filename String, project String, version String, type Enum8('bdist_wheel' = 0, 'sdist' = 1, 'bdist_egg' = 2, 'bdist_wininst' = 3, 'bdist_dumb' = 4, 'bdist_msi' = 5, 'bdist_rpm' = 6, 'bdist_dmg' = 7)),
9   `installer` Tuple(name LowCardinality(String), version LowCardinality(String)),
10   `python` LowCardinality(String),
11   `implementation` Tuple(name LowCardinality(String), version LowCardinality(String)),
12   `distro` Tuple(name LowCardinality(String), version LowCardinality(String), id LowCardinality(String), libc Tuple(lib Enum8('' = 0, 'glibc' = 1, 'libc' = 2), version LowCardinality(String))),
13   `system` Tuple(name LowCardinality(String), release String),
14   `cpu` LowCardinality(String),
15   `openssl_version` LowCardinality(String),
16   `setuptools_version` LowCardinality(String),
17   `rustc_version` LowCardinality(String),
18   `tls_protocol` Enum8('TLSv1.2' = 0, 'TLSv1.3' = 1),
19   `tls_cipher` Enum8('ECDHE-RSA-AES128-GCM-SHA256' = 0, 'ECDHE-RSA-CHACHA20-POLY1305' = 1, 'ECDHE-RSA-AES128-SHA256' = 2, 'TLS_AES_256_GCM_SHA384' = 3, 'AES128-GCM-SHA256' = 4, 'TLS_AES_128_GCM_SHA256' = 5, 'ECDHE-RSA-AES256-GCM-SHA384' = 6, 'AES128-SHA' = 7, 'ECDHE-RSA-AES128-SHA' = 8)
20)
21ENGINE = MergeTree
22ORDER BY (project, date, timestamp)
```
Copy command
We apply a number of type optimizations here as well as adding the materialized column `date` to the schema. This is not part of the raw data and has been added purely for use in the primary key and filter queries. We have represented the nested structures `file`, `installer`, `implementation`, and `distro` as named tuples. These are [hierarchical data structures](https://docs.snowflake.com/en/user-guide/semistructured-intro#what-is-hierarchical-data) (rather than fully semi\-structured) and thus have predictable sub\-columns. This allows us to apply the same type of optimizations as those applied to root columns.

Full details on the optimizations applied can be found [here](https://github.com/ClickHouse/clickhouse_vs_snowflake/tree/main/compression).

#### Snowflake \#

Our Snowflake schema:
