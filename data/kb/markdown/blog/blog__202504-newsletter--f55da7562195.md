# April 2025 Newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# April 2025 Newsletter

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Apr 16, 2025 · 6 minutes readHello, and welcome to the April 2025 ClickHouse newsletter!


This month, we bring you CloudQuery's compelling experience report after 6 months with ClickHouse, unveil the powerful new query condition cache in 25\.3, reflect on our year of Rust development, announce our strategic acquisition of HyperDX, and more!


## Featured community member: Julian LaNeve [\#](/blog/202504-newsletter#featured-community-member)


This month's featured community member is Julian LaNeve, CTO at Astronomer.


![0_april.png](/uploads/0_april_f7df5dfe00.png)
Before stepping into the CTO role in November 2023, Julian worked in the product team, focusing on developer experience, data observability, and open\-source initiatives. Notably, he led the launch of Astronomer's Cloud IDE \- a notebook tool designed for writing data pipelines.


Julian recently wrote a blog post describing why Astronomer chose ClickHouse Cloud to power its new data observability platform, Astro Observe. ClickHouse's ability to handle billions of Airflow workflow events with fast query performance and minimal maintenance requirements made it their database of choice. Julian also presented on the same topic at the [ClickHouse New York November 2024 meetup](https://clickhouse.com/blog/why-astronomer-chose-clickhouse-to-power-its-new-data-observability-platform-astro-observe).


