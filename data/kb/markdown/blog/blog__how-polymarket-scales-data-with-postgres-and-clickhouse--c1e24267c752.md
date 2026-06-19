# How Polymarket scaled their data stack with Postgres and ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Polymarket scaled their data stack with Postgres and ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 21, 2026 · 8 minutes readPolymarket is a prediction market platform where users can trade on the outcomes of real\-world events. As the platform grew, their data needs expanded. We talked to Max "Primo" Mershon, a Senior Data Engineer at Polymarket, about how they built their real\-time data warehouse for faster internal insights, and migrated computationally expensive analytical workloads from PostgreSQL to ClickHouse to power real\-time, user\-facing features that scale with rapid growth.


## Postgres isn’t built to do everything [\#](/blog/how-polymarket-scales-data-with-postgres-and-clickhouse#postgres-isnt-built-to-do-everything)


Like many fast\-growing startups, Polymarket started simple. They used PostgreSQL for everything:


- The trading system used Postgres for core transactional data.
- Internal dashboards queried the production Postgres directly to power charts and analysis.
- User facing APIs for stats and other aggregate views also ran against Postgres.


For a while, this worked fine. But as data volumes grew, it became clear Postgres was being asked to do a job it wasn’t built for, a common challenge for [real\-time applications outgrowing standard Postgres](https://clickhouse.com/resources/engineering/managed-postgres-for-ai-and-real-time-apps).


The Polymarket team used Hex dashboards for internal analytics, running queries directly against Postgres. As the database was populated with more trading data, these analytical queries started timing out or taking too long.



> "I knew that ClickHouse was fast and that we could run these aggregates in milliseconds, whereas it would literally time out with Postgres." \- Max "Primo" Mershon, Senior Data Engineer at Polymarket


The impact extended to user\-facing features in the Polymarket app. The [Polymarket Leaderboard](https://polymarket.com/leaderboard) lets anyone see how traders compare to each other, showing their transaction volume and profit/loss. These aggregate stats were computed on a schedule inside Postgres.


Serving the pre\-calculated aggregates from Postgres wasn’t the problem; calculating the Leaderboard was computationally expensive and consumed significant resources on the Postgres cluster. This resource contention threatened the stability of other workloads, including critical transactional flows. As resources were already strained, adding more features and granularity (e.g., categorical leaderboards, like Sports, Politics) wasn’t possible, as it would just make the problem worse.


Polymarket wanted to solve two challenges:


1. Make internal analytical workloads faster and work with larger data
2. Support more granular user\-facing analytical features without impacting transactional workloads


## Designing the solution [\#](/blog/how-polymarket-scales-data-with-postgres-and-clickhouse#designing-the-solution)


The goal was not to replace Postgres, but to complement it with a system that is designed to handle the analytical workloads. The end state would be Postgres \+ (something), working together.


The team had clear requirements:


- Handle growing on chain and off chain data with room to scale.
- Run heavy aggregate queries with low latency.
- Keep the operational surface area small enough for a lean team.
- Get to value quickly, Polymarket moves fast.


Polymarket evaluated ClickHouse and several other data platforms that the team were familiar with from previous roles. They realized they could get up and running quickly on ClickHouse and it would meet their scale and performance requirements.


ClickHouse offered a distinct advantage in time to value. Max had previous experience with ClickHouse and knew it could handle their scale and performance requirements. ClickHouse was also no stranger in the crypto space: Goldsky, a partner they use for blockchain data, [uses ClickHouse](https://clickhouse.com/blog/clickhouse-redpanda-architecture-with-goldsky) and [offers native integrations for its data streams](https://docs.goldsky.com/mirror/sinks/clickhouse).



> "I had experience with several data platforms, and we looked at them. We landed on ClickHouse because we could get started really quickly. It was fast, it was affordable." \- Max "Primo" Mershon, Senior Data Engineer at Polymarket


## Building the data warehouse [\#](/blog/how-polymarket-scales-data-with-postgres-and-clickhouse#building-the-data-warehouse)


Polymarket uses Hex for dashboarding and data exploration. When these dashboards ran on Postgres, deep analysis was difficult because queries would often run slowly or time out.


Polymarket successfully implemented a brand new data warehouse on ClickHouse in just a few weeks: integrating data sources, moving queries and updating dashboards.



> "In the span of a couple months we’ve established ClickHouse as our data warehouse, and integrated it into a production API." \- Max "Primo" Mershon, Senior Data Engineer at Polymarket


The warehouse pulls in three main classes of data.


**On chain trading data**  

Polymarket relies on Goldsky to index blockchain data. Goldsky provides a ClickHouse sink, so trades and other on\-chain events can be streamed straight into ClickHouse tables. That gives Polymarket high volume, append heavy datasets in the format ClickHouse handles best.


**Web and product analytics**  

Frontend and product analytics data lands in S3 as files. Rather than building a custom loader, Polymarket uses ClickPipes to sync those files into ClickHouse. That keeps ingestion simple while still making all of the clickstream data available for analysis.


**Off chain metadata**  

User profiles, market metadata, and other off\-chain data still flows through Postgres. They sync this data into ClickHouse on a schedule using [ClickHouse's native PostgreSQL Table Engine](https://clickhouse.com/docs/engines/table-engines/integrations/postgresql). This engine lets ClickHouse push queries down to Postgres and read the results, then transform and load the data into native ClickHouse MergeTree tables for analytics.


This gave them a single warehouse with streaming on\-chain data, batch off\-chain metadata, and web analytics, all queryable together.


The data team's Hex dashboards were updated to point to ClickHouse instead of Postgres, and the difference was immediate. No more timeouts. They could query down to any level of granularity they needed. The queries that used to time out in Postgres now ran in milliseconds.


## From internal analytics to user facing features [\#](/blog/how-polymarket-scales-data-with-postgres-and-clickhouse#from-internal-analytics-to-user-facing-features)


With the data warehouse running smoothly, Polymarket saw an opportunity to solve another problem: the expensive leaderboard calculation that was bogging down the production Postgres cluster.



> "The leaderboard is aggregated data. We were running these processes in Postgres and it's pretty computationally expensive… that's where ClickHouse thrives." \- Max "Primo" Mershon, Senior Data Engineer at Polymarket


In the new architecture, the leaderboard is modeled as aggregated data inside ClickHouse.


- Raw trades and related events flow into ClickHouse from Goldsky.
- Refreshable materialized views roll those events up into a leaderboard table on a regular schedule.
- The materialized views handle the heavy lifting, so the production API hits pre\-aggregated views.


Because these aggregations are so efficient, they can be infinitely more granular. Previously, the Leaderboard was limited to a single view, where transactions were aggregated across all categories. Now, the Leaderboard can be filtered to new categories and time dimensions.


![polymarket_leaderboard_screenshot.png](/uploads/polymarket_leaderboard_screenshot_b2eb78a3a4.png)
The Polymarket API (written in Go, and using the ClickHouse Go client) queries views that wrap the leaderboard table. These views let them add dynamic parameters, so users can filter by category, time period, or other dimensions on the fly.


The migration of the leaderboard feature from idea to production took approximately two weeks. The [API](https://docs.polymarket.com/api-reference/core/get-trader-leaderboard-rankings) now handles 100s requests per second, with an average latency of approximately 25 milliseconds.


## Impact and benefits [\#](/blog/how-polymarket-scales-data-with-postgres-and-clickhouse#impact-and-benefits)


Moving analytical workloads to ClickHouse delivered three major wins:


**Increased granularity**: The efficiency of ClickHouse meant they could build categorical leaderboards (Sports, Politics, P\&L, Volume) without overloading Postgres, and enable internal teams to perform larger and more complex analysis without query timeouts.


**Handle future scale**: ClickHouse allows the Polymarket team to continue to scale rapidly, particularly important as their platform has become a social phenomena. The resulting API is performant enough to be used not only by the Polymarket frontend but also by third\-party developers building trading bots and analytics tools.


**Reduced load on Postgres**: By moving leaderboard calculations off Postgres, they freed up compute capacity for the core trading platform. No more competing for resources between analytics and transactions.


## What's next [\#](/blog/how-polymarket-scales-data-with-postgres-and-clickhouse#whats-next)


Polymarket is growing rapidly, with every user creating more data and making more requests than ever. New features in the Polymarket app and [public APIs](https://docs.polymarket.com/api-reference/core/get-trader-leaderboard-rankings) continue to evolve how Polymarket uses data. With a U.S. launch coming soon, the pace of growth is set to accelerate even further. ClickHouse will underpin Polymarkets data strategy to handle scale, reduce latency and keep costs in check.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
