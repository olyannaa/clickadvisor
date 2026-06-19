# February 2026 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# February 2026 newsletter

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Feb 19, 2026 · 9 minutes readHello, and welcome to the February 2026 ClickHouse newsletter!


This month, we have ClickHouse’s $400M Series D, the release of the official Kubernetes operator, a data modelling guide, how ClickHouse optimizes Top\-N queries, and more!


## Featured community member: Ino de Bruijn [\#](/blog/202602-newsletter#featured-community-member)


This month's featured community member is Ino de Bruijn, Data Visualization Team Lead at Memorial Sloan Kettering Cancer Center's Cancer Data Science Initiative.


![](/uploads/feb2026_nl_image1_a784b3580c.png)
Ino leads a team of engineers building software tools for cancer research, visualizing and disseminating data from major consortia including HTAN, Break Through Cancer, AACR GENIE, and the Gray BRCA Pre\-Cancer Atlas.


For nearly 11 years, he's also been instrumental in developing cBioPortal \- the most popular cancer genomics tool worldwide, with over 3,000 daily users and more than 25,000 citations.


At the ClickHouse New York Meetup in December, [Ino presented on his team's work](https://clickhouse.com/videos/nymeetupdec82025) building a conversational AI interface for cBioPortal using ClickHouse, Anthropic's Claude, and LibreChat \- a fully open\-source solution making cancer research data more accessible to researchers and clinicians.


➡️ [Connect with Ino on LinkedIn](https://www.linkedin.com/in/inodb/)


## Upcoming events [\#](/blog/202602-newsletter#upcoming-events)


### Global virtual events [\#](/blog/202602-newsletter#global-virtual-events)


- [v26\.1 Community Call](https://clickhouse.com/company/events/v25-12-community-release-call) \- 26th February
- [CDC ClickPipes: The Fastest Way to Replicate Your Database to ClickHouse](https://clickhouse.com/company/events/202602-APJ-Webinar-CDC-ClickPipes) \- 26th February
- [Under\-the\-Hood: ClickHouse Incremental Materialized Views and Dictionaries](https://clickhouse.com/company/events/202602-EMEA-Webinar-Materialized-Views) \- 4th March


### Virtual training [\#](/blog/202602-newsletter#virtual-training)


- [ClickHouse Query Optimization Workshop](https://clickhouse.com/company/events/202602-amer-emea-query-optimization) \- 19th February
- [chDB: Data Analytics with ClickHouse and Python](https://clickhouse.com/company/events/202603-AMER-EMEA-chDB:Data-Analytics-with-ClickHouse-and-Python) \- 18th March
- [Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202603-AMER-Real-time-Analytics-w-ClickHouse) \- 5th March


**Data Warehousing**


- [Data Warehousing with ClickHouse: Level 2](https://clickhouse.com/company/events/202602-AMER-data-warehousing-Level2) \- 25th February
- [Data Warehousing with ClickHouse: Level 1](https://clickhouse.com/company/events/202603-APJ-data-warehousing-Level1) \- 3rd March
- [Data Warehousing with ClickHouse: Level 2](https://clickhouse.com/company/events/202603-APJ-data-warehousing-Level2) \- 4th March
- [Data Warehousing with ClickHouse: Level 3](https://clickhouse.com/company/events/202603-APJ-data-warehousing-Level3) \- 5th March


### Events in AMER [\#](/blog/202602-newsletter#events-in-amer)


- [Toronto Meetup](https://www.meetup.com/clickhouse-toronto-user-group/events/312881151/?slug=clickhouse-toronto-user-group&eventId=310164482&isFirstPublish=true) \- 19th February
- [Seattle Meetup](https://luma.com/jsctpwoa) \- 26th February
- [LA Meetup](https://luma.com/wbkqmaqk) \- 6th March
- [Atlanta In\-person Training: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202603-AMER-Atlanta-Real-time-Analytics-w-ClickHouse) \- 5th March


### Events in EMEA [\#](/blog/202602-newsletter#events-in-emea)


- [ClickHouse Meetup in Tbilisi Georgia](https://www.meetup.com/clickhouse-georgia-meetup-group/events/312852206/) \- 24th February


### Events in APAC [\#](/blog/202602-newsletter#events-in-apac)


- [ClickHouse Melbourne Meetup](https://clickhouse.com/company/events/202602-APJ-Melbourne-Meetup) \- 24th February
- [Dink \& Data: Executive Pickleball Social, Singapore](https://clickhouse.com/company/events/202602-APJ-Singapore-DinkDataHappyHour) \- 25th February
- [Webinar: CDC ClickPipes: The Fastest Way to Replicate Your Database to ClickHouse](https://clickhouse.com/company/events/202602-APJ-Webinar-CDC-ClickPipes) \- 26th February
- [ClickHouse \+ GDG \+ Deutsche Bank Bangalore Meetup](https://www.meetup.com/clickhouse-bangalore-user-group/events/313325219/) \- 28th February
- [ClickHouse Tokyo Meetup \- LibreChat Night](https://www.meetup.com/clickhouse-tokyo-user-group/events/313275265/) \- 9th March
- [Data Streaming World Melbourne](https://clickhouse.com/company/events/202603-APJ-3PC-Melbourne-DataStreamingWorld) \- 5th March
- [Hackomania Singapore](https://hackomania.geekshacking.com/) \- 7th \- 8th March
- [PGConf India](https://pgconf.in/conferences/pgconfin2026) \- 11th \- 13th March
- [AWS Unicorn Day 2026 Seoul](https://clickhouse.com/company/events/202603-APJ-3PC-Seoul-AWSUnicornDay) \- 17th March
- [Python Asia 2026](https://2026.pythonasia.org/) \- 21st \- 23rd March


## 26\.1 release [\#](/blog/202602-newsletter#release)


![](/uploads/feb2026_nl_image6_adff8e72ed.png)
The first release of 2026 adds support for the sparseGrams tokenizer to the text index, which also now supports arrays of Strings or FixedStrings.


There’s support for the Variant data type in all functions, new syntax for indexing projections, deduplication of asynchronous inserts with materialized views, and more!


➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-26-01)


## ClickHouse raises $400M Series D, acquires Langfuse, and launches Postgres [\#](/blog/202602-newsletter#series_d)


![](/uploads/feb2026_nl_image7_c50bd14a9f.png)
ClickHouse closed a $400 million Series D funding round led by Dragoneer Investment Group, with participation from Bessemer Venture Partners, GIC, Index Ventures, Khosla Ventures, Lightspeed Venture Partners, T. Rowe Price Associates, and WCM Investment Management.


Alongside the funding announcement, ClickHouse [acquired Langfuse](https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability), an open\-source LLM observability platform with over 20K GitHub stars and more than 26M\+ SDK installs per month. Additionally, ClickHouse launched [an enterprise\-grade PostgreSQL service](https://clickhouse.com/blog/postgres-managed-by-clickhouse) integrated with its platform.


➡️ [Read the blog post](https://clickhouse.com/blog/clickhouse-raises-400-million-series-d-acquires-langfuse-launches-postgres)


## Provable Completeness: Guaranteeing Zero Data Loss in Trade Collection from Crypto Exchanges [\#](/blog/202602-newsletter#provable_completeness)


![](/uploads/feb2026_nl_image9_6dde790b1e.png)
Unreliable WebSocket connections and network interruptions create a persistent challenge to data quality in cryptocurrency market data collection. Koinju, a crypto platform built for finance professionals, ingests millions of trades per day across hundreds of markets. For their clients, even a single missing trade can distort volumes, P\&L calculations, risk exposures, and regulatory reports \- making data completeness non\-negotiable.


In this blog post, Dmitry Prokofyev, CTO of Koinju, describes a novel solution using only ClickHouse to detect and automatically remediate missing trades from Coinbase. The architecture combines three ClickHouse features to create a self\-healing system: Refreshable Materialized Views for detection, a separate validation service for REST API backfilling, and ReplacingMergeTree for automatic deduplication of resolved gaps.


➡️ [Read the blog post](https://koinju.io/blog/provable-completeness-how-we-achieve-zero-data-loss-in-trade-collection-from-crypto-exchanges)


## Introducing the Official ClickHouse Kubernetes Operator: Seamless Analytics at Scale [\#](/blog/202602-newsletter#kubernetes_operator)


![](/uploads/feb2026_nl_image5_891092f82b.png)
Grisha Pervakov introduces ClickHouse's official open\-source Kubernetes Operator, designed to simplify the deployment and management of ClickHouse clusters on Kubernetes.


The operator enables rapid provisioning of production\-ready clusters with built\-in sharding and replication capabilities while eliminating the need for separate ZooKeeper installations by using ClickHouse Keeper for cluster coordination.


➡️ [Read the blog post](https://clickhouse.com/blog/clickhouse-kubernetes-operator)


## AI\-Generated analytics without wrecking your cluster [\#](/blog/202602-newsletter#ai_generated_analytics)


![](/uploads/feb2026_nl_image4_f4c62f344a.png)
Luke from Faster Analytics Fridays outlines three guardrail patterns for safely enabling AI\-generated database queries without crashing clusters:


1. Using pre\-vetted query templates with parameter binding instead of raw SQL generation
2. Exposing curated materialized views rather than raw tables, and
3. Enforcing query budgets that validate estimated row scans and execution time before queries hit the database.


➡️ [Read the blog post](https://www.newsletter.hypequery.com/p/ai-generated-analytics-without-wrecking-your-cluster)


## Data modeling guide for real\-time analytics with ClickHouse [\#](/blog/202602-newsletter#data_modeling_guide)


![](/uploads/feb2026_nl_image3_0addcbc0a4.png)
Simon Späti has written a comprehensive guide to designing optimized data models in ClickHouse for sub\-second real\-time analytics, emphasizing that performance comes from shifting computational work from query time to insertion time.


The article covers core principles, including denormalization to minimize joins, partitioning by time and secondary dimensions for query pruning, and predicate pushdown optimization that moves filters closer to data sources.


➡️ [Read the blog post](https://www.ssp.sh/blog/practical-data-modeling-clickhouse/)


## PostgreSQL \+ ClickHouse as the Open Source unified data stack [\#](/blog/202602-newsletter#postgres_clickhouse)


![](/uploads/feb2026_nl_image2_90bf827bd5.png)  

Lionel Palacin introduces an open\-source unified data stack that combines PostgreSQL for transactional workloads with ClickHouse for analytics.
It uses PeerDB for near\-real\-time CDC replication and the pg\_clickhouse extension for transparent query offloading without rewriting SQL, enabling teams to start with PostgreSQL and add ClickHouse when analytical performance becomes critical.


➡️ [Read the blog post](https://clickhouse.com/blog/postgres-clickhouse-oss)


## Quick reads [\#](/blog/202602-newsletter#quick-reads)


- Mikhail Zharkov describes [building a scalable price distribution pipeline for trading systems using ClickHouse](https://mikhail-zharkov.medium.com/price-server-0b4da9d38f29).
- Abhinaav Ramesh [built Ollama\-Local\-Serve](https://medium.com/@contactabhinaav/building-a-self-hosted-llm-server-youll-actually-use-dae13111447a), a self\-hosted LLM server with complete observability, using ClickHouse for time\-series analytics, OpenTelemetry instrumentation, FastAPI monitoring APIs, and a React dashboard with streaming chat.
- Pranav Mehta describes [investigating ClickHouse connection retry warnings](https://medium.com/@pranavmehta94/clickhouse-internals-a-deep-dive-into-clickhouse-distributed-connection-pooling-d9e956b5eb57) in an on\-prem environment that initially appeared to be a critical connection leak but turned out to be expected behavior when the connection pool attempts to reuse stale connections after idle periods.
- Lionel Palacin [redesigned the data pipeline of ClickPy](https://clickhouse.com/blog/clickpy-2-trillion-rows), a ClickHouse\-backed service that contains 2\.2 trillion rows of Python package analytics. Data was previously ingested using custom batch scripts but has been migrated to ClickPipes and uses ClickHouse's lightweight deletes to correct historical data without rebuilding the entire dataset.
- Tom Schreiber explains [how ClickHouse optimizes Top\-N queries](https://clickhouse.com/blog/clickhouse-top-n-queries-granule-level-data-skipping) using granule\-level data skipping with min/max metadata filtering, achieving 5\-10× speedup and 10\-100× reduction in data processed.
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
