# hudi \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- hudi
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/hudi.md)# hudi

Provides a read\-only table\-like interface to Apache [Hudi](https://hudi.apache.org/) tables in Amazon S3\.


## Syntax[​](#syntax "Direct link to Syntax")



```
hudi(url [,aws_access_key_id, aws_secret_access_key] [,format] [,structure] [,compression] [,extra_credentials])

```

## Arguments[​](#arguments "Direct link to Arguments")




| Argument Description| `url` Bucket url with the path to an existing Hudi table in S3\.| `aws_access_key_id`, `aws_secret_access_key` Long\-term credentials for the [AWS](https://aws.amazon.com/) account user. You can use these to authenticate your requests. These parameters are optional. If credentials are not specified, they are used from the ClickHouse configuration. For more information see [Using S3 for Data Storage](/docs/engines/table-engines/mergetree-family/mergetree#table_engine-mergetree-s3).| `format` The [format](/docs/interfaces/formats) of the file.| `structure` Structure of the table. Format `'column1_name column1_type, column2_name column2_type, ...'`.| `compression` Parameter is optional. Supported values: `none`, `gzip/gz`, `brotli/br`, `xz/LZMA`, `zstd/zst`. By default, compression will be autodetected by the file extension.| `extra_credentials` Parameter is optional. Used to pass a `role_arn` for role\-based access in ClickHouse Cloud. See [Secure S3](/docs/cloud/data-sources/secure-s3) for configuration steps. | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


## Returned value[​](#returned_value "Direct link to Returned value")


A table with the specified structure for reading data in the specified Hudi table in S3\.


## Virtual Columns[​](#virtual-columns "Direct link to Virtual Columns")


- `_path` — Path to the file. Type: `LowCardinality(String)`.
- `_file` — Name of the file. Type: `LowCardinality(String)`.
- `_size` — Size of the file in bytes. Type: `Nullable(UInt64)`. If the file size is unknown, the value is `NULL`.
- `_time` — Last modified time of the file. Type: `Nullable(DateTime)`. If the time is unknown, the value is `NULL`.
- `_etag` — The etag of the file. Type: `LowCardinality(String)`. If the etag is unknown, the value is `NULL`.


## Related[​](#related "Direct link to Related")


- [Hudi engine](/docs/engines/table-engines/integrations/hudi)
- [Hudi cluster table function](/docs/sql-reference/table-functions/hudiCluster)
[PrevioushdfsCluster](/docs/sql-reference/table-functions/hdfsCluster)[Nextytsaurus](/docs/sql-reference/table-functions/ytsaurus)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned_value)- [Virtual Columns](#virtual-columns)- [Related](#related)
Was this page helpful?
