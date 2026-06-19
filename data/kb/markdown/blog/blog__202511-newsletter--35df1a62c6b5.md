# November 2025 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# November 2025 newsletter

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Nov 20, 2025 · 8 minutes readHello, and welcome to the November 2025 ClickHouse newsletter!


This month, we have big news with our LibreChat acquisition, a data analyst's AI\-powered warehouse build, 170x log compression techniques, and auto\-exporting traces to OpenTelemetry.


## Featured community member: Kiyose Ryu [\#](/blog/202511-newsletter#featured-community-member)


This month's featured community member is Kiyose Ryu, Engineering Manager at Smartnews, Inc.


![nov2025_image1.png](/uploads/nov2025_image1_44b9d11f45.png)
Kiyose Ryu has worked at Smartnews for the past five years, where he's helped build a real\-time aggregation system using ClickHouse.


Smartnews began introducing ClickHouse in 2020, and by 2021, had converted all advertiser reports to real\-time. Advertisers need up\-to\-the\-minute data to manage their campaigns effectively, which is why Smartnews prioritized delivering accurate, real\-time reports. Kiyose Ryu [shared the details of their implementation at the ClickHouse Tokyo meetup](https://clickhouse.com/videos/tokyo-meetup-smartnews-15apr25).


➡️ [Learn more about Smartnews](https://about.smartnews.com/ja/)


## Upcoming events [\#](/blog/202511-newsletter#upcoming-events)


### Global virtual events [\#](/blog/202511-newsletter#global-virtual-events)


- [How F45 Turns 1B\+ Data Points into 70% Higher Member Satisfaction](https://clickhouse.com/company/events/webinar-f45-fiveonefour-clickhouse) \- November 20
- [v25\.11 Community Call](https://clickhouse.com/company/events/v25-11-community-release-call) \- November 25


### Virtual training [\#](/blog/202511-newsletter#virtual-training)


**Real\-time Analytics**


- [Real\-time Analytics with ClickHouse: Level 1](https://clickhouse.com/company/events/202511-AMER-Real-time-Analytics-with-ClickHouse-Level1) \- November 19
- [Real\-time Analytics with ClickHouse: Level 1](https://clickhouse.com/company/events/202511-APJ-Real-time-Analytics-with-ClickHouse-Level1) (APJ\-friendly) \- November 25
- [Real\-time Analytics with ClickHouse: Level 2](https://clickhouse.com/company/events/202511-APJ-Real-time-Analytics-with-ClickHouse-Level2) (APJ\-friendly) \- November 26
- [Real\-time Analytics with ClickHouse: Level 3](https://clickhouse.com/company/events/202511-APJ-Real-time-Analytics-with-ClickHouse-Level3) (APJ\-friendly) \- November 27
- [Real\-time Analytics with ClickHouse: Level 1](https://clickhouse.com/company/events/202512-AMER-Real-time-Analytics-with-ClickHouse-Level1) \- December 2
- [Real\-time Analytics with ClickHouse: Level 2](https://clickhouse.com/company/events/202512-AMER-Real-time-Analytics-with-ClickHouse-Level2) \- December 3
- [Real\-time Analytics with ClickHouse: Level 3](https://clickhouse.com/company/events/202512-AMER-Real-time-Analytics-with-ClickHouse-Level3) \- December 4
- [Real\-time Analytics with ClickHouse: Level 1](https://clickhouse.com/company/events/202512-AMER-Real-time-Analytics-with-ClickHouse-Level1) \- December 9
- [Real\-time Analytics with ClickHouse: Level 2](https://clickhouse.com/company/events/202512-AMER-Real-time-Analytics-with-ClickHouse-Level2) \- December 10
- [Real\-time Analytics with ClickHouse: Level 3](https://clickhouse.com/company/events/202512-AMER-Real-time-Analytics-with-ClickHouse-Level3) \- December 11


**Observability**


- [Observability at Scale with ClickStack](https://clickhouse.com/company/events/202511-EMEA-Observability-at-Scale-with-ClickStack) \- November 26
- [Observability at Scale with ClickStack](https://clickhouse.com/company/events/202512-AMER-Observability-at-Scale-with-ClickStack) \- December 3
- [Observability with ClickStack: Level 2](https://clickhouse.com/company/events/202512-AMER-Observability-with-ClickStack) \- December 17


### Events in AMER [\#](/blog/202511-newsletter#events-in-amer)


- [House Party, The SQL](https://clickhouse.com/houseparty/the-sql), Las Vegas \- December 3


### Events in EMEA [\#](/blog/202511-newsletter#events-in-emea)


- [ForwardData Paris (Data\&AI)](https://www.forward-data-conference.com/en) \- November 24
- [Paris Monitoring Day](https://www.be4data.com/) \- November 25
- [ClickHouse Meetup Warsaw](https://www.meetup.com/clickhouse-poland-user-group/events/311309076/?eventOrigin=network_page) \- November 26
- [ClickHouse Meetup in Tel Aviv](https://clickhouse.com/company/events/202512-EMEA-TelAviv-meetup) \- December 29


### Events in APAC [\#](/blog/202511-newsletter#events-in-apac)


- [Mumbai In\-Person Training \- Real\-time Analytics with ClickHouse: Level 1](https://clickhouse.com/company/events/202511-in-person-Mumbai-Real-time-Analytics-with-ClickHouse-Level1) \- November 21
- [ClickHouse \+ AWS Bangkok Meetup](https://www.meetup.com/clickhouse-thailand-meetup-group/events/311852739/) \- November 25
- [Open Source Summit Japan](https://clickhouse.com/company/events/2025-12-APJ-Tokyo-OpenSourceSummitJapan) \- December 8
- [Jakarta In\-Person Training \- Real\-time Analytics with ClickHouse: Level 1](https://clickhouse.com/company/events/202512-in-person-Jakarta-Real-time-Analytics-with-ClickHouse-Level1) \- December 9
- [ClickHouse Jakarta Meetup](https://www.meetup.com/clickhouse-indonesia-user-group/events/311988089/) \- December 9
- [ClickHouse Tokyo Meetup \& Year\-End Party](https://www.meetup.com/clickhouse-tokyo-user-group/events/311974739/) \- December 15
- [AI Engineering Summit Tokyo](https://clickhouse.com/company/events/2025-12-APJ-Tokyo-AIEngineeringSummitJapan) \- December 16


## 25\.10 release [\#](/blog/202511-newsletter#release)


![nov2025_image2.png](/uploads/nov2025_image2_d724343f36.png)
ClickHouse 25\.10 sees a collection of JOIN performance optimizations. These include lazy column replication, bloom filter optimizations, and smarter push\-down of complex conditions, delivering up to 24 times faster queries in some cases.


There are also several additions to the SQL syntax, including the `<=>` (IS NOT DISTINCT FROM) operator, negative limit and offset (perfect for getting the n most recent records but returning them in ascending order), and `LIMIT BY ALL`.


And finally, my personal favorite \- as of ClickHouse 25\.10, we can query the ClickHouse Arrow Flight server using the ClickHouse Arrow Flight client.


➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-25-10)


## ClickHouse welcomes LibreChat: Introducing the open\-source Agentic Data Stack [\#](/blog/202511-newsletter#librechat)


![nov2025_image3.png](/uploads/nov2025_image3_cdd181698e.png)
We acquired LibreChat, the leading open\-source AI chat platform, to create the "Agentic Data Stack" \- combining LibreChat's multi\-LLM interface with ClickHouse's analytical speed so users can query data in plain English.


Companies like Shopify, Daimler Truck, and cBioPortal are already using this stack to democratize data access, and [our own AI\-powered data warehouse](https://clickhouse.com/blog/ai-first-data-warehouse) now handles 70% of queries for 200\+ users.


LibreChat remains 100% open\-source under its MIT license, and we plan to implement deeper native integrations while preserving the platform's flexibility.


➡️ [Read the announcement](https://clickhouse.com/blog/librechat-open-source-agentic-data-stack)


## Streaming asynchronous inserts monitoring in ClickHouse [\#](/blog/202511-newsletter#streaming-asynchronous-inserts-monitoring-in-clickhouse)


![nov2025_image4.png](/uploads/nov2025_image4_bcbf17b7d3.png)
AB Tasty's William Attache explains how his team built a comprehensive monitoring system to track ClickHouse asynchronous inserts end\-to\-end, from initial requests through flush queries to final part merges. The team created a custom view that joins data from multiple system tables to visualize the complete lifecycle of streaming inserts.


Along the way, they achieved significant cost savings by switching from JSON to RowBinary format and optimizing their batch sizes based on how ClickHouse actually creates and merges parts.


➡️ [Read the blog post](https://medium.com/the-ab-tasty-tech-blog/streaming-asynchronous-inserts-monitoring-in-clickhouse-c1378bd8b159)


## We built a vector search engine that lets you choose precision at query time [\#](/blog/202511-newsletter#we-built-a-vector-search-engine-that-lets-you-choose-precision-at-query-time)


![nov2025_image5.png](/uploads/nov2025_image5_178fcf89ba.png)
Raufs Dunamalijevs added QBit to ClickHouse, a column type that stores floats as bit planes. It allows you to choose how many bits to read during vector search, thereby tuning recall and performance without altering the data.


➡️ [Read the blog post](https://clickhouse.com/blog/qbit-vector-search)


## From 0–1: Building our data warehouse with ClickHouse to enable self\-serve analytics and observability at scale [\#](/blog/202511-newsletter#from-0-1-building-our-data-warehouse-with-clickhouse-to-enable-self-serve-analytics-and-observability-at-scale)


![nov2025_image6.png](/uploads/nov2025_image6_ea0a2450fb.png)
Viralo hit 10M users, and their PostgreSQL analytics setup collapsed, with dashboards taking over 30 minutes to load, CPUs maxing out at over 80%, and queries failing. They migrated to ClickHouse Cloud and implemented a [medallion architecture](https://clickhouse.com/blog/building-a-medallion-architecture-with-clickhouse), using SQL for all data transformations instead of external ETL tools, which reduced query time to under 30 seconds.


Notably, Shubham Bhardwaj's team constructed the entire warehouse using a low\-code approach, leveraging Claude Sonnet for code assistance, thereby eliminating orchestration tool costs and demonstrating that innovative architecture and AI tooling can effectively replace complex data stacks.


➡️ [Read the blog post](https://medium.com/@shubhamb957/from-0-1-building-our-data-warehouse-with-clickhouse-to-enable-self-serve-analytics-and-f5fbe2cd7e3a)


## Tracing the invisible: Building end\-to\-end observability in a real\-time streaming pipeline [\#](/blog/202511-newsletter#tracing-the-invisible-building-end-to-end-observability-in-a-real-time-streaming-pipeline)


![nov2025_image7.png](/uploads/nov2025_image7_919adb86b2.png)
When building end\-to\-end observability for their real\-time metrics pipeline, Pranav Mehta's team faced a unique challenge: ClickHouse stores query spans internally, but it cannot use an SDK to push those traces to an OpenTelemetry collector, as is done with application services.


They came up with a clever idea of using an incremental materialized view that writes to a table backed by the URL engine, which points at the OTel collector API.


Now they can trace a request all the way from the application, through NATS JetStream, into ClickHouse query execution \- and see it all in one view.


➡️ [Read the blog post](https://medium.com/@pranavmehta94/tracing-the-invisible-building-end-to-end-observability-in-a-real-time-streaming-pipeline-eccc91524e24)


## ClickHouse partners with Japan Cloud to establish ClickHouse K.K. and accelerate growth in Japan [\#](/blog/202511-newsletter#clickhouse-partners-with-japan-cloud-to-establish-clickhouse-k-k-and-accelerate-growth-in-japan)


![nov2025_image8.png](/uploads/nov2025_image8_c644ce69a0.png)
Earlier this month, ClickHouse announced the establishment of ClickHouse K.K., its Japanese subsidiary, through a strategic partnership with Japan Cloud.


➡️ [Read the blog post](https://clickhouse.com/blog/japan-cloud)


## Quick reads [\#](/blog/202511-newsletter#quick-reads)


- Alexey Milovidov [derives and visualizes real\-time weather data](https://clickhouse.com/blog/planes-weather) (wind direction, speed, and air pressure) from airplane telemetry stored in ClickHouse using trigonometry and color mapping.
- Nisarg Pipaliy has written [a beginner\-friendly explainer that breaks down ClickHouse's table engines](https://medium.com/@nisargpipaliya2402/clickhouse-explained-simply-why-its-different-and-when-to-use-it-9b298406485d), showing how different engines, such as MergeTree, ReplacingMergeTree, and SummingMergeTree, give tables distinct "personalities" for handling deduplication, aggregation, and replication. This makes it clear why ClickHouse is fundamentally different from traditional row\-based databases, such as PostgreSQL.
- Julian Virguez [wired ClickHouse directly into Salesforce](https://medium.com/@julianvirguez/real-time-product-sentiment-wiring-clickhouse-data-into-sf-ui-557812267d29) using a Lightning Web Component that queries 150M rows of Amazon review data in under a second.
- Lionel Palacin demonstrated [how to achieve 170x\+ compression on Nginx logs](https://clickhouse.com/blog/log-compression-170x) by transforming raw text into structured columns with optimized data types and strategic ordering keys. He then followed this up with another post showing how to [automatically group similar log messages and extract variable fields into columns](https://clickhouse.com/blog/improve-compression-log-clustering), achieving nearly 50x compression while keeping logs fully queryable and reconstructable.
- Andrii K walks through [setting up a complete CDC pipeline](https://medium.com/@andriikrymus/streaming-postgresql-data-changes-to-clickhouse-with-debezium-kafka-18dbebb8f29a) using Debezium to capture PostgreSQL changes, stream them through Kafka with Avro serialization, and sink into ClickHouse.


## Video corner [\#](/blog/202511-newsletter#video-corner)


- Mark Needham demonstrates the [ClickHouse MCP server's new chDB mode](https://clickhouse.com/videos/mcp-server-chdb), which enables in\-process execution of ClickHouse queries without a server.
- At Web Summit 2025, [Alexey Milovidov demonstrated loading massive public datasets into ClickHouse and then running real\-time analytics](https://clickhouse.com/videos/web-summit-2025-alexey-milovidov), such as comparing writing styles across domains, tracking trends on Reddit, and creating an interactive map that showed the "best photo" for every location on Earth.
- At [OpenHouse Bangalore 2025](https://clickhouse.com/openhouse/bangalore), Kiran Raparti and Pragnesh Bhavsar from HighLevel explained how they [migrated four critical use cases from MySQL, Elasticsearch, and MongoDB to ClickHouse](https://clickhouse.com/videos/open-house-bangalore-highlevel).
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
