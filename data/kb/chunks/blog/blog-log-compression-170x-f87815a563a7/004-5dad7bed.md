---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Compressing
topic: compressing-nginx-logs-170x-with-column-storage-clickhouse
ch_version_introduced: '1185.161'
last_updated: '2026-09-07'
chunk_index: 4
total_chunks_in_doc: 12
---

calculate compression rate, we divide compress size by the original uncompressed size on disk.* Now we capture our baseline for comparison, let’s ingest the data into ClickHouse and start applying our ideas. ## Ingest logs into ClickHouse \#

First we need to create a table to insert the logs, we call it nginx\_raw that has a simple String field and no specific order.

```
1CREATE TABLE nginx_raw
2(
3    `Body` String
4) ORDER BY ()
```
Copy command
With the table created, we can ingest the logs file. In the example below we insert from S3 directly. We can also validate that the full dataset was ingested correctly.

```
INSERT INTO nginx_raw SELECT line As Body FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/http_logs/nginx-66.log.gz', 'LineAsString')

SELECT count() FROM nginx_raw

┌──count()─┐
│ 66747290 │ -- 66.75 million
└──────────┘
```
Copy command

> The above insert command can be used to load the data into your own ClickHouse instance. Load time will depend on your local ClickHouse resources and connectivity (file is \~640MB).

Let's check how much disk space this table uses. We can do that by querying the [system.parts](https://clickhouse.com/docs/operations/system-tables/parts) table, which stores details about each table part, including its uncompressed and compressed sizes on disk.

```
SELECT
    `table`,
    formatReadableSize(SUM(data_uncompressed_bytes)) AS uncompressed_size,
    formatReadableSize(SUM(data_compressed_bytes)) AS compressed_size
FROM system.parts
WHERE (database = 'logs_blog') AND (`table` = 'nginx_raw') AND active
GROUP BY `table`
ORDER BY `table` ASC

   ┌─table─────┬─uncompressed_size─┬─compressed_size─┐
   │ nginx_raw │ 20.19 GiB         │ 575.62 MiB      │
   └───────────┴───────────────────┴─────────────────┘
```
Copy command
No surprises here, the uncompressed size matches the one on the local disk. Internally, ClickHouse uses ZSTD(1\) compression by default \- hence the comparable compressed size.

### Turn Nginx log to a structured log (up to 56x)  \#

The first step towards 170x compression is to turn the plain log we have into a structured log where each significant value (e.g., IP address, request method, URL, status code, user agent) can be stored into its own column.

Instead of storing this entire string as one column, we can parse it into individual columns like:
