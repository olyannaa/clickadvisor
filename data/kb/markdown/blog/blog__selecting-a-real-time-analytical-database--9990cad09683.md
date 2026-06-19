# What to look for when selecting a real\-time analytical database


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# What to look for when selecting a real\-time analytical database

![](/_next/image?url=%2Fuploads%2FMelvyn_00a76a1519.PNG&w=96&q=75)[Melvyn Peignon](/authors/melvyn-peignon)Jun 4, 2026 · 13 minutes read"Real\-time" is one of the most overloaded terms in the data industry. To a trading desk, it means microsecond order matching, to a team building a user\-facing app, a sub\-second page load, to a finance analyst "fresh by this morning.” Different workloads, all valid.


In analytics, "real\-time" usually means the user experience itself feels live. A customer refreshes a dashboard, opens a leaderboard, or investigates an issue and expects the data to reflect what just happened. Technically, this means not just delivering low\-latency analytical queries but achieving this while data is being continuously inserted at high volume.



> **Real\-time analytics is not just delivering fast queries, but delivering fast queries over continuously changing data.**


In this blog, we are going to walk you through why this form of real\-time analytics matters more than ever now, and how you can parse the problem by looking at both data availability and query latency. You’ll also come away with a practical set of questions to ask when evaluating whether a database can actually support real\-time analytics workloads.


## Why real\-time analytics matters now [\#](/blog/selecting-a-real-time-analytical-database#why-real-time-analytics-matters-now)


Analytics has undergone dramatic changes over the years, but a paradigm shift is now driven by three factors that are breaking down the previous batch\-based models.


