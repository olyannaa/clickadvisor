# INSERT INTO Statement \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- INSERT INTO
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/insert-into.md)# INSERT INTO Statement

Inserts data into a table.


**Syntax**



```
INSERT INTO [TABLE] [db.]table [(c1, c2, c3)] [SETTINGS ...] VALUES (v11, v12, v13), (v21, v22, v23), ...

```

You can specify a list of columns to insert using the `(c1, c2, c3)`. You can also use an expression with column [matcher](/docs/sql-reference/statements/select#asterisk) such as `*` and/or [modifiers](/docs/sql-reference/statements/select#select-modifiers) such as [APPLY](/docs/sql-reference/statements/select/apply-modifier), [EXCEPT](/docs/sql-reference/statements/select/except-modifier), [REPLACE](/docs/sql-reference/statements/select/replace-modifier).


For example, consider the table:



```
SHOW CREATE insert_select_testtable;

```


```
CREATE TABLE insert_select_testtable
(
    `a` Int8,
    `b` String,
    `c` Int8
)
ENGINE = MergeTree()
ORDER BY a

```


```
INSERT INTO insert_select_testtable (*) VALUES (1, 'a', 1) ;

```

If you want to insert data into all of the columns, except column `b`, you can do so using the `EXCEPT` keyword. With reference to the syntax above, you will need to ensure that you insert as many values (`VALUES (v11, v13)`) as you specify columns (`(c1, c3)`) :



```
INSERT INTO insert_select_testtable (* EXCEPT(b)) Values (2, 2);

```


```
SELECT * FROM insert_select_testtable;

```


```
┌─a─┬─b─┬─c─┐
│ 2 │   │ 2 │
└───┴───┴───┘
┌─a─┬─b─┬─c─┐
│ 1 │ a │ 1 │
└───┴───┴───┘

```

In this example, we see that the second inserted row has `a` and `c` columns filled by the passed values, and `b` filled with value by default. It is also possible to use the `DEFAULT` keyword to insert default values:



```
INSERT INTO insert_select_testtable VALUES (1, DEFAULT, 1) ;

```

If a list of columns does not include all existing columns, the rest of the columns are filled with:


- The values calculated from the `DEFAULT` expressions specified in the table definition.
- Zeros and empty strings, if `DEFAULT` expressions are not defined.


Data can be passed to the INSERT in any [format](/docs/sql-reference/formats) supported by ClickHouse. The format must be specified explicitly in the query:



```
INSERT INTO [db.]table [(c1, c2, c3)] FORMAT format_name data_set

```

For example, the following query format is identical to the basic version of `INSERT ... VALUES`:



```
INSERT INTO [db.]table [(c1, c2, c3)] FORMAT Values (v11, v12, v13), (v21, v22, v23), ...

```

ClickHouse removes all spaces and one line feed (if there is one) before the data. When forming a query, we recommend putting the data on a new line after the query operators which is important if the data begins with spaces.


Example:



```
INSERT INTO t FORMAT TabSeparated
11  Hello, world!
22  Qwerty

```

You can insert data separately from the query by using the [command\-line client](/docs/operations/utilities/clickhouse-local) or the [HTTP interface](/docs/interfaces/http).


NoteIf you want to specify `SETTINGS` for `INSERT` query then you have to do it *before* the `FORMAT` clause since everything after `FORMAT format_name` is treated as data. For example:
```
INSERT INTO table SETTINGS ... FORMAT format_name data_set

```



## Constraints[​](#constraints "Direct link to Constraints")


If a table has [constraints](/docs/sql-reference/statements/create/table#constraints), their expressions will be checked for each row of inserted data. If any of those constraints is not satisfied — the server will raise an exception containing the constraint name and expression, and the query will be stopped.


## Data Type Validation[​](#data-type-validation "Direct link to Data Type Validation")


ClickHouse validates allowed data types (controlled by settings like `enable_time_time64_type`, `allow_suspicious_low_cardinality_types`, `allow_suspicious_fixed_string_types`, etc.) only during table creation (`CREATE TABLE`) and schema modification (`ALTER TABLE`), not during `INSERT`.


This means that if a table with a disallowed data type already exists, data can be inserted into it even when the corresponding setting is disabled on the server. This is by design — once a table is created, inserts should not be blocked by settings that control type creation.


For example:



```
SET enable_time_time64_type = 1;

CREATE TABLE events
(
    `id` UInt64,
    `event_time` Time
)
ENGINE = MergeTree()
ORDER BY id;

SET enable_time_time64_type = 0;

-- This works even though the setting is now disabled.
-- The table already exists, so inserts are not blocked.
INSERT INTO events VALUES (1, '14:30:25');

-- But creating a new table with the Time type will fail.
CREATE TABLE events_new
(
    `id` UInt64,
    `event_time` Time
)
ENGINE = MergeTree()
ORDER BY id; -- ERR: TYPE_TIME_TIME64_IS_NOT_ENABLED

```

NoteAs a consequence, a client with a newer version (where a setting is enabled by default) can insert data with disallowed data types into a server with an older version (where the setting is disabled), as long as the target table already has the corresponding column types. The validation is enforced at the DDL level, not at the DML level.


## Inserting the Results of SELECT[​](#inserting-the-results-of-select "Direct link to Inserting the Results of SELECT")


**Syntax**



```
INSERT INTO [TABLE] [db.]table [(c1, c2, c3)] SELECT ...

```

Columns are mapped according to their position in the `SELECT` clause. However, their names in the `SELECT` expression and the table for `INSERT` may differ. If necessary, type casting is performed.


None of the data formats except the Values format allow setting values to expressions such as `now()`, `1 + 2`, and so on. The Values format allows limited use of expressions, but this is not recommended, because in this case inefficient code is used for their execution.


Other queries for modifying data parts are not supported: `UPDATE`, `DELETE`, `REPLACE`, `MERGE`, `UPSERT`, `INSERT UPDATE`.
However, you can delete old data using `ALTER TABLE ... DROP PARTITION`.


The `FORMAT` clause must be specified at the end of the query if the `SELECT` clause contains the table function [input()](/docs/sql-reference/table-functions/input).


To insert a default value instead of `NULL` into a column with a non\-nullable data type, enable the [insert\_null\_as\_default](/docs/operations/settings/settings#insert_null_as_default) setting.


`INSERT` also supports CTE (common table expression). For example, the following two statements are equivalent:



```
INSERT INTO x WITH y AS (SELECT * FROM numbers(10)) SELECT * FROM y;
WITH y AS (SELECT * FROM numbers(10)) INSERT INTO x SELECT * FROM y;

```

## Inserting Data from a File[​](#inserting-data-from-a-file "Direct link to Inserting Data from a File")


**Syntax**



```
INSERT INTO [TABLE] [db.]table [(c1, c2, c3)] FROM INFILE file_name [COMPRESSION type] [SETTINGS ...] [FORMAT format_name]

```

Use the syntax above to insert data from a file, or files, stored on the **client** side. `file_name` and `type` are string literals. Input file [format](/docs/interfaces/formats) must be set in the `FORMAT` clause.


Compressed files are supported. The compression type is detected by the extension of the file name. Or it can be explicitly specified in a `COMPRESSION` clause. Supported types are: `'none'`, `'gzip'`, `'deflate'`, `'br'`, `'xz'`, `'zstd'`, `'lz4'`, `'bz2'`.


This functionality is available in the [command\-line client](/docs/interfaces/client) and [clickhouse\-local](/docs/operations/utilities/clickhouse-local).


**Examples**


### Single file with FROM INFILE[​](#single-file-with-from-infile "Direct link to Single file with FROM INFILE")


Execute the following queries using [command\-line client](/docs/interfaces/client):



```
echo 1,A > input.csv ; echo 2,B >> input.csv
clickhouse-client --query="CREATE TABLE table_from_file (id UInt32, text String) ENGINE=MergeTree() ORDER BY id;"
clickhouse-client --query="INSERT INTO table_from_file FROM INFILE 'input.csv' FORMAT CSV;"
clickhouse-client --query="SELECT * FROM table_from_file FORMAT PrettyCompact;"

```


```
┌─id─┬─text─┐
│  1 │ A    │
│  2 │ B    │
└────┴──────┘

```

### Multiple files with FROM INFILE using globs[​](#multiple-files-with-from-infile-using-globs "Direct link to Multiple files with FROM INFILE using globs")


This example is very similar to the previous one but inserts are performed from multiple files using `FROM INFILE 'input_*.csv`.



```
echo 1,A > input_1.csv ; echo 2,B > input_2.csv
clickhouse-client --query="CREATE TABLE infile_globs (id UInt32, text String) ENGINE=MergeTree() ORDER BY id;"
clickhouse-client --query="INSERT INTO infile_globs FROM INFILE 'input_*.csv' FORMAT CSV;"
clickhouse-client --query="SELECT * FROM infile_globs FORMAT PrettyCompact;"

```

TipIn addition to selecting multiple files with `*`, you can use ranges (`{1,2}` or `{1..9}`) and other [glob substitutions](/docs/sql-reference/table-functions/file#globs-in-path). These three all would work with the example above:
```
INSERT INTO infile_globs FROM INFILE 'input_*.csv' FORMAT CSV;
INSERT INTO infile_globs FROM INFILE 'input_{1,2}.csv' FORMAT CSV;
INSERT INTO infile_globs FROM INFILE 'input_?.csv' FORMAT CSV;

```



## Inserting using a Table Function[​](#inserting-using-a-table-function "Direct link to Inserting using a Table Function")


Data can be inserted into tables referenced by [table functions](/docs/sql-reference/table-functions).


**Syntax**



```
INSERT INTO [TABLE] FUNCTION table_func ...

```

**Example**


The [remote](/docs/sql-reference/table-functions/remote) table function is used in the following queries:



```
CREATE TABLE simple_table (id UInt32, text String) ENGINE=MergeTree() ORDER BY id;
INSERT INTO TABLE FUNCTION remote('localhost', default.simple_table)
    VALUES (100, 'inserted via remote()');
SELECT * FROM simple_table;

```


```
┌──id─┬─text──────────────────┐
│ 100 │ inserted via remote() │
└─────┴───────────────────────┘

```

## Inserting into ClickHouse Cloud[​](#inserting-into-clickhouse-cloud "Direct link to Inserting into ClickHouse Cloud")


By default, services on ClickHouse Cloud provide multiple replicas for high availability. When you connect to a service, a connection is established to one of these replicas.


After an `INSERT` succeeds, data is written to the underlying storage. However, it may take some time for replicas to receive these updates. Therefore, if you use a different connection that executes a `SELECT` query on one of these other replicas, the updated data may not yet be reflected.


It is possible to use the `select_sequential_consistency` to force the replica to receive the latest updates. Here is an example of a `SELECT` query using this setting:



```
SELECT .... SETTINGS select_sequential_consistency = 1;

```

Note that using `select_sequential_consistency` will increase the load on ClickHouse Keeper (used by ClickHouse Cloud internally) and may result in slower performance depending on the load on the service. We recommend against enabling this setting unless necessary. The recommended approach is to execute read/writes in the same session or to use a client driver that uses the native protocol (and thus supports sticky connections).


## Inserting into a replicated setup[​](#inserting-into-a-replicated-setup "Direct link to Inserting into a replicated setup")


In a replicated setup, data will be visible on other replicas after it has been replicated. Data begins being replicated (downloaded on other replicas) immediately after an `INSERT`. This differs from ClickHouse Cloud, where data is immediately written to shared storage and replicas subscribe to metadata changes.


Note that for replicated setups, `INSERTs` can sometimes take a considerable amount of time (in the order of one second) as it requires committing to ClickHouse Keeper for distributed consensus. Using S3 for storage also adds additional latency.


## Performance Considerations[​](#performance-considerations "Direct link to Performance Considerations")


`INSERT` sorts the input data by primary key and splits them into partitions by a partition key. If you insert data into several partitions at once, it can significantly reduce the performance of the `INSERT` query. To avoid this:


- Add data in fairly large batches, such as 100,000 rows at a time.
- Group data by a partition key before uploading it to ClickHouse.


Performance will not decrease if:


- Data is added in real time.
- You upload data that is usually sorted by time.


### Asynchronous inserts[​](#asynchronous-inserts "Direct link to Asynchronous inserts")


It is possible to asynchronously insert data in small but frequent inserts. The data from such insertions is combined into batches and then safely inserted into a table. To use asynchronous inserts, enable the [`async_insert`](/docs/operations/settings/settings#async_insert) setting.


Using `async_insert` or the [`Buffer` table engine](/docs/engines/table-engines/special/buffer) results in additional buffering.


### Large or long\-running inserts[​](#large-or-long-running-inserts "Direct link to Large or long-running inserts")


When you are inserting large amounts of data, ClickHouse will optimize write performance through a process called "squashing". Small blocks of inserted data in memory are merged and squashed into larger blocks before being written to disk. Squashing reduces the overhead associated with each write operation. In this process, inserted data will be available to query after ClickHouse completes writing each [`max_insert_block_size`](/docs/operations/settings/settings#max_insert_block_size) rows.


**See Also**


- [async\_insert](/docs/operations/settings/settings#async_insert)
- [wait\_for\_async\_insert](/docs/operations/settings/settings#wait_for_async_insert)
- [wait\_for\_async\_insert\_timeout](/docs/operations/settings/settings#wait_for_async_insert_timeout)
- [async\_insert\_max\_data\_size](/docs/operations/settings/settings#async_insert_max_data_size)
- [async\_insert\_busy\_timeout\_ms](/docs/operations/settings/settings#async_insert_busy_timeout_max_ms)
- [async\_insert\_stale\_timeout\_ms](/docs/operations/settings/settings#async_insert_max_data_size)
[PreviousWITH](/docs/sql-reference/statements/select/with)[NextCREATE](/docs/sql-reference/statements/create)- [Constraints](#constraints)- [Data Type Validation](#data-type-validation)- [Inserting the Results of SELECT](#inserting-the-results-of-select)- [Inserting Data from a File](#inserting-data-from-a-file)
	- [Single file with FROM INFILE](#single-file-with-from-infile)- [Multiple files with FROM INFILE using globs](#multiple-files-with-from-infile-using-globs)- [Inserting using a Table Function](#inserting-using-a-table-function)- [Inserting into ClickHouse Cloud](#inserting-into-clickhouse-cloud)- [Inserting into a replicated setup](#inserting-into-a-replicated-setup)- [Performance Considerations](#performance-considerations)
	- [Asynchronous inserts](#asynchronous-inserts)- [Large or long\-running inserts](#large-or-long-running-inserts)
Was this page helpful?
