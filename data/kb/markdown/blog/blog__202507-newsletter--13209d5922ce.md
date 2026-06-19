# July 2025 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# July 2025 newsletter

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Jul 17, 2025 · 10 minutes readHello, and welcome to the July 2025 ClickHouse newsletter!


This month, we have a blog exploring ClickHouse’s join performance vs Databricks and Snowflake, reflections on getting the ClickHouse Certified developer credential, scaling our observability platform beyond 100 Petabytes, using ClickHouse for real\-time sports analytics, and more!


## Featured community member: Amos Bird [\#](/blog/202507-newsletter#featured-community-member)


This month's featured community member is Amos Bird, Software Engineer at Tencent.


![Featured Community Member Twitter Post (6).png](/uploads/Featured_Community_Member_Twitter_Post_6_5f4eb23a5e.png)
Amos Bird is the top ClickHouse contributor with more than 600 pull requests over 8 years. He implemented many features in ClickHouse, such as [projections](https://github.com/ClickHouse/ClickHouse/pull/20202), [common table expressions](https://github.com/ClickHouse/ClickHouse/pull/14771), [column transformers](https://github.com/ClickHouse/ClickHouse/pull/14233), and many optimizations, such as a [hash table with string keys segmented by size classes](https://github.com/ClickHouse/ClickHouse/pull/5417).


Amos Bird is actively involved in architecture discussions about ClickHouse. Every time Alexey travels to Beijing, he takes the opportunity to meet with Amos Bird and the local ClickHouse community!


➡️ [Follow Amos on LinkedIn](https://www.linkedin.com/in/amos-bird-25790b176/)


## Upcoming events [\#](/blog/202507-newsletter#upcoming-events)


### Global events [\#](/blog/202507-newsletter#global-events)


- [v25\.7 Community Call](https://clickhouse.com/company/events/v25-7-community-release-call) \- July 24


### Training [\#](/blog/202507-newsletter#training)


- [Migration to ClickHouse \- Hong Kong](https://clickhouse.com/company/events/202507-apj-hongkong-inperson-migration-to-clickhouse) \- July 17
- [ClickHouse Fundamentals \- Virtual](https://clickhouse.com/company/events/202507-amer-clickhouse-fundamentals) \- July 30
- [ClickHouse Deep Dive \- Bogota, Colombia](https://clickhouse.com/company/events/202508-in-person-bogota-clickhouse-deep-dive) \- August 5
- [ClickHouse Deep Dive \- Buenos Aires, Argentina](https://clickhouse.com/company/events/202508-in-person-buenos-aires-clickhouse-deep-dive) \- August 7
- [ClickHouse Deep Dive \- São Paulo, Brazil](https://clickhouse.com/company/events/202508-in-person-sao-paulo-clickhouse-deep-dive) \- August 12
- [ClickHouse Deep Dive \- Virtual](https://clickhouse.com/company/events/202508-amer-clickhouse-deeep-dive) \- August 12
- [ClickHouse Query Optimization \- Virtual](https://clickhouse.com/company/events/202508-apj-query-optimization) \- August 27


### Events in AMER [\#](/blog/202507-newsletter#events-in-amer)


- [Bogota ClickHouse Meetup](https://clickhouse.com/company/events/202508-latam-bo-meetup) \- August 5
- [Buenos Aires ClickHouse Meetup](https://clickhouse.com/company/events/202508-latam-BA-meetup) \- August 7
- [AWS Summit Toronto](https://clickhouse.com/company/events/2025-09-Amer-AWSSummit-Toronto) \- September 4
- [AWS Summit Los Angeles](https://clickhouse.com/company/events/2025-09-Amer-AWSSummit-LosAngeles) \- September 17


### Events in EMEA [\#](/blog/202507-newsletter#events-in-emea)


- [Tech BBQ Copenhagen](https://techbbq.dk/) \- August 27\-28
- [AWS Summit Zurich](https://aws.amazon.com/events/summits/zurich/) \- September 11
- [HayaData Tel Aviv](https://www.haya-data.com/), September 16
- [BigData London](https://www.bigdataldn.com/) \- September 24\-25
- [PyData Amsterdam](https://amsterdam.pydata.org/) \- September 24\-25
- [AWS Cloud Day Riyadh](https://aws.amazon.com/events/cloud-days/), September 29


### Events in APAC [\#](/blog/202507-newsletter#events-in-apac)


- [Hong Kong ClickHouse Meetup](https://clickhouse.com/company/events/202507-apj-hongkong-meetup) \- July 17
- [DataEngBytes Melbourne](https://clickhouse.com/company/events/202507-APJ-Melbourne-DataEngBytes) \- July 24\-25
- [DataEngBytes Sydney](https://clickhouse.com/company/events/202507-APJ-Sydney-DataEngBytes) \- July 29\-30
- [AWS Startup Dev Day Melbourne](https://clickhouse.com/company/events/202508-APJ-Melbourne-AWSStartupDevDay) \- August 1
- [KubeCon \+ CloudNativeCon India](https://clickhouse.com/company/events/202508-APJ-Hyderabad-KubeCon-India) \- August 6
- [AWS Summit Jakarta](https://clickhouse.com/company/events/202508-APJ-AWSSummit-Jakarta) \- August 7
- [Philippines Data \& AI Conference 2025](https://clickhouse.com/company/events/202508-APJ-Manila-DataAIConference) \- August 14


## 25\.6 release [\#](/blog/202507-newsletter#release)


![3_july.png](/uploads/3_july_56da9637be.png)
ClickHouse 25\.6 has some cool features, including consistent snapshots across complex queries, multiple projection filtering, and chdig (a built\-in monitoring TUI with real\-time flamegraphs).


The release also includes the Bloom filter optimization that saved OpenAI during the GPT\-4o image generation launch, now available to the entire community.


➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-25-06)


## Using ClickHouse Cloud for real\-time sports analytics [\#](/blog/202507-newsletter#real-time-sports-analytics)


![4_july_small.webp](/uploads/4_july_small_5149642916.webp)
In his latest article, Benjamin Wootton demonstrates how you can use ClickHouse Cloud to power real\-time sports analytics by processing player position data to create interactive visualizations of movement patterns, distance covered, and team dynamics on the football pitch.


The solution showcases ClickHouse's ability to handle high\-frequency sensor data with complex spatial calculations while enabling coaches to gain immediate insights during matches, all with the flexibility to scale from zero during weekdays to handling thousands of concurrent users on game day.


➡️ [Read the blog post](https://benjaminwootton.com/insights/sports-analytics-with-clickhouse/)


## Join me if you can: ClickHouse vs. Databricks \& Snowflake \- Part 1 [\#](/blog/202507-newsletter#join-me-if-you-can)


![2_july.png](/uploads/2_july_381724482e.png)
My colleagues Al Brown and Tom Schreiber challenge the myth that "ClickHouse can't do joins" by running unmodified, join\-heavy queries against a coffee\-shop\-themed benchmark used to compare Databricks and Snowflake.


Without any special tuning, ClickHouse consistently outperformed both competitors across all data scales (721M to 7\.2B rows), completing most queries in under a second while being faster and more cost\-effective.


These results stem from six months of targeted improvements to ClickHouse's join capabilities, significantly enhancing speed and scalability. In a [follow\-up blog post](https://clickhouse.com/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-part-2), Al and Tom show how to make things even faster using ClickHouse\-specific optimizations.


➡️ [Read the blog post](https://clickhouse.com/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance)


## Reflections on getting the ClickHouse Certified Developer credential [\#](/blog/202507-newsletter#clickhouse-developer)


![6_july.webp](/uploads/6_july_879bed1d0c.webp)
Burak Uyar shares his journey to becoming a ClickHouse Certified Developer in a practical guide highlighting the exam's focus on hands\-on SQL queries and real\-world problem\-solving rather than theoretical knowledge.


This blog provides useful preparation tips if you plan to take the certification soon. It emphasizes mastery of core topics like table engines, query optimization, and architecture through the official documentation and learning paths.


➡️ [Read the blog post](https://medium.com/@burakuyar/reflections-on-getting-the-clickhouse-certified-developer-credential-06f0aa5f2f82)


## Analytics at scale: Our journey to ClickHouse [\#](/blog/202507-newsletter#analytics-at-scale)


![5_july.webp](/uploads/5_july_145292edef.webp)
Didier Darricau shares how Partoo tackled the growing pains of their analytics product, where PostgreSQL queries were taking minutes to complete as their data grew to 800M records across 500GB, severely impacting client experiences and limiting their ability to onboard enterprise customers.


After comparing solutions against criteria including performance, editing capabilities, and AWS integration, they found ClickHouse outperformed AWS RedShift by 30% in volume testing and handled 10x more parallel queries, making it the best choice for their real\-time analytics needs.


Their implementation journey offers valuable insights into the trade\-offs between different ClickHouse data modification approaches. When faced with the challenge of updating existing records, Partoo evaluated ReplacingMergeTree and a custom solution, ultimately choosing the latter approach as it best fits their specific aggregation workload while achieving queries up to 50x faster than their previous implementation.


➡️ [Read the blog post](https://medium.com/partoo/analytics-at-scale-our-journey-to-clickhouse-d06ce7a4a72f)


## Scaling our Observability platform beyond 100 Petabytes by embracing wide events and replacing OTel [\#](/blog/202507-newsletter#observability-beyond-100-petabytes)


![1_july.png](/uploads/1_july_c3018f0f97.png)
Rory Crispin and Dale McDiarmid explain how our internal LogHouse observability platform scaled from 19PB to over 100PB of data by moving beyond OpenTelemetry's limitations with a purpose\-built System Tables Exporter (SysEx).


This custom solution handles 20x more data with 90% less CPU than OpenTelemetry. It embraces a "store everything, aggregate nothing" philosophy that enables powerful fleet\-wide analysis using ClickHouse's native capabilities.


➡️ [Read the blog post](https://clickhouse.com/blog/scaling-observability-beyond-100pb-wide-events-replacing-otel)


## Observability 2\.0: Breaking the Three\-Pillar Silos for Good [\#](/blog/202507-newsletter#observability-2)


![8_july.jpg](/uploads/8_july_958ba05478.jpg)
Zakaria El Bazi proves to be a kindred spirit who shares our vision at ClickHouse. He examines the shift from traditional "three\-pillar" observability to the unified ["Observability 2\.0"](https://clickhouse.com/videos/intro-to-observability) approach that stores all telemetry as rich contextual "wide events" in a columnar database.


Zakaria echoes ClickStack's core philosophy that unified observability eliminates tool fragmentation, dramatically reduces costs (potentially saving companies $450k/year), and enables natural data correlation, making troubleshooting faster and more effective in today's complex distributed systems.


➡️ [Read the blog post](https://medium.com/aws-morocco/observability-2-0-breaking-the-three-pillar-silos-for-good-bf3cdca1f40f)


## When SIGTERM Does Nothing: A Postgres Mystery [\#](/blog/202507-newsletter#when-sigterm-does-nothing-a-postgres-mystery)


![10_july.png](/uploads/10_july_d8e478ff54.png)
Kevin Biju Kizhake Kanichery’s deep dive into a mysterious PostgreSQL bug where logical replication slots became completely unkillable on read replicas was recently featured in [Postgres Weekly](https://postgresweekly.com/issues/607).


The investigation identified a subtle issue in PostgreSQL's transaction handling that could threaten database stability. Our patch was accepted and backported to all supported PostgreSQL versions. This work demonstrates our ongoing engagement with the PostgreSQL community and complements our ClickPipes PostgreSQL CDC offering, which enables smooth, reliable data integration between PostgreSQL and ClickHouse.


➡️ [Read the blog post](https://clickhouse.com/blog/sigterm-postgres-mystery)


## Quick reads [\#](/blog/202507-newsletter#quick-reads)


- Ashkan Golehpour [shares advice for PostgreSQL developers transitioning to ClickHouse](https://towardsdev.com/from-rows-to-columns-preventing-aggregation-pitfalls-when-migrating-to-clickhouse-5cf058c47304) around how CTEs work differently in ClickHouse and can produce incorrect aggregation results.
- Sajjad Aghapour demonstrates how to [enhance ClickHouse data security using the SQL security definer](https://medium.com/@sajjadaghapour/apply-data-security-on-clickhouse-using-security-definer-6da187cd79d2). This feature allows views to execute with the privileges of a predefined user rather than the querying user.
- Sanjeev Singh shows how to [use projections to speed up queries](https://medium.com/@sjksingh/solving-the-clickhouse-order-by-problem-with-projections-a3bec4da1f15) against the UK price paid dataset.
- Yash Patel provides [a practical guide to managing ClickHouse's system tables](https://medium.com/@yashpateld22d/optimizing-clickhouse-for-log-ingestion-and-system-table-cleanup-a97f9c55cce9), which can silently grow to consume more storage than your primary data. He discusses multiple solutions, including using force\_drop\_table flags to bypass size limits when truncating oversized tables, applying Time\-To\-Live (TTL) settings to automatically purge older logs, reducing logging levels in configuration, and implementing regular monitoring.


## Video corner [\#](/blog/202507-newsletter#video-corner)


- Mark Needham did a [3 minute introduction to observability](https://clickhouse.com/videos/intro-to-observability) and another [\~5 minute introduction to ClickStack](https://clickhouse.com/videos/intro-to-clickstack).
- And if you need more ClickStack, Mike Shi and Dale McDiarmid presented a webinar, [Introducing ClickStack: The Future of Observability on ClickHouse](https://clickhouse.com/videos/introducing-clickstack-july-2025).
- Dmitry Pavlov explains why Model Context Protocol completed changed his view about AI and [led to him building a production grade AI agent](https://clickhouse.com/videos/real-world-mcp).
- Robert Schulze [dives into the internals of how the JSON data type](https://clickhouse.com/videos/json-type-performant) was built to deliver high\-speed analytical performance, without sacrificing flexibility.
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
