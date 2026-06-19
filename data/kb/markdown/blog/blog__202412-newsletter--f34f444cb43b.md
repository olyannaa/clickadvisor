# December 2024 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# December 2024 newsletter

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Dec 19, 2024 · 7 minutes readWelcome to the December ClickHouse newsletter, our last one for 2024! This month we’ve got a guide to query optimization, a real\-world example of SQL\-based observability, product announcements around Amazon’s re\-Invent conference, the Postgres CDC connector for ClickPipes moving into Private Preview, and more.


 


## Inside this issue [\#](/blog/202412-newsletter#inside-this-issue)


- [Upcoming events](https://clickhouse.com/blog/202412-newsletter#upcoming-events)
- [Featured community member](https://clickhouse.com/blog/202412-newsletter#featured-community-member)
- [24\.11 Release](https://clickhouse.com/blog/202412-newsletter#2411-release)
- [A simple guide to ClickHouse query optimization: part 1](https://clickhouse.com/blog/202412-newsletter#a-simple-guide-to-clickhouse-query-optimization-part-1)
- [Building SQL\-based Observability With ClickHouse and Grafana](https://clickhouse.com/blog/202412-newsletter#building-sql-based-observability-with-clickhouse-and-grafana)
- [Postgres CDC connector for ClickPipes is now in Private Preview](https://clickhouse.com/blog/202412-newsletter#postgres-cdc-connector-for-clickpipes-is-now-in-private-preview)
- [ClickHouse Decoded: Making Sense of Fast Data](https://clickhouse.com/blog/202412-newsletter#clickhouse-decoded-making-sense-of-fast-data)
- [ClickHouse at AWS re:Invent 2024](https://clickhouse.com/blog/202412-newsletter#clickhouse-at-aws-reinvent-2024)
- [Video corner](https://clickhouse.com/blog/202412-newsletter#video-corner)
- [Quick reads](https://clickhouse.com/blog/202412-newsletter#quick-reads)
- [ClickHouse User Conference](https://clickhouse.com/blog/202412-newsletter#clickhouse-user-conference)
- [Post of the month](https://clickhouse.com/blog/202412-newsletter#post-of-the-month)


 


## Upcoming events [\#](/blog/202412-newsletter#upcoming-events)


**Global events**


- [Release call 24\.12](https://clickhouse.com/company/events/v24-12-community-release-call?utm_source=clickhouse&utm_medium=email&utm_campaign=202412-newsletter) \- Dec 19
- [Release call 25\.1](https://clickhouse.com/company/events/v25-1-community-release-call?utm_source=clickhouse&utm_medium=email&utm_campaign=202412-newsletter) \- Jan 30


**Free training**


- [ClickHouse Fundamentals](https://clickhouse.com/company/events/clickhouse-fundamentals?utm_source=clickhouse&utm_medium=email&utm_campaign=202412-newsletter) \- Virtual \- Jan 8 and Jan 15
- [ClickHouse Query Optimization Workshop](https://clickhouse.com/company/events/202501-emea-query-optimization?utm_source=clickhouse&utm_medium=email&utm_campaign=202412-newsletter) \- Virtual \- Jan 22
- [Using ClickHouse for Observability](https://clickhouse.com/company/events/202501-amer-clickhouse-observability?utm_source=clickhouse&utm_medium=email&utm_campaign=202412-newsletter) \- Virtual \- Jan 29


**Events in EMEA**


- [Meetup in London](https://www.meetup.com/clickhouse-london-user-group/events/305146729/) \- Feb 5
- [Meetup in Dubai](https://www.meetup.com/clickhouse-dubai-meetup-group/events/303096989/) \- Feb 10


**Events in APAC**


- [Alibaba Developer Summit Jakarta](https://www.alibabacloud.com/en/events/alibabacloud-developer-summit-2025?_p_lc=1) \- Jan 21
- [Meetup in Tokyo](https://www.meetup.com/clickhouse-tokyo-user-group/events/305126993/) \- Jan 23


  

## Featured community member [\#](/blog/202412-newsletter#featured-community-member)


This month's featured community member is Azat Khuzhin, Lead Engineer at Semrush.


![featured-202412.png](/uploads/featured_202412_d0a6498ade.png)

Azat has been working at Semrush for over 13 years. His expertise lies in working with ClickHouse and other database management systems, handling large\-scale distributed systems, and data processing. 



He regularly contributes to ClickHouse, submitting over 60 pull requests this year, focused on performance optimization, system stability, and feature enhancements across various components. His work spans from improving distributed query processing and replication to enhancing security, configuration management, and user experience. 



[Follow Azat on LinkedIn](https://www.linkedin.com/in/iamazat?utm_source=clickhouse&utm_medium=email&utm_campaign=202412-newsletter)


 


## 24\.11 release [\#](/blog/202412-newsletter#2411-release)


![release-24.11.png](/uploads/release_24_11_7412f9e511.png)
The standout feature in the 24\.11 release was parallel hash join becoming the default join strategy. Other features include the ability to pre\-warm the marks cache, the BFloat16 data type for vector search, and the STALENESS modifier for WITH FILL.


In the [24\.11 community call](https://clickhouse.com/videos/202411-release-call), we also had a fun demo of [HyperDX](https://www.hyperdx.io/), an open\-source observability platform that uses ClickHouse.


[Read the release post](https://clickhouse.com/blog/clickhouse-release-24-11)


 


## A simple guide to ClickHouse query optimization: part 1 [\#](/blog/202412-newsletter#a-simple-guide-to-clickhouse-query-optimization-part-1)


![query-optimization.png](/uploads/query_optimization_b787976d7b.png)
Lionel Palacin recently joined the ClickHouse Product Marketing Engineering team and, while working on the [new ClickHouse Playground](https://sql.clickhouse.com/), became curious about how to improve the performance of sample queries used in the playground.



In the first of a two\-part blog series, he shares some things he’s learned. In the blog post, Lio explains what happens when a query runs, how to identify slow queries, and how to understand what happens during query execution using the EXPLAIN clause. He then shows how to apply various optimizations and see if they work.



[Read the blog post](https://clickhouse.com/blog/a-simple-guide-to-clickhouse-query-optimization-part-1)


 


## Building SQL\-based Observability With ClickHouse and Grafana [\#](/blog/202412-newsletter#building-sql-based-observability-with-clickhouse-and-grafana)


![observability-grafana.png](/uploads/observability_grafana_f791b8b1f7.png)
[Timofey Chuchkanov](https://www.linkedin.com/in/crt0r/), DevOps Engineer at EVALAR JSC has written a blog post detailing his experience building an observability stack based on ClickHouse and Grafana.


After reviewing the criteria for the ideal stack, which included querying using SQL, the ability to query logs and metrics, and integrations with other software, Timofey went through the candidate stacks. These included Elasticserach, Loki, Timescale, and more, but they settled on ClickHouse.



I enjoyed reading this one, and seeing more examples in the wild of [SQL\-based observability](https://clickhouse.com/blog/evolution-of-sql-based-observability-with-clickhouse) is cool.



[Read the blog post](https://cmtops.dev/posts/building-observability-with-clickhouse/)


 


## Postgres CDC connector for ClickPipes is now in Private Preview [\#](/blog/202412-newsletter#postgres-cdc-connector-for-clickpipes-is-now-in-private-preview)


![postgres-connector.png](/uploads/postgres_connector_3b1f2f93e3.png)
We recently announced the private preview of the Postgres Change Data Capture (CDC) connector in ClickPipes.



This enables customers to replicate their Postgres databases to ClickHouse Cloud in just a few clicks and leverage ClickHouse for blazing\-fast analytics. You can use this connector for continuous replication and one\-time migrations use cases from Postgres.



[Read the blog post](https://clickhouse.com/blog/postgres-cdc-connector-clickpipes-private-preview)


 


## ClickHouse Decoded: Making Sense of Fast Data [\#](/blog/202412-newsletter#clickhouse-decoded-making-sense-of-fast-data)


![fast-data.png](/uploads/fast_data_12c5108f28.png)
Shubham Bhardwaj takes a detailed look into the way that ClickHouse works. He starts by exploring the way data is laid out on disk and describes each component. Next, we move onto materialized views, table engines, and, finally, how to scale ClickHouse.



[Read the blog post](https://towardsdev.com/clickhouse-decoded-making-sense-of-fast-data-41c5a020734d)


 


## ClickHouse at AWS re 2024 [\#](/blog/202412-newsletter#clickhouse-at-aws-re-2024)


![product-reinvent.png](/uploads/product_reinvent_9dc038e9ff.png)
A bunch of colleagues spent the first week of December at the AWS re\-Invent conference in Las Vegas, and we had some product announcements simultaneously. 



Some highlights: Bring Your Own Cloud, Dashboards, and Native JSON support are all in Beta, the Postgres CDC connector in ClickPipes is in private preview, and vector similarity indexes are in early access.



[Read the blog post](https://clickhouse.com/blog/reinvent-2024-product-announcements)


 


## Video corner [\#](/blog/202412-newsletter#video-corner)


- ClickHouse has no PIVOT operator, but you can still achieve similar functionality using aggregate function combinators. Mark shows us how in his latest video, ‘[Can you PIVOT in ClickHouse?](https://clickhouse.com/videos/pivot-clickhouse)!
- Tony Burke works in the platform engineering team at SolarWinds, where they ingest three million messages per second into ClickHouse. Tony [explains how his team enhanced ClickHouse performance](https://clickhouse.com/videos/solarwinds-observability-3-milion-records-per-second), shedding light on real\-time telemetry data management and query optimization.
- [Refreshable materialized views](https://clickhouse.com/videos/intro-refreshable-materialized-views) were recently made production\-ready, so Mark did another video introducing them and showing some use cases.


 


## Quick reads [\#](/blog/202412-newsletter#quick-reads)


- Niels Reijers wanted to do a [Python itertools\-style GROUP BY in ClickHouse SQL](https://medium.com/@nielsreijers/python-itertools-style-group-by-in-sql-with-some-help-from-ai-ab072018fea4), and with help from the Brave Browser’s AI and some of his own refactoring, he got there!
- Zander Matheson [discusses the latest connector module available for Bytewax, the ClickHouse Sink](https://bytewax.io/blog/building-a-click-house-sink-for-bytewax). This sink enables users to seamlessly write data from Bytewax into ClickHouse.
- Wolfram Kriesing explains [how to call ClickHouse’s aggregation functions from Django](https://picostitch.hashnode.dev/clickhouse-aggregations-and-django).
- Matt Blewitt shares his [7 Databases to look at in 2025](https://matt.blwt.io/post/7-databases-in-7-weeks-for-2025/), and includes this great quote: “If I had to only pick two databases to deal with, I’d be quite happy with just Postgres and ClickHouse \- the former for OLTP, the latter for OLAP.”


 


## ClickHouse User Conference [\#](/blog/202412-newsletter#clickhouse-user-conference)


![user-conference.png](/uploads/user_conference_a2b03043e6.png)
Are you planning the conferences you'll attend in 2025? We suggest Open House—The ClickHouse User Conference, which will be held on May 28th and 29th in San Francisco.



We'll have a day of free training on the 28th, followed by talks on the 29th. Tickets aren’t available yet but register below to be updated on all information.



[Register to be kept informed](https://clickhouse.com/company/events/202505-global-open-house)


 


## Post of the month [\#](/blog/202412-newsletter#post-of-the-month)


Our favorite post this month was by [Gulzar Ahmed](https://x.com/megulzar), who’s using ClickHouse to help build Hyperzod, online delivery software for local businesses in India:


![twitter-202412.png](/uploads/twitter_202412_72254b4837.png)

[Read the post](https://x.com/megulzar/status/1864880796143583399)


Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
