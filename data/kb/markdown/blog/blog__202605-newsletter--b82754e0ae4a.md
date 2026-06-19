# May 2026 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# May 2026 newsletter

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)May 21, 2026 · 9 minutes readHello, and welcome to the May 2026 ClickHouse newsletter!


This month's issue is heavy on observability, with Javier Ortiz on how Qonto replaced Grafana Tempo with ClickHouse Cloud, and LINE MAN Wongnai's walkthrough of rebuilding their stack to handle 60 billion records a day at 10x better storage efficiency.


There's also an AI thread running through: Qonto's MCP\-powered incident companion, Mastra's new ClickHouse adapter for agent telemetry, and Benjamin Wootton on agentic analytics in financial services.


And rounding things out, Mark Needham covers index\-based pruning, and Tom Schreiber and Lionel Palacin make the case against Elasticsearch for log analytics.


## Featured community member: Javier Ortiz [\#](/blog/202605-newsletter#featured-community-member)


This month's featured community member is Javier Ortiz, Tech Lead for SRE Observability at Qonto, a digital banking platform serving over 600,000 small businesses and freelancers across Europe.


![](/uploads/newsletter_may2026_image1_b67d7bae92.png)
Javier built their observability function from the ground up, growing the team from zero to four engineers while staying hands\-on across architecture, tooling, and incident response.


