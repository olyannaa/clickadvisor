---
source: kb.altinity.com
url: https://altinity.com/blog/2020-5-20-reducing-clickhouse-storage-cost-with-the-low-cardinality-type-lessons-from-an-instana-engineer
topic: sampling-example-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '0.5'
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 4
---

granularity of `timestamp` column is not reduced. #### Verifying Sampling Does Not Work The following tests shows that sampling is **not** working because of the lack of `timestamp` granularity. The `Elapsed` time is longer when sampling is used.

```
-- Q1. No where filters.
-- The query is 2 times SLOWER!!! with SAMPLE 0.01
-- Because it needs to read excessive column with sampling data!
select banner_id, sum(value), count(value), max(value)
from table_one
group by banner_id format Null;
0 rows in set. Elapsed: 11.196 sec.
     Processed 10.00 billion rows, 60.00 GB (893.15 million rows/s., 5.36 GB/s.)

select banner_id, sum(value), count(value), max(value)
from table_one SAMPLE 0.01
group by banner_id format Null;
0 rows in set. Elapsed: 24.378 sec.
     Processed 10.00 billion rows, 140.00 GB (410.21 million rows/s., 5.74 GB/s.)

-- Q2. Filter by the first column in index (banner_id = 42)
-- The query is SLOWER with SAMPLE 0.01
select banner_id, sum(value), count(value), max(value)
from table_one
WHERE banner_id = 42
group by banner_id format Null;
0 rows in set. Elapsed: 0.022 sec.
     Processed 10.27 million rows, 61.64 MB (459.28 million rows/s., 2.76 GB/s.)

select banner_id, sum(value), count(value), max(value)
from table_one SAMPLE 0.01
WHERE banner_id = 42
group by banner_id format Null;
0 rows in set. Elapsed: 0.037 sec.
     Processed 10.27 million rows, 143.82 MB (275.16 million rows/s., 3.85 GB/s.)

-- Q3. No filters
-- The query is SLOWER with SAMPLE 0.01
select banner_id,
       toStartOfHour(toDateTime(timestamp)) hr,
       sum(value), count(value), max(value)
from table_one
group by banner_id, hr format Null;
0 rows in set. Elapsed: 21.663 sec.
     Processed 10.00 billion rows, 140.00 GB (461.62 million rows/s., 6.46 GB/s.)

select banner_id,
       toStartOfHour(toDateTime(timestamp)) hr, sum(value),
       count(value), max(value)
from table_one SAMPLE 0.01
group by banner_id, hr format Null;
0 rows in set. Elapsed: 26.697 sec.
     Processed 10.00 billion rows, 220.00 GB (374.57 million rows/s., 8.24 GB/s.)

-- Q4. Filter by not indexed column
-- The query is SLOWER with SAMPLE 0.01
select count()
from table_one
where value = 666 format Null;
0 rows in set. Elapsed: 7.679 sec.
     Processed 10.00 billion rows, 40.00 GB (1.30 billion rows/s., 5.21 GB/s.)

select count()
from table_one  SAMPLE 0.01
where value = 666 format Null;
0 rows in set. Elapsed: 21.668 sec.
     Processed 10.00 billion rows, 120.00 GB (461.51 million rows/s., 5.54 GB/s.)

```
Last modified 2025\.01\.16: [Streamlined page metadata, simplified directory structure (afe0f3c)](https://github.com/Altinity/altinityknowledgebase/commit/afe0f3c3e76e848e6941903e93f05dd41fccfea0)
