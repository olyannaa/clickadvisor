# Consuming the Delta Lake Change Data Feed for CDC


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Consuming the Delta Lake Change Data Feed for CDC

![](/_next/image?url=%2Fuploads%2Fkelsey_s_avatar_a033778296.jpg&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fpete_h_avatar_b5e79cbc11.jpg&w=96&q=75)Pete Hampton \& Kelsey SchlarmanAug 19, 2025 · 23 minutes readAs part of the ClickPipes team at ClickHouse, we develop high\-performance, managed connectors for moving data from various data sources to ClickHouse. After building Change Data Capture (CDC) connectors for [Postgres](https://clickhouse.com/docs/integrations/clickpipes/postgres%20), [MySQL](https://clickhouse.com/docs/integrations/clickpipes/mysql), and [MongoDB](https://clickhouse.com/cloud/clickpipes/mongodb-cdc-connector), we’re now looking at supporting CDC from data lake sources, starting with [Delta Lake](https://delta.io/).


In this post, we share everything we have learnt from our investigation into working with [Delta Lake’s Change Data Feed (CDF)](https://docs.delta.io/latest/delta-change-data-feed.html). On top, we’re [open sourcing an MIT\-licensed, reference implementation of CDC from Delta Lake to ClickHouse in Python.](https://github.com/ClickHouse/deltalake-cdc)



> We plan to add production\-grade support for Delta Lake CDC in ClickPipes in the coming months. If you're interested in partnering with us as a design partner, please email **[clickpipes@clickhouse.com](mailto:clickpipes@clickhouse.com)**.


## Delta Lake and ClickHouse [\#](/blog/consuming-delta-lake-change-data-feed-cdc#delta-lake-and-clickhouse)


Delta Lake provides a transactional storage layer on top of object storage, which is ideal for data ingestion and processing petabyte\-scale volumes of data. ClickHouse, on the other hand, is an open\-source, columnar database optimised for high\-performance analytical queries. Combining these technologies allows users to leverage the strengths of both: Delta Lake for [data lakehouse](https://clickhouse.com/resources/engineering/data-lakehouse) concerns and ClickHouse for fast, real\-time data access. ClickHouse can already be used as a read\-only query engine on your Delta Lake parquet using the **DeltaLake** or **deltaLakeCluster** table engines, with [write support](https://github.com/ClickHouse/ClickHouse/issues/79603) coming soon.



```

```
CREATE TABLE my_delta_table
ENGINE = DeltaLake('s3://path/to/deltalake/table', 'access-key', 'secret-key')
```


```

The schema is automatically inferred from Delta Lake metadata and can be queried like so:



```

```
SELECT col1, col2, col3, _file, _time, …etc 
FROM my_delta_table
```


```

For more ad\-hoc queries, the table functions **deltaLake** and **deltaLakeCluster** can be used to query data in place:



```

```
SELECT col1, col2, col3, _file, _time, …etc 
FROM deltaLake('s3://path/to/deltalake/table', 'access-key', 'secret-key')
```


```

Using ClickHouse as the query layer for your Delta tables is an effective strategy if the data is mostly cold and not frequently queried, and you are willing to tolerate the performance of remote object storage reads, without a need for duplication across your lakehouse\-warehouse. Some users could benefit from frequent, latency\-sensitive reads, likely using ClickHouse for real\-time data access used by other systems \- such as APIs, dashboards, recommender systems or other user\-facing applications. Furthermore, even with optimisation techniques such as caching, remote object storage scans can be slower and costly, making data residency in ClickHouse a compelling interface for such use cases.


Change Data Capture (CDC) is a process for replicating incremental changes from a Delta Lake table, typically after a snapshot of the data. This reduces data transfer overhead and ensures that ClickHouse always reflects the latest state of the data in the delta table with minimal latency.


## Key components of the pipeline [\#](/blog/consuming-delta-lake-change-data-feed-cdc#key-components-of-the-pipeline)


A CDC pipeline from Delta Lake to ClickHouse would involve the following core components:


- **Delta Lake table(s):** The source data lake where data is persisted.
- **Change Data Feed (CDF):** Delta Lake's mechanism for capturing row\-level changes.
- **ClickHouse:** The destination database to enable real\-time usage of the data.


### Data modelling [\#](/blog/consuming-delta-lake-change-data-feed-cdc#data-modelling)


Due to the eventually consistent reconciliation of the upstream state, we use the ClickHouse ReplacingMergeTree table engine, a variant of MergeTree that is helpful in CDC workflows to resolve duplication or out\-of\-order data ingest (such as insert, then delete, then update operations). These techniques more or less [align with Postgres data modelling guidance provided in the past](https://clickhouse.com/blog/postgres-to-clickhouse-data-modeling-tips-v2). A ClickHouse table can be created with the below DDL, with an `name` and `age` as our ordering key and the `_commit_version` from the Delta Table CDF as our version key. For append\-only workflows with no update or delete operations, a MergeTree table would provide more optimal query conditions.



```

```
CREATE TABLE default.new_cdc_table
(
    `id` String,
    `name` String,
    `age` Int64,
    `created_at` DateTime,
    `_change_type` String,
    `_commit_version` Int64,
    `_commit_timestamp` DateTime
)
ENGINE = ReplacingMergeTree(`_commit_version`)
PARTITION BY toYYYYMM(`created_at`)
ORDER BY (`name`, `age`)
```


```

This table definition configures deduplication based on the primary key. When duplicates are found during merges, ClickHouse keeps only one row per unique key combination. Adding a version column (in this case, **\_commit\_version**) signals to ClickHouse to retain the row with the highest commit version. If no version column is specified, ClickHouse defaults to the last inserted row, which is typically not optimal for eventually consistent use cases such as CDC. This pattern of data insertion is well established and is what we use in the internals of the [Postgres](https://clickhouse.com/docs/integrations/clickpipes/postgres) and [MySQL](https://clickhouse.com/docs/integrations/clickpipes/mysql) CDC processes with ClickPipes and PeerDB.


There are a few caveats to consider when using the ReplacingMergeTree to model CDC data. The first is merge timing \- unlike UPSERT operations in traditional RDBMSs, duplications aren’t removed immediately upon insertion. Deduplication of data only happens during background merge operations, which ClickHouse controls automatically. This can be circumvented by making queries on the table FINAL. Another condition some users find is the presence of a deleted record \- due to soft deleting the row, it continues to exist in the ClickHouse destination table with the last values or default ClickHouse values. The example script in our pipeline does not support deletion events at this time.


## Data preparation in Delta Lake [\#](/blog/consuming-delta-lake-change-data-feed-cdc#data-preparation-in-delta-lake)


[An example data loader script](https://github.com/ClickHouse/deltalake-cdc?tab=readme-ov-file#1-generate-sample-data) is used to create an unpartitioned Delta Lake table (although partitioning the table is recommended for very large tables) and stream synthetically generated data. The DataFrame library Polars is used to create records at a batch size provided. A sample performance benchmark of the data generation is that it can generate and write 20,000 records at a time, which is approximately 10MB worth of data into the Delta Lake table that can be generated on a c5\.large AWS EC2 instance with 2 vCPU and 4 GB RAM every 1 second in the same region as the S3 bucket; the batch size is configurable and can be run on commodity hardware such as a laptop. The data loader script will create the Delta Lake table if it doesn’t already exist, and enable the CDF on creation, which has an insignificant impact on insertion. Once there are enough commits in the Delta Lake table, the data is ready to start ingesting into ClickHouse.


## Change Data Capture [\#](/blog/consuming-delta-lake-change-data-feed-cdc#change-data-capture)


CDC can be a challenging process depending on the source and the protocols involved. Open Table Formats (OTF) like Delta Lake and Apache Iceberg introduce complexity for CDC compared to traditional transactional databases like Postgres. While Postgres maintains a built\-in Write\-Ahead log (WAL) that records every change in chronological order within transaction boundaries, open table formats must reconstruct change streams from file\-level operations across distributed storage. These formats rely on metadata layers and commit version differencing to track changes, which creates challenges in maintaining ordering, handling concurrent writes, and ensuring that consumers can reliably identify what changed between table versions. Fortunately, Delta Lake provides the [Change Data Feed (CDF)](https://docs.delta.io/latest/delta-change-data-feed.html), which enables operations on row\-level data and can be processed by downstream systems like ClickHouse and ClickPipes. The change data is committed as part of the transaction, and becomes available at the same time new data is committed to the table. This setting can be enabled on Delta Lake table creation:



```

```
CREATE TABLE my_cdc_table (id STRING, name STRING, age INT, created_at TIMESTAMP) TBLPROPERTIES (delta.enableChangeDataFeed = true)
```


```

Or can be added to existing tables like so:



```

```
ALTER TABLE my_cdc_table SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
```


```

Unlike RDBMS CDC mechanisms, the CDF is a **logical abstraction that is constructed from multiple components** when querying for change data rather than explicit change records consumed from some physical storage. The data, once committed, is recorded in the transaction log (within the `_delta_log` directory), which references the data part and can be read as a stream of record batches. This is the case with INSERT (append) only workloads where the record (like the example below) identifies changes within specific time ranges. Delta Lake uses the [min/max statistics to skip data files that wouldn’t contain relevant changes](https://docs.databricks.com/aws/en/delta/data-skipping). This data skipping reduces the amount of data that needs to be read to compute change events. The contents of the transaction log look like the following example:



```

```
{
  "add": {
    "path": "part-00001-bcb81f71-8bd9-4626-9186-0580428941d0-c000.snappy.parquet",
    "partitionValues": {},
    "size": 489819,
    "modificationTime": 1752068897913,
    "dataChange": true,
    "stats": {
      "numRecords": 10000,
      "minValues": {
        "id": "000bcedc-d231-40f7-9897-189010d9d7f5",
        "name": "AABCX",
        "age": 18,
        "created_at": "2025-07-09T13:48:13.648587Z"
      },
      "maxValues": {
        "id": "fff6a0e8-bccb-46be-9af4-0d7d3c5d37172",
        "name": "ZZZTR",
        "age": 65,
        "created_at": "2025-07-09T13:48:13.650625Z"
      },
      "nullCount": {
        "id": 0,
        "name": 0,
        "age": 0,
        "created_at": 0
      }
    },
    "tags": null,
    "baseRowId": null,
    "defaultRowCommitVersion": null,
    "clusteringProvider": null
  }
}
{
  "commitInfo": {
    "timestamp": 1752068897913,
    "operation": "WRITE",
    "operationParameters": {
      "mode": "Append"
    },
    "clientVersion": "delta-rs.py-1.0.2",
    "operationMetrics": {
      "execution_time_ms": 1213,
      "num_added_files": 1,
      "num_added_rows": 10000,
      "num_partitions": 0,
      "num_removed_files": 0
    }
  }
}
```


```

When it comes to updates and deletes to the Delta Lake table, the changes are recorded in a `_change_data` subdirectory, which contains only Parquet files containing the changed records. A transaction log that has recorded updates would look like so:



```

```
{ "add": { "path": "part-00001-bf9a82c5-0eda-433a-a2e6-8ec7c8757f23-c000.snappy.parquet", ... }}
{ "cdc": { "path": "_change_data/part-00001-5482b246-deb0-4338-a82c-d56a32d38ac3-c000.snappy.parquet", ... }}
{ "add": { "path": "part-00001-e653da14-92ee-4b6d-a03d-86333a1a56a5-c000.snappy.parquet", ... }}
{ "cdc": { "path": "_change_data/part-00001-3acf8a12-71aa-4f0c-8c61-e24046633a98-c000.snappy.parquet", ... }}
{ "remove": { "path": "part-00001-ec06b026-ca3b-48ec-8687-bafd2706a877-c000.snappy.parquet", ... }}
{ "remove": { "path": "part-00001-93252f4b-72ae-4bf3-8be0-ae2031441ab8-c000.snappy.parquet", ... }}
{ "commitInfo": { "timestamp": 1753784155897, "operation": "MERGE", ... }}
```


```

The above records a merge operation that updated 100 existing records in the target table by matching them with 100 source records based on the condition `target.id = source.id`. 2 new data files were created containing the updated records, and 2 CDC files were created to track the changes. Further, 2 old data files were deleted.


To list the change data event files, you can see raw data, which can be queried from ClickHouse like so:



```

```
select _file from s3(
   's3://path/to/deltalake/table/_change_data/*.parquet',
   '[HIDDEN]',
   '[HIDDEN]'
)
```


```


```
part-00001-08d3c1e5-87e9-4455-8b48-ea7398277003-c000.snappy.parquet
part-00001-08d3c1e5-87e9-4455-8b48-ea7398277003-c000.snappy.parquet
part-00001-08d3c1e5-87e9-4455-8b48-ea7398277003-c000.snappy.parquet
part-00001-08d3c1e5-87e9-4455-8b48-ea7398277003-c000.snappy.parquet
part-00001-08d3c1e5-87e9-4455-8b48-ea7398277003-c000.snappy.parquet
part-00001-08d3c1e5-87e9-4455-8b48-ea7398277003-c000.snappy.parquet
part-00001-08d3c1e5-87e9-4455-8b48-ea7398277003-c000.snappy.parquet
part-00001-08d3c1e5-87e9-4455-8b48-ea7398277003-c000.snappy.parquet
…

```

The `_change_data` part files can be queried in place with ClickHouse



```

```
select *, _file, _time from s3(
   's3://path/to/deltalake/table/_change_data/*.parquet',
   '[HIDDEN]',
   '[HIDDEN]'
)
```


```


```
431cbe31-e33f-4a8c-9d4d-5d0b0f1b38c1	XUBSG	53	2025-07-09 14:38:21.646311	update_preimage	part-00001-08d3c1e5-87e9-4455-8b48-ea7398277003-c000.snappy.parquet	2025-07-28 13:04:52
431cbe31-e33f-4a8c-9d4d-5d0b0f1b38c1	WDMGN	43	2025-07-28 13:03:49.198168	update_postimage	part-00001-08d3c1e5-87e9-4455-8b48-ea7398277003-c000.snappy.parquet	2025-07-28 13:04:52
07edd0c9-adc2-4110-8cc3-448b99ec1900	OJSSL	29	2025-07-09 13:48:50.254035	update_preimage	part-00001-08d3c1e5-87e9-4455-8b48-ea7398277003-c000.snappy.parquet	2025-07-28 13:04:52
07edd0c9-adc2-4110-8cc3-448b99ec1900	GEKKK	38	2025-07-28 13:03:49.198218	update_postimage	part-00001-08d3c1e5-87e9-4455-8b48-ea7398277003-c000.snappy.parquet	2025-07-28 13:04:52
…
286e746a-eb0f-4474-a72f-0323a95b79d9	TURGH	46	2025-07-09 13:56:11.702183	delete	part-00001-8421b723-9407-47aa-826e-1c594698e5cc-c000.snappy.parquet	2025-07-28 13:05:55
26c54093-5aae-4bf6-93a8-58912ec41655	SFYVN	53	2025-07-09 14:15:59.204611	delete	part-00001-8421b723-9407-47aa-826e-1c594698e5cc-c000.snappy.parquet	2025-07-28 13:05:55
26c54093-5aae-4bf6-93a8-58912ec41655	SFYVN	53	2025-07-09 14:15:59.204611	delete	part-00001-8421b723-9407-47aa-826e-1c594698e5cc-c000.snappy.parquet	2025-07-28 13:05:55

```

You can see that for updates, there are 2 change events recorded \- `update_preimage` reflects the data before the operation, and `update_postimage`, which is the data after the operation. `delete` events are only single records, indicating which rows have been deleted and can also be marked as such downstream. This data can then be inserted into ClickHouse. Similar to the meta field discussed above, we include the `_change_type`, `_commit_version`, and `_commit_type` metadata when inserting into ClickHouse. These, along with the DDL for the table described in the previous section, enable us to resolve the latest version in the event of an update. The general advice is to let the ReplacingMergeTree table engine resolve the state of the table in an eventually consistent way, rather than reconcile in program memory or at source, as this can be costly and slow.


## Python prototype for CDC from Delta Lake to ClickHouse [\#](/blog/consuming-delta-lake-change-data-feed-cdc#python-prototype-for-cdc-from-delta-lake-to-clickhouse)


Our [reference implementation](https://github.com/ClickHouse/deltalake-cdc) uses the [DeltaLake Python library](https://pypi.org/project/deltalake/), which uses [delta\-rs](https://github.com/delta-io/delta-rs) bindings to read from Delta Lake. At a high level, the underlying algorithm iterates through each version in the specified range (starting version \- continuous polling), reads through the transaction log for each version, and categorises the actions in CDC / add row / remove row operations. Separate DataFusion execution plans are created for each file type. It then combines all 3 operations and projects the final schema with the CDF metadata columns (\_change\_type, \_commit\_version, \_commit\_timestamp).


The underlying library supports consuming the CDF from a version or timestamp, but for our example, we have opted to support only version. The number of records received can vary based on the size of changes made when that version was committed. To control for this, we batch records in groups of \~80,000, which we found optimal for collecting CDF records and writing to ClickHouse; once a batch size of change data records has met or exceeded this batch size, the data is flushed to ClickHouse. A sample benchmark is that our reference CDF reader/writer can move \~80,000 records to ClickHouse in \~1\.2 seconds on a c5\.large AWS EC2 instance (2 vCPU, 4 GiB memory, 10 Gbps of network bandwidth), in the same region as the Delta Lake S3 bucket and the ClickHouse service. Scaling the instance profile beyond this did not improve the workload throughput. A potential optimisation could involve introducing multiple ClickHouse writers inserting batches between 10,000\-100,000 records based on the amount of data materialised from reading the CDF \- this could be ideal for bursty workloads, possibly caused by the likes of batch jobs, rather than data continuously streaming to the delta lake tables.



```

```
$ python main.py 
 -p "s3://path/to/deltalake/table" 
 -r "us-east-2"
 -t "default.my_cdc_table"
 -H "[service].us-east-2.aws.clickhouse.cloud"
 -v 28000
 -b 80000
```


```


```
2025-07-23 10:56:54,143 - INFO - Using provided AWS credentials
2025-07-23 10:56:54,625 - INFO - Starting continuous processing from version 28000
2025-07-23 10:56:55,064 - INFO - Processing changes from version 28000 to 28252
2025-07-23 10:57:02,185 - INFO - Processed batch 1: 81920 rows (total: 81920) in 1.55 seconds
2025-07-23 10:57:03,411 - INFO - Processed batch 2: 83616 rows (total: 165536) in 1.23 seconds
2025-07-23 10:57:04,535 - INFO - Processed batch 3: 83616 rows (total: 249152) in 1.12 seconds
2025-07-23 10:57:05,651 - INFO - Processed batch 4: 81920 rows (total: 331072) in 1.12 seconds
2025-07-23 10:57:06,754 - INFO - Processed batch 5: 81920 rows (total: 412992) in 1.10 seconds
...

```

## Snapshotting [\#](/blog/consuming-delta-lake-change-data-feed-cdc#snapshotting)


Capturing change in a data lake is a notable technical challenge. Backfilling data before the snapshot took place on tables that previously did not have the CDF enabled requires additional focus. If the CDF was enabled on table creation, a snapshot is not technically required because it can be consumed from version 0 of the Delta table. This may not be optimal if the table has had many versions. Delta Lake writes checkpoints every 100 commits as an aggregate state of the Delta table that can be used to perform a more efficient backfill by querying at a specific version rather than reading from version 0 if the CDF was enabled. The backfill can take advantage of data\-skipping if there are more than just INSERT operations on the table. We know that ClickHouse users who also use data lakes tend to have table sizes in the terabyte and petabyte range, which is a lot of data to move in one shot. This can be moved asynchronously by ClickHouse with the following queries:



```

```
CREATE TABLE my_delta_table
   ENGINE = DeltaLakeCluster('"s3://path/to/deltalake/table"');

INSERT INTO
 `default`.`my_cdc_table`
SELECT
 *, 'snapshot', 0, now()
FROM
 `default`.`my_delta_table``
LIMIT 2000000000;
```


```

This **INSERT INTO SELECT** query populates the table metadata columns with the values ‘snapshot’, 0, `now()` for the ReplacingMergeTree to resolve the correct upstream state as data is ingested and ClickHouse performs background merges. For reference, this example query moved 2 billion rows from a Delta Lake table to a ClickHouse Cloud service with autoscaling disabled, where the Delta Lake table and ClickHouse service are in the same region. Memory usage remained constant between 700 MB and 2 GB. This impressive performance is achieved due to the object storage engines backing the Data Lake table functions and engines, which make use of parallelization and prefetching. This snapshot finishes in 1,936 seconds (\~32 minutes).


![cdf-img1.png](/uploads/cdf_img1_9e2fba7587.png)
This query had a negligible impact on resource utilisation in the ClickHouse cluster. Throughput could be tuned further by increasing the number of threads used by the query.


![cdf-image2.png](/uploads/cdf_image2_73ee373f5c.png)
A further benefit is that these reads do not put pressure on the Delta Lake table if it is object storage\-backed, unlike other CDC ClickPipes, where great care has to be given to the source database in case adverse effects impact it, such as crashing the database server. The following query can be used to view the data that has been written to ClickHouse.



```

```
SELECT
   hostName(),
   database,
   table,
   sum(rows) AS rows,
   formatReadableSize(sum(bytes_on_disk)) AS total_bytes_on_disk,
   formatReadableSize(sum(data_compressed_bytes)) AS total_data_compressed_bytes,
   formatReadableSize(sum(data_uncompressed_bytes)) AS total_data_uncompressed_bytes,
round(sum(data_compressed_bytes) / sum(data_uncompressed_bytes), 3) AS compression_ratio
FROM system.parts
WHERE database != 'system'
GROUP BY
   hostName(),
   database,
   table
ORDER BY sum(bytes_on_disk) DESC FORMAT Vertical
```


```


```
hostName():                    c-creamaws-by-66-server-pzltzls-0
database:                      default
table:                         new_cdc_table
rows:                          2000000000 -- 2.00 billion
total_bytes_on_disk:           45.44 GiB
total_data_compressed_bytes:   45.43 GiB
total_data_uncompressed_bytes: 141.56 GiB
compression_ratio:             0.321

```

Another way to improve the snapshot's performance would be to run multiple of these INSERT INTO SELECT queries in parallel, where each query targets a partition group (assuming the data is appropriately partitioned in some way). Otherwise, the snapshot process would have to infer an appropriate column to act as a partitioning key. This would require batch tracking but would yield significant performance benefits at the cost of increased CPU and memory usage.


What is notable and interesting about coupling this approach to the above CDF reader is that both can, in theory, be run at the same time. Unlike traditional RDBMS CDC ClickPipes, where an initial load (if selected) is performed first, and then the database\-specific CDC log is consumed, the Delta Lake process can happen simultaneously, as it will eventually resolve to its correct state due to the CDC log having higher versions than the snapshot. In RDBMS CDC ClickPipes, running initial load from a snapshot and CDC in parallel is non\-trivial and a difficult implementation. In MySQL, for instance, there isn't a snapshot or replication slot provided to us. That means there isn’t a guarantee that events will be synced in chronological order if a snapshot and binlogs are read in parallel. Currently, in all CDC ClickPipes, if 1 table needs to be resynced, all CDC operations are typically stalled until that snapshot is complete. This does not have to be the case for Delta Lake CDC, as tables can be resynced without impacting the CDF consumption of other tables \- this improves CDF consumption throughput across multiple tables.


## Limitations of the reference implementation [\#](/blog/consuming-delta-lake-change-data-feed-cdc#limitations-of-the-reference-implementation)


This reference implementation is a precursor to a production\-grade ClickPipe and has notable limitations. It is not production\-ready. It lays a foundation that you can extend and integrate into your existing orchestration and processing tools, such as Spark or Airflow, to build a production\-ready Delta Lake to ClickHouse replication / CDC.


### Fault tolerance [\#](/blog/consuming-delta-lake-change-data-feed-cdc#fault-tolerance)


Currently, when starting the CDC process, the user has to specify the version. If, for whatever reason, the script fails and stops working, the user would have to take note of the last version that was processed and restart the script or start the script again. Offset tracking is a key feature of all CDC ClickPipes. This is also the case for large snapshots, as queries can fail to complete for various reasons.


Updates and Deletes  

We use the ReplacingMergeTree table for CDC workloads that have update and delete operations—essentially treating these DML operations as INSERT operations. This leads to the eventually consistent table state as we described above.


ClickHouse, like most column stores, was not originally designed for fast row\-level updates. However, [since June 2025, ClickHouse v25\.7 has supported high\-performance, SQL\-standard UPDATEs](https://clickhouse.com/blog/updates-in-clickhouse-2-sql-style-updates).


ReplacingMergeTree is already used in all ClickPipe CDC connectors and has proved reliable and performant in production for many years; hence, we continue to use this pattern.


### Schema evolution [\#](/blog/consuming-delta-lake-change-data-feed-cdc#schema-evolution)


Snapshotting the initial state of the table is unlikely to be troublesome as the schema is fixed at this time. The Delta Lake CDF has a limitation when dealing with schema changes as these DDL change events are not represented at the protocol level. Non\-additive schema changes like column renames, drops, or data type changes can break CDF consumption entirely. This requires the users to carefully manage schema evolution timelines, or otherwise be forced to stop the CDC process and resync the table state. One such approach is to use catalog support \- we only provide IAM credential support in our script, and understand we would need to support various authentication protocols to meet customers where they are. Multiple catalogs may need to be supported, such as Amazon Glue catalog, Open Metadata, Hive MetaStore, or Unity Catalog.


### Delete support [\#](/blog/consuming-delta-lake-change-data-feed-cdc#delete-support)


Supporting deletes is a key feature in CDC pipelines. It is not relevant for snapshots (if applicable) as deletes are already considered materialised due to the ACID properties of a Delta Lake table. Our prototype currently ignores deletes in the change log. Like our other CDC ClickPipes, we plan to support soft deleting where the row is marked as deleted, the primary key and metadata fields continue to be present, but all other row fields are set to the default value of the ClickHouse type. Due to performance reasons, we recommend against using null values in the tombstoned record, as this can impact compression.


## Planned improvements [\#](/blog/consuming-delta-lake-change-data-feed-cdc#planned-improvements)


As you can see, building such a prototype highlights some of the existing limitations of ClickHouse when working with Delta Tables. It would be convenient just to write:



```

```
SELECT * FROM table_changes(‘default.my_delta_table’, 5, 10);
```


```

And get back the data that changed between versions 5 and 10\. Or being able to query a specific snapshot, like ClickHouse already supports it for Iceberg:



```

```
SELECT * FROM deltaLakeCluster(‘s3://path/to/deltalake/table’) SETTINGS snapshot_version=5;
```


```

Like many improvements to the ClickHouse data lake integrations, both features will be coming soon to ClickHouse: [\#73704](https://github.com/ClickHouse/ClickHouse/issues/73704) and [\#85070](https://github.com/ClickHouse/ClickHouse/issues/85070) that can be used to improve the CDC experience.


## Conclusion [\#](/blog/consuming-delta-lake-change-data-feed-cdc#conclusion)


Building a [CDC pipeline from Delta Lake as a source to ClickHouse](https://github.com/ClickHouse/deltalake-cdc) enables a compelling solution for designing real\-time analytical applications. By leveraging the strengths of both technologies and carefully considering the architectural components and implementation details, organisations can achieve a reliable and scalable data replication solution. This enables faster insights and more informed decision\-making based on the latest data.


As a reminder, [ClickPipes](https://clickhouse.com/cloud/clickpipes) already offers enterprise\-grade connectors for change data capture from [Postgres](https://clickhouse.com/docs/integrations/clickpipes/postgres%20), [MySQL](https://clickhouse.com/docs/integrations/clickpipes/mysql), and [MongoDB](https://clickhouse.com/cloud/clickpipes/mongodb-cdc-connector), along with robust ingestion support for [Object Storage](https://clickhouse.com/docs/integrations/clickpipes/object-storage%20) and [Streaming sources](https://clickhouse.com/docs/integrations/clickpipes/kafka/).


We plan to add production\-grade support for Delta Lake CDC in ClickPipes in the coming months. If you're interested in partnering with us as a design partner, please email **[clickpipes@clickhouse.com](mailto:clickpipes@clickhouse.com)**.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
