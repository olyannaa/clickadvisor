---
source: blog
url: https://clickhouse.com/docs/integrations/clickpipes/postgres
topic: change-data-capture-cdc-with-postgresql-and-clickhouse-part-2
ch_version_introduced: '80.885'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 17
---

be used to create a table using Postgres types \- these will be automatically converted to ClickHouse types, as shown. Note that we drop the primary key and convert the `id` column of type `serial` to Uint64 manually.

```
CREATE TABLE default.uk_price_paid
(
    `id` UInt64,
    `price` INTEGER,
    `date` Date,
    `postcode1` varchar(8),
    `postcode2` varchar(3),
    `type` varchar(13),
    `is_new` SMALLINT,
    `duration` varchar(9),
    `addr1` varchar(100),
    `addr2` varchar(100),
    `street` varchar(60),
    `locality` varchar(35),
    `town` varchar(35),
    `district` varchar(40),
    `county` varchar(35),
    `version` UInt64,
    `deleted` UInt8
)
ENGINE = ReplacingMergeTree(version, deleted)
PRIMARY KEY (postcode1, postcode2, addr1, addr2)
ORDER BY (postcode1, postcode2, addr1, addr2, id)

SHOW CREATE TABLE default.uk_price_paid

CREATE TABLE default.uk_price_paid
(
    `id` UInt64,
    `price` Int32,
    `date` Date,
    `postcode1` String,
    `postcode2` String,
    `type` String,
    `is_new` Int16,
    `duration` String,
    `addr1` String,
    `addr2` String,
    `street` String,
    `locality` String,
    `town` String,
    `district` String,
    `county` String,
    `version` UInt64,
    `deleted` UInt8
)
ENGINE = ReplicatedReplacingMergeTree('/clickhouse/tables/{uuid}/{shard}', '{replica}', version, deleted)
PRIMARY KEY (postcode1, postcode2, addr1, addr2)
ORDER BY (postcode1, postcode2, addr1, addr2, id)
SETTINGS index_granularity = 8192

```

Considering the concepts explored in our previous blog around the ReplacingMergeTree engine, there are some important notes here:

- We use the version and deleted columns in our table definition. Both of these are optional. For example, if you don’t need to support deletes, simply omit the column in the schema and engine definition.
- We have selected columns for our `ORDER BY` clause optimizing for query access patterns. Note how the `id` column is specified last, as we don’t expect these to be used in analytical queries but still need the uniqueness property it provides \- especially as our addresses do not go beyond street level.
- We specify the primary index using the `PRIMARY KEY` clause, omitting the `id` column to save memory with no impact on our usual queries.

## Configuring a CDC pipeline [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#configuring-a-cdc-pipeline)

### Architectural overview [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#architectural-overview)

The end\-to\-end architecture we presented in our [previous blog](https://clickhouse.com/blog/clickhouse-postgresql-change-data-capture-cdc-part-1)), is shown below.
