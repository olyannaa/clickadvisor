# August 2025 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# August 2025 newsletter

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Aug 22, 2025 · 6 minutes readHello, and welcome to the August 2025 ClickHouse newsletter!


This month, we have lightweight updates introduced in ClickHouse 25\.7, LLM observability for LibreChat with ClickStack, a Gemini vs Claude SQL bake\-off, and more!


## Featured community member: Gene Makarov [\#](/blog/202508-newsletter#featured-community-member)


This month's featured community member is Gene Makarov, CTO at SWOT Mobility.


![0_august.png](/uploads/0_august_d79f4f633d.png)
As CTO of SWAT Mobility, he leads data science teams creating algorithms for demand\-responsive public transit systems, dealing with real\-time GPS data processing, traffic analysis, and logistics optimization for millions of commuters.


Gene is a long\-time user of ClickHouse, picking it up for the first time almost a decade ago, just after it became open\-source! Recently, he tackled an interesting challenge: [rendering vector tiles directly from ClickHouse for mapping engines like MapboxGL and MapLibre](https://www.linkedin.com/posts/gene-makarov-18aa9511_clickhouse-is-quite-powerful-database-which-activity-7334866878877548544-bANc?utm_source=share&utm_medium=member_desktop&rcm=ACoAAACI6V4B_x0ZnBa8U3AkVEmxmQ7-T2kWckI).


Building on Alexey Milovidov's bitmap tile example, Gene created an elegant solution using an intermediate Golang server to generate MVT format tiles. His weekend experiment demonstrates how ClickHouse can efficiently serve hundreds of millions of geospatial points for real\-time mapping applications.


➡️ [Follow Gene on LinkedIn](https://www.linkedin.com/in/gene-makarov-18aa9511/)


## Upcoming events [\#](/blog/202508-newsletter#upcoming-events)


### Global events [\#](/blog/202508-newsletter#global-events)


- [v25\.8 Community Call](https://clickhouse.com/company/events/v25-8-community-release-call) \- August 28


### Virtual training [\#](/blog/202508-newsletter#virtual-training)


- [Observability at Scale with ClickStack (Virtual)](https://clickhouse.com/company/events/202509-emea-clickstack-deep-dive-part1) \- August 27
- [ClickHouse Query Optimization (Virtual)](https://clickhouse.com/company/events/202508-apj-query-optimization) \- August 27
- [ClickHouse Deep Dive Part 1](https://clickhouse.com/company/events/202509-amer-clickhouse-deep-dive-part1) \- September 3
- [ClickHouse Query Optimization Workshop](https://clickhouse.com/company/events/202509-emea-query-optimization) \- September 11
- [ClickHouse Deep Dive Part 1](https://clickhouse.com/company/events/202509-emea-clickhouse-deep-dive-part1) \- September 24


### Events in AMER [\#](/blog/202508-newsletter#events-in-amer)


- [San Francisco ClickHouse Meetup](https://clickhouse.com/company/events/202509-amer-SF-meetup) \- August 26
- [Menlo Park In\-Person Training \- Observability at Scale with ClickStack: Logs, Metrics, Traces and RUM on ClickHouse](https://clickhouse.com/company/events/20250827-in-person-SanFrancisco-Observability-at-Scale-ClickStack) \- August 27
- [San Francisco In\-Person Training \- Observability at Scale with ClickStack: Logs, Metrics, Traces and RUM on ClickHouse](https://clickhouse.com/company/events/20250828-in-person-SanFrancisco-Observability-at-Scale-ClickStack) \- August 28
- [Toronto ClickHouse Meetup](https://clickhouse.com/company/events/202509-namer-tor-meetup) \- September 3
- [Raleigh ClickHouse Meetup](https://clickhouse.com/company/events/202509-amer-ra-meetup) \- September 4
- [AWS Summit Toronto](https://clickhouse.com/company/events/2025-09-Amer-AWSSummit-Toronto) \- September 4
- [ClickHouse Deep Dive Training \- Toronto](https://clickhouse.com/company/events/202509-in-person-clickhouse-deep-dive) \- September 5
- [New York ClickHouse \+ Docker Meetup](https://clickhouse.com/company/events/202509-amer-NY-meetup) \- September 8
- [AWS Summit Los Angeles](https://clickhouse.com/company/events/2025-09-Amer-AWSSummit-LosAngeles) \- September 17
- [ClickHouse Deep Dive Part 1 \- In\-Person Training (New York)](https://clickhouse.com/company/events/202510-nyc-clickhouse-deep-dive-part1) \- 7 October


### Events in EMEA [\#](/blog/202508-newsletter#events-in-emea)


- [Tech BBQ Copenhagen](https://techbbq.dk/) \- August 27\-28
- [ClickHouse Meetup in Tel Aviv](https://clickhouse.com/company/events/202509-EMEA-TelAviv-meetup) \- September 9
- [AWS Summit Zurich](https://aws.amazon.com/events/summits/zurich/) \- September 11
- [HayaData Tel Aviv](https://www.haya-data.com/), September 16
- [ClickHouse Meetup in Dubai](https://clickhouse.com/company/events/202509-EMEA-Dubai-meetup) \- September 16
- [Roundtable: "Real\-Time Data \& AI: Best Practices with AWS \& ClickHouse"](https://clickhouse.com/company/events/202509-EMEA-Dubai-RoundTable) \- September 17
- [BigData London](https://www.bigdataldn.com/) \- September 24\-25
- [PyData Amsterdam](https://amsterdam.pydata.org/) \- September 24\-25
- [AWS Cloud Day Riyadh](https://aws.amazon.com/events/cloud-days/), September 29
- [ClickHouse Meetup in Madrid](https://clickhouse.com/company/events/202509-EMEA-Madrid-meetup) \- September 30
- [ClickHouse Meetup in Barcelona](https://clickhouse.com/company/events/202510-EMEA-Barcelona-meetup) \- October 1
- [AI in ClimateTech Panel \- Amsterdam C\-Level Meetup](https://clickhouse.com/company/events/AI-ClimateTechPanel-Amsterdam) \- October 7
- [ClickHouse Meetup in Zürich](https://clickhouse.com/company/events/202510-EMEA-Zurich-meetup) \- October 9
- [ClickHouse Meetup in London](https://clickhouse.com/company/events/202510-EMEA-London-meetup) \- October 15
- [Amsterdam User Conference](https://clickhouse.com/company/events/202510-amsterdam-open-house) \- October 27
- [ClickHouse Deep Dive Part 1 In\-Person Training](https://clickhouse.com/company/events/202510-in-person-clickhouse-deep-dive-part-1) (Amsterdam) \- October 28
- [ClickHouse Meetup in Cyprus](https://clickhouse.com/company/events/202511-EMEA-Cyprus-meetup) \- November 20


### Events in APAC [\#](/blog/202508-newsletter#events-in-apac)


- [Database Technology Conference China](https://dtcc.it168.com/) \- August 21
- [AWS Community Day Pune](https://clickhouse.com/company/events/202508-APJ-Pune-AWSCommunityDayPune) \- August 23
- [Delhi/Gurgaon Migration to ClickHouse Workshop (in\-person)](https://clickhouse.com/company/events/202509-apj-Gurgaon-inperson-migration-to-clickhouse) \- September 4
- [CloudCon Sydney](https://clickhouse.com/company/events/202509-APJ-Sydney-CloudCon) \- September 9\-10
- [Asia Data Analytics Conference Vietnam](https://vdac.vn/pages/vietnam-11-september-2025) \- September 11
- [AWS Community Day Vadodara](https://communityday.awsugvad.in/) \- September 13
- [AWS Startup Dev Day Sydney](https://aws.amazon.com/startups/events/aws-startup-dev-day-sydney-2025) \- September 18
- [Data \& AI Summit Singapore](https://forefrontevents.co/event/data-ai-summit-singapore-2025/) \- September 24
- [Sydney Open House User Conference](https://clickhouse.com/openhouse/sydney) \- October 2
- [Bangalore Open House User Conference](https://clickhouse.com/openhouse/bangalore) \- October 7


## 25\.7 release [\#](/blog/202508-newsletter#release)


![1_august.png](/uploads/1_august_2dc99aa221.png)
In ClickHouse 25\.7, we've delivered lightweight SQL UPDATE and DELETE operations that are up to 1,000× times faster thanks to Anton Popov's new patch\-part mechanism.


We've also added [AI\-powered SQL generatio](https://clickhouse.com/docs/use-cases/AI/ai-powered-sql-generation)n from Kaushik Iska (just type `??` and ask your question in plain English!), Amos Bird's clever optimization that makes `count()` aggregations 20\-30% faster by skipping memory allocation, and Nikita Taranov's continued JOIN improvements delivering up to 1\.8× speedups.


➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-25-07)


## Using Gemini and Claude For SQL Analytics \- A Bake Off [\#](/blog/202508-newsletter#using-gemini-and-claude-for-sql-analytics-a-bake-off)


![2_august.png](/uploads/2_august_2088af27a6.png)
Benjamin Wootton benchmarked Claude Opus and Gemini 2\.5 Pro for SQL analytics with ClickHouse, using Danny's Diner SQL. Both LLMs achieved near\-perfect accuracy, generating complex SQL queries from plain English prompts via the [MCP (Model Context Protocol)](https://clickhouse.com/docs/use-cases/AI/MCP) standard. You'll have to read the blog to find out which model solved the questions more quickly!


➡️ [Read the blog post](https://benjaminwootton.com/insights/clickhouse-gemini-claude)


## How we built fast UPDATEs for the ClickHouse column store [\#](/blog/202508-newsletter#how-we-built-fast-updates-for-the-clickhouse-column-store)


![3_august.png](/uploads/3_august_0e430e119d.png)
In the first part of Tom Schreiber’s deep dive into ClickHouse updates, he explains how ClickHouse solves the performance challenges of row\-level updates by treating updates as inserts through purpose\-built engines like ReplacingMergeTree, CoalescingMergeTree, and CollapsingMergeTree that leverage ClickHouse's insert throughput and background merge process.


➡️ [Read the blog post](https://clickhouse.com/blog/updates-in-clickhouse-1-purpose-built-engines)


## Querying \~86 Million rows/s for high\-performance dashboard analytics [\#](/blog/202508-newsletter#querying-86-million-rows-s-for-high-performance-dashboard-analytics)


![4_august.png](/uploads/4_august_cf0cf3f366.png)
Edouard Kombo shares how he abandoned his initial Python \+ PostgreSQL stack when faced with 4\-second query times on just 50 million rows, discovering that ClickHouse's columnar storage and vectorized execution could scan 400 million rows at \~86 million rows per second \- making sub\-second analytics on billions of rows achievable.


➡️ [Read the blog post](https://edouard-kombo.medium.com/querying-billions-of-data-in-seconds-with-go-clickhouse-svelte-5157e9cb5232)


## LLM observability with ClickStack, OpenTelemetry, and MCP [\#](/blog/202508-newsletter#llm-observability-with-clickstack-opentelemetry-and-mcp)


![5_august.png](/uploads/5_august_71915d3759.png)
Dale McDiarmid and Lionel Palacin demonstrate how to build comprehensive LLM observability using ClickStack, our open\-source observability stack, to instrument LibreChat \- an AI chat platform with MCP support.


➡️ [Read the blog post](https://clickhouse.com/blog/llm-observability-clickstack-mcp)


## Quick reads [\#](/blog/202508-newsletter#quick-reads)


- Mohamed Hussain S explores [generating a Parquet file using Python and loading it into ClickHouse using Go](https://dev.to/mohhddhassan/from-python-to-clickhouse-parquet-etl-with-go-lm1).
- Mohamed Hussain S also [shares some lessons he learnt about writing better ClickHouse queries](https://medium.com/@mohhddhassan/my-first-clickhouse-query-mistakes-and-what-they-taught-me-acd7fbee4773).
- Divyanshu Raj [explores the AggregatingMergeTree table engine](https://www.glassflow.dev/blog/aggregatingmergetree-clickhouse), explains how it works, where it shines, and how it compares with other engines like ReplacingMergeTree.
- Bayu Setiawan builds a [medallion architecture](https://clickhouse.com/blog/building-a-medallion-architecture-with-clickhouse) [using Kafka, Debezium, Flink, Airflow, ClickHouse, and MinIO](https://towardsdev.com/building-a-scalable-real-time-etl-pipeline-with-kafka-debezium-flink-airflow-minio-and-b5a85ae28a02).
- Alireza Mousavizade explains how to build a [real\-time session analytics pipeline](https://medium.com/@alireza.mousavizade/real-time-user-behavior-analytics-at-scale-with-kafka-and-clickhouse-cf3107a30728) designed for high\-throughput, resilience, and superior query performance, capable of transforming raw event streams into interactive, live dashboards.
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
