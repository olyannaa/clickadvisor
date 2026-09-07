---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"What's
topic: what-s-new-in-clickstack-february-26-clickhouse
ch_version_introduced: '0.99'
last_updated: '2026-09-07'
chunk_index: 8
total_chunks_in_doc: 11
---

(set to `100000`) to allow the optimization to kick in for sufficiently large result scans. When the `ORDER BY` aligns with the table’s ordering key, pruning is highly effective because granules can be skipped purely based on metadata.

> When the sort column is not part of the ordering key, ClickHouse can still apply a dynamic Top\-N threshold during execution, skipping granules that cannot improve the result set via `use_top_k_dynamic_filtering = 1`, delivering up to 2x improvements in some real\-world log searches depending on data distribution and predicates; however, this is **not yet enabled** globally in ClickStack because features such as Event Patterns rely on functions like `rand()` that are incompatible with the optimization. We plan to enable it selectively in the near future.

These settings turn many Top\-N queries into a metadata pruning problem rather than a full table scan. As datasets grow and cold cache scenarios become more common, avoiding unnecessary reads at the granule level becomes increasingly impactful, and ClickStack now takes advantage of this automatically.

For a deep dive on these features, we recommend our [dedicated blog post.](https://clickhouse.com/blog/clickhouse-top-n-queries-granule-level-data-skipping)

### Faster skip indices \#

ClickStack already relies heavily on ClickHouse [data skipping indexes](https://clickhouse.com/docs/optimize/skipping-indexes/examples) to accelerate common observability workloads. Bloom filter indexes power fast text search across logs. Minmax indexes are widely used to accelerate numeric range queries, especially on timestamps and other high cardinality fields. Users are [encouraged to exploit these indices](https://clickhouse.com/docs/use-cases/observability/clickstack/performance_tuning#adding-skip-indices) if they need to perform schema optimization.

Before ClickHouse 25\.9, skip indexes such as minmax, set, bloom filter, vector, and more [recently text](https://clickhouse.com/blog/full-text-search-ga-release) were evaluated up front, before any table data was read. This sequential approach had a few important drawbacks. Queries with LIMIT still had to scan the entire index before execution could begin. There was an initial startup delay while index analysis completed. In some cases, scanning the index itself could cost more than processing the data.
