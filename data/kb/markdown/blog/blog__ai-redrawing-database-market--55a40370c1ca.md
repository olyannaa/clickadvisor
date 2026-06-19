# AI is redrawing the database market


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# AI is redrawing the database market

![TanyaBragin.jpeg](/_next/image?url=%2Fuploads%2FTanya_Bragin_84bf5232c3.jpeg&w=96&q=75)[Tanya Bragin](/authors/tanya-bragin)Mar 17, 2026 · 13 minutes read## Summary

- Adopting AI means not only re\-thinking user experiences, but also getting your data strategy right. If you do not, your AI initiatives will fail.
- AI workloads demand high\-concurrency, real\-time query processing, and full\-fidelity data at scale. Legacy batch\-oriented architectures weren't built for it.
- Previously siloed use cases, such as data warehousing and observability, are converging at the data layer.
- ClickHouse is evolving into a unified platform for powering AI workloads across AI Apps, AI Analyst, and AI SRE experiences… read on for more.
AI isn't just another workload on top of your data platform. It fundamentally changes workload expectations across every existing use case.


The three big shifts happening right now are: 1\) Applications are becoming agentic, 2\) Analytics interfaces are becoming conversational, 3\) Observability is shifting from static dashboards to AI\-driven investigations. In each case, the underlying data requirements converge around high concurrency, real\-time query performance, and full\-fidelity data at scale.


These are not requirements that incumbent data platforms were designed for. The data platform choices made over the next few years will shape what's possible: how fast teams can move, what products can be built, what insights are accessible to your business. The question worth asking now is not just whether your current platform handles today's workloads, but whether it's the right foundation for what AI\-driven applications actually demand.


