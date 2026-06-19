---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/newjson.md)#
topic: json-data-type-clickhouse-docs
ch_version_introduced: '42.42'
last_updated: '2026-06-12'
chunk_index: 15
total_chunks_in_doc: 26
---

however, depend on the implementation. Let's see an example of such a merge. First, let's create a table with a `JSON` column, set the limit of dynamic paths to `3` and then insert values with `5` different paths:

```
CREATE TABLE test (id UInt64, json JSON(max_dynamic_paths=3)) ENGINE=MergeTree ORDER BY id;
SYSTEM STOP MERGES test;
INSERT INTO test SELECT number, formatRow('JSONEachRow', number as a) FROM numbers(5);
INSERT INTO test SELECT number, formatRow('JSONEachRow', number as b) FROM numbers(4);
INSERT INTO test SELECT number, formatRow('JSONEachRow', number as c) FROM numbers(3);
INSERT INTO test SELECT number, formatRow('JSONEachRow', number as d) FROM numbers(2);
INSERT INTO test SELECT number, formatRow('JSONEachRow', number as e) FROM numbers(1);

```

Each insert will create a separate data part with the `JSON` column containing a single path:

```
SELECT
    count(),
    groupArrayArrayDistinct(JSONDynamicPaths(json)) AS dynamic_paths,
    groupArrayArrayDistinct(JSONSharedDataPaths(json)) AS shared_data_paths,
    _part
FROM test
GROUP BY _part
ORDER BY _part ASC

```

```
┌─count()─┬─dynamic_paths─┬─shared_data_paths─┬─_part─────┐
│       5 │ ['a']         │ []                │ all_1_1_0 │
│       4 │ ['b']         │ []                │ all_2_2_0 │
│       3 │ ['c']         │ []                │ all_3_3_0 │
│       2 │ ['d']         │ []                │ all_4_4_0 │
│       1 │ ['e']         │ []                │ all_5_5_0 │
└─────────┴───────────────┴───────────────────┴───────────┘

```

Now, let's merge all parts into one and see what will happen:

```
SELECT
    count(),
    groupArrayArrayDistinct(JSONDynamicPaths(json)) AS dynamic_paths,
    groupArrayArrayDistinct(JSONSharedDataPaths(json)) AS shared_data_paths,
    _part
FROM test
GROUP BY _part
ORDER BY _part ASC

```

```
┌─count()─┬─dynamic_paths─┬─shared_data_paths─┬─_part─────┐
│      15 │ ['a','b','c'] │ ['d','e']         │ all_1_5_2 │
└─────────┴───────────────┴───────────────────┴───────────┘

```

As we can see, ClickHouse kept the most frequent paths `a`, `b` and `c` and moved paths `d` and `e` to a shared data structure.

## Shared data structure[​](#shared-data-structure "Direct link to Shared data structure")

As was described in the previous section, when the `max_dynamic_paths` limit is reached all new paths are stored in a single shared data structure.
In this section we will look into the details of the shared data structure and how we read paths sub\-columns from it.

See section ["introspection functions"](/docs/sql-reference/data-types/newjson#introspection-functions) for details of functions used for inspecting the contents of a JSON column.

### Shared data structure in memory[​](#shared-data-structure-in-memory "Direct link to Shared data structure in memory")
