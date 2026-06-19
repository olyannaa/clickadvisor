# Compressing nginx logs 170x with column storage


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Compressing nginx logs 170x with column storage

![](/_next/image?url=%2Fuploads%2Flio_headshot_singapore_7cc9852011.jpg&w=96&q=75)![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Lionel Palacin](/authors/lionel-palacin) and [Dale McDiarmid](/authors/dale-mcdiarmid)Oct 23, 2025 · 18 minutes read
> **TL;DR**
> 
> 
> Columnar storage offers a path to store logs efficiently while keeping queries fast and flexible. By turning raw logs into structured columns, using optimized data types, and ordering similar values together, it’s possible to achieve over 170x compression.


Storing logs at scale is difficult.


They’re usually unstructured text that doesn’t compress efficiently. Yet, they hold important historical details about how applications and systems behave, information you don’t want to lose that is valuable for debugging during issues.


In an observability system, logs sit alongside traces and metrics. Unlike logs, traces and metrics are already structured and repetitive, which makes them compress naturally in a columnar format. Fields such as Timestamp, ServiceName, and Latency fit well into column\-based storage and compress effectively.


But what if we could give logs a similar structure? Logs could achieve the same kind of efficient compression by identifying the variable parts of each message, extracting them into separate columns, using the most efficient data types, and storing similar data close together on disk.


In this first post, we’ll experiment with this approach and transform raw logs into structured data, with the goal of reaching 170x compression. **In a follow\-up blog, we will explore how to leverage log clustering techniques to extend these ideas to any type of logs and automatically improve their compression ratio.** 


## Why compression is important [\#](/blog/log-compression-170x#why-compression-is-important)


Compression is not just about reduced storage; it also positively impacts performance and resource usage. 


**Reduced I/O and faster queries**


Smaller data means less time to read from disk. In a columnar database, queries often scan large volumes of data, so reading compressed blocks significantly reduces I/O. This reduces stress on resources, such as disk bandwidth and network, and leads to faster query execution.


**Lower storage requirements**


Reducing how much data needs to be stored lowers storage costs. Even when using object storage like S3, where capacity is relatively cheap, compression still matters as more data can be cached locally in NVMEs for fast access.


**Better caching efficiency**


Compressed data fits more easily into memory and cache layers. This increases cache hit rates, reducing the need to fetch data from disks.


## Experiment with Nginx access logs [\#](/blog/log-compression-170x#experiment-with-nginx-access-logs)


Nginx access logs record every request handled by an Nginx server. It is a known dataset and makes it easy for anyone to relate and reproduce the experiment.


Each log typically includes information such as the client IP address, timestamp, HTTP method, status code, user agent, and response time. Below is an example of an nginx log entry.



```
185.161.113.50 - - [2019-02-04 23:40:49] "GET /filter/p62,b113?page=0 HTTP/1.1" 200 33948 "https://www.zanbil.ir/" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

```

These logs are great candidates for our experiment:


