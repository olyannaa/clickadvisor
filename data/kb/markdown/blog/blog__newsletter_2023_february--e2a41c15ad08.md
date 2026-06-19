# ClickHouse Newsletter February 2023: A ‘Sample’ of What’s Happening in the Community


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter February 2023: A ‘Sample’ of What’s Happening in the Community

![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Dale McDiarmid](/authors/dale-mcdiarmid)Feb 15, 2023 · 13 minutes read![sampling.jpg](/uploads/sampling_860f8460e8.jpg)
How is it possible that it is 2023? And, not only that, already time for our second newsletter of the year! Compiling the reading list this month was particularly difficult as the amount of content was immense. If you aren’t keeping an eye on the [blog](https://clickhouse.com/blog), or our social media, you should be. The next weeks promise to be very exciting with webinars, in\-person events, and…of course…the upcoming release of 23\.2\.


If you’d like to continue receiving these updates, please [click here](https://discover.clickhouse.com/newsletter.html?utm_medium=email&utm_source=clickhouse&utm_campaign=newsletter) to confirm your email preferences.


## Upcoming Events [\#](/blog/newsletter_2023_february#upcoming-events)


Mark your calendars for the following events:


**ClickHouse v23\.02 Release Webinar**   

***When?*** Thursday, February 23 @ 9 AM PST / 6 PM CET   

***How do I join?*** Register [here](https://clickhouse.com/company/events/v23-2-release-webinar).


**ClickHouse Meetup \- Amsterdam**   

***When?*** Thursday, March 9 @ 6 PM CET   

***How do I join?*** Register [here](https://www.meetup.com/clickhouse-netherlands-user-group/events/291485868/).


**ClickHouse Meetup \- San Francisco**   

***When?*** Tuesday, March 14 @ 6 PM PST   

***How do I join?*** Register [here](https://www.meetup.com/clickhouse-silicon-valley-meetup-group/events/291490121/).


**ClickHouse Meetup \- Austin**   

***When?*** Thursday, March 16 @ 6 PM CET   

***How do I join?*** Register [here](https://www.meetup.com/clickhouse-austin-user-group/events/291486654/).


### Free upcoming training [\#](/blog/newsletter_2023_february#free-upcoming-training)


**ClickHouse Cloud Onboarding**   

***When?*** Tuesday, February 28 @ 8 AM PST   

***How do I join?*** Register [here](https://clickhouse.com/company/events/2023-02-28-clickhouse-onboarding-workshop).


**ClickHouse Workshop**   

***When?*** March 8 \+ 9, 2023 @ 8 AM PST  

***How do I join?*** Register [here](https://clickhouse.com/company/events/2023-03-08-clickhouse-workshop).


## ClickHouse v23\.1 [\#](/blog/newsletter_2023_february#clickhouse-v231)


As usual, the January release did not disappoint. A great start to the new year with a number of important features. Have a look at the [blog post](https://clickhouse.com/blog/clickhouse-release-23-01).


1. **Inverted Full Text Indices** \- In this release, we add experimental support for Inverted Indices in ClickHouse as a data\-skipping index. While this doesn't make ClickHouse a fully\-fledged search engine, it introduces some interesting possibilities for improving the performance of specific token\-based queries.
2. **Parameterized Views** \- Anyone who writes a lot of SQL learns to appreciate views quickly. They allow users to abstract away complex queries and expose them with table syntax. Until now, users could only create static views. With the 23\.1 release of ClickHouse, we can create dynamic views based on parameters passed at query time.
3. **Query Results Cache** \- To achieve maximum performance, analytical databases optimize every step of their internal data storage and processing pipeline. But the best kind of work performed by a database is work that is not done at all! In 23\.1, we introduce a new member to the ClickHouse family of Caches, the Query Result Cache!


It is worth spending time with the [recording](https://www.youtube.com/watch?v=zYSZXBnTMSE) of the live presentation and please upgrade unless you want to stay on a [Long Term Support (LTS) release](https://clickhouse.com/docs/en/faq/operations/production/#how-to-choose-between-clickhouse-releases).


## Query of the Month \- “New Context Forms From Old” [\#](/blog/newsletter_2023_february#query-of-the-month---new-context-forms-from-old)


It may be hard to believe, but sometimes it's possible to have so much data that it's impractical to query in the required response time… even when using ClickHouse. So what are your options once you’ve overcome the shock of a query response time where you had time to blink!?!?? Well, this is when we turn to the ClickHouse toolbox and pull out **SAMPLE BY**.


Often we don’t need precise answers, especially if your source data isn’t precise and approximate answers are sufficient. At PB or even TB scale, some businesses can accept some imprecision in exchange for a significant reduction in cost. Alternatively, strict latency requirements may be more important than complete accuracy. This is the spirit of SAMPLE BY.


Consider the Wikistat dataset. This provides us with a row for every page on Wikipedia per hour, with a count of the number of visits, from May 2015 to April 2022\. This is a decent\-sized dataset of around 425 billion rows and 15TB uncompressed. For those of you with some spare time, you can download and load it into ClickHouse by following the instructions [here](https://clickhouse.com/docs/en/getting-started/example-datasets/wikistat).


Suppose we wanted to compute the average number of page hits per month since 2015\. This needs a full table scan to compute the answer. On a 60\-core machine with no tuning, ClickHouse runs this query in under 5 minutes (limited by I/O):



```

SELECT
	month,
	avg(hits)
FROM wikistat
GROUP BY toStartOfMonth(time) AS month
ORDER BY month ASC

┌──────month─┬──────────avg(hits)─┐
│ 2015-05-01 │  3.617108988953329 │
│ 2015-06-01 │ 3.4978754072915894 │
│ 2015-07-01 │ 3.3329051255889595 │
│ 2015-08-01 │ 3.3877185707856237 │
│ 2015-09-01 │ 3.4814217901734508 │
…
│ 2022-11-01 │ 3.5633514296196567 │
│ 2022-12-01 │ 3.5317530490738696 │
│ 2023-01-01 │ 3.5829006605488463 │
│ 2023-02-01 │ 3.4581641236938476 │
└────────────┴────────────────────┘

94 rows in set. Elapsed: 278.166 sec. Processed 425.11 billion rows, 5.10 TB (1.53 billion rows/s., 18.34 GB/s.)


```

  

Even if we could speed this up with some tuning, it's unlikely we’d achieve performance gains sufficient to make this a sub\-minute query (without a projection e.g. `ORDER BY (cityHash64(path), time)`). But suppose we were content with an approximation for these values. We could naively try manual sampling by limiting to the first 1m rows.



```

 SELECT
   month,
   avg(hits)
   FROM ( SELECT time, hits FROM wikistat LIMIT 1000000 )
GROUP BY toStartOfMonth(time) AS month
ORDER BY month ASC
┌──────month─┬──────────avg(hits)─┐
│ 2015-05-01 │  2.359986873769416 │
│ 2015-06-01 │  2.292891439278604 │
│ 2015-07-01 │ 2.3796534376746785 │
│ 2015-08-01 │  2.229300091491308 │
...
│ 2022-01-01 │  2.395112662646779 │
│ 2022-02-01 │ 2.5044186449488826 │
│ 2022-03-01 │  2.168976377952756 │
│ 2022-04-01 │  2.182795698924731 │
└────────────┴────────────────────┘
84 rows in set. Elapsed: 0.290 sec. Processed 4.91 million rows, 58.87 MB (16.91 million rows/s., 202.88 MB/s.)


```

  

300s to 0\.2s is quite some speedup, but the results are clearly imprecise \- it's unlikely your manager would accept this for a degree of inaccuracy no matter the cost and latency saving! This can be attributed to the lack of randomness here, i.e., we simply use the first 1m rows.


To address this, ClickHouse offers native random sampling. This allows the user to only execute the query on a random fraction of data (a sample). This requires us to define a sampling key at table creation time, which is ideally a prefix of the primary key for optimal performance.



```

CREATE TABLE default.wikistat_sampled (
   `time` DateTime CODEC(Delta(4), ZSTD(3)),
   `project` LowCardinality(String),
   `subproject` LowCardinality(String),
   `path` String CODEC(ZSTD(3)),
   `hits` UInt64 CODEC(ZSTD(3))
) ENGINE = MergeTree ORDER BY (cityHash64(path), time) SAMPLE BY cityHash64(path)


```

  

A few key points here:
- The SAMPLE BY expression must be part of the primary key and return an integer \- hence we use the [cityHash64 function](https://clickhouse.com/docs/en/sql-reference/functions/hash-functions/#cityhash64). Ensure this is not an ascending numeric and randomly distributed in the space for random sampling \- tip: use a hash to randomize an auto incrementing integer.
- It should be uniformly distributed in the domain if its datatype. In this case, path is actually imperfect as it doesnt fully satisfy this property but is sufficient for our example. A better distributed value will result in better sampling and more accurate estimations.
- If optimal sampling performance is required, as in our case, the SAMPLE BY column should be the first element in the ORDER BY key. If you needed to optimize for matching on Path, you might place it 2nd or just use `cityHash64(path)=cityHash64(“value”)`. However you include it, ensure the low cardinality columns come first to allow the [use of the generic exclusion algorithm](https://clickhouse.com/docs/en/guides/improving-query-performance/sparse-primary-indexes/sparse-primary-indexes-cardinality).


We can now query, using only a fraction of our data \- expressing the sample as either an [absolute number of rows](https://clickhouse.com/docs/en/sql-reference/statements/select/sample/#sample-n) or as [a ratio from 0 to 1](https://clickhouse.com/docs/en/sql-reference/statements/select/sample/#sample-k). Below, we utilize 1% of the data with a value of 0\.01\.



```

SELECT
	month,
	avg(hits)
FROM wikistat_sampled SAMPLE 0.01
GROUP BY toStartOfMonth(time) AS month
ORDER BY month ASC


┌──────month─┬──────────avg(hits)─┐
│ 2015-05-01 │ 3.2243997815421004 │
│ 2015-06-01 │ 3.1547988082990828 │
│ 2015-07-01 │ 2.9813449766968887 │
│ 2015-08-01 │ 3.0210786179578397 │
│ 2015-09-01 │ 3.1277045971550463 │

│ 2022-11-01 │ 3.4243634422663884 │
│ 2022-12-01 │  3.415336905631455 │
│ 2023-01-01 │ 3.4066985347564027 │
│ 2023-02-01 │  3.254118466286919 │
└────────────┴────────────────────┘

94 rows in set. Elapsed: 6.272 sec. Processed 4.26 billion rows, 179.40 GB (679.64 million rows/s., 28.60 GB/s.)


```

  

Notice the accuracy of the results is reasonable, as well as the dramatic performance improvements. This sampling is entirely deterministic and consistent across tables for the same values. As a final note, the above is fine for an average, but for other calculations, such as a sum, we’d need to factor in the fact we’re only using a sample in any calculations. Consider the above query but computing hits per month:



```

SELECT
	month,
	sum(hits)
FROM wikistat
GROUP BY toStartOfMonth(time) AS month
ORDER BY month ASC

┌──────month─┬───sum(hits)─┐
│ 2015-05-01 │ 18505958911 │
│ 2015-06-01 │ 16325574540 │
│ 2015-07-01 │ 15541045668 │
│ 2015-08-01 │ 15763416762 │

│ 2022-10-01 │ 16041055714 │
│ 2022-11-01 │ 16195366347 │
│ 2022-12-01 │ 15383779088 │
│ 2023-01-01 │ 16631174276 │
│ 2023-02-01 │  5061601075 │
└────────────┴─────────────┘

94 rows in set. Elapsed: 289.147 sec. Processed 425.11 billion rows, 5.10 TB (1.47 billion rows/s., 17.64 GB/s.)


```

  


```

SELECT
	month,
	sum(hits) * 100
FROM wikistat_sampled
SAMPLE 1 / 100
GROUP BY toStartOfMonth(time) AS month
ORDER BY month ASC

┌──────month─┬─multiply(sum(hits), 100)─┐
│ 2015-05-01 │          	16546351200 │
│ 2015-06-01 │          	14769222800 │
│ 2015-07-01 │          	13938421600 │
│ 2015-08-01 │          	14087318900 │

│ 2022-10-01 │          	15483441000 │
│ 2022-11-01 │          	15595982500 │
│ 2022-12-01 │          	14908441500 │
│ 2023-01-01 │          	15842792600 │
│ 2023-02-01 │           	4772219400 │
└────────────┴──────────────────────────┘
94 rows in set. Elapsed: 6.184 sec. Processed 4.26 billion rows, 179.40 GB (689.32 million rows/s., 29.01 GB/s.)


```

  

## Reading List [\#](/blog/newsletter_2023_february#reading-list)


Some of our favorite reads from the past month include.


1. [ClickHouse Release 23\.1](https://clickhouse.com/blog/clickhouse-release-23-01) \- It's a new year! And, it is also a new release of ClickHouse. We are delighted to introduce the first release of the 23\.x series with 23\.1\.
2. [Introducing the ClickHouse Query Cache](https://clickhouse.com/blog/introduction-to-the-clickhouse-query-cache-and-design) \- The query cache is based on the idea that there are situations where it is okay to cache the result of expensive `SELECT` queries such that further executions of the same queries can be served directly from the cache.
3. [Using Aggregate Combinators in ClickHouse](https://clickhouse.com/blog/aggregate-functions-combinators-in-clickhouse-for-arrays-maps-and-states) \- Combinators allow extending and mixing aggregations to address a wide range of data structures. This capability enables us to adapt queries instead of tables to answer even the most complex questions.
4. [Analyzing AWS Flow Logs using ClickHouse](https://clickhouse.com/blog/analyzing-aws-fow-logs-using-clickhouse) \- Debugging security group issues, monitoring ingress and egress traffic, checking cross availability zone traffic all for the purpose of reducing your cloud spend. AWS VPC Flow Logs allow you to capture detailed information about the IP traffic going to and from network interfaces in your VPC.
5. [Introducing Inverted Indices in ClickHouse](https://clickhouse.com/blog/clickhouse-search-with-inverted-indices) \- After a long time in the making, ClickHouse v23\.1 shipped a highly anticipated feature \- experimental support for inverted indexes. A big "thank you!" to IBM, who developed and contributed the code for inverted indexes over the course of the last six months.
6. [ClickHouse and dbt \- A Gift from the Community](https://clickhouse.com/blog/clickhouse-dbt-project-introduction-and-webinar) \- As a company dedicated to the ethos of open\-source, it is important that we accept not only requests from the community but also features and new integrations. In this post, we explore dbt, the value it potentially brings when combined with ClickHouse, and a small tale of evolving support for more advanced capabilities.
7. [Using TTL to Manage Data Lifecycles in ClickHouse](https://clickhouse.com/blog/using-ttl-to-manage-data-lifecycles-in-clickhouse) \- If the data that you are analyzing in ClickHouse grows over time you may want to plan to move, remove, or summarize older data on a schedule. ClickHouse has a simple but powerful data lifecycle management tool configured with the `TTL` clause of DDL statements.
8. [An Introduction to Data Formats in ClickHouse](https://clickhouse.com/blog/data-formats-clickhouse-csv-tsv-parquet-native) \- Users new to ClickHouse are often surprised by the number of supported data formats, but sometimes need help identifying the best and easiest way to load their data. This post provides a brief overview of ClickHouse's extensive support for different formats and how to load your local files.
9. [ClickHouse Fiddle — A SQL Playground for ClickHouse](https://clickhouse.com/blog/clickhouse-fiddle-sql-playground) \- Sometimes we want to run SQL queries online to validate them, to share them with other people, or just because we are too lazy to install a database locally. Online SQL playgrounds can help us with this.
10. [Using Materialized Views in ClickHouse](https://clickhouse.com/blog/using-materialized-views-in-clickhouse) \- In the real world, data doesn’t only have to be stored, but processed as well. In this blog post, we explore materialized views and how they can be used in ClickHouse for accelerating queries as well as data transformation, filtering and routing tasks.


Thanks for reading, and we’ll see you next month.


The ClickHouse Team

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
