---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Optimizing
topic: optimizing-clickhouse-for-intel-s-ultra-high-core-count-processors-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 4
total_chunks_in_doc: 17
---

the currently read part has a final mark The query condition cache is read\-heavy, i.e. there are far more reads than writes, but the original implementation used exclusive locking for all operations. **Reducing critical paths in read\-heavy workloads**

This optimization demonstrates the importance of reducing the time spent holding locks, especially write locks in read\-heavy code.

With 240 threads within a single query, the original code created a perfect storm:

1. **Unnecessary write locks**: All threads acquired exclusive locks, even when they only read cache entries.
2. **Long critical sections**: Expensive updates of cache entries were performed inside exclusive locks.
3. **Redundant work**: Multiple threads updated the same cache entries potentially multiple times.

Our optimization uses [double\-checked locking](https://en.wikipedia.org/wiki/Double-checked_locking) with atomic operations to resolve these bottlenecks:

1. The code now first checks with atomic reads (no locking), respectively under a shared lock if an update is needed at all (fast path).
2. Next, the code checks immediately after acquiring an exclusive lock (slow path) if an update is actually required \- another thread may have performed the same update in the meantime.

**Implementation**

Based on [PR \#80247](https://github.com/ClickHouse/ClickHouse/pull/80247/files), the optimization introduces a fast path which checks if an update is needed before acquiring the expensive write lock.

```
1/// Original code
2void updateCache(mark_ranges, has_final_mark)
3{
4    acquire_exclusive_lock(cache_mutex);  /// 240 threads wait here!
5
6    /// Always update marks, even if already in desired state
7    for (const auto & range : mark_ranges)
8        set_marks_to_false(range.begin, range.end);
9
10    if (has_final_mark):
11        set_final_mark_to_false();
12
13    release_lock(cache_mutex);
14}
```
Copy command
