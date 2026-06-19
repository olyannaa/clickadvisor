# Getting Data Into ClickHouse \- Part 1


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Getting Data Into ClickHouse \- Part 1

![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Dale McDiarmid](/authors/dale-mcdiarmid)Aug 26, 2022 · 14 minutes readThis blog post is part of a series:


- [Getting Data Into ClickHouse \- Part 2 \- A JSON detour](https://clickhouse.com/blog/getting-data-into-clickhouse-part-2-json)
- [Getting Data Into ClickHouse \- Part 3 \- Using S3](https://clickhouse.com/blog/getting-data-into-clickhouse-part-3-s3)


## Getting Data Into ClickHouse [\#](/blog/getting-data-into-clickhouse-part-1#getting-data-into-clickhouse)


A common question from ClickHouse users who are just getting started is how to load data into ClickHouse efficiently. In this blog series, we will demonstrate several options to achieve this task: from the clickhouse\-client to officially supported client libraries. In this specific post, we start simple by relying on schema inference and assuming our dataset is sufficiently structured, perfectly clean (almost), and ready for immediate insertion. Later posts will introduce advanced techniques for data cleansing and schema optimization.


As both ClickHouse users and data lovers, we’re always looking for interesting datasets of sufficient size to challenge ClickHouse: we even track potential opportunities for fun with a specific [GitHub label](https://github.com/ClickHouse/ClickHouse/issues?q=is%3Aopen+is%3Aissue+label%3Adataset) on the main repository. This post originates from [an issue](https://github.com/ClickHouse/ClickHouse/issues/29693) to explore [Hacker News data](https://github.com/HackerNews/API). To keep things simple, we distribute a clean version of this dataset in several formats. Users should be able to reproduce all examples.


All examples use a ClickHouse Cloud instance with the client hosted on a [c5ad.4xlarge](https://aws.amazon.com/ec2/instance-types/c5/) with 16 cores and 32GB of RAM. All commands will also be compatible with self managed ClickHouse clusters. High end machines speed up the process, but you can run these steps on the average laptop.


### Download [\#](/blog/getting-data-into-clickhouse-part-1#download)


A CSV version of the dataset can be downloaded from [here](https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.csv.gz), or by running this command:



```
wget https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.csv.gz

```

At 4\.6GB, and 28m rows, this compressed file should take 5\-10 minutes to download.


### Sampling [\#](/blog/getting-data-into-clickhouse-part-1#sampling)


[clickhouse\-local](https://clickhouse.com/docs/en/operations/utilities/clickhouse-local/) allows users to perform fast processing on local files without having to deploy and configure the ClickHouse server.


Before storing any data in ClickHouse, let's sample the file using clickhouse\-local. From the clickhouse\-local console:



```
clickhouse-local

```


```
SELECT *
FROM file('hacknernews.csv.gz', CSVWithNames)
LIMIT 2
SETTINGS input_format_try_infer_datetimes = 0
FORMAT Vertical


Row 1:
──────
id:          344065
deleted:     0
type:        comment
by:          callmeed
time:        2008-10-26 05:06:58
text:        What kind of reports do you need?<p>ActiveMerchant just connects your app to a gateway for cc approval and processing.<p>Braintree has very nice reports on transactions and it's very easy to refund a payment.<p>Beyond that, you are dealing with Rails after all–it's pretty easy to scaffold out some reports from your subscriber base.
dead:        0
parent:      344038
poll:        0
kids:        []
url:
score:       0
title:
parts:       []
descendants: 0

Row 2:
──────
id:          344066
deleted:     0
type:        story
by:          acangiano
time:        2008-10-26 05:07:59
text:
dead:        0
parent:      0
poll:        0
kids:        [344111,344202,344329,344606]
url:         http://antoniocangiano.com/2008/10/26/what-arc-should-learn-from-ruby/
score:       33
title:       What Arc should learn from Ruby
parts:       []
descendants: 10

```

There are a lot of subtle capabilities in this command. The [file](https://clickhouse.com/docs/en/sql-reference/functions/files/#file) operator allows us to read the file from a local disk, specifying only the format “CSVWithNames”. Most importantly, the schema is automatically inferred for us from the file contents. Note also how clickhouse\-local is able to read the compressed file, inferring the gzip format from the extension. We format Verticially for the purposes of rendering.


As well as inferring the structure, schema inference determines a type for each column.


An astute reader may have noticed that we used the setting `input_format_try_infer_datetimes=0`. This setting disables date parsing during schema inference as, at the time of writing (22\.8\), the datetimes in this specific CSV file cannot be parsed automatically. This has been addressed in later versions.


### Loading the Data [\#](/blog/getting-data-into-clickhouse-part-1#loading-the-data)


Our simplest and most powerful tool for data loading is the [clickhouse\-client](https://clickhouse.com/docs/en/interfaces/cli/#clickhouse-client): a feature\-rich native command\-line client. To load data, we can again exploit schema inference, relying on ClickHouse to determine the types of the columns.


In the following command, we create a table and insert the data directly from the remote CSV file, accessing the contents via the [url](https://clickhouse.com/docs/en/sql-reference/table-functions/url) function. The schema is inferred, and the data is effortlessly inserted to the table. Execute the following from the clickhouse\-client console.



```
CREATE TABLE hackernews ENGINE = MergeTree ORDER BY tuple
(
) EMPTY AS SELECT * FROM url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.csv.gz', 'CSVWithNames');

```

This creates an empty table using the schema inferred from the data. The DESCRIBE command allows us to understand these assigned types.



```
DESCRIBE TABLE hackernews
┌─name────────┬─type─────────────────────┬
│ id          │ Nullable(Float64)        │
│ deleted     │ Nullable(Float64)        │
│ type        │ Nullable(String)         │
│ by          │ Nullable(String)         │
│ time        │ Nullable(String)         │
│ text        │ Nullable(String)         │
│ dead        │ Nullable(Float64)        │
│ parent      │ Nullable(Float64)        │
│ poll        │ Nullable(Float64)        │
│ kids        │ Array(Nullable(Float64)) │
│ url         │ Nullable(String)         │
│ score       │ Nullable(Float64)        │
│ title       │ Nullable(String)         │
│ parts       │ Array(Nullable(Float64)) │
│ descendants │ Nullable(Float64)        │
└─────────────┴──────────────────────────┴

```

For insertion we can utilize an [INSERT INTO, SELECT](https://clickhouse.com/docs/en/sql-reference/statements/insert-into/#inserting-the-results-of-select), streaming the data directly from the url.



```
INSERT INTO hackernews SELECT *
FROM url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.csv.gz', 'CSVWithNames')

0 rows in set. Elapsed: 203.682 sec. Processed 28.74 million rows, 15.15 GB (141.09 thousand rows/s., 74.40 MB/s.)

```

The table schema here is far from optimal, and the insertion speed could be improved significantly with some simple settings. We leave this task for later blog posts. We have, however, successfully inserted 28m rows into ClickHouse with a single command!


Let's sample the Hacker News stories and specific columns.



```
SELECT
    id,
    title,
    type,
    by,
    time,
    url,
    score
FROM hackernews
WHERE type = 'story'
LIMIT 3
FORMAT Vertical

Row 1:
──────
id:    2596866
title:
type:  story
by:
time:  1306685152
url:
score: 0

Row 2:
──────
id:    2596870
title: WordPress capture users last login date and time
type:  story
by:    wpsnipp
time:  1306685252
url:   http://wpsnipp.com/index.php/date/capture-users-last-login-date-and-time/
score: 1

Row 3:
──────
id:    2596872
title: Recent college graduates get some startup wisdom
type:  story
by:    whenimgone
time:  1306685352
url:   http://articles.chicagotribune.com/2011-05-27/business/sc-cons-0526-started-20110527_1_business-plan-recession-college-graduates
score: 1

```

While schema inference is a great tool for initial data exploration, it is “best effort” and not a long\-term substitute for defining an optimal schema for your data.


### Define a schema [\#](/blog/getting-data-into-clickhouse-part-1#define-a-schema)


An obvious immediate optimization is to define a type for each field. As well as declaring the time field as a DateTime, we define an appropriate type for each of the fields below after dropping our existing dataset. Also, note that we define a primary key id for our data via the ORDER BY clause. This is a little beyond this post's scope, but readers are recommended to read our introduction to [ClickHouse primary keys](https://clickhouse.com/docs/en/guides/improving-query-performance/sparse-primary-indexes/sparse-primary-indexes-intro). In summary, this will make some queries faster and help with compression.



```
DROP TABLE IF EXISTS hackernews;
 
CREATE TABLE hackernews
(
   `id` UInt32,
   `deleted` UInt8,
   `type` Enum('story' = 1, 'comment' = 2, 'poll' = 3, 'pollopt' = 4, 'job' = 5),
   `by` LowCardinality(String),
   `time` DateTime,
   `text` String,
   `dead` UInt8,
   `parent` UInt32,
   `poll` UInt32,
   `kids` Array(UInt32),
   `url` String,
   `score` Int32,
   `title` String,
   `parts` Array(UInt32),
   `descendants` Int32
)
ENGINE = MergeTree
ORDER BY id

```

With an optimized schema, we can now demonstrate inserting data from the local file system. Again we turn to clickhouse\-client, inserting the file using the [INFILE](https://clickhouse.com/docs/en/sql-reference/statements/insert-into/#inserting-data-from-a-file) clause with an explicit [INSERT INTO](https://clickhouse.com/docs/en/sql-reference/statements/insert-into/#inserting-data-from-a-file). Again this is capable of reading the gz file.



```
INSERT INTO hackernews FROM INFILE '/data/hacknernews.csv.gz' FORMAT CSVWithNames

Query id: 35fa5a90-68ea-466f-bdb5-cdd24f33f047

Ok.

28737557 rows in set. Elapsed: 93.824 sec.

```

There is much more we can do here to optimize this schema \- codecs and support for text tokenization on the text column would be a start, but we’ll explore these in later posts.


### Simple queries [\#](/blog/getting-data-into-clickhouse-part-1#simple-queries)


[Our first thoughts](https://github.com/ClickHouse/ClickHouse/issues/29693#issuecomment-933086439) were to investigate how pervasive ClickHouse is a topic in Hacker News and whether this is increasing over time. The [score](https://github.com/HackerNews/API) field provides us with a metric of popularity for stories, while the id field and [\|\| concatenation operator](https://clickhouse.com/docs/en/sql-reference/operators/#concatenation-operator) can be used to produce a link to the original post.



```
SELECT
    time,
    score,
    descendants,
    title,
    url,
    'https://news.ycombinator.com/item?id=' || toString(id) AS hn_url
FROM hackernews
WHERE (type = 'story') AND (title ILIKE '%ClickHouse%')
ORDER BY score DESC
LIMIT 5 FORMAT Vertical

Row 1:
──────
time:        1632154428
score:       519
descendants: 159
title:       ClickHouse, Inc.
url:         https://github.com/ClickHouse/ClickHouse/blob/master/website/blog/en/2021/clickhouse-inc.md
hn_url:      https://news.ycombinator.com/item?id=28595419

Row 2:
──────
time:        1614699632
score:       383
descendants: 134
title:       ClickHouse as an alternative to Elasticsearch for log storage and analysis
url:         https://pixeljets.com/blog/clickhouse-vs-elasticsearch/
hn_url:      https://news.ycombinator.com/item?id=26316401

Row 3:
──────
time:        1465985177
score:       243
descendants: 70
title:       ClickHouse – high-performance open-source distributed column-oriented DBMS
url:         https://clickhouse.yandex/reference_en.html
hn_url:      https://news.ycombinator.com/item?id=11908254

Row 4:
──────
time:        1578331410
score:       216
descendants: 86
title:       ClickHouse cost-efficiency in action: analyzing 500B rows on an Intel NUC
url:         https://www.altinity.com/blog/2020/1/1/clickhouse-cost-efficiency-in-action-analyzing-500-billion-rows-on-an-intel-nuc
hn_url:      https://news.ycombinator.com/item?id=21970952

Row 5:
──────
time:        1622160768
score:       198
descendants: 55
title:       ClickHouse: An open-source column-oriented database management system
url:         https://github.com/ClickHouse/ClickHouse
hn_url:      https://news.ycombinator.com/item?id=27310247

```

Is ClickHouse generating more noise over time? Note the importance here of our work to ensure the time field is a DateTime, using a proper data type allows us to use the toYYYYMM() function.



```
SELECT
   toYYYYMM(time) AS monthYear,
   bar(count(), 0, 120, 20)
FROM hackernews
WHERE (type IN ('story', 'comment')) AND ((title ILIKE '%ClickHouse%') OR (text ILIKE '%ClickHouse%'))
GROUP BY monthYear
ORDER BY monthYear ASC

Query id: 9c7a0bb3-2a16-42dd-942f-fa9e03cad2c9

┌─monthYear─┬─bar(count(), 0, 120, 20)─┐
│    201606 │ ██▎                      │
│    201607 │ ▏                        │
│    201610 │ ▎                        │
│    201612 │ ▏                        │
│    201701 │ ▎                        │
│    201702 │ █                        │
│    201703 │ ▋                        │
│    201704 │ █                        │
│    201705 │ ██                       │
│    201706 │ ▎                        │
│    201707 │ ▎                        │
│    201708 │ ▏                        │
│    201709 │ ▎                        │
│    201710 │ █▌                       │
│    201711 │ █▌                       │
│    201712 │ ▌                        │
│    201801 │ █▌                       │
│    201802 │ ▋                        │
│    201803 │ ███▏                     │
│    201804 │ ██▏                      │
│    201805 │ ▋                        │
│    201806 │ █▏                       │
│    201807 │ █▌                       │
│    201808 │ ▋                        │
│    201809 │ █▌                       │
│    201810 │ ███▌                     │
│    201811 │ ████                     │
│    201812 │ █▌                       │
│    201901 │ ████▋                    │
│    201902 │ ███                      │
│    201903 │ ▋                        │
│    201904 │ █                        │
│    201905 │ ███▋                     │
│    201906 │ █▏                       │
│    201907 │ ██▎                      │
│    201908 │ ██▋                      │
│    201909 │ █▋                       │
│    201910 │ █                        │
│    201911 │ ███                      │
│    201912 │ █▎                       │
│    202001 │ ███████████▋             │
│    202002 │ ██████▌                  │
│    202003 │ ███████████▋             │
│    202004 │ ███████▎                 │
│    202005 │ ██████▏                  │
│    202006 │ ██████▏                  │
│    202007 │ ███████▋                 │
│    202008 │ ███▋                     │
│    202009 │ ████                     │
│    202010 │ ████▌                    │
│    202011 │ █████▏                   │
│    202012 │ ███▋                     │
│    202101 │ ███▏                     │
│    202102 │ █████████                │
│    202103 │ █████████████▋           │
│    202104 │ ███▏                     │
│    202105 │ ████████████▋            │
│    202106 │ ███                      │
│    202107 │ █████▏                   │
│    202108 │ ████▎                    │
│    202109 │ ██████████████████▎      │
│    202110 │ ▏                        │
└───────────┴──────────────────────────┘

62 rows in set. Elapsed: 1.725 sec. Processed 28.74 million rows, 10.35 GB (16.66 million rows/s., 6.00 GB/s.)

```

It appears we’re heading in the right direction concerning our ability to generate Hacker News conversation. Despite a rather inefficient ILIKE condition on the text field this is still fairly fast at 1\.7s. Later posts will look to optimize this tokenization use case.


What about the top commentators concerning ClickHouse posts?



```
SELECT
   by,
   count() AS comments
FROM hackernews
WHERE (type IN ('story', 'comment')) AND ((title ILIKE '%ClickHouse%') OR (text ILIKE '%ClickHouse%'))
GROUP BY by
ORDER BY comments DESC
LIMIT 5

Query id: 1460bb8d-3263-4521-ace5-9e2300289bb0

┌─by──────────┬─comments─┐
│ hodgesrm    │       78 │
│ zX41ZdbW    │       45 │
│ manigandham │       39 │
│ pachico     │       35 │
│ valyala     │       27 │
└─────────────┴──────────┘

5 rows in set. Elapsed: 1.809 sec. Processed 28.74 million rows, 10.72 GB (15.88 million rows/s., 5.92 GB/s.)

```

Some well\-known community members but most importantly, whose comments generate the most interest?



```
SELECT
	by,
	sum(score) AS total_score,
	sum(length(kids)) AS total_sub_comments
FROM hackernews
WHERE (type IN ('story', 'comment')) AND ((title ILIKE '%ClickHouse%') OR (text ILIKE '%ClickHouse%'))
GROUP BY by
ORDER BY total_score DESC
LIMIT 5

Query id: e9500734-469e-402b-a22a-153914cbe72f

┌─by───────┬─total_score─┬─total_sub_comments─┐
│ zX41ZdbW │     	571 │             	50 │
│ jetter   │     	386 │             	30 │
│ hodgesrm │     	312 │             	50 │
│ mechmind │     	243 │             	16 │
│ tosh 	│     	198 │             	12 │
└──────────┴─────────────┴────────────────────┘

5 rows in set. Elapsed: 1.864 sec. Processed 28.74 million rows, 11.16 GB (15.42 million rows/s., 5.99 GB/s.)

```

### Other formats [\#](/blog/getting-data-into-clickhouse-part-1#other-formats)


One of the strengths of ClickHouse is its ability to handle any [number of formats](https://clickhouse.com/docs/en/interfaces/formats/). We appreciate that CSV represents a rather ideal use case, as well as not being the most efficient for data exchange. Both Parquet and JSON are common interchange formats for different reasons. While Parquet is an efficient column\-oriented format, JSON has become the dominant means of data transfer for semi\-structured information and the web. Both are supported in ClickHouse.


Parquet has [minimal types,](https://parquet.apache.org/docs/file-format/types/) which ClickHouse needs to respect. This type information is encoded in the format itself. Type inference on a Parquet file will invariably lead to a slightly different schema. Below we demonstrate reading the same data in Parquet format, again using the url function to read the remote data. Note we have to accept that keys might be Null (although they aren’t in the data) as a condition of the Parquet format.



```
DROP TABLE IF EXISTS hackernews;

CREATE TABLE hackernews
ENGINE = MergeTree
ORDER BY id
SETTINGS allow_nullable_key = 1 EMPTY AS
SELECT *
FROM url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.parquet', 'Parquet')

INSERT INTO hackernews SELECT *
FROM url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.parquet', 'Parquet')

Ok.

0 rows in set. Elapsed: 314.165 sec. Processed 28.74 million rows, 13.95 GB (91.47 thousand rows/s., 44.39 MB/s.)

```

And the resulting schema,



```
DESCRIBE TABLE hackernews

┌─name────────┬─type───────────────────┬
│ id          │ Nullable(Int64)        │
│ deleted     │ Nullable(UInt8)        │
│ type        │ Nullable(String)       │
│ time        │ Nullable(Int64)        │
│ text        │ Nullable(String)       │
│ dead        │ Nullable(UInt8)        │
│ parent      │ Nullable(Int64)        │
│ poll        │ Nullable(Int64)        │
│ kids        │ Array(Nullable(Int64)) │
│ url         │ Nullable(String)       │
│ score       │ Nullable(Int32)        │
│ title       │ Nullable(String)       │
│ parts       │ Array(Nullable(Int64)) │
│ descendants │ Nullable(Int32)        │
└─────────────┴────────────────────────┴

```

ndJson represents a common interchange format. ClickHouse supports parsing this data through the JSONEachRow format. For the purposes of example, we load a ndjson version of the file from disk.



```
wget https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.json.gz

DROP TABLE IF EXISTS hackernews;
CREATE TABLE hackernews
(
  `id` UInt32,
  `deleted` UInt8,
  `type` Enum('story' = 1, 'comment' = 2, 'poll' = 3, 'pollopt' = 4, 'job' = 5),
  `by` LowCardinality(String),
  `time` DateTime,
  `text` String,
  `dead` UInt8,
  `parent` UInt32,
  `poll` UInt32,
  `kids` Array(UInt32),
  `url` String,
  `score` Int32,
  `title` String,
  `parts` Array(UInt32),
  `descendants` Int32
)
ENGINE = MergeTree
ORDER BY id;

INSERT INTO hackernews FROM INFILE '/data/hacknernews.json.gz' FORMAT JSONEachRow

Ok.

28737557 rows in set. Elapsed: 94.491 sec.

```

### Summary [\#](/blog/getting-data-into-clickhouse-part-1#summary)


In this post we explored getting data into ClickHouse from local and remote files. We exploited schema inference and demonstrated the support for several popular file formats. In future posts, we’ll look to optimize the schema and insert/read performance before demonstrating the loading of data using other clients.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
