---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-24-12-clickhouse
ch_version_introduced: '85.24'
last_updated: '2026-09-07'
chunk_index: 9
total_chunks_in_doc: 12
---

2 CASE 3 WHEN p_type LIKE 'PROMO%' 4 THEN l_extendedprice * (1 - l_discount) 5 ELSE 0 END) / sum(l_extendedprice * (1 - l_discount)) AS promo_revenue 6FROM part, lineitem 7WHERE l_partkey = p_partkey 8SETTINGS query_plan_join_swap_table='false'; ``` Copy command

```
1┌──────promo_revenue─┐
21. │ 16.650141208349083 │
3   └────────────────────┘
4
51 row in set. Elapsed: 55.687 sec. Processed 620.04 million rows, 12.67 GB (11.13 million rows/s., 227.57 MB/s.)
6Peak memory usage: 24.39 GiB.
```
Copy command
Next, we run the same query with the new `query_plan_join_swap_table` setting set to `auto` (the default value). Now ClickHouse will use estimations of the table sizes to determine which side of the join should be the build table. Therefore, ClickHouse first loads the data from the very much smaller `part` table into the main memory into hash tables before streaming and joining the data from the `lineitem` table:

```
1SELECT 100.00 * sum(
2  CASE
3  WHEN p_type LIKE 'PROMO%'
4  THEN l_extendedprice * (1 - l_discount)
5  ELSE 0 END) / sum(l_extendedprice * (1 - l_discount)) AS promo_revenue
6FROM part, lineitem
7WHERE l_partkey = p_partkey
8SETTINGS query_plan_join_swap_table='auto';
```
Copy command

```
1┌──────promo_revenue─┐
21. │ 16.650141208349083 │
3   └────────────────────┘
4
51 row in set. Elapsed: 9.447 sec. Processed 620.04 million rows, 12.67 GB (65.63 million rows/s., 1.34 GB/s.)
6Peak memory usage: 4.72 GiB.
```
Copy command
As you can see, the query runs over 5 times faster and uses 5 times less memory.

## Optimization of JOIN expressions \#

### Contributed by János Benjamin Antal \#

For joins with a chain of conditions, separated by `OR`s, like shown in this abstract example…

```
1JOIN ... ON (a=b AND x) OR (a=b AND y) OR (a=b AND z)
```
Copy command
… ClickHouse uses hash tables per condition (when one of the [hash table\-based join algorithms](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2) is used).

One way to reduce the number of hash tables and to allow better predicate push downs is to extract common expressions from ON clause of the example JOIN above:

```
1JOIN ...ON a=b AND (x OR y OR z)
```
Copy command
This behavior can be enabled by setting the new `optimize_extract_common_expressions` setting to `1`. Because this setting is currently experimental, the default value is currently `0`.
