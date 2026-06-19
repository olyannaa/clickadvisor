# How to test different compression codecs \| Altinity® Knowledge Base for ClickHouse®


1. [Schema design](/altinity-kb-schema-design/)
2. [Codecs](/altinity-kb-schema-design/codecs/)
3. How to test different compression codecs
# How to test different compression codecs

## Example

Create test\_table based on the source table.


```
CREATE TABLE test_table AS source_table ENGINE=MergeTree() PARTITION BY ...;

```
If the source table has Replicated\*MergeTree engine, you would need to change it to non\-replicated.

Attach one partition with data from the source table to test\_table.


```
ALTER TABLE test_table ATTACH PARTITION ID '20210120' FROM source_table;

```
You can modify the column or create a new one based on the old column value.


```
ALTER TABLE test_table MODIFY COLUMN column_a CODEC(ZSTD(2));
ALTER TABLE test_table ADD COLUMN column_new UInt32
                         DEFAULT toUInt32OrZero(column_old) CODEC(T64,LZ4);

```
After that, you would need to populate changed columns with data.


```
ALTER TABLE test_table UPDATE column_a=column_a, column_new=column_new WHERE 1;

```
You can look status of mutation via the `system.mutations` table


```
SELECT * FROM system.mutations;

```
And it’s also possible to kill mutation if there are some problems with it.


```
KILL MUTATION WHERE ...

```
## Useful queries


```
SELECT
    database,
    table,
    count() AS parts,
    uniqExact(partition_id) AS partition_cnt,
    sum(rows),
    formatReadableSize(sum(data_compressed_bytes) AS comp_bytes) AS comp,
    formatReadableSize(sum(data_uncompressed_bytes) AS uncomp_bytes) AS uncomp,
    uncomp_bytes / comp_bytes AS ratio
FROM system.parts
WHERE active
GROUP BY
    database,
    table
ORDER BY comp_bytes DESC

```

```
SELECT
  database,
  table,
  column,
  type,
  sum(rows) AS rows,
  sum(column_data_compressed_bytes) AS compressed_bytes,
  formatReadableSize(compressed_bytes) AS compressed,
  formatReadableSize(sum(column_data_uncompressed_bytes)) AS uncompressed,
  sum(column_data_uncompressed_bytes) / compressed_bytes AS ratio,
  any(compression_codec) AS codec
FROM system.parts_columns AS pc
LEFT JOIN system.columns AS c
ON (pc.database = c.database) AND (c.table = pc.table) AND (c.name = pc.column)
WHERE (database LIKE '%') AND (table LIKE '%') AND active
GROUP BY
  database,
  table,
  column,
  type
ORDER BY database, table, sum(column_data_compressed_bytes) DESC

```
Last modified 2021\.08\.12: [General corrections and updates. (876b7b6\)](https://github.com/Altinity/altinityknowledgebase/commit/876b7b6ff51841633719a018675a096a09a68eaa)
