---
source: blog
url: https://clickhouse.com/docs/en/integrations/data-formats
topic: an-introduction-to-data-formats-in-clickhouse
ch_version_introduced: '1.112'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 5
---

custom text formats is to use a [Template format](https://clickhouse.com/docs/en/integrations/data-formats/templates-regexp#importing-based-on-a-template). The Template format is even more powerful in terms of exporting data because it allows rendering query results into high\-level formats, like [HTML](https://clickhouse.com/docs/en/integrations/data-formats/templates-regexp#exporting-to-html-files). ## Native and binary formats [\#](/blog/data-formats-clickhouse-csv-tsv-parquet-native#native-and-binary-formats)

ClickHouse has its own [native format](https://clickhouse.com/docs/en/integrations/data-formats/binary-native#exporting-in-a-native-clickhouse-format) that can be used to import and export data. It's more efficient than text formats regarding processing speed and space usage. The Native format is helpful for transferring data between ClickHouse servers when they don't have a direct connection with each other. For example, to transfer data from a ClickHouse server to ClickHouse Cloud:

```
clickhouse-client -q "SELECT * FROM some_table FORMAT Native" | \
clickhouse-client --host some.aws.clickhouse.cloud --secure \
--port 9440 --password 12345 \
-q "INSERT INTO some_table FORMAT Native"

```

[Binary formats](https://clickhouse.com/docs/en/integrations/data-formats/binary-native#exporting-to-rowbinary) are usually more efficient and safe than text formats but are limited in support. ClickHouse has the RowBinary format for general binary cases, and RawBLOB is used with (but is not limited to) files. Additionally, ClickHouse supports popular serialization formats like [Protocol Buffers](https://clickhouse.com/docs/en/integrations/data-formats/binary-native#protocol-buffers), [Cap’n Proto](https://clickhouse.com/docs/en/integrations/data-formats/binary-native#capn-proto) and [Message Pack](https://clickhouse.com/docs/en/integrations/data-formats/binary-native#messagepack).

## Parquet and other Apache formats [\#](/blog/data-formats-clickhouse-csv-tsv-parquet-native#parquet-and-other-apache-formats)

Apache has multiple data storage and serialization formats that are popular in Hadoop environments. ClickHouse can work with all of them, [including Parquet](https://clickhouse.com/docs/en/integrations/data-formats/parquet-arrow-avro-orc#working-with-parquet-data).

We can import data from a Parquet file:

```
clickhouse-client -q "INSERT INTO some_table FORMAT Parquet" < 
data.parquet

```

By using the [`file()`](https://clickhouse.com/docs/en/sql-reference/table-functions/file/) function and [`clickhouse-local`](https://clickhouse.com/blog/extracting-converting-querying-local-files-with-sql-clickhouse-local), we can explore data before actually loading it into a table:

```

SELECT *
FROM file('data.parquet')
LIMIT 3;

┌─path──────────────────────┬─date───────┬─hits─┐
│ Akiba_Hebrew_Academy      │ 2017-08-01 │  241 │
│ Aegithina_tiphia          │ 2018-02-01 │   34 │
│ 1971-72_Utah_Stars_season │ 2016-10-01 │    1 │
└───────────────────────────┴────────────┴──────┘


```

We can also export data to a Parquet file using the client:

```
clickhouse-client -q "SELECT * FROM some_table FORMAT Parquet" > 
file.parquet

```

Find out more about other supported Apache formats, such as [Avro](https://clickhouse.com/docs/en/integrations/data-formats/parquet-arrow-avro-orc#importing-and-exporting-in-avro-format), [Arrow](https://clickhouse.com/docs/en/integrations/data-formats/parquet-arrow-avro-orc#working-with-arrow-format), and [ORC](https://clickhouse.com/docs/en/integrations/data-formats/parquet-arrow-avro-orc#importing-and-exporting-orc-data).

## SQL dumps [\#](/blog/data-formats-clickhouse-csv-tsv-parquet-native#sql-dumps)

Though SQL dumps are inefficient in storing and transferring data, ClickHouse supports loading data from MySQL dumps and creating SQL dumps for Mysql, PostgreSQL, and other databases.

To create a SQL dump, the [`SQLInsert`](https://clickhouse.com/docs/en/interfaces/formats/#sqlinsert) format should be used:

```
SET output_format_sql_insert_table_name = 'a_table_name';
SET output_format_sql_insert_include_column_names = 0;
SELECT * FROM some_table
INTO OUTFILE 'dump.sql'
FORMAT SQLInsert;

```
