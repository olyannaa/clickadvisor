# ClickHouse Release 24\.3


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 24\.3

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Apr 9, 2024 · 14 minutes readIt's Spring up here in the Northern hemisphere and it's time for another ClickHouse release.



ClickHouse version 24\.3 contains **12 new features** 🎁 **18 performance optimisations** 🛷 **60 bug fixes** 🐛



## New Contributors [\#](/blog/clickhouse-release-24-03#new-contributors)


As always, we send a special welcome to all the new contributors in 24\.3! ClickHouse's popularity is, in large part, due to the efforts of the community that contributes. Seeing that community grow is always humbling.


Below are the names of the new contributors:



> *johnnymatthews, AlexeyGrezz, Aliaksei Khatskevich, Aris Tritas, Artem Alperin, Blacksmith, Blargian, Brokenice0415, Charlie, Dan Wu, Daniil Ivanik, Eyal Halpern Shalev, Fille, HowePa, Jayme Bird, Joshua Hildred, Juan Madurga, Kirill Nikiforov, Lino Uruñuela, LiuYuan, Maksim Alekseev, Marina Fathouat, Mark Needham, Mathieu Rey, MochiXu, Nataly Merezhuk, Nickolaj Jepsen, Nikita Fomichev, Nikolai Fedorovskikh, Nikolay Edigaryev, Nikolay Monkov, Nikolay Yankin, Oxide Computer Company, Pablo Musa, PapaToemmsn, Peter, Pham Anh Tuan, Roman Glinskikh, Ronald Bradford, Shanfeng Pang, Shaun Struwig, Shuai li, Shubham Ranjan, Tim Liou, Waterkin, William Schoeffel, YenchangChan, Zheng Miao, avinzhang, beetelbrox, bluikko, chenwei, conicliu, danila\-ermakov, divanik, edpyt, jktng, josh\-hildred, mikhnenko, mochi, nemonlou, qaziqarta, rogeryk, shabroo, shuai\-xu, sunny, sunny19930321, tomershafir, una, unashi, Кирилл Гарбар, 豪肥肥*


Hint: if you’re curious how we generate this list… [click here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).



