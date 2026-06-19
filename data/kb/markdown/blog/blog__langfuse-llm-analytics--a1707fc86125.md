# How Langfuse is scaling LLM observability for the agentic era with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Langfuse is scaling LLM observability for the agentic era with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Feb 3, 2026 · 11 minutes read## Summary


div.w\-full \+ p, 
pre \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

Langfuse uses ClickHouse Cloud to power real\-time observability and analytics for complex, agentic LLM applications at scale. Migrating from Postgres to ClickHouse Cloud cut query latency from minutes to near real\-time while supporting rapidly growing ingestion volumes. An upcoming shift to immutable, wide\-table modeling reduces memory usage by 3x and results in 20x faster analytical queries.

When [Langfuse](https://langfuse.com/) first shared its [journey from Postgres to ClickHouse](https://clickhouse.com/blog/langfuse-and-clickhouse-a-new-data-stack-for-modern-llm-applications) in March 2025, the challenge was clear. Their open\-source LLM engineering platform had outgrown a simple, developer\-friendly architecture, and the team needed a new data foundation to keep pace with rapidly scaling usage. ClickHouse became that foundation, allowing Langfuse to ingest and analyze orders of magnitude more data without sacrificing performance or flexibility.


By October, at our [Open House roadshow in Amsterdam](https://clickhouse.com/openhouse/amsterdam), the focus had naturally shifted. [ClickHouse Cloud](https://clickhouse.com/cloud) was running in production, and the questions were no longer about database choice. They were about how the shape of LLM applications themselves is changing, and what starts to break when systems that once handled millions of records are suddenly dealing with billions every month. As teams move from relatively simple RAG workflows to complex, agentic systems, observability must evolve along with them. The bottlenecks that matter most are no longer the obvious ones.


What followed was a field report from the frontier, tracing how Langfuse’s data model, ingestion patterns, and even SDK design have had to adapt as LLM applications continue to mature. As Langfuse co\-founder and CTO Max Deichmann puts it, “What we’re building is observability for engineering teams working on the most complex and advanced agentic systems.”


## When LLMs got complicated [\#](/blog/langfuse-llm-analytics#when-llms-got-complicated)


In the earliest days of production\-grade LLM applications, the architecture was relatively straightforward. A user query went into a retrieval system, a handful of documents came back, and those documents were passed to a model to generate a response. These RAG workflows were simple enough to reason about, and simple enough to observe.


But that simplicity didn’t last long. “People realized this is not enough,” Max says. If you want better answers, more reliability, or richer behavior, the system has to do more.


As teams pushed for higher\-quality outputs, they moved beyond single\-shot prompts toward agentic systems that plan, iterate, and interact with external tools. Now, an agent might call a search API, query a database, invoke an internal service, reassess its plan, and repeat the process several times before producing an answer.


Once applications cross that line, observability becomes a different story. Engineers are no longer simply asking whether a request succeeded. They want to know whether the agent took the right tool call, passed the right parameters, or planned the right next step. And because, as Max puts it, “LLMs don’t have predictable outcomes,” the same input can lead to different execution paths.


Langfuse is built around that reality. “Tracing is at our core,” Max says. The platform started with familiar trace trees, but expanded into graph views that show how an agent moves through its turns and tool calls over time, along with specialized rendering for [large prompts](https://langfuse.com/docs/prompt-management/overview), completions, and business\-level metadata.


From there, Langfuse moved beyond individual traces to analytics. Teams want to understand how latency, cost, and quality evolve across thousands or even millions of runs. They want to compare versions of an agent, test changes against production data, and see how behavior shifts over time. That’s why Langfuse added tools like datasets, which let users treat real traces as integration tests and [evaluate different agent versions](https://langfuse.com/docs/evaluation/overview) side by side.


Over the last two years, the product has grown into a full data platform that’s open by design, with [public APIs](https://langfuse.com/docs/api-and-data-platform/features/public-api) and export paths, supporting a growing ecosystem of teams building increasingly complex LLM systems. And all of that activity flows through one place: the database.


## From Postgres to ClickHouse [\#](/blog/langfuse-llm-analytics#from-postgres-to-clickhouse)


Langfuse’s previous architecture was intentionally simple: JavaScript and Python SDKs fed events into a single container backed by Postgres. Self\-hosting was easy, and the team could move fast without much operational overhead. Even so, it was clear they would outgrow the setup someday. “We always knew this would happen,” Max says.


By June 2024, ingestion volumes had “skyrocketed,” along with IOPS costs. The team was running the largest available instance, and it still wasn’t enough. Analytical queries timed out. The ingestion API got so slow that users complained their SDKs couldn’t send data reliably. As a single\-node database, Postgres was also an uptime risk. “We realized we needed to change Postgres,” he says, “or at least move the tracing data somewhere else.”


The team wrote a list of requirements: [columnar storage](https://clickhouse.com/docs/faq/general/columnar-database) for analytical queries, very high\-volume [insert throughput](https://clickhouse.com/docs/best-practices/selecting-an-insert-strategy), [multiple write and read nodes](https://clickhouse.com/docs/academic_overview), and [SQL](https://clickhouse.com/docs/sql-reference) so users could slice and dice their data at low latency. Because Langfuse is open\-source and widely self\-hosted, the database also had to be deployable anywhere under an OSS license. ClickHouse checked all those boxes.


They built a new pipeline with [SDKs](https://langfuse.com/docs/observability/sdk/overview) and an [OTel endpoint](https://langfuse.com/integrations/native/opentelemetry) feeding events into Redis queues and S3, async workers processing those events, and ClickHouse at the center as the analytical engine. “It worked surprisingly well at very high traffic,” Max says.


![Langfuse Issue 1225.jpg](/uploads/Langfuse_Issue_1225_f20eeb99d8.jpg)
Langfuse’s ingestion pipeline, moving SDK events through queues and storage into ClickHouse.


The turning point came quietly. “One Saturday afternoon, I decided to flip the switch and start reading data from ClickHouse,” Max recalls. The impact was immediate. “It was like minutes on Postgres, and then once I flipped it, latencies dropped right away.” The team wrote an extensive [blog post](https://langfuse.com/blog/2024-12-langfuse-v3-infrastructure-evolution) on that architecture transition.


Over the following year, the system continued to scale as adoption grew. Charts that once showed massive ingestion spikes now barely register. “What was big then is very small now,” Max says. “ClickHouse has served us really, really well.”


With the database no longer holding them back, new questions emerged: “What are our next steps?” Max asks. “Where are the bottlenecks we see today?”


## Lessons learned at scale [\#](/blog/langfuse-llm-analytics#lessons-learned-at-scale)


As Max shared at Open House, running Langfuse on ClickHouse surfaced a new class of problems that had less to do with raw throughput, and more to do with how data models and access patterns interact with real\-world usage.


One early lesson was that performance doesn’t stop at the database boundary. The team learned the importance of passing [primary keys](https://clickhouse.com/docs/best-practices/choosing-a-primary-key), especially timestamps, through frontend state, ensuring that every query hitting ClickHouse is as selective as possible. Small choices in how queries are shaped often matter just as much as how fast the database itself can run.


Another lesson was skepticism. Rather than assuming a single data model would work for everyone, Langfuse now spins up alternative models in separate ClickHouse services and tests them side by side using real production data. With users free to ingest almost anything, cardinality and distribution vary widely. “Test in production,” Max advises. “What works for one user doesn’t work for another one.”


They’ve also learned the value of isolating workloads. “[Compute\-compute separation](https://clickhouse.com/blog/introducing-warehouses-compute-compute-separation-in-clickhouse-cloud) is really helpful for us,” Max says. “If one ClickHouse cluster is under fire, the other one is still chill and can serve the UI for our users.” That separation makes performance more predictable and helps protect interactive queries from ingestion spikes.


The hardest lessons, though, came from mutability and joins. Langfuse’s original design allowed SDKs to emit multiple events per span: one capturing the model and input immediately, another arriving later with outputs and cost. That behavior matched how users expect LLM systems to work—calls can take time, and teams want visibility as soon as something happens—but it pushed Langfuse toward mutable tables and frequent deduplication.


[ReplacingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree) can be a “great” solution for this, Max says, but it comes with tradeoffs. “If you want to have very accurate data, you need to deduplicate whenever you read the data.” At the same time, frequent joins across massive trace and span tables added pressure of their own, pushing query complexity and latency higher as usage grew.


All this led Max to step back and ask: “Why do we even have mutable data? Why do we update? Because in traditional observability systems, people don’t update.” Those questions marked a turning point that would reshape how Langfuse models agent behavior and observability at scale.


## One immutable path forward [\#](/blog/langfuse-llm-analytics#one-immutable-path-forward)


For Langfuse, the answer lies in how user expectations have changed. While partial updates once mattered, “now people care more about the overall performance of agents rather than single calls,” Max says. That shift makes a new model possible.


Today, Langfuse is moving toward a wide, immutable observations table (called the “Events” table) that collapses trace\- and span\-level data into one structure. Metadata like user and session IDs are propagated directly into that table, making it much easier to query without joins.


Staying true to Max’s earlier advice, the team didn’t treat this as a theoretical improvement. “We tested this new table in production,” he says. Compared to the old approach, the new model delivered around three times less memory usage and up to 20 times faster queries.


The question now, Max says, is, “How do we get there?” Thousands of deployments still rely on older SDKs that emit multiple events per span. Langfuse can’t force everyone to upgrade. Instead, the team is running background jobs to backfill legacy data into the new schema, while newer SDKs write directly to the immutable table.


It’s an incremental transition, but a deliberate one. “This will help our users get very low latencies across the UI and also our APIs,” Max says.


A year ago, ClickHouse helped Langfuse escape the limits of a single\-node database. What followed is more subtle: removing hidden taxes in the data model, aligning ingestion with how users actually reason about agents, and continuously reshaping the system as LLM applications evolve.


As Max made clear in Amsterdam, scaling is less a destination than a moving target. With ClickHouse Cloud, Langfuse has the data foundation to keep adapting as that target moves.


## Langfuse joins ClickHouse [\#](/blog/langfuse-llm-analytics#langfuse-joins-clickhouse)


In the time since this story was drafted, [we announced that ClickHouse has acquired Langfuse](https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability), deepening the integration between Langfuse's LLM observability platform and ClickHouse's analytical capabilities.


The story of scaling observability for agentic systems continues \- now under one roof.

### Looking to scale your team’s data operations?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-51-looking-to-scale-your-team-s-data-operations-sign-up&utm_blogctaid=51)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
