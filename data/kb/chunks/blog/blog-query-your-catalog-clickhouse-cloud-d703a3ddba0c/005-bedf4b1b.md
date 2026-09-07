---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"If
topic: if-it-s-in-your-catalog-you-can-query-it-the-datalakecatalog-engine-in-clickhouse-cloud-clickhouse
ch_version_introduced: '27.8'
last_updated: '2026-09-07'
chunk_index: 5
total_chunks_in_doc: 10
---

aws_access_key_id = '...', aws_secret_access_key = '...', allow_database_glue_catalog = 1; -- beta feature in Cloud ``` Copy command > The `glue` database we created in ClickHouse Cloud acts as a **local proxy for the remote AWS Glue Catalog**. ![Blog-Catalogs.005.png](/_next/image?url=%2Fuploads%2FBlog_Catalogs_005_2ed78443d2.png&w=2048&q=75)

It behaves like a normal ClickHouse database, supporting the same metadata lookups and queries you’d use on native databases.

### Exploring metadata \#

Now that the AWS Glue Catalog is connected, we can run the usual metadata lookups available in any ClickHouse database, for example, listing all tables:

```
SHOW tables FROM glue;
```
Copy command

```
┌─name──────────────────────────────────────────────────┐
│ agenthouse.player_match_history                       │
│ clickhouse_datalake_demo.player_match_history_delta   │
│ clickhouse_datalake_demo.player_match_history_iceberg │
│ clickhouse_datalake_demo.pypi_delta_flat              │
│ clickhouse_datalake_demo.pypi_delta_part              │
│ clickhouse_datalake_demo.pypi_iceberg_flat            │
│ clickhouse_datalake_demo.pypi_iceberg_part            │
│ clickhouse_datalake_demo.pypi_parquet                 │
│ clickhouse_datalake_demo.pypi_test_iceberg_flat       │
│ clickhouse_datalake_demo.pypi_test_iceberg_part       │
│ openhouse.player_match_history_iceberg_p              │
└───────────────────────────────────────────────────────┘
```
Copy command
We can inspect the DDL of our example table directly from the connected Glue Catalog:

```
SHOW CREATE TABLE glue.`openhouse.player_match_history_iceberg_p`;
```
Copy command

```
┌─statement──────────────────────────────────────────────────────┐
│ CREATE TABLE glue.`openhouse.player_match_history_iceberg_p`  ↴│
│↳(                                                             ↴│
│↳    `account_id` Nullable(Int64),                             ↴│
│↳    `match_id` Nullable(Int64),                               ↴│
│↳    `hero_id` Nullable(Int64),                                ↴│
│↳    `hero_level` Nullable(Int64),                             ↴│
│↳    `start_time` Nullable(Int64),                             ↴│
│↳    `game_mode` Nullable(Int32),                              ↴│
│↳    `match_mode` Nullable(Int32),                             ↴│
│↳    `player_team` Nullable(Int32),                            ↴│
│↳    `player_kills` Nullable(Int64),                           ↴│
│↳    `player_deaths` Nullable(Int64),                          ↴│
│↳    `player_assists` Nullable(Int64),                         ↴│
│↳    `denies` Nullable(Int64),                                 ↴│
│↳    `net_worth` Nullable(Int64),                              ↴│
│↳    `last_hits` Nullable(Int64),                              ↴│
│↳    `team_abandoned` Nullable(Bool),                          ↴│
│↳    `abandoned_time_s` Nullable(Int64),                       ↴│
│↳    `match_duration_s` Nullable(Int64),                       ↴│
│↳    `match_result` Nullable(Int64),                           ↴│
│↳    `objectives_mask_team0` Nullable(Int64),                  ↴│
│↳    `objectives_mask_team1` Nullable(Int64),                  ↴│
│↳    `created_at` Nullable(DateTime64(6)),                     ↴│
│↳    `event_day` Nullable(String),                             ↴│
│↳    `event_month` Nullable(String)                            ↴│
│↳)                                                             ↴│
│↳ENGINE = Iceberg('s3://clickhouse-datalake-demo/              ↴│
│↳                  data/openhouse_managed/                     ↴│
│                   player_match_history_iceberg_p')             │
└────────────────────────────────────────────────────────────────┘
```
Copy command
Notice that the table’s **engine is [Iceberg](https://clickhouse.com/docs/engines/table-engines/integrations/iceberg)**, the built\-in ClickHouse [table engine](https://clickhouse.com/docs/academic_overview#5-integration-layer) for reading Apache Iceberg data. The data itself lives remotely in **Amazon S3**.

> While we could have used the Iceberg engine directly by specifying the S3 path manually, the **DataLakeCatalog** [database engine](https://clickhouse.com/docs/academic_overview#5-integration-layer) does this automatically by reading metadata from the AWS Glue Catalog.

Since the catalog entry identifies `player_match_history_iceberg_p` as an **Iceberg** table, ClickHouse transparently routes the query through its **Iceberg engine**, leveraging all standard Iceberg optimizations (a topic for another post).

The diagram below summarizes how this works end\-to\-end:

![Blog-Catalogs.006.png](/_next/image?url=%2Fuploads%2FBlog_Catalogs_006_e8a5d41241.png&w=2048&q=75)

### Querying Iceberg data \#
