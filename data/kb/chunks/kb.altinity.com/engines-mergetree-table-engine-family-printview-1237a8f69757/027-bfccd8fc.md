---
source: kb.altinity.com
url: https://github.com/ClickHouse/clickhouse\-presentations/blob/master/meetup41/merge\_tree.pdf](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup41/merge_tree.pdf
topic: mergetree-table-engine-family-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '192.168'
last_updated: '2026-06-12'
chunk_index: 27
total_chunks_in_doc: 32
---

table t1 (ts DateTime64(3)) as select now64(3); select Department, sum(sign), sum(sign*metric1) from Example3 group by Department order by Department format Null ; select '---',timeSpent(),'GROUP BY OPTIMIZED'; ``` You can use fiddle or `clickhouse-local` to run such a test:

```
cat test.sql | clickhouse-local -nm

```
Results (Mac A2 Pro), milliseconds:

```
---	252	INSERT
---	1710	UPSERT
---	763	FINAL
---	311	GROUP BY
---	314	FINAL OPTIMIZED
---	295	GROUP BY OPTIMIZED

```
UPSERT is six times slower than direct INSERT because it requires looking up the destination table. That is the price. It is better to use idempotent inserts with an exactly\-once delivery guarantee. However, it’s not always possible.

The FINAL speed is quite good, especially if we split the table by 20 partitions, use `do_not_merge_across_partitions_select_final` setting, and keep most of the table’s partitions optimized (1 part per partition). But we can do it better.

### Adding projections

Let’s add an aggregating projection, and also add a more useful `updated_at` timestamp instead of an abstract `_version` and replace `String` for Department dimension by LowCardinality(String). Let’s look at the difference in time execution.

[https://fiddle.clickhouse.com/3140d341\-ccc5\-4f57\-8fbf\-55dbf4883a21](https://fiddle.clickhouse.com/3140d341-ccc5-4f57-8fbf-55dbf4883a21)
