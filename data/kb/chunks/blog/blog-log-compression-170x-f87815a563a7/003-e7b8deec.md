---
source: blog
url: https://www.zanbil.ir/"
topic: compressing-nginx-logs-170x-with-column-storage
ch_version_introduced: '185.161'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 11
---

look at compression formats achievable for logs with less obvious structure. ### Get started with ClickStack [\#](/blog/log-compression-170x#test) Spin up the world’s fastest and most scalable open source observability stack, in seconds. [Try now](https://clickhouse.com/docs/use-cases/observability/clickstack/getting-started?loc=blog-o11y-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) ## Capture a baseline [\#](/blog/log-compression-170x#capture-a-baseline)

For any experiment that aims at benchmarking something, you need to establish a baseline. For us the baseline is how much storage space a log dataset uses on local disk when stored uncompressed.

For our experiments we’ll use a dataset of nginx access logs containing 66 millions entries. Users can replicate these tests \- we’ve made the file publicly accessible in subsequent commands. On disk this file when uncompressed uses 20Gb of disk space.

```
$ wc -l nginx-66.log
66747290 nginx-66.log

$ du -h nginx-66.log
20G	nginx-66.log

```

Since ClickHouse compresses data when storing it on disk and supports different [compression algorithms](https://clickhouse.com/docs/data-compression/compression-in-clickhouse#choosing-the-right-column-compression-codec), it's also important to capture a few algorithms to see how well they compare to our experiment.

We compressed the raw log file using GZIP, ZSTD(3\) and LZ4 to compare the performances. As we can see, compression on disk is actually quite impressive, with ZSTD(3\) already achieving a 38x compression ratio.

| Compression | Size on disk | Compression ratio |
| --- | --- | --- |
| None | 20 GB | 1 |
| LZ4 | 1 GB | 20x |
| GZIP | 641 MB | 31x |
| ZSTD(3\) | 522 MB | 38x |


*To calculate compression rate, we divide compress size by the original uncompressed size on disk.*

Now we capture our baseline for comparison, let’s ingest the data into ClickHouse and start applying our ideas.

## Ingest logs into ClickHouse [\#](/blog/log-compression-170x#ingest-logs-into-clickhouse)

First we need to create a table to insert the logs, we call it nginx\_raw that has a simple String field and no specific order.

```

```
1CREATE TABLE nginx_raw
2(
3    `Body` String
4) ORDER BY ()
```

```

With the table created, we can ingest the logs file. In the example below we insert from S3 directly. We can also validate that the full dataset was ingested correctly.

```

```
INSERT INTO nginx_raw SELECT line As Body FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/http_logs/nginx-66.log.gz', 'LineAsString')

SELECT count() FROM nginx_raw

┌──count()─┐
│ 66747290 │ -- 66.75 million
└──────────┘
```

```
