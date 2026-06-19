---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/newjson.md)#
topic: json-data-type-clickhouse-docs
ch_version_introduced: '42.42'
last_updated: '2026-06-12'
chunk_index: 24
total_chunks_in_doc: 26
---

events VALUES ('{"metric": {"cpu": 0.95}, "host": "srv1"}'); ``` You can use `EXPLAIN indexes = 1` to verify that the skip index is being used. When a path exists only in one part, the index skips the other part:

```
EXPLAIN indexes = 1 SELECT * FROM events WHERE data.user.name = 'Alice';

```

```
...
    Indexes:
      Skip
        Name: idx
        Description: bloom_filter GRANULARITY 1
        Parts: 1/2
        Granules: 1/2

```

When a path does not exist in any part, all parts and granules are skipped:

```
EXPLAIN indexes = 1 SELECT * FROM events WHERE data.nonexistent = 1;

```

```
...
    Indexes:
      Skip
        Name: idx
        Description: bloom_filter GRANULARITY 1
        Parts: 0/2
        Granules: 0/2

```

`IS NOT NULL` also uses the index — it skips granules where the path is absent (since the value would be `NULL`):

```
EXPLAIN indexes = 1 SELECT * FROM events WHERE data.user.name IS NOT NULL;

```

```
...
    Indexes:
      Skip
        Name: idx
        Description: bloom_filter GRANULARITY 1
        Parts: 1/2
        Granules: 1/2

```

#### How it works[​](#json-indexes-jsonallpaths-how-it-works "Direct link to How it works")

The `JSONAllPaths(json_column)` expression produces an `Array(String)` containing all paths present in a JSON value.
The skip index stores these path strings in its data structure (bloom filter or inverted index).
When a query filters on `json.some.path`, the index checks whether the string `"some.path"` is present in the index for each granule and skips granules where it is absent.

#### Safety with missing paths[​](#json-indexes-jsonallpaths-safety-with-missing-paths "Direct link to Safety with missing paths")

When a JSON path is absent from a granule, the subcolumn evaluates to:

- `NULL` for `Dynamic` type (e.g., `json.path`) and `Nullable` typed subcolumns (e.g., `json.path.:Int64`) — comparisons with `NULL` always return false, so skipping is safe.
- The type's default value for non\-`Nullable` CAST expressions (e.g., `json.path::Int64` produces `0` when the path is missing) — skipping is safe only when the compared value differs from the default. The index automatically handles this distinction.

### Full\-text search with JSONAllValues[​](#json-indexes-jsonallvalues "Direct link to Full-text search with JSONAllValues")
