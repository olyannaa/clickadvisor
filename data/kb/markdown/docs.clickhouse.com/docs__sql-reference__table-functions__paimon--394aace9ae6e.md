# paimon \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- paimon
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/paimon.md)# paimon Table Function


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)
Provides a read\-only table\-like interface to Apache [Paimon](https://paimon.apache.org/) tables in Amazon S3, Azure, HDFS or locally stored.


## Syntax[​](#syntax "Direct link to Syntax")



```
paimon(url [,access_key_id, secret_access_key] [,format] [,structure] [,compression] [,extra_credentials])

paimonS3(url [,access_key_id, secret_access_key] [,format] [,structure] [,compression] [,extra_credentials])

paimonAzure(connection_string|storage_account_url, container_name, blobpath, [,account_name], [,account_key] [,format] [,compression_method])

paimonHDFS(path_to_table, [,format] [,compression_method])

paimonLocal(path_to_table, [,format] [,compression_method])

```

## Arguments[​](#arguments "Direct link to Arguments")


Description of the arguments coincides with description of arguments in table functions `s3`, `azureBlobStorage`, `HDFS` and `file` correspondingly.
`format` stands for the format of data files in the Paimon table.


For `paimonS3`, an optional `extra_credentials` parameter can be used to pass a `role_arn` for role\-based access in ClickHouse Cloud. See [Secure S3](/docs/cloud/data-sources/secure-s3) for configuration steps.


### Returned value[​](#returned-value "Direct link to Returned value")


A table with the specified structure for reading data in the specified Paimon table.


## Defining a named collection[​](#defining-a-named-collection "Direct link to Defining a named collection")


Here is an example of configuring a named collection for storing the URL and credentials:



```
<clickhouse>
    <named_collections>
        <paimon_conf>
            <url>http://test.s3.amazonaws.com/clickhouse-bucket/</url>
            <access_key_id>test</access_key_id>
            <secret_access_key>test</secret_access_key>
            <format>auto</format>
            <structure>auto</structure>
        </paimon_conf>
    </named_collections>
</clickhouse>

```


```
SELECT * FROM paimonS3(paimon_conf, filename = 'test_table')
DESCRIBE paimonS3(paimon_conf, filename = 'test_table')

```

## Aliases[​](#aliases "Direct link to Aliases")


Table function `paimon` is an alias to `paimonS3` now.


## Virtual Columns[​](#virtual-columns "Direct link to Virtual Columns")


- `_path` — Path to the file. Type: `LowCardinality(String)`.
- `_file` — Name of the file. Type: `LowCardinality(String)`.
- `_size` — Size of the file in bytes. Type: `Nullable(UInt64)`. If the file size is unknown, the value is `NULL`.
- `_time` — Last modified time of the file. Type: `Nullable(DateTime)`. If the time is unknown, the value is `NULL`.
- `_etag` — The etag of the file. Type: `LowCardinality(String)`. If the etag is unknown, the value is `NULL`.


## Data Types supported[​](#data-types-supported "Direct link to Data Types supported")




| Paimon Data Type Clickhouse Data Type| BOOLEAN Int8| TINYINT Int8| SMALLINT Int16| INTEGER Int32| BIGINT Int64| FLOAT Float32| DOUBLE Float64| STRING,VARCHAR,BYTES,VARBINARY String| DATE Date| TIME(p),TIME Time('UTC')| TIMESTAMP(p) WITH LOCAL TIME ZONE DateTime64| TIMESTAMP(p) DateTime64('UTC')| CHAR FixedString(1\)| BINARY(n) FixedString(n)| DECIMAL(P,S) Decimal(P,S)| ARRAY Array| MAP Map | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


## Partition supported[​](#partition-supported "Direct link to Partition supported")


Data types supported in Paimon partition keys:


- `CHAR`
- `VARCHAR`
- `BOOLEAN`
- `DECIMAL`
- `TINYINT`
- `SMALLINT`
- `INTEGER`
- `DATE`
- `TIME`
- `TIMESTAMP`
- `TIMESTAMP WITH LOCAL TIME ZONE`
- `BIGINT`
- `FLOAT`
- `DOUBLE`


## See Also[​](#see-also "Direct link to See Also")


- [Paimon cluster table function](/docs/sql-reference/table-functions/paimonCluster)
[Previousiceberg](/docs/sql-reference/table-functions/iceberg)[NexticebergCluster](/docs/sql-reference/table-functions/icebergCluster)- [Syntax](#syntax)- [Arguments](#arguments)
	- [Returned value](#returned-value)- [Defining a named collection](#defining-a-named-collection)- [Aliases](#aliases)- [Virtual Columns](#virtual-columns)- [Data Types supported](#data-types-supported)- [Partition supported](#partition-supported)- [See Also](#see-also)
Was this page helpful?
