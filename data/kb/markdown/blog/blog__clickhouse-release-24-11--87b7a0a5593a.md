# ClickHouse Release 24\.11


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 24\.11

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Dec 6, 2024 · 8 minutes readAnother month goes by, which means it’s time for another release!


ClickHouse version 24\.11 contains 9 new features 🦃 15 performance optimizations ⛸️ 68 bug fixes 🏕️


In this release, parallel hash join becomes the default join strategy, `WITH FILL` gets a `STALENESS` modifier, you can pre\-warm the marks cache, and vector search gets faster with the `BFloat16` data type.


## New Contributors [\#](/blog/clickhouse-release-24-11#new-contributors)


As always, we send a special welcome to all the new contributors in 24\.11! ClickHouse's popularity is, in large part, due to the efforts of the community that contributes. Seeing that community grow is always humbling.


Below are the names of the new contributors:


*0xMihalich, Max Vostrikov, Payam Qorbanpour, Plasmaion, Roman Antonov, Romeo58rus, Zoe Steinkamp, kellytoole, ortyomka, qhsong, udiz, yun, Örjan Fors, Андрей*


Hint: if you’re curious how we generate this list… [here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).



You can also [view the slides from the presentation](https://presentations.clickhouse.com/release_24.11/).


## Parallel hash join is the default join strategy [\#](/blog/clickhouse-release-24-11#parallel-hash-join-is-the-default-join-strategy)


## Contributed by Nikita Taranov [\#](/blog/clickhouse-release-24-11#contributed-by-nikita-taranov)


The parallel hash join algorithm is now the default join strategy, replacing hash join.


The parallel hash join algorithm is a variation of a hash join that splits the input data to build several hash tables concurrently in order to speed up the join at the expense of higher memory overhead. You can see a diagram of the algorithm's query pipeline below:


![Parallel Hash Join.png](/uploads/Parallel_Hash_Join_4b3e255dda.png)
You can learn more about parallel hash join in the [ClickHouse Joins Under the Hood \- Hash Join, Parallel Hash Join, Grace Hash Join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2) blog post.


As well as becoming the default, a performance optimization was done to the algorithm where blocks scattered between threads for parallel processing now [use zero\-copy](https://github.com/ClickHouse/ClickHouse/pull/67782/files) instead of copying block columns each time.


## STALENESS Modifier For ORDER BY WITH FILL [\#](/blog/clickhouse-release-24-11#staleness-modifier-for-order-by-with-fill)


## Contributed by Mikhail Artemenko [\#](/blog/clickhouse-release-24-11#contributed-by-mikhail-artemenko)


This release introduces the `STALENESS` clause to `WITH FILL`. Let’s look at how to use it with help from the [MidJourney dataset](https://huggingface.co/datasets/vivym/midjourney-messages). Assuming we’ve downloaded the Parquet files, we can populate a table using the following queries:



```

```
1CREATE TABLE images (
2    id String,
3    timestamp DateTime64,
4    height Int64,
5    width Int64,
6    size Int64
7
8)
9ENGINE = MergeTree
10ORDER BY (size, height, width);
11
12
13INSERT INTO images WITH data AS (
14  SELECT
15    assumeNotNull(timestamp) AS ts,
16    assumeNotNull(id) AS id,
17    assumeNotNull(height) AS height,
18    assumeNotNull(width) AS width,
19    assumeNotNull(size) AS size,
20    parseDateTime64BestEffort(ts) AS ts2
21  FROM file('data/0000{00..55}.parquet')
22)
23SELECT id, ts2 AS timestamp,  height, width, size
24FROM data;
```


```

Let’s say we want to count the number of images generated during one second on the 24th of March 2023\. We’ll define start and end dates using parameters:



```
  
```
1SET param_start = '2023-03-24 00:24:02', 
2    param_end = '2023-03-24 00:24:03';
```


```

We can then write this query to compute the count per 100 milliseconds using the `WITH FILL` clause to populate empty buckets with a zero value:



```

```
1SELECT
2    toStartOfInterval(timestamp, toIntervalMillisecond(100)) AS bucket,
3    count() AS count, 'original' as original
4FROM MidJourney.images
5WHERE (timestamp >= {start: String}) AND (timestamp <= {end: String})
6GROUP BY ALL
7ORDER BY bucket ASC
8WITH FILL
9FROM toDateTime64({start:String}, 3)
10TO toDateTime64({end:String}, 3) STEP toIntervalMillisecond(100);
```


```


```
┌──────────────────bucket─┬─count─┬─original─┐
│ 2023-03-24 00:24:02.000 │     0 │          │
│ 2023-03-24 00:24:02.100 │     0 │          │
│ 2023-03-24 00:24:02.200 │     0 │          │
│ 2023-03-24 00:24:02.300 │     3 │ original │
│ 2023-03-24 00:24:02.400 │     0 │          │
│ 2023-03-24 00:24:02.500 │     0 │          │
│ 2023-03-24 00:24:02.600 │     1 │ original │
│ 2023-03-24 00:24:02.700 │     1 │ original │
│ 2023-03-24 00:24:02.800 │     2 │ original │
│ 2023-03-24 00:24:02.900 │     0 │          │
└─────────────────────────┴───────┴──────────┘


```

This release introduces the `STALENESS` clause. From the documentation:



> When `STALENESS const_numeric_expr` is defined, the query will generate rows until the difference from the previous row in the original data exceeds `const_numeric_expr`.


You can’t use `STALENESS` at the same time as the `WITH FILL...FROM` clause, so we’ll need to remove that, which leaves us with this query:



```

```
1SELECT
2    toStartOfInterval(timestamp, toIntervalMillisecond(100)) AS bucket,
3    count() AS count, 'original' as original
4FROM MidJourney.images
5WHERE (timestamp >= {start: String}) AND (timestamp <= {end: String})
6GROUP BY ALL
7ORDER BY bucket ASC
8WITH FILL
9TO toDateTime64({end:String}, 3) STEP toIntervalMillisecond(100);
```


```

Removing the `WITH FILL...FROM` clause means that our result set will start from the first actual value rather than pre\-filling with `0`s back to the specified timestamp.



```
┌──────────────────bucket─┬─count─┬─original─┐
│ 2023-03-24 00:24:02.300 │     3 │ original │
│ 2023-03-24 00:24:02.400 │     0 │          │
│ 2023-03-24 00:24:02.500 │     0 │          │
│ 2023-03-24 00:24:02.600 │     1 │ original │
│ 2023-03-24 00:24:02.700 │     1 │ original │
│ 2023-03-24 00:24:02.800 │     2 │ original │
│ 2023-03-24 00:24:02.900 │     0 │          │
└─────────────────────────┴───────┴──────────┘

```

If we now add a `STALENESS` value of 200 milliseconds, it will only fill in empty rows until the difference from the previous row exceeds 200 milliseconds:



```

```
1SELECT
2    toStartOfInterval(timestamp, toIntervalMillisecond(100)) AS bucket,
3    count() AS count, 'original' as original
4FROM MidJourney.images
5WHERE (timestamp >= {start: String}) AND (timestamp <= {end: String})
6GROUP BY ALL
7ORDER BY bucket ASC
8WITH FILL
9TO toDateTime64({end:String}, 3) STEP toIntervalMillisecond(100)
10STALENESS toIntervalMillisecond(200);
```


```


```
┌──────────────────bucket─┬─count─┬─original─┐
│ 2023-03-24 00:24:02.300 │     3 │ original │
│ 2023-03-24 00:24:02.400 │     0 │          │
│ 2023-03-24 00:24:02.600 │     1 │ original │
│ 2023-03-24 00:24:02.700 │     1 │ original │
│ 2023-03-24 00:24:02.800 │     2 │ original │
│ 2023-03-24 00:24:02.900 │     0 │          │
└─────────────────────────┴───────┴──────────┘

```

We lose the following row from the result set:



```
│ 2023-03-24 00:24:02.500 │     0 │          │

```

## Exceptions in the HTTP interface [\#](/blog/clickhouse-release-24-11#exceptions-in-the-http-interface)


## Contributed by Sema Checherinda [\#](/blog/clickhouse-release-24-11#contributed-by-sema-checherinda)


The HTTP interface can now reliably detect errors even after the result has been streamed to the client. In previous versions if we ran the following query against the ClickHouse Server:



```

```
1curl http://localhost:8123/?output_format_parallel_formatting=0 -d "SELECT throwIf(number > 100000) FROM system.numbers FORMAT Values"
```


```

We’d see a stream of values followed by this error message appended at the end:



```
Code: 395. DB::Exception: Value passed to 'throwIf' function is non-zero: while executing 'FUNCTION throwIf(greater(number, 100000) :: 2) -> throwIf(greater(number, 100000)) UInt8 : 1'. (FUNCTION_THROW_IF_VALUE_IS_NON_ZERO) (version 24.3.1.465 (official build))

```

The exit code is 0, which suggests the query has run successfully. From 24\.11, we’ll instead see the following output:



```
Code: 395. DB::Exception: Value passed to 'throwIf' function is non-zero: while executing 'FUNCTION throwIf(greater(__table1.number, 100000_UInt32) :: 0) -> throwIf(greater(__table1.number, 100000_UInt32)) UInt8 : 1'. (FUNCTION_THROW_IF_VALUE_IS_NON_ZERO) (version 24.11.1.2557 (official build))
curl: (18) transfer closed with outstanding read data remaining

```

And we have a non\-zero code of 18\.


## Prewarming the Mark cache [\#](/blog/clickhouse-release-24-11#prewarming-the-mark-cache)


## Contributed by Anton Popov [\#](/blog/clickhouse-release-24-11#contributed-by-anton-popov)


Marks map primary keys to offsets in every column's file, forming part of a table’s index. There is one mark file per table column. They can take considerable memory and are selectively loaded into the mark cache.


From 24\.11, you can pre\-warm this cache using the `mark_cache_prewarm_ratio` setting, which is set to 95% by default.


The server eagerly brings marks to the cache in memory on every insert, merge, or fetch of data parts until it is almost full.


A new system command, `SYSTEM PREWARM MARK CACHE t,` will immediately load all marks into the cache.


## BFloat16 data type [\#](/blog/clickhouse-release-24-11#bfloat16-data-type)


## Contributed by Alexey Milovidov [\#](/blog/clickhouse-release-24-11#contributed-by-alexey-milovidov)


The [Bfloat16 data type](https://en.wikipedia.org/wiki/Bfloat16_floating-point_format) was developed at Google Brain to represent vector embeddings. As the name suggests, it consists of 16 bits—a sign bit, an 8\-bit exponent, and then 7 bits for the mantissa/fraction.


![2024-12-05_13-19-27.png](/uploads/2024_12_05_13_19_27_8032f8f0bb.png)
It has the same exponent range as Float32 (single precision float), with fewer bits for the mantissa (7 bits instead of 23\).


This data type is now available in ClickHouse and will help with AI and vector searches. You’ll need to configure the following setting to use the new type:



```
SET allow_experimental_bfloat16_type=1;

```

We ran the nearest neighbor search with a full scan over 28 million 384\-dimensional vectors on a single machine, AWS c7a.metal\-48xl, and saw the following results:



```
clickhouse-benchmark --query "WITH
[-0.02925783360957671,-0.03488947771094666,...,0.032484047621093616]::Array(BFloat16)
AS center SELECT d FROM (SELECT cosineDistance(vector, center) AS d
    FROM hackernews_llama_memory ORDER BY d LIMIT 10
) SETTINGS allow_experimental_bfloat16_type = 1"

```


```
BFloat16: 0.061 sec, 301 GB/sec.
Float32: 0.146 sec, 276 GB/sec.

```
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
