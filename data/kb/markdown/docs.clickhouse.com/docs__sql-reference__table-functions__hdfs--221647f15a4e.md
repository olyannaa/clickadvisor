# hdfs \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- hdfs
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/hdfs.md)# hdfs Table Function


Creates a table from files in HDFS. This table function is similar to the [url](/docs/sql-reference/table-functions/url) and [file](/docs/sql-reference/table-functions/file) table functions.


## Syntax[​](#syntax "Direct link to Syntax")



```
hdfs(URI, format, structure)

```

## Arguments[​](#arguments "Direct link to Arguments")




| Argument Description| `URI` The relative URI to the file in HDFS. Path to file support following globs in readonly mode: `*`, `?`, `{abc,def}` and `{N..M}` where `N`, `M` — numbers, `'abc', 'def'` — strings.| `format` The [format](/docs/sql-reference/formats) of the file.| `structure` Structure of the table. Format `'column1_name column1_type, column2_name column2_type, ...'`. | | | | | | | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- |


## Returned value[​](#returned_value "Direct link to Returned value")


A table with the specified structure for reading or writing data in the specified file.


**example**


Table from `hdfs://hdfs1:9000/test` and selection of the first two rows from it:



```
SELECT *
FROM hdfs('hdfs://hdfs1:9000/test', 'TSV', 'column1 UInt32, column2 UInt32, column3 UInt32')
LIMIT 2

```


```
┌─column1─┬─column2─┬─column3─┐
│       1 │       2 │       3 │
│       3 │       2 │       1 │
└─────────┴─────────┴─────────┘

```

## Globs in path[​](#globs_in_path "Direct link to Globs in path")


Paths may use globbing. Files must match the whole path pattern, not only the suffix or prefix.


- `*` — Represents arbitrarily many characters except `/` but including the empty string.
- `**` — Represents all files inside a folder recursively.
- `?` — Represents an arbitrary single character.
- `{some_string,another_string,yet_another_one}` — Substitutes any of strings `'some_string', 'another_string', 'yet_another_one'`. The strings can contain the `/` symbol.
- `{N..M}` — Represents any number `>= N` and `<= M`.


Constructions with `{}` are similar to the [remote](/docs/sql-reference/table-functions/remote) and [file](/docs/sql-reference/table-functions/file) table functions.


**Example**


1. Suppose that we have several files with following URIs on HDFS:


- 'hdfs://hdfs1:9000/some\_dir/some\_file\_1'
- 'hdfs://hdfs1:9000/some\_dir/some\_file\_2'
- 'hdfs://hdfs1:9000/some\_dir/some\_file\_3'
- 'hdfs://hdfs1:9000/another\_dir/some\_file\_1'
- 'hdfs://hdfs1:9000/another\_dir/some\_file\_2'
- 'hdfs://hdfs1:9000/another\_dir/some\_file\_3'


2. Query the amount of rows in these files:



```
SELECT count(*)
FROM hdfs('hdfs://hdfs1:9000/{some,another}_dir/some_file_{1..3}', 'TSV', 'name String, value UInt32')

```

3. Query the amount of rows in all files of these two directories:



```
SELECT count(*)
FROM hdfs('hdfs://hdfs1:9000/{some,another}_dir/*', 'TSV', 'name String, value UInt32')

```

NoteIf your listing of files contains number ranges with leading zeros, use the construction with braces for each digit separately or use `?`.


**Example**


Query the data from files named `file000`, `file001`, ... , `file999`:



```
SELECT count(*)
FROM hdfs('hdfs://hdfs1:9000/big_dir/file{0..9}{0..9}{0..9}', 'CSV', 'name String, value UInt32')

```

## Virtual Columns[​](#virtual-columns "Direct link to Virtual Columns")


- `_path` — Path to the file. Type: `LowCardinality(String)`.
- `_file` — Name of the file. Type: `LowCardinality(String)`.
- `_size` — Size of the file in bytes. Type: `Nullable(UInt64)`. If the size is unknown, the value is `NULL`.
- `_time` — Last modified time of the file. Type: `Nullable(DateTime)`. If the time is unknown, the value is `NULL`.


## use\_hive\_partitioning setting[​](#hive-style-partitioning "Direct link to use_hive_partitioning setting")


When setting `use_hive_partitioning` is set to 1, ClickHouse will detect Hive\-style partitioning in the path (`/name=value/`) and will allow to use partition columns as virtual columns in the query. These virtual columns will have the same names as in the partitioned path.


**Example**


Use virtual column, created with Hive\-style partitioning



```
SELECT * FROM HDFS('hdfs://hdfs1:9000/data/path/date=*/country=*/code=*/*.parquet') WHERE date > '2020-01-01' AND country = 'Netherlands' AND code = 42;

```

## Storage Settings[​](#storage-settings "Direct link to Storage Settings")


- [hdfs\_truncate\_on\_insert](/docs/operations/settings/settings#hdfs_truncate_on_insert) \- allows to truncate file before insert into it. Disabled by default.
- [hdfs\_create\_new\_file\_on\_insert](/docs/operations/settings/settings#hdfs_create_new_file_on_insert) \- allows to create a new file on each insert if format has suffix. Disabled by default.
- [hdfs\_skip\_empty\_files](/docs/operations/settings/settings#hdfs_skip_empty_files) \- allows to skip empty files while reading. Disabled by default.


## Related[​](#related "Direct link to Related")


- [Virtual columns](/docs/engines/table-engines#table_engines-virtual_columns)
[PreviousmergeTreeTextIndex](/docs/sql-reference/table-functions/mergeTreeTextIndex)[NexthdfsCluster](/docs/sql-reference/table-functions/hdfsCluster)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned_value)- [Globs in path](#globs_in_path)- [Virtual Columns](#virtual-columns)- [use\_hive\_partitioning setting](#hive-style-partitioning)- [Storage Settings](#storage-settings)- [Related](#related)
Was this page helpful?
