---
source: kb.altinity.com
url: http://altinity.com/
topic: altinity-knowledge-base-for-clickhouse
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 174
total_chunks_in_doc: 478
---

query): 226.04 MiB. Elapsed: 5.700 sec. Processed 11.53 million rows, 92.23 MB (2.02 million rows/s., 16.18 MB/s.) ``` Almost 100 times faster than first query! # 3\.6 \- assumeNotNull and friends assumeNotNull and friends`assumeNotNull` result is implementation specific:

```
WITH CAST(NULL, 'Nullable(UInt8)') AS column
SELECT
    column,
    assumeNotNull(column + 999) AS x;

┌─column─┬─x─┐
│   null │ 0 │
└────────┴───┘

WITH CAST(NULL, 'Nullable(UInt8)') AS column
SELECT
    column,
    assumeNotNull(materialize(column) + 999) AS x;

┌─column─┬───x─┐
│   null │ 999 │
└────────┴─────┘

CREATE TABLE test_null
(
    `key` UInt32,
    `value` Nullable(String)
)
ENGINE = MergeTree
ORDER BY key;

INSERT INTO test_null SELECT
    number,
    concat('value ', toString(number))
FROM numbers(4);

SELECT *
FROM test_null;

┌─key─┬─value───┐
│   0 │ value 0 │
│   1 │ value 1 │
│   2 │ value 2 │
│   3 │ value 3 │
└─────┴─────────┘

ALTER TABLE test_null
    UPDATE value = NULL WHERE key = 3;

SELECT *
FROM test_null;

┌─key─┬─value───┐
│   0 │ value 0 │
│   1 │ value 1 │
│   2 │ value 2 │
│   3 │ null    │
└─────┴─────────┘

SELECT
    key,
    assumeNotNull(value)
FROM test_null;

┌─key─┬─assumeNotNull(value)─┐
│   0 │ value 0              │
│   1 │ value 1              │
│   2 │ value 2              │
│   3 │ value 3              │
└─────┴──────────────────────┘

WITH CAST(NULL, 'Nullable(Enum8(\'a\' = 1, \'b\' = 0))') AS test
SELECT assumeNotNull(test)

┌─assumeNotNull(test)─┐
│ b                   │
└─────────────────────┘

WITH CAST(NULL, 'Nullable(Enum8(\'a\' = 1))') AS test
SELECT assumeNotNull(test)

Error on processing query 'with CAST(null, 'Nullable(Enum8(\'a\' = 1))') as test
select assumeNotNull(test); ;':
Code: 36, e.displayText() = DB::Exception: Unexpected value 0 in enum, Stack trace (when copying this message, always include the lines below):

```
#### Info

Null values in ClickHouse® are stored in a separate dictionary: is this value Null. And for faster dispatch of functions there is no check on Null value while function execution, so functions like plus can modify internal column value (which has default value). In normal conditions it’s not a problem because on read attempt, ClickHouse first would check the Null dictionary and return value from column itself for non\-Nulls only. And `assumeNotNull` function just ignores this Null dictionary. So it would return only column values, and in certain cases it’s possible to have unexpected results.If it’s possible to have Null values, it’s better to use `ifNull` function instead.
