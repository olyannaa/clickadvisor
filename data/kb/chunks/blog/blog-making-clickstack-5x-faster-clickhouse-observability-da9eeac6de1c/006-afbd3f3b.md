---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-we-made-clickstack-5x-faster-for-clickhouse-observability-clickhouse
ch_version_introduced: '0.001'
last_updated: '2026-09-07'
chunk_index: 6
total_chunks_in_doc: 18
---

meaningful gains elsewhere**. We then evaluate the impact on the compute\-compute\-separated read service, accounting for changes in CPU and memory requirements. Again, if these are appreciably impacted, they must be evaluated against the gains made in query performance.

Assuming any additional costs are acceptable, we evaluate the performance of individual queries. While most optimizations targeted a specific query pattern, every benchmark run also includes the broader workload to ensure improvements are not achieved at the expense of regressions elsewhere in the product.

## Schema optimizations \#

We explored a wide range of potential optimizations, but the most impactful changes fell into five categories: primary key changes, index updates, new index additions, query rewrites, and table settings.

As a reminder, this was our original schema:
