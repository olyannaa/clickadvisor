# Change Data Capture (CDC) with PostgreSQL and ClickHouse \- Part 2


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Change Data Capture (CDC) with PostgreSQL and ClickHouse \- Part 2

![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Dale McDiarmid](/authors/dale-mcdiarmid)Jun 15, 2023 · 31 minutes read
> While many of the approaches in this blog post remain valid, the content is from 2023\. For the latest guidance on migrating data from Postgres to ClickHouse, we recommend exploring newer resources \- primarily how ClickPipes, ClickHouse Cloud's managed data ingestion pipeline, now supports ingesting data into [ClickHouse from Postgres using CDC](https://clickhouse.com/docs/integrations/clickpipes/postgres).


## Introduction [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#introduction)


Continuing [our series on building a Change Capture Control (CDC) pipeline for Postgresql to ClickHouse](/blog/clickhouse-postgresql-change-data-capture-cdc-part-1), this post focuses on the steps and configuration required to build a functional pipeline. For this, we use an example dataset loaded into Postgres and ClickHouse. Considering Postgres as the source of truth, we apply a mixed workload of inserts, updates, and deletes. Using a CDC pipeline constructed of Debezium, ClickHouse Kafka Connect, and a materialized view, we can reflect these changes in near\-real time on a table in ClickHouse.


For our examples, we use a development instance in ClickHouse Cloud cluster and an AWS Aurora instance of Postgres. These examples should, however, be reproducible on an equivalently sized self\-managed cluster. Alternatively, [start your ClickHouse Cloud](https://clickhouse.cloud/signUp) cluster today, and receive $300 of credit. Let us worry about the infrastructure and get querying!


## Example dataset [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#example-dataset)


For our example dataset, we use the popular [UK property price dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid). This is of moderate size (28 million rows) with a schema that is easy to reason about. Each row represents a house sale in the UK in the last 20 yrs, with fields representing the price, date, and location. A full description of the fields can be found [here](https://www.gov.uk/guidance/about-the-price-paid-data#explanations-of-column-headers-in-the-ppd). We will load this dataset into Postgres and ClickHouse, before subjecting the former to random inserts, updates, and deletes. These changes should be captured by Debezium and used to update ClickHouse in near real\-time.


### Postgres schema and data loading [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#postgres-schema-and-data-loading)


The Postgres schema is shown below. Note the use of the serial `id` field as the primary key. While a primary key is not mandatory, [an additional Postgres configuration](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-replica-identity) is required for Debezium to work.



```
CREATE TABLE uk_price_paid                                                                                                                                                               (
   id serial,
   price INTEGER,
   date Date,
   postcode1 varchar(8),
   postcode2 varchar(3),
   type varchar(13),
   is_new SMALLINT,
   duration varchar(9),
   addr1 varchar(100),
   addr2 varchar(100),
   street varchar(60),
   locality varchar(35),
   town varchar(35),
   district varchar(40),
   county varchar(35),
   primary key(id)
);

```

We distribute this dataset as Postgres\-compatible SQL, ready for insert, downloadable from [here](https://datasets-documentation.s3.eu-west-3.amazonaws.com/uk-house-prices/postgres/uk_prices.sql.tar.gz). Loading the data requires a few simple commands, assuming the [psql client](https://www.postgresql.org/docs/current/app-psql.html) has been configured with [environment variables](https://www.postgresql.org/docs/current/app-psql.html):



```
wget
https://datasets-documentation.s3.eu-west-3.amazonaws.com/uk-house-prices/postgres/uk_prices.sql.tar.gz
tar -xzvf uk_prices.sql.tar.gz
psql < uk_prices.sql

INSERT 0 10000
INSERT 0 10000
INSERT 0 10000
…

postgres=> SELECT count(*) FROM uk_price_paid;
  count
----------
 27734966
(1 row)

```

Note: we are using an AWS Aurora instance of Postgres version 14\.7 with eight cores. This data takes around 10 minutes to load.


### ClickHouse schema [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#clickhouse-schema)


Below we present a modified version of the schema used in [our documentation](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid), using the ReplacingMergeTree.



```
CREATE TABLE default.uk_price_paid
(
	`id` UInt64,
	`price` UInt32,
	`date` Date,
	`postcode1` LowCardinality(String),
	`postcode2` LowCardinality(String),
	`type` Enum8('other' = 0, 'terraced' = 1, 'semi-detached' = 2, 'detached' = 3, 'flat' = 4),
	`is_new` UInt8,
	`duration` Enum8('unknown' = 0, 'freehold' = 1, 'leasehold' = 2),
	`addr1` String,
	`addr2` String,
	`street` LowCardinality(String),
	`locality` LowCardinality(String),
	`town` LowCardinality(String),
	`district` LowCardinality(String),
	`county` LowCardinality(String),
	`version` UInt64,
	`deleted` UInt8
)
ENGINE = ReplacingMergeTree(version, deleted)
PRIMARY KEY (postcode1, postcode2, addr1, addr2)
ORDER BY (postcode1, postcode2, addr1, addr2, id)

```

While above, we migrated the earlier schema to ClickHouse types for optimization purposes, the original Postgres schema can also be interpreted automatically by ClickHouse (except for the `serial` type). For example, the DDL below could be used to create a table using Postgres types \- these will be automatically converted to ClickHouse types, as shown. Note that we drop the primary key and convert the `id` column of type `serial` to Uint64 manually.



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


![Final CDC schema.png](/uploads/Final_CDC_schema_021b49888b.png)
This architecture assumes the user has an instance of Kafka with the [Kafka Connect framework](https://docs.confluent.io/platform/current/connect/index.html). For our examples, we assume the user is using Confluent Cloud to host Kafka, which auto\-creates an appropriate topic for the events. However, self\-managed Kafka installations are also supported. The proposed schema will work with any ingestion pipeline that writes events generated by Debezium. Instructions for installing Debezium, and considerations for the topic configuration, can be found [here](https://debezium.io/documentation/reference/stable/install.html).


As noted in our previous post, users should ensure the change events are delivered in order for each unique Postgres row (if delete events are to be removed). This can be guaranteed by either using a single partition (Debezium source default) or by using [hash\-based partitioning](https://debezium.io/documentation/reference/stable/transformations/partition-routing.html) for cases where more than a single partition is required due to throughput requirements. While the latter case should be rare, this involves ensuring all change events for a specific Postgres row are sent to the same partition by hashing its primary key.


[Log compaction](https://kafka.apache.org/documentation/#compaction) in Kafka can be used to ensure only the last event for a row is retained, thus minimizing Kafka storage size. This does [require tombstone events](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-delete-events) to be omitted in Debezium when a delete occurs. To simplify our pipeline, we disable these. Users should drop these in their [Kafka Sink](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#configure-kafka-connect-sink) should they need this advanced feature.


### Configuring Postgresql [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#configuring-postgresql)


The PostgreSQL connector can be used with a standalone PostgreSQL server or with a cluster of PostgreSQL servers but is supported on primary servers only \- the Debezium connector cannot connect to a replica instance.


Note [the following](https://debezium.io/documentation/reference/stable/connectors/postgresql.html) from the Debezium documentation:



> “If the primary server fails or is demoted, the connector stops. After the primary server has recovered, you can restart the connector. If a different PostgreSQL server has been promoted to primary, adjust the connector configuration before restarting the connector.”


Ensure the Postgres instance is appropriately configured:


- Self\-managed configuration details [here](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-server-configuration).
- For Cloud\-based environments e.g. Amazon RDS see [here](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-in-the-cloud).


As mentioned in our previous post, we assume the use of the output plugin `pgoutput` to transform the data from the WAL internal representation into a format Debezium can consume. Our examples below, therefore, use logical replication stream mode `pgoutput`. This is built into PostgreSQL 10\+. Users of earlier versions can explore using the [decoderbufs](https://github.com/debezium/postgres-decoderbufs) plugin, which is maintained by the Debezium community or the [wal2json](https://github.com/eulerto/wal2json/blob/master/README.md). We have not tested these configurations.


We recommend users read the following sections regarding security and configuration of users:


- [Setting up basic permissions](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-permissions) \- We use the `postgres` superuser for our example below. This is not advised for production deployments.
- [Privileges to create Publications](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-replication-user-privileges) \- Debezium streams change events for PostgreSQL source tables from publications that are created for the tables. Publications contain a filtered set of change events that are generated from one or more tables. The data in each publication is filtered based on the publication specification. We assume Debezium is configured with sufficient permission to create these publications. By default, the `postgres` super user has permission for this operation. For production use cases, however, we recommend users create these publications themselves or [minimize the permissions](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-replication-user-privileges) of the Debezium user assigned to the connector used to create them.
- [Permissions](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-host-replication-permissions) to allow replication with the Debezium connector host


#### Configuring Replica Identity [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#configuring-replica-identity)


The content of the messages sent by Debezium depends on how you configure `REPLICA IDENTITY` for your source target. `REPLICA IDENTITY` is a PostgreSQL\-specific table\-level setting that determines the amount of information available to the logical decoding plug\-in for UPDATE and DELETE events. More specifically, this setting controls what (if any) information is available for the previous values of the table columns involved whenever an UPDATE or DELETE event occurs.


While four different values are supported, we recommend the following based on whether you need support for deletes:


- `DEFAULT` \- The default behavior is that update and delete events contain the previous values for the primary key columns of a table if that table has a primary key. For an UPDATE event, only the primary key columns with changed values are present. If a table does not have a primary key, the connector does not emit UPDATE or DELETE events for that table. Only use this value if:
	- Your ClickHouse `ORDER BY` clause only contains the Postgres primary key columns. This is unlikely since typically users add columns to the `ORDER BY` to optimize aggregation queries that are unlikely to be primary keys in Postgres.
	- You do not need support for deletes. Note: The configuration used below does not need the previous column values for updates. They are required for deletes as the new state is null.
- `FULL` \- Emitted events for update and delete operations contain the previous values of all columns in the table. This is needed if you need to support delete operations.


Set this setting using the `ALTER` command.



```
ALTER TABLE uk_price_paid REPLICA IDENTITY FULL;

```

The rest of this post assumes the user needs to support deletes. If the steps differ for the case where delete support is not required, we provide references for alternative configurations.


### Prepare ClickHouse [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#prepare-clickhouse)


#### Initial data load [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#initial-data-load)


Prior to handling a stream of change events, we need to preload our ClickHouse table to ensure it is consistent with Postgres. This can be accomplished in a few ways, including but not limited to:


- Using the [postgres table function](https://clickhouse.com/docs/en/sql-reference/table-functions/postgresql) to load the dataset directly from our Postgres instance using an `INSERT INTO SELECT`. This offers a fast and easy way to load our dataset but requires us to pause changes on our Postgres instance. This may not be available in production scenarios.
- Use the Postgres export provided for download. This could be converted into a [format supported](https://clickhouse.com/docs/en/sql-reference/formats) by ClickHouse and loaded. This is unrealistic for most large datasets.
- Configure Debezium to perform a consistent snapshot on first starting. Once the snapshot is complete, it continues streaming changes from the exact point at which the snapshot was made. This allows the connector to start with a consistent view of all of the data, with no changes that were made while the snapshot was being taken being omitted. The full process of how this was achieved is detailed [here](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-snapshots). The result of this process is a stream of read events similar to those sent when a row is inserted. While these can be handled by our materialized view pipeline below, the process tends to be suboptimal with respect to throughput.


For speed and simplicity, we use option one above. Note that our `INSERT INTO SELECT` statement sets the version and deleted columns to the values of 1 and 0, respectively.



```
INSERT INTO uk_price_paid SELECT
	id,
	price,
	date,
	postcode1,
	postcode2,
	type,
	is_new,
	duration,
	addr1,
	addr2,
	street,
	locality,
	town,
	district,
	county,
	1 AS version,
	0 AS deleted
FROM postgresql('<host>', '<database>', '<table>', '<user>', '<password>')

0 rows in set. Elapsed: 80.885 sec. Processed 27.73 million rows, 5.63 GB (342.89 thousand rows/s., 69.60 MB/s.)

```

With no tuning we are able to load all 28m rows in 80 seconds.


#### Materialized views [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#materialized-views)


Debezium uses a nested JSON format to send messages. If configured appropriately (see below), with the `REPLICA IDENTITY` set to the `FULL`, change events will include the before and after values for a row's columns as nested JSON. Full examples of these messages can be found [here](https://github.com/ClickHouse/examples/tree/main/blog-examples/postgresql-cdc/messages), including if `REPLICA IDENTITY` is set to `DEFAULT` when delete support is not required.


As an example we show an update message below (`REPLICA IDENTITY=Full`).



```
{
  "before": {
	"id": 50658675,
	"price": 227500,
	"date": 11905,
	"postcode1": "SP2",
	"postcode2": "7EN",
	"type": "detached",
	"is_new": 0,
	"duration": "freehold",
	"addr1": "31",
	"addr2": "",
	"street": "CHRISTIE MILLER ROAD",
	"locality": "SALISBURY",
	"town": "SALISBURY",
	"district": "SALISBURY",
	"county": "WILTSHIRE"
  },
  "after": {
	"id": 50658675,
	"price": 227500,
	"date": 11905,
	"postcode1": "SP2",
	"postcode2": "7EN",
	"type": "terraced",
	"is_new": 0,
	"duration": "freehold",
	"addr1": "31",
	"addr2": "",
	"street": "CHRISTIE MILLER ROAD",
	"locality": "SALISBURY",
	"town": "SALISBURY",
	"district": "SALISBURY",
	"county": "WILTSHIRE"
  },
  "source": {
	"version": "1.9.6.Final",
	"connector": "postgresql",
	"name": "postgres_server",
	"ts_ms": 1685378780355,
	"snapshot": "false",
	"db": "postgres",
	"sequence": "[\"247833040488\",\"247833042536\"]",
	"schema": "public",
	"table": "uk_price_paid",
	"txId": 106940,
	"lsn": 247833042536,
	"xmin": null
  },
  "op": "u",
  "ts_ms": 1685378780514,
  "transaction": null
}

```

The `op` field here indicates the operation, with the values `u`, `d`, and `c` indicating an update, delete and insert operation, respectively. The `source.lsn` field provides our version value. For delete events, the `after` fields are null. Conversely, for insert events, the `before` fields are null.


This message format is not compatible with our destination table `uk_price_paid` in ClickHouse. We can use a materialized view for transforming these messages at insert time. We show this below:



```
CREATE MATERIALIZED VIEW uk_price_paid_mv TO uk_price_paid
(
   `id` Nullable(UInt64),
   `price` Nullable(UInt32),
   `date` Nullable(Date),
   `postcode1` Nullable(String),
   `postcode2` Nullable(String),
   `type` Nullable(Enum8('other'=0, 'terraced'=1, 'semi-detached'=2, 'detached'=3, 'flat'=4)),
   `is_new` Nullable(UInt8),
   `duration` Nullable(Enum8('unknown'=0, 'freehold'=1, 'leasehold'=2)),
   `addr1` Nullable(String),
   `addr2` Nullable(String),
   `street` Nullable(String),
   `locality` Nullable(String),
   `town` Nullable(String),
   `district` Nullable(String),
   `county` Nullable(String),
   `version` UInt64,
   `deleted` UInt8
) AS
SELECT
   if(op = 'd', before.id, after.id) AS id,
   if(op = 'd', before.price, after.price) AS price,
   if(op = 'd', toDate(before.date), toDate(after.date)) AS date,
   if(op = 'd', before.postcode1, after.postcode1) AS postcode1,
   if(op = 'd', before.postcode2, after.postcode2) AS postcode2,
   if(op = 'd', before.type, after.type) AS type,
   if(op = 'd', before.is_new, after.is_new) AS is_new,
   if(op = 'd', before.duration, after.duration) AS duration,
   if(op = 'd', before.addr1, after.addr1) AS addr1,
   if(op = 'd', before.addr2, after.addr2) AS addr2,
   if(op = 'd', before.street, after.street) AS street,
   if(op = 'd', before.locality, after.locality) AS locality,
   if(op = 'd', before.town, after.town) AS town,
   if(op = 'd', before.district, after.district) AS district,
   if(op = 'd', before.county, after.county) AS county,
   if(op = 'd', source.lsn, source.lsn) AS version,
   if(op = 'd', 1, 0) AS deleted
FROM default.uk_price_paid_changes
WHERE (op = 'c') OR (op = 'r') OR (op = 'u') OR (op = 'd')

```

Notice our materialized view here selects the appropriate value for each column depending on the operation. The `version` is based on the `source.lsn` column, and we set the `deleted` column to 1, if the `op` column has a `d` value and 0 otherwise. The `op = r` value allows us to also support snapshot events if needed. This materialized view [can be simplified](https://github.com/ClickHouse/examples/blob/main/blog-examples/postgresql-cdc/views/create_update.sql) if delete support is not required.


Readers familiar with ClickHouse will notice that this view inserts rows into our `uk_price_paid` and selects rows from a `uk_price_paid_changes` table. This latter table will receive row inserts from our Kafka sink. The schema of this table must align with the Debezium messages shown earlier. We show the schema of this table below:



```
CREATE TABLE uk_price_paid_changes
(
	`before.id` Nullable(UInt64),
	`before.price` Nullable(UInt32),
	`before.date` Nullable(UInt32),
	`before.postcode1` Nullable(String),
	`before.postcode2` Nullable(String),
	`before.type` Nullable(Enum8('other'=0,'terraced'=1,'semi-detached'=2,'detached'=3,'flat'=4)),
	`before.is_new` Nullable(UInt8),
	`before.duration` Nullable(Enum8('unknown' = 0, 'freehold' = 1, 'leasehold' = 2)),
	`before.addr1` Nullable(String),
	`before.addr2` Nullable(String),
	`before.street` Nullable(String),
	`before.locality` Nullable(String),
	`before.town` Nullable(String),
	`before.district` Nullable(String),
	`before.county` Nullable(String),
	`after.id` Nullable(UInt64),
	`after.price` Nullable(UInt32),
	`after.date` Nullable(UInt32),
	`after.postcode1` Nullable(String),
	`after.postcode2` Nullable(String),
	`after.type` Nullable(Enum8('other'=0,'terraced'=1,'semi-detached'=2,'detached'=3,'flat'=4)),
	`after.is_new` Nullable(UInt8),
	`after.duration` Nullable(Enum8('unknown' = 0, 'freehold' = 1, 'leasehold' = 2)),
	`after.addr1` Nullable(String),
	`after.addr2` Nullable(String),
	`after.street` Nullable(String),
	`after.locality` Nullable(String),
	`after.town` Nullable(String),
	`after.district` Nullable(String),
	`after.county` Nullable(String),
	`op` LowCardinality(String),
	`ts_ms` UInt64,
	`source.sequence` String,
	`source.lsn` UInt64
)
ENGINE = MergeTree
ORDER BY tuple()

```

For debugging purposes, we are using a `MergeTree` engine for this table. In production scenarios, this could be a [Null](https://clickhouse.com/docs/en/engines/table-engines/special/null) engine \- changes will then not be persisted, but transformed rows will still be sent to the target table `uk_price_paid`. If delete support is not required, and `REPLICA IDENTITY` is set to `DEFAULT`, [a simpler table](https://github.com/ClickHouse/examples/blob/main/blog-examples/postgresql-cdc/schemas/uk_price_paid_changes_no_delete.sql) can be used.


An astute reader will notice our schema is flattened from the nested messages sent by Debezium. We will do this in our Debezium connector. This is simpler from a schema perspective and allows us to configure the `Nullable` values. Alternatives involving `Tuple` are more complex.


### Configuring Debezium [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#configuring-debezium)


Deploying the connector in the Kafka connect framework requires the following settings. Note how we assume messages are sent as [JSON without a schema](https://docs.confluent.io/platform/current/connect/userguide.html#json-without-sr):


- `value.converter` \- `org.apache.kafka.connect.json.JsonConverter`
- `key.converter` \- `org.apache.kafka.connect.storage.StringConverter`
- `key.converter.schemas.enable` \- `false`
- `value.converter.schemas.enable` \- `false`
- `decimal.format` \- Controls which format this converter will serialize decimals in. This value is case\-insensitive and can be either `BASE64` (default) or `NUMERIC`. This should be set to `BASE64`. For more details on Decimal handling, see [here](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-decimal-types).


A complete list of the required configuration settings for this pipeline, such as database connection details, can be found [here](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-connector-properties). Below we highlight those which most impact the format of messages. **Important**: We configure the connector to track changes at a per table level:


- [plugin.name](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-property-plugin-name) \- The name of the PostgreSQL logical decoding plugin installed on the PostgreSQL server. We recommend `pgoutput`.
- [slot.name](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-property-slot-name) \- Logical decoding slot name. It must be unique to a database and schema. If replicating only one, use `debezium`.
- [publication.name](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-property-publication-name) \- The name of the PostgreSQL publication created for streaming changes when using `pgoutput`. This will be created on startup if you have configured the Postgres user to have [sufficient permissions](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#configuring-postgresql). Alternatively, it can be pre\-created. `dbz_publication` default can be used.
- [table.include.list](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-property-table-include-list) \- An optional, comma\-separated list of regular expressions that match fully\-qualified table identifiers for tables whose changes you want to capture. Ensure the format is `<schema_name>.<table_name>`. For our example, we use `public.uk_price_paid`. **Only one table can be specified in this parameter.**
- [tombstones.on.delete](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-property-tombstones-on-delete) \- Controls whether a delete event is followed by a tombstone event. Set to `false`. It can be set to `true` if you are interested in using [log compaction](https://kafka.apache.org/documentation/#compaction) \- this requires you to drop these tombstones in the ClickHouse Sink.
- [publication.autocreate.mode](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-publication-autocreate-mode) \- Set to `filtered`. This causes a publication to be created for only the table in the property `table.include.list` to be created. Further details [here](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-publication-autocreate-mode).
- [snapshot.mode](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-property-snapshot-mode) \- We utilize `never` for the snapshot mode \- since we loaded the initial data using the `postgres` function. Users can utilize the `initial` mode if they are unable to pause changes to their Postgres instance.
- [decimal.handling.mode](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-decimal-types) \- specifies how the connector should handle values for `DECIMAL` and `NUMERIC` columns. The default value of `precise` will encode these in their binary form, i.e., `java.math.BigDecimal`. Combined with the `decimal.format` setting above, this will cause these to be output in the JSON as numeric. Users may wish to adjust depending on the precision required.


The following settings will impact the delay between changes in Postgres and their arrival time in ClickHouse. Consider these in the context of required SLAs and efficient batching to ClickHouse \- see [Other Considerations](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#other-considerations).


- [max.batch.size](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-property-max-batch-size) \- the maximum size of each batch of events.
- [max.queue.size](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-property-max-queue-size) \- queue size before sending events to Kafka. Allows backpressure. It should be greater than the batch size.
- [poll.interval.ms](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-property-max-queue-size) \- Positive integer value that specifies the number of milliseconds the connector should wait for new change events to appear before it starts processing a batch of events. Defaults to 500 milliseconds.


Confluent provides [additional documentation](https://docs.confluent.io/kafka-connectors/debezium-postgres-source/current/postgres_source_connector_config.html#auto-topic-creation) for those deploying using the Confluent Kafka or Cloud. A Debezium connector can be configured in Confluent Cloud, as shown below. This connector will automatically create a Kafka topic when messages are received.


![debezium_configuration_cdc.gif](/uploads/debezium_configuration_cdc_5e41f3dd3a.gif)
Note above we set the `after.state.only` property to `false`. This setting appears specific to Confluent Cloud and must be set as `false` to ensure the previous values of rows are provided as well as the LSN number.


We also use the SMT capabilities of Kafka connect to [flatten the messages](https://kafka.apache.org/documentation/#org.apache.kafka.connect.transforms.Flatten) and set the Kafka topic to `uk_price_paid_changes`. This can be achieved in self\-manage through configuration. Further details [\[1]\[2]](https://debezium.io/documentation/reference/stable/transformations/topic-routing.html#_example).


In the example above, we have assumed a single partition for our target topic \- this is created by Debezium automatically. As discussed earlier, multiple partitions require the use of [hash\-based routing](https://debezium.io/documentation/reference/stable/transformations/partition-routing.html) to ensure events for the same Postgres row are delivered to the same partition \- thus ensuring in\-order delivery downstream. This is beyond the scope of this blog and requires further testing.


The associated JSON configuration for the above can be found [here](https://github.com/ClickHouse/examples/tree/main/blog-examples/postgresql-cdc/connectors) and can be used with the officially documented [steps](https://docs.confluent.io/cloud/current/connectors/cc-postgresql-cdc-source-debezium.html). Self\-managed installation instructions can be found [here](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-deployment).


### Configure Kafka Connect sink [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#configure-kafka-connect-sink)


We can use the [ClickHouse Kafka Connect](https://github.com/ClickHouse/clickhouse-kafka-connect) sink to read change event messages from Kafka and send them to ClickHouse. This assumes the user is running the Kafka Connect framework. A [number of Kafka Connect Sinks](https://clickhouse.com/docs/en/integrations/kafka#choosing-an-option) can be used with ClickHouse, including the [Confluent HTTP Connector](https://clickhouse.com/docs/en/integrations/kafka#confluent-http-sink-connector). For our use case, however, we choose to use the official [Kafka Connect Sink for ClickHouse](https://clickhouse.com/blog/kafka-connect-connector-clickhouse-with-exactly-once). While the properties of the ReplacingMergeTree only require at\-least\-once semantics, this provides [exactly\-once semantics](https://github.com/ClickHouse/clickhouse-kafka-connect/blob/main/docs/DESIGN.md) and can now be deployed in Confluent Cloud using the "[Custom Connectors](https://docs.confluent.io/cloud/current/connectors/bring-your-connector/overview.html)" offering.


Importantly the Kafka Connect sink guarantees that messages are delivered in order per partition. This is guaranteed by:


- The Kafka Connect framework only assigns [one task to any given partition](https://kafka.apache.org/20/javadoc/org/apache/kafka/connect/sink/SinkTask.html) \- although a task can potentially consume from multiple partitions.
- At insert time, the ClickHouse Kafka Connect sink groups rows by topic and partition prior to inserting. The insert of a batch is acknowledged prior to another batch being consumed.


This allows the number of partitions for a topic to be scaled while still meeting our requirement of in\-order delivery for any changes pertaining to a specific Postgres row, assuming we can guarantee that any events for a row are sent to the same [partition via hashing](https://debezium.io/documentation/reference/stable/transformations/partition-routing.html) from the Debezium connector.


We show configuring the ClickHouse Kafka Connect Sink in Confluent Cloud below. Notice how we first upload the connector package to make it available. This can be downloaded from [here](https://github.com/ClickHouse/clickhouse-kafka-connect/releases). We assume the user has configured the Debezium connector to send data to the topic `uk_price_paid_changes`.


![kafka_connect_config.gif](/uploads/kafka_connect_config_e59fefc4c4.gif)
The JSON representation of the above configuration can be found [here](https://github.com/ClickHouse/examples/blob/main/blog-examples/postgresql-cdc/connectors/kafka_connect.json).


Alternatives to a Kafka Connect\-based approach exist, e.g., users can use [Vector](https://clickhouse.com/docs/en/integrations/kafka#using-vector-with-kafka-and-clickhouse), [Kafka table engine](https://clickhouse.com/docs/en/engines/table-engines/integrations/kafka), or the [HTTP connector](https://clickhouse.com/docs/en/integrations/kafka#confluent-http-sink-connector) offered by Confluent Cloud.


## Testing [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#testing)


To confirm our pipeline is working correctly, we have provided a script that makes random changes to the Postgres table \- adding, updating, and deleting rows. Specifically, regarding updates, this script changes the `type`, `price`, and `is_new` columns for random rows. The full code and dependencies can be found [here](https://github.com/ClickHouse/examples/blob/main/blog-examples/postgresql-cdc/randomize.py).



```
export PGDATABASE=<database>
export PGUSER=postgres
export PGPASSWORD=<password>
export PGHOST=<host>
export PGPORT=5432
pip3 install -r requirements.txt
python randomize.py --iterations 1 --weights "0.4,0.4,0.2" --delay 0.5

```

Note the `weights` parameter and value `0.4,0.4,0.2` denote the ratio of creates, updates, and deletes. The `delay` parameter sets the time delay between each operation (default 0\.5 secs). `iterations` sets the total number of changes to make to the table. In the example above, we modify 1000 rows.


Once the script has finished, we can run the following queries against Postgres and ClickHouse to confirm consistency. The responses shown may differ from your values, as changes are random. The values from both databases should, however, be identical. We use `FINAL` for simplicity.


### Identical row count [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#identical-row-count)



```
-- Postgres
postgres=> SELECT count(*) FROM uk_price_paid;
  count
----------
 27735027
(1 row)


-- ClickHouse
SELECT count()
FROM uk_price_paid
FINAL

┌──count()─┐
│ 27735027 │
└──────────┘

```

### Same price statistics [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#same-price-statistics)



```
-- Postgres
postgres=> SELECT sum(price) FROM uk_price_paid;
     sum
---------------
5945061701495
(1 row)

-- ClickHouse
SELECT sum(price)
FROM uk_price_paid
FINAL

┌────sum(price)─┐
│ 5945061701495 │
└───────────────┘

```

### Same house price distribution [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#same-house-price-distribution)



```
postgres=> SELECT type, count(*) c FROM uk_price_paid GROUP BY type;
 	type  	|	c
---------------+---------
 detached  	| 6399743
 flat      	| 4981171
 other     	|  419212
 semi-detached | 7597039
 terraced  	| 8337862
(5 rows)


-- ClickHouse
SELECT
	type,
	count() AS c
FROM uk_price_paid
FINAL
GROUP BY type

┌─type──────────┬───────c─┐
│ other     	│  419212 │
│ terraced  	│ 8337862 │
│ semi-detached │ 7597039 │
│ detached  	│ 6399743 │
│ flat      	│ 4981171 │
└───────────────┴─────────┘

```

## Other considerations [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#other-considerations)


There are a few other considerations when running a CDC pipeline using Debezium for ClickHouse and Postgres:


- The Debezium connector will batch row changes where possible, up to a max size of the `max.batch.size`. These batches are formed every poll interval `poll.interval.ms` (500ms default). Users can increase these values for larger and more efficient batches at the expense of higher end\-to\-end latency. Remember that ClickHouse prefers batches of at [least 1000](https://clickhouse.com/docs/en/cloud/bestpractices/bulk-inserts) to avoid common issues such as [too many parts](https://clickhouse.com/docs/knowledgebase/exception-too-many-parts). For low throughput environments (\<100 rows per second), this batching is not as critical as ClickHouse will likely keep up with merges. However, users should avoid small batches at a high rate of insert.


Batching can also be configured on the Sink side. This is currently not supported explicitly in the ClickHouse Connect Sink but can be configured through the Kafka connect framework \- see the setting [`consumer.override.max.poll.records`](https://docs.confluent.io/platform/current/installation/configuration/consumer-configs.html#max-poll-records). Alternatively, users can configure [ClickHouse Async inserts](https://clickhouse.com/docs/en/optimize/asynchronous-inserts#enabling-asynchronous-inserts) and allow ClickHouse to batch. In this mode, inserts can be sent as small batches to ClickHouse, which will batch rows before flushing. Note that while flushing, rows will not be searchable. This approach, therefore, \*\*does not \*\*help with end\-to\-end latency.
- Users should be cognizant of [WAL disk usage](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-wal-disk-space) and the importance of [`heartbeat.interval.ms`](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-property-heartbeat-interval-ms) in cases where tables with few changes are being monitored in databases with many updates.
- The above approach **does not currently support Postgres primary key changes**. To implement this, users will need to detect `op=delete` messages from Debezium, which have no `before` or `after` fields. The `id` should then be used to delete these rows in ClickHouse \- preferably using [Lightweight deletes](https://clickhouse.com/docs/en/guides/developer/lightweght-delete). This requires custom code instead of using a Kafka sink for sending data to ClickHouse.
- If the Primary key of a table changes, users will likely need to create a new ClickHouse table with the new column as part of the `ORDER BY` clause. Note this also requires a [process to be performed for the Debezium connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-streaming-changes).
- The logical decoding, on which the Debezium connector depends, does not support DDL changes. This means that the connector is unable to report DDL change events back to consumers.
- Logical decoding replication slots are supported only on primary servers. When there is a cluster of PostgreSQL servers, the connector can run on only the active primary server. It cannot run on hot or warm standby replicas. If the primary server fails or is demoted, the connector stops. After the primary server has recovered, you can restart the connector. If a different PostgreSQL server has been promoted to primary, adjust the connector configuration before restarting the connector.
- While Kafka Sinks can be safely scaled to use more workers (assuming events for the same Postgres row are hashed to the same partition), the Debezium connector allows only a [single task](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-property-tasks-max). The solution proposed above uses a connector per table, allowing the solution to be scaled at a table level.
- The documented approach assumes a connector instance per table. We currently do not support a connector monitoring several tables \- although this may be achievable with topic routing, i.e., messages are routed to a table\-specific topic. This configuration has not yet been tested.


## Conclusion [\#](/blog/clickhouse-postgresql-change-data-capture-cdc-part-2#conclusion)


In this blog post, we have explored how a CDC pipeline can be constructed to replicate changes from Postgres to ClickHouse in near real\-time. We discussed how the ReplacingMergeTree is fundamental to this design and how users can optimize the table design and use the FINAL operator for query time deduplication. As well as providing the instructions for building a pipeline, including how to configure Debezium, we have discussed other considerations for users wanting to build a production solution. While the details in this blog post are specific to Postgres, they can potentially be applied to all source databases supported by Debezium thanks to its DBMS\-independent message format. We leave this as an exercise for the reader to explore other databases and let us know how you get on!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
