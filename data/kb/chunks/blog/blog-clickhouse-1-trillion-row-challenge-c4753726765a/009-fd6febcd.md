---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-and-the-one-trillion-row-challenge-clickhouse
ch_version_introduced: '0.2441'
last_updated: '2026-09-07'
chunk_index: 9
total_chunks_in_doc: 14
---

over 920 MB/sec. With less time spent waiting, we utilize our threads more efficiently, increasing CPU utilization to around 23 cores. All of this has the effect of reducing our execution time from 486 seconds to 303s seconds.

```
10 rows in set. Elapsed: 303.462 sec. Processed 111.11 billion rows, 279.18 GB (366.14 million rows/s., 919.97 MB/s.)
2Peak memory usage: 534.87 MiB.
```
Copy command
After confirming that further increases in the buffer size yielded no benefit, as expected, and given that at 920MB/s, our instances are still definitely not network bound, we considered how we might further increase the CPU utilization.

By default most stages of this query will be run with 48 threads on each node as confirmed with an `EXPLAIN PIPELINE`:

```
1EXPLAIN PIPELINE
2SELECT
3	station,
4	min(measure),
5	max(measure),
6	round(avg(measure), 2)
7FROM s3('https://coiled-datasets-rp.s3.us-east-1.amazonaws.com/1trc/measurements-1*.parquet', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', headers('x-amz-request-payer' = 'requester'))
8GROUP BY station
9ORDER BY station ASC
10
11┌─explain─────────────────────────────────────┐
12│ (Expression)                            	  │
13│ ExpressionTransform                     	  │
14│   (Sorting)                             	  │
15│   MergingSortedTransform 48 → 1         	  │
16│ 	MergeSortingTransform × 48          	  │
17│   	LimitsCheckingTransform × 48      	  │
18│     	PartialSortingTransform × 48    	  │
19│       	(Expression)                  	  │
20│       	ExpressionTransform × 48      	  │
21│         	(Aggregating)               	  │
22│         	Resize 48 → 48              	  │
23│           	AggregatingTransform × 48 	  │
24│             	StrictResize 48 → 48    	  │
25│               	(Expression)          	  │
26│               	ExpressionTransform × 48  │
27│                 	(ReadFromStorageS3Step)   │
28│                 	S3 × 48 0 → 1       	  │
29└─────────────────────────────────────────────┘
30
3117 rows in set. Elapsed: 0.305 sec.
```
Copy command
This defaults to the number of vCPUs per node by default and represents a sensible default for most queries. In our case, given the read\-intensive nature of the task, increasing this made sense.

> Ideally we would like to be able to increase just the number of download threads in this test. Currently, this isn’t available as a setting in ClickHouse, but is [something we’re considering](https://github.com/ClickHouse/ClickHouse/issues/60766).

While we didn’t perform exhaustive testing, some simple tests showed the benefit of increasing the `max_threads` to 128:

![max_threads_vs_latency.png](/_next/image?url=%2Fuploads%2Fmax_threads_vs_latency_aa068f259f.png&w=2048&q=75)

*The above represents the average from 3 executions.*

This also delivered a decent improvement, reducing the total runtime to 138 seconds.
