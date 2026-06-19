---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/engines/table-engines/mergetree-family/textindexes.md)#
topic: full-text-search-with-text-indexes-clickhouse-docs
ch_version_introduced: '192.168'
last_updated: '2026-06-12'
chunk_index: 16
total_chunks_in_doc: 24
---

'some_token'_String) UInt8 : 2 [...] ``` whereas the same query run with `query_plan_direct_read_from_text_index = 1` ``` EXPLAIN PLAN actions = 1 SELECT count() FROM table WHERE hasToken(col, 'some_token') SETTINGS query_plan_direct_read_from_text_index = 1, -- enable direct read ``` returns

```
[...]
Expression (Before GROUP BY)
Positions:
  Filter
  Filter column: __text_index_idx_hasToken_94cc2a813036b453d84b6fb344a63ad3 (removed)
  Actions: INPUT :: 0 -> __text_index_idx_hasToken_94cc2a813036b453d84b6fb344a63ad3 UInt8 : 0
[...]

```

The second EXPLAIN PLAN output contains a virtual column `__text_index_<index_name>_<function_name>_<id>`.
If this column is present, then direct read is used.

If the WHERE filter clause only contains text search functions, the query can avoid reading the column data entirely and has the greatest performance benefit by direct read.
However, even if the text column is accessed elsewhere in the query, direct read will still provide performance improvement.

**Direct read as a hint**

Direct read as a hint is based on the same principles as normal direct read, but instead adds an additional filter build from the text index data without removing the underlying text column.
It is used for functions when reading only from the text index would produce false positives.

Supported functions are: `like`, `startsWith`, `endsWith`, `equals`, `has`, `hasPhrase`, `mapContainsKey`, and `mapContainsValue`.

The additional filter can provide additional selectivity to restrict the result set in combination with other filters further, helping to reduce the amount of data read from other columns.

Direct read as a hint is controlled by setting [query\_plan\_text\_index\_add\_hint](/docs/operations/settings/settings#query_plan_text_index_add_hint) (enabled by default).

Example of query without hint:

```
EXPLAIN actions = 1
SELECT count()
FROM table
WHERE (col LIKE '%some-token%') AND (d >= today())
SETTINGS query_plan_text_index_add_hint = 0
FORMAT TSV

```

returns

```
[...]
Prewhere filter column: and(like(__table1.col, \'%some-token%\'_String), greaterOrEquals(__table1.d, _CAST(20440_Date, \'Date\'_String))) (removed)
[...]

```

whereas the same query run with `query_plan_text_index_add_hint = 1`

```
EXPLAIN actions = 1
SELECT count()
FROM table
WHERE col LIKE '%some-token%'
SETTINGS query_plan_text_index_add_hint = 1

```

returns

```
[...]
Prewhere filter column: and(__text_index_idx_col_like_d306f7c9c95238594618ac23eb7a3f74, like(__table1.col, \'%some-token%\'_String), greaterOrEquals(__table1.d, _CAST(20440_Date, \'Date\'_String))) (removed)
[...]

```
