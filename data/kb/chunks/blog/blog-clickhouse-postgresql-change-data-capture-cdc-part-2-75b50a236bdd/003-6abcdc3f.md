---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Change
topic: change-data-capture-cdc-with-postgresql-and-clickhouse-part-2-clickhouse
ch_version_introduced: '80.885'
last_updated: '2026-09-07'
chunk_index: 3
total_chunks_in_doc: 19
---

AWS Aurora instance of Postgres version 14\.7 with eight cores. This data takes around 10 minutes to load. ### ClickHouse schema \# Below we present a modified version of the schema used in [our documentation](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid), using the ReplacingMergeTree.

```
1CREATE TABLE default.uk_price_paid
2(
3	`id` UInt64,
4	`price` UInt32,
5	`date` Date,
6	`postcode1` LowCardinality(String),
7	`postcode2` LowCardinality(String),
8	`type` Enum8('other' = 0, 'terraced' = 1, 'semi-detached' = 2, 'detached' = 3, 'flat' = 4),
9	`is_new` UInt8,
10	`duration` Enum8('unknown' = 0, 'freehold' = 1, 'leasehold' = 2),
11	`addr1` String,
12	`addr2` String,
13	`street` LowCardinality(String),
14	`locality` LowCardinality(String),
15	`town` LowCardinality(String),
16	`district` LowCardinality(String),
17	`county` LowCardinality(String),
18	`version` UInt64,
19	`deleted` UInt8
20)
21ENGINE = ReplacingMergeTree(version, deleted)
22PRIMARY KEY (postcode1, postcode2, addr1, addr2)
23ORDER BY (postcode1, postcode2, addr1, addr2, id)
```
Copy command
While above, we migrated the earlier schema to ClickHouse types for optimization purposes, the original Postgres schema can also be interpreted automatically by ClickHouse (except for the `serial` type). For example, the DDL below could be used to create a table using Postgres types \- these will be automatically converted to ClickHouse types, as shown. Note that we drop the primary key and convert the `id` column of type `serial` to Uint64 manually.
