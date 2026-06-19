# ClickHouse Release 25\.3


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 25\.3

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Mar 27, 2025 · 11 minutes read
pre div.p\-2 {
 margin\-bottom: 2rem;
}

Another month goes by, which means it’s time for another release!


ClickHouse version 25\.3 contains 18 new features 🌱 13 performance optimizations 🐣 48 bug fixes 🌦️


This release brings query support for the AWS Glue and Unity catalogs, the new query condition cache, automatic parallelization when querying S3, and new array functions!


## New Contributors [\#](/blog/clickhouse-release-25-03#new-contributors)


A special welcome to all the new contributors in 25\.3! The growth of ClickHouse's community is humbling, and we are always grateful for the contributions that have made ClickHouse so popular.


Below are the names of the new contributors:


*Andrey Nehaychik, Arnaud Briche, Cheryl Tuquib, Didier Franc, Filipp Abapolov, Ilya Kataev, Jason Wong, Jimmy Aguilar Mena, Mark Roberts, Onkar Deshpande, Shankar Iyer, Tariq Almawash, Vico.Wu, f.abapolov, flyaways, otlxm, pheepa, rienath, talmawash*


Hint: if you’re curious how we generate this list… [here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).



You can also [view the slides from the presentation](https://presentations.clickhouse.com/2025-release-25.3/).


## AWS Glue and Unity catalogs [\#](/blog/clickhouse-release-25-03#aws-glue-and-unity-catalogs)


### Contributed by Alexander Sapin [\#](/blog/clickhouse-release-25-03#contributed-by-alexander-sapin)


This release adds support for more Lakehouse catalogs \- AWS Glue and Unity.


You can query Apache Iceberg tables via AWS Glue by first creating a database engine:



```

```
1CREATE DATABASE demo_catalog 
2ENGINE = DataLakeCatalog
3SETTINGS catalog_type = 'glue', region = 'us-west-2',
4    aws_access_key_id = 'AKIA...', aws_secret_access_key = '...';
```

```

And then querying the data:



```

```
1SHOW TABLES 
2FROM demo_catalog;
3
4SELECT * 
5FROM "demo_catalog"."db.table";
```

```

There’s support for Apache Iceberg and Delta Lake tables via the Unit catalog. Again, you’ll need to create a database engine:



```

```
1CREATE DATABASE unity_demo
2ENGINE = DataLakeCatalog(
3    'https://endpoint.cloud.databricks.com/api/2.1/unity-catalog')
4SETTINGS catalog_type = 'unity',
5    warehouse = 'workspace', catalog_credential = '...'
```

```

And then you can query it like a normal table:



```

```
1SHOW TABLES 
2FROM unity_demo;
3
4SELECT * 
5FROM "unity_demo"."db.table";
```


```

## JSON data type is production\-ready [\#](/blog/clickhouse-release-25-03#json-data-type-is-production-ready)


### Contributed by Pavel Kruglov [\#](/blog/clickhouse-release-25-03#contributed-by-pavel-kruglov)


About 1\.5 years ago, we weren’t happy with our JSON implementation, so we [returned to the drawing board](https://github.com/ClickHouse/ClickHouse/issues/54864). A [year later](https://clickhouse.com/blog/clickhouse-release-24-08#json-data-type), Pavel delivered a completely reimagined implementation for storing JSON on top of columnar storage. You can read about the journey in [How we built a new powerful JSON data type for ClickHouse](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse).


The result: unmatched performance, compression, and usability—far beyond anything offered by existing JSON data stores: [The billion docs JSON Challenge: ClickHouse vs. MongoDB, Elasticsearch, and more](https://clickhouse.com/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql).


**TL;DR:** As far as we know, this is the first time columnar storage has been implemented *right* for semi\-structured data. ClickHouse’s new JSON storage is:


- More compact than compressed files on disk
- Thousands of times faster than traditional JSON stores like MongoDB and as easy to use
- The only JSON store that fully supports dynamic JSON paths *without* forcing them into a least common type


Our new [JSON type](https://clickhouse.com/docs/sql-reference/data-types/newjson) is now production\-ready and fully integrated with ClickHouse’s query acceleration features. Read more in [Accelerating ClickHouse queries on JSON data for faster Bluesky insights](https://clickhouse.com/blog/accelerating-clickhouse-json-queries-for-fast-bluesky-dashboards).


We also created [JSONBench](https://jsonbench.com/), the first fair, vendor\-neutral benchmark focused on analytics over JSON documents. Just try searching for anything comparable—there’s nothing else like it.


Finally, the core building blocks—[Variant](https://clickhouse.com/blog/clickhouse-release-24-01#variant-type) and [Dynamic](https://clickhouse.com/blog/clickhouse-release-24-05#dynamic-data-type) types—are now production\-ready as standalone features. They power our JSON implementation and pave the way for future support of semi\-structured formats like XML, YAML, and more.


We can’t wait to see what you build with it. Give it a try—and if you’re curious about what’s coming next for JSON in ClickHouse, [check out our roadmap](https://github.com/ClickHouse/ClickHouse/issues/68428).


## Query condition cache [\#](/blog/clickhouse-release-25-03#query-condition-cache)


### Contributed by ZhongYuanKai [\#](/blog/clickhouse-release-25-03#contributed-by-zhongyuankai)


This release adds the [query condition cache](https://clickhouse.com/docs/operations/query-condition-cache), which accelerates repeatedly run queries—such as in dashboarding or observability scenarios—with selective WHERE clauses that don’t benefit from the primary index. It’s especially effective when the same condition is reused across different queries.


For example, the following query counts all [Bluesky](https://bsky.social/about) posts that include the pretzel emoji:



```

```
1SELECT count()
2FROM bluesky
3WHERE (data.kind = 'commit')
4  AND (data.commit.operation = 'create')
5  AND (data.commit.collection = 'app.bsky.feed.post')
6  AND (data.commit.record.text LIKE '%🥨%');
```


```

This query returns the top languages for pretzel emoji posts:



```

```
1SELECT
2    arrayJoin(CAST(data.commit.record.langs, 'Array(String)')) AS language,
3    count() AS count
4FROM bluesky
5WHERE (data.kind = 'commit')
6  AND (data.commit.operation = 'create')
7  AND (data.commit.collection = 'app.bsky.feed.post')
8  AND (data.commit.record.text LIKE '%🥨%')
9GROUP BY language
10ORDER BY count DESC;
```


```

Both queries share the same predicate:



```

```
1WHERE (data.kind = 'commit')
2  AND (data.commit.operation = 'create')
3  AND (data.commit.collection = 'app.bsky.feed.post')
4  AND (data.commit.record.text LIKE '%🥨%')
```


```

With the query condition cache, the scan result from the first query is cached and reused by the second—resulting in a significant speedup.
You can find results for the queries above, performance metrics, and a deep dive into how the query condition cache works in our [dedicated blog post](https://clickhouse.com/blog/introducing-the-clickhouse-query-condition-cache).


## Automatic parallelization for external data [\#](/blog/clickhouse-release-25-03#automatic-parallelization-for-external-data)


### Contributed by Konstantin Bogdanov [\#](/blog/clickhouse-release-25-03#contributed-by-konstantin-bogdanov)


In the previous section, we saw how to count the number of pretzel emoji mentions when querying the BlueSky dataset loaded into a `MergeTree` table. Let’s now see how long it takes to query that data directly on S3:



```

```
1SELECT count()
2FROM s3('https://clickhouse-public-datasets.s3.amazonaws.com/bluesky/file_{0001..0100}.json.gz', 'JSONAsObject')
3WHERE (json.kind = 'commit') 
4AND (json.commit.operation = 'create') 
5AND (json.commit.collection = 'app.bsky.feed.post') 
6AND (json.commit.record.text LIKE '%🥨%')
7SETTINGS 
8  input_format_allow_errors_num = 100, 
9  input_format_allow_errors_ratio = 1;
```

```


```

```
┌─count()─┐
│      69 │
└─────────┘

1 row in set. Elapsed: 64.902 sec. Processed 100.00 million rows, 13.35 GB (1.54 million rows/s., 205.75 MB/s.)
Peak memory usage: 2.68 GiB.
```

```

Just over 1 minute! I have a ClickHouse Cloud cluster with 10 nodes, and I can spread the reading of the files across all the nodes by using the `s3Cluster` table function:



```

```
1SELECT count()
2FROM s3Cluster(default, 'https://clickhouse-public-datasets.s3.amazonaws.com/bluesky/file_{0001..0100}.json.gz', 'JSONAsObject')
3WHERE (json.kind = 'commit') 
4AND (json.commit.operation = 'create') 
5AND (json.commit.collection = 'app.bsky.feed.post') 
6AND (json.commit.record.text LIKE '%🥨%')
7SETTINGS 
8  input_format_allow_errors_num = 100, 
9  input_format_allow_errors_ratio = 1;
```

```

Let’s see how long this takes!



```

```
┌─count()─┐
│      69 │
└─────────┘

1 row in set. Elapsed: 16.689 sec. Processed 100.00 million rows, 13.38 GB (5.99 million rows/s., 801.86 MB/s.)
Peak memory usage: 2.06 GiB.
```

```


That’s cut the time down by 4x \- not quite linear, but not too bad!


`…Cluster` functions like [s3Cluster](https://clickhouse.com/docs/sql-reference/table-functions/s3Cluster), [azureBlobStorageCluster](https://clickhouse.com/docs/sql-reference/table-functions/azureBlobStorageCluster), [deltaLakeCluster](https://clickhouse.com/docs/sql-reference/table-functions/deltalakeCluster), [icebergCluster](https://clickhouse.com/docs/sql-reference/table-functions/icebergCluster), and [more](https://clickhouse.com/docs/sql-reference/table-functions) distribute work similarly to [parallel replicas](https://clickhouse.com/docs/deployment-guides/parallel-replicas)—but with a key difference: parallel replicas split work by [granule](https://clickhouse.com/docs/guides/best-practices/sparse-primary-indexes#data-is-organized-into-granules-for-parallel-data-processing) ranges, while `…Cluster` functions operate at the file level. We illustrate this below for our example query above with a diagram:


![Blog-release-25.3.001.png](/uploads/Blog_release_25_3_001_e098f3d404.png)
The initiator server—the one receiving the query—resolves the file glob pattern, connects to all other servers, and dynamically dispatches files. The other servers request files from the initiator as they finish processing, repeating until all files are handled. Each server uses N parallel streams (based on its CPU cores) to read and process different ranges within each file. All partial results are then merged and streamed back to the initiator, which assembles the final result. Due to the overhead of coordination and merging partial results, the speedup isn’t always linear.


Starting from 25\.3, you don’t need to call the `…Cluster` versions of remote data access functions to get distributed processing. Instead, ClickHouse will automatically distribute the work when called from a cluster if you have enabled parallel replicas.


If you don’t want distributed processing, you can disable it by setting the following property:



```

```
1SET parallel_replicas_for_cluster_engines = 0;
```

```

## arraySymmetricDifference [\#](/blog/clickhouse-release-25-03#arraysymmetricdifference)


### Contributed by Filipp Abapolov [\#](/blog/clickhouse-release-25-03#contributed-by-filipp-abapolov)


ClickHouse has an extensive collection of array functions that can solve various problems. One such problem is determining which elements in a pair of arrays exist in one array but not the other.


We can work this out by computing the union of the array and then removing any elements that are contained in the intersection of the arrays:



```

```
1WITH
2    [1, 2, 3] AS a,
3    [2, 3, 4] AS b
4SELECT
5    arrayUnion(a, b) AS union,
6    arrayIntersect(a, b) AS intersect,
7    arrayFilter(x -> (NOT has(intersect, x)), union) AS unionButNotIntersect;
```

```

This works fine, but we thought it’d be cool if you could do this with a single function. Enter arraySymmetricDifference:



```

```
1WITH
2    [1, 2, 3] AS a,
3    [2, 3, 4] AS b
4SELECT
5    arrayUnion(a, b) AS union,
6    arrayIntersect(a, b) AS intersect,
7    arrayFilter(x -> (NOT has(intersect, x)), union) AS unionNotIntersect,
8    arraySymmetricDifference(a, b) AS symmetricDifference;
```

```


```

```
┌─union─────┬─intersect─┬─unionNotIntersect─┬─symmetricDifference─┐
│ [3,2,1,4] │ [2,3]     │ [1,4]             │ [1,4]               │
└───────────┴───────────┴───────────────────┴─────────────────────┘
```

```

## estimateCompressionRatio [\#](/blog/clickhouse-release-25-03#estimatecompressionratio)


### Contributed by Tariq Almawash [\#](/blog/clickhouse-release-25-03#contributed-by-tariq-almawash)


Another function added in this release is `estimateCompressionRatio`, which can assess the potential impact of applying different compression algorithms to a column.



> Remember from the [data compression section of Why is ClickHouse fast?](https://clickhouse.com/docs/concepts/why-clickhouse-is-so-fast#storage-layer-data-compression) that ClickHouse compresses data at the column level.


We can see how it works by applying compression algorithms to the `CounterID` column in the `hits` table on <play.clickhouse.com>:



```

```
1SELECT round(estimateCompressionRatio('NONE')(CounterID)) AS none,
2       round(estimateCompressionRatio('LZ4')(CounterID)) AS lz4,
3       round(estimateCompressionRatio('ZSTD')(CounterID)) AS zstd,
4       round(estimateCompressionRatio('ZSTD(3)')(CounterID)) AS zstd3,
5       round(estimateCompressionRatio('GCD')(CounterID)) AS gcd,
6       round(estimateCompressionRatio('Gorilla')(CounterID)) AS gorilla,
7       round(estimateCompressionRatio('Gorilla, ZSTD')(CounterID)) AS mix
8FROM hits
9FORMAT PrettyMonoBlock;
```

```

We can see the output of the query below:



```

```
┏━━━━━━┳━━━━━┳━━━━━━┳━━━━━━━┳━━━━━┳━━━━━━━━━┳━━━━━━┓
┃ none ┃ lz4 ┃ zstd ┃ zstd3 ┃ gcd ┃ gorilla ┃  mix ┃
┡━━━━━━╇━━━━━╇━━━━━━╇━━━━━━━╇━━━━━╇━━━━━━━━━╇━━━━━━┩
│    1 │ 248 │ 4974 │  5110 │   1 │      32 │ 6682 │
└──────┴─────┴──────┴───────┴─────┴─────────┴──────┘
```

```

The specialized codecs (`GCD` and `Gorilla`) have little impact. The more generic codecs, `LZ4` and, in particular, `ZSTD,` significantly reduce the space taken. We can also adjust the level of `ZSTD`, where a higher value means more compression. The higher the compression level, the longer it takes to compress a value, increasing the time for write operations.


We can also use this function on data that hasn’t been ingested into ClickHouse. The following query returns the schema of an Amazon Reviews Parquet file stored in an S3 bucket:



```

```
1DESCRIBE  s3(
2  'https://datasets-documentation.s3.eu-west-3.amazonaws.com' ||
3  '/amazon_reviews/amazon_reviews_2015.snappy.parquet'
4)
5SETTINGS describe_compact_output=1;
```

```


```

```
┌─name──────────────┬─type─────────────┐
│ review_date       │ Nullable(UInt16) │
│ marketplace       │ Nullable(String) │
│ customer_id       │ Nullable(UInt64) │
│ review_id         │ Nullable(String) │
│ product_id        │ Nullable(String) │
│ product_parent    │ Nullable(UInt64) │
│ product_title     │ Nullable(String) │
│ product_category  │ Nullable(String) │
│ star_rating       │ Nullable(UInt8)  │
│ helpful_votes     │ Nullable(UInt32) │
│ total_votes       │ Nullable(UInt32) │
│ vine              │ Nullable(Bool)   │
│ verified_purchase │ Nullable(Bool)   │
│ review_headline   │ Nullable(String) │
│ review_body       │ Nullable(String) │
└───────────────────┴──────────────────┘
```

```

The following query computes the compression ratio of the `product_category` column:



```

```
1SELECT round(estimateCompressionRatio(‘NONE’)(product_category)) AS none,
2          round(estimateCompressionRatio(‘LZ4’)(product_category)) AS lz4,
3          round(estimateCompressionRatio(‘ZSTD’)(product_category)) AS zstd
4FROM
5 s3(
6  'https://datasets-documentation.s3.eu-west-3.amazonaws.com' ||
7  '/amazon_reviews/amazon_reviews_2015.snappy.parquet'
8);
```

```


```

```
┌─none─┬─lz4─┬─zstd─┐
│    1 │ 227 │ 1750 │
└──────┴─────┴──────┘
```

```

We can also see how well the data will be compressed if we import the data into a different column type:



```

```
1SELECT round(estimateCompressionRatio(‘NONE’)(product_category)) AS none,
2          round(estimateCompressionRatio(‘LZ4’)(product_category)) AS lz4,
3          round(estimateCompressionRatio(‘ZSTD’)(product_category)) AS zstd
4FROM
5 s3(
6  'https://datasets-documentation.s3.eu-west-3.amazonaws.com' ||
7  '/amazon_reviews/amazon_reviews_2015.snappy.parquet',
8  ‘Parquet’,
9  ‘product_category LowCardinality(String)’
10);
```

```


```

```
┌─none─┬─lz4─┬─zstd─┐
│    1 │ 226 │ 1691 │
└──────┴─────┴──────┘
```

```

Or if we change the sort order of the data:



```

```
1SELECT round(estimateCompressionRatio(‘NONE’)(product_category)) AS none,
2          round(estimateCompressionRatio(‘LZ4’)(product_category)) AS lz4,
3          round(estimateCompressionRatio(‘ZSTD’)(product_category)) AS zstd
4FROM (
5  SELECT * 
6  FROM
7   s3(
8    'https://datasets-documentation.s3.eu-west-3.amazonaws.com' ||
9    '/amazon_reviews/amazon_reviews_2015.snappy.parquet',
10    ‘Parquet’,
11    ‘product_category LowCardinality(String)’
12  )
13  ORDER BY product_category
14);
```

```


```

```
┌─none─┬─lz4─┬─zstd─┐
│    1 │ 252 │ 7097 │
└──────┴─────┴──────┘
```

```
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