➡️ [Follow Julian on LinkedIn](https://www.linkedin.com/in/julianlaneve/)


## Upcoming events [\#](/blog/202504-newsletter#upcoming-events)


We've started announcing our first speakers with just over a month until [Open House, The ClickHouse User Conference](https://clickhouse.com/openhouse?utm_source=marketo&utm_medium=email&utm_campaign=newsletter) in San Francisco on May 29\.


Kevin Weil (CPO at OpenAI) and Martin Casado (Partner at Andreessen Horowitz) will join Aaron Katz (CEO at ClickHouse) for a fireside chat about the future of data infrastructure for AI at scale.


Lukas Biewald (Founder and CEO at Weights \& Biases) will also join us to discuss the future of AI and the role high\-performance databases like ClickHouse play in powering next\-gen AI apps.


➡️ [Register for Open House](https://clickhouse.com/openhouse?utm_source=marketo&utm_medium=email&utm_campaign=newsletter)


### Global events [\#](/blog/202504-newsletter#global-events)


- [v25\.4 Community Call](https://clickhouse.com/company/events/v25-4-community-release-call) \- April 22


### Free training [\#](/blog/202504-newsletter#free-training)


- [ClickHouse Fundamentals \- Virtual](https://clickhouse.com/company/events/202504-emea-clickhouse-fundamentals) \- April 22
- [In\-Person BigQuery to ClickHouse \- Jakarta](https://clickhouse.com/company/events/202504-apj-jakarta-inperson-bigquery-to-clickhouse) \- April 22
- [Using ClickHouse for Observability](https://clickhouse.com/company/events/202505-amer-clickhouse-observability) \- May 7
- [ClickHouse Fundamentals \- Virtual](https://clickhouse.com/company/events/clickhouse-fundamentals) \- May 13
- [In\-Person ClickHouse Developer Fast Track \- Munich](https://clickhouse.com/company/events/202505-emea-munich-inperson-developer-fast-track) \- May 14
- [ClickHouse Developer Training \- Virtual](https://clickhouse.com/company/events/202505-amer-clickhouse-developer) \- May 21


### Events in AMER [\#](/blog/202504-newsletter#events-in-amer)


- [ClickHouse Meetup in Denver](https://www.meetup.com/clickhouse-denver-user-group/events/306934991/) \- April 23


### Events in EMEA [\#](/blog/202504-newsletter#events-in-emea)


- [AWS Summit 2025, London](https://clickhouse.com/company/events/04-2025-aws-london) \- April 30
- [AWS Summit 2025, Poland](https://clickhouse.com/company/events/202505-EMEA-Poland-AWS-Summit-MeetingRequests) \- May 6
- [ClickHouse Meetup in London](https://www.meetup.com/clickhouse-london-user-group/events/306047172/) \- May 13
- [ClickHouse Happy Hour Munich](https://clickhouse.com/company/events/202505-EMEA-Munich-HappyHour) \- May 14
- [ClickHouse Istanbul Meetup](https://www.meetup.com/clickhouse-turkiye-meetup-group/events/306978337/) \- May 14


### Events in APAC [\#](/blog/202504-newsletter#events-in-apac)


- [ClickHouse Jakarta Meetup \- AI Night!](https://www.meetup.com/clickhouse-indonesia-user-group/events/306973747/) \- April 22
- [AWS Summit Bengaluru](https://aws.amazon.com/events/summits/bengaluru/) \- May 7\-8
- [AWS Summit Hong Kong](https://aws.amazon.com/events/summits/hongkong/) \- May 8
- [Data Engineering Summit](https://des.analyticsindiamag.com/), Bengaluru \- May 15\-16


## 25\.3 release [\#](/blog/202504-newsletter#release)


![1_april.png](/uploads/1_april_706d25bab0.png)
My favorite feature in the 25\.3 release is the [query condition cache](https://clickhouse.com/blog/introducing-the-clickhouse-query-condition-cache), which caches the ranges of data that match a `WHERE` clause. This is useful in dashboarding or observability use cases where multiple queries have a different overall shape but the same filtering condition.


This release adds read support for the AWS Glue and Unity catalogs, new array functions, and automatic parallelization for external data. Finally, the JSON data type is now production\-ready!


➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-25-03)


## Six Months with ClickHouse at CloudQuery (The Good, The Bad, and the Unexpected) [\#](/blog/202504-newsletter#six-months-clickhouse)


![2_april.png](/uploads/2_april_e9f4a4925d.png)
Herman Schaaf and Joe Karlsson shared their six\-month experience using ClickHouse as their database backend for cloud asset inventory.


Their key insights include understanding when to use JOINs versus dictionaries for reference data, the critical importance of properly designing sorting keys for query performance, limitations of Materialized Views that led them to create custom snapshot tables, and ClickHouse's surprising versatility for logging and observability data.


Despite some challenges, CloudQuery found that ClickHouse delivered on its promises of speed and scalability for its cloud governance platform.


➡️ [Read the blog post](https://www.cloudquery.io/blog/six-months-with-clickhouse-at-cloudquery)


## A Year of Rust in ClickHouse [\#](/blog/202504-newsletter#year-of-rust)


![3_april.png](/uploads/3_april_b8aa814052.png)
Alexey Milovidov, ClickHouse's CTO, has written a blog about integrating Rust into their codebase.


The initiative began with small components like BLAKE3 and PRQL (with contributions from community members) before implementing more practical features such as Delta Lake support.


Throughout this journey, numerous technical challenges have been tackled, including build system integration, sanitizer compatibility, cross\-compilation problems, and symbol size bloat.


➡️ [Read the blog post](https://clickhouse.com/blog/rust)


## Scalable EDR Advanced Agent Analytics with ClickHouse [\#](/blog/202504-newsletter#scalable-edr-analytics)


![7_april.png](/uploads/7_april_c5df7e0bec.png)
Huntress has implemented ClickHouse to enhance its EDR analytics capabilities. Using ClickHouse has allowed them to process billions of data points daily across millions of endpoints while maintaining rapid query performance.


The implementation leverages [AggregatingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/aggregatingmergetree) and [Materialized Views](https://clickhouse.com/docs/materialized-view/incremental-materialized-view) to monitor agent health and stability efficiently.


➡️ [Read the blog post](https://www.huntress.com/blog/scalable-edr-advanced-agent-analytics-with-clickhouse)


## ClickHouse acquires HyperDX: The future of open\-source observability [\#](/blog/202504-newsletter#clickhouse-hyperdx)


![4_april.png](/uploads/4_april_f55fe2c585.png)
ClickHouse has acquired HyperDX, a fully open\-source observability platform built on ClickHouse.


This acquisition strengthens our ability to provide developers and enterprises with efficient and scalable observability solutions. By combining HyperDX's UI and session replay capabilities with ClickHouse's database performance, we're enhancing our open\-source observability offerings.


➡️ [Read the blog post](https://clickhouse.com/blog/clickhouse-acquires-hyperdx-the-future-of-open-source-observability)


## Make Before Break \- Faster Scaling Mechanics for ClickHouse Cloud [\#](/blog/202504-newsletter#make-before-break)


![5_april.png](/uploads/5_april_bafbeed1b7.png)
Jayme Bird and Manish Gill wrote a blog post about the "Make Before Break" (MBB) scaling approach introduced in ClickHouse Cloud to address limitations in the previous scaling method.


Initially, ClickHouse Cloud used a single StatefulSet to manage all server replicas, requiring rolling restarts that could take hours during scaling. The MBB approach creates new pods with desired resources before removing old ones, eliminating downtime during scaling operations.


This required developing a MultiSTS architecture where each pod is managed by its own StatefulSet and custom Kubernetes controllers to orchestrate migrations. Despite technical challenges, the team successfully migrated their entire fleet to this new architecture, significantly improving scaling times and reducing customer disruptions.


➡️ [Read the blog post](https://clickhouse.com/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud)


## Quick reads [\#](/blog/202504-newsletter#quick-reads)


- Hossein Kohzadi has written a blog post explaining [how to use ClickHouse in .NET applications](https://itnext.io/integrating-clickhouse-with-net-a-comprehensive-guide-to-blazing-fast-analytics-3e178503d54e).
- Roman Ianvarev [introduces QuerySight](https://medium.com/@rianvarev/introducing-querysight-a-query-driven-approach-to-data-warehouse-development-5f29b4bde4be), a command\-line tool that analyzes ClickHouse query logs and provides intelligent optimization recommendations for your dbt project​.
- Raj Kantaria [briefly introduces Anthropic’s Model Context Protocol](https://medium.com/@kantariyaraj/talk-to-your-database-with-mcp-88cf2468851d), using the ClickHouse MCP Server as an example.
- Tom Schreiber walks us through [accelerating ClickHouse queries on JSON data with the BlueSky dataset](https://clickhouse.com/blog/accelerating-clickhouse-json-queries-for-fast-bluesky-dashboards).
- Keshav Agrawal builds a [Real\-time data pipeline with Go, Kafka, ClickHouse, and Apache Superset](https://www.akitmcs.com/post/building-a-real-time-data-pipeline-with-go-kafka-clickhouse-and-apache-superset).


## Post of the month [\#](/blog/202504-newsletter#post-of-the-month)


My favorite post this month was by [Andi Pangeran](https://x.com/A_Pangeran), who’s been trying out Clickhouse’s support for reading from Delta Lake catalogs.


![6_april.png](/uploads/6_april_c0fe0f49cb.png)
➡️ [Read the post](https://x.com/A_Pangeran/status/1904807887463211506)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