You can also [view the slides from the presentation](https://presentations.clickhouse.com/release_24.3/).


## Analyzer enabled by default [\#](/blog/clickhouse-release-24-03#analyzer-enabled-by-default)


### Contributed by Maksim Kita, Nikolai Kochetov, Dmitriy Novik, Vladimir Cherkasov, Igor Nikonov, Yakov Olkhovskiy, and others [\#](/blog/clickhouse-release-24-03#contributed-by-maksim-kita-nikolai-kochetov-dmitriy-novik-vladimir-cherkasov-igor-nikonov-yakov-olkhovskiy-and-others)


Analyzer is a new query analysis and optimization infrastructure in ClickHouse that’s been worked on for the last couple of years. It provides better compatibility and feature completeness and enables complex query optimizations.


We’ve had experimental support for the analyzer for a while now, but starting from version 24\.3, this feature is beta and enabled by default.


If you don’t want to use it you can still disable it by configuring the following setting:



```
SET allow_experimental_analyzer = 0;

```

In version 24\.4 or 24\.5, we plan to promote the analyzer to production and remove the old query analysis implementation.


One thing that the old query runtime couldn’t handle very well was queries that used nested CTEs and joins. For example, the following query should return the number 1:



```
WITH example AS (
    SELECT '2021-01-01' AS date, 1 AS node, 1 AS user
)
SELECT extra_data 
FROM (
    SELECT join1.*
    FROM example
    LEFT JOIN (
        SELECT '2021-01-01' AS date, 1 AS extra_data
    ) AS join1
    ON example.date = join1.date
LEFT JOIN (
    SELECT '2021-01-01' AS date
) AS join2
ON example.date = join2.date);

```

But if we run it with the old query runtime (which we can simulate in 24\.3 by setting `allow_experimental_analyzer = 0`), we’ll get the following error instead:



```
Received exception:
Code: 47. DB::Exception: Missing columns: 'extra_data' while processing query: 'WITH example AS (SELECT '2021-01-01' AS date, 1 AS node, 1 AS user) SELECT extra_data FROM (SELECT join1.* FROM example LEFT JOIN (SELECT '2021-01-01' AS date, 1 AS extra_data) AS join1 ON example.date = join1.date LEFT JOIN (SELECT '2021-01-01' AS date) AS join2 ON example.date = join2.date) SETTINGS allow_experimental_analyzer = 0', required columns: 'extra_data' 'extra_data'. (UNKNOWN_IDENTIFIER)

```

The analyzer also supports multiple `ARRAY JOIN` clauses in the same query, which wasn’t possible before.


Imagine that we have the following JSON file that contains orders, products, and reviews.



```
[
  {
    "order_id": 1,
    "products": [
      {
        "product_id": 101,
        "name": "Laptop",
        "reviews": [
          {"review_id": 1001, "rating": 5, "comment": "Excellent product!"},
          {"review_id": 1002, "rating": 4, "comment": "Very good, but could be cheaper."}
        ]
      },
      {
        "product_id": 102,
        "name": "Smartphone",
        "reviews": [
          {"review_id": 2001, "rating": 5, "comment": "Best phone I've ever had."},
          {"review_id": 2002, "rating": 3, "comment": "Battery life could be better."}
        ]
      }
    ]
  },
  {
    "order_id": 2,
    "products": [
      {
        "product_id": 103,
        "name": "Headphones",
        "reviews": [
          {"review_id": 3001, "rating": 5, "comment": "Great sound quality!"},
          {"review_id": 3002, "rating": 2, "comment": "Stopped working after a month."}
        ]
      },
      {
        "product_id": 104,
        "name": "E-book Reader",
        "reviews": [
          {"review_id": 4001, "rating": 4, "comment": "Makes reading so convenient!"},
          {"review_id": 4002, "rating": 5, "comment": "A must-have for book lovers."}
        ]
      }
    ]
  }
]

```

We want to massage the data so that we can see the reviews line\-by\-line alongside product information. We can do this with the following query:



```
SELECT
    review.rating AS rating,
    review.comment,
    product.product_id AS id,
    product.name AS name
FROM `products.json`
ARRAY JOIN products AS product
ARRAY JOIN product.reviews AS review
ORDER BY rating DESC

```


```
   ┌─rating─┬─review.comment───────────────────┬──id─┬─name──────────┐
1. │      5 │ Excellent product!               │ 101 │ Laptop        │
2. │      5 │ Best phone I've ever had.        │ 102 │ Smartphone    │
3. │      5 │ Great sound quality!             │ 103 │ Headphones    │
4. │      5 │ A must-have for book lovers.     │ 104 │ E-book Reader │
5. │      4 │ Very good, but could be cheaper. │ 101 │ Laptop        │
6. │      4 │ Makes reading so convenient!     │ 104 │ E-book Reader │
7. │      3 │ Battery life could be better.    │ 102 │ Smartphone    │
8. │      2 │ Stopped working after a month.   │ 103 │ Headphones    │
   └────────┴──────────────────────────────────┴─────┴───────────────┘

```

We can now treat tuple elements like columns, which means we can pass in all the elements from the `review` tuple and format the output:



```
SELECT format('{}: {} [{}]', review.*) AS r
FROM `products.json`
ARRAY JOIN products AS product
ARRAY JOIN product.reviews AS review;

```


```
   ┌─r──────────────────────────────────────────┐
1. │ Excellent product!: 5 [1001]               │
2. │ Very good, but could be cheaper.: 4 [1002] │
3. │ Best phone I've ever had.: 5 [2001]        │
4. │ Battery life could be better.: 3 [2002]    │
5. │ Great sound quality!: 5 [3001]             │
6. │ Stopped working after a month.: 2 [3002]   │
7. │ Makes reading so convenient!: 4 [4001]     │
8. │ A must-have for book lovers.: 5 [4002]     │
   └────────────────────────────────────────────┘

```

We can also create aliases for lambda functions:



```
WITH x -> round(x * 1.2, 2) AS addTax
SELECT
    round(randUniform(8, 20), 2) AS amount,
    addTax(amount)
FROM numbers(5)

```


```
   ┌─amount─┬─addTax(amount)─┐
1. │  15.76 │          18.91 │
2. │  19.27 │          23.12 │
3. │   8.45 │          10.14 │
4. │   9.46 │          11.35 │
5. │  13.02 │          15.62 │
   └────────┴────────────────┘

```

There are also a bunch of other improvements, which you can read about in the [presentation slides](https://presentations.clickhouse.com/release_24.3/).


## ATTACH PARTITION from a remote disk [\#](/blog/clickhouse-release-24-03#attach-partition-from-a-remote-disk)


### Contributed by Unalian [\#](/blog/clickhouse-release-24-03#contributed-by-unalian)


[Attaching a table from another disk](https://clickhouse.com/docs/en/sql-reference/statements/attach#attach-existing-database) is a feature that’s existed in ClickHouse for a while, but let’s quickly recap how it works before looking at our next feature.


The [ClickHouse/web\-tables\-demo](https://github.com/ClickHouse/web-tables-demo/tree/main) repository contains the database files for the UK housing price dataset. We can attach that table by running the following command:



```
ATTACH TABLE uk_price_paid_web UUID 'cf712b4f-2ca8-435c-ac23-c4393efe52f7'
(
    price UInt32,
    date Date,
    postcode1 LowCardinality(String),
    postcode2 LowCardinality(String),
    type Enum8('other' = 0, 'terraced' = 1, 'semi-detached' = 2, 'detached' = 3, 'flat' = 4),
    is_new UInt8,
    duration Enum8('unknown' = 0, 'freehold' = 1, 'leasehold' = 2),
    addr1 String,
    addr2 String,
    street LowCardinality(String),
    locality LowCardinality(String),
    town LowCardinality(String),
    district LowCardinality(String),
    county LowCardinality(String)
)
ENGINE = MergeTree
ORDER BY (postcode1, postcode2, addr1, addr2)
SETTINGS disk = disk(type = web, endpoint = 'https://raw.githubusercontent.com/ClickHouse/web-tables-demo/main/web/');

```

The UUID needs to stay as it is or it won’t attach properly. You won’t see an error when you run the `ATTACH TABLE` command, but resulting queries won’t return any results;


We can then run the following query to find the average house prices grouped by year for the 10 most recent years:



```
SELECT
    toYear(date) AS year,
    round(avg(price)) AS price,
    bar(price, 0, 1000000, 80)
FROM uk_price_paid_web
GROUP BY year
ORDER BY year ASC;

```


```
    ┌─year─┬──price─┬─bar(price, 0, 1000000, 80)──────┐
 1. │ 2022 │ 387415 │ ██████████████████████████████▉ │
 2. │ 2021 │ 382166 │ ██████████████████████████████▌ │
 3. │ 2020 │ 376855 │ ██████████████████████████████▏ │
 4. │ 2019 │ 352562 │ ████████████████████████████▏   │
 5. │ 2018 │ 350913 │ ████████████████████████████    │
 6. │ 2017 │ 346486 │ ███████████████████████████▋    │
 7. │ 2016 │ 313543 │ █████████████████████████       │
 8. │ 2015 │ 297282 │ ███████████████████████▊        │
 9. │ 2014 │ 280029 │ ██████████████████████▍         │
10. │ 2013 │ 256928 │ ████████████████████▌           │
    └──────┴────────┴─────────────────────────────────┘

10 rows in set. Elapsed: 3.249 sec. Processed 27.40 million rows, 164.42 MB (8.43 million rows/s., 50.60 MB/s.)
Peak memory usage: 209.20 MiB.

```

The amount of time that this query takes is a function of the internet bandwidth speed of the machine on which you run it \- the data isn’t stored locally so the data needs to be pulled down before the query can be run against it.


The `ATTACH PARTITION` command has been updated in 24\.3 to let you attach data from a different/remote disk, which makes it easy to copy the database from GitHub onto our machine. Let’s first create another table with the same schema:



```
CREATE TABLE uk_price_paid_local
(
    price UInt32,
    date Date,
    postcode1 LowCardinality(String),
    postcode2 LowCardinality(String),
    type Enum8('other' = 0, 'terraced' = 1, 'semi-detached' = 2, 'detached' = 3, 'flat' = 4),
    is_new UInt8,
    duration Enum8('unknown' = 0, 'freehold' = 1, 'leasehold' = 2),
    addr1 String,
    addr2 String,
    street LowCardinality(String),
    locality LowCardinality(String),
    town LowCardinality(String),
    district LowCardinality(String),
    county LowCardinality(String)
)
ENGINE = MergeTree
ORDER BY (postcode1, postcode2, addr1, addr2);

```

And we can then attach the data from `uk_price_paid_web` into `uk_price_paid_local`:



```
ALTER TABLE uk_price_paid_local 
ATTACH PARTITION () FROM uk_price_paid_web;

0 rows in set. Elapsed: 4.669 sec.

```

This command copies the database files from the GitHub repository onto our machine. This is significantly quicker than doing an `INSERT INTO...SELECT AS` query which would need to deserialize the data from GitHub into in\-memory data structures before serializing it back into database files on our machine.


Let’s now run the query to find the average sale price against the local table:



```
SELECT
    toYear(date) AS year,
    round(avg(price)) AS price,
    bar(price, 0, 1000000, 80)
FROM uk_price_paid_local
GROUP BY year
ORDER BY year DESC
LIMIT 10;

```


```
    ┌─year─┬──price─┬─bar(price, 0, 1000000, 80)──────┐
 1. │ 2022 │ 387415 │ ██████████████████████████████▉ │
 2. │ 2021 │ 382166 │ ██████████████████████████████▌ │
 3. │ 2020 │ 376855 │ ██████████████████████████████▏ │
 4. │ 2019 │ 352562 │ ████████████████████████████▏   │
 5. │ 2018 │ 350913 │ ████████████████████████████    │
 6. │ 2017 │ 346486 │ ███████████████████████████▋    │
 7. │ 2016 │ 313543 │ █████████████████████████       │
 8. │ 2015 │ 297282 │ ███████████████████████▊        │
 9. │ 2014 │ 280029 │ ██████████████████████▍         │
10. │ 2013 │ 256928 │ ████████████████████▌           │
    └──────┴────────┴─────────────────────────────────┘

10 rows in set. Elapsed: 0.045 sec.

```

Much faster!


## S3 Express One Zone Support [\#](/blog/clickhouse-release-24-03#s3-express-one-zone-support)


### Contributed by Nikita Taranov [\#](/blog/clickhouse-release-24-03#contributed-by-nikita-taranov)


In November 2023, Amazon announced support for the [S3 Express One Zone Storage Class](https://aws.amazon.com/s3/storage-classes/express-one-zone/) which aims to provide lower latency and higher reads per second but at [a much higher (7x) cost](https://aws.amazon.com/s3/pricing/) with [less availability](https://aws.amazon.com/s3/faqs/).


Support for this new storage class required an update to the AWS/S3 library and as of version 24\.3, ClickHouse supports reading from and writing to these buckets. You can learn more in the [S3 Express documentation](https://clickhouse.com/docs/en/integrations/s3#s3express).


Let’s have a look at how we’d go about querying data in an S3 Express bucket and the potential performance benefits.


We recently participated in the [1 trillion row challenge](https://clickhouse.com/blog/clickhouse-1-trillion-row-challenge) where we had to query 1 trillion rows of data spread across 100,000 Parquet files in an S3 bucket. We copied all those files into an S3 Express bucket.


Next, we created an EC2 instance in the same region and with the same availability zone as the S3 Express bucket (important since express is AZ specific). We’re using the [c7gn.16xlarge](https://instances.vantage.sh/aws/ec2/c7gn.16xlarge) instance type, which has a network bandwidth of 125 Gigabytes per second \- that should be more than enough for our needs.


We then downloaded and installed ClickHouse and added an entry for our S3 express bucket to the configuration file:



```
<s3>
    <perf-bucket-url>
        <endpoint>https://super-fast-clickhouse--use1-az4--x-s3.s3express-use1-az4.us-east-1.amazonaws.com</endpoint>
        <region>us-east-1</region>
    </perf-bucket-url>
</s3>

```

The `region` property is used when querying the bucket and if you don’t specify this config, you’ll get the following error:



```
Region should be explicitly specified for directory buckets

```

Now that we’ve got that setup, it’s time to have a look at the queries. First, we’re going to count the number of records across all the files. Since we’re querying Parquet files, we’ll be able to compute the result from Parquet metadata in each file and therefore won’t need to download every file.


Let’s run it on the normal S3 bucket:



```
SELECT count()
FROM s3('https://clickhouse-1trc.s3.amazonaws.com/1trc/measurements-*.parquet', '<key>', '<secret>') SETTINGS schema_inference_use_cache_for_s3=0;


1 row in set. Elapsed: 219.933 sec. Processed 1.00 trillion rows, 11.30 MB (4.55 billion rows/s., 51.36 KB/s.)

```

And now for S3 express. The S3 express API doesn’t support glob expressions in file paths, so we’ll instead return all the files in the bucket. This also returns the root directory, which we’ll remove by writing a `WHERE` clause (an issue we need to address).



```
SELECT count()
FROM s3('https://super-fast-clickhouse--use1-az4--x-s3.s3express-use1-az4.us-east-1.amazonaws.com/1trc/*', '<key>', '<secret>', 'Parquet')
WHERE _file LIKE '%.parquet'
SETTINGS schema_inference_use_cache_for_s3 = 0

   ┌───────count()─┐
1. │ 1000000000000 │ -- 1.00 trillion
   └───────────────┘


1 row in set. Elapsed: 29.544 sec. Processed 1.00 trillion rows, 0.00 B (33.85 billion rows/s., 0.00 B/s.)
Peak memory usage: 99.29 GiB.

```

We ran these queries a few times and got similar results. For this query, we’re seeing an almost 7 times improvement in query performance.


The cost of storing data in S3 Express is $0\.16 per GB, compared to $0\.023 per GB in a normal bucket. So that 7x improvement performance comes with a 7x increase in storage costs.


Let’s see how we get on if we run the actual query from the 1 trillion row challenge, which computes the minimum, maximum, and average measurements grouped by station. This query requires us to download all 100,000 files, which ClickHouse will do in parallel. Latency matters less for this query, so we shouldn’t get as much of a performance improvement as we did with the count query.


Starting with the normal bucket:



```
SELECT
    station,
    min(measure),
    max(measure),
    round(avg(measure), 2)
FROM s3('https://clickhouse-1trc.s3.amazonaws.com/1trc/measurements-*.parquet', '', '')
GROUP BY station
ORDER BY station ASC
FORMAT `Null`

0 rows in set. Elapsed: 3087.855 sec. Processed 1.00 trillion rows, 2.51 TB (323.85 million rows/s., 813.71 MB/s.)
Peak memory usage: 98.87 GiB.

```

That’s just over 51 minutes. And how about with S3 Express?



```
SELECT
    station,
    min(measure),
    max(measure),
    round(avg(measure), 2)
FROM s3('https://super-fast-clickhouse--use1-az4--x-s3.s3express-use1-az4.us-east-1.amazonaws.com/1trc/*', '', '', 'Parquet')
WHERE _file LIKE '%.parquet'
GROUP BY station
ORDER BY station ASC
FORMAT `Null`
SETTINGS schema_inference_use_cache_for_s3 = 0

0 rows in set. Elapsed: 1227.979 sec. Processed 1.00 trillion rows, 2.51 TB (814.35 million rows/s., 2.05 GB/s.)
Peak memory usage: 98.90 GiB.

```

That’s just over 20 minutes, so the improvement this time is around 2\.5x.


In summary, S3 Express offers a significant reduction in query latency for an equivalent increase in price. This tends to matter in cases where there are many small files and latency dominates the query time. In cases where larger files must be downloaded and there is sufficient parallelism in the query, the benefits of the Express tier are likely to be less appreciable.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
