# Getting Data Into ClickHouse \- Part 2 \- A JSON detour


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Getting Data Into ClickHouse \- Part 2 \- A JSON detour

![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Dale McDiarmid](/authors/dale-mcdiarmid)Sep 1, 2022 · 13 minutes read![train-g63180fbf5_1920.jpg](/uploads/large_train_g63180fbf5_1920_3325f12d5d.jpg)
This blog post is part of a series:


- [Getting Data Into ClickHouse \- Part 1](https://clickhouse.com/blog/getting-data-into-clickhouse-part-1)
- [Getting Data Into ClickHouse \- Part 3 \- Using S3](https://clickhouse.com/blog/getting-data-into-clickhouse-part-3-s3)


This post continues the series “Getting Data Into ClickHouse”. In our previous post, we showed the basics of loading a Hacker News dataset. As well as demonstrating the power of schema inference to a getting\-started user, we also highlighted the need to define a schema for efficient query execution. Before delving into more complex topics such as schema optimization and primary key selection, we exploit the fact that the Hacker News dataset is distributed as JSON to take a small detour and explore the recently added JSON capabilities of ClickHouse.


The JSON file format has become ubiquitous for encoding datasets, such as structured logs, due to its human\-readable, self\-describing format. ClickHouse has become an increasingly popular data store to analyze logs and events encoded in JSON. The JSON data type enhances existing JSON capabilities by allowing columns to be automatically inferred and created from the data, i.e. there is no requirement beyond declaring a column as “JSON”. This allows ClickHouse to deal with dynamic schemas where new columns are added and removed continuously. In this post, we demonstrate these capabilities through the Hacker News dataset.


While the examples below are executed using [ClickHouse Cloud](https://clickhouse.cloud/signUp), all commands will also be compatible with self\-managed ClickHouse clusters running on the average laptop with internet access. Our client is hosted on a [c5ad.4xlarge](https://aws.amazon.com/ec2/instance-types/c5/) with 16 cores and 32GB of RAM.


The JSON data type is still experimental within ClickHouse as of version 22\.8\. This feature is therefore not ready for production use. Users are encouraged to experiment and provide feedback as we move to a production\-ready state.


## Download [\#](/blog/getting-data-into-clickhouse-part-2-json#download)


Our examples all access the file via the url function and do not require the user to download the dataset explicitly. The JSON version of the dataset can, however, be downloaded from here for more curious readers. At 4\.9GB, and 28m rows, this compressed file should take 5\-10 minutes to download.


## Reading JSON [\#](/blog/getting-data-into-clickhouse-part-2-json#reading-json)


Our Hacker News data is effectively ndjson, with one JSON row per line. This equates to the ClickHouse JSONEachRow format. Using the DESCRIBE command, we can inspect the types assigned by schema inference before sampling a row.



```

DESCRIBE TABLE url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.json.gz', 'JSONEachRow');

┌─name────────┬─type─────────────────────|
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
└─────────────┴──────────────────────────|


```



```

SELECT *
FROM url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.json.gz', JSONEachRow)
LIMIT 1
FORMAT Vertical;

Row 1:
──────
id:          11132929
deleted:     0
type:        story
by:          brakmic
time:        2016-02-19 11:40:55
text:
dead:        1
parent:      0
poll:        0
kids:        [11133170]
url:         https://www.washingtonpost.com/news/morning-mix/wp/2016/02/18/s-f-tech-bro-writes-open-letter-to-mayor-i-shouldnt-have-to-see-the-pain-struggle-and-despair-of-homeless-people/
score:       3
title:       SF ‘tech bro’ writes to mayor: ‘I shouldn’t have to see the despair of homeless’
parts:       []
descendants: 0



```


Readers of our [previous blog post in this series](https://clickhouse.com/blog/getting-data-into-clickhouse-part-1) will notice this isn’t significantly different from our CSV example \- each column is assigned a type by schema inference. While we’re reading the data as JSON, we aren’t treating it as a JSON object. To achieve this, we introduce the JSONAsObject format.



```

DESCRIBE TABLE url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.json.gz', 'JSONAsObject', 'post JSON');

┌─name──┬─type───────────|
│ post │ Object('json')  │
└───────┴────────────────┴



```



```

SELECT *
FROM url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.json.gz', 'JSONAsObject', 'post JSON')
LIMIT 1
FORMAT JSONEachRow;

{"post":{"by":"brakmic","dead":1,"deleted":0,"descendants":0,"id":11132929,"kids":[11133170],"parent":0,"poll":0,"score":3,"text":"","time":"2016-02-19 11:40:55","title":"SF ‘tech bro’ writes to mayor: ‘I shouldn’t have to see the despair of homeless’","type":"story",
"url":"https:\/\/www.washingtonpost.com\/news\/morning-mix\/wp\/2016\/02\/18\/s-f-tech-bro-writes-open-letter-to-mayor-i-shouldnt-have-to-see-the-pain-struggle-and-despair-of-homeless-people\/"}}
 
1 row in set. Elapsed: 3.456 sec.



```


This requires us to specify a target field for the JSON: post in this case. Note how we can also request our output to be returned in JSON by reusing the format JSONEachRow. The key observation is that the post column is assigned the new type `Object('json')`.


## JSON As Objects [\#](/blog/getting-data-into-clickhouse-part-2-json#json-as-objects)


Above, we introduced the `Object(‘json’)` type to represent a JSON row. Assuming we map our Hacker News rows to this type, our schema definition becomes trivial. This is the true power of this type. Our data is now treated as semi\-structured, and any sub\-columns will automatically be created and their types inferred from the data!



```

DROP TABLE IF EXISTS hackernews;
 
SET allow_experimental_object_type = 1;
 
CREATE TABLE hackernews
(
   `post` JSON
)
ENGINE = MergeTree
ORDER BY tuple();



```


A few important observations here. We use the JSON type as an abbreviation for `Object('JSON')` \- in the future, we may add additional Object representations beyond JSON. Secondly, we are required to set `allow_experimental_object_type = 1` to use this type since it is experimental. Finally, note that we can’t utilize any sub\-columns of post as primary keys and thus have defined our `ORDER BY as tuple()`, i.e., no primary key. We address this limitation later.


With this table created, insertion becomes trivial.



```

INSERT INTO hackernews SELECT post
FROM url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.json.gz', 'JSONAsObject', 'post JSON')
 
0 rows in set. Elapsed: 214.846 sec. Processed 28.74 million rows, 13.42 GB (133.76 thousand rows/s., 62.46 MB/s.)



```


Selecting a single row gives us an insight into how JSON is represented in ClickHouse.



```

SELECT *
FROM hackernews
LIMIT 1
FORMAT Vertical
 
Row 1:
──────
post: ('brakmic',1,0,0,11132929,[11133170],0,[],0,3,'','2016-02-19 11:40:55','SF ‘tech bro’ writes to mayor: ‘I shouldn’t have to see the despair of homeless’','story','https://www.washingtonpost.com/news/morning-mix/wp/2016/02/18/s-f-tech-bro-writes-open-letter-to-mayor-i-shouldnt-have-to-see-the-pain-struggle-and-despair-of-homeless-people/')


```


Using the `DESCRIBE` command and setting `describe_extend_object_types=1` confirms the use of Tuples as an internal representation:



```

DESCRIBE TABLE hackernews
FORMAT Vertical
SETTINGS describe_extend_object_types = 1

Query id: bcbf8c48-82eb-4916-869c-842a32445711

Row 1:
──────
name:               post
type:               Tuple(by String, dead Int8, deleted Int8, descendants Int16, id Int32, kids Array(Int32), parent Int32, parts Array(Int32), poll Int32, score Int16, text String, time String, title String, type String, url String)


```


As well as the type providing a clean representation of JSON by using Tuples, Arrays and Nested columns under the hood, it ensures new columns will automatically be created and a type inferred as they occur in the data. As of 22\.8, type inference works for numeric and strings: with the former being assigned the minimal bit representation possible based on the observed data.


## Querying JSON [\#](/blog/getting-data-into-clickhouse-part-2-json#querying-json)


Querying our columns within each row requires us to use dot representation to indicate field paths in the JSON. Below we repeat a query from our first post in this series that identifies the number of posts concerning ClickHouse. Since our time column has been mapped as a String, we are forced to parse this at query time using the [parseDateTimeBestEffort](https://clickhouse.com/docs/en/sql-reference/functions/type-conversion-functions/#parsedatetimebesteffort) function \- forcing a linear scan. For brevity purposes, we also limit the results to the last 2 yrs.



```

SELECT
    toYYYYMM(parseDateTimeBestEffort(post.time)) AS monthYear,
    bar(count(), 0, 120, 20)
FROM hackernews
WHERE (post.type IN ('story', 'comment')) AND ((post.title ILIKE '%ClickHouse%') OR (post.text ILIKE '%ClickHouse%')) AND (monthYear > '201908')
GROUP BY monthYear
ORDER BY monthYear ASC

┌─monthYear─┬─bar(count(), 0, 120, 20)─┐
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
 
26 rows in set. Elapsed: 2.626 sec. Processed 28.74 million rows, 11.47 GB (10.94 million rows/s., 4.37 GB/s.)



```


## Overcoming Limitations [\#](/blog/getting-data-into-clickhouse-part-2-json#overcoming-limitations)


As noted above, we can’t currently utilize a JSON sub column as a primary key since ClickHouse has no knowledge of the potentially dynamic columns at table creation time. We can’t specify codecs for sub\-columns for similar reasons. To overcome this restriction, we recommend users use the JSON type for the semi\-structured parts of rows that are subject to change but explicitly specify columns for those for which a reliable structure and type can be declared. For example, below, we explicitly define the time and type columns but leave the others to be captured by the post column. This, in turn, allows us to define these as components of the primary key.



```

SET allow_experimental_object_type = 1;
 
DROP TABLE IF EXISTS hackernews;
 
CREATE TABLE hackernews
(
   `post` JSON,
   `type` String,
   `time` DateTime
)
ENGINE = MergeTree ORDER BY (time, type);



```


To insert data we need to use the format JSONAsString which interprets each row as a single JSON string. This allows the use of the [JSONExtract\*](https://clickhouse.com/docs/en/sql-reference/functions/json-functions/) functions for extracting specific fields. Future releases of ClickHouse will support these functions with JSONAsObject. We include the optional `post String` component of the [url](https://clickhouse.com/docs/en/sql-reference/table-functions/url/) function for clarity. If excluded, ClickHouse will infer a column `json`.



```

INSERT INTO hackernews SELECT
   post::JSON,
   JSONExtractString(post, 'type') AS type,
   toDateTime(JSONExtractString(post, 'time')) AS time
FROM url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.json.gz', 'JSONAsString', 'post String')
 
0 rows in set. Elapsed: 335.605 sec. Processed 28.74 million rows, 16.24 GB (85.63 thousand rows/s., 48.38 MB/s.)



```


Repeating the earlier query, and adjusting for our field names, demonstrates the performance benefit of managing our structured fields separately and using them in the primary key (notice the speed up!).



```

SELECT
   toYYYYMM(time) AS monthYear,
   bar(count(), 0, 120, 20)
FROM hackernews
WHERE (type IN ('story', 'comment')) AND ((post.title ILIKE '%ClickHouse%') OR (post.text ILIKE '%ClickHouse%')) AND (monthYear > '201908')
GROUP BY monthYear
ORDER BY monthYear ASC
 
// omitted for brevity
 
26 rows in set. Elapsed: 0.742 sec. Processed 7.93 million rows, 3.09 GB (10.69 million rows/s., 4.17 GB/s.)



```

## A few gotchas [\#](/blog/getting-data-into-clickhouse-part-2-json#a-few-gotchas)


ClickHouse can only base the inferred types on the data it has seen. For numeric types, we aim to minimize resource utilization (disk and memory) by assigning the lowest bit representation possible. However, should a new value arrive which requires this to be extended, the type will transparently change. For example, suppose we receive an update of our data, and a new column “likes” has been added to represent equivalent functionality added to Hacker News.


If we insert a single comment with 2 likes, our new column will be initially represented as an Int8\.



```

INSERT INTO hackernews(post, type, time) FORMAT JSONEachRow {"post":{"by":"zX41ZdbW","id":20684796,"text":"ClickHouse is happy to use multiple cores if the query is heavy enough.","likes":2},"type":"comment","time":"2022-08-12 11:48:08"};



```



```

DESCRIBE TABLE hackernews
FORMAT Vertical
SETTINGS describe_extend_object_types = 1

Query id: c1a80073-b5c3-48c1-aa77-7cef5f3eb2d1

Row 1:
──────
name:               post
type:               Tuple(by String, dead Int8, deleted Int8, descendants Int16, id Int32, kids Array(Int32), likes Int8, parent Int32, parts Array(Int32), poll Int32, score Int16, text String, time String, title String, type String, url String)
default_type:
default_expression:
comment:
codec_expression:
ttl_expression:



```


However, suppose a 2nd comment receives several thousand likes.



```

INSERT INTO hackernews(post, type, time) FORMAT JSONEachRow {"post":{"by":"dalem","id":1111111,"text":"ClickHouse is just the best OLAP DB ever!!!!!.","likes":2000000},"type":"comment","time":"2022-08-13 11:48:08"};


```



```

DESCRIBE TABLE hackernews
FORMAT Vertical
SETTINGS describe_extend_object_types = 1

Query id: 3056120f-1e7c-4494-b43a-510518c93380

Row 1:
──────
name:               post
type:               Tuple(by String, dead Int8, deleted Int8, descendants Int16, id Int32, kids Array(Int32), likes Int32, parent Int32, parts Array(Int32), poll Int32, score Int16, text String, time String, title String, type String, url String)
default_type:
default_expression:
comment:
codec_expression:
ttl_expression:


```


Our column has been transparently mapped to a UInt32\.


This functionality rarely impacts queries. However, if the value is sent as a string (e.g. due to a single “dirty” document), it will transparently convert the column to a String type. This potentially could break queries that rely on numeric values. Either cleanse your data diligently or explicitly declare columns outside of the JSON to enforce type correctness.


## Summary [\#](/blog/getting-data-into-clickhouse-part-2-json#summary)


In this post, we have explored reading JSON datasets and the JSON object type. We have demonstrated the flexibility of this type and its ability to adapt to changing data, as well as some limitations and how to overcome them. Future posts will utilize this capability more fully, once it is no longer experimental, for addressing problems such as using ClickHouse as a log store.


For users looking for more information on the JSON capabilities of ClickHouse, we have updated our [documentation](https://clickhouse.com/docs/en/guides/developer/working-with-json) to describe the alternative approaches to dealing with semi\-structured data.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
