---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/operations/settings/merge-tree-settings.md)#
topic: mergetree-tables-settings-clickhouse-docs
ch_version_introduced: '10.1016'
last_updated: '2026-06-12'
chunk_index: 29
total_chunks_in_doc: 42
---

and Tuple el ## ratio\_of\_defaults\_for\_sparse\_serialization[​](#ratio_of_defaults_for_sparse_serialization "Direct link to ratio_of_defaults_for_sparse_serialization") Minimal ratio of the number of *default* values to the number of *all* values in a column. Setting this value causes the column to be stored using sparse serializations.

If a column is sparse (contains mostly zeros), ClickHouse can encode it in
a sparse format and automatically optimize calculations \- the data does not
require full decompression during queries. To enable this sparse
serialization, define the `ratio_of_defaults_for_sparse_serialization`
setting to be less than 1\.0\. If the value is greater than or equal to 1\.0,
then the columns will be always written using the normal full serialization.

Possible values:

- Float between `0` and `1` to enable sparse serialization
- `1.0` (or greater) if you do not want to use sparse serialization

**Example**

Notice the `s` column in the following table is an empty string for 95% of
the rows. In `my_regular_table` we do not use sparse serialization, and in
`my_sparse_table` we set `ratio_of_defaults_for_sparse_serialization` to
0\.95:

```
CREATE TABLE my_regular_table
(
`id` UInt64,
`s` String
)
ENGINE = MergeTree
ORDER BY id;

INSERT INTO my_regular_table
SELECT
number AS id,
number % 20 = 0 ? toString(number): '' AS s
FROM
numbers(10000000);


CREATE TABLE my_sparse_table
(
`id` UInt64,
`s` String
)
ENGINE = MergeTree
ORDER BY id
SETTINGS ratio_of_defaults_for_sparse_serialization = 0.95;

INSERT INTO my_sparse_table
SELECT
number,
number % 20 = 0 ? toString(number): ''
FROM
numbers(10000000);

```

Notice the `s` column in `my_sparse_table` uses less storage space on disk:

```
SELECT table, name, data_compressed_bytes, data_uncompressed_bytes FROM system.columns
WHERE table LIKE 'my_%_table';

```

```
┌─table────────────┬─name─┬─data_compressed_bytes─┬─data_uncompressed_bytes─┐
│ my_regular_table │ id   │              37790741 │                75488328 │
│ my_regular_table │ s    │               2451377 │                12683106 │
│ my_sparse_table  │ id   │              37790741 │                75488328 │
│ my_sparse_table  │ s    │               2283454 │                 9855751 │
└──────────────────┴──────┴───────────────────────┴─────────────────────────┘

```

You can verify if a column is using the sparse encoding by viewing the
`serialization_kind` column of the `system.parts_columns` table:

```
SELECT column, serialization_kind FROM system.parts_columns
WHERE table LIKE 'my_sparse_table';

```

You can see which parts of `s` were stored using the sparse serialization:
