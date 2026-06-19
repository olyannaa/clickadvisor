# Table Functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- Table functions
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/index.md)# Table Functions

Table functions are methods for constructing tables.




| Page Description| [azureBlobStorage](/docs/sql-reference/table-functions/azureBlobStorage) Provides a table\-like interface to select/insert files in Azure Blob Storage. Similar to the s3 function.| [azureBlobStorageCluster](/docs/sql-reference/table-functions/azureBlobStorageCluster) Allows processing files from Azure Blob storage in parallel with many nodes in a specified cluster.| [clusterAllReplicas](/docs/sql-reference/table-functions/cluster) Allows accessing all shards (configured in the `remote_servers` section) of a cluster without creating a Distributed table.| [deltaLake](/docs/sql-reference/table-functions/deltalake) Provides a read\-only table\-like interface to the Delta Lake tables in Amazon S3\.| [deltaLakeCluster](/docs/sql-reference/table-functions/deltalakeCluster) This is an extension to the deltaLake table function.| [dictionary](/docs/sql-reference/table-functions/dictionary) Displays the dictionary data as a ClickHouse table. Works the same way as the Dictionary engine.| [executable](/docs/engines/table-functions/executable) The `executable` table function creates a table based on the output of a user\-defined function (UDF) that you define in a script that outputs rows to **stdout**.| [file](/docs/sql-reference/table-functions/file) A table engine which provides a table\-like interface to SELECT from and INSERT into files, similar to the s3 table function. Use `file()` when working with local files, and `s3()` when working with buckets in object storage such as S3, GCS, or MinIO.| [fileCluster](/docs/sql-reference/table-functions/fileCluster) Enables simultaneous processing of files matching a specified path across multiple nodes within a cluster. The initiator establishes connections to worker nodes, expands globs in the file path, and delegates file\-reading tasks to worker nodes. Each worker node is querying the initiator for the next file to process, repeating until all tasks are completed (all files are read).| [filesystem](/docs/sql-reference/table-functions/filesystem) Provides access to the file system to list files and return their metadata and contents.| [format](/docs/sql-reference/table-functions/format) Parses data from arguments according to specified input format. If structure argument is not specified, it's extracted from the data.| [gcs](/docs/sql-reference/table-functions/gcs) Provides a table\-like interface to `SELECT` and `INSERT` data from Google Cloud Storage. Requires the `Storage Object User` IAM role.| [fuzzJSON](/docs/sql-reference/table-functions/fuzzJSON) Perturbs a JSON string with random variations.| [fuzzQuery](/docs/sql-reference/table-functions/fuzzQuery) Perturbs the given query string with random variations.| [generateRandom](/docs/sql-reference/table-functions/generate) Generates random data with a given schema. Allows populating test tables with that data. Not all types are supported.| [mergeTreeIndex](/docs/sql-reference/table-functions/mergeTreeIndex) Represents the contents of index and marks files of MergeTree tables. It can be used for introspection.| [mergeTreeProjection](/docs/sql-reference/table-functions/mergeTreeProjection) Represents the contents of some projection in MergeTree tables. It can be used for introspection.| [mergeTreeTextIndex](/docs/sql-reference/table-functions/mergeTreeTextIndex) Represents the dictionary of a text index in a MergeTree table. It can be used for introspection.| [hdfs](/docs/sql-reference/table-functions/hdfs) Creates a table from files in HDFS. This table function is similar to the url and file table functions.| [hdfsCluster](/docs/sql-reference/table-functions/hdfsCluster) Allows processing files from HDFS in parallel from many nodes in a specified cluster.| [hudi](/docs/sql-reference/table-functions/hudi) Provides a read\-only table\-like interface to Apache Hudi tables in Amazon S3\.| [ytsaurus](/docs/sql-reference/table-functions/ytsaurus) The table function allows to read data from the YTsaurus cluster.| [hudiCluster Table Function](/docs/sql-reference/table-functions/hudiCluster) An extension to the hudi table function. Allows processing files from Apache Hudi tables in Amazon S3 in parallel with many nodes in a specified cluster.| [iceberg](/docs/sql-reference/table-functions/iceberg) Provides a read\-only table\-like interface to Apache Iceberg tables in Amazon S3, Azure, HDFS or locally stored.| [paimon](/docs/sql-reference/table-functions/paimon) Provides a read\-only table\-like interface to Apache Paimon tables in Amazon S3, Azure, HDFS or locally stored.| [icebergCluster](/docs/sql-reference/table-functions/icebergCluster) An extension to the iceberg table function which allows processing files from Apache Iceberg in parallel from many nodes in a specified cluster.| [paimonCluster](/docs/sql-reference/table-functions/paimonCluster) An extension to the paimon table function which allows processing files from Apache Paimon in parallel from many nodes in a specified cluster.| [input](/docs/sql-reference/table-functions/input) Table function that allows effectively converting and inserting data sent to the server with a given structure to a table with another structure.| [jdbc](/docs/sql-reference/table-functions/jdbc) Returns a table that is connected via JDBC driver.| [merge](/docs/sql-reference/table-functions/merge) Creates a temporary Merge table. The structure will be derived from underlying tables by using a union of their columns and by deriving common types.| [mongodb](/docs/sql-reference/table-functions/mongodb) Allows `SELECT` queries to be performed on data that is stored on a remote MongoDB server.| [mysql](/docs/sql-reference/table-functions/mysql) Allows `SELECT` and `INSERT` queries to be performed on data that are stored on a remote MySQL server.| [null](/docs/sql-reference/table-functions/null) Creates a temporary table of the specified structure with the Null table engine. The function is used for the convenience of test writing and demonstrations.| [numbers](/docs/sql-reference/table-functions/numbers) Returns a table with a single `number` column that contains a sequence of integers.| [primes](/docs/sql-reference/table-functions/primes) Returns a table with a single `prime` column that contains prime numbers.| [prometheusQuery](/docs/sql-reference/table-functions/prometheusQuery) Evaluates a prometheus query using data from a TimeSeries table.| [prometheusQueryRange](/docs/sql-reference/table-functions/prometheusQueryRange) Evaluates a prometheus query using data from a TimeSeries table.| [timeSeriesData](/docs/sql-reference/table-functions/timeSeriesData) timeSeriesData returns the data table used by table `db_name.time_series_table` whose table engine is TimeSeries.| [timeSeriesMetrics](/docs/sql-reference/table-functions/timeSeriesMetrics) timeSeriesMetrics returns the metrics table used by table `db_name.time_series_table` whose table engine is the TimeSeries engine.| [timeSeriesSelector](/docs/sql-reference/table-functions/timeSeriesSelector) Reads time series from a TimeSeries table filtered by a selector and with timestamps in a specified interval.| [timeSeriesTags](/docs/sql-reference/table-functions/timeSeriesTags) timeSeriesTags table function returns the tags table use by table `db_name.time_series_table` whose table engine is the TimeSeries engine.| [zeros](/docs/sql-reference/table-functions/zeros) Used for test purposes as the fastest method to generate many rows. Similar to the `system.zeros` and `system.zeros_mt` system tables.| [generate\_series (generateSeries)](/docs/sql-reference/table-functions/generate_series) Returns a table with the single `generate_series` column (UInt64\) that contains integers from start to stop inclusively.| [odbc](/docs/sql-reference/table-functions/odbc) Returns the table that is connected via ODBC.| [postgresql](/docs/sql-reference/table-functions/postgresql) Allows `SELECT` and `INSERT` queries to be performed on data that is stored on a remote PostgreSQL server.| [redis](/docs/sql-reference/table-functions/redis) This table function allows integrating ClickHouse with Redis.| [remote, remoteSecure](/docs/sql-reference/table-functions/remote) Table function `remote` allows to access remote servers on\-the\-fly, i.e. without creating a distributed table. Table function `remoteSecure` is same as `remote` but over a secure connection.| [s3 Table Function](/docs/sql-reference/table-functions/s3) Provides a table\-like interface to select/insert files in Amazon S3 and Google Cloud Storage. This table function is similar to the hdfs function, but provides S3\-specific features.| [s3Cluster](/docs/sql-reference/table-functions/s3Cluster) An extension to the s3 table function, which allows processing files from Amazon S3 and Google Cloud Storage in parallel with many nodes in a specified cluster.| [sqlite](/docs/sql-reference/table-functions/sqlite) Allows to perform queries on data stored in a SQLite database.| [arrowFlight](/docs/sql-reference/table-functions/arrowflight) Allows to perform queries on data exposed via an Apache Arrow Flight server.| [url](/docs/sql-reference/table-functions/url) Creates a table from the `URL` with given `format` and `structure`| [urlCluster](/docs/sql-reference/table-functions/urlCluster) Allows processing files from URL in parallel from many nodes in a specified cluster.| [values](/docs/sql-reference/table-functions/values) creates a temporary storage which fills columns with values.| [view](/docs/sql-reference/table-functions/view) Turns a subquery into a table. The function implements views.| [loop](/docs/sql-reference/table-functions/loop) The loop table function in ClickHouse is used to return query results in an infinite loop. | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


