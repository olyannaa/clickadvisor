# ClickHouse Newsletter March 2022: There’s a window function for that!


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter March 2022: There’s a window function for that!

![photo-christoph-wurm[1].jpeg](/_next/image?url=%2Fuploads%2Fphoto_christoph_wurm_1_7af9415ecb.jpeg&w=96&q=75)[Christoph Wurm](/authors/christoph-wurm)Mar 7, 2022 · 8 minutes readWelcome to our March newsletter, a monthly roundup of the latest ClickHouse goodness. Below you will find new exciting features we released, recent meetup and webinar recordings, some neat queries using window functions and a few recommended reads.


## **ClickHouse v22\.2** [\#](/blog/clickhouse-newsletter-march-2022-theres-a-window-function-for-that#clickhouse-v222)


We released ClickHouse 22\.2, the newest and greatest version of your favorite database. Highlights include:


- **[Projections](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree/#projections)** are production ready and enabled by default. They allow you to store part of a table in a subdirectory of the original table, often using a different sorting key or aggregating the original data – similar to materialized views but without all the overhead. Their usage is refreshingly simple: Queries will be automatically analyzed and redirected to the projection if less data has to be read there to produce the same result. Almost like magic!
- **Custom deduplication on insert** – a [new setting](https://clickhouse.com/docs/en/operations/settings/settings/#insert_deduplication_token) `[insert_deduplication_token]` allows you to specify a custom token (any string) that is used to determine if a block has already been inserted. If it has, then any subsequent blocks with the same token are discarded. Any insert statement creates a block but large inserts are divided into multiple blocks of about 1 million rows (controlled by [max\_insert\_block\_size](https://clickhouse.com/docs/en/operations/settings/settings/#settings-max_insert_block_size)). This makes it easier to implement exactly\-once semantics in ClickHouse. Note: By default, ClickHouse will already deduplicate inserted data blocks that are identical (consist of the same rows in the same order). This new setting gives you more control over the process if you need it.
- **Default table engine** – You can now set a default table engine so you no longer have to specify one when creating a table. For example:



```
SET default_table_engine = 'MergeTree'
CREATE TABLE table1 (x int PRIMAY KEY (x))


```

- **[Ephemeral columns](https://clickhouse.com/docs/en/sql-reference/statements/create/table/#ephemeral)** can be used at insert time to calculate other columns but are not stored themselves.
- **[Text classification](https://github.com/ClickHouse/ClickHouse/pull/33314)** – Experimental functions for detecting language, character set, tonality and programming language were added. For example:



```
SET allow_experimental_nlp_functions = 1
SELECT detectLanguage('Ich bin ein Berliner')
// returns 'de'


```

- **[Implicit casting in dictGet\* functions](https://github.com/ClickHouse/ClickHouse/pull/33672)**, now you can simplify your queries! For example, when you have a dictionary with UInt32 as the primary key you can access it using any of these:



```
dictGetOrNull(dict, attr, 1)
dictGetOrNull(dict, attr, '1')
dictGetOrNull(dict, attr, 1.0)
dictGetOrNull(dict, attr, toUInt8(1))
dictGetOrNull(dict, attr, toInt256(1))

```

For more details head over to the [release blog post](https://clickhouse.com/blog/clickhouse-22-2-released/) and the [changelog](https://clickhouse.com/docs/en/whats-new/changelog/#clickhouse-release-v22-2-2022-02-17).


## Meetups \& Webinars [\#](/blog/clickhouse-newsletter-march-2022-theres-a-window-function-for-that#meetups--webinars)


The last few weeks have seen a number of meetups and webinars in ClickHouse land. Check out the recordings (at 2x speed if you like, we won’t judge you):


- [Virtual Meetup with Contentsquare](https://youtu.be/bTz--qJpQHs), where we learned about how they use ClickHouse to power their experience analytics platform. It’s an impressive journey that started with moving from Elasticsearch to ClickHouse to be 11x cheaper (with 6x more data) and 10x faster! We also heard about the ClickHouse Proxy (Chproxy) project and Alexey’s favorite ClickHouse features in 2021 and 2022\. *Highlight: Listen in at [1:20](https://youtu.be/bTz--qJpQHs?t=4811) on our plans for a new JSON data type.*
- Learn about the new features we released in the [v22\.02 Release Webinar](https://youtu.be/6EG1gwhSTPg) including upcoming performance improvements for running ClickHouse on top of S3 at [42](https://youtu.be/6EG1gwhSTPg?t=2525) (the performance numbers are very impressive, if we may say so!).
- The San Francisco Bay Area meetup [had guest speakers](https://youtu.be/6mvngWsOd30) from Materialize and FastNetMon.


Upcoming webinars:


**ClickHouse v22\.3 Release Webinar**


- **When?** Thursday, March 17 @ 8 am PDT / 4 pm GMT  

[Add to your calendar](https://calendar.google.com/calendar/u/0/r/eventedit?dates=20220317T160000Z/20220317T170000Z&text=ClickHouse+v22.3+Release+Webinar&location=https://zoom.us/j/91955953263?pwd%3DSXBKWW5ETkNMc1dmVWUxTUJKNm5hUT09&details=Please+click+the+link+below+to+join+the+webinar:%0D%0Ahttps://zoom.us/j/91955953263?pwd%3DSXBKWW5ETkNMc1dmVWUxTUJKNm5hUT09%0D%0A%0D%0APasscode:+139285%0D%0A%0D%0AOr+One+tap+mobile+:+%0D%0A++++US:+%2B12532158782,,91955953263%23,,,,*139285%23++or+%2B13462487799,,91955953263%23,,,,*139285%23+%0D%0A%0D%0AOr+Telephone:%0D%0A++++Dial(for+higher+quality,+dial+a+number+based+on+your+current+location):%0D%0A++++++++US:+%2B1+253+215+8782++or+%2B1+346+248+7799++or+%2B1+669+900+9128++or+%2B1+301+715+8592++or+%2B1+312+626+6799++or+%2B1+646+558+8656+%0D%0A%0D%0AWebinar+ID:+919+5595+3263%0D%0APasscode:+139285%0D%0A++++International+numbers+available:+https://zoom.us/u/asrDyM28Q&sf=true)


## Query of the Month: There’s a window function for that! [\#](/blog/clickhouse-newsletter-march-2022-theres-a-window-function-for-that#query-of-the-month-theres-a-window-function-for-that)


Did you know that ClickHouse has window functions? It’s a relatively recent (early 2021\) feature but very powerful. Let’s go on a whirlwind tour of what’s possible that used to be much harder before. Note: We will use the [UK Price Paid dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid/) of all property transactions in the UK in the last few decades, so feel free to reproduce the queries!


**Query 1: Compare with cohort average**



```
SELECT avg(price) OVER(PARTITION BY postcode1) AS postcode_avg, *
FROM uk_price_paid
WHERE type = 'flat'
ORDER BY price DESC

```

This query will show the most expensive flats / apartments ever sold in the UK but in addition will show the average prices in their postcodes as the first column. So now we can see who’s really overpaying!


**Query 2: When was this property sold previously?**



```
SELECT
lagInFrame(date) OVER (PARTITION BY postcode1, postcode2, addr1, addr2 ORDER BY date ASC) AS previous_date,
lagInFrame(price) OVER (PARTITION BY postcode1, postcode2, addr1, addr2 ORDER BY date ASC) AS previous_price,
* FROM uk_price_paid

```

With a time series dataset like this we will often want to see the previous record for a particular entity. We can do this with `lagInFrame`. If we use `first_value` we would get the first time the property was sold instead (the dataset only goes back to 1995\).


**Query 3: Sorting with window functions**


You can also sort by window functions. For example, this query shows the most expensive sub\-postcodes within the most expensive postcode (in the UK, postcodes have two parts):



```
SELECT DISTINCT
    postcode1,
    postcode2,
    avg(price) OVER (PARTITION BY postcode1, postcode2) AS avg_price
FROM uk_price_paid
WHERE type = 'flat'
ORDER BY
    avg(price) OVER (PARTITION BY postcode1) DESC,
    avg_price DESC

```

Note the two window functions used in the `ORDER BY` clause. For those of you that are familiar with London you won’t be surprised that this query comes up with the W1S postcode at the edge of Mayfair and Soho.


## Reading Corner [\#](/blog/clickhouse-newsletter-march-2022-theres-a-window-function-for-that#reading-corner)


What we’ve been reading:


1. [How we scale out our ClickHouse cluster](https://engineering.contentsquare.com/2022/scaling-out-clickhouse-cluster/) by our friends at Contentsquare. They have a neat “ClickHouse resharding\-cooker” combining `clickhouse-backup` and `clickhouse-copier`. Well worth a read if you’re running a ClickHouse cluster!
2. [Opensee: Analyzing Terabytes of Financial Data a Day With ClickHouse](https://clickhouse.com/blog/en/2022/opensee-analyzing-terabytes-of-financial-data-a-day-with-clickhouse/) by our friends at financial analytics company Opensee. They’ve been using ClickHouse for years to analyze financial institutions’ risk profiles.
3. [ClickHouse 22\.2 release blog post](https://clickhouse.com/blog/clickhouse-22-2-released/) – read up on the most recent ClickHouse release and exciting new features including production\-ready projections, custom deduplication and flexible memory limits.


[New ClickHouse Adopters](https://clickhouse.com/docs/en/introduction/adopters/): Welcome [Gigasheet](https://www.gigasheet.co/). Get yourself added as well!


Thanks for reading. We’ll see you next month!


The ClickHouse Team


Photo by [Fernando Venzano](https://unsplash.com/@fernandovenzano?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
