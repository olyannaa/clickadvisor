# ClickHouse Newsletter May 2022: Explain Statement – Query Optimization


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter May 2022: Explain Statement – Query Optimization

![photo-christoph-wurm[1].jpeg](/_next/image?url=%2Fuploads%2Fphoto_christoph_wurm_1_7af9415ecb.jpeg&w=96&q=75)[Christoph Wurm](/authors/christoph-wurm)May 9, 2022 · 12 minutes read
A warm welcome to you all. It has been a busy few weeks at the ClickHouse office in Amsterdam – we have launched the private preview phase of our ClickHouse Cloud service! In the coming weeks and months the brave users that have joined this preview will help us find and fix all the bugs and tiny details we want to get right before we open it up to the world later this year. If you’re interested in a serverless managed service for ClickHouse, join our waitlist [here](https://clickhouse.com/cloud/).


We also released ClickHouse 22\.4, [new documentation pages](https://clickhouse.com/docs/), and the new [official ClickHouse plugin for Grafana](https://grafana.com/grafana/plugins/grafana-clickhouse-datasource/). There is a date to [release ClickHouse 22\.5](https://clickhouse.com/company/events/v22-5-release-webinar/) and some meetups are coming up so don’t forget to block your calendars!


## **Upcoming Events** [\#](/blog/clickhouse-newsletter-may-2022-explain-statement-query-optimization#upcoming-events)


Mark your calendars for these:


**ClickHouse v22\.5 Release Webinar**


- **When?** Thursday, May 19 @ 9 am PDT, 5 pm GMT
- **How to join?** Register [here](https://clickhouse.com/company/events/v22-5-release-webinar/).


**ClickHouse Americas Virtual Meetup**


- ***What?*** Gigasheet is using ClickHouse to build a simple, no\-code analytics product with a web\-based spreadsheet interface. Something to finally replace Excel with?! Also our own Geoff Genz will share his journey of implementing ClickHouse at scale at Comcast. A must\-see!
- ***When?*** Thursday, May 12 @ 11 am PST, 2 pm EST
- ***How?*** Register in the meetup groups for [New York](https://www.meetup.com/clickhouse-new-york-user-group/events/285565903/) or [Seattle](https://www.meetup.com/clickhouse-seattle-user-group/events/285568527/)**.**


**ClickHouse EMEA Virtual Meetup**


- ***What?*** Fintech company Opensee will talk about how they use ClickHouse to provide self\-service analytics across large amounts of data at financial institutions. And afterwards, Alexey – the creator of ClickHouse – will dive into the internals that make ClickHouse fast. Come prepared with your questions!
- ***When?*** Thursday, May 12 @ 1 pm BST / 2 pm CEST / 3 pm EEST \\
- ***How?*** Register in the meetup groups for [Netherlands](https://www.meetup.com/clickhouse-netherlands-user-group/events/285565831/), [France](https://www.meetup.com/clickhouse-france-user-group/events/285568216/), [London](https://www.meetup.com/clickhouse-london-user-group/events/285567041/), [Germany](https://www.meetup.com/clickhouse-berlin-user-group/events/285568230/), [Bangalore](https://www.meetup.com/clickhouse-bangalore-user-group/events/285569477/) – or all of them if you like!


## New Documentation [\#](/blog/clickhouse-newsletter-may-2022-explain-statement-query-optimization#new-documentation)


We have given the ClickHouse Documentation pages a new look! There is a new navigation structure on the left side and also lots of new content. We are sure there is at least one new thing for you to learn:


- **[Quick Start](https://clickhouse.com/docs/en/quick-start/)** The fastest way to get started with ClickHouse. Just download, run, create a table, insert some data and query!
- **[Tutorial](https://clickhouse.com/docs/en/tutorial/)** Takes you through loading the New York City taxi rides dataset into ClickHouse, some fun aggregation queries you can run on it, how to use a dictionary and how to join.
- **[Connect a UI](https://clickhouse.com/docs/en/connect-a-ui)** Step\-by\-step guides on how to connect [Grafana](https://clickhouse.com/docs/en/connect-a-ui/grafana-and-clickhouse), [Metabase](https://clickhouse.com/docs/en/connect-a-ui/metabase-and-clickhouse), [Superset](https://clickhouse.com/docs/en/connect-a-ui/superset-and-clickhouse) and [Tableau](https://clickhouse.com/docs/en/connect-a-ui/tableau-and-clickhouse) to ClickHouse.
- **[Integrations](https://clickhouse.com/docs/en/integrations)** More step\-by\-step guides on how to integrate ClickHouse with [Airbyte](https://clickhouse.com/docs/en/integrations/airbyte-and-clickhouse), [dbt](https://clickhouse.com/docs/en/integrations/dbt), [JDBC](https://clickhouse.com/docs/en/integrations/jdbc), [Kafka](https://clickhouse.com/docs/en/integrations/kafka), [MySQL](https://clickhouse.com/docs/en/integrations/mysql), [PostgreSQL](https://clickhouse.com/docs/en/integrations/postgresql), [S3](https://clickhouse.com/docs/en/integrations/s3), and [Vector](https://clickhouse.com/docs/en/integrations/vector-to-clickhouse).
- **[User Guides](https://clickhouse.com/docs/en/guides/)** Lots of new user guides, including how to set up [ClickHouse Keeper](https://clickhouse.com/docs/en/guides/sre/clickhouse-keeper), [rebalance shards](https://clickhouse.com/docs/en/guides/sre/scaling-clusters), [work with JSON](https://clickhouse.com/docs/en/guides/developer/working-with-json), and improve query performance using [data skipping indexes](https://clickhouse.com/docs/en/guides/improving-query-performance/skipping-indexes) and [sparse primary indexes](https://clickhouse.com/docs/en/guides/improving-query-performance/sparse-primary-indexes). This is what many of you have been waiting for!


## **ClickHouse v22\.4** [\#](/blog/clickhouse-newsletter-may-2022-explain-statement-query-optimization#clickhouse-v224)


What’s in our regular monthly April release:


1. **[Transactions](https://github.com/ClickHouse/ClickHouse/pull/24258)** are available as a (highly experimental) preview feature. `BEGIN TRANSACTION`, `COMMIT` and `ROLLBACK` statements support atomic inserts into multiple tables and materialized views as well as consistent and isolated reads from a single snapshot. More to come here, stay tuned!
2. **[Keeper load balancing](https://github.com/ClickHouse/ClickHouse/pull/30325)** You can now specify how a ClickHouse instance chooses a (ClickHouse) Keeper or (Apache) ZooKeeper instance to connect to. The new `config.xml` setting is `&lt;zookeeper_load_balancing>` with possible values `random` (default), `in_order`, `nearest_hostname`, `first_or_random` and `round_robin`. This can help ensure low latency between ClickHouse and Keeper when you have different Keeper nodes that are far apart from each other.
3. **[Table metadata cache](https://github.com/ClickHouse/ClickHouse/pull/32928)** A new table setting `use_metadata_cache` uses the embedded RocksDB engine to cache table metadata. When ClickHouse starts up, it will try to read from this cache and fall back to the table files on disk if needed. This is useful when you have a very large number of data parts (usually caused by having a lot of databases, tables, and/or partitions, or by very high insert volume creating a lot of parts). In one extreme instance (700k parts), the metadata cache was able to reduce startup time from 75 minutes to 20 seconds.
4. **[Kafka metrics](https://github.com/ClickHouse/ClickHouse/pull/35916)** The Kafka table engine is now exposing some metrics, e.g. number of processed messages, number of errors, number of messages that failed to parse. You can find these in the `system.metrics` and `system.events` tables.
5. **[Gap filling](https://github.com/ClickHouse/ClickHouse/pull/35349)** You can now fill gaps in result sets using interpolation. For example, when you have minute\-by\-minute data but sometimes the value for a minute might be missing (completely missing, or maybe it’s stil making it’s way through the ingest pipeline and arriving late), you can have ClickHouse use the previous value instead using `ORDER BY toStartOfMinute(timestamp) WITH FILL INTERPOLATE (c AS c)`. More complex expressions are possible.
6. **[Last day of month](https://github.com/ClickHouse/ClickHouse/pull/34394)** So far, the ClickHouse date functions would round to the start of a time period ( `toStartOf[Year|Month|Week|Day|Hour|Minute|etc.`). Now, we also have `toLastDayOfMonth` if you want to round to the last day of a month (useful for financial and accounting data).
7. **[H3](https://github.com/ClickHouse/ClickHouse/pull/34568)** We’ve rounded out support for H3, the “hexagonal hierarchical geospatial indexing system” originally developed and open sourced by Uber. If you don’t know it yet, have a look at the [website](https://h3geo.org/) and the comparisons to other systems like [S2](https://h3geo.org/docs/comparisons/s2) and [Geohash](https://h3geo.org/docs/comparisons/geohash).


Take a look at the [release webinar slides](https://presentations.clickhouse.com/release_22.4/) and please upgrade (unless you want to stay on an LTS release).


## **Query of the Month: Explain Statement – Query Optimization** [\#](/blog/clickhouse-newsletter-may-2022-explain-statement-query-optimization#query-of-the-month-explain-statement--query-optimization)


One of the most important skills you can have as a ClickHouse user is query optimization. This will get you started.


**EXPLAIN SYNTAX**


If you’re not familiar yet with the EXPLAIN statement head over to the [documentation](https://clickhouse.com/docs/en/sql-reference/statements/explain/) and have a look. This is your best friend when debugging queries in ClickHouse. The first instance of this command you should know is EXPLAIN SYNTAX. You can use it like this:



```
EXPLAIN SYNTAX
SELECT sum(number)
FROM (SELECT * FROM numbers(10000))
WHERE number <= 10

```

This will show what query is actually going to be executed after any syntax optimizations. The output:



```
┌─explain─────────────────┐
│ SELECT sum(number)      │
│ FROM                    │
│ (                       │	
│     SELECT number       │
│     FROM numbers(10000) │
│     WHERE number <= 10  │
│ )                       │
│ WHERE number <= 10      │
└─────────────────────────┘

```

You can see two things:


1. The wildcard projection in the subquery was replaced with the actual column name `number`.
2. Even though the WHERE condition appears only on the outside, ClickHouse can determine that it can also be applied in the subquery to vastly reduce the amount of rows selected.


**EXPLAIN PLAN**


This will show us the query plan. It is often the first thing you want to look at when a query is slow because it will show how much data ClickHouse is reading from disk. For example, imagine two MergeTree tables, each with 1 billion rows, one unsorted and one sorted:



```
CREATE TABLE numbers (number int) ENGINE = MergeTree ORDER BY tuple()
AS SELECT number FROM numbers(1e9)

CREATE TABLE numbers_sorted (number int) ENGINE = MergeTree ORDER BY number
AS SELECT number FROM numbers(1e9)

```

Query speeds will be very different:



```
SELECT sum(number) FROM numbers WHERE number <= 10

1 rows in set. Elapsed: 0.688 sec. Processed 1.00 billion rows, 4.00 GB (1.45 billion rows/s., 5.81 GB/s.)

SELECT sum(number) FROM numbers_sorted WHERE number <= 10

1 rows in set. Elapsed: 0.007 sec. Processed 8.19 thousand rows, 32.77 KB (1.23 million rows/s., 4.90 MB/s.)

```

Both queries need only 10 values to calculate their results, but while the first query has to read all 1 billion rows of the entire table, the second query reads only 8192 rows (the default size of the table’s `index_granularity`). We can see why this is by running the queries through EXPLAIN PLAIN (the output is cropped):



```
EXPLAIN PLAN actions = 1, indexes = 1 SELECT [...] numbers [...]
┌─explain────────────┐
│ [...]              |
│ ReadFromMergeTree  │
│ ReadType: Default  │
│ Parts: 1           │
│ Granules: 122071   │
└────────────────────┘


EXPLAIN PLAN actions = 1, indexes = 1 SELECT [...] numbers_sorted [...]


┌─explain───────────────────────────────┐
│ [...]                                 │
│ ReadFromMergeTree                     │
│ ReadType: Default                     │
│ Parts: 1                              │
│ Granules: 1                           │
│ Indexes:                              │
│   PrimaryKey                          │
│     Keys:                             │
│       number                          │
│     Condition: (number in (-Inf, 10]) │
│     Parts: 1/1                        │
│     Granules: 1/122071                │
└───────────────────────────────────────┘

```

Both queries return the same result (55, the sum of numbers from 1 to 10\), but the first query reads all 122071 granules (each granule contains 8192 rows so that comes out to the entire dataset of 1 billion rows) and the second query reads just the single granule that contains the ten numbers needed to compute the correct result.


Whenever you have a slow query, run it through EXPLAIN and you might quickly find out why it is taking so long and what to do about it.


## **Recordings to catch up on** [\#](/blog/clickhouse-newsletter-may-2022-explain-statement-query-optimization#recordings-to-catch-up-on)


These recordings are not as short as a TikTok video, but well worth your time if you’re a ClickHouse user. Feel free to watch at 2x speed to make it feel more like social media:


- The [ClickHouse 22\.4 release webinar](https://youtu.be/aFQs_zoYoXY). Do you know the answer to the brain teaser at [17](https://youtu.be/aFQs_zoYoXY?t=1033)?
- The San Francisco Bay Area meetup [talked about](https://youtu.be/Sg7I2GHYmtg) ClickHouse combinators, Hydrolix and streaming into ClickHouse from Apache Pulsar.


## **Reading Corner** [\#](/blog/clickhouse-newsletter-may-2022-explain-statement-query-optimization#reading-corner)


What we’ve been reading:


1. [10x improved response times, cheaper to operate, and 30% storage reduction](https://clickhouse.com/blog/10x-improved-response-times-cheaper-to-operate-and-30-storage-reduction-why-instabug-chose-clickhouse-for-apm/): Instabug explains why they chose ClickHouse as their database for APM data. It wasn’t a hard decision if we’re being honest!
2. [Two sizes fit most: PostgreSQL and Clickhouse](https://about.gitlab.com/blog/2022/04/29/two-sizes-fit-most-postgresql-and-clickhouse/): Gitlab wrote about ClickHouse and PostgreSQL and also [did some benchmarks](https://gitlab.com/gitlab-org/incubation-engineering/apm/apm/-/issues/4#results) in which ClickHouse looks very good!
3. [ClickHouse Keeper](https://pradeepchhetri.xyz/clickhousekeeper/): Somebody tested ClickHouse Keeper with Kafka, Solr and Mesos – and it all worked! Keeper is not just for ClickHouse.
4. [Introducing the official ClickHouse plugin for Grafana](https://grafana.com/blog/2022/05/05/introducing-the-official-clickhouse-plugin-for-grafana/): Read about the new plugin and see some of the beautiful dashboards you can create with it.
5. [ClickHouse Docs have a new look and feel!](https://clickhouse.com/blog/clickhouse-docs-have-a-new-look-and-feel/): Rich points to the new content in the revamped Clickhouse Documentation pages.
6. [New ClickHouse Adopters](https://clickhouse.com/docs/en/introduction/adopters/): Welcome [Better Stack](https://betterstack.com/), [PingCAP](https://github.com/pingcap/tiflash), [Synapse](https://synpse.net/), [Piwik](https://piwik.pro/), [Marfeel](https://www.marfeel.com/), [Datafold](https://www.datafold.com/), [Kaiko](https://www.kaiko.com/), and [Improvado](https://improvado.io/). Get yourself added as well!


Thanks for reading. We’ll see you next month!


The ClickHouse Team

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
