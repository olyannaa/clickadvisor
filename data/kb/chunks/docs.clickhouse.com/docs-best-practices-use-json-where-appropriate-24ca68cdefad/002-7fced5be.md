---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/json_type.md)#
topic: use-json-where-appropriate-clickhouse-docs
ch_version_introduced: '3.9'
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 6
---

within JSON objects whose structure you can't predict upfront - Your use case involves semi\-structured data like logs, events, or user\-generated content with inconsistent schemas ### Use a `String` column (or structured types) when:[​](#use-string-type "Direct link to use-string-type")

- Your data structure is known and consistent \- in this case, use normal columns, `Tuple`, `Array`, `Dynamic`, or `Variant` types instead
- `JSON` documents are treated as opaque blobs that are only stored and retrieved in their entirety without field\-level analysis
- You don't need to query or filter on individual JSON fields within the database
- The `JSON` is simply a transport/storage format, not analyzed within ClickHouse

TipIf `JSON` is an opaque document that isn't analyzed inside the database, and only stored and retrieved back, it should be stored as a `String` field. The `JSON` type's benefits only materialize when you need to efficiently query, filter, or aggregate on specific fields within dynamic `JSON` structures.You can also mix approaches—use standard columns for predictable top\-level fields and a `JSON` column for dynamic sections of the payload.

## Considerations and tips for using JSON[​](#considerations-and-tips-for-using-json "Direct link to Considerations and tips for using JSON")

The JSON type enables efficient columnar storage by flattening paths into subcolumns. But with flexibility comes responsibility. To use it effectively:

- **Specify path types** using [hints in the column definition](/docs/sql-reference/data-types/newjson) to specify types for known subcolumns, avoiding unnecessary type inference.
- **Skip paths** if you don't need the values, with [SKIP and SKIP REGEXP](/docs/sql-reference/data-types/newjson) to reduce storage and improve performance.
- **Avoid setting [`max_dynamic_paths`](/docs/sql-reference/data-types/newjson#reaching-the-limit-of-dynamic-paths-inside-json) too high**—large values increase resource consumption and reduce efficiency. As a rule of thumb, keep it below 10,000\.

Type hintsType hints offer more than just a way to avoid unnecessary type inference—they eliminate storage and processing indirection entirely. JSON paths with type hints are always stored just like traditional columns, bypassing the need for [**discriminator columns**](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse#storage-extension-for-dynamically-changing-data) or dynamic resolution during query time. This means that with well\-defined type hints, nested JSON fields achieve the same performance and efficiency as if they were modeled as top\-level fields from the outset. As a result, for datasets that are mostly consistent but still benefit from the flexibility of JSON, type hints provide a convenient way to preserve performance without needing to restructure your schema or ingest pipeline.
