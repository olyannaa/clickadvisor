# ClickHouse Newsletter August 2022: Airlines are maybe not that bad


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter August 2022: Airlines are maybe not that bad

![photo-christoph-wurm[1].jpeg](/_next/image?url=%2Fuploads%2Fphoto_christoph_wurm_1_7af9415ecb.jpeg&w=96&q=75)[Christoph Wurm](/authors/christoph-wurm)Aug 11, 2022 · 11 minutes read*Did you find this page by clicking the "View in Browser" link in an email? Well, that's unfortunate. You can find the [December Newsletter](/blog/newsletter_2022_december) just by clicking the link.*


At ClickHouse, we are very happy that in\-person meetups are finally back. It’s true that sometimes they coincide with 38 C (100 F) heat \- like our meetup in London the past month. But hey, that’s why they’re in the evening, plus there’s pizza. Join a [ClickHouse meetup](https://www.meetup.com/pro/clickhouse) group close by if you can!


We also have a new webpage! It’s much snazzier than the old one, take a look: [https://clickhouse.com/](https://clickhouse.com)


Read on to learn about our new benchmark, let us get you up to speed on what’s new in ClickHouse 22\.7, find out if airlines are really as bad as they say, and fill your reading list with some summer material.


By the way, if you’re reading this on our website, did you know you can receive every monthly newsletter as an email in your inbox as well? Sign up [here](https://discover.clickhouse.com/newsletter.html).


**Upcoming Events**


**ClickHouse v22\.8 Release Webinar**


- ***When?*** Thursday, August 18 @ 9 am PST / 6 pm CEST
- ***How do I join?*** Register [here](https://clickhouse.com/company/events/v22-8-release-webinar).


**ClickBench \- Benchmark for analytical databases**
Did you know that we’re obsessed with performance at ClickHouse? In our [changelog](https://clickhouse.com/docs/en/whats-new/changelog/), we have an entire section “Performance Improvement” for every release, and it’s often a very long section. That’s why so [many](https://clickhouse.com/docs/en/about-us/adopters/) companies use ClickHouse for [use cases](https://clickhouse.com/customer-stories) requiring fast queries on a lot of data. It’s also why our T\-shirts have this text on the back:



```
12 rows in set.
Elapsed: 0.920 sec.
Processed: 107.43 billion rows.
214.86 GB (116.80 billion rows/s, 233.61 GB/s)

```

To continue to track ClickHouse performance and compare it to other systems, we launched ClickBench, our benchmark for analytical databases. The dataset is based on a real\-world web analytics workload, the kind that ClickHouse is often used for. Many other use cases have similar data and similar queries, for example, network traffic, structured logs, and event data.


Read up on the background and methodology [here](https://github.com/ClickHouse/ClickBench/) and see the current results at <https://benchmark.clickhouse.com/>.


By the way, did you know [the fastest way to parse JSON is not to parse JSON](https://youtu.be/JBomQk4Icjo?t=3284)?


**ClickHouse v22\.7**


As usual, our monthly release is full of features:


1. **Positional arguments** are now turned on by default, so you can use `SELECT ... ORDER BY 1, 2`. But as we’re discovering ourselves, old habits die hard!
2. [**Deprecate Ordinary**](https://github.com/ClickHouse/ClickHouse/pull/38335) Only long\-time users will know this: the Ordinary database engine and old \*MergeTree syntax are now deprecated. If you have any old databases that have survived countless upgrades, now is the time to change them.
3. [**Expressions in window functions**](https://github.com/ClickHouse/ClickHouse/pull/37848) are now supported.
4. **Not one, but two new join algorithms** \- [`direct`](https://github.com/ClickHouse/ClickHouse/pull/35363) and [`full_sorting_merge`](https://github.com/ClickHouse/ClickHouse/pull/35796), give them a try! More to come.
5. [**MongoDB table function**](https://github.com/ClickHouse/ClickHouse/pull/37213) to query MongoDB from ClickHouse. Even better, to read data from MongoDB and write it to ClickHouse for better query performance! Especially aggregations should be much, much faster in ClickHouse.
6. [**Additional filters**](https://github.com/ClickHouse/ClickHouse/pull/38475) to transparently apply filter conditions when reading from a table (`additional_table_filters`) or on a result set (`additional_result_filter`).
7. [**Simple charts**](https://github.com/ClickHouse/ClickHouse/pull/38197) The built\-in Play UI (e.g. [`http://localhost:8123/play`](http://localhost:8123/play)) can now draw some basic charts.
8. [**HTTP support**](https://github.com/ClickHouse/clickhouse-go/issues/597) for Go The official [clickhouse\-go](https://github.com/ClickHouse/clickhouse-go) driver now supports HTTP.
9. [**ClickHouse \+ Superset**](https://github.com/ClickHouse/clickhouse-connect) We have a new Superset connector, [clickhouse\-connect](https://github.com/ClickHouse/clickhouse-connect). Please give it a try and report any issues.


Take a look at the [release webinar slides](https://presentations.clickhouse.com/release_22.7/), the [recording](https://youtu.be/IOJyo14BpTQ) and please upgrade (unless you want to stay on an LTS release).


**Query of the Month: Airlines are maybe not that bad**


Common wisdom has it that airlines are terrible and only getting worse. Extra charges for everything from bags to in\-flight water, seats that have less legroom every year \- and flight schedules that are so tightly packaged they lead to endless delays. The first two are certainly true, but what about the third? We can investigate with ClickHouse!


One of the example datasets in the ClickHouse documentation is [OnTime](https://clickhouse.com/docs/en/getting-started/example-datasets/ontime). It contains over 200 million records of many commercial flights in the US dating back to 1987\. Each record contains information about a flight including the date and time of the flight, departure and arrival airports, flight number, and much more. Importantly for us, there are fields showing how delayed the flight was (if at all) compared to its scheduled times.


We want to check if flight schedules are too tight and many planes get caught up in delays that then get worse throughout the day. For that, we need to isolate individual planes. Luckily, the dataset contains the tail number uniquely identifying a particular aircraft. Let’s play around with a few queries to get to know the data:



```
-- Total number of unique aircraft in the dataset
SELECT count(DISTINCT Tail_Number) FROM ontime

-- Number of unique tail numbers by year
SELECT Year, count(DISTINCT Tail_Number) count FROM ontime GROUP BY Year
ORDER BY count DESC

```

The first query shows that there are 18,531 distinct tail numbers in the dataset. Note, the total number of actual aircraft is going to be different \- planes can and do change tail numbers, for example, when changing carriers or countries of registration. This is also likely the reason why the second query shows an all\-time high of 7,768 unique tail numbers in the year 2002, much higher than the second\-highest value of 5,892 in 2019\. 2002 was a particularly bad year for the aviation industry and many planes likely changed owners.


The second query also shows that prior to 1995 the dataset does not contain any tail numbers. So we should limit our queries to just those rows that have them. We might think that `WHERE Tail_Number != ''` would work, but it does not:



```
SELECT DISTINCT Tail_Number FROM ontime WHERE Tail_Number != '' ORDER BY Tail_Number
-- Top results: #N/A, '144DA, (null), -N037M

SELECT DISTINCT Tail_Number FROM ontime WHERE Tail_Number != '' ORDER BY Tail_Number DESC
-- Top results: �NKNO�, XXXXXX, Unknow, UNKNOW 

```

Lots of values that do not look like valid tail numbers! Instead of filtering out what we don’t want we should just filter for what we want, i.e. valid tail numbers. Luckily, tail numbers have a uniform structure: Letters representing the country of registration, some numbers and more letters often representing the airline. The letters at the end are optional. So we can select only rows with valid tail numbers like this:



```
SELECT DISTINCT Tail_Number FROM ontime WHERE match(Tail_Number,
'^[A-Z]+[0-9]+[A-Z0-9]*$') ORDER BY Tail_Number
-- Top results: A367NW, D942DN, M67153, etc. - all valid

```

The kind of simple queries we’ve run so far are very important when using a new dataset to learn its contents and limitations \- no dataset is perfect, and the sooner you work out where the trouble is the better.


Before you read on for the last step, head over to the documentation for the `sequenceMatch` function [here](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/parametric-functions/#sequencematchpatterntimestamp-cond1-cond2-). It’s an ingenious function that allows you to check whether an ordered set of rows contains rows that match a sequence of conditions. It is often used to identify user behavior, for example, you could use it to identify all users of an online shop that first searched for a particular word or phrase, then went on to look at a product detail page, put it in their shopping cart and bought it. You could check sub\-sequences of the main sequence to see which step had the biggest drop\-off.


`sequenceMatch` is one of 1261 functions currently built into ClickHouse (`SELECT count() FROM system.functions`). Some are well\-known SQL functions (count, sum, avg, etc.) but many are specific to ClickHouse and I bet you don’t know all of them! It took me over six months to notice `sequenceMatch`. Have a look around the list of functions sometimes, chances are good you’ll learn something new.


Back to our dataset. We can use `sequenceMatch` to check how the delays of aircraft evolve during a day \- do they tend to get worse or do they get better? In the first query, we check how many planes that are delayed by more than 60 minutes subsequently become delayed by more than 90 minutes:



```
WITH (
	DepDelayMinutes > 60 AS delay,
	DepDelayMinutes > 90 AS longer_delay
)
SELECT sum(c) FROM (
	SELECT count() c FROM ontime
	WHERE match(Tail_Number, '^[A-Z]+[0-9]+[A-Z0-9]*$')
	GROUP BY FlightDate, Tail_Number
	HAVING sequenceMatch('(?1)(?2)')(toDateTime(DepTime), delay, longer_delay)
)

```

The result: 6,884,070\. What about the delay getting shorter, to less than 30 minutes:



```
WITH (
   DepDelayMinutes > 60 AS delay,
   DepDelayMinutes < 30 AS shorter_delay
)
SELECT sum(c) from (
   SELECT count() c FROM ontime
   WHERE match(Tail_Number, '^[A-Z]+[0-9]+[A-Z0-9]*$')
   GROUP BY FlightDate, Tail_Number
   HAVING sequenceMatch('(?1)(?2)')(toDateTime(DepTime), delay, shorter_delay)
)

```

The result here: 7,264,056\. Seems quite a few planes do actually catch up with their schedule over a day. Maybe not everything in the airline industry is as bad as we think. Then again, delays have been getting worse over the years, average delays today are about twice as long as they were in the 90s:



```
 SELECT Year, avg(DepDelayMinutes) FROM ontime GROUP BY Year ORDER BY Year DESC

```

Let’s end it here for today. And next time you’re stuck at an airport, fire up ClickHouse and explore!


**Reading Corner**


What we’ve been reading:


1. [DeepL’s journey with ClickHouse](https://clickhouse.com/blog/deepls-journey-with-clickhouse) DeepL brought in ClickHouse, Kafka and Metabase for a shift to data\-driven development of the world’s best machine translator.
2. [NANO Corp: From experimentation to production, the journey to Supercolumn](https://clickhouse.com/blog/from-experimentation-to-production-the-journey-to-supercolumn) Read how NANO Corp stumbled into ClickHouse after being frustrated with all other alternatives and stayed because it was the perfect fit for their use case of monitoring gigabit networks in real time.
3. [Fast, Feature Rich and Mutable : ClickHouse Powers Darwinium's Security and Fraud Analytics Use Cases](https://clickhouse.com/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases) Digital risk platform Darwinium chose ClickHouse for high\-throughput and low\-latency writes into wide tables of thousands of columns.
4. [ClickHouse and the open source modern data stack](https://blog.luabase.com/clickhouse-for-data-nerds/) Blockchain analytics provider Luabase chose ClickHouse for its speed and walks through some neat queries including pivoting data.
5. [New ClickHouse Adopters:](https://clickhouse.com/docs/en/introduction/adopters/) Welcome open source feature flagging and experimentation platform [GrowthBook](https://www.growthbook.io/). Get yourself added as well!


Thanks for reading. We’ll see you next month!


The ClickHouse Team

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
