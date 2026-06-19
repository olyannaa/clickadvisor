# ClickHouse Newsletter January 2023: Better Safe Than Sorry


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter January 2023: Better Safe Than Sorry

![photo-christoph-wurm[1].jpeg](/_next/image?url=%2Fuploads%2Fphoto_christoph_wurm_1_7af9415ecb.jpeg&w=96&q=75)[Christoph Wurm](/authors/christoph-wurm)Jan 19, 2023 · 8 minutes read![202301-newsletter.png](/uploads/202301_newsletter_be26926eb6.png)
Happy New Year! Like many of you, we at ClickHouse took some time off and are using January to catch up and plan. To help you think about what you can do with ClickHouse in 2023, have a look at our joint webinars with dbt Labs and Grafana this month, the new features we released in version 22\.12 just before the holidays, how to use encryption in ClickHouse and a reading list to get you started into the year.


By the way, if you’re reading this on our website, did you know you can receive every monthly newsletter as an email in your inbox? [Sign up here](https://discover.clickhouse.com/newsletter.html?utm_source=clickhouse&utm_medium=email&utm_campaign=newsletter-202301).


## Upcoming Events [\#](/blog/newsletter_2023_january#upcoming-events)


Mark your calendars for the following virtual events:


**Webinar: Using dbt to Transform Data in ClickHouse**  

**When?** Tuesday, January 24 @ 2 pm GMT / 3 pm CET  

**How do I join?** [Register here](https://clickhouse.com/company/events/2023-01-24-dbt-clickhouse-webinar?utm_source=clickhouse&utm_medium=email&utm_campaign=newsletter-202301)  

**Speakers:** dbt Labs, Datricks, ClickHouse


**ClickHouse v23\.01 Release Webinar**  

**When?** Wednesday, January 25 @ 9 am PST / 6 pm CET  

**How do I join?** [Register here](https://clickhouse.com/company/events/v23-01-release-webinar?utm_source=clickhouse&utm_medium=email&utm_campaign=newsletter-202301)


**Webinar: Real\-time SQL analytics at scale: A story of open\-source GitHub activity using ClickHouse and Grafana**  

**When?** Thursday, January 26 @ 6 pm CET / 9 am PST  

**How do I join?** [Register here](https://grafana.com/go/webinar/clickhouse-and-grafana/?src=partner-clickhouse-email)  

**Speakers:** Grafana, ClickHouse


**Webinar: ClickHouse Cloud Onboarding**  

**When?** Thursday, January 26 @ 1 pm PST  

**How do I join?** [Register here](https://clickhouse.com/company/events/2023-01-26-clickhouse-onboarding-workshop?utm_source=clickhouse&utm_medium=email&utm_campaign=newsletter-202301)


## ClickHouse v22\.12 [\#](/blog/newsletter_2023_january#clickhouse-v2212)


There was a lot of goodness in our December release. Have a look at the [blog post](https://clickhouse.com/blog/clickhouse-release-22-12) as well:


1. **[Grace hash join](https://github.com/ClickHouse/ClickHouse/pull/38191)** A new join type that splits the to\-be\-joined tables into buckets and joins those buckets one by one, vastly reducing memory usage (at the cost of slower speed). Give it a try, and also take a look at all the other join algorithms ClickHouse supports [here](https://clickhouse.com/docs/en/operations/settings/settings#settings-join_algorithm).
2. **[Async insert deduplication](https://github.com/ClickHouse/ClickHouse/pull/43304)** Asynchronous inserts are now deduplicated, so if you send the same data twice ClickHouse will only accept one.
3. **[Password complexity](https://github.com/ClickHouse/ClickHouse/pull/43719)** ClickHouse can now enforce password complexity rules for user passwords \- how long a password has to be and whether it has to contain any specific character types. If you’re creating users in ClickHouse, you should probably configure this, so people don’t just set “asdf”.
4. **[GROUP BY ALL](https://github.com/ClickHouse/ClickHouse/issues/37631)** Grouping by ALL will group by every column in a SELECT statement that is not part of an aggregation. A handy shorthand, so you don’t have to specify them manually.
5. **[Numbers with underscores](https://github.com/ClickHouse/ClickHouse/pull/43925)** Sometimes it’s just easier to specify `1_000_000` rather than `1000000` (if you’re like me, you’re pausing shortly after typing the first three zeros to make sure you’re getting it right). Though in this particular case, you can also use `1e6`.
6. **[Async reading from MergeTree](https://github.com/ClickHouse/ClickHouse/pull/43260)** On slower disks, especially remote stores like object storage (S3, etc.), reading data can take some time. Therefore it makes sense to send many parallel read requests to reduce the overall time it takes to gather all data for a query. New settings allow specifying how many parallel requests ClickHouse will make, allowing you to speed up some queries significantly, especially on smaller machines. This is especially useful when using ClickHouse Cloud, which is based on object storage.


Take a look at the [release webinar slides](https://presentations.clickhouse.com/release_22.12/) and the [recording](https://youtu.be/sREupr6uc2k), and please upgrade unless you want to stay on a [Long Term Support (LTS) release](https://clickhouse.com/docs/en/faq/operations/production/#how-to-choose-between-clickhouse-releases). If you are using [ClickHouse Cloud](https://clickhouse.com/cloud), you are already using the new release.


## Query of the Month: Better safe than sorry [\#](/blog/newsletter_2023_january#query-of-the-month-better-safe-than-sorry)


In this section, we like to explore lesser\-known but potentially very useful features in ClickHouse. One such feature is built\-in encryption and decryption.
Let’s say you have a customer table that contains potentially sensitive information such as customer addresses:



```
CREATE TABLE customers
(
   id String,
   address String
)
ENGINE = MergeTree
ORDER BY id

```

Instead of storing the addresses in plaintext, you can encrypt them like this:



```
INSERT INTO customers
SELECT 1, encrypt('aes-128-cbc', '35 Highcombe, London,SE7 7HT', 'donotusethisword')

```

The resulting data will be unreadable:



```
SELECT * FROM customers FORMAT Values


('1','��kg`�\0�\0"��́Xf����ĭ\n0�Ą.\f�')

```

Unless you have the correct key:



```
SELECT id, decrypt('aes-128-cbc', address, 'donotusethisword') 
FROM customers FORMAT Values


('1','35 Highcombe, London,SE7 7HT')

```

Ah, but I hear you say that if certain users shouldn’t be able to see some columns, it’s better to `REVOKE` their access to those columns. You’re certainly right, but maybe they should have access to some values but not others, depending on whether they have access to the key.
By default, if decryption fails, ClickHouse will throw an exception. If this is sometimes expected (when the user has a valid key for some values but not others), you can use `tryDecrypt` instead, which will return `NULL` for the values that cannot be decrypted and allow the query to continue.



```
INSERT INTO customers
SELECT 2, encrypt('aes-128-cbc', '31 Richmond Court, Ellesmere Port,CH65 9EA', 'usesomeotherword')


SELECT id, tryDecrypt('aes-128-cbc', address, 'usesomeotherword') address
FROM customers WHERE address IS NOT NULL


('2','31 Richmond Court, Ellesmere Port,CH65 9EA')

```

Native database encryption is a straightforward and low\-cost way to improve data security. It is not as secure as using an external key management system, but those are not always available or easy to set up.


## New Year Reading List [\#](/blog/newsletter_2023_january#new-year-reading-list)


Some reading material to start the year with.


1. [ClickHouse Release 22\.12](https://clickhouse.com/blog/clickhouse-release-22-12) The release blog post for our awesome pre\-holiday Christmas release. If you’re using joins, you should look into the new grace hash join!
2. [Announcing a new official ClickHouse Kafka Connector](https://clickhouse.com/blog/kafka-connect-connector-clickhouse-with-exactly-once) The official Kafka Connect Sink for ClickHouse with exactly\-once delivery semantics is now in beta. Give it a try!
3. [Optimizing ClickHouse with Schemas and Codecs](https://clickhouse.com/blog/optimize-clickhouse-codecs-compression-schema) With a bit of work on your table definitions, you can often significantly reduce storage and speed up queries at the same time. Have a look at how we did it here.
4. [Super charging your ClickHouse queries](https://clickhouse.com/blog/clickhouse-faster-queries-with-projections-and-primary-indexes) Another way to increase query speed is to use projections and specify good sorting keys (primary indexes). Walk through an example with us here.
5. [System Tables and a window into the internals of ClickHouse](https://clickhouse.com/blog/clickhouse-debugging-issues-with-system-tables) Your first port of call when monitoring ClickHouse should be the system tables. There are a lot of them, and they give you detailed information about almost everything ClickHouse is doing. Read our primer here.
6. Essential monitoring queries: [Part 1 (INSERT)](https://clickhouse.com/blog/monitoring-troubleshooting-insert-queries-clickhouse) and [Part 2 (SELECT)](https://clickhouse.com/blog/monitoring-troubleshooting-select-queries-clickhouse). These articles will help you get started monitoring the two most important query types, inserts and selects.
7. [Building an Observability Solution with ClickHouse in 2023 \- Part 1 \- Logs](https://clickhouse.com/blog/storing-log-data-in-clickhouse-fluent-bit-vector-open-telemetry) More and more companies are choosing ClickHouse to store their observability data. In this first part of a longer series, we show you how to use ClickHouse for logs.
8. [Extracting, converting, and querying data in local files using clickhouse\-local](https://clickhouse.com/blog/extracting-converting-querying-local-files-with-sql-clickhouse-local) Don’t want to run a database but still want to use ClickHouse? Use headless ClickHouse (clickhouse\-local)! It’s one of the best tools out there to query data anywhere, including in local files. We think every data engineer should have it installed.
9. [Generating random data in ClickHouse](https://clickhouse.com/blog/generating-random-test-distribution-data-for-clickhouse) Ever needed to generate some random data? We had to many times, so ClickHouse has a lot of functionality built in to help with that. Have a read and outsource your data generation to ClickHouse.
10. [HIFI’s migration from BigQuery to ClickHouse](https://clickhouse.com/blog/hifis-migration-from-bigquery-to-clickhouse) HIFI is providing financial analytics to music creators worldwide. Initially using BigQuery, they were unhappy with its per\-query pricing, so they switched to ClickHouse.


Thanks for reading, and we’ll see you next month.  

The ClickHouse Team

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