When Qonto's Grafana Tempo\-based tracing setup started hitting its limits, Javier led the migration to ClickHouse Cloud for unified observability across traces, logs, and events. [ClickHouse's compression](https://clickhouse.com/resources/engineering/database-compression) reduced their high\-cardinality trace metadata from 231 TB uncompressed to 376 GB on disk, making it feasible to store everything without sampling, and query windows expanded from a few hours to two weeks. He also built an AI\-powered incident companion on top of the [ClickHouse MCP server](https://clickhouse.com/blog/integrating-clickhouse-mcp), enabling engineers to quickly investigate production issues in natural language.


In February 2026, Javier presented this work at the ClickHouse Meetup in Paris in a talk titled "[Supercharging Observability with ClickHouse and AI](https://clickhouse.com/videos/qonto-supercharging-observability)", which was also written up as a [blog post](https://clickhouse.com/blog/qonto).


➡️ [Connect with Javier on LinkedIn](https://www.linkedin.com/in/ortizjaviere/)


## Open House 2026 [\#](/blog/202605-newsletter#open-house)


It's now only one week until Open House, a free three\-day ClickHouse user conference running May 26\-28 at Convene, San Francisco.


Kick things off on May 26 with hands\-on workshops on real\-time analytics, observability, AI agents, and database administration, then head into two days of keynotes, technical sessions, and networking.


Hear from ClickHouse's CEO Aaron Katz and CTO Alexey Milovidov, plus Bret Taylor (Sierra), Guillermo Rauch (Vercel), Charity Majors (Honeycomb.io), Tristan Handy (dbt Labs), and practitioners from Visa, Cisco, Shopify, and Zoox. Admission is free!


➡️ [Register now](https://clickhouse.com/openhouse/san-francisco)


## 26\.4 release [\#](/blog/202605-newsletter#26-4-release)


![](/uploads/newsletter_may2026_image2_6e5c11640f.png)
The 26\.4 release had a big focus on SQL compatibility features, including VALUES as a table expression, natural join, and compound INTERVAL literals.


There's also a new function, `JSONAllValues`, for adding a text index on all JSON sub\-columns, `COUNT(DISTINCT)` got faster on machines with many cores, and the web UI was polished.


➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-26-04)


## How LINE MAN Wongnai handles 60 billion records a day at 10x better storage efficiency [\#](/blog/202605-newsletter#how-line-man-wongnai-handles-60-billion-records-a-day)


![](/uploads/newsletter_may2026_image3_a6b59dcfbb.png)
Tanawit Aeabsakul walks through how the Platform \& SRE team at LINE MAN Wongnai rebuilt their observability stack on self\-hosted ClickHouse to serve three independent business clusters (LINE MAN, Wongnai, and FoodStory) that previously had no shared query surface.


The result is 1\.5 million rows per second at peak ingest, 10x compression with 143 TB of raw data stored in just 14 TB on disk, a 53% reduction in observability costs, and 100% trace retention after years of sampling.


➡️ [Read the blog post](https://life.wongnai.com/how-we-reduced-storage-10x-while-handling-60-billion-records-a-day-0ed9b9783362)


## Do you still need Elasticsearch for log analytics? ClickHouse says no. [\#](/blog/202605-newsletter#do-you-still-need-elasticsearch-for-log-analytics)


![](/uploads/newsletter_may2026_image4_28bb62ef54.png)
Tom Schreiber and Lionel Palacin benchmarked ClickHouse against Elasticsearch for log analytics on datasets up to 50 billion rows.


ClickHouse uses 5x less disk space and runs queries 4\-6x faster on cold runs, and Tom and Lio argue that logs are fundamentally analytical data that happen to contain text, making a dedicated search engine the wrong tool for the job.


➡️ [Read the blog post](https://clickhouse.com/blog/elasticsearch-log-analytics-clickhouse)


## Deploying agentic analytics in financial services [\#](/blog/202605-newsletter#deploying-agentic-analytics-in-financial-services)


![](/uploads/newsletter_may2026_image5_8be65be4ff.png)
Benjamin Wootton explores why financial services has emerged as an early adopter of agentic analytics, with use cases spanning trade surveillance, complaint analysis, and KYC/AML automation.


He argues that the convergence of better LLMs, MCP servers, and observability tooling has made the approach production\-ready, and that ClickHouse's ability to handle tens of concurrent queries makes it a natural fit for the workload.


➡️ [Read the blog post](https://benjaminwootton.com/insights/agentic-analytics-financial-services)


## ClickStack SQL Charting and Alerting [\#](/blog/202605-newsletter#clickstack-sql-charting-and-alerting)


![](/uploads/newsletter_may2026_image6_2d0db8b946.png)
Drew Davis and Dale McDiarmid introduce SQL\-based charting and alerting in ClickStack, letting you build dashboards and alerts from arbitrary ClickHouse SQL rather than a fixed query builder.


Queries adapt automatically to dashboard time ranges and filters via macros, and alerting supports analytical patterns, such as error spikes relative to rolling baselines rather than static thresholds.


➡️ [Read the blog post](https://clickhouse.com/blog/clickstack-sql-charting-and-alerting)


## Index\-based pruning in ClickHouse [\#](/blog/202605-newsletter#index-based-pruning-in-clickhouse)


![](/uploads/newsletter_may2026_image7_0e9d16c884.png)
Mark Needham walks through three index\-based pruning strategies in ClickHouse: the primary index, lightweight projections, and minmax skip indexes.


Using a UK property sales dataset, he builds intuition for which technique to reach for and why the choice depends on how your data is ordered on disk.


➡️ [Read the blog post](https://clickhouse.com/blog/index-based-pruning)


## Quick reads [\#](/blog/202605-newsletter#quick-reads)


- The Mastra team [announced native ClickHouse support in the Mastra AI agent framework](https://mastra.ai/blog/introducing-clickhouse-support) with a new storage adapter that persists agent telemetry, traces, and logs to ClickHouse Cloud or self\-hosted ClickHouse for production observability.
- Mobin Shaterian [walks through connecting a SASL\_SSL\-secured Kafka cluster to ClickHouse](https://medium.com/stackademic/connecting-kafka-to-clickhouse-with-ssl-a-complete-integration-guide-e5a0a5957de3), covering SSL configuration, building the ingestion pipeline with a Kafka engine table and materialized view, and performance tuning tips.
- Denis Sazonov covers ClickHouse in [part nine of his Learning System Design series](https://medium.com/@sadensmol/learning-system-design-9-clickhouse-why-analytical-databases-are-absurdly-fast-9bc1dfef29f9), explaining why analytical databases are so fast through columnar storage, per\-column compression codecs, vectorized SIMD execution, and the sparse primary index. He also provides practical guidance on MergeTree, LowCardinality, and correctly batching inserts.
- The ClickStack team introduces [otel.fyi](https://clickhouse.com/blog/otel-fyi), a search\-first documentation site for the OpenTelemetry Collector that consolidates receiver, processor, exporter, and extension configuration into a single place.
### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-656-get-started-today-sign-up&utm_blogctaid=656)## Upcoming events [\#](/blog/202605-newsletter#upcoming-events)


### Global virtual events [\#](/blog/202605-newsletter#global-virtual-events)


- [Observing and Improving AI Agents with Langfuse](https://clickhouse.com/company/events/202605-APJ-Webinar-Observing-and-Improving-AI-Agents-with-Langfuse) \- May 27, 2026
- [Real\-Time Analytics ohne ETL: Inkrementelle Materialized Views und Dictionaries in ClickHouse](https://clickhouse.com/company/events/202605-EMEA-DACH-Webinar-MaterializedViews-DE) \- May 28, 2026
- [Maximizando a produtividade dos seus Agentes de IA com ClickHouse](https://clickhouse.com/company/events/202605-LATAM-Agentic-AI-Webinar) \- Jun 16, 2026


### Virtual training [\#](/blog/202605-newsletter#virtual-training)


- [Observability with ClickStack: Level 1](https://clickhouse.com/company/events/202606-AMER-Observability-with-ClickStack-Level1) \- Jun 3, 2026
- [ClickHouse Fundamentals](https://clickhouse.com/company/events/202606-APJ-ClickHouse-Fundamentals) \- Jun 10, 2026
- [ClickHouse Fundamentals](https://clickhouse.com/company/events/202606-AMER-EMEA-ClickHouse-Fundamentals) \- Jun 24, 2026
- [Observability with ClickStack: Level 1](https://clickhouse.com/company/events/202607-APJ-Observability-with-ClickStack-Level1) \- Jul 8, 2026
- [Observability with ClickStack: Level 2](https://clickhouse.com/company/events/202607-APJ-Observabiity-with-ClickStack-Level2) \- Jul 9, 2026
- [Observability with ClickStack: Level 3](https://clickhouse.com/company/events/202607-APJ-Observabiity-with-ClickStack-Level3) \- Jul 10, 2026
- [Query Optimization with ClickHouse Workshop](https://clickhouse.com/company/events/202607-AMER-EMEA-query-optimization-workshop) \- Jul 22, 2026


### Events in AMER [\#](/blog/202605-newsletter#events-in-amer)


- [Toronto Meetup](https://clickhouse.com/company/events/202606torontomeetup) \- Toronto \- Jun 2, 2026
- [Capacitación presencial en Bogotá: Analytics en tiempo real con ClickHouse](https://clickhouse.com/company/events/202606-LATAM-Bogota-Real-time-Analytics-with-ClickHouse) \- Bogotá \- Jun 2, 2026
- [Bogotá Meetup](https://luma.com/64ox1was) \- Jun 2, 2026
- [ClickHouse Café @ Snowflake Summit](https://luma.com/clickh-0h6k) \- Jun 3, 2026
- [AWS Summit Toronto Happy Hour with rootly AI](https://luma.com/c7p3qazp) \- Toronto \- Jun 3, 2026
- AWS Summit Toronto \- Toronto \- Jun 3, 2026
- [Toronto In\-Person Training: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202606-AMER-Toronto-Real-time-Analytics-w-ClickHouse) \- Toronto \- Jun 5, 2026
- [Web Summit Rio de Janeiro](https://rio.websummit.com/) \- Jun 9\-11, 2026
- AWS Summit Los Angeles \- Los Angeles \- Jun 10, 2026
- [ClickHouse \+ Hex AI Hackathon](https://luma.com/clickh-2ujv) \- Jun 11, 2026
- [Sao Paulo Meetup](https://luma.com/clickh-87tk) \- Jun 11, 2026
- [ClickHouse Cafe @ Data \& AI summit](https://luma.com/clickh-vrjd) \- San Francisco \- Jun 16, 2026
- AWS Summit NYC \- NYC \- Jun 17, 2026
- [AWS Summit NYC Happy Hour with rootly AI](https://luma.com/odgqf98e) \- New York \- Jun 17, 2026
- [ClickHouse Vancouver Meetup](https://luma.com/jr8tc94e) \- Jun 23, 2026
- [Apache Iceberg Seattle Meetup](https://luma.com/vwt2i2rs) \- Jun 25, 2026
- [AI Demo Night SF](https://luma.com/clickh-2crf) \- Jul 1, 2026
- [Happy Hour Open Source de Montreal](https://luma.com/clickh-o8up) \- Jul 9, 2026


### Events in EMEA [\#](/blog/202605-newsletter#events-in-emea)


- [AWS Summit](https://clickhouse.com/company/events/202605-EMEA-DACH-Germany-Hamburg-AWS-Summit-Hamburg) \- Hamburg \- May 19, 2026
- [London In\-Person Training: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202605-EMEA-London-Real-time-Analytics-w-ClickHouse) \- London \- May 19, 2026
- [Google Summit Madrid](https://clickhouse.com/company/events/202605-EMEA-SPIGT-Spain-GoogleSummit-Madrid) \- Madrid \- May 28, 2026
- [Money 2020](https://europe.money2020.com/) \- Amsterdam \- Jun 2, 2026
- [AWS Summit Madrid](https://clickhouse.com/company/events/202605-EMEA-SPIGT-Spain-AWSSummitMadrid) \- Madrid \- Jun 4, 2026
- [Hands\-on Workshop](https://luma.com/0stvf1vi) \- Tel Aviv \- Jun 9, 2026
- [Google Cloud AI Live](https://cloudonair.withgoogle.com/events/cloud-ai-live-amsterdam-2026) \- Amsterdam \- Jun 11, 2026
- [Benelux CDO Network](https://thenetwork-group.com/benelux-chief-data-officer-network/) \- Amsterdam \- Jun 15, 2026
- [Vivatech](https://vivatech.com/) \- Paris \- Jun 17, 2026
- [The Agentic Data Stack](https://clickhouse.com/company/events/202606-EMEA-Benelux-Amsterdam-The-Agentic-Data-Stack) \- Amsterdam \- Jun 18, 2026
- [TDWI](https://www.tdwi-konferenz.de/) \- Munich \- Jun 23, 2026


### Events in APAC [\#](/blog/202605-newsletter#events-in-apac)


- [Findy VPoE Summit](https://clickhouse.com/company/events/202605-APJ-3P-Tokyo-FindyVPoESummit) \- Tokyo \- May 22, 2026
- Bangkok OSS \& Data Evening \- Bangkok \- May 27, 2026
- [AWS Summit Mumbai](https://clickhouse.com/company/events/202605-APJ-3P-Mumbai-AWSSummit) \- Mumbai \- May 28, 2026
- [AWS Summit Bangkok](https://clickhouse.com/company/events/202605-APJ-3P-Bangkok-AWSSummit) \- Bangkok \- May 28, 2026
- [AI Engineering Summit](https://clickhouse.com/company/events/202606-APJ-3P-Tokyo-FindyAIEngineeringSummit) \- Tokyo \- Jun 8, 2026
- [SuperAI](https://clickhouse.com/company/events/202606-APJ-3P-Singapore-SuperAI) \- Singapore \- Jun 10, 2026
- [Gartner Data \& Analytics Summit Sydney](https://clickhouse.com/company/events/202606-APJ-3P-Sydney-GartnerData-and-Analytics) \- Sydney \- Jun 16, 2026
- [AWS Summit Hong Kong](https://clickhouse.com/company/events/202606-APJ-3P-HongKong-AWSSummit) \- Hong Kong \- Jun 17, 2026
- [KubeCon \+ CloudNativeCon India](https://clickhouse.com/company/events/202606-APJ-3P-Mumbai-KubeCon) \- Mumbai \- Jun 18, 2026
- [KCD Kuala Lumpur](https://clickhouse.com/company/events/202606-APJ-3P-KualaLumpur-KCD) \- Kuala Lumpur \- Jun 27, 2026
- [DataEngBytes Melbourne](https://clickhouse.com/company/events/202607-APJ-3P-Melbourne-DataEngBytes) \- Melbourne \- Jul 23, 2026
- [DataEngBytes Sydney](https://clickhouse.com/company/events/202607-APJ-3P-Sydney-DataEngBytes) \- Sydney \- Jul 28, 2026
- [Google Cloud Next Tokyo](https://clickhouse.com/company/events/202607-APJ-3P-Tokyo-GoogleNext) \- Tokyo \- Jul 30, 2026
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