First, analytics is moving into the product. The dashboards that used to be exclusively internal are increasingly being exposed directly to customers: [usage explorers](https://clickhouse.com/blog/how-gitlab-uses-clickhouse-to-scale-analytical-workloads) in SaaS products, performance views for advertisers, trading and risk views for end users. Every application has become data\-driven, and as a result, analytics latency has become non\-negotiable. Real\-time analytics has become a part of the user experience.


Second, an agent generating a customer summary, [scoring an investigation](https://www.harvey.ai/blog/building-an-agentic-security-operations-center), or routing a [support ticket](https://clickhouse.com/blog/mintlify) is only as good as the data it can see, and only as fast as it can query that data. Latency can become the real bottleneck. But freshness is only half the problem. Agents don't query the way humans do: agents can fire off 100x or more the number of queries in rapid succession, and multiply that by hundreds of agents running concurrently, each burning tokens while they wait. Most analytical engines were never built for workloads this bursty and unpredictable. Getting the data layer right isn't a footnote to agent development; it's a prerequisite.


Third, [more automated decisions](https://clickhouse.com/blog/mintlify) are based on live data. Pricing, personalization, [fraud prevention](https://tech.instacart.com/real-time-fraud-detection-with-yoda-and-clickhouse-bd08e9dbe3f4?gi=aab23e4a7857), observability alerts, and ad targeting. These are no longer reports that a human reads later, but decisions made inside a request, where end\-to\-end latency directly affects the quality and usefulness of the decision itself.


The demand is clear. As we parse the challenge here, "latency" is often mistaken as query latency only, when in reality it is actually a much broader system property, including how fast your data arrives, and when it becomes ready for querying.


## Real\-time analytics is a system property, not an engine feature [\#](/blog/selecting-a-real-time-analytical-database#real-time-analytics-is-a-system-property-not-an-engine-feature)


When customers evaluate a real\-time analytics platform, they often focus only on query latency. "Can it return an answer within 50ms?" is a reasonable question, and one most analytical engines can answer convincingly if you throw enough compute at a static dataset.


The question that decides what users actually experience is harder. It is whether the system can return a 50ms answer **on data that arrived a second ago**, while ingestion is still running, and while other users are also querying.


Data availability requires thinking about end\-to\-end time\-to\-insight, which has three components.


- **Time to ingest.** How long does it take for newly generated data to land in the platform and become durably stored?
- **Time to transform and prepare.** How long does it take to clean, enrich, join, pre\-aggregate, or update the serving structures (materialized views, rollups, indexes) that queries actually hit?
- **Time to query.** How long does it take to plan and execute the read once the data is available?


![data_delays.png](/uploads/data_delays_7b8b4a6044.png)
A system can be fast on one of these dimensions but still feel slow to the user if another one dominates.


**All of these properties need to hold at scale and with resource efficiency under high ingest throughput and high query concurrency.**


Importantly, a platform that achieves real\-time latencies only by throwing unbounded compute at the workload is not a real\-time platform you can afford. The hard part is meeting all of these requirements, with the same engine, against the same data, without trading one off against the other.


## Why data platforms struggle with this shape of workload [\#](/blog/selecting-a-real-time-analytical-database#why-data-platforms-struggle-with-this-shape-of-workload)


Most of the platforms in use today were designed for an earlier generation of analytics: batch ingestion, scheduled transformations, and internal users running ad\-hoc queries on data that was hours old. They are excellent at what they were built for, but struggle with real\-time analytics for reasons that are fundamentally architectural.


These architectural limitations can be broadly grouped into several categories:


1. **An ingest path that is optimized for batches, not continuous streams.** Many warehouse architectures use optimistic concurrency control. Writers proceed independently and resolve conflicts at commit time through retries. This works when writes are infrequent and well\-sized batches. However, as concurrent writers grow, the system is subject to more retries to resolve conflicts, causing tail latencies to increase. Continuous high\-concurrency ingestion is exactly the workload that exposes this.
2. **Fresh writes are not immediately visible.** In many modern lakehouse and warehouse architectures, data is not queryable immediately after it is written. It has to pass through a catalog refresh, a manifest update, a materialized view refresh, or a metadata reconciliation step before queries can see it. This delay is fine for an end\-of\-day report but fatal for a feature whose value depends on showing what just happened.
3. **Optimizations are not applied to live data.** Many warehouse architectures rely on materialized views to perform scheduled transformations and precompute results for low\-latency serving. These optimizations are often refreshed every hour, every fifteen minutes, or every minute if you are paying for it. As a result, the freshest your serving layer can possibly be is bounded by that interval. This limitation is architectural, with no amount of additional compute able to remove it. While a 15\-minute lag is invisible in a billing dashboard, it is the difference between catching and missing an event in a fraud signal or live leaderboard.
4. **Headline performance depends on caches that do not survive ingestion.** Benchmarks on a static dataset show performance for cached, pre\-warmed queries. Once continuous writes are added to the workload, every new part potentially invalidates some of these caches on which performance is dependent. The result is that the performance you saw in the demo is not the performance you will see in production.
5. **Real\-time capabilities are isolated feature sets of the platform.** When a platform was not designed for real\-time from the start, the common pattern is to bolt on a separate tier: a different table type, a different warehouse type, a different set of supported operations. Snowflake's Interactive Tables and Interactive Warehouses are a recent example. Low\-latency queries are available, but only against a specific table and warehouse type that cannot query standard tables, with a list of feature limitations that the [documentation describes as architectural](https://docs.snowflake.com/en/user-guide/interactive#limitations-of-interactive-warehouses-and-interactive-tables). A user who wants real\-time behavior across their entire dataset, not just a carved\-out capability, is forced to make compromises and architect their solution according to the constraints.
6. **Specialized query types that each need their own system.** Modern analytical workloads are not just structured rows. Teams want to filter logs by keyword, compare embeddings for similarity, and query semi\-structured JSON with evolving schemas. The traditional answer is to add a search engine for text queries, a vector database for embeddings, and a separate warehouse for everything else. Each additional system is another ingestion pipeline, another consistency boundary, another freshness floor, and more architectural complexity. Your end\-to\-end latency is determined by the slowest component.


None of this is a criticism of those platforms for what they were built to do. Batch\-era warehouses are still excellent at scheduled, internal\-facing analytics. The point is that real\-time analytics is different enough in shape that retrofitting it onto those architectures runs into limits that are not simply a matter of tuning.


## What a real\-time analytics platform actually has to do [\#](/blog/selecting-a-real-time-analytical-database#what-a-real-time-analytics-platform-actually-has-to-do)


A platform built from the ground up for real\-time analytics has to make a few specific design decisions. When you evaluate platforms for this workload, these are the requirements to check.


1. **Does ingestion scale without degrading queries?** Continuous writes should not pull query latency along with them. In practice, that means an ingestion path that can run on isolated resources from the read path, and a concurrency model that holds tail latencies bounded as writers grow. ClickHouse, for example, uses consensus\-based coordination through Keeper rather than optimistic concurrency. It pays a small coordination cost on every write, but keeps tail latencies predictable at the high insert concurrency seen in real\-time workloads.
2. **Is data queryable within a second or two of being written?** At real\-world scale, the realistic target is a delay measured in milliseconds to a couple of seconds, with no catalog or manifest refresh sitting in the middle.
3. **Do transformations update incrementally, and not on a schedule?** Materialized views, rollups, and pre\-aggregations (done using [AggregatingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/aggregatingmergetree) in ClickHouse) should update with each insert, not on an interval. This ensures that they're immediately applied and enforce a delay on data availability. This ensures, for example, that:
	- A live billing or usage view stays accurate as charges accrue, instead of jumping every fifteen minutes when the rollup refreshes. This matters when customers are looking at the same number you are.
	- A fraud or anomaly aggregation reflects the most recent events, instead of always being one window behind. This matters when the value of catching the event decays in seconds.


![scheduled_vs_incremental_views.png](/uploads/scheduled_vs_incremental_views_09e6115f62.png)
This maintenance model matters to cost and scalability. Materialized views that rely on full rescans for every update turn freshness into a scaling problem, with update cost growing alongside table size. Incremental materialized views amortize this cost across inserts, processing each row once as it arrives instead of repeatedly recomputing the full dataset.


4. **Can you bias the system towards read\-time or write\-time work?** Different workloads want different trade\-offs. For some, you want indexes and aggregations built at write time so the freshest queries are immediately accelerated. For others, you want to keep the ingest throughput maximal and let the background work catch up. A real\-time platform should expose that choice without forcing it. And index maintenance should never block ingestion. New data should be queryable as soon as it is committed, with or without its indexes fully built.
5. **Does a single engine serve all workloads?** Text search, vector similarity, JSON, structured analytics. These should live in the same storage and query engine, not in four loosely coupled systems with their own freshness floors. Every system you remove from the stack is one fewer place where data can fall behind.


![loosely_tightly_coupled.png](/uploads/loosely_tightly_coupled_07060e9416.png)
6. **Is the performance shown on hot data, not just on cached benchmarks?** The realistic question to ask of any platform is how fast its queries are on data that arrived a second ago, not how fast its repeated queries are on yesterday's table. The first number is what production looks like.
7. **Does resource efficiency hold up at scale?** Real\-time systems need to remain efficient as ingest volume, query concurrency, and retention grow. The important question is whether performance scales linearly with workload, or whether latency and compute costs begin to degrade disproportionately as traffic increases.


The common thread across these requirements is that real\-time analytics is not a feature you switch on. It is a set of design decisions about ingest, storage, transformation, and query that have to be made consistently across the whole system. Either the platform was designed for this workload, or it is working hard to approximate it.


## Bullet \- what real\-time looks like in practice [\#](/blog/selecting-a-real-time-analytical-database#bullet---what-real-time-looks-like-in-practice)


Bullet, a crypto derivatives exchange, runs a trading frontend that depends on real\-time data. Their previous batch\-era stack ran 5 to 30 second queries and 20\-minute hourly ETL jobs, leaving users looking at data up to 1\.5 hours stale. On ClickHouse Cloud, queries return in milliseconds, data latency dropped 99\.4% to under 5 seconds, and the team handles 1,000× more data at comparable cost. As Co\-Founder and CTO Tristan Frizza puts it:



> "We used to have a data lake, a serving layer, and all these other things that would break all the time. ClickHouse became the one\-size\-fits\-all."


For real\-world examples of real\-time analytics at scale, [explore how our customers](https://clickhouse.com/user-stories?useCase=1) are delivering fresh data and low\-latency insights with ClickHouse.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-816-get-started-today-sign-up&utm_blogctaid=816)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