## Usage[​](#usage "Direct link to Usage")


Table functions can be used in the [`FROM`](/docs/sql-reference/statements/select/from)
clause of a `SELECT` query. For example, you can `SELECT` data from a file on your local
machine using the `file` table function.



```
echo "1, 2, 3" > example.csv

```


```
./clickhouse client
:) SELECT * FROM file('example.csv')
┌─c1─┬─c2─┬─c3─┐
│  1 │  2 │  3 │
└────┴────┴────┘

```

You can also use table functions for creating a temporary table that is available
only in the current query. For example:



```
SELECT * FROM generateSeries(1,5);

```


```
┌─generate_series─┐
│               1 │
│               2 │
│               3 │
│               4 │
│               5 │
└─────────────────┘

```

The table is deleted when the query finishes.


Table functions can be used as a way to create tables, using the following syntax:



```
CREATE TABLE [IF NOT EXISTS] [db.]table_name AS table_function()

```

For example:



```
CREATE TABLE series AS generateSeries(1, 5);
SELECT * FROM series;

```


```
┌─generate_series─┐
│               1 │
│               2 │
│               3 │
│               4 │
│               5 │
└─────────────────┘

```

Finally, table functions can be used to `INSERT` data into a table. For example,
we could write out the contents of the table we created in the previous example
to a file on disk using the `file` table function again:



```
INSERT INTO FUNCTION file('numbers.csv', 'CSV') SELECT * FROM series;

```


```
cat numbers.csv
1
2
3
4
5

```

NoteYou can't use table functions if the [allow\_ddl](/docs/operations/settings/settings#allow_ddl) setting is disabled.

[PreviousuniqArrayIf](/docs/examples/aggregate-function-combinators/uniqArrayIf)[NextazureBlobStorage](/docs/sql-reference/table-functions/azureBlobStorage)- [Usage](#usage)
Was this page helpful?
