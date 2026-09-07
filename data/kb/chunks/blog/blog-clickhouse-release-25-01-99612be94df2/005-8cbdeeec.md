---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-25-1-clickhouse
ch_version_introduced: '24.12'
last_updated: '2026-09-07'
chunk_index: 5
total_chunks_in_doc: 12
---

by the two\-level hash table requires only lightweight modulo operations. To showcase the new parallel hash join's speed improvements, we first run a synthetic test on an AWS EC2 m6i.8xlarge instance with 32 vCPUs and 128 GiB RAM.

We run this query on ClickHouse version 24\.12:

```
1SELECT
2    count(c),
3    version()
4FROM numbers_mt(100000000) AS a
5INNER JOIN
6(
7    SELECT
8        number,
9        toString(number) AS c
10    FROM numbers(2000000)
11) AS b ON (a.number % 10000000) = b.number
12SETTINGS join_algorithm = 'parallel_hash';
```
Copy command

```
1┌─count(c)─┬─version()──┐
21. │ 20000000 │ 24.12.1.27 │
3   └──────────┴────────────┘
4
51 row in set. Elapsed: 0.521 sec. Processed 102.00 million rows, 816.00 MB (195.83 million rows/s., 1.57 GB/s.)
6Peak memory usage: 259.52 MiB.
```
Copy command
And on ClickHouse version 25\.1:

```
1SELECT
2    count(c),
3    version()
4FROM numbers_mt(100000000) AS a
5INNER JOIN
6(
7    SELECT
8        number,
9        toString(number) AS c
10    FROM numbers(2000000)
11) AS b ON (a.number % 10000000) = b.number
12SETTINGS join_algorithm = 'parallel_hash';
```
Copy command

```
1┌─count(c)─┬─version()─┐
21. │ 20000000 │ 25.1.3.23 │
3   └──────────┴───────────┘
4
51 row in set. Elapsed: 0.330 sec. Processed 102.00 million rows, 816.00 MB (309.09 million rows/s., 2.47 GB/s.)
6Peak memory usage: 284.96 MiB.
```
Copy command
0\.330 seconds is approximately **36\.66% faster** than 0\.521 seconds.

Speed improvements are also tested on the same machine using the [TPC\-H dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/tpch) with a scaling factor of 100\. The tables, modeling a wholesale supplier’s data warehouse, were created and loaded [following the official documentation](https://clickhouse.com/docs/en/getting-started/example-datasets/tpch#data-generation-and-import).

A typical query joins the `lineitem` and `orders` tables using ClickHouse 24\.12\. The hot run results are shown below, where the hot run is the fastest of three consecutive runs:

```
1SELECT
2    count(),
3    version()
4FROM lineitem AS li
5INNER JOIN orders AS o ON li.l_orderkey = o.o_orderkey
6SETTINGS join_algorithm = 'parallel_hash';
```
Copy command

```
1┌───count()─┬─version()──┐
21. │ 600037902 │ 24.12.1.27 │
3   └───────────┴────────────┘
4
51 row in set. Elapsed: 3.100 sec. Processed 750.04 million rows, 3.00 GB (241.97 million rows/s., 967.89 MB/s.)
6Peak memory usage: 16.79 GiB.
```
Copy command
Now on ClickHouse version 25\.1:

```
1SELECT
2    count(),
3    version()
4FROM lineitem AS li
5INNER JOIN orders AS o ON li.l_orderkey = o.o_orderkey
6SETTINGS join_algorithm = 'parallel_hash';
```
Copy command
