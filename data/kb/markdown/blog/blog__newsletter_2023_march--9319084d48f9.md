# ClickHouse Newsletter March 2023: Contributing to ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter March 2023: Contributing to ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Mar 23, 2023 · 9 minutes readHow is it approaching spring already? We’ve been as busy as always at ClickHouse, writing new content, hosting events, releasing software and…of course…sharing as much of the internals with you as we can. We’ve reordered this month’s newsletter to get into the query of the month more quickly, but the customary reading list and upcoming events appear at the bottom.


By the way, if you’re reading this on our website, did you know you can receive every monthly newsletter as an email in your inbox? [Sign up here](https://discover.clickhouse.com/newsletter.html?utm_medium=email&utm_source=clickhouse&utm_campaign=newsletter).


## ClickHouse v23\.2 [\#](/blog/newsletter_2023_march#clickhouse-v232)


- 18 new features.
- 30 performance optimisations.
- 43 bug fixes.


Multiple SQL language features and extended integrations support. But, as always, there are a few headline items worth checking out. You can read about all the features in detail in the [v23\.2 blog post](https://clickhouse.com/blog/clickhouse-release-23-02) and, if you are interested,, don’t forget to sign\-up for the live [v23\.3 release presentation](https://clickhouse.com/company/events/v23-3-release-webinar) (Q\&A welcome).


**Multi\-stage PREWHERE**


The `PREWHERE`  clause has been a feature in ClickHouse since the first OSS release. This optimization is designed to reduce the number of rows a query is required to read, and prior to 22\.2 used, a 2\-step execution process.


**Support for Apache Iceberg**


ClickHouse currently supports reading v1 (v2 support is coming soon!) of the Iceberg format via the `iceberg` table function and `Iceberg` table engine. This table format is increasingly popular and has rapidly become an industry standard for managing data in data lakes. Iceberg brings SQL table\-like functionality to files in a data lake in an open and accessible manner.


**Support for Correlation Matrices**


In 23\.2, we add support for computing correlation matrices. As a reminder, a correlation matrix is a table that contains the correlation coefficient between all possible values in a table. This represents an easy way to summarise a large dataset and identify columns that are either strongly or negatively correlated.


## Query of the Month \- “Contributing to ClickHouse” [\#](/blog/newsletter_2023_march#query-of-the-month---contributing-to-clickhouse)


Real\-time analytics is an important, and perhaps often misunderstood, concept. Real\-time can imply at the point of ingestion, at the point of transformation, at the point of application interaction, or…importantly…at the point of interest.   

  

We found ourselves interested, in the last week, about the number of contributors (over time) to the various ClickHouse repositories. And, also the number of unique users per month. The query itself turned out to be quite interesting.   

  

This is a little challenging as we want the cumulative unique users, not just the unique number per month. To achieve this, we first generate an array of the unique contributors grouped by month (`uniq_users`) via the aggregate function `groupArrayDistinct` (see our [recent blog post](https://clickhouse.com/blog/aggregate-functions-combinators-in-clickhouse-for-arrays-maps-and-states) on aggregate functions). A window function in turn groups these monthly arrays and produces an array of the distinct contributors so far for each month. Finally an outer query identifies the unique number of values in each column.


The query itself is fairly direct and shown below (and also available for perusing on [ClickHouse Play)](https://sql.clickhouse.com?query_id=KIZPJXDYG1QB6DQDFSAVIE).



```

SELECT
    month,
    arrayUniq(cul_users) AS cul_users,
    arrayUniq(uniq_users) AS uniq_users
FROM
(
    SELECT
        month,
        groupArrayDistinctArray(uniq_users) OVER (ORDER BY month ASC) AS cul_users,
        groupArrayDistinct(actor_login) AS uniq_users
    FROM default.github_events
    WHERE (repo_name LIKE 'ClickHouse%') AND (event_type = 'PullRequestEvent')
    GROUP BY toStartOfMonth(created_at) AS month
    ORDER BY month ASC
)

┌──────month─┬─cul_users─┬─uniq_users─┐
│ 2018-08-01 │         2 │          2 │
│ 2018-10-01 │         4 │          2 │
│ 2018-11-01 │         4 │          2 │
│ 2018-12-01 │         7 │          5 │
│ 2019-02-01 │         8 │          2 │
│ 2019-03-01 │         9 │          1 │
│ 2019-05-01 │        10 │          2 │
│ 2019-06-01 │        10 │          2 │
│ 2019-07-01 │        12 │          3 │
│ 2019-08-01 │        15 │          5 │
│ 2019-09-01 │        38 │         31 │
│ 2019-10-01 │        75 │         60 │
│ 2019-11-01 │       114 │         77 │
│ 2019-12-01 │       145 │         81 │
…
│ 2022-06-01 │      1118 │        122 │
│ 2022-07-01 │      1157 │        121 │
│ 2022-08-01 │      1208 │        120 │
│ 2022-09-01 │      1239 │        118 │
│ 2022-10-01 │      1280 │        131 │
│ 2022-11-01 │      1317 │        133 │
│ 2022-12-01 │      1344 │        119 │
│ 2023-01-01 │      1374 │        123 │
│ 2023-02-01 │      1405 │        142 │
│ 2023-03-01 │      1441 │        124 │
└────────────┴───────────┴────────────┘


53 rows in set. Elapsed: 0.032 sec. Processed 202.50 thousand rows, 8.18 MB (6.25 million rows/s., 252.65 MB/s.)
[✎](https://sql.clickhouse.com?query_id=KIZPJXDYG1QB6DQDFSAVIE)

```

  

This was the first effort and not as synatically succinct as possible \- although still impressively fast. After consulting and obtaining some enlightenment around state functions, we realised these could be used at query time for passing states from a subquery \- not just for storing [intermediate states from materialized views](https://clickhouse.com/blog/using-materialized-views-in-clickhouse). The query below uses the [`uniqState`](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/combinators#-state) function to return “a sketch” of unique contributors per month. We then use a simple window function which performs a cumulative merge of these sketches using the [`uniqMerge`](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/combinators#-state) function.



```

WITH states AS
    (
        SELECT
            month,
            uniqState(actor_login) AS uniq_users
        FROM default.github_events
        WHERE (repo_name LIKE 'ClickHouse%') AND (event_type = 'PullRequestEvent')
        GROUP BY toStartOfMonth(created_at) AS month
        ORDER BY month ASC
    )
SELECT
    month,
    uniqMerge(uniq_users) OVER (ORDER BY month ASC) AS cul_users
FROM states

53 rows in set. Elapsed: 0.024 sec. Processed 181.30 thousand rows, 8.32 MB (7.47 million rows/s., 343.05 MB/s.)
[✎](https://sql.clickhouse.com?query_id=7YB4Q9HMD22ZV7VQWBFREA)

```

  

So array functions, aggregate combinators and state functions all in 2 queries…oh and we saved 8ms…it all adds up.


## Reading List [\#](/blog/newsletter_2023_march#reading-list)


Some of our favorite reads that you may have missed include:


1. [Building ClickHouse Cloud](https://clickhouse.com/blog/building-clickhouse-cloud-from-scratch-in-a-year) \- Have you ever wondered what it takes to build a serverless software as a service (SaaS) offering in under a year? In this blog post, we will describe how we built ClickHouse Cloud – a managed service on top of one of the most popular online analytical processing (OLAP) databases in the world – from the ground up.
2. [Women Who Inspire Us: The Women Pioneers in ClickHouse Community and Company](https://clickhouse.com/blog/women-who-inspire-us-the-women-pioneers-in-clickhouse-community-and-company) \- International Women's Day presents an opportunity to acknowledge and appreciate the countless professional women who are shaping the world in diverse fields, ranging from executives and entrepreneurs to scientists and activists. This day offers a chance to reflect on the progress that has been made towards gender parity, and the work that still remains to be done. It is also about honoring the inspiring women who are breaking barriers and making a difference in their respective industries.
3. [Fintech Leader Juspay Analyzes Over 50 Million Daily Payment Transactions in Real\-Time with ClickHouse](https://clickhouse.com/blog/juspay-analyzes-payment-transactions-in-real-time-with-clickhouse) \- Juspay, an Indian fintech company, uses ClickHouse to power A/B testing and monitoring for its end\-to\-end payment solutions and real\-time merchant dashboards. With over 50 million daily transactions for clients such as Amazon, Google, and Vodafone, ClickHouse was chosen for its ability to handle large volumes of data.
4. [Handling Updates and Deletes in ClickHouse](https://clickhouse.com/blog/handling-updates-and-deletes-in-clickhouse) \- As the world’s fastest database for real\-time analytics, many ClickHouse workloads involve large amounts of data that is written once and not frequently modified (for example, telemetry events generated by IOT devices or customer clicks generated by an e\-commerce website). While these are typically immutable, additional data sets critical to providing context during analytics (e.g., lookup tables with information based on device or customer ID) may require modifications.


In our December NYC meetup, we were excited to have three amazing presentations that showcased the diverse applications of ClickHouse. We couldn't resist sharing them with you again!


1. [Managing Traffic Spikes at Disney\+](https://clickhouse.com/blog/nyc-meetup-report-high-speed-content-distribution-analytics-for-streaming-platforms): Learn how Disney\+ handles surges in traffic on their content distribution network by harnessing the power of ClickHouse, ensuring a smooth streaming experience for millions of users worldwide.
2. [Personalized Real\-Time Offers with Rokt](https://clickhouse.com/blog/nyc-meetup-report-real-time-slicing-and-dicing-reporting-with-clickhouse): Discover how Rokt leverages ClickHouse to power their dynamic, real\-time offers and create tailored experiences for their customers.
3. [Bloomberg's Real\-Time Stock Market Analysis](https://clickhouse.com/blog/nyc-meetup-report-large-scale-financial-market-analytics-with-clickhouse): Gain insight into how Bloomberg utilizes ClickHouse to perform real\-time analysis of the entire stock market, enabling them to make data\-driven decisions and stay ahead in the financial world.


## Upcoming Events [\#](/blog/newsletter_2023_march#upcoming-events)


Mark your calendars for the following events:


**ClickHouse v23\.03 Release Webinar**   

***When?*** Thursday, March 30 @ 9 AM PST / 6 PM CET   

***How do I join?*** Register [here](https://clickhouse.com/company/events/v23-3-release-webinar).


**ClickHouse Cloud Onboarding**   

***When?*** Wednesday, April 5 @ 8 AM PDT   

***How do I join?*** Register [here](https://clickhouse.com/company/events/clickhouse-onboarding-workshop).


**ClickHouse Spring Meetup in Manhattan**   

***When?*** Wednesday, April 26 @ 5 PM EDT   

***How do I join?*** Register [here](https://www.meetup.com/clickhouse-new-york-user-group/events/292362015/).


Thanks for reading, and we’ll see you next month!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
