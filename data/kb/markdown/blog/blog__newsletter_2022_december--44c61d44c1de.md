# ClickHouse Newsletter December 2022: Project all your troubles away


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter December 2022: Project all your troubles away

![photo-christoph-wurm[1].jpeg](/_next/image?url=%2Fuploads%2Fphoto_christoph_wurm_1_7af9415ecb.jpeg&w=96&q=75)[Christoph Wurm](/authors/christoph-wurm)Dec 13, 2022 · 9 minutes read![projector.jpg](/uploads/projector_0f1ea9ef72.jpg)
We’re all excited to share that the official managed service for ClickHouse, ClickHouse Cloud, is now generally available and production ready. Give it a spin if you’re looking to focus on using ClickHouse rather than managing it. As always, we are here to help you!


Keep reading to read about the new features in ClickHouse Cloud, upcoming events in the coming days and weeks, what is new in ClickHouse 22\.11 and how projections can help you speed up queries without changing your queries.


And take a look at our holiday reading list. If you read only the most technical articles, we have you covered with [this](https://clickhouse.com/blog/clickhouse-just-in-time-compiler-jit) 25\-page blog post about JIT compilation in ClickHouse!


By the way, if you’re reading this on our website, did you know you can receive every monthly newsletter as an email in your inbox? Sign up [here](https://discover.clickhouse.com/newsletter.html).


\#\#ClickHouse Cloud is now Generally Available


As usual, we like to deliver things quickly. So here it is, the GA release of our ClickHouse Cloud managed service, just in time for Christmas. We’ve added a number of features including SOC 2 Type II compliance, uptime status and SLAs, availability in the AWS Marketplace, a lower priced development tier, an interactive SQL console, free [ClickHouse Academy](https://clickhouse.com/learn) training and we’ve enabled the PostgreSQL and MySQL engines, dictionaries and SQL UDFs.


If you’re just getting started with ClickHouse or need something to host your non\-production development, staging and QA take a look at our new and affordable Development tier where prices can be as low as $50 per month.


Take a look at our [pricing](https://clickhouse.com/pricing) here, read the [release blog post](https://clickhouse.com/blog/clickhouse-cloud-generally-available) and sign up for a free trial at <https://clickhouse.cloud/signUp>.


**Upcoming Events**


Mark your calendars for the following virtual and in\-person events:


**6\-hour ClickHouse Workshop (2 x 3 hours)**
  
**What?** If you’re new to ClickHouse, this is for you. In two 3\-hour sessions on two days we’ll take you through all the basics, from modeling data to query optimization
  
 **When?**


1. Register [here](https://clickhouse.com/company/events/clickhouse-workshop) for Wednesday, Dec 14 @ 8 am PST / 5 pm CET and Thursday, Dec 15 @ 8 am PST / 5 pm CET.
2. Register [here](https://clickhouse.com/company/events/2023-01-04-clickhouse-workshop) for Wednesday, Jan 4 @ 9 am PST and Thursday, Jan 5 @ 9 am PST.
3. Register [here](https://clickhouse.com/company/events/2023-01-18-clickhouse-workshop) for Wednesday, Jan 18 @ 10 am GMT and Thursday, Jan 19 @ 10 am GMT


**ClickHouse v22\.12 Release Webinar**


- ***When?*** Thursday, December 15 @ 9 am PST / 6 pm CET
- ***How do I join?*** Register [here](https://clickhouse.com/company/events/v22-12-release-webinar).


**Meetup Tel Aviv**


- **When?** Monday, January 16 @ 6 pm (register [here](https://www.meetup.com/clickhouse-tel-aviv-user-group/events/289599423/))
- ***Speakers:*** ServiceNow, Contentsquare, CHEQ, ClickHouse


**Meetup Seattle**


- **When?** Wednesday, January 18 @ 11 am (register [here](https://www.meetup.com/clickhouse-seattle-user-group/events/290310025/))
- ***Speakers:*** To be announced


\#\#ClickHouse v22\.11


Lots of new features in our regular monthly release \- this month accompanied by a [dedicated blog post](https://clickhouse.com/blog/clickhouse-release-22-11).


1. **[Composite time intervals](https://github.com/ClickHouse/ClickHouse/pull/42195)** You can now combine different intervals in one go, for example `INTERVAL '1 HOUR 1 MINUTE 1 SECOND'` or `SELECT '2023-01-30'::Date + (INTERVAL 1 MONTH - INTERVAL 2 DAY)`. Can you guess the result of the second statement?
2. **[Recursive globs in paths](https://github.com/ClickHouse/ClickHouse/pull/42376)** Use `**` for recursive directory traversal in a filesystem or in S3\. For example, to read all Parquet files in an S3 bucket use `FROM s3('https://mybucket.s3.us-east-1.amazonaws.com/**/*.parquet')`
3. **[Retry keeper during inserts](https://github.com/ClickHouse/ClickHouse/pull/42607)** Long\-running inserts can sometimes fail when the keeper connection to ClickHouse Keeper or ZooKeeper is temporarily lost. We have a new setting `insert_keeper_max_retries` that enables retries for keeper operations to prevent this from failing the entire insert query.
4. **Hudi and DeltaLake** [table engines](https://github.com/ClickHouse/ClickHouse/pull/41054) and [table functions](https://github.com/ClickHouse/ClickHouse/pull/43080) to query and ingest data from “data lakes”.
5. **[Readonly S3 disks](https://github.com/ClickHouse/ClickHouse/pull/42628)** You can attach a MergeTree table from S3 directly in readonly mode. This is an experimental feature.
6. **[Object (JSON) inside types](https://github.com/ClickHouse/ClickHouse/pull/36969)** The experimental Object (also known as JSON) type can now be wrapped in other types, e.g. `Array(JSON)`.


Take a look at the [release webinar slides](https://presentations.clickhouse.com/release_22.11/) and the [recording](https://youtu.be/LR-fckOOaFo), and please upgrade unless you want to stay on a Long Term Support (LTS) release.


## Query of the Month: Project all your troubles away [\#](/blog/newsletter_2022_december#query-of-the-month-project-all-your-troubles-away)


Today we’re going to take a look at a very useful ClickHouse feature that you’re probably not using enough: Projections.


Projections are a more convenient alternative to materialized views when all the data is from the same table. Materialized view queries can contain subqueries or dictionary lookups so the destination table will contain data from multiple sources. Like a materialized view, a projection is defined as a query, but the result of this query is saved in the same table (but hidden).


When ClickHouse receives a query for data in a table with a projection, it will first analyze whether it should use the original data or the projection data to answer the query. Whichever requires less data to be read and processed will be chosen.


As an example, consider a simple table containing metric names and values:



```
CREATE TABLE metrics
(
	timestamp DateTime64 CODEC(Delta, Default),
	name LowCardinality(String),
	value Float64
) ENGINE = MergeTree()
ORDER BY (name, timestamp)

```

Take a note of two optimizations to the data types:


1. Instead of storing the `timestamp` as is we use delta encoding where only the difference between one value and the next are stored. We expect most values to be quite similar (same year, month, day, hour, etc.) so this will reduce the storage required for this column by a lot.
2. Similarly, instead of storing the names of our metrics as they are, we use the `LowCardinality` dictionary encoding to store a map of names and pointers to where they occur in the data. We only expect a limited number of unique metrics so this will also reduce storage by a lot.


Notice also how we order the data by metric name first and then by timestamp. This will make queries that look for individual metrics very fast. The following query finds the latest temperature reading:



```
SELECT name, argMax(value, timestamp) val_max FROM metrics
WHERE symbol = 'TEMP' GROUP BY symbol
 
┌─name───┬─val_max─┐
│ TEMP   │     179 │
└────────┴─────────┘
 
1 row in set. Elapsed: 0.009 sec. Processed 73.73 thousand rows, 1.38 MB (8.01 million rows/s., 150.32 MB/s.)

```

Requesting the latest values for all metrics is 100x slower:



```
SELECT name, argMax(value, timestamp) val_max
FROM metrics GROUP BY symbol
255 rows in set. Elapsed: 0.902 sec. Processed 220.01 million rows, 6.08 GB (259.38 million rows/s., 6.74 GB/s.)

```

To speed up this query we can add a projection that always stores the latest value for a metric



```
ALTER TABLE metrics ADD PROJECTION latest_values
(SELECT argMax(value, timestamp) GROUP BY name)

```

And to make the data available immediately we can materialize the projection like this:



```
ALTER TABLE metrics MATERIALIZE PROJECTION latest_values
SETTINGS mutations_sync = 1

```

Now let’s run the same query again:



```
SELECT name, argMax(value, timestamp) val_max
FROM metrics GROUP BY symbol
255 rows in set. Elapsed: 0.007 sec. Processed 255 rows, 156.13 KB (1.42 million rows/s., 84.33 MB/s.)

```

Getting the latest value for all metrics is faster than getting the latest value for a single metric was! All we had to do was add a projection. No need to change our query or our table structure even one bit.


Give projections a try! We bet there are some that will be useful on your data.


## Holiday Reading List [\#](/blog/newsletter_2022_december#holiday-reading-list)


Some reading material for you:


1. [ClickHouse Cloud is now Generally Available](https://clickhouse.com/blog/clickhouse-cloud-generally-available) A very exciting time for ClickHouse users, the official ClickHouse managed service is generally available and fully production ready. Read all about it in this post.
2. [User\-defined functions in ClickHouse Cloud](https://clickhouse.com/blog/user-defined-functions-clickhouse-udfs) A refresher on UDFs from our team now that they are available in ClickHouse Cloud.
3. [Using dictionaries to accelerate queries](https://clickhouse.com/blog/faster-queries-dictionaries-clickhouse) An in\-depth explainer with examples of how to use dictionaries to speed up your queries in ClickHouse.
4. [JIT in ClickHouse](https://clickhouse.com/blog/clickhouse-just-in-time-compiler-jit) One of the most technical posts we’ve read in a while, our own Maksim Kita dives deeply into JIT compilation and how it’s implemented in ClickHouse.
5. [Window and array functions for Git commit sequences](https://clickhouse.com/blog/clickhouse-window-array-functions-git-commits) Some really good visual explainers of window and array functions in this blog post on analyzing Git commits.
6. [How We Use ClickHouse to Analyze Trends Across Millions of Builds](https://www.buildbuddy.io/blog/clickhouse-build-trends/) BuildBuddy moved their Trends page from MySQL to ClickHouse \- one query improved from taking 24 minutes (!) to 0\.317s in ClickHouse!
7. [Using partitions in Clickhouse](https://medium.com/datadenys/using-partitions-in-clickhouse-3ea0decb89c4) A quick primer on using partitions and how they can speed up queries. Check out the other posts [here](https://medium.com/datadenys) as well!


Thanks for reading, and we’ll see you next year.


The ClickHouse Team

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
