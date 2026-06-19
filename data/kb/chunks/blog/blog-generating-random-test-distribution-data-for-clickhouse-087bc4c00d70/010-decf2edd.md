---
source: blog
url: https://clickhouse.com/docs/en/sql-reference/table-functions/generate/
topic: generating-random-data-in-clickhouse
ch_version_introduced: '9.9'
last_updated: '2026-06-12'
chunk_index: 10
total_chunks_in_doc: 10
---

= 2) ) ENGINE = MergeTree ORDER BY dt ``` Let’s populate this table with 10m events: ``` INSERT INTO click_events SELECT (parseDateTimeBestEffortOrNull('12:00') - toIntervalHour(randNormal(0, 3))) - toIntervalDay(number % 30), 'Click', ['fail', 'success'][randBernoulli(0.9) + 1] FROM numbers(10000000) ```

```
0 rows in set. Elapsed: 3.726 sec. Processed 10.01 million rows, 80.06 MB (2.69 million rows/s., 21.49 MB/s.)

```

We’ve used `randBernoulli()` with a 90% success probability, so we’ll have `success` value for the `status` column 9 out of 10 times. We’ve used `randNormal()` to generate the distribution of the events. Let’s visualize that data with the following query:

```
  
```
1SELECT
2    dt,
3    count(*) AS c,
4    bar(c, 0, 100000)
5FROM random.click_events
6GROUP BY dt
7ORDER BY dt ASC
```


```

```
722 rows in set. Elapsed: 0.045 sec. Processed 10.00 million rows, 40.00 MB (224.41 million rows/s., 897.64 MB/s.)

```

This will yield the following output:

![click_events_distribution.png](/uploads/large_click_events_distribution_f070075669.png)
## Summary [\#](/blog/generating-random-test-distribution-data-for-clickhouse#summary)

Using powerful random functions available since 22\.10, we have shown how to generate data of a realistic nature. This data can be used to help test your solutions on close\-to\-the\-real\-world data instead of irrelevant generated sets.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
