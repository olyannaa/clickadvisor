---
source: blog
url: https://clickhouse.com/blog/netflix-petabyte-scale-logging
topic: how-clickstack-makes-clickhouse-faster-for-observability
ch_version_introduced: '0.01'
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 16
---

3WHERE (Timestamp >= '2026-01-01') 4 AND (Timestamp < '2026-03-14') 5 AND (Body ILIKE '% error %'); ``` ``` ``` 1 row in set. Elapsed: 0.708 sec. Processed 91.56 million rows, 14.91 GB (129.37 million rows/s., 21.06 GB/s.) ```

This works, but does not exploit the text index. ClickStack, however, detects the index is available and uses the `hasAllTokens()` function \- specifically designed to leverage the text index:

```

```
1SELECT *
2FROM otel_logs
3WHERE (Timestamp >= '2026-01-01')
4  AND (Timestamp < '2026-03-14')
5  AND hasAllTokens(Body, 'error');
```

```

```
1 row in set. Elapsed: 0.029 sec. Processed 2.86 million rows, 22.92 MB (97.87 million rows/s., 784.96 MB/s.)

```

For multi\-word phrases such as "connection refused", ClickStack combines index usage with a confirmation filter to preserve ordering semantics:

```

```
1SELECT *
2FROM otel_logs
3WHERE (Timestamp >= '2026-01-01')
4  AND (Timestamp < '2026-03-14')
5  AND hasAllTokens(Body, 'connection refused')
6  AND (lower(Body) LIKE lower('%connection refused%'));
```

```

The result is a single multi\-token lookup against the text index, dramatically reducing scanned granules.

Similar care is needed if exploiting bloom filters. In this case, ClickStack detects the expression used for the bloom filter index and ensures it combines this appropriately with the appropriate functions for matching. Consider the following (simplified) schema for logs:

```

```
1CREATE TABLE otel_logs (
2    Body String,
3    INDEX idx_body_bloom tokens(lower(Body))
4        TYPE bloom_filter(0.001)
5        GRANULARITY 8
6)
```

```

> Note we lower the body to achieve case insensitive matching.

Suppose a user searches for "error", this requires use of the [`hasToken`](https://clickhouse.com/docs/sql-reference/functions/string-search-functions#hasToken) function but also requires us to combine this with the [`lower`](https://clickhouse.com/docs/sql-reference/functions/string-functions#lower) function to ensure the index is used. ClickStack detects the expression, reflecting this in the final transpiled SQL:

```

```
1SELECT *
2FROM otel_logs
3WHERE (Timestamp >= '2026-01-01')
4  AND (Timestamp < '2026-03-14')
5  AND hasAll(
6      tokens(lower(Body)),
7      tokens(lower('error'))
8  );
```

```

The key is that the left side exactly matches the stored index expression. This allows ClickHouse to activate the Bloom filter and skip granules that definitely do not contain the token.

The same principle applies to Map\-based columns, such as LogAttributes and ResourceAttributes for default OTel tables. These often have Bloom filter indices on `mapKeys(...)` and `mapValues(...)` designed to allow granules to be skipped if an attribute key or value is not present.
