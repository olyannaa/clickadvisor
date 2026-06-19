# March 2026 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# March 2026 newsletter

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Mar 19, 2026 · 9 minutes readHello, and welcome to the March 2026 ClickHouse newsletter!


This month, we have an overview of Geospatial, the launch of chDB 4, how Hookdeck made payload search 60 times faster, The Agentic Data Stack, and more!


## Featured community member: Jamie Herre [\#](/blog/202603-newsletter#featured-community-member)


This month's featured community member is Jamie Herre, Sr. Director of Engineering at Cloudflare.


![](/uploads/mar2026_nl_image4_2c5abe927e.png)
Jamie leads engineering on Cloudflare's analytics infrastructure \- a system that processes over 1\.61 quadrillion events every day across more than 300 global data centers, built on ClickHouse.


At the [ClickHouse meetup in August 2025](https://clickhouse.com/blog/cloudflare), Jamie shared how his team designed for both explosive growth and catastrophic failure simultaneously. In one live demonstration, a single query scanned 96 trillion events in under 2 seconds \- while a simulated North American outage caused European clusters to silently absorb the load without missing a beat.


➡️ [Connect with Jamie on LinkedIn](https://www.linkedin.com/in/jherre/)


## Upcoming events [\#](/blog/202603-newsletter#upcoming-events)


### Global virtual events [\#](/blog/202603-newsletter#global-virtual-events)


- [v26\.3 Community Call](https://clickhouse.com/company/events/v26-3-community-release-call) \- Mar 26, 2026
- [CDC ClickPipes: 데이터베이스를 ClickHouse로 복제하는 가장 빠른 방법](https://clickhouse.com/company/events/202604-APJ-Korea-Webinar-CDC-ClickPipes) \- Apr 1, 2026
- [Under\-the\-Hood: ClickHouse Incremental Materialized Views and Dictionaries](https://clickhouse.com/company/events/202603-AMER-Webinar-MaterializedViews) \- Apr 9, 2026
- [Combining Postgres \& ClickHouse to Build a Unified Data Stack](https://clickhouse.com/company/events/202604-APJ-Webinar-Unified-Data-Stack-ClickHouse-Postgres) \- Apr 22, 2026


### Virtual training [\#](/blog/202603-newsletter#virtual-training)


- [Observability with ClickStack: Level 3](https://clickhouse.com/company/events/202603-AMER-EMEA-Observabiity-with-ClickStackLevel3) \- Mar 25, 2026
- [Observability with ClickStack: Level 2](https://clickhouse.com/company/events/202604-AMER-EMEA-Observabiity-with-ClickStackLevel2) \- Apr 7, 2026
- [Query Optimization with ClickHouse Workshop](https://clickhouse.com/company/events/202604-APJ-query-optimization) \- Apr 7, 2026


### Events in AMER [\#](/blog/202603-newsletter#events-in-amer)


- [SRECon](https://clickhouse.com/company/events/20250325) \- Seattle \- Mar 25, 2026
- [Bay Area Iceberg Meetup: RSA Edition](https://clickhouse.com/company/events/20260324RSA) \- San Francisco \- Mar 24, 2026
- [Seattle Observability Meetup](https://clickhouse.com/company/events/20260326OBS) \- Seattle \- Mar 26, 2026
- [Fireside Chat in San Francisco: Column Stores \& the Evolution of Observability](https://clickhouse.com/company/events/20260331SF) \- San Francisco \- Mar 31, 2026
- [Seattle Startup Summit](https://clickhouse.com/company/events/20260401Start) \- Seattle \- Apr 1, 2026
- [Iceberg Summit](https://clickhouse.com/company/events/2026048ICEY) \- San Francisco \- Apr 8, 2026
- [AI Demo Night](https://clickhouse.com/company/events/20260409SF) \- San Francisco \- Apr 9, 2026
- [Google Cloud Next 2026](https://clickhouse.com/company/events/google-cloud-next-2026) \- Las Vegas \- Apr 22, 2026
- [House Party, Google Cloud Next](https://clickhouse.com/company/events/2026-houseparty-google-next) \- Las Vegas \- Apr 22, 2026
- [Open House](https://clickhouse.com/company/events/202605-global-open-house) \- San Francisco \- May 26, 2026


### Events in EMEA [\#](/blog/202603-newsletter#events-in-emea)


- [ClickHouse Meetup Munich](https://clickhouse.com/company/events/202603-EMEA-Munich-meetup) \- Munich \- Mar 19, 2026
- [KubeCon EU](https://talk.clickhouse.com/MjM4LUZQQy0zMTcAAAGgUzZGmrCsh9LwlOhfQ5S4NuJ8xeCq3mUb8G5BcC77kIWCSLiIIgxcRMEPPICfZJY68i42uok=) \- Amsterdam, 23\-26 March \- Hall 2 stand 261
- [DW\&BI](https://talk.clickhouse.com/MjM4LUZQQy0zMTcAAAGgUzZGmmaesRMWlmOCJFDfP-dRMIF62KX7wSNwW7XuKDPuAZhovJEFU7vmLZKWfQhES_NXQvg=) \- Utrecht, 24 March
- [ClickHouse x Apache Kafka x AWS](https://clickhouse.com/company/events/202603-EMEA-Milan-meetup) \- Milan \- Mar 26, 2026
- [ClickHouse x AWS x DoiT \- Gaming and Betting AI Workshop](https://ti.to/maltaawsusergroup/gen-a-i-day-malta/with/lpqxlepi9ww) \- Malta \- March 26, 2026
- [Lunch \& Learn with ClickHouse](https://clickhouse.com/company/events/202603-EMEA-Benelux-Amsterdam-LunchandLearn) \- Amsterdam \- Mar 31, 2026
- [AWS Summit Paris](https://aws.amazon.com/events/summits/paris/) \- Paris, 1 April \- Level 1 (nr. G3\)
- [Amsterdam In\-Person Training: Observability with ClickStack](https://clickhouse.com/company/events/202604-EMEA-Observability-with-ClickStack) \- Amsterdam \- Apr 8, 2026
- [CTO Networking Event with ClickHouse, AWS, Confluent \& DoiT](https://events.confluent.io/awsstartupexchangevienna2026) \- Vienna \- Apr 9, 2026
- [Scaling the Enterprise AI Operating Model](https://luma.com/wjv3v1tn) \- Berlin \- Apr 14, 2026
- [Paris In\-Person Training: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202604-EMEA-Paris-Real-time-Analytics-w-ClickHouse) \- Paris \- Apr 15, 2026
- [ClickHouse Meetup in Dublin](https://www.meetup.com/clickhouse-ireland-user-group/events/313793261) \- Dublin \- Apr 16, 2026
- [GrafanaCON](https://grafana.com/events/grafanacon/) \- Barcelona \- Apr 20\-22, 2026
- [Barcelona In\-Person Training: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202604-EMEA-Barcelona-Real-time-Analytics-w-ClickHouse) \- Barcelona \- Apr 20, 2026
- [AWS Summit London](https://aws.amazon.com/events/summits/london/) \- London \- Apr 22 \- Booth G18
- [Rise of AI Berlin](https://riseof.ai/conference-2026/) \- Berlin \- May 5\-6, 2026
- [AWS Summit Tel Aviv](https://aws.amazon.com/events/summits/tel-aviv/) \- Tel Aviv \- May 6, 2026
- [Data Innovation Summit](https://datainnovationsummit.com/) \- Stockholm \- May 6\-8, 2026
- [Gartner Data \& Analytics](http://gartner.com/en/data-analytics) \- London \- May 11\-13, 2026
- [Revolution Banking](https://www.revolutionbanking.es/) \- Madrid \- May 12, 2026
- [Platforma 2026](https://www.platfor-ma.com/) \- Tel Aviv \- May 20, 2026
- [AWS Summit Hamburg](https://aws.amazon.com/events/summits/hamburg/) \- Hamburg \- May 20, 2026
- [London 2\-day In\-Person Training: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202605-EMEA-London-Real-time-Analytics-w-ClickHouse) \- London \- May 19, 2026
- [ClickHouse Meetup London](https://www.meetup.com/clickhouse-london-user-group/events/313759007/) \- London \- May 19, 2026
- [Google Summit Madrid](https://cloudonair.withgoogle.com/events/cloud-ai-live-madrid-2026) \- Madrid \- May 28, 2026


### Events in APAC [\#](/blog/202603-newsletter#events-in-apac)


- [Python Asia 2026](https://2026.pythonasia.org/) \- Manila \- Mar 21\-22, 2026
- [Postgres \+ ClickHouse: Building a Real\-Time Open\-Source Data Stack](https://clickhouse.com/company/events/meetup-nz-23mar2026) \- Auckland \- Mar 23, 2026
- [DataEngBytes Auckland](https://dataengbytes.com/2026/auckland) \- Mar 24, 2026
- [Wellington Data Eng Meetup](https://clickhouse.com/company/events/meetup-nz-25mar2026) \- Wellington \- Mar 25, 2026
- [ClickHouse Shenzhen Meetup](https://clickhouse.com/company/events/202603-apj-shenzhen-meetup) \- Shenzhen \- Mar 28, 2026
- [Korean Webinar: CDC ClickPipes: 데이터베이스를 ClickHouse로 복제하는 가장 빠른 방법](https://clickhouse.com/company/events/202604-APJ-Korea-Webinar-CDC-ClickPipes) \- Apr 1, 2026
- [Data Streaming World Mumbai](https://events.confluent.io/dswt2026mumbai) \- Apr 13, 2026
- [Data Streaming World Bangalore](https://events.confluent.io/dswt2026bangalore) \- Apr 16, 2026
- [Taipei Open Source Meetup](https://clickhouse.com/company/events/taipei-open-source-meetup) \- Taipei \- Apr 16, 2026
- [Bangalore Meetup with Alexey Milovidov](https://www.meetup.com/clickhouse-bangalore-user-group/events/313739871/) \- Apr 18, 2026
- [Data Streaming World Jakarta](https://events.confluent.io/dswt2026jakarta) \- Apr 21, 2026
- [APJ Webinar: Combining Postgres \& ClickHouse to Build a Unified Data Stack](https://clickhouse.com/company/events/202604-APJ-Webinar-Unified-Data-Stack-ClickHouse-Postgres) \- Apr 22, 2026
- [Ho Chi Minh In\-Person Training: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202604-APJ-HoChiMinh-Real-time-Analytics-with-ClickHouse) \- Ho Chi Minh \- Apr 22, 2026
- [AWS Summit Bengaluru](https://aws.amazon.com/events/summits/bengaluru/) \- Apr 22\-23, 2026


## 26\.2 release [\#](/blog/202603-newsletter#26-2-release)


![](/uploads/mar2026_nl_image9_00d00cbf75.png)
My favorite feature in the recent ClickHouse 26\.2 release is time\-based block flushing for streaming data. This lets you batch inserts by time interval rather than row count, which is useful for low\-throughput feeds like Wikimedia recent changes.


The release also brings production\-ready text index and QBit data types, 3\.2x faster RIGHT/FULL JOINs, and embedded ClickStack for in\-product observability.


➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-26-02)


## Building towards an enterprise\-grade Postgres service in ClickHouse Cloud [\#](/blog/202603-newsletter#building-towards-an-enterprise-grade-postgres-service)


![](/uploads/mar2026_nl_image3_b4e4cebe10.jpg)
Sai Srirampur introduces the enterprise\-grade Postgres service, coming soon to ClickHouse Cloud, bringing cross\-AZ high availability, point\-in\-time recovery, automated backups, and failover\-safe CDC slots for ClickHouse integration.


In other Postgres news, Kaushik Iska introduces [pg\_stat\_ch](https://clickhouse.com/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse), an open\-source Postgres extension that streams query metrics directly into ClickHouse for latency analysis and error tracking without impacting production performance.


➡️ [Read the blog post](https://clickhouse.com/blog/enterprise-postgres-service-in-clickhouse-cloud)


## Announcing chDB 4: Write Pandas, Run ClickHouse, Now on Hex [\#](/blog/202603-newsletter#announcing-chdb-4)


![](/uploads/mar2026_nl_image10_d4f00e1d08.png)
Ryadh Dahimene and Auxten Wang introduce chDB 4, which adds a Pandas\-compatible DataStore API that executes on ClickHouse's engine under the hood.


Operations run lazily as an optimized pipeline, with automatic routing between ClickHouse and Pandas engines, and it's now available natively in Hex notebooks.


➡️ [Read the release post](https://clickhouse.com/blog/chdb.4-0-pandas-hex)


## How Trigger.dev built a custom SQL language on top of ClickHouse [\#](/blog/202603-newsletter#how-trigger-dev-built-a-custom-sql-language)


![](/uploads/mar2026_nl_image6_3d154dfd7b.png)
Matt Aitken, CEO of Trigger.dev, explains how they gave users SQL access to a shared multi\-tenant ClickHouse cluster without risking data leaks.


Their solution is TRQL, a SQL\-style DSL that compiles to tenant\-isolated ClickHouse queries \- dangerous operations are grammatically impossible, and tenant filters are injected at compile time.


➡️ [Read the blog post](https://trigger.dev/blog/how-trql-works)


## Announcing General Availability of ClickHouse Full\-text Search [\#](/blog/202603-newsletter#announcing-general-availability-of-full-text-search)


![](/uploads/mar2026_nl_image7_a3a43dd469.png)
Melvyn Peignon announces the general availability of full\-text search in ClickHouse, which uses native inverted indexes to enable fast token\-based filtering at scale.


The implementation supersedes Bloom filters for string matching, delivering deterministic results without false positives and reducing the number of granules scanned by up to 96%.


To see it in action, Lionel Palacin built [GitTrends](https://clickhouse.com/blog/gittrends), an open\-source demo that searches and aggregates nearly 10 billion GitHub events in real time, with a live comparison tool showing the performance differences between full\-text search, Bloom filters, and a full table scan.


➡️ [Read the blog post](https://clickhouse.com/blog/full-text-search-ga-release)


## How we made payload search 60x faster in ClickHouse [\#](/blog/202603-newsletter#how-we-made-payload-search-60x-faster)


![](/uploads/mar2026_nl_image5_7eaefa6d9a.png)
Maurice Kherlakian at Hookdeck describes how webhook payload search across millions of semi\-structured JSON records was timing out at 30\+ seconds, making debugging nearly impossible.


The fix: hashing values into typed bucket columns so queries scan a single bucket instead of all, combined with iterative time\-window scanning that stops once enough results are found, bringing latency down to under 400ms.


➡️ [Read the blog post](https://hookdeck.com/blog/how-we-made-payload-search-60x-faster-in-clickhouse)


## The Agentic Data Stack [\#](/blog/202603-newsletter#the-agentic-data-stack)


![](/uploads/mar2026_nl_image1_9d8086f2d3.png)
Dustin Healy outlines an open\-source agentic data stack that lets AI agents query ClickHouse directly via natural language, replacing dashboards and data tickets with real\-time conversational access.


The architecture combines ClickHouse's MCP server with an open\-source LLM interface and Langfuse for observability, keeping data and infrastructure under the user's control.


➡️ [Read the blog post](https://clickhouse.com/blog/the-agentic-data-stack)


## ClickHouse TTL in production: A safe strategy for data retention and disk optimization [\#](/blog/202603-newsletter#clickhouse-ttl-in-production)


![](/uploads/mar2026_nl_image8_5f21853f75.png)
Aliakbar Hosseinzadeh shares a production runbook for implementing ClickHouse TTL policies after his cluster hit 97% disk utilization, covering the key mental model shift: TTL runs during background merges, not at insert time.


The winning combination is to align partitioning with your TTL time unit and `set ttl_only_drop_parts=1`, which lets ClickHouse drop whole parts cleanly rather than triggering expensive mutation\-style rewrites.


➡️ [Read the blog post](https://medium.com/@aliakbarhosseinzadeh/clickhouse-ttl-in-production-a-safe-strategy-for-data-retention-and-disk-optimization-9f1546fe673f)


## Quick reads [\#](/blog/202603-newsletter#quick-reads)


- Mark Needham [surveys everything ClickHouse can do with geospatial data in 2026](https://clickhouse.com/blog/state-of-geospatial-march-2026) \- from Geometry types and spatial operations to H3 grid\-based analytics that run 12x faster than bounding\-box queries on 10 million rows.
- Fiona J. Sylvester shows how to run [STL\-based anomaly detection directly in ClickHouse](https://medium.com/@fiona.j.sylvester/wait-you-can-do-anomaly-detection-directly-inside-a-database-ba6ec8dceb8c), catching subtle deviations like a silent 4% transaction drop that would be missed by fixed thresholds.
- Parade suggests that [Microsoft Fabric's shared capacity model creates unpredictable performance](https://medium.com/@parade4940/stop-calling-it-saas-why-you-should-dump-microsoft-fabric-and-use-clickhouse-for-data-analytics-62e73b3cffbe) and runaway costs, and that swapping in ClickHouse as the analytics engine keeps Power BI intact while cutting bills from tens to thousands of dollars a month.
- Tom Schreiber [explains how the CLONE AS command](https://clickhouse.com/blog/table-cloning) creates instant copies of tables of any size by hard\-linking immutable data parts rather than copying bytes, enabling safe experimentation on production\-scale data with near\-zero storage overhead.
- Shuva Jyoti Kar [built a SecOps agent](https://medium.com/google-cloud/agentic-threat-hunting-conversational-telemetry-with-clickhouse-the-new-mcp-java-sdk-and-google-bb3d98aff1f3) that uses Google's MCP Toolbox and ClickHouse to let analysts query millions of rows of security telemetry in plain English, without exposing the schema or letting the LLM write raw SQL.
- Mohamed Hussain S explains how [understanding two ClickHouse internals](https://medium.com/@mohhddhassan/the-clickhouse-mental-model-most-engineers-miss-c1f39b18f46f) \- aggregation states and argMax \- unlocks simpler, more powerful query design that would require subqueries and joins in traditional SQL databases.
### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-110-get-started-today-sign-up&utm_blogctaid=110)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
