# An Introduction to Data Formats in ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# An Introduction to Data Formats in ClickHouse

![](/_next/image?url=%2Fuploads%2FDenys_96799559c1.png&w=96&q=75)[Denys Golotiuk](/authors/denys-golotiuk)Jan 24, 2023 · 4 minutes read![data-formats.png](/uploads/data_formats_48f2df5c4d.png)
## Introduction [\#](/blog/data-formats-clickhouse-csv-tsv-parquet-native#introduction)


Users new to ClickHouse are often surprised by the number of supported data formats, but sometimes need help identifying the best and easiest way to load their data. Since we believe loading data into your favorite OSS database should be as easy as possible, we have recently [enhanced our docs](https://clickhouse.com/docs/en/integrations/data-formats) to include examples for the most popular formats. This also includes some useful hints and tricks for more experienced users.


This post provides a brief overview of ClickHouse's extensive support for different formats and how to load your local files.


## Importing and exporting data [\#](/blog/data-formats-clickhouse-csv-tsv-parquet-native#importing-and-exporting-data)


ClickHouse supports most of the known text and binary data formats. This allows easy integration into almost any working data pipeline to leverage the benefits of ClickHouse.


### Standard text formats [\#](/blog/data-formats-clickhouse-csv-tsv-parquet-native#standard-text-formats)


CSV is one of the most popular formats to store data due to its simplicity. Importing and exporting CSV data is easy with the [CSV](https://clickhouse.com/docs/en/interfaces/formats/#csv) format:



```
clickhouse-client -q "INSERT INTO some_table FORMAT CSV" < data.csv

```

In many cases, CSV files are broken, poorly encoded, and have custom delimiters or even line separators. ClickHouse provides ways to handle any of these cases.


To process CSVs with custom delimiters (`;` in our example), we have to set the following option:



```
SET format_csv_delimiter = ';';

```

### Importing data from broken or custom CSV files [\#](/blog/data-formats-clickhouse-csv-tsv-parquet-native#importing-data-from-broken-or-custom-csv-files)


In cases where the CSV file is encoded in a non\-standard way or just invalid, we can use the [CustomSeparated](https://clickhouse.com/docs/en/sql-reference/formats/#format-customseparated) format to customize escaping rules and delimiters:



```
SET format_custom_field_delimiter = '|';
SET format_custom_row_between_delimiter = ';';
SET format_custom_escaping_rule = 'JSON';

```

Here, we've used the JSON [escaping rule](https://clickhouse.com/docs/en/operations/settings/settings/#format_custom_escaping_rule), `|` as a custom value delimiter, and `;` as the line separator. After the settings are changed, we can continue with our import:



```
INSERT INTO some_table FROM INFILE 'custom.csv' FORMAT CustomSeparated

```

Another popular text data format is Tab Separated Values (TSV), which ClickHouse also supports with the [TabSeparated](https://clickhouse.com/docs/en/interfaces/formats/#tabseparated) format:



```
clickhouse-client -q "INSERT INTO some_table FORMAT TabSeparated" < 
data.tsv

```

Explore more of ClickHouse's capabilities for working with the family of CSV formats in our docs, including [rows skipping](https://clickhouse.com/docs/en/integrations/data-formats/csv-tsv/#skipping-lines-in-a-csv-file), controlling [Null values](https://clickhouse.com/docs/en/integrations/data-formats/csv-tsv#treating-null-values-in-csv-files), [automatic decompression](https://clickhouse.com/docs/en/integrations/data-formats/csv-tsv#working-with-large-csv-files), and more.


### JSON data [\#](/blog/data-formats-clickhouse-csv-tsv-parquet-native#json-data)


ClickHouse can work with almost any JSON data, be that an array of values, an object of objects, or separate JSON objects.


For example, a logging app can write logs as a JSON object per line (known as [NDJson](http://ndjson.org/)). This case can be addressed using the [JSONEachRow](https://clickhouse.com/docs/en/interfaces/formats/#jsoneachrow) format in ClickHouse:



```
clickhouse-client - q "INSERT INTO sometable FORMAT JSONEachRow" < 
access.log

```

Explore how JSON data of different forms can be [loaded to ClickHouse](https://clickhouse.com/docs/en/integrations/data-formats/json#importing-json-data) as well as [exported](https://clickhouse.com/docs/en/integrations/data-formats/json#exporting-json-data). It is worth mentioning that ClickHouse also supports the [BSON format](https://clickhouse.com/docs/en/integrations/data-formats/json#importing-and-exporting-bson) used by MongoDB.


## Regular expressions for custom text formats [\#](/blog/data-formats-clickhouse-csv-tsv-parquet-native#regular-expressions-for-custom-text-formats)


Besides standard formats like CSV or JSON, ClickHouse also supports data import based on [regular expressions](https://clickhouse.com/docs/en/integrations/data-formats/templates-regexp#importing-data-based-on-regular-expressions). In this case, the [`Regexp`](https://clickhouse.com/docs/en/interfaces/formats/#data-format-regexp) format should be used together with the `format_regexp` option containing regular expression with capture groups (treated as table columns):



```
INSERT INTO some_log FROM INFILE 'custom.txt'
SETTINGS
  format_regexp = '([0-9]+?) \[(.+?)\] \- "(.+)"'
FORMAT Regexp

```

This query can be used to load the following example file:



```
121201 [notice] - "Started service"
121202 [error] - "Configuration file not found"
122203 [warning] - "Creating default configuration file"

```

Another option to process custom text formats is to use a [Template format](https://clickhouse.com/docs/en/integrations/data-formats/templates-regexp#importing-based-on-a-template). The Template format is even more powerful in terms of exporting data because it allows rendering query results into high\-level formats, like [HTML](https://clickhouse.com/docs/en/integrations/data-formats/templates-regexp#exporting-to-html-files).


## Native and binary formats [\#](/blog/data-formats-clickhouse-csv-tsv-parquet-native#native-and-binary-formats)


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

This will create the `dump.sql` file with an SQL values dump in it. It will use `a_table_name` as a table name and skip columns declaration. It can then be fed to other DBMS:



```
psql < dump.sql

```

ClickHouse also supports importing data from MySQL dumps using the [`MySQLDump`](https://clickhouse.com/docs/en/interfaces/formats/#mysqldump) format:



```
cat mysql-dump.sql | clickhouse-client -q "INSERT INTO some_data FORMAT MySQLDump"

```

Learn more about [importing and exporting SQL data](https://clickhouse.com/docs/en/integrations/data-formats/sql) in ClickHouse.


## Null format for performance testing [\#](/blog/data-formats-clickhouse-csv-tsv-parquet-native#null-format-for-performance-testing)


There's also a special [Null](https://clickhouse.com/docs/en/interfaces/formats/#null) data format that will not print anything but wait for the query to execute:



```
SELECT *
FROM big_table
LIMIT 100000
FORMAT `Null`

0 rows in set. Elapsed: 1.112 sec. Processed 131.07 thousand rows, 167.57 MB (117.86 thousand rows/s., 150.68 MB/s.)

```

ClickHouse server still returns data to the client, but it's not printed. This makes the `Null` format useful for testing query performance which returns too much data to fit into the terminal.


## Prettifying command line [\#](/blog/data-formats-clickhouse-csv-tsv-parquet-native#prettifying-command-line)


By default, ClickHouse uses the [PrettyCompact](https://clickhouse.com/docs/en/interfaces/formats/#prettycompact) format for the command line client. It outputs data in blocks sometimes (as soon as results are returned):



```

┌─id──────────────────────────┬─gender─┬─birth_year─┐
│ B7mkoLYIZEdoPkfCRTKtYg_0000 │ female │ 1951       │
└─────────────────────────────┴────────┴────────────┘
┌─id──────────────────────────┬─gender─┬─birth_year─┐
│ nzHXUMnmjspwV4JxL-KqzQ_0000 │ female │ 1956       │
└─────────────────────────────┴────────┴────────────┘
┌─id──────────────────────────┬─gender─┬─birth_year─┐
│ 5cs05UbDttZBFBE6tPpjUg_0000 │ male   │ 1989       │
│ 5cs05UbDttZBFBE6tPpjUg_0000 │ male   │ 1989       │
└─────────────────────────────┴────────┴────────────┘
...


```

  

We can use [PrettyCompactMonoBlock](https://clickhouse.com/docs/en/interfaces/formats/#prettycompactmonoblock) to ask ClickHouse to output results as a single table:



```

SELECT * FROM some_table
FORMAT PrettyCompactMonoBlock;

┌─id──────────────────────────┬─gender─┬─birth_year─┐
│ B7mkoLYIZEdoPkfCRTKtYg_0000 │ female │ 1951       │
│ nzHXUMnmjspwV4JxL-KqzQ_0000 │ female │ 1956       │
│ 5cs05UbDttZBFBE6tPpjUg_0000 │ male   │ 1989       │
│ 5cs05UbDttZBFBE6tPpjUg_0000 │ male   │ 1989       │
│ mcXoSkxAk-1xGpSiqnCB1Q_0000 │ female │ 1961       │
└─────────────────────────────┴────────┴────────────┘


```

  

Less compact but easier to perceive is the [Pretty](https://clickhouse.com/docs/en/interfaces/formats/#pretty) format (also [PrettyMonoBlock](https://clickhouse.com/docs/en/interfaces/formats/#prettymonoblock) is available for single table output):



```

SELECT FROM some_table
FORMAT PrettyMonoBlock;

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ path                           ┃ hits ┃ bar(hits, 0, 1500, 25)  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Bangor_City_Forest             │   34 │ ▌                       │
├────────────────────────────────┼──────┼─────────────────────────┤
│ Alireza_Afzal                  │   24 │ ▍                       │
├────────────────────────────────┼──────┼─────────────────────────┤
│ Akhaura-Laksam-Chittagong_Line │   30 │ ▌                       │
├────────────────────────────────┼──────┼─────────────────────────┤
│ 1973_National_500              │   80 │ █▎                      │
├────────────────────────────────┼──────┼─────────────────────────┤
│ Attachment                     │ 1356 │ ██████████████████████▌ │
├────────────────────────────────┼──────┼─────────────────────────┤
│ Kellett_Strait                 │    5 │                         │
├────────────────────────────────┼──────┼─────────────────────────┤
│ Ajarani_River                  │   30 │ ▌                       │
├────────────────────────────────┼──────┼─────────────────────────┤
│ Akbarabad,_Khomeyn             │    8 │ ▏                       │
├────────────────────────────────┼──────┼─────────────────────────┤
│ Adriaan_Theodoor_Peperzak      │   88 │ █▍                      │
├────────────────────────────────┼──────┼─────────────────────────┤
│ Alucita_dryogramma             │    1 │                         │
└────────────────────────────────┴──────┴─────────────────────────┘


```

  

Finally, we can ask ClickHouse to get rid of the table grid with the [PrettySpace](https://clickhouse.com/docs/en/interfaces/formats/#prettyspace) format (and [PrettySpaceMonoBlock](https://clickhouse.com/docs/en/interfaces/formats/#prettyspacemonoblock)):



```

SELECT FROM some_table
FORMAT PrettySpace;

 path                             hits   bar(hits, 0, 1500, 25)

 Bangor_City_Forest                 34   ▌                       
 Alireza_Afzal                      24   ▍                       
 Akhaura-Laksam-Chittagong_Line     30   ▌                       
 1973_National_500                  80   █▎                      
 Attachment                       1356   ██████████████████████▌
 Kellett_Strait                      5                           
 Ajarani_River                      30   ▌                       
 Akbarabad,_Khomeyn                  8   ▏                       
 Adriaan_Theodoor_Peperzak          88   █▍                      
 Alucita_dryogramma                  1       


```

  

## Summary [\#](/blog/data-formats-clickhouse-csv-tsv-parquet-native#summary)


ClickHouse provides tools for all imaginable formats \- standard text, binary or custom ones. Explore in\-depth data formats in the official documentation and [our new guides](https://clickhouse.com/docs/en/integrations/data-formats), which we plan to continue to enhance. Consider using [clickhouse\-local](https://clickhouse.com/blog/extracting-converting-querying-local-files-with-sql-clickhouse-local), which is a powerful portable tool to query, convert and transform data from local files.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
