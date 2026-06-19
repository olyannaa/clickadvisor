# ClickHouse Agents: Claude\-powered agentic analytics, now in public beta


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Agents: Claude\-powered agentic analytics, now in public beta

![](/_next/image?url=%2Fuploads%2FRyadh_d50dc0546c.png&w=96&q=75)[Ryadh Dahimene](/authors/ryadh-dahimene)Jun 9, 2026 · 11 minutes readAfter running agentic analytics in production for more than a year at ClickHouse, at [Open House 2026](https://clickhouse.com/blog/open-house-2026-day-1) in San Francisco, we announced the public beta of [ClickHouse Agents](https://clickhouse.com/docs/cloud/features/ai-ml/agents), a fully managed agentic analytics service in ClickHouse Cloud, powered by Claude.


ClickHouse Agents is a native AI experience inside ClickHouse Cloud. With ClickHouse Agents, you can build agents easily with no code required where users can ship agents grounded in their live ClickHouse data, with no SQL or setup required. You put those agents to work through a fully managed chat experience right in the Cloud console, with no setup and no separate environment to host.


## What ClickHouse Agents is [\#](/blog/clickhouse-agents-beta#what-clickhouse-agents-is)


ClickHouse Agents is built on [LibreChat](https://github.com/danny-avila/LibreChat), the battle\-tested open\-source AI platform, and runs fully managed inside ClickHouse Cloud. At its core is the no\-code agent builder, which lets anyone, whether analyst, PM, data engineer, or executive, define, configure, and ship agents grounded in their ClickHouse data. ClickHouse Agents also comes with an out\-of\-box chat interface, a sandboxed code interpreter, shareable artifacts, skills, memories, and multi\-agent workflows. Agents connect natively to ClickHouse and to any MCP\-compatible system, pulling context from wherever it already lives.

Loading video...What's included:


- **No\-code Agent Builder**: define agents with custom instructions, skills, context files, and MCP tool access, governed by your Cloud RBAC.
- **Chat interface**: a fully managed, multi\-tenant chat experience. Ask in natural language, generate SQL and visualizations, build artifacts, and run multi\-turn conversations against your data.
- **Sandboxed code interpreter**: secure Bash, Python and JavaScript [execution](https://clickhouse.com/docs/cloud/features/ai-ml/agents/builder/code-interpreter) inside any conversation, running against live query results without leaving the chat.
- **Claude, pre\-configured**: every Cloud customer gets Claude models (Sonnet and Haiku) wired in as the default model.
- **Skills, memories, and artifacts**: package repeatable workflows and context as skills, persist context with memories, and share charts and dashboards as artifacts.
- **Multi\-agent workflows**: orchestrate subagents across end\-to\-end analytical tasks.
- **Enterprise security**: SSO, encrypted message storage, and governed data access, built into the managed runtime.


## The ClickHouse Platform for AI [\#](/blog/clickhouse-agents-beta#the-clickhouse-platform-for-ai)


ClickHouse Agents is a piece of what we coined "the ClickHouse Platform for AI".


As every major cloud data platform is racing to make AI a native capability, most are doing it the same way: a walled garden where data and AI come bundled, proprietary, expensive, and locked to a single ecosystem of data constructs, models, agents, and tools. Given how fast this space is moving, we think that is the wrong direction and that openness and interoperability is key. The ClickHouse Platform for AI is an open stack, layered from the data up and served to apps, agents, users, and an API:


- **The data layer**: ClickHouse, the open\-source columnar engine that companies like [Shopify](https://clickhouse.com/videos/shopify-open-source-network-monitoring), [Uber](https://www.uber.com/us/en/blog/logging/), [Ramp](https://clickhouse.com/videos/ramp), [Anthropic](https://clickhouse.com/blog/how-anthropic-is-using-clickhouse-to-scale-observability-for-ai-era), [Tesla](https://clickhouse.com/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse), and [Deutsche Bank](https://clickhouse.com/videos/big-sensitive-data-warehouse-deutsche-bank-clickhouse) already run for real\-time analytics at scale, alongside managed Postgres for transactional data. Managed ingestion brings data in from open table formats, data lakes, and other sources, and a context management layer (aka. skills) grounds agents in your own definitions.
- **The connectivity layer**: the managed ClickHouse MCP server, plus clients, CLIs, and plugins. Our customers keep the flexibility and full control over any MCP\-compatible app or agent they want to connect. We are seeing customers already plugging in Claude Code, Cursor, Amazon Bedrock agents, and their own custom agents.
- **The agentic layer**: the ClickHouse Assistant for quick questions in the SQL Console, and ClickHouse Agents for full agentic workflows with a sandboxed code interpreter.
- **Observability and evals, end to end**: ClickHouse also includes ClickStack for observability and Langfuse for LLM observability and evaluations, so you can see what your agents are doing and keep them reliable in production.


![](/uploads/clickhouse_agents_jun2026_image3_8315470075.png)
The goal is to allow our customers to benefit from the power of AI with the best real\-time analytics platform that is portable, extensible, and free of lock\-in. Customers have the flexibility to use our managed agents out of the box, build your own with the no\-code builder, or bring your own framework and let ClickHouse be the open data layer underneath.


What's different with this approach is that ClickHouse does not force customers to choose between first\-party or third\-party AI as an either\-or scenario. Bring your own agents, models, and tools to ClickHouse and run them over our connectivity layer, or reach for our first\-party capabilities like ClickHouse Agents. Both paths sit on the same open data foundation, and meet our customers where you are instead of making you pick a side.


![](/uploads/clickhouse_agents_jun2026_image4_33e7a643e2.png)
*MCP Adoption in ClickHouse Cloud (The graph above shows the number of unique services using our remote MCP feature over time)*


To illustrate this, we worked closely with Amazon Web Services to ship a native integration with the AgentCore Registry in ClickHouse Agents. This allows users to use MCP in order to bring their agents, tools and skills managed in AgentCore, and use them in ClickHouse agents.


![](/uploads/clickhouse_agents_jun2026_image5_9d4230b8e1.png)
We build ClickHouse as an open data platform for AI. ClickHouse Agents, LibreChat, MCP, and our work with systems like AWS Agent Registry all reflect the same belief: openness, composability, and interoperability are what enable enterprises move at the speed AI demands. No single vendor is going to integrate a complete AI stack fast enough and complete enough, and the ones that try will lock users into a walled garden. ClickHouse's open and community driven DNA is what makes it the substrate of the agentic era for all our customers.


## How we got here: Productizing our own experience [\#](/blog/clickhouse-agents-beta#how-we-got-here)


In March 2025 we made our own data warehouse AI\-first and built our internal analytics agent, on top of it. We documented the whole thing in [how we made our internal data warehouse AI\-first](https://clickhouse.com/blog/ai-first-data-warehouse), and the short version is that it took off fast. Today around 80% of ClickHouse employees use LibreChat daily, and our platform alone handles roughly 70% of our internal data warehouse queries, processing more than 45 million tokens a day. By some distance, it is the most\-used internal tool we run.


Picking the chat layer was a real build\-versus\-buy decision, and our requirements were non\-negotiable: work with any LLM provider, solid MCP support, ship enterprise features like SSO and audit logging, render artifacts, and never lock us into a single vendor. [LibreChat](https://github.com/danny-avila/LibreChat) checked every box. For anyone who has not met it, LibreChat is a leading open\-source AI chat platform: one self\-hostable UI in front of virtually every LLM provider, with enterprise SSO, RBAC, MCP support, agents, artifacts, and a sandboxed code interpreter built in.


What convinced us LibreChat was the right platform was also the list of companies already running it in production. Shopify CEO Tobi Lütke [put it plainly](https://x.com/tobi/status/1932846291794510241):


"Shopify runs an internal fork of librechat, and we merge most everything back. I highly recommend other companies give this project a look for their internal LLM system. It works very well for us."


[Daimler Truck](https://www.daimlertruck.com/en/newsroom/stories/daimler-truck-makes-artificial-intelligence-accessible-to-all-employees-worldwide-with-librechat) runs a company\-wide AI platform on LibreChat with thousands of employees and over 3,000 agents in production. In healthcare, cBioPortal shipped [cBioAgent](https://chat.cbioportal.org/) on the ClickHouse, MCP, and LibreChat stack, letting cancer researchers query genomics datasets in plain language. As Ino de Bruijn, who manages bioinformatics software engineering there, put it, it "puts discovery at cancer researchers' fingertips." In November 2025 [we acquired LibreChat](https://clickhouse.com/blog/clickhouse-acquires-librechat) and welcomed Danny Avila and the team into ClickHouse. ClickHouse Agents inherits LibreChat's production readiness.


Running our internal use\-case also produced a large body of real agentic\-analytics workloads, actual questions against actual schemas, with the SQL and tool\-use traces to match. That lets us evaluate virtually every available model on the task itself rather than on generic benchmarks. The Claude family came out on top consistently, across SQL generation, schema reasoning, and tool use. It is the leading model for code, and SQL and schema work are a natural extension of that strength, which is why Claude is wired in as the default in ClickHouse Agents.


![](/uploads/clickhouse_agents_jun2026_image6_0be9866d16.png)
## Real\-time OLAP for agents [\#](/blog/clickhouse-agents-beta#real-time-olap-for-agents)


Over a year ago, we wrote about [agent\-facing analytics](https://clickhouse.com/blog/agent-facing-analytics): the idea that AI agents are a new user persona for real\-time databases. The ones that never sleep, never take breaks, and generate SQL like there is no tomorrow. The argument was that a real\-time analytics database is the natural context provider for these agents, because it can serve fast, concurrent, exploratory queries over fresh data, exactly the access pattern agents lean on. A year of running them in production and working closely with early adopters confirmed our hypothesis.


![](/uploads/clickhouse_agents_jun2026_image7_e65251f928.png)
Agents fire 10 to 100x the volume of queries a human analyst would, in bursts, and every retry and timeout burns tokens and adds load. Sub\-second latency on billions of rows, petabyte\-scale storage, thousands of concurrent queries, and the cost efficiency to keep agent traffic affordable as it grows as key characteristics of a platform like ClickHouse. Recent engine work makes this even better, including [joins up to 6x faster](https://clickhouse.com/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance) over the past year, [multi\-stage distributed query execution](https://clickhouse.com/blog/multi-stage-distributed-query-execution-clickhouse-cloud), and [full\-text search GA](https://clickhouse.com/blog/full-text-search-ga-release).


It unlocks time to insight. The traditional path runs through handoffs: data engineers write queries, analysts build dashboards, business users interpret the results, each step measured in hours or days. With ClickHouse Agents, a PM can ask "what's driving the churn spike last week?" and get the answer, the query behind it, a chart, and the next questions to explore, in seconds.


## What's next [\#](/blog/clickhouse-agents-beta#whats-next)


Besides all the exciting new announcements, we are working with our customers for


- Deeper Cloud integration, with richer in\-chat visualizations and tighter coupling to the SQL Console.
- An Agent API for programmatic access to the agents built in ClickHouse Agents
- Trust feedback loop: allowing users to run evals and influence context by leveraging our native integration with Langfuse, which [joined ClickHouse in January 2026](https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability)


## Get started today [\#](/blog/clickhouse-agents-beta#get-started-today)


ClickHouse Agents is available to all ClickHouse Cloud customers in public beta. If you have a ClickHouse account, you can now access ClickHouse Agents through the SQL console, or simply start using <https://ai.clickhouse.cloud/>. As with any beta, your feedback is the only way this gets better. Find us via the form, our [community Slack](https://clickhouse.com/slack).


If you are building agentic analytics on ClickHouse and want to be a design partner, [reach out](https://clickhouse.com/company/contact).


*Huge thanks to the AI/ML team, to Danny Avila and the LibreChat community, to our friends at Anthropic and AWS who joined us on the keynote stage, and to every customer working with us on agentic analytics. We are just getting started.*

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_appoints_apac_leader_f2c3722e9c.jpg&w=828&q=75)Company and culture### [ClickHouse appoints new leader for Asia Pacific and expands global go\-to\-market leadership team](/blog/clickhouse-appoints-apac-leader-and-expands-global-gtm-leadership)

ClickHouse · Jun 8, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
