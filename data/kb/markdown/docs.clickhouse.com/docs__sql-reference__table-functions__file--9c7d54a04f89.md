# file \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- file
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/file.md)# file Table Function


A table engine which provides a table\-like interface to SELECT from and INSERT into files, similar to the [s3](/docs/sql-reference/table-functions/url) table function. Use `file()` when working with local files, and `s3()` when working with buckets in object storage such as S3, GCS, or MinIO.


The `file` function can be used in `SELECT` and `INSERT` queries to read from or write to files.


## Syntax[​](#syntax "Direct link to Syntax")



```
file([path_to_archive ::] path [,format] [,structure] [,compression])

```

For `SELECT` queries, `path` can also be an expression that returns an `Array(String)`:



```
file(['file1.csv', 'file2.csv'], 'CSV', 'column1 UInt32, column2 UInt32')

```

## Arguments[​](#arguments "Direct link to Arguments")




| Parameter Description| `path` The relative path to the file from [user\_files\_path](/docs/operations/server-configuration-parameters/settings#user_files_path), or an `Array(String)` of paths in `SELECT` queries. Supports in read\-only mode the following [globs](#globs-in-path): `*`, `?`, `{abc,def}` (with `'abc'` and `'def'` being strings) and `{N..M}` (with `N` and `M` being numbers).| `path_to_archive` The relative path to a zip/tar/7z archive. Supports the same globs as `path`.| `format` The [format](/docs/interfaces/formats) of the file.| `structure` Structure of the table. Format: `'column1_name column1_type, column2_name column2_type, ...'`.| `compression` The existing compression type when used in a `SELECT` query, or the desired compression type when used in an `INSERT` query. Supported compression types are `gz`, `br`, `xz`, `zst`, `lz4`, and `bz2`. | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


TipWhen the `structure` argument is omitted, ClickHouse infers the schema from the format itself.
Different formats produce different default column names and types.
To see the schema for a specific format, use [`DESC`](/docs/sql-reference/statements/describe-table) with the [`format`](/docs/sql-reference/table-functions/format) table function.For example:
```
DESC format(LineAsString, 'Hello\nWorld')

```

```
┌─name─┬─type───┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
│ line │ String │              │                    │         │                  │                │
└──────┴────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

```





## Returned value[​](#returned_value "Direct link to Returned value")


A table for reading or writing data in a file.


## Examples for Writing to a File[​](#examples-for-writing-to-a-file "Direct link to Examples for Writing to a File")


### Write to a TSV file[​](#write-to-a-tsv-file "Direct link to Write to a TSV file")



```
INSERT INTO TABLE FUNCTION
file('test.tsv', 'TSV', 'column1 UInt32, column2 UInt32, column3 UInt32')
VALUES (1, 2, 3), (3, 2, 1), (1, 3, 2)

```

As a result, the data is written into the file `test.tsv`:



```
# cat /var/lib/clickhouse/user_files/test.tsv
1    2    3
3    2    1
1    3    2

```

### Partitioned write to multiple TSV files[​](#partitioned-write-to-multiple-tsv-files "Direct link to Partitioned write to multiple TSV files")


If you specify a `PARTITION BY` expression when inserting data into a table function of type `file()`, then a separate file is created for each partition. Splitting the data into separate files helps to improve performance of read operations.



```
INSERT INTO TABLE FUNCTION
file('test_{_partition_id}.tsv', 'TSV', 'column1 UInt32, column2 UInt32, column3 UInt32')
PARTITION BY column3
VALUES (1, 2, 3), (3, 2, 1), (1, 3, 2)

```

As a result, the data is written into three files: `test_1.tsv`, `test_2.tsv`, and `test_3.tsv`.



```
# cat /var/lib/clickhouse/user_files/test_1.tsv
3    2    1

# cat /var/lib/clickhouse/user_files/test_2.tsv
1    3    2

# cat /var/lib/clickhouse/user_files/test_3.tsv
1    2    3

```

## Examples for Reading from a File[​](#examples-for-reading-from-a-file "Direct link to Examples for Reading from a File")


### SELECT from a CSV file[​](#select-from-a-csv-file "Direct link to SELECT from a CSV file")


First, set `user_files_path` in the server configuration and prepare a file `test.csv`:



```
$ grep user_files_path /etc/clickhouse-server/config.xml
    <user_files_path>/var/lib/clickhouse/user_files/</user_files_path>

$ cat /var/lib/clickhouse/user_files/test.csv
    1,2,3
    3,2,1
    78,43,45

```

Then, read data from `test.csv` into a table and select its first two rows:



```
SELECT * FROM
file('test.csv', 'CSV', 'column1 UInt32, column2 UInt32, column3 UInt32')
LIMIT 2;

```


```
┌─column1─┬─column2─┬─column3─┐
│       1 │       2 │       3 │
│       3 │       2 │       1 │
└─────────┴─────────┴─────────┘

```

### Inserting data from a file into a table[​](#inserting-data-from-a-file-into-a-table "Direct link to Inserting data from a file into a table")



```
INSERT INTO FUNCTION
file('test.csv', 'CSV', 'column1 UInt32, column2 UInt32, column3 UInt32')
VALUES (1, 2, 3), (3, 2, 1);

```


```
SELECT * FROM
file('test.csv', 'CSV', 'column1 UInt32, column2 UInt32, column3 UInt32');

```


```
┌─column1─┬─column2─┬─column3─┐
│       1 │       2 │       3 │
│       3 │       2 │       1 │
└─────────┴─────────┴─────────┘

```

Reading data from `table.csv`, located in `archive1.zip` or/and `archive2.zip`:



```
SELECT * FROM file('user_files/archives/archive{1..2}.zip :: table.csv');

```

## Globs in path[​](#globs-in-path "Direct link to Globs in path")


Paths may use globbing. Files must match the whole path pattern, not only the suffix or prefix. There is one exception that if the path refers to an existing
directory and does not use globs, a `*` will be implicitly added to the path so
all the files in the directory are selected.


- `*` — Represents arbitrarily many characters except `/` but including the empty string.
- `?` — Represents an arbitrary single character.
- `{some_string,another_string,yet_another_one}` — Substitutes any of strings `'some_string', 'another_string', 'yet_another_one'`. The strings can contain the `/` symbol.
- `{N..M}` — Represents any number `>= N` and `<= M`.
- `**` \- Represents all files inside a folder recursively.


Constructions with `{}` are similar to the [remote](/docs/sql-reference/table-functions/remote) and [hdfs](/docs/sql-reference/table-functions/hdfs) table functions.


## Examples[​](#examples "Direct link to Examples")


**Example**


Suppose there are these files with the following relative paths:


- `some_dir/some_file_1`
- `some_dir/some_file_2`
- `some_dir/some_file_3`
- `another_dir/some_file_1`
- `another_dir/some_file_2`
- `another_dir/some_file_3`


Query the total number of rows in all files:



```
SELECT count(*) FROM file('{some,another}_dir/some_file_{1..3}', 'TSV', 'name String, value UInt32');

```

An alternative path expression which achieves the same:



```
SELECT count(*) FROM file('{some,another}_dir/*', 'TSV', 'name String, value UInt32');

```

Query the total number of rows in `some_dir` using the implicit `*`:



```
SELECT count(*) FROM file('some_dir', 'TSV', 'name String, value UInt32');

```

NoteIf your listing of files contains number ranges with leading zeros, use the construction with braces for each digit separately or use `?`.


**Example**


Query the total number of rows in files named `file000`, `file001`, ... , `file999`:



```
SELECT count(*) FROM file('big_dir/file{0..9}{0..9}{0..9}', 'CSV', 'name String, value UInt32');

```

**Example**


Query the total number of rows from all files inside directory `big_dir/` recursively:



```
SELECT count(*) FROM file('big_dir/**', 'CSV', 'name String, value UInt32');

```

**Example**


Query the total number of rows from all files `file002` inside any folder in directory `big_dir/` recursively:



```
SELECT count(*) FROM file('big_dir/**/file002', 'CSV', 'name String, value UInt32');

```

## Virtual Columns[​](#virtual-columns "Direct link to Virtual Columns")


- `_path` — Path to the file. Type: `LowCardinality(String)`.
- `_file` — Name of the file. Type: `LowCardinality(String)`.
- `_size` — Size of the file in bytes. Type: `Nullable(UInt64)`. If the file size is unknown, the value is `NULL`.
- `_time` — Last modified time of the file. Type: `Nullable(DateTime)`. If the time is unknown, the value is `NULL`.


## use\_hive\_partitioning setting[​](#hive-style-partitioning "Direct link to use_hive_partitioning setting")


When setting `use_hive_partitioning` is set to 1, ClickHouse will detect Hive\-style partitioning in the path (`/name=value/`) and will allow to use partition columns as virtual columns in the query. These virtual columns will have the same names as in the partitioned path.


**Example**


Use virtual column, created with Hive\-style partitioning



```
SELECT * FROM file('data/path/date=*/country=*/code=*/*.parquet') WHERE date > '2020-01-01' AND country = 'Netherlands' AND code = 42;

```

## Settings[​](#settings "Direct link to Settings")




| Setting Description| [engine\_file\_empty\_if\_not\_exists](/docs/operations/settings/settings#engine_file_empty_if_not_exists) allows to select empty data from a file that doesn't exist. Disabled by default.| [engine\_file\_truncate\_on\_insert](/docs/operations/settings/settings#engine_file_truncate_on_insert) allows to truncate file before insert into it. Disabled by default.| [engine\_file\_allow\_create\_multiple\_files](/docs/operations/settings/settings#engine_file_allow_create_multiple_files) allows to create a new file on each insert if format has suffix. Disabled by default.| [engine\_file\_skip\_empty\_files](/docs/operations/settings/settings#engine_file_skip_empty_files) allows to skip empty files while reading. Disabled by default.| [storage\_file\_read\_method](/docs/operations/settings/settings#engine_file_empty_if_not_exists) method of reading data from storage file, one of: read, pread, mmap (only for clickhouse\-local). Default value: `pread` for clickhouse\-server, `mmap` for clickhouse\-local. | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


## Related[​](#related "Direct link to Related")


- [Virtual columns](/docs/engines/table-engines#table_engines-virtual_columns)
- [Rename files after processing](/docs/operations/settings/settings#rename_files_after_processing)
[Previousexecutable](/docs/engines/table-functions/executable)[NextfileCluster](/docs/sql-reference/table-functions/fileCluster)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned_value)- [Examples for Writing to a File](#examples-for-writing-to-a-file)
	- [Write to a TSV file](#write-to-a-tsv-file)- [Partitioned write to multiple TSV files](#partitioned-write-to-multiple-tsv-files)- [Examples for Reading from a File](#examples-for-reading-from-a-file)
	- [SELECT from a CSV file](#select-from-a-csv-file)- [Inserting data from a file into a table](#inserting-data-from-a-file-into-a-table)- [Globs in path](#globs-in-path)- [Examples](#examples)- [Virtual Columns](#virtual-columns)- [use\_hive\_partitioning setting](#hive-style-partitioning)- [Settings](#settings)- [Related](#related)
Was this page helpful?
