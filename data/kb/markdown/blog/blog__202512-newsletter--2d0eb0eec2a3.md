# December 2025 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# December 2025 newsletter

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Dec 18, 2025 · 7 minutes readHello, and welcome to the December 2025 ClickHouse newsletter!


This month, we have a Postgres extension for querying ClickHouse, an analysis of how the five major cloud data warehouses compare in terms of cost\-performance, a review of the year in Postgres CDC, and more!


## Featured community member: Zjan Carlo Turla [\#](/blog/202512-newsletter#featured-community-member)


This month's featured community member is Zjan Carlo Turla, Software Engineer at Canva.


![dec2025_image3.png](/uploads/dec2025_image3_5c148fc70e.png)
Zjan works on Canva's Observability team, where he builds and maintains systems that monitor and ensure reliability across Canva's distributed infrastructure. Previously, he worked as a DevOps Consultant supporting large\-scale platforms and spent several years at Kalibrr as an SRE, migrating monolithic applications to microservices on Kubernetes.


At the recent [Open House roadshow in Sydney](https://clickhouse.com/openhouse/sydney), he shared [how Canva migrated production observability workloads in ClickHouse](https://clickhouse.com/blog/canva-faster-search-lower-costs), processing 3 million spans and 3 million logs per second for 240 million monthly active users, achieving 10x faster search and 70% cost savings.


➡️ [Connect with Zjan](https://www.linkedin.com/in/zjan-carlo-turla-358b28164/)


## Upcoming events [\#](/blog/202512-newsletter#upcoming-events)


### Global virtual events [\#](/blog/202512-newsletter#global-virtual-events)


- [v25\.12 Community Call](https://clickhouse.com/company/events/v25-12-community-release-call) \- December 18


### Virtual training [\#](/blog/202512-newsletter#virtual-training)


- [Preparing for the ClickHouse Certified Developer Exam](https://clickhouse.com/company/events/202512-amer-clickhouse-certified-developer-exam) \- December 18


**Real\-time Analytics**


- [Real\-time Analytics with ClickHouse: Level 1](https://clickhouse.com/company/events/202601-EMEA-Real-time-Analytics-with-ClickHouse-Level1) \- January 14
- [Real\-time Analytics with ClickHouse: Level 2](https://clickhouse.com/company/events/202601-EMEA-Real-time-Analytics-with-ClickHouse-Level2) \- January 21
- [Real\-time Analytics with ClickHouse: Level 3](https://clickhouse.com/company/events/202601-EMEA-Real-time-Analytics-with-ClickHouse-Level3) \- January 28


**Observability**


- [Observability with ClickStack: Level 2](https://clickhouse.com/company/events/202512-AMER-Observability-with-ClickStack) \- December 17
- [Observability with ClickStack: Level 1](https://clickhouse.com/company/events/202602-AMER-Observability-with-ClickStack-Level1) \- February 4


### Events in AMER [\#](/blog/202512-newsletter#events-in-amer)


- [Iceberg Meetup in Menlo Park](https://luma.com/abggijbh) \- January 21st
- [Iceberg Meetup in NYC](https://luma.com/ifxnj82q) \- January 23rd
- [New York Meetup](https://luma.com/iicnlq41) \- January 26th


### Events in EMEA [\#](/blog/202512-newsletter#events-in-emea)


- [ClickHouse Meetup in Tel Aviv](https://clickhouse.com/company/events/202512-EMEA-TelAviv-meetup) \- December 29
- [Data \& AI Paris Meetup](https://luma.com/3szhmv9h) \- January 22nd
- [Apache Iceberg™ Meetup Belgium: FOSDEM Edition](https://luma.com/yx3lhqu9) \- January 30th


### Events in APAC [\#](/blog/202512-newsletter#events-in-apac)


- [Under\-the\-Hood: Incremental Materialized Views \& Dictionaries Webinar](https://clickhouse.com/company/events/202601-APJ-Webinar-Materialized-Views) \- January 15


## Our gift to you: Free ClickHouse certification and new learning paths [\#](/blog/202512-newsletter#gift)


We've launched all\-new self\-paced learning paths designed to deliver the hands\-on experience needed to build real\-world skills and expertise to match your goals. Explore our new paths today:


- [Real\-time Analytics with ClickHouse](https://clickhouse.com/learn/real-time-analytics) \- Learn how to power real\-time dashboards, alerts, and event\-driven apps with ClickHouse.
- [Observability with ClickStack](https://clickhouse.com/learn/observability) \- Ingest logs, metrics, and traces to monitor systems and power observability dashboards.
- [Machine Learning and GenAI with ClickHouse](https://learn.clickhouse.com/class_catalog/category/141050) \- Use ClickHouse to prepare data, feed models, and support GenAI workflows at scale.
- Data Warehousing with ClickHouse \- Coming Soon! Design, build, and optimize modern data warehouses using ClickHouse.


As our holiday gift, get certified for free through the end of 2025\. Use code **2025CERTFREE** at checkout to claim your certification at no cost.


➡️ [Start learning](https://clickhouse.com/learn)


## 25\.11 release [\#](/blog/202512-newsletter#release)


![dec2025_image9.png](/uploads/dec2025_image9_d03fe17462.png)
My favourite feature in our penultimate release of the year, 25\.11, is projections as secondary indices, which lets you create lightweight projections that behave like a secondary index without duplicating complete rows of data.


This release also features faster GROUP BY operations on 8\-bit and 16\-bit integer keys, as well as the argAndMin and argAndMax functions, fractional LIMIT and OFFSET, and more.


➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-25-11)


## Introducing pg\_clickhouse: A Postgres extension for querying ClickHouse [\#](/blog/202512-newsletter#pg_clickhouse)


![dec2025_image8.png](/uploads/dec2025_image8_030a51e094.png)
David Wheeler announced the release of pg\_clickhouse, a PostgreSQL extension that brings ClickHouse's analytical power directly into your Postgres queries through foreign data wrappers.


Query ClickHouse tables from Postgres with intelligent pushdown optimization that executes aggregations and filters in ClickHouse for maximum performance, giving you access to massive analytical datasets without leaving your Postgres environment.


➡️ [Read the announcement](https://clickhouse.com/blog/introducing-pg_clickhouse)


## Dlt\+ClickHouse\+Rill: Multi\-Cloud Cost Analytics, Cloud\-Ready [\#](/blog/202512-newsletter#dlt_clickhouse_rill)


![dec2025_image6.png](/uploads/dec2025_image6_919ef77e95.png)
Simon Späti demonstrates how to build a real\-time FinOps dashboard using dlt to ingest AWS cost and usage reports into ClickHouse, and then visualizes the data with Rill.


The setup provides a practical blueprint for instant cost analysis at scale, with ClickHouse serving as the analytical engine to handle millions of cost records.


➡️ [Read the blog post](https://www.ssp.sh/blog/finops-dlt-clickhouse-rill/)


## Postgres CDC in ClickHouse, A year in review [\#](/blog/202512-newsletter#postgres_cdc_clickhouse)


![dec2025_image2.png](/uploads/dec2025_image2_b6a73bb304.png)
Sai Srirampur reflects on a year of building Postgres CDC in ClickHouse Cloud, growing from a handful of PeerDB users to over 400 companies replicating more than 200 TB of data monthly.


The post highlights technical wins, such as eliminating expensive replication reconnects that caused hours of lag and reducing partition generation from over 7 hours to under a second, while outlining next steps to close data modeling gaps and further scale logical replication.


➡️ [Read the blog post](https://clickhouse.com/blog/postgres-cdc-year-in-review-2025)


## ClickHouse as a security engine: Tempesta FW's approach to L7 DDoS and bot mitigation [\#](/blog/202512-newsletter#clickhouse_security_engine)


![dec2025_image4.jpg](/uploads/dec2025_image4_f0455307df.jpg)
Tempesta Technologies developed WebShield, an open\-source bot detection system that utilizes ClickHouse to analyze access logs in real\-time and automatically block Layer 7 DDoS attacks and malicious bots.


➡️ [Read the blog post](https://tempesta-tech.com/blog/defending-against-l7-ddos-and-web-bots-with-tempesta-fw/)


## How the five major cloud data warehouses compare on cost\-performance [\#](/blog/202512-newsletter#cloud_data_warehouses_cost_performance)


![dec2025_image1.png](/uploads/dec2025_image1_a877836355.png)
Did you know that public price lists of cloud data warehouses don't tell you real costs? Much more important is the amount of computing power the underlying engine consumes to run your queries.


Tom Schreiber \& Lionel Palacin break down [how Snowflake, BigQuery, Databricks, and Redshift bill you](https://clickhouse.com/blog/how-cloud-data-warehouses-bill-you), then benchmark their actual cost\-performance against ClickHouse.


➡️ [Read the blog post](https://clickhouse.com/blog/cloud-data-warehouses-cost-performance-comparison)


## clickhouse.build: An agentic CLI to accelerate Postgres apps with ClickHouse [\#](/blog/202512-newsletter#clickhouse_build)


![dec2025_image7.png](/uploads/dec2025_image7_7e52ce635d.png)
A Postgres \+ ClickHouse proof of concept in an hour? It sounds too good to be true, but clickhouse.build does precisely that.


Our new open\-source CLI uses agents to scan your TypeScript code, identify analytical queries, configure ClickPipes CDC, and rewrite your app to use both databases \- with a feature flag to toggle between backends and measure the impact.


➡️ [Read the blog post](https://clickhouse.com/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps)


## Quick reads [\#](/blog/202512-newsletter#quick-reads)


- Ahmet Kürşat Şerolar [shares a deep\-dive on optimizing ClickHouse](https://medium.com/logalarm-devs/clickhouse-fine-tuning-maximize-performance-for-time-series-and-logs-5b6f6943ca7c) for logs and time\-series data, covering engine selection, partitioning, LowCardinality fields, codecs (DoubleDelta \+ ZSTD), materialized views, and TTL\-based storage tiers.
- Vignesh T K [explains the difference](https://www.mafiree.com/readBlog/speeding-up-clickhouse-queries-materialized-views-vs-refreshable-views-explained) between ClickHouse's Materialized Views (real\-time updates on insert, best for streaming data) and Refreshable Materialized Views (scheduled periodic updates, better for complex joins and batch analytics).
- Georgii Baturin walks through [setting up a local dbt analytics environment with ClickHouse](https://medium.com/hands-on-dbt-with-clickhouse/hands-on-dbt-with-clickhouse-1-local-sandbox-and-safe-training-data-64f897be6843), covering Docker setup, creating separate training databases for raw data and dbt models, connecting dbt\-core with the ClickHouse adapter, and configuring Git \- providing a practical sandbox for learning dbt without touching production systems.
- Thinh Dang provides [a comprehensive guide to creating tables in distributed ClickHouse clusters](https://thinhdanggroup.github.io/tables-distributed-clickhouse-cluster/), covering local vs Distributed tables, ReplicatedMergeTree with Keeper coordination, ON CLUSTER DDL, sharding keys, internal\_replication settings, and operational patterns like materialized views for aggregations \- plus a practical checklist to avoid schema inconsistencies and replication headaches.
- Paul Bardea explains [how Blacksmith built a logging platform for GitHub Actions with ClickHouse](https://www.blacksmith.sh/blog/logging).
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
