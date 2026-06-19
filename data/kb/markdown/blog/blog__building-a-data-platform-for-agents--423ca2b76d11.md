# How we’re building a data platform for a new user: agents


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How we’re building a data platform for a new user: agents

![Al Brown](/_next/image?url=%2Fuploads%2Fal_brown_headshot_09ae0cbce6.jpg&w=96&q=75)[Al Brown](/authors/al-brown)Mar 27, 2026 · 14 minutes readOne of the most important shifts in software right now is that [AI agents are becoming a new kind of database user](https://clickhouse.com/blog/agent-facing-analytics). Traditional analytics workflows are built around people. A business user asks a question, an analyst writes SQL, a dashboard gets built, and the answer arrives later. Agents change that loop. They inspect available tools, reason over schema, generate SQL, run queries, observe the results, and iterate in seconds.


![ai_march2026_3_69dc9fcbf2.jpg](/uploads/ai_march2026_3_69dc9fcbf2_31969e1512.jpg)
This new user needs a data platform that can keep up: real\-time ingestion, fast aggregation, flexible handling of semi\-structured events, low\-latency concurrency, and economics that still work at massive scale. ClickHouse already has this foundation. Not because we pivoted to AI, but because the things ClickHouse has always been good at happen to match the shape of modern AI workloads surprisingly well.


What changes is *how* this new user interacts with the database. Agents need better discoverability, query patterns tuned for exploratory AI workflows, LLM\-friendly documentation, stronger server\-side state and memory patterns, and access control designed around short\-lived, task\-scoped permissions. There is a lot of iteration ahead. But the direction is clear.


## The Agentic Data Stack [\#](/blog/building-a-data-platform-for-agents#the-agentic-data-stack)


Building for this new user means rethinking the workflow. The old pattern, someone asks a question, an analyst writes SQL, a dashboard gets built, is too slow when the consumer is an agent that can reason and iterate in seconds. The Agentic Data Stack is our view of what replaces it.


It has three layers: LibreChat as the chat interface, ClickHouse plus MCP as the data layer, and Langfuse for LLM observability. LibreChat gives teams a provider\-agnostic, MCP\-connected interface for conversational analytics. ClickHouse plus MCP makes the database queryable as part of an agent's reasoning loop. And Langfuse, which itself already runs on ClickHouse, adds tracing, prompt management, and cost and latency monitoring. Together they form a practical reference architecture for [agentic analytics](https://clickhouse.com/blog/agent-facing-analytics).


![AI_is_Redrawing_the_Database_Market_1409_eac7cc339d.jpg](/uploads/AI_is_Redrawing_the_Database_Market_1409_eac7cc339d_90321404d6.jpg)
We have written about this architecture in more detail in [The Agentic Data Stack](https://clickhouse.com/blog/the-agentic-data-stack) and the [Langfuse acquisition announcement](https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability).


### We are using this stack ourselves [\#](/blog/building-a-data-platform-for-agents#we-are-using-this-stack-ourselves)


Internally, we built DWAINE, the Data Warehouse AI Natural Expert, on this architecture. It connects LibreChat to our ClickHouse data warehouse through MCP, with a comprehensive business glossary to give the model context on our data model and business logic. It now serves more than 250 users, sees more than 200 daily messages, handles roughly 70% of data warehouse questions, and has reduced analyst workload by an estimated 50 to 70%. We wrote about the full build in [How we made our internal data warehouse AI\-first](https://clickhouse.com/blog/ai-first-data-warehouse).


We also made that experience public through [AgentHouse](https://clickhouse.com/blog/agenthouse-demo-clickhouse-llm-mcp) at [`llm.clickhouse.com`](http://llm.clickhouse.com), where anyone can query dozens of public datasets in natural language and see ClickHouse plus MCP in action.


## Releases for agents and agentic developers [\#](/blog/building-a-data-platform-for-agents#releases-for-agents-and-agentic-developers)


Beyond the big\-picture architecture, we have already shipped a concrete set of tools for agents and their teams building with ClickHouse.


### [Agentic Data Stack quickstart](https://clickhouse.com/blog/the-agentic-data-stack) [\#](/blog/building-a-data-platform-for-agents#agentic-data-stack-quickstart)


We published the Agentic Data Stack as a one\-command, composable Docker deployment. It bundles LibreChat, ClickHouse, and Langfuse into a setup that teams can run on their own infrastructure. The components are pre\-wired, so LibreChat can talk to ClickHouse through MCP and Langfuse can trace interactions from the start.


That local\-first, open architecture matters. Teams can keep their data in their own ClickHouse deployment, choose any model provider they want, and avoid stitching together a stack from scratch just to begin experimenting.


### [ClickHouse MCP servers](https://clickhouse.com/blog/clickhouse-cloud-joins-aws-ai-agents-and-tools-mcp) [\#](/blog/building-a-data-platform-for-agents#clickhouse-mcp-servers)


We ship both an open\-source ClickHouse MCP server and a remote MCP server for ClickHouse Cloud.


The open\-source server gives agents the ability to list databases, inspect tables, and run queries through a standard MCP interface. It is read\-only by default and designed to work with MCP\-compatible clients such as Claude Desktop, Cursor, Windsurf, and custom agents. It also supports chDB for querying local files and URLs without a full ETL flow.


The remote MCP server extends that model into ClickHouse Cloud, letting teams expose analytical data to AI tools without having to deploy and manage an MCP server themselves.


### [chDB 4](https://clickhouse.com/blog/chdb.4-0-pandas-hex) [\#](/blog/building-a-data-platform-for-agents#chdb-4)


We also pushed ClickHouse into a more embedded, developer\-friendly shape with chDB 4\.


chDB is the embedded ClickHouse engine, and version 4 introduced a Pandas\-like DataStore API. That matters for AI because LLMs are already very good at generating Pandas\-style code. chDB 4 lets developers keep that ergonomic surface while executing on the ClickHouse engine, with optimizations such as lazy execution, filter pushdown, and column pruning under the hood.


In other words, it closes part of the gap between what language models naturally produce and what high\-performance analytics systems want to execute.


### ClickHouse Assistant [\#](/blog/building-a-data-platform-for-agents#clickhouse-assistant)


We also built the agent experience directly into the product. ClickHouse Assistant is a co\-pilot inside the ClickHouse Cloud SQL Console, designed for ad\-hoc agentic analytics. It is loaded with ClickHouse Agent Skills so its recommendations follow ClickHouse best practices out of the box. It supports a context selector using `@` syntax, letting users scope conversations to specific databases, tables, or saved queries. It also supports `AGENTS.md` files, so teams can define domain\-specific instructions that the assistant picks up automatically.


Behind the scenes, we are also building a native RAG API and working on custom domain skills, both still in progress but aimed at the same goal: making the assistant context\-aware enough to be genuinely useful for real analytical work, not just SQL generation.


### [ClickHouse Agent Skills](https://clickhouse.com/blog/introducing-clickhouse-agent-skills) [\#](/blog/building-a-data-platform-for-agents#clickhouse-agent-skills)


General\-purpose models can write SQL, but they can often struggle to get the best practices right across different databases. They can make predictable mistakes around schema design, partitioning, ordering keys, joins, materialized views, and ingestion patterns.


To close that gap, we shipped ClickHouse Agent Skills: an open\-source package of prioritized best practices that can be installed into your agent environments. The Skills significantly improve an agent's ability to get the most out of ClickHouse, and allow us to continually refresh knowledge as things change.


### IDE integrations [\#](/blog/building-a-data-platform-for-agents#ide-integrations)


We also moved this closer to where developers already work.


The [ClickHouse Cursor plugin](https://github.com/ClickHouse/clickhouse-cursor-plugin) packages ClickHouse agent guidance and MCP configuration directly into Cursor workflows. The [ClickHouse Kiro Power](https://github.com/ClickHouse/clickhouse-kiro-power) does the same in Kiro, exposing ClickHouse tools and best\-practice guidance inside the IDE. Database interaction is becoming part of the coding agent loop, not a separate activity.


### LLM\-accessible content [\#](/blog/building-a-data-platform-for-agents#llm-accessible-content)


We have also started making our written content directly consumable by agents. Every blog post and guide on clickhouse.com is available as clean Markdown, and we publish an llms.txt file so that agents and crawlers can discover and navigate our content programmatically. We are also investigating automatically serving Markdown to known LLM user\-agents, so that when an agent fetches a ClickHouse page it gets structured text rather than a full HTML document.


As agents are becoming a primary consumer of technical content, the content should be shaped to serve them well.


### Agent\-friendly docs [\#](/blog/building-a-data-platform-for-agents#agent-friendly-docs)


We have applied the same thinking to our documentation. The ClickHouse docs already serve an `llms.txt` file and a docs MCP server is behind our Ask AI feature.


Soon, we will be adding one\-click MCP server connections from docs pages, `llms-full.txt`, content negotiation to serve Markdown instead of HTML when an agent visits the site, the ability to append `.md` to any URL to view raw Markdown, a semantic search tool exposed to agents as a tool call so they can find information by intent rather than keyword, and per\-page context menus that let users open conversations in popular AI chat interfaces with page context pre\-filled.


### [clickhouse.build](https://clickhouse.com/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps) [\#](/blog/building-a-data-platform-for-agents#clickhousebuild)


We shipped an experimental agent, clickhouse.build, an agentic CLI that used multiple agents to inspect a Postgres\-backed application, identify candidate analytical workloads, set up real\-time syncing, and adapt the application code.


It launched just before Anthropic introduced Agent Skills as a pattern for encoding reusable agent workflows. It has helped us to learn a lot about the boundaries of shipping custom agents, and perhaps that these migration and evaluation flows might now be better expressed as composable skills. The lessons from clickhouse.build are feeding directly into how we think about packaging ClickHouse guidance for agents going forward.


## AI runs on data, and that data runs on ClickHouse [\#](/blog/building-a-data-platform-for-agents#ai-runs-on-data-and-that-data-runs-on-clickhouse)


Some of the most demanding AI companies in the world are already running core workloads on ClickHouse.


[OpenAI uses ClickHouse for petabyte\-scale observability](https://clickhouse.com/blog/why-openai-uses-clickhouse-for-petabyte-scale-observability). Their systems ingest petabytes of log data per day, growing more than 20% month over month. When GPT\-4o image generation launched and log volume jumped 50% overnight, ClickHouse absorbed the spike. Their deployment runs across 90 shards with 2 replicas each, and even low\-level optimizations paid off at that scale.


[Anthropic has said ClickHouse "played an instrumental role" in helping them develop and ship Claude 4\.](https://clickhouse.com/blog/how-anthropic-is-using-clickhouse-to-scale-observability-for-ai-era) They run ClickHouse in custom air\-gapped environments to satisfy stringent safety requirements, and a team of just three people managed the entire observability stack through rapid growth. Claude itself recommended ClickHouse when they were evaluating solutions.


[Character.AI processes more than 450 petabytes of raw log data per month across thousands of GPUs](http://Character.AI). After moving to ClickHouse, they were able to store 10x more data while cutting costs by 50%.


[Lovable](https://clickhouse.com/blog/lovable-ai-powered-observability) built its analytics pipeline with remarkable speed and now uses ClickHouse in its AI\-native product. [Poolside](https://clickhouse.com/blog/poolside-using-clickhouse-to-build-next-gen-ai-for-software-development) uses ClickHouse to work across billions of documents and code artifacts for next\-generation code models. [Sierra](https://clickhouse.com/blog/sierra-observability-analytics) uses ClickHouse to unify observability and analytics for customer\-facing AI agents. [Memorial Sloan Kettering Cancer Center](https://clickhouse.com/blog/how-memorial-sloan-kettering-cancer-center-is-using-clickhouse-to-accelerate-cancer-research) uses ClickHouse to accelerate genomic research over billions of data points.


These companies did not choose ClickHouse because it had an "AI" label on it. They chose it because AI workloads are, at their core, hard data workloads.


## Guides and further reading [\#](/blog/building-a-data-platform-for-agents#guides-and-further-reading)


We have published detailed guides covering the ideas and tools in this post.


[**The Agentic Data Stack**](https://clickhouse.com/blog/the-agentic-data-stack) explains the full architecture: why conversational analytics needs a chat layer, a data layer, and an observability layer, and how LibreChat, ClickHouse, and Langfuse fit together.


[**Introducing AgentHouse**](https://clickhouse.com/blog/agenthouse-demo-clickhouse-llm-mcp) is the story behind `llm.clickhouse.com`, a public demo where anyone can query dozens of real datasets in natural language using ClickHouse and MCP.


[**Integrating with ClickHouse MCP**](https://clickhouse.com/blog/integrating-clickhouse-mcp) walks through connecting the ClickHouse MCP server to clients like Claude Desktop, Cursor, and custom agents, with practical setup and usage examples.


[**How we made our internal data warehouse AI\-first**](https://clickhouse.com/blog/ai-first-data-warehouse) covers the full DWAINE build: architecture decisions, security model, what worked, and where traditional BI still wins.


[**How to set up ClickHouse for agentic analytics**](https://clickhouse.com/blog/how-to-set-up-clickhouse-for-agentic-analytics) is the operational guide. It covers curated marts, resource guardrails, agent\-facing roles, and the warehouse design changes that matter when your user is an LLM.


[**AI\-generated ClickHouse schemas: mistakes and advice**](https://clickhouse.com/blog/ai-generated-clickhouse-schemas-mistakes-and-advice) documents the predictable mistakes LLMs make around partitioning, ordering keys, codecs, and engine choice, and how to catch them before they hit production.


[**Define once, use everywhere: a metrics layer for ClickHouse with MooseStack**](https://clickhouse.com/blog/metrics-layer-with-fiveonefour) shows how to define metrics once in a semantic layer and expose them consistently to both agents and dashboards.


[**AI\-powered migrations from Postgres to ClickHouse**](https://clickhouse.com/blog/ai-powered-migraiton-from-postgres-to-clickhouse-with-fiveonefour) walks through using AI agents to inspect a Postgres application, identify analytical workloads, and generate a working ClickHouse migration.


## Where this is going [\#](/blog/building-a-data-platform-for-agents#where-this-is-going)


Our vision is that ClickHouse should be the data engine that AI agents interact with as naturally as human analysts do today. The Agentic Data Stack is a practical implementation of that vision, an open, composable architecture where conversation, data access, and observability work together.


But the impact of AI on databases goes well beyond conversational analytics. As we wrote in [AI is redrawing the database market](https://clickhouse.com/blog/ai-redrawing-database-market), AI is changing workload expectations across every major use case. In real\-time analytics, AI\-powered application features are tightening the feedback loop between transactional writes and analytical reads. In data warehousing, agent\-facing analytics turns what used to be occasional batch queries into bursts of high\-concurrency, low\-latency requests that break the assumptions legacy platforms were built on. In observability, AI\-driven investigation requires full\-fidelity data at granularity levels that pre\-aggregation and sampling cannot support.


Across all three, the requirements converge: high concurrency, real\-time query performance, and full\-fidelity data at scale. Those are the same properties that ClickHouse was built around from the start.


This is a fast\-moving space. A lot of what we are doing is experimenting, listening to the market and our users, and discovering where AI adds real value and where it does not. That is why companies like OpenAI, Anthropic, Character.AI, Lovable, and Sierra choose to build on ClickHouse. Not because we put an AI label on it, but because the foundation was already right.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
