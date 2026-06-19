# ClickHouse Release 25\.4


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 25\.4

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 9, 2025 · 11 minutes readAnother month goes by, which means it’s time for another release!


ClickHouse version 25\.4 contains **25** new features 🌸 **23** performance optimizations 🦋 **58** bug fixes 🐝


This release brings lazy materialization, Apache Iceberg time travel, correlated subqueries for the `EXISTS` clause, and more!


## New Contributors [\#](/blog/clickhouse-release-25-04#new-contributors)


A special welcome to all the new contributors in 25\.4! The growth of ClickHouse's community is humbling, and we are always grateful for the contributions that have made ClickHouse so popular.


Below are the names of the new contributors:


*Amol Saini, Drew Davis, Elmi Ahmadov, Fellipe Fernandes, Grigory Korolev, Jia Xu, John Doe, Luke Gannon, Muzammil Abdul Rehman, Nikolai Ryzhov, ParvezAhamad Kazi, Pavel Shutsin, Saif Ullah, Samay Sharma, Shahbaz Aamir, Sumit, Todd Yocum, Vladimir Baikov, Wudidapaopao, Xiaozhe Yu, arf42, cjw, felipeagfranceschini, krzaq, wujianchao5, zouyunhe*


Hint: if you’re curious how we generate this list… [here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).



  

