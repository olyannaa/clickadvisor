# ClickHouse Newsletter November 2022: The purifying effects of obfuscation


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter November 2022: The purifying effects of obfuscation

![photo-christoph-wurm[1].jpeg](/_next/image?url=%2Fuploads%2Fphoto_christoph_wurm_1_7af9415ecb.jpeg&w=96&q=75)[Christoph Wurm](/authors/christoph-wurm)Nov 10, 2022 · 11 minutes readDid you know ClickHouse is the world’s fastest tool for querying JSON files? [Here](https://clickhouse.com/blog/worlds-fastest-json-querying-tool-clickhouse-local) is the proof!


Also, have you ever wondered what the ClickHouse binary would look like as a picture? Well, we have. It’s big, it’s beautiful \- and gray? See it [here](https://youtu.be/sz9SES5-mdc?t=2319).


This month, read on for simplified pricing of ClickHouse Cloud, an entire “tour calendar” of upcoming events, new features in ClickHouse 22\.10, some modern dataset alchemy, and your regular dose of light reading material.


By the way, if you’re reading this on our website, did you know you can receive every monthly newsletter as an email in your inbox? Sign up [here](https://discover.clickhouse.com/newsletter.html).


## ClickHouse Cloud \- Simplified Pricing [\#](/blog/newsletter_2022_november#clickhouse-cloud---simplified-pricing)


Good news, we have simplified the pricing of our ClickHouse Cloud service. Now we only charge for two things: compute and storage. Head over to the [pricing page](https://clickhouse.com/pricing) to see the details. And for the next few days \- until Nov 15, 2022 \- we offer an additional $500 in credits.


On October 27, we broadcast our official launch webinar. We discussed why and how we built ClickHouse Cloud, showed a demo and answered your questions. Watch the recording [here](https://clickhouse.com/company/events/cloud-beta).


## Tour Calendar (aka “Upcoming Events”) [\#](/blog/newsletter_2022_november#tour-calendar-aka-upcoming-events)


The next few weeks are going to be full of ClickHouse events. We hope to meet many of you in person, either virtually or in person. Take a look at where you can find other Clickhouse users (and us):


**ClickHouse v22\.11 Release Webinar**


- ***When?*** Thursday, November 17 @ 9 am PST / 6 pm CEST
- ***How do I join?*** Register [here](https://clickhouse.com/company/events/v22-11-release-webinar).


**ClickHouse Cloud Onboarding Workshops**


- ***What?*** Hear from our team on how to take the first steps with ClickHouse Cloud. We’ll discuss the architecture, data modeling, views, data ingest and performance tuning \- with time for Q\&A at the end.
- ***When?*** Thursday, November 10 @ 10 am PST (AMER)


**Meetups** We’ll be holding a series of meetups with talks from ClickHouse users and experts. Come prepared with your curiosity and questions. Bring some colleagues and friends as well!


**Meetup Stockholm**


- ***When?*** Thursday, December 1 @ 6 pm (register [here](https://www.meetup.com/clickhouse-stockholm-user-group/events/289492084/))
- ***Speakers:*** RELEX, ClickHouse


**Meetup Berlin**


- ***When?*** Monday, December 5 @ 6 pm (register [here](https://www.meetup.com/clickhouse-berlin-user-group/events/289311596/))
- ***Speakers:*** Deutsche Bank, BENOCS, ClickHouse


**Meetup New York City**


- ***When?*** Tuesday, December 6 @ 6 pm (register [here](https://www.meetup.com/clickhouse-new-york-user-group/events/289403909/))
- ***Speakers:*** Bloomberg, Disney, Prequel, Rokt, ClickHouse


**Meetup Tel Aviv**


- ***When?*** Monday, January 16 @ 6 pm (register [here](https://www.meetup.com/clickhouse-tel-aviv-user-group/events/289599423/))
- ***Speakers:*** To be announced


## ClickHouse v22\.10 [\#](/blog/newsletter_2022_november#clickhouse-v2210)


This past month, ClickHouse received its 100,000th commit! You can look for it with `git log`, but first, let’s take a look at the new features in the October release:


1. [Backup to S3](https://clickhouse.com/docs/en/manage/backups/#configuring-backuprestore-to-use-an-s3-endpoint) ClickHouse can now back up your data to an S3 bucket. You can back up (and restore) individual tables and dictionaries or an entire database. Both full and incremental backups are supported.
2. [Reset setting](https://github.com/ClickHouse/ClickHouse/pull/42187) You can now reset a setting to its default value using `SET setting_name = DEFAULT`.
3. [Always merge old parts](https://github.com/ClickHouse/ClickHouse/pull/42423) You can specify that parts will be merged after a certain amount of time using `min_age_to_force_merge_seconds`. This way, you can ensure that after a set amount of time, data will be in the least number of files, improving query performance. It also helps when using the [`FINAL` modifier](https://clickhouse.com/docs/en/sql-reference/statements/select/from/#final-modifier) together with `do_not_merge_across_partitions_select_final` since ClickHouse will not have to merge these files at query time.
4. [Too many parts](https://github.com/ClickHouse/ClickHouse/pull/42002) We have relaxed the too many parts check. By default, ClickHouse will throw an exception if the number of active parts in a partition exceeds 300 (configurable with `parts_to_throw_insert`). With this change, no error will be thrown if the average part size is greater than 10 GiB, allowing very large partitions (100\+ TB). It is configurable with the new setting `max_avg_part_size_for_too_many_parts` (default: 10 GiB).
5. [Random data](https://github.com/ClickHouse/ClickHouse/pull/42411) To help you generate random data that is more realistic than a uniform distribution, there are now 11 new `rand*` functions. For example, `randNormal` and `randExponential`.


And one preview feature:


1. **Kafka Connect Sink** We’ve started developing an official Kafka Connect sink for ClickHouse. It will support exactly\-once semantics without any third\-party dependencies. You can find the current source code [here](https://github.com/ClickHouse/clickhouse-kafka-connect). If you use ClickHouse with Kafka, give it a try and give us some feedback!


Take a look at the [release webinar slides](https://presentations.clickhouse.com/release_22.10/) and the [recording](https://youtu.be/sz9SES5-mdc), and please upgrade unless you want to stay on a Long Term Support (LTS) release.


## Query of the Month: The purifying effects of obfuscation [\#](/blog/newsletter_2022_november#query-of-the-month-the-purifying-effects-of-obfuscation)


Useful datasets are like large diamonds: hard to find but very valuable. And when you have some, you typically lock them in a secure space \- in a vault or in a database. Unfortunately, the best datasets often contain sensitive information about customers, proprietary data, or trade secrets. And so they only ever live in production databases, and even for internal development and testing purposes, other data has to be used, often synthetically generated test data.


However, synthetic data is often flawed. It usually does not accurately represent what the real data is like. Characteristics like the cardinality of dimensions, the range and distribution of numeric values, and the proportion of empty values will often differ significantly from the actual data. This is a major problem for developing and testing queries that scan a large amount of data to arrive at a result \- exactly what ClickHouse is good at.


For example, for a query that contains `GROUP BY dimension`, there is a big difference in memory usage and performance between `dimension` having a cardinality in the hundreds or billions. A `GROUP BY` will be calculated using a hash map with one key for each distinct value. A few hundred key\-value pairs will easily fit into memory, and the query will be lightning fast \- whereas for billions of values, the hash map will have to be offloaded to disk resulting in a much slower query, or the query might even fail.


So how do we develop and test with data that is close to the actual data in characteristics (such as the cardinality of values in columns) \- but is not the actual data?


One answer is obfuscation. And ClickHouse actually ships with a built\-in obfuscator, either `clickhouse-obfuscator` (on Linux) or `clickhouse obfuscator` (on Mac). Docs are [here](https://clickhouse.com/docs/en/operations/utilities/clickhouse-obfuscator/).


The ClickHouse Obfuscator will read a dataset as its input and produce as its output a dataset that is very similar in characteristics but won’t contain the same actual values. Let’s look at how it works using the [UK Property Price Paid](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid/) dataset.


First, a look at some high\-level characteristics:



```

SELECT count(), avg(price), max(price) FROM uk_price_paid

┌──count()─┬──────avg(price)─┬─max(price)─┐
│ 26763022 │ 208231.24594106 │  932540400 │
└──────────┴─────────────────┴────────────┘


```


As we can see, the total number of real estate transactions in the dataset is 26\.7 million, with an average price of about £208,000 and a maximum price ever paid of £932 million.
Let’s obfuscate this:



```
clickhouse obfuscator --structure "price Int64, date UInt16, postcode1 String, postcode2 String, type String, is_new UInt8, duration String, addr1 String, addr2 String, street String, locality String, town String, district String, county String, category String" --input-format Parquet --output-format Parquet --seed "${RANDOM}${RANDOM}${RANDOM}${RANDOM}" < uk_price_paid.parquet > obfuscated.parquet

```

Notice how we convert one Parquet file into another \- the obfuscator works on non\-ClickHouse data!
Let’s check what the same characteristics of the obfuscated dataset look like:



```

SELECT count(), avg(price), max(price) FROM file('obfuscated.parquet')
 
┌──count()─┬─────────avg(price)─┬─max(price)─┐
│ 26763022 │ 223585.90603467726 │  994963827 │
└──────────┴────────────────────┴────────────┘


```


The number of rows is the same \- but the average and maximum prices have changed slightly.
Even the distribution of prices has stayed about the same. For example, the distribution of prices below £1M:



```

SELECT band, q1.count AS real, q2.count AS obfuscated FROM
(SELECT floor(price, -5) band, count() count FROM file('uk_price_paid.parquet') GROUP BY band) q1
LEFT JOIN
(SELECT floor(price, -5) band, count() count FROM file('obfuscated.parquet') GROUP BY band) q2
USING band WHERE band < 1e6 ORDER BY band
 
┌───band─┬────real─┬─obfuscated─┐
│      0 │ 8728237 │    8803178 │
│ 100000 │ 9277684 │    7936176 │
│ 200000 │ 4422328 │    5148196 │
│ 300000 │ 1944389 │    1906225 │
│ 400000 │  975584 │    1493438 │
│ 500000 │  465029 │     361164 │
│ 600000 │  291360 │     221633 │
│ 700000 │  178879 │     249621 │
│ 800000 │  117307 │     113644 │
│ 900000 │   77406 │     166402 │
└────────┴─────────┴────────────┘


```


It’s worth noting that the obfuscator does not encrypt or hash the data \- so not all information is lost (on purpose, to preserve the characteristics). Therefore it is not automatically safe to share an obfuscated dataset with just anybody. But it should go a long way toward making sharing easier and should be especially useful for internal use, for example, for development and testing of an application.


Have fun with the ClickHouse Obfuscator \- and maybe you can free up a useful dataset or two.


## Reading Corner [\#](/blog/newsletter_2022_november#reading-corner)


What we’ve been reading:


1. [**100x Faster: GraphQL Hive migration from Elasticsearch to ClickHouse**](https://clickhouse.com/blog/100x-faster-graphql-hive-migration-from-elasticsearch-to-clickhouse) The Guild tested InfluxDB, TimescaleDB and ClickHouse to replace their existing Elasticsearch setup. Unsurprisingly (at least to us), ClickHouse emerged as the clear winner \- with query times of 100ms compared to 3 seconds for TimescaleDB and 5 seconds for InfluxDB. By switching from Elasticsearch to ClickHouse, The Guild can now ingest billions instead of only millions of events.


![average_read_time.png](/uploads/average_read_time_1e59bdec8f.png)
2. [**13 ClickHouse "Deadly Sins"**](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse) and how to avoid them If you are using ClickHouse, then this blog post is for you. Just before Halloween, we wrote up 13 common issues that ClickHouse users run into \- and how to avoid them. Have a read, there are probably a few you have run into yourself (and maybe one or two you are about to).
3. [**The world’s fastest tool for querying JSON files**](https://clickhouse.com/blog/worlds-fastest-json-querying-tool-clickhouse-local) \- ClickHouse takes on general\-purpose tools like Spark SQL \- as well as specialized tools like OctoSQL and SPyQL \- and comes out ahead.
4. [**Sending Kubernetes logs To ClickHouse with Fluent Bit**](https://clickhouse.com/blog/kubernetes-logs-to-clickhouse-fluent-bit) and [**Sending Nginx logs to ClickHouse**](https://clickhouse.com/blog/nginx-logs-to-clickhouse-fluent-bit) with Fluent Bit A two\-part series on using the Fluent Bit log processor and forwarder to ingest logs into ClickHouse. You should give putting logs into ClickHouse a try \- the data size on disk is likely to be much lower, and dashboards much faster than what you have today!
5. [**Visualizing Data with ClickHouse \- Part 3 \- Metabase**](https://clickhouse.com/blog/visualizing-data-with-metabase) \- Part 3 of our series on visualizing data in ClickHouse using different user interfaces. Part 3 covers Metabase, while Part 1 covers Grafana and Part 2 Superset.
6. [**Optimizing star\-schema queries with IN queries and denormalization**](https://medium.com/datadenys/optimizing-star-schema-queries-with-in-queries-and-denormalization-cc281bbe19a5) \- Some neat tricks here on speeding up ClickHouse queries combining data from multiple tables. For example, using `IN` instead of `JOIN` reduced query time from 19 seconds to 130 milliseconds.
7. [**In\-depth: ClickHouse vs PostgreSQL**](https://posthog.com/blog/clickhouse-vs-postgres) \- Like many other companies, Posthog started with PostgreSQL and later migrated to ClickHouse. Here they go into some detail on their thinking and the benefits they achieved. Also, lots of cute hedgehogs.


Thanks for reading, and we’ll see you next month.


*The ClickHouse Team*

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