In a [previous post](https://clickhouse.com/blog/the-unbundling-of-the-cloud-data-warehouse), I wrote about the unbundling of the cloud data warehouse — how the shift toward interactive, customer\-facing applications exposed the architectural mismatch between batch\-oriented warehouses and real\-time workloads. What I want to describe here is the next wave of that disruption, across three markets: real\-time analytics, data warehousing, and observability.


![Data-platform-AI.png](/uploads/Data_platform_AI_67dafd4b5a.png)
## Real\-time analytics: The dawn of the "best of breed" database [\#](/blog/ai-redrawing-database-market#real-time_analytics)


**Stakeholders: Developers building next\-generation user\-facing and AI\-powered applications**


Postgres has become the default database for building modern user\-facing applications, because of its superior ability to handle row\-oriented transactional data. This worked fine until applications became genuinely data\-intensive, driven by real\-time dashboards, usage analytics, customer\-facing metrics, event streams with millions of rows per second. For these increasingly analytical workloads, Postgres alone stopped scaling. The queries were too slow, the indexes too expensive, the concurrency too low.


The solution the industry landed on was Postgres \+ ClickHouse: Postgres for transactions and application state, ClickHouse for analytics. This pairing became the de facto modern data stack for any customer\-facing application with serious analytical requirements. ClickHouse evolved to be the obvious choice for analytical workloads: fast ingestion, sub\-second queries on billions of rows, efficient at the concurrency levels customer\-facing applications demand. The data moved from Postgres to ClickHouse via [CDC pipelines](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database), and ClickHouse powered everything from embedded product analytics to customer\-facing dashboards.


Now AI is accelerating the need for a best\-in\-class transactional and analytical base for building modern AI applications and agents that power them. LLM\-based features including AI\-generated insights, anomaly detection, recommendations, and natural language interfaces to product data, require a tighter feedback loop between transactional writes and analytical reads. This is why we are doubling down and [building a native Postgres \+ ClickHouse](https://clickhouse.com/blog/postgres-managed-by-clickhouse) data stack: a single unified experience where Postgres handles transactional workloads and ClickHouse handles analytics, tightly integrated at the engine level via a native extension – for automatic data replication and management and a unified developer experience.


For platform decision\-makers building customer\-facing experiences, the trajectory is clear – transactional and analytical capabilities at the datastore layer are required. And tight integration between transactional and analytical capabilities, without losing "best of breed" benefits, is an additional advantage speeding up developer workflow and enabling you to ship new AI\-powered capabilities faster.


![](/uploads/ai_march2026_2_6b0c8065e3.jpg)
## Data warehousing: AI Analyst workloads break batch\-oriented DWH architectures [\#](/blog/ai-redrawing-database-market#data_warehousing)


**Stakeholders: Data engineering teams modernizing data warehousing and business analytics**


In the [unbundling post](https://clickhouse.com/blog/the-unbundling-of-the-cloud-data-warehouse), I described how cloud data warehouses like Snowflake were architected for batch ingestion, heavy ETL, and periodic reporting, and how that made them a poor fit for interactive, customer\-facing applications.


Now the role of traditional data warehouses is being questioned in their "bread\-and\-butter" use case with the advent of the "AI Analyst" \- business analytics starting with natural language prompts deriving downstream assets, including ad\-hoc reports and dashboards.


[Agent\-facing analytics](https://clickhouse.com/blog/agent-facing-analytics), powered by text\-to\-SQL tools and natural language analytics interfaces are moving from experimentation to production. The UX implication is obvious: users ask questions in plain English and expect answers in seconds. The infrastructure implication is less obvious but more consequential: each natural language query doesn't just generate one SQL query — it can trigger dozens in rapid succession, as it explores available datasets and reasons through many parallel possibilities. What looks like a single user question becomes a burst of concurrent database queries. As a result, internal analyst\-generated workloads start to resemble external customer\-facing workloads – high\-concurrency, low\-latency, interactive responses. The same pattern extends to agents autonomously querying data platforms to find the right data points to base a decision on while solving a problem.


This inverts the assumptions that legacy data warehouse architectures are built around. Platforms like Snowflake and Databricks were designed for ad\-hoc, batch\-oriented analytics. Their compute models assume queries are infrequent and non\-interactive in nature. They optimize for high overall throughput across many queries, not high concurrency and low latency for each query. AI analyst experiences make queries fast and very frequent, and running that workload on a legacy DWH architecture means either unacceptable latency, making the AI assistant feel slow, or costs that scale faster than the value delivered.


ClickHouse was built from the ground up to excel at these requirements: petabyte\-scale data, high query concurrency, sub\-second response times. It was designed to serve thousands of concurrent users running interactive queries against billions of rows, not occasional analysts running batch reports. It turns out these are exactly the properties the agentic era demands.


For teams making long\-term platform bets, the calculus is straightforward: AI\-powered business analytics is not a future possibility, it is already here. The platforms that were right for the previous era of batch reporting do not meet its technical requirements. The switching costs of migrating off legacy data warehousing systems are real, but finite. The cost of spending the next five years on the wrong platform, paying a concurrency tax while competitors run interactive AI analytics, is larger.


![](/uploads/ai_march2026_3_69dc9fcbf2.jpg)
## Observability: AI SRE demands granular data at scale [\#](/blog/ai-redrawing-database-market#observability)


**Stakeholders: Platform and infrastructure teams owning observability strategy**


The traditional observability stack is built around three separate pillars (metrics, logs, and traces) each stored in its own specialized system. That architecture made sense when storage and compute were expensive: you pre\-aggregated metrics, sampled logs, and kept trace retention short to control costs. The tradeoff was manageable.


AI SRE workflows disrupt this model by introducing two new pressures: a high volume of concurrent natural language queries and a constant need for granular, high\-cardinality, long\-retention data to drive automated incident triage, root cause analysis and anomaly correlation. Sampled logs and downsampled metrics are not useful for an AI agent trying to correlate an error pattern with a deployment event from three days ago. The more capable you want your AI tooling to be, the more data you need to keep, and the more the cost structure of incumbent platforms works against you.


This is the core shift that Charity Majors has been describing as [Observability 2\.0](https://charity.wtf/tag/observability-2-0/): replacing the three\-pillar model with a single source of truth based on wide structured events stored in a columnar storage engine. Rather than pre\-deciding what questions you'll ask and pre\-aggregating for them, you store full\-fidelity events and derive metrics, traces, and SLOs from them at query time. Every modern observability company is now built on this model, and many use ClickHouse as the main storage engine.


Traditional observability players like Datadog are facing a real "innovator's dilemma" here. As they are priced on data volumes and significantly rate\-limit their platforms, their customers have been trained to ingest *less* data — sampling logs, downsampling metrics, limiting trace retention — to control costs. Reducing per\-GB pricing to enable AI SRE workflows means cannibalizing the revenue model the business is built on. Rebuilding around wide events and columnar storage means abandoning the specialized data structures and pricing mechanics they've scaled for decades.


ClickHouse, on the other hand, is uniquely well\-suited here for straightforward reasons: high compression on log and event data, sub\-second queries on high\-cardinality wide events, efficient at the ingestion volumes that production infrastructure generates, and a cost model based on compute and storage rather than per\-GB data ingestion fees.


This is also why we are investing in a turnkey observability stack, [ClickStack](https://clickhouse.com/clickstack), observability based on OpenTelemetry and ClickHouse, with an opinionated UI and AI SRE capabilities, available both in [open source](https://clickhouse.com/docs/use-cases/observability/clickstack/getting-started/oss) and as a [managed offering](https://clickhouse.com/blog/introducing-managed-clickstack-beta).


![](/uploads/ai_march2026_4_144b78aea2.jpg)
## Observability and DWH are converging: Two markets, one architecture [\#](/blog/ai-redrawing-database-market#observability_and_dwh)


Data warehousing and observability have been treated as separate domains for the last decade: separate buyers, separate vendors, separate stacks. And historically, that separation made some technical sense: storage backends, user interface, and consumption patterns. Even the datasets were different, because at first few businesses were fueled by their online presence.


Today, this separation is an outdated convention rather than a technical necessity. On the storage side, virtually all modern data platforms, whether business analytics or observability, now write to object stores. And the compute engines require interactive, low latency queries at high concurrency, as well as support for AI Analyst or AI SRE capabilities.


Finally, in the past, most teams treated observability data as purely operational. But in reality today, API calls are purchases and errors are failed transactions. Instead of looking at the same source of truth, the same events are often being stored twice, on two platforms, by two teams, with a fragile synchronization layer in between.


Teams that reframe all of it as business data, stored once in open formats and queryable by both AI Analyst and AI SRE tooling, eliminate that duplication and unlock context that neither silo had alone.


![](/uploads/ai_march2026_5_e7e91c2ca3.jpg)
## The platform layer: Agentic analytics and LLM observability [\#](/blog/ai-redrawing-database-market#the_platform_layer)


A complete data platform in 2026 is more than just a database. It is a database plus the tools that make it accessible to AI agents and the instrumentation to understand how those agents behave.


Two things are happening simultaneously. First, AI agents are becoming the primary interface to data. Users increasingly don't write SQL, but instead ask questions in natural language, and agents decompose those questions into queries, execute them, and synthesize results. This means a data platform needs to expose its capabilities to agents natively: ready\-made UIs, MCP\-compatible APIs, agent frameworks that can reach into your data without bespoke integration work for every use case. This is why we acquired [LibreChat](https://clickhouse.com/blog/librechat-open-source-agentic-data-stack), the leading open\-source AI chat platform, and made it a core component of what we call the Agentic Data Stack. LibreChat combined with ClickHouse gives teams a turnkey way to deploy analytics agents over their data, without building the agent layer from scratch.


Second, as AI agents proliferate, understanding and governing how they behave becomes a first\-order engineering problem. LLM observability (tracing agent execution, monitoring model performance, tracking costs, debugging failures across multi\-step agentic workflows) is not optional infrastructure. It is the difference between running AI in production with confidence or having it get stuck in the POC/experimentation stage. The observability problem for agentic systems is harder than for traditional software: the execution graphs are dynamic, the inputs and outputs are high\-dimensional, and failures are often subtle rather than binary. [Langfuse](https://clickhouse.com/blog/langfuse-llm-analytics), which runs on ClickHouse Cloud to power real\-time LLM observability at scale, is solving this problem.


![AI is Redrawing the Database Market #1409.jpg](/uploads/AI_is_Redrawing_the_Database_Market_1409_eac7cc339d.jpg)
For platform decision\-makers, the takeaway is clear: the database is necessary, but not sufficient. The complete picture includes agent\-ready interfaces and LLM observability tooling, natively integrated into the data platform experience.


## A unified data platform for interactive AI\-driven applications [\#](/blog/ai-redrawing-database-market#a_unified_data_platform)


ClickHouse is evolving into what we see as the **unified data platform for interactive AI\-driven applications**: one platform that handles transactional and analytical workloads, modern real\-time data warehousing and conversational BI, and evolving AI\-SRE driven observability workflows, at the performance and cost profile that AI\-native applications demand.


The market is moving fast, and the platforms winning the next era are already visible. The question for every team making long\-term infrastructure decisions is whether they are making the right bet now, while the switching costs are manageable, or whether they will be making a harder, more expensive decision later.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-105-get-started-today-sign-up&utm_blogctaid=105)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
