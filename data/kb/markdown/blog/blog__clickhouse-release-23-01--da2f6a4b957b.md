# ClickHouse Release 23\.1


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 23\.1

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 30, 2023 · 9 minutes read![23.1 Release Post.png](/uploads/23_1_Release_Post_9b8030390c.png)
It's a new year! And, it is also a new release of ClickHouse. We are delighted to introduce the first release of the 23\.x series with 23\.1\.


As per usual, we hosted a ClickHouse community call to talk through the release, provide live demos, and answer your questions.


Keep an out for the 23\.2 release webinar announcement. And, if you want to learn more about ClickHouse fundamentals, check out upcoming training sessions:


- [ClickHouse Workshop (11 AM PST) \- Feb 1 \& 2](https://clickhouse.com/company/events/2023-02-01-clickhouse-workshop)
- [ClickHouse Cloud Onboarding (3 PM GMT) \- Feb 8](https://clickhouse.com/company/events/2023-02-08-clickhouse-onboarding-workshop)



## Release Summary [\#](/blog/clickhouse-release-23-01#release-summary)


- 17 new features.
- 17 performance optimisations.
- 78 bug fixes.


And, of course, a host of performance improvements.


If that’s not enough to get you interested in trying it out. Check out some of the headline items:


## Inverted Full Text Indices \- Larry Luo, Harry Lee [\#](/blog/clickhouse-release-23-01#inverted-full-text-indices---larry-luo-harry-lee)


Yes, you read it right. In this release, we add experimental support for Inverted indices in ClickHouse as a data\-skipping index. While this doesn't make ClickHouse a fully\-fledged search engine, it introduces some interesting possibilities for improving the performance of specific token\-based queries. If you have a dataset with large text blobs on which you perform token matches, this feature is for you.


This index can be used to speed up any String functions performing token matching, specifically the [multiSearchAny](https://clickhouse.com/docs/en/sql-reference/functions/string-search-functions/#multisearchanyhaystack-needle1-needle2--needlen) and hasToken functions. This should allow you to build fairly complex boolean conditions as shown below. Furthermore, equality operators such as `LIKE`, `IN` and `==` all benefit i.e.



```
SELECT * from tab WHERE s == 'Hello World';
SELECT * from tab WHERE s IN ('Hello', 'World');
SELECT * from tab WHERE s LIKE '%Hello%';

```

The easiest way to demonstrate this feature is by using a dataset with a decent amount of Text. What better than our favorite Hacker News data?


Consider this query in our [sql.clickhouse.com](https://sql.clickhouse.com?query_id=VWNMT1VWGJACNVNNPZYMFD) environment finding all posts mentioning ClickHouse over time:



```

SELECT
    toYYYYMM(toDateTime(time)) AS monthYear,
    bar(count(), 0, 120, 20) AS count
FROM hackernews
WHERE (text ILIKE '%ClickHouse%')
GROUP BY monthYear
ORDER BY monthYear ASC

│    201910 │ ▊                    │
│    201911 │ ██▊                  │
│    201912 │ █▎                   │
│    202001 │ ███████████▏         │
│    202002 │ ██████               │
│    202003 │ ███████████▌         │
│    202004 │ ███████▏             │
│    202005 │ █████▋               │
│    202006 │ █████▊               │
│    202007 │ ███████▎             │
│    202008 │ ███▌                 │
│    202009 │ ██▊                  │
│    202010 │ ████▌                │
│    202011 │ ████▋                │
│    202012 │ ███▏                 │
│    202101 │ ██▊                  │
│    202102 │ ████████▎            │
│    202103 │ ████████████▏        │
│    202104 │ ██▌                  │
│    202105 │ ████████████▏        │
│    202106 │ ██▏                  │
│    202107 │ ████▏                │
│    202108 │ ████                 │
│    202109 │ ████████████████▎    │
│    202110 │ ████████████████████ │
│    202111 │ ███████████▌         │
│    202112 │ ███████████▏         │
│    202201 │ ██████▊              │
│    202202 │ ███████              │
│    202203 │ ████▊                │
│    202204 │ █████████▋           │
│    202205 │ █████████████        │
│    202206 │ █████████████▊       │
│    202207 │ ████████████▌        │
│    202208 │ ██████▊              │
│    202209 │ █████████▊           │
│    202210 │ ████████████████████ │
│    202211 │ ██████▏              │
│    202212 │ █▋                   │
└───────────┴──────────────────────┘

67 rows in set. Elapsed: 0.561 sec. Processed 33.95 million rows, 11.62 GB (60.53 million rows/s., 20.72 GB/s.)
[✎](https://sql.clickhouse.com?query_id=VWNMT1VWGJACNVNNPZYMFD)

```


Aside from how more newsworthy we're becoming, note the timing here. Despite being fast, in its current form, this query requires a linear scan over the entire document set. We can add our inverted index to text and title fields using the normal syntax for skipping indices:



```
ALTER TABLE hackernews ADD INDEX inv_idx(text) TYPE inverted;
ALTER TABLE hackernews MATERIALIZE INDEX inv_idx;

```


```
SELECT
    toYYYYMM(toDateTime(time)) AS monthYear,
    bar(count(), 0, 120, 20) AS count
FROM hackernews_indexed
WHERE multiSearchAny(text, ['ClickHouse', 'Clickhouse', 'clickHouse', 'clickhouse'])
GROUP BY monthYear
ORDER BY monthYear ASC

│    202210 │ ████████████████████ │
│    202211 │ ██████▏              │
│    202212 │ █▋                   │
└───────────┴──────────────────────┘

72 rows in set. Elapsed: 0.285 sec. Processed 6.07 million rows, 2.18 GB (21.27 million rows/s., 7.65 GB/s.)

```


To check if the index is being used, you can prepend `EXPLAIN indexes=` to your query i.e.



```
EXPLAIN indexes = 1
SELECT
    toYYYYMM(toDateTime(time)) AS monthYear,
    bar(count(), 0, 120, 20) AS count
FROM hackernews_indexed
WHERE text LIKE '%clickhouse%'
GROUP BY monthYear
ORDER BY monthYear ASC

┌─explain──────────────────────────────────────────────────────┐
│ Expression ((Projection + Before ORDER BY [lifted up part])) │
│   Sorting (Sorting for ORDER BY)                             │
│     Expression (Before ORDER BY)                             │
│       Aggregating                                            │
│         Expression (Before GROUP BY)                         │
│           ReadFromMergeTree (default.hackernews_indexed)     │
│           Indexes:                                           │
│             PrimaryKey                                       │
│               Condition: true                                │
│               Parts: 1/1                                     │
│               Granules: 4150/4150                            │
│             Skip                                             │
│               Name: inv_idx                                  │
│               Description: inverted GRANULARITY 1            │
│               Parts: 1/1                                     │
│               Granules: 4150/4150                            │
└──────────────────────────────────────────────────────────────┘

```


Some limitations (it's experimental, after all):


- We don't store positions of terms with our postings, preventing phrase matching or the optimization of functions such as [multisearchallpositions](https://clickhouse.com/docs/en/sql-reference/functions/string-search-functions/#multisearchallpositions).
- We have no relevancy calculation \- for this, we would need to persist term statistics, considered out of scope for the initial iteration. Currently the index is purely used to speed up matches.
- Text is either tokenized by splitting on whitespace OR via a [configurable n\-gram size](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/invertedindexes/) if you need substring matching. Text processing is not configurable, and thus this feature isn't comparable to natural language engines such as Lucene.


In summary, if you need to accelerate simple token matching, this is for you. "What about logging data?" you say, maybe? We'll discuss in a follow\-up post as part of our Observability series.


If you need relevancy features and more nuanced text matching e.g. e\-commerce, maybe don't replace your search engine quite yet.... but stay tuned; we expect to see improvements in this feature over the coming releases and things move fast in ClickHouse :)


We expect many of you will have questions as to how this feature has been implemented. Expect a follow\-up blog very soon on the internals.


## Parametized Views \- Smita Kulkarni [\#](/blog/clickhouse-release-23-01#parametized-views---smita-kulkarni)


Anyone who writes a lot of SQL learns to appreciate views quickly. They allow users to abstract away complex queries and expose them with table syntax \- allowing further more complex queries to be constructed from component parts without being overwhelmed with pages of SQL.
Until now, users could only create static views. With the 23\.1 release of ClickHouse, we can create dynamic views based on parameters passed at query time.


Suppose we want a view for searching a Stack Overflow dataset. This dataset is available \[<https://archive.org/details/stackexchange>] and [described as a post](https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede).


Our example below is static and limited to searching for `ClickHouse` posts.



```

CREATE VIEW search_clickhouse_stackoverflow AS
SELECT
    Id,
    CreationDate,
    Title,
    LastActivityDate,
    ViewCount,
    AnswerCount,
    Score
FROM stackoverflow
WHERE (PostTypeId = 1) AND multiSearchAny(Body, ['ClickHouse'])

SELECT *
FROM search_clickhouse_stackoverflow
LIMIT 1
FORMAT Vertical

Row 1:
──────
Id:               71655910
CreationDate:     2022-03-29 02:50:35.920000000
Title:            How to execute "with" query locally in ClickHouse？
LastActivityDate: 2022-03-29 03:08:04.863000000
ViewCount:        48
AnswerCount:      0
Score:            0

1 row in set. Elapsed: 1.445 sec. Processed 200.26 thousand rows, 276.42 MB (138.60 thousand rows/s., 191.31 MB/s.)
[✎](https://sql.clickhouse.com?query_id=5RZTNTHWWQKVMZHBTXSRG2)

```


Ideally, we'd like this view to be more flexible than just searching for ClickHouse posts. Using Parameterized views we can now generalize this view:



```

CREATE VIEW search_stackoverflow AS
SELECT
    Id,
    CreationDate,
    Title,
    LastActivityDate,
    ViewCount,
    AnswerCount,
    Score
FROM stackoverflow
WHERE (PostTypeId = 1) AND multiSearchAny(Body, splitByWhitespace({text:String}))

SELECT *
FROM search_stackoverflow(text = 'ClickHouse MergeTree')
ORDER BY Score DESC
LIMIT 1 FORMAT Vertical

Row 1:
──────
Id:               40592010
CreationDate:     2016-11-14 15:13:55.310000000
Title:            Multiple small inserts in clickhouse
LastActivityDate: 2021-01-06 09:14:48.947000000
ViewCount:        15849
AnswerCount:      5
Score:            15

1 row in set. Elapsed: 0.594 sec. Processed 5.79 million rows, 8.10 GB (9.75 million rows/s., 13.62 GB/s.)
[✎](https://sql.clickhouse.com?query_id=OVVFRFJVZXTWGQDB2CQDU7)

```


Note we also split the query string on whitespace to exploit the `multiSearchAny` function. We also optimize with an Inverted Index. This represents a crude search capability but hopefully gives you an idea of how to combine these features.


## Query Results Cache \- Robert Schutze, Mikhail Stetsyuk [\#](/blog/clickhouse-release-23-01#query-results-cache---robert-schutze-mikhail-stetsyuk)


To achieve maximum performance, analytical databases optimize every step of their internal data storage and processing pipeline. But the best kind of work performed by a database is work that is not done at all! Caching is an especially popular technique for avoiding unnecessary work by storing the results of earlier computation or remote data, which is expensive to access. ClickHouse uses caching extensively, for example, to cache DNS records, local and remote (S3\) data, inferred schemas, compiled queries, and regular expressions. In 23\.1, we introduce a new member to the ClickHouse family of Caches, the Query Result Cache!


The query cache is based on the idea that sometimes there are situations where it is okay to cache the result of expensive SELECT queries such that further executions of the same queries can be served directly from the cache. Depending on the type of queries, this can dramatically reduce the latency and resource consumption of the ClickHouse server. As an example, consider a data visualization tool like Grafana or Apache Superset, which displays a report of aggregated sales figures for the last 24 hours. In most cases, sales numbers within a day will change rather slowly, and we can afford to refresh the report only (for example) every three hours. Starting with ClickHouse v23\.1, SELECT queries can be provided with a "time\-to\-live" during which the server will only compute the first execution of the query, and further executions are answered without further computation directly from the cache.


Users should note this is not a transactionally consistent cache \- entries will **not** be removed from the cache if the underlying data changes. This is by design and justified for a number of reasons. As an OLAP database, we tolerate slightly inaccurate results for the benefit of performance and cache scalability. ClickHouse also has background operations, such as collapsing merges that potentially change data, that would make a transactionally consistent cache likely ineffective. Cache entries are, therefore, only based on a TTL, after which their entries will be removed.


Since this is such a substantial feature, with lots of tunable settings, we'll have a dedicated blog post on this shortly.


## Helpful Links [\#](/blog/clickhouse-release-23-01#helpful-links)


- [23\.1 Release Changelog](https://github.com/ClickHouse/ClickHouse/blob/master/CHANGELOG.md#231)
- [23\.1 Release Presentation](https://presentations.clickhouse.com/release_23.1/)
- [ClickHouse 23\.1 Release Webinar](https://www.youtube.com/watch?v=zYSZXBnTMSE&list=PL0Z2YDlm0b3jAlSy1JxyP8zluvXaN3nxU&index=1)
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