You can also [view the slides from the presentation](https://presentations.clickhouse.com/2025-release-25.4/).


## Lazy materialization [\#](/blog/clickhouse-release-25-04#lazy-materialization)


### Contributed by Xiaozhe Yu [\#](/blog/clickhouse-release-25-04#contributed-by-xiaozhe-yu)


Lazy materialization is a new query optimization in ClickHouse that defers reading column data until it’s actually needed. In Top N queries with sorting and LIMIT, this means ClickHouse can often skip loading most of the data, cutting down I/O, memory usage, and runtime by orders of magnitude.


Here’s a real\-world example: this query finds the [Amazon reviews](https://clickhouse.com/docs/getting-started/example-datasets/amazon-reviews) with the highest number of helpful votes, returning the top 3 along with their title, headline, and full text.


We first run it with lazy materialization disabled (and cold filesystem cache):



```

```
1SELECT helpful_votes, product_title, review_headline, review_body
2FROM amazon.amazon_reviews
3ORDER BY helpful_votes DESC
4LIMIT 3
5FORMAT Null
6SETTINGS query_plan_optimize_lazy_materialization = false;
```

```


```
0 rows in set. Elapsed: 219.071 sec. Processed 150.96 million rows, 71.38 GB (689.08 thousand rows/s., 325.81 MB/s.)
Peak memory usage: 1.11 GiB.

```

Then we rerun the exact same query, but this time with lazy materialization enabled (after clearing the filesystem cache again):



```

```
1SELECT helpful_votes, product_title, review_headline, review_body
2FROM amazon.amazon_reviews
3ORDER BY helpful_votes DESC
4LIMIT 3
5FORMAT Null
6SETTINGS query_plan_optimize_lazy_materialization = true;
```

```


```
0 rows in set. Elapsed: 0.139 sec. Processed 150.96 million rows, 1.81 GB (1.09 billion rows/s., 13.06 GB/s.)
Peak memory usage: 3.80 MiB.

```

Boom: a **1,576× speedup!** With 40× less I/O and 300× lower memory.


Same query. Same table. Same machine.  

All we changed? When ClickHouse reads the data.


Tom Schreiber recently wrote a blog post, [ClickHouse gets lazier (and faster): Introducing lazy materialization](https://clickhouse.com/blog/clickhouse-gets-lazier-and-faster-introducing-lazy-materialization), in which he explains this feature in detail.


## Data Lakes from MergeTree tables [\#](/blog/clickhouse-release-25-04#data-lakes-from-mergetree-tables)


### Contributed by Alexey Milovidov [\#](/blog/clickhouse-release-25-04#contributed-by-alexey-milovidov)


MergeTree tables on read\-only disks can now refresh their state and load new data parts, if they appear in the background.


This lets you run an unlimited number of readers on top of externally hosted, continuously updating datasets, which is great for data sharing and publishing.


We can create at most one writer:



```

```
1CREATE TABLE writer (...) ORDER BY ()
2SETTINGS 
3  table_disk = true,
4  disk = disk(
5      type = object_storage,
6      object_storage_type = s3,
7      endpoint = 'https://mybucket.s3.us-east-1.amazonaws.com/data/',
8      metadata_type = plain_rewritable);
```

```

And an unlimited number of readers in any locations:



```

```
1CREATE TABLE reader (...) ORDER BY ()
2SETTINGS 
3  table_disk = true, 
4  refresh_parts_interval = 1,
5  disk = disk(
6      readonly = true,
7      type = object_storage,
8      object_storage_type = s3,
9      endpoint = 'https://mybucket.s3.us-east-1.amazonaws.com/data/',
10      metadata_type = plain_rewritable);
```

```

Let's have a look at one we created earlier, so to speak.
The following table dataset contains over 40 million posts from Hacker News:



```

```
1CREATE TABLE hackernews_history UUID '66491946-56e3-4790-a112-d2dc3963e68a'
2(
3    `update_time` DateTime DEFAULT now(),
4    `id` UInt32,
5    `deleted` UInt8,
6    `type` Enum8(
7        'story' = 1, 'comment' = 2, 'poll' = 3, 'pollopt' = 4, 'job' = 5
8    ),
9    `by` LowCardinality(String),
10    `time` DateTime,
11    `text` String,
12    `dead` UInt8,
13    `parent` UInt32,
14    `poll` UInt32,
15    `kids` Array(UInt32),
16    `url` String,
17    `score` Int32,
18    `title` String,
19    `parts` Array(UInt32),
20    `descendants` Int32
21)
22ENGINE = ReplacingMergeTree(update_time)
23ORDER BY id
24SETTINGS 
25  refresh_parts_interval = 60, 
26  disk = disk(
27    readonly = true, 
28    type = 's3_plain_rewritable', 
29    endpoint = 'https://clicklake-test-2.s3.eu-central-1.amazonaws.com/', 
30    use_environment_credentials = false
31  );
```

```

We can write a query against it just like any other table:



```

```
1SELECT type, count()
2FROM hackernews_history
3GROUP BY ALL
4ORDER BY count() DESC;
```

```


```
┌─type────┬──count()─┐
│ comment │ 38549467 │
│ story   │  5777529 │
│ job     │    17677 │
│ pollopt │    15261 │
│ poll    │     2247 │
└─────────┴──────────┘

```

## CPU workload scheduler [\#](/blog/clickhouse-release-25-04#cpu-workload-scheduler)


### Contributed by Sergei Trifonov [\#](/blog/clickhouse-release-25-04#contributed-by-sergei-trifonov)


This release adds [CPU slot scheduling](https://clickhouse.com/docs/operations/workload-scheduling#cpu_scheduling) for workloads, which lets you limit the number of concurrent threads for a specific workload.


This feature makes it possible to share ClickHouse clusters between different workloads and provide weighted fair allocation and priority\-based allocation for CPU resources.
This lets you, for example, run heavy ad\-hoc queries without affecting high\-priority real time reporting.


Let's have a look at how to configure it.
We first need to define a CPU resource:



```

```
1CREATE RESOURCE cpu (MASTER THREAD, WORKER THREAD);
```

```


> Once we define a CPU resource, the setting `max_concurrent_threads` is enabled for controlling CPU allocation. Without a CPU resource declaration, ClickHouse will use the server\-level concurrency control settings (`concurrent_threads_soft_limit_num` and related settings) instead.


A quick explainer on the thread types from the docs:


- Master thread — the first thread that starts working on a query or background activity like a merge or a mutation.
- Worker thread — the additional threads that master can spawn to work on CPU\-intensive tasks.


To achieve better responsiveness, we might choose to use separate resources for master and worker threads:



```

```
1CREATE RESOURCE worker_cpu (WORKER THREAD);
2CREATE RESOURCE master_cpu (MASTER THREAD);
```

```

We can list the resources on our ClickHouse service by running the following query:



```

```
1SELECT *
2FROM system.resources
3FORMAT Vertical;
```

```

We can then create workloads that use those resources.



```

```
1CREATE WORKLOAD all;
2
3CREATE WORKLOAD admin IN all 
4SETTINGS max_concurrent_threads = 10;
5
6CREATE WORKLOAD production IN all 
7SETTINGS max_concurrent_threads = 100;
8
9CREATE WORKLOAD analytics IN production
10SETTINGS max_concurrent_threads = 60, weight = 9;
11
12CREATE WORKLOAD ingestion IN production;
```

```


> We can only have one top level workload i.e. one that doesn't include the `IN <workload>` clause.


We can list the workloads on our ClickHouse service by running the following query:



```

```
1SELECT *
2FROM system.workloads
3FORMAT Vertical;
```

```

We can then set the appropriate workload when querying:



```

```
1SET workload = 'analytics';
```

```

## Correlated subqueries for EXISTS [\#](/blog/clickhouse-release-25-04#correlated-subqueries-for-exists)


### Contributed by Dmitry Novik [\#](/blog/clickhouse-release-25-04#contributed-by-dmitry-novik)


Our next feature is a fun one \- the `EXISTS` clause now supports correlated subqueries! Let’s see how this works with help from the [UK property dataset](https://clickhouse.com/docs/getting-started/example-datasets/uk-price-paid).


Below is the schema for this dataset:



```

```
1CREATE TABLE uk.uk_price_paid
2(
3    price UInt32,
4    date Date,
5    postcode1 LowCardinality(String),
6    postcode2 LowCardinality(String),
7    type Enum8('terraced' = 1, 'semi-detached' = 2, 'detached' = 3, 'flat' = 4, 'other' = 0),
8    is_new UInt8,
9    duration Enum8('freehold' = 1, 'leasehold' = 2, 'unknown' = 0),
10    addr1 String,
11    addr2 String,
12    street LowCardinality(String),
13    locality LowCardinality(String),
14    town LowCardinality(String),
15    district LowCardinality(String),
16    county LowCardinality(String)
17)
18ENGINE = MergeTree
19ORDER BY (postcode1, postcode2, addr1, addr2);
```

```

Let’s say we want to find districts/towns with the highest average property prices in 2009 where at least five properties were sold, but with one caveat: they must have sold at least one detached property for over £1 million in 2006!


We can now work this out with the following query:



```

```
1SELECT district, town,
2       round(AVG(price), 2) AS avgPrice,
3       COUNT(*) AS totalSales
4FROM uk.uk_price_paid p1
5WHERE date BETWEEN '2009-01-01' AND '2009-12-31'
6AND EXISTS (
7  SELECT 1
8  FROM uk.uk_price_paid p2
9  WHERE p2.district = p1.district
10  AND p2.town = p1.town
11  AND p2.type = 'detached'
12  AND p2.price > 1000000
13  AND p2.date BETWEEN '2006-01-01' AND '2006-12-31'
14)
15GROUP BY ALL
16HAVING totalSales > 5
17ORDER BY avgPrice DESC
18LIMIT 10
19SETTINGS allow_experimental_correlated_subqueries = 1;
```

```


```
┌─district───────────────┬─town─────────────┬───avgPrice─┬─totalSales─┐
│ ELMBRIDGE              │ LEATHERHEAD      │  1118756.9 │         58 │
│ KENSINGTON AND CHELSEA │ LONDON           │ 1060251.76 │       1620 │
│ WOKING                 │ GUILDFORD        │     901000 │          9 │
│ CHILTERN               │ TRING            │  893333.33 │          6 │
│ ENFIELD                │ BARNET           │  891921.88 │         48 │
│ ELMBRIDGE              │ COBHAM           │   875841.6 │        202 │
│ WYCOMBE                │ HENLEY-ON-THAMES │     846300 │         10 │
│ GUILDFORD              │ GODALMING        │  831977.67 │          9 │
│ RUNNYMEDE              │ VIRGINIA WATER   │  802773.53 │         85 │
│ THREE RIVERS           │ NORTHWOOD        │  754197.22 │         36 │
└────────────────────────┴──────────────────┴────────────┴────────────┘

```

Notice that we must enable `allow_experimental_correlated_subqueries` as this is an experimental feature.


Lines 10 and 11 reference fields from the outer query (`p1`) within the subquery (`p2`). The condition `p2.district = p1.district AND p2.town = p1.town` creates a dynamic relationship between the two query levels, evaluating the subquery separately for each district/town combination.


## Persistent databases in clickhouse\-local [\#](/blog/clickhouse-release-25-04#persistent-databases-in-clickhouse-local)


### Contributed by Alexey Milovidov [\#](/blog/clickhouse-release-25-04#contributed-by-alexey-milovidov-1)


The default database is now persistent when using [clickhouse\-local](https://clickhouse.com/docs/operations/utilities/clickhouse-local).


To see the difference that this makes, let's launch clickhouse\-local in 25\.3:



```

```
1clickhouse -m --path data
```

```

We’ll create a table:



```

```
1CREATE TABLE foo (a UInt8) ORDER BY a;
```

```

If we exit the CLI by typing `exit;` and relaunch it, the following query will return no rows:



```

```
1SHOW TABLES
```

```


```
Ok.

0 rows in set. Elapsed: 0.008 sec.

```

Now let’s do the same with ClickHouse 25\.4:



```

```
1clickhouse -m --path data2
```

```

We’ll create a table:



```

```
1CREATE TABLE foo (a UInt8) ORDER BY a;
```

```

And then if we exit before relaunching, we’ll see the following:



```

```
1SHOW TABLES
```

```


```
   ┌─name─┐
1. │ foo  │
   └──────┘

1 row in set. Elapsed: 0.006 sec.

```

## Apache Iceberg time travel [\#](/blog/clickhouse-release-25-04#apache-iceberg-time-travel)


### Contributed by Brett Hoerner, Dan Ivanik [\#](/blog/clickhouse-release-25-04#contributed-by-brett-hoerner-dan-ivanik)


Over the last few releases, we’ve been adding more support to ClickHouse for open table formats like Apache Iceberg/Delta Lake and catalogs like Unity/AWS Glue, and this release is no exception.


It’s now possible to run Apache Iceberg queries based on previous snapshots, aka time travel. We’ve also recorded [a video showing how to use this functionality with the AWS Glue catalog](https://clickhouse.com/videos/iceberg-aws-glue-clickhouse).



Below is an example showing the query syntax for this functionality:



```

```
1CREATE DATABASE test
2ENGINE = DataLakeCatalog
3SETTINGS 
4  catalog_type = 'glue', 
5  region = '', 
6  aws_access_key_id = '', 
7  aws_secret_access_key = '';
```

```


```

```
1SELECT count()
2FROM test.`iceberg_benchmark.time_travel`
3SETTINGS iceberg_timestamp_ms = 1742497721135;
```

```

You can also see the [AWS Glue Catalog developer guide](https://clickhouse.com/docs/use-cases/data-lake/glue-catalog) for more examples.


## Default compression codec for tables [\#](/blog/clickhouse-release-25-04#default-compression-codec-for-tables)


### Contributed by Gvoelfin [\#](/blog/clickhouse-release-25-04#contributed-by-gvoelfin)


It’s now possible to set a default compression codec for every column in `MergeTree` tables. For example:



```

```
1CREATE TABLE t (
2    time DateTime CODEC(ZSTD(3)), -- codec on a column level
3    user_id UInt64, -- uses the default codec
4    ...
5) ORDER BY time
6SETTINGS default_compression_codec = 'ZSTD(1)' -- codec on a table level
```

```

As a reminder, ClickHouse applies `LZ4` compression in the self\-managed version and `ZSTD` in ClickHouse Cloud by default.


As well as setting the default codec at a table level, we can also set it globally for all tables via a config file:


*config.d/compression.yaml*



```

```
1compression:
2    case:
3        min_part_size: 1000000000 # Optional condition
4        method: 'zstd'
```

```

## SSH Interface [\#](/blog/clickhouse-release-25-04#ssh-interface)


### George Gamezardashvili, Nikita Mikhailov [\#](/blog/clickhouse-release-25-04#george-gamezardashvili-nikita-mikhailov)


ClickHouse 25\.3 saw the ClickHouse Server add support for the SSH protocol, which means any SSH client can connect to it directly


We've now added support for this to [play.clickhouse.com](https://play.clickhouse.com).
You can connect to that service by running the following:



```

```
1ssh play@play.clickhouse.com
```

```

There's no password, so you can just press enter when prompted for one.


There are a range of datasets to play with and below is an example of a query against a table containing stock prices:



```

```
1SELECT symbol, max(price), sum(volume)
2FROM stock
3GROUP BY ALL
4ORDER BY max(price) DESC
5LIMIT 10;
```

```


```
    ┌─symbol─┬─max(price)─┬─sum(volume)─┐
 1. │ RBAK   │    9963.24 │ 11569148200 │
 2. │ SEB    │    1670.01 │     2382900 │
 3. │ WPO    │     996.74 │    30127600 │
 4. │ NVR    │        938 │   178289600 │
 5. │ GIW    │        767 │     1306400 │
 6. │ WTM    │      702.5 │    21839600 │
 7. │ INFY   │    670.062 │   670302700 │
 8. │ QCOM   │        659 │ 28698244000 │
 9. │ MCHXP  │        585 │       58200 │
10. │ MTB    │     575.25 │   507431900 │
    └────────┴────────────┴─────────────┘

```
[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
