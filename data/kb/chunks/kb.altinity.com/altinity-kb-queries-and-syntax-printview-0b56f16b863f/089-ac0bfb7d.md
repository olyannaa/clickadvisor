---
source: kb.altinity.com
url: https://github.com/ClickHouse/ClickHouse/blob/8ab5270ded39c8b044f60f73c1de00c8117ab8f2/src/Interpreters/Aggregator.cpp#L382
topic: queries-syntax-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '8.888'
last_updated: '2026-06-12'
chunk_index: 89
total_chunks_in_doc: 117
---

count() from table_one SAMPLE 0.01 where value = 666 format Null; 0 rows in set. Elapsed: 21.668 sec. Processed 10.00 billion rows, 120.00 GB (461.51 million rows/s., 5.54 GB/s.) ``` # 38 \- Simple aggregate functions \& combinators

Simple aggregate functions \& combinators### Q. What is SimpleAggregateFunction? Are there advantages to use it instead of AggregateFunction in AggregatingMergeTree?

The ClickHouse® SimpleAggregateFunction can be used for those aggregations when the function state is exactly the same as the resulting function value. Typical example is `max` function: it only requires storing the single value which is already maximum, and no extra steps needed to get the final value. In contrast `avg` need to store two numbers \- sum \& count, which should be divided to get the final value of aggregation (done by the `-Merge` step at the very end).

|  | SimpleAggregateFunction | AggregateFunction |
| --- | --- | --- |
| inserting | accepts the value of underlying type ORa value of corresponding SimpleAggregateFunction type`CREATE TABLE saf_test( x SimpleAggregateFunction(max, UInt64) )ENGINE=AggregatingMergeTreeORDER BY tuple();INSERT INTO saf_test VALUES (1);INSERT INTO saf_test SELECT max(number) FROM numbers(10);INSERT INTO saf_test SELECT maxSimpleState(number) FROM numbers(20);` | ONLY accepts the state of same aggregate function calculated using \-State combinator |
| storing | Internally store just a value of underlying type | function\-specific state |
| storage usage | typically is much better due to better compression/codecs | in very rare cases it can be more optimal than raw valuesadaptive granularity doesn't work for large states |
| reading raw value per row | you can access it directly | you need to use `finalizeAggregation` function |
| using aggregated value | just`select max(x) from test;` | you need to use `-Merge` combinator`select maxMerge(x) from test;` |
| memory usage | typically less memory needed (in some corner cases even 10 times) | typically uses more memory, as every state can be quite complex |
| performance | typically better, due to lower overhead | worse |

See also:

- [Altinity Knowledge Base article on AggregatingMergeTree](../../engines/mergetree-table-engine-family/aggregatingmergetree/)
- <https://github.com/ClickHouse/ClickHouse/pull/4629>
- <https://github.com/ClickHouse/ClickHouse/issues/3852>

### Q. How maxSimpleState combinator result differs from plain max?

They produce the same result, but types differ (the first have `SimpleAggregateFunction` datatype). Both can be pushed to SimpleAggregateFunction or to the underlying type. So they are interchangeable.

#### Info
