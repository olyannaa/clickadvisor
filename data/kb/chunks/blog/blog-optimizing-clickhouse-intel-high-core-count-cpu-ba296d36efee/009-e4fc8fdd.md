---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Optimizing
topic: optimizing-clickhouse-for-intel-s-ultra-high-core-count-processors-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 9
total_chunks_in_doc: 17
---

90 temporary columns (one per expression), 3. **Sum values** performing 90 separate aggregation operations on each computed column. Creating 90 temporary columns and running 90 redundant aggregations obviously created massive memory pressure. **Frontend query optimization for memory efficiency**

This optimization demonstrates how better optimizer rules can reduce memory pressure by eliminating redundant computations. The key insight is that many analytical queries contain patterns that can be algebraically simplified.

The optimization recognizes that `sum(column + literal)` can be rewritten to `sum(column) + count(column) * literal`.

**Performance impact**

- ClickBench query Q29 sped up by 11\.5x on a 2×80 vCPU system.
- The geometric mean of all ClickBench queries saw a 5\.3% improvement overall.

More intelligent query plans can be more effective than optimizing execution itself. Avoiding work is better than doing work efficiently.

## **Bottleneck 3: Increase parallelism** \#

Fast aggregation is a core promise of any analytical database. From a database perspective, aggregating data in parallel threads is only one part of the equation. It is equally important to merge the local results in parallel.

ClickHouse's aggregation operator has two phases: In the first phase, each thread processes its portion of the data in parallel, creating a local and partial result. In the second phase, all partial results must be merged. If the merge phase is not properly parallelized, it becomes a bottleneck. More threads can actually make this issue worse by creating more partial results to merge.

Solving this issue requires careful algorithm design, smart data structure choices, and a deep understanding how hash tables behave under different load patterns. The goal is to eliminate the serial merge phase and enable linear scaling even for the most complex aggregation queries.

### **Optimization 3\.1: Hash Table Conversion ([PR \#50748](https://github.com/ClickHouse/ClickHouse/pull/50748))** \#

ClickBench query Q5 showed a severe performance degradation as the core count increased from 80 to 112 threads. Our pipeline analysis revealed serial processing in the hash table conversion.

**Understanding hash tables in ClickHouse**

ClickHouse uses two types of hash tables for hash aggregation:

1. **Single\-level hash tables**: This is a flat hash table that is suitable (\= faster) for smaller datasets.
2. **Two\-level hash tables**: This is a hierarchical hash table with 256 buckets. Two\-level hash tables are more amendable to large datasets.