1. **Consistent structure**: They follow a fixed pattern defined by the [Nginx log format](https://docs.nginx.com/nginx/admin-guide/monitoring/logging/). While values change (timestamps, IPs, URLs, response times), the overall structure remains stable.
2. **Mix of data types**: In an nginx access log, we have IP addresses, numbers, strings, and dates. This makes for a great mix of data types to highlight how to approach each of them to store best.
3. **High volume**: Access logs accumulate quickly in production systems, often generating gigabytes or terabytes of data. This scale directly impacts compression efficiency and storage costs.



> Although nginx logs are typically stored in plain text files, their format is predictable. This might not be representative of typical application logs. We're cognizant of this, but pick this dataset to establish an optimistic upper bound. A later post will look at compression formats achievable for logs with less obvious structure.


### Get started with ClickStack [\#](/blog/log-compression-170x#test)

Spin up the world’s fastest and most scalable open source observability stack, in seconds.

[Try now](https://clickhouse.com/docs/use-cases/observability/clickstack/getting-started?loc=blog-o11y-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## Capture a baseline [\#](/blog/log-compression-170x#capture-a-baseline)


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


> The above insert command can be used to load the data into your own ClickHouse instance. Load time will depend on your local ClickHouse resources and connectivity (file is \~640MB).


Let's check how much disk space this table uses. We can do that by querying the [system.parts](https://clickhouse.com/docs/operations/system-tables/parts) table, which stores details about each table part, including its uncompressed and compressed sizes on disk.



```

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

```

No surprises here, the uncompressed size matches the one on the local disk. Internally, ClickHouse uses ZSTD(1\) compression by default \- hence the comparable compressed size.


### Turn Nginx log to a structured log (up to 56x)  [\#](/blog/log-compression-170x#turn-nginx-log-to-a-structured-log-up-to-56x)


The first step towards 170x compression is to turn the plain log we have into a structured log where each significant value (e.g., IP address, request method, URL, status code, user agent) can be stored into its own column.


Instead of storing this entire string as one column, we can parse it into individual columns like:




| Column Name | Data Type | Example Value |
| --- | --- | --- |
| remote\_addr | IPv4 | 185\.161\.113\.50 |
| remote\_user | String | user |
| time\_local | DateTime | 2025\-10\-13 10:00 |
| request\_type | String | GET |
| request\_path | String | /index.html |
| status | String | HTTP/1\.1 |
| size | UInt16 | 200 |
| referrer | String | \- |
| user\_agent | String | Mozilla/5\.0 (...) |


The defined format of Nginx logs allows for easy parsing using regular expression matching functions.


Let’s create a new table using the schema we defined for our nginx access log.



```

```
CREATE TABLE nginx_column_tuple
(
    `remote_addr` String,
    `remote_user` String,
    `time_local` DateTime,
    `request_type` String,
    `request_path` String,
    `request_protocol` String,
    `status` UInt64,
    `size` UInt64,
    `referer` String,
    `user_agent` String
)
ORDER BY ()
```

```

Now let’s ingest the log dataset into this table using the nginx\_raw table as a source and applying a regular expression to extract each value into its own column.



```

```
INSERT INTO nginx_column_tuple
SELECT
    m[1],
    m[2],
    parseDateTimeBestEffortOrNull(m[3]),
    m[4],
    m[5],
    m[6],
    toUInt64OrZero(m[7]),
    toUInt64OrZero(m[8]),
    if(length(trim(m[9])) = 0, '-', m[9]),
    m[10]
FROM (
    SELECT arrayElement(extractAllGroups(
        toValidUTF8(Body),'^(\S+) - (\S+) \[([^\]]+)\] "([A-Z]+)?\s*(.*?)\s*(HTTP\S+)?" (\d{3}) (\d+) "([^"]*)" "([^"]*)"'
    ), 1) AS m
    FROM nginx_raw
);
```

```

Let’s have another look at the size of this table.



```

```
SELECT
    `table`,
    formatReadableSize(sum(data_compressed_bytes)) AS compressed_size,
    formatReadableSize(sum(data_uncompressed_bytes)) AS uncompressed_size
FROM system.columns
WHERE `table` = 'nginx_column_tuple'
GROUP BY `table`
FORMAT VERTICAL

Row 1:
──────
table:             nginx_column_tuple
compressed_size:   359.52 MiB
uncompressed_size: 18.48 GiB
```

```


> Notice that the uncompressed size is smaller than in the previous experiment. This reduction comes from using a columnar format and from the regular expression filtering, which removed unnecessary characters.


The compressed size now is 359\.52 MB, which gives a compression ratio of 56x. Simply structuring the log to store key values in separate columns already improves the compression ratio from 35x to 56x. Although the log is no longer stored in its original format, none of the significant information has been lost. We can still reconstruct the log if needed, and we'll do that later in the blog.


## Optimize data types (up to 92x)  [\#](/blog/log-compression-170x#optimize-data-types-up-to-92x)


It's important to choose [column data types carefully](https://clickhouse.com/docs/best-practices/select-data-types) in a columnar database. The data type decides how much disk space is reserved to fit the largest possible value of that type. Even if the actual value is small, the database still uses space based on the full size of the data type. Note that if only smaller values are stored in this type, the data should compress well (lots of 0 sequences are favorable to compression). However, this still wastes considerable memory when the data is uncompressed for reading.


We already noticed that the nginx access log contains data that matches specific data types supported by ClickHouse, and already used them in our first experiment. Now we want to optimize further the types we're using. 


We can leverage the [LowCardinality](https://clickhouse.com/docs/sql-reference/data-types/lowcardinality) type, which optimizes the way data is stored on disk by applying dictionary coding to the column. The only caveat is that this method is efficient up to a certain scale. It's best to experiment with it, but the rule of thumb is that any column with a cardinality below 100,000 distinct values can benefit from this approach. 


Let's have a look at the cardinality of each column.



```

```
SELECT * APPLY uniq
FROM nginx_column_tuple
FORMAT VERTICAL

Row 1:
──────
uniq(remote_addr):      258115
uniq(remote_user):      2
uniq(time_local):       2579628 -- 2.58 million
uniq(request_type):     5
uniq(request_path):     881124
uniq(request_protocol): 3
uniq(status):           15
uniq(size):             69712
uniq(referer):          103048
uniq(user_agent):       28344
```

```

From this, we can see that the String columns `remote_user`, `request_type`, `request_protocol` and `user_agent` are good candidates for LowCardinality.


Next, we can leverage [compression codecs](https://clickhouse.com/docs/data-compression/compression-in-clickhouse#choosing-the-right-column-compression-codec) supported by ClickHouse to further optimize the compression rate.


Let's do a new experiment with LowCardinality and different compression codecs.



```

```
CREATE TABLE nginx_column_tuple_optimized_types
(
    `remote_addr` IPv4,
    `remote_user` LowCardinality(String),
    `time_local` DateTime CODEC(Delta(4), ZSTD(1)),
    `request_type` LowCardinality(String),
    `request_path` String CODEC(ZSTD(6)),
    `request_protocol` LowCardinality(String),
    `status` UInt16,
    `size` UInt32,
    `referer` String CODEC(ZSTD(6)),
    `user_agent` LowCardinality(String)
)
ORDER BY ()
```

```

Now we can simply re\-ingest the data from the table `nginx_column_tuple` as it's already stored in columns.



```

```
INSERT INTO nginx_column_tuple_optimized_types SELECT * FROM nginx_column_tuple;
```

```

Let’s look at the table size.



```

```
SELECT
    `table`,
    formatReadableSize(sum(data_compressed_bytes)) AS compressed_size,
    formatReadableSize(sum(data_uncompressed_bytes)) AS uncompressed_size
FROM system.columns
WHERE `table` = 'nginx_column_tuple_optimized_types'
GROUP BY `table`
FORMAT VERTICAL

Row 1:
──────
table:             nginx_column_tuple_optimized_types
compressed_size:   218.42 MiB
uncompressed_size: 9.69 GiB
```

```

The compressed size is down to 218 MB \- a compression ratio of 92x. This is a great achievement, but not quite the 170x we promised. We still have one lever to action, how data is ordered on disk.


## Ordering data on disk (reached 178x!) [\#](/blog/log-compression-170x#ordering-data-on-disk-reached-178x)


Most compression algorithms benefit from storing the same and similar values next to each other. ClickHouse allows the order in which columns are written for a table to be specified via its primary/ordering key. Therefore, when we're aiming to reach the best compression ratio possible, we can deliberately pick an ordering key that would benefit compression.



> Note the ordering key should also consider the user's access patterns \- filtering on keys occurring early in the key will be faster than those which appear later (or not at all). Here, we optimize for compression only. In production environments, users will typically need to balance query access patterns and optimal compression \- although higher compression typically helps to also improve query performance.


To achieve the higher compression ratio, we need to choose an ordering key that compresses all columns of the table in the most efficient way. It needs to be a balance between the total size of the column and its cardinality. A high cardinality column, even if using a lot of space, will not benefit greatly from ordering and will also penalize the compression of subsequent columns, offering less opportunity for continuous sequences in their values. As we see in the diagram below, compression is more efficient when using columns that allow for data to be clustered together.


![blog-100x-1.jpg](/uploads/blog_100x_1_bd2163accc.jpg)
To achieve the best compression possible, we need to choose an ordering key that balances between highest impact and low cardinality. First, we need to understand what columns account for the most space in our table. For this, we can query the [system.columns](https://clickhouse.com/docs/operations/system-tables/columns) table that contains table columns statistics.



```

```
INSERT INTO nginx_column_tuple_optimized_types SELECT * FROM nginx_column_tuple;
```

```

Let’s look at the table size.



```

```
SELECT
    name,
    formatReadableSize(sum(data_compressed_bytes)) AS compressed_size,
    formatReadableSize(sum(data_uncompressed_bytes)) AS uncompressed_size
FROM system.columns
WHERE `table` = 'nginx_column_tuple_optimized_types'
GROUP BY name
ORDER BY sum(data_uncompressed_bytes) DESC

    ┌─name─────────────┬─compressed_size─┬─uncompressed_size─┐
 1. │ referer          │ 13.69 MiB       │ 4.96 GiB          │
 2. │ request_path     │ 127.19 MiB      │ 3.55 GiB          │
 3. │ size             │ 39.37 MiB       │ 254.62 MiB        │
 4. │ time_local       │ 22.58 MiB       │ 254.62 MiB        │
 5. │ remote_addr      │ 10.76 MiB       │ 254.62 MiB        │
 6. │ user_agent       │ 589.91 KiB      │ 129.05 MiB        │
 7. │ status           │ 3.42 MiB        │ 127.31 MiB        │
 8. │ request_type     │ 722.43 KiB      │ 63.78 MiB         │
 9. │ request_protocol │ 62.79 KiB       │ 63.78 MiB         │
10. │ remote_user      │ 56.81 KiB       │ 63.78 MiB         │
    └──────────────────┴─────────────────┴───────────────────┘
```

```

Using this information combined with the cardinality we can identify the ordering key that offers the best compression.




| Columns | Uncompressed size | Cardinality |
| --- | --- | --- |
| referer | 4\.96 GiB | 103048 |
| request\_path | 3\.55 GiB | 881124 |
| size | 254\.62 MiB | 69712 |
| time\_local | 254\.62 MiB | 2579628 |
| remote\_addr | 254\.62 MiB | 258115 |
| user\_agent | 129\.05 MiB | 28344 |
| status | 127\.31 MiB | 15 |
| request\_type | 63\.78 MiB | 5 |
| request\_protocol | 63\.78 MiB | 3 |
| remote\_user | 63\.78 MiB | 2 |


Using this information, we identify the following columns as candidates for the ordering key: `referrer`, `remote_addr` and `user_agent`. The `request_path` is also an interesting candidate because of its size but due to its high cardinality it is unlikely that it is going to offer great compression.


One more factor to consider is value distribution. Even with medium or high cardinality, a column can be a good ordering key if a few values cover most of the data.


For `referer`, `remote_addr`, `user_agent`, and `request_path`, we take the top 20 values in each column and compute their percentage share.


The `referer` and `user_agent` columns show a more skewed distribution than the other two. We also see that after about the 12th value, the distribution flattens, so there’s no need to analyze a longer tail.
Based on this, we can select the following ordering keys: `referer`, `remote_user`, `user_agent`, `request_path`. The idea is to start with the `referer` column since it’s the largest one. Its high cardinality is offset by a skewed distribution, which helps compression. Next comes remote\_addr, a low\-cardinality column that won’t break data clusters in the following columns. Then we include `user_agent` for reasons similar to the `referer`. Finally, we order by request\_path to get additional compression benefits on that large column.


Let’s create the table and ingest the data. 



```

```
-- Create table
CREATE TABLE nginx_column_tuple_optimized_types_sort
(
    `remote_addr` IPv4,
    `remote_user` LowCardinality(String),
    `time_local` DateTime CODEC(Delta(4), ZSTD(1)),
    `request_type` LowCardinality(String),
    `request_path` String CODEC(ZSTD(6)),
    `request_protocol` LowCardinality(String),
    `status` UInt16,
    `size` UInt32,
    `referer` String CODEC(ZSTD(6)),
    `user_agent` LowCardinality(String)
)
ORDER BY (referer, user_agent, remote_user, request_path);

-- Ingest data to new table
INSERT INTO nginx_column_tuple_optimized_types_sort SELECT * FROM nginx_column_tuple;
```

```

Let’s have a look at the total size used by this table.



```

```
SELECT
    `table`,
    formatReadableSize(sum(data_compressed_bytes)) AS compressed_size,
    formatReadableSize(sum(data_uncompressed_bytes)) AS uncompressed_size
FROM system.columns
WHERE `table` = 'nginx_column_tuple_optimized_types_sort'
GROUP BY `table`
FORMAT VERTICAL

Row 1:
──────
table:             nginx_column_tuple_optimized_types_sort
compressed_size:   109.12 MiB
uncompressed_size: 9.70 GiB
```

```

This gives us a very impressive compression rate from the raw log file on disk. 20 Gb down to 109 Mb \- a **178x compression ratio**!


## Back to (sad) reality [\#](/blog/log-compression-170x#back-to-sad-reality)


This is a great achievement, but let’s be honest, it’s uncommon to filter nginx logs by `referer` or `user_agent`. Those fields can be useful during analysis but most queries filter by time e.g. “show me the access logs from the last hour”. Let’s have a quick look at the compression ratio in this more typical scenario.


Let’s create the table with time\_local as the first ordering key. To reduce the effect of high cardinality in timestamps, we can round the values to a coarser time unit (avoiding the cardinality issues) — for example, by day.



```

```
-- Create table
CREATE TABLE logs_blog.nginx_column_tuple_optimized_types_time_sort
(
    `remote_addr` IPv4,
    `remote_user` LowCardinality(String),
    `time_local` DateTime CODEC(Delta(4), ZSTD(1)),
    `request_type` LowCardinality(String),
    `request_path` String CODEC(ZSTD(6)),
    `request_protocol` LowCardinality(String),
    `status` UInt16,
    `size` UInt32,
    `referer` String CODEC(ZSTD(6)),
    `user_agent` LowCardinality(String)
)
ORDER BY (toStartOfDay(time_local), referer, user_agent, remote_user, request_path);

-- Ingest data
INSERT INTO logs_blog.nginx_column_tuple_optimized_types_time_sort SELECT * FROM logs_blog.nginx_column_tuple_optimized_types_sort;

-- Check size
SELECT
    `table`,
    formatReadableSize(sum(data_compressed_bytes)) AS compressed_size,
    formatReadableSize(sum(data_uncompressed_bytes)) AS uncompressed_size
FROM system.columns
WHERE `table` = 'nginx_column_tuple_optimized_types_time_sort'
GROUP BY `table`
FORMAT VERTICAL

Row 1:
──────
table:             nginx_column_tuple_optimized_types_time_sort
compressed_size:   380.82 MiB
uncompressed_size: 9.76 GiB
```

```

The result isn’t as strong; we reach only about 50x compression in this case. This shows how much the choice of ordering key affects overall compression efficiency.


## Quick summary  [\#](/blog/log-compression-170x#quick-summary)


Applying our ideas to compress raw logs efficiently, we achieved a 178x compression rate. Below is a table that summarizes all the experiments and their results. 




| Name | Storage | Compression | Size (in bytes) | Size (human) | Ratio |
| --- | --- | --- | --- | --- | --- |
| nginx\-66\.log | local | None | 21237294480 | 20G | 1\.00 |
| nginx\-66\.log.gz | local | GZIP | 672053616 | 641M | 31\.60 |
| nginx\_raw | Clickhouse | Uncompressed | 21673487121 | 20\.19 GiB | 0\.98 |
| nginx\_raw | Clickhouse | Compressed | 603582977 | 575\.62 MiB | 35\.19 |
| nginx\_column\_tuple | Clickhouse | Compressed | 1387994151 | 1\.29 GiB | 15\.30 |
| optimized\_types | Clickhouse | Compressed | 229027241 | 218\.42 MiB | 92\.73 |
| optimized\_types\_sort | Clickhouse | Compressed | 118984801 | 109\.12 MiB | 178\.49 |
| optimized\_types\_sort\_time | Clickhouse | Compressed | 402837184 | 380\.82 MiB | 52\.71 |


## Conclusion  [\#](/blog/log-compression-170x#conclusion)


Storing logs at very high compression ratios is challenging, but columnar databases like ClickHouse make it achievable. By converting raw logs into a structured format, storing each field using efficient data types, and ordering data to cluster similar values together, we can reach impressive levels of compression. While this layout may not always be ideal for query performance, it’s an excellent option when the goal is to retain log data in the most space\-efficient form possible.


In this post, we showed how columnar storage enables best\-in\-class log compression, improving I/O efficiency, speeding up queries, and lowering storage costs. Using Nginx access logs as an example, we achieved more than 170x compression.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
