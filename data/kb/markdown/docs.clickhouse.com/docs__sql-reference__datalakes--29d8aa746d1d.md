# Data Lakes \| ClickHouse Docs


- - Data Lakes
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/datalakes.md)In this section, we will take a look at ClickHouse's support for Data Lakes.
ClickHouse supports many of the most popular table formats and data catalogs, including Iceberg, Delta Lake, Hudi, AWS Glue, REST Catalog, Unity Catalog and Microsoft OneLake.


# Open table formats


## Iceberg[​](#iceberg "Direct link to Iceberg")


See [iceberg](https://clickhouse.com/docs/sql-reference/table-functions/iceberg) which supports reading from Amazon S3 and S3\-compatible services, HDFS, Azure and local file systems. [icebergCluster](https://clickhouse.com/docs/sql-reference/table-functions/icebergCluster) is the distributed variant of the `iceberg` function.


## Delta Lake[​](#delta-lake "Direct link to Delta Lake")


See [deltaLake](https://clickhouse.com/docs/sql-reference/table-functions/deltalake) which supports reading from Amazon S3 and S3\-compatible services, Azure and local file systems. [deltaLakeCluster](https://clickhouse.com/docs/sql-reference/table-functions/deltalakeCluster) is the distributed variant of the `deltaLake` function.


## Hudi[​](#hudi "Direct link to Hudi")


See [hudi](https://clickhouse.com/docs/sql-reference/table-functions/hudi) which supports reading from Amazon S3 and S3\-compatible services. [hudiCluster](https://clickhouse.com/docs/sql-reference/table-functions/hudiCluster) is the distributed variant of the `hudi` function.


# Data catalogs


## AWS Glue[​](#aws-glue "Direct link to AWS Glue")


AWS Glue Data Catalog can be used with Iceberg tables. You can use it with the `iceberg` table engine, or with the [DataLakeCatalog](https://clickhouse.com/docs/engines/database-engines/datalakecatalog) database engine.


## Iceberg REST Catalog[​](#iceberg-rest-catalog "Direct link to Iceberg REST Catalog")


The Iceberg REST Catalog can be used with Iceberg tables. You can use it with the `iceberg` table engine, or with the [DataLakeCatalog](https://clickhouse.com/docs/engines/database-engines/datalakecatalog) database engine.


## Unity Catalog[​](#unity-catalog "Direct link to Unity Catalog")


Unity Catalog can be used with both Delta Lake and Iceberg tables. You can use it with the `iceberg` or `deltaLake` table engines, or with the [DataLakeCatalog](https://clickhouse.com/docs/engines/database-engines/datalakecatalog) database engine.


## Microsoft OneLake[​](#microsoft-onelake "Direct link to Microsoft OneLake")


Microsoft OneLake can be used with both Delta Lake and Iceberg tables. You can use it with the [DataLakeCatalog](https://clickhouse.com/docs/engines/database-engines/datalakecatalog) database engine.

[PreviousXML](/docs/interfaces/formats/XML)- [Iceberg](#iceberg)- [Delta Lake](#delta-lake)- [Hudi](#hudi)- [AWS Glue](#aws-glue)- [Iceberg REST Catalog](#iceberg-rest-catalog)- [Unity Catalog](#unity-catalog)- [Microsoft OneLake](#microsoft-onelake)
Was this page helpful?
