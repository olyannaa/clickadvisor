---
source: blog
url: https://clickhouse.com/blog/hifis-migration-from-bigquery-to-clickhouse
topic: clickhouse-vs-bigquery-using-clickhouse-to-serve-real-time-queries-on-top-of-bigquery-data
ch_version_introduced: '22.712'
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 20
---

which offers multiple precisions for decimals, [floats](https://clickhouse.com/docs/en/sql-reference/data-types/float), and [ints](https://clickhouse.com/docs/en/sql-reference/data-types/int-uint). With these, ClickHouse users can optimize storage and memory overhead, resulting in faster queries and lower resource consumption. Below we map the equivalent ClickHouse type for each BigQuery type:

| **BigQuery** | **ClickHouse** |
| --- | --- |
| [ARRAY](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#array_type) | [Array(t)](https://clickhouse.com/docs/en/sql-reference/data-types/array) |
| [NUMERIC](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#decimal_types) | [Decimal(P, S), Decimal32(S), Decimal64(S), Decimal128(S)](https://clickhouse.com/docs/en/sql-reference/data-types/decimal) |
| [BIG NUMERIC](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#decimal_types) | [Decimal256(S)](https://clickhouse.com/docs/en/sql-reference/data-types/decimal) |
| [BOOL](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#boolean_type) | [Bool](https://clickhouse.com/docs/en/sql-reference/data-types/boolean) |
| [BYTES](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#bytes_type) | [FixedString](https://clickhouse.com/docs/en/sql-reference/data-types/fixedstring) |
| [DATE](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#date_type) | [Date32](https://clickhouse.com/docs/en/sql-reference/data-types/date32) (with narrower range) |
| [DATETIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#datetime_type) | [DateTime](https://clickhouse.com/docs/en/sql-reference/data-types/datetime), [DateTime64](https://clickhouse.com/docs/en/sql-reference/data-types/datetime64) (narrow range, higher precision) |
| [FLOAT64](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#floating_point_types) | [Float64](https://clickhouse.com/docs/en/sql-reference/data-types/float) |
| [GEOGRAPHY](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#geography_type) | [Geo Data Types](https://clickhouse.com/docs/en/sql-reference/data-types/geo) |
| [INT64](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#integer_types) | [UInt8, UInt16, UInt32, UInt64, UInt128, UInt256, Int8, Int16, Int32, Int64, Int128, Int256](https://clickhouse.com/docs/en/sql-reference/data-types/int-uint) |
| [INTERVAL](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#integer_types) | NA [supported as expression](https://clickhouse.com/docs/en/sql-reference/data-types/special-data-types/interval/#usage-remarks) or [through functions](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions/#addyears-addmonths-addweeks-adddays-addhours-addminutes-addseconds-addquarters) |
| [JSON](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#json_type) | [JSON](https://clickhouse.com/docs/en/guides/developer/working-with-json/json-semi-structured/#relying-on-schema-inference) |
| [STRING](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#string_type) | [String (bytes)](https://clickhouse.com/docs/en/sql-reference/data-types/string) |
| [STRUCT](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#constructing_a_struct) | [Tuple](https://clickhouse.com/docs/en/sql-reference/data-types/tuple), [Nested](https://clickhouse.com/docs/en/sql-reference/data-types/nested-data-structures/nested) |
| [TIME](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#time_type) | [DateTime64](https://clickhouse.com/docs/en/sql-reference/data-types/datetime64) |
| [TIMESTAMP](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#timestamp_type) | [DateTime64](https://clickhouse.com/docs/en/sql-reference/data-types/datetime64) |





When presented with multiple options for ClickHouse types, consider the actual range of the data and pick the lowest required. Also, consider utilizing [appropriate codecs](https://clickhouse.com/blog/optimize-clickhouse-codecs-compression-schema) for further compression.

The current schema for a BigQuery table can be retrieved with the following query:

```
SELECT table_name, ddl FROM `bigquery-public-data`.crypto_ethereum.INFORMATION_SCHEMA.TABLES
WHERE  table_name = 'blocks';

```

The original BigQuery schemas can be found [here](https://github.com/blockchain-etl/ethereum-etl/blob/develop/docs/schema.md#blockscsv). Using the results from the above queries, we can create a ClickHouse table with appropriate types based on the known ranges of each column. You can run an additional query to identify the data range and cardinality, for example:

```
SELECT
 MAX(number) AS max_number, 
 MIN(number) AS min_number, 
 MAX(size) AS max_size, 
 MIN(size) AS min_size
FROM bigquery-public-data.crypto_ethereum.blocks

max_number    min_number    max_size    min_size
16547585    0    1501436    514

```

We make some basic optimizations to these schemas with appropriate types and codecs to minimize storage, but leave a full analysis to a later blog dedicated to this dataset. The schema for blocks:

```
CREATE TABLE ethereum.blocks
(
    `number` UInt32 CODEC(Delta(4), ZSTD(1)),
    `hash` String,
    `parent_hash` String,
    `nonce` String,
    `sha3_uncles` String,
    `logs_bloom` String,
    `transactions_root` String,
    `state_root` String,
    `receipts_root` String,
    `miner` String,
    `difficulty` Decimal(38, 0),
    `total_difficulty` Decimal(38, 0),
    `size` UInt32 CODEC(Delta(4), ZSTD(1)),
    `extra_data` String,
    `gas_limit` UInt32 CODEC(Delta(4), ZSTD(1)),
    `gas_used` UInt32 CODEC(Delta(4), ZSTD(1)),
    `timestamp` DateTime CODEC(Delta(4), ZSTD(1)),
    `transaction_count` UInt16,
    `base_fee_per_gas` UInt64
)
ENGINE = MergeTree
ORDER BY timestamp

```
