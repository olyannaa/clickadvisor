# Open House 2026 Day 2: 10 years of open source and what the ecosystem is building next


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Open House 2026 Day 2: 10 years of open source and what the ecosystem is building next

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 28, 2026 · 15 minutes readIf you missed Day 1, catch up on all the ClickHouse Cloud and ClickStack announcements [in our Day 1 roundup blog post](https://clickhouse.com/blog/open-house-2026-day-1).


Last year was our first annual Open House conference, and we covered a lot in a single day. This year, we had so much content and announcements to make that we decided to extend by another day. Day 2 delved deeper into what the open\-source community, our partners, and our customers are building on top of ClickHouse. We focused not just on the features being built, but also on why the world is betting on this data platform.


This year, ClickHouse turns 10 as an open source project. Over that decade, the ecosystem has grown to 200\+ integrations built by us, by partners, and by a community that just keeps shipping. The pace has accelerated recently. MCP support and our skills framework are seeing explosive adoption, and we are watching entirely new categories of embedded and bespoke integrations emerge organically. People and agents alike are finding ways to wire ClickHouse into their stacks that we would not have thought to build ourselves.


## 10 years of Open Source [\#](/blog/open-house-2026-day-2#10-years-of-open-source)


The opening keynote looked back at 10 years of ClickHouse as an open\-source project, including contributor growth, community milestones, and the launch of the [Community Champions Program](https://clickhouse.com/community). Alexey Milovidov took the stage and walked us through his thought process in building and designing ClickHouse and what he has learned over the years in a session entitled 'How to build a great database.' It hasn't just been Alexey working on ClickHouse all this time. With over 2\.6k contributors to ClickHouse and nearly 48k stars in GitHub, the support we've seen from our community over the last decade has been amazing, and we can't thank you enough for all of your contributions.


![open_house_day2_may2026_image5.png](/uploads/open_house_day2_may2026_image5_54d9436e8d.png)
## House Mates: the inaugural cohort [\#](/blog/open-house-2026-day-2#house-mates-the-inaugural-cohort)


To support the momentum behind the ClickHouse ecosystem, we announced [House Mates](https://clickhouse.com/blog/introducing-house-mates), ClickHouse's official partner program. House Mates was officially launched with 25\+ ISV \& technology partners and 35\+ services \& channel partners. You can't ask for more out of our first cohort; they shipped.


The first wave of House Mates covers the integrations our customers have asked about most. On the data and transformation side, Fivetran is now generally available as a ClickHouse Cloud destination, bringing 500\+ sources with schema migration support and an enterprise SLA. Sigma Computing is moving its official connector to public beta. Notion is adding first\-party support for the ClickHouse MCP server for custom agents. And ClickHouse is now the first partner to build a community dbt Fusion adapter, taking our first step towards natively running on the dbt platform. More on each of these below.


Beyond those announcements, the cohort spans: Artie for sub\-minute CDC replication from Postgres, MySQL, SQL Server, Oracle, and MongoDB; Dreambase as an AI\-native analytics platform connecting ClickHouse and Supabase; Laravel for a full\-featured ClickHouse driver with Eloquent models, Query Builder, Schema Builder, and native migration support via artisan; Odigos for zero\-code OpenTelemetry tracing with ClickHouse as the analytics backend; Tavily for AI search with ClickHouse Agents as a fast retrieval backend; Hightouch for reverse ETL from ClickHouse to CRMs, ad platforms, and SaaS destinations; and DataHub as an open source data catalog with lineage and discovery for ClickHouse tables and pipelines. The list goes on.


We're humbled to have such an amazing group of partners building for tomorrow with us. During our conference, we had some exciting announcements across the ClickHouse ecosystem.


## Fivetran: generally available [\#](/blog/open-house-2026-day-2#fivetran-generally-available)


The Fivetran destination connector for ClickHouse Cloud is now generally available. This is one of the most\-requested integrations we have heard from customers over the past two years.


Teams can now replicate data from 500\+ sources into ClickHouse without writing or maintaining pipeline code. Fivetran handles schema migrations, column additions, and retries automatically. The GA release includes schema migration support and an enterprise SLA, making this a production\-ready path for teams running enterprise SaaS data into ClickHouse from Salesforce, HubSpot, Google Ads, Stripe, SAP, NetSuite, Snowflake, Databricks, and hundreds more.



> "ClickHouse has been a fast\-growing data destination on Fivetran, and going GA reflects how seriously both teams have invested in this partnership. Enterprise data teams run their businesses on sources such as Salesforce, Google Analytics, SAP, Databricks, Snowflake, Workday, and NetSuite. Getting that data into ClickHouse reliably, with automated schema management and an enterprise SLA, is what Fivetran was built for. We are proud to give customers a production\-grade path from every major enterprise source into ClickHouse Cloud."
> 
> 
> \-\- Shiva Mogili, Director of Product Management, Connectors \& Extensibility


**Google Cloud Dataflow: Pub/Sub template generally available**


Adding to our BigQuery template, the ClickHouse template for Pub/Sub support is now in the Google Cloud Dataflow gallery.


Previously, moving Pub/Sub data into ClickHouse required custom Beam pipelines with no official support. Now teams can configure a managed pipeline to ClickHouse directly from the Dataflow console. For teams on ClickHouse Cloud, [the same integration is also available as a native ClickPipes connector](https://clickhouse.com/blog/open-house-2026-day-1#clickpipes), so you can set it up from whichever side makes more sense for your workflow.


Learn more about how to get started using Pub/Sub on Dataflow [here](https://clickhouse.com/docs/integrations/google-dataflow/templates/pubsub-to-clickhouse).


## Sigma Computing: connector in public beta [\#](/blog/open-house-2026-day-2#sigma-computing-connector-in-public-beta)


The Sigma Computing connector for ClickHouse is moving from private beta to public beta after successfully being used in production across a variety of customers. The connector is now available to any Sigma customer who wants to connect to ClickHouse.


In addition to the connector going to public beta, Sigma also selected ClickHouse as the first database target for its new ETL Cache Layer, now in private preview. When Sigma queries hit the primary warehouse at every dashboard load, teams pay full compute cost regardless of how often the data underneath is actually changing. The ETL Cache Layer pre\-materializes hot datasets and serves them sub\-second at any concurrency level, with intelligent routing that falls back to the source warehouse on a cache miss. This has not only major performance benefits, but cost benefits as well.


*"ClickHouse is one of the fastest\-growing databases in the market, and our customers are building on it because it delivers disruptive cost\-performance," said Mike Palmer, CEO, Sigma. "Entering the House Mates partner program is our commitment to making Sigma the best AI runtime experience on top of ClickHouse."*


## dbt: ClickHouse Fusion adapter [\#](/blog/open-house-2026-day-2#dbt-clickhouse-fusion-adapter)


ClickHouse is the first partner to co\-develop a dbt Fusion engine adapter with dbt Labs. Fusion is a true SQL compiler built in Rust: the engine underneath dbt that makes it faster at any project scale, gives developers real feedback before anything hits the warehouse, and generates the structured metadata that makes AI\-assisted data work reliably. It's the future of dbt, and we are excited to partner with dbt Labs to bring the adapter to our joint community.


Our growing community of dbt users, combined with the dbt vision, was the catalyst for this work. As a result, the adapter is now available in alpha via the CLI. Analytics engineers can run dbt models against ClickHouse using Fusion today. This is the first milestone toward a full dbt platform (fka Cloud) integration. We're excited not only to address one of our most common integration requests but also to help shape the new adapter program at dbt Labs. As Fusion becomes the default, we're committed to delivering a first\-class experience for our shared customers.



> "ClickHouse has become one of the fastest\-growing databases in the dbt community, and it is easy to see why. The combination of speed at scale and a genuine commitment to the open ecosystem makes it a natural fit for the composable data infrastructure the market is moving toward. Fusion is how dbt will power the platform going forward, and getting ClickHouse there early means our shared customers can build a fully open stack today. We are excited about what we are building together, and there is a lot more to come."
> 
> 
> \-\- Hope Watson, Product Manager, dbt Labs


## Apache Airflow: native provider [\#](/blog/open-house-2026-day-2#apache-airflow-native-provider)


A native Apache Airflow provider for ClickHouse will be available from the Airflow registry [soon](https://github.com/apache/airflow/pull/67080). We've seen a lot of interest in native orchestration connectors and want to thank Ivan Klimenko ([klimenkoIv](https://github.com/klimenkoIv)), Anton Bryzgalov ([bryzgaloff](https://github.com/bryzgaloff)), and the Airflow community for [supporting this effort](https://github.com/bryzgaloff/airflow-clickhouse-plugin) to date. Our native provider adds a ClickHouse hook and operator to the Airflow ecosystem, so teams can schedule queries, table refreshes, and data loads directly from DAGs without writing custom operator wrappers. The new provider is built on the new Apache Airflow standards, will be maintained by ClickHouse, and will work out of the box with Astronomer Astro connections once it clears the registry. We're excited to see how this project evolves and can't wait to get this out to our community.


## Vercel AI SDK v7 \+ Langfuse [\#](/blog/open-house-2026-day-2#vercel-ai-sdk-v7-langfuse)


Vercel AI SDK v7 ships with a new Telemetry system for more granular agent observability. Langfuse offers a native integration with this new telemetry system via OpenTelemetry.


AI SDK v7 is available as a canary build today and will be generally available in June.


Langfuse integrates with the AI SDK v7 with a single `registerTelemetry()` call, giving full hierarchical trace visibility across every tool call, sub\-agent span, and LLM invocation in a production AI agent. No extra boilerplate, no custom instrumentation wiring.


![open_house_day2_may2026_image4.png](/uploads/open_house_day2_may2026_image4_7d04c525ed.png)
## Notion: Native ClickHouse connector for custom agents [\#](/blog/open-house-2026-day-2#notion-native-clickhouse-connector-for-custom-agents)


Notion is adding ClickHouse as a native connector for custom agents, so teams can query their ClickHouse data directly from inside Notion without any external tooling.


What makes this integration interesting is the architecture. There's no separate semantic layer sitting between your data and your questions. Instead, Notion pages written in plain English describe your table structures, how data is tagged, and what different fields mean. The agent reads those docs, connects to ClickHouse via MCP, and returns answers in natural language. Your existing Notion workspace becomes the context layer. ClickHouse does the querying. This will be rolling out to Notion custom agents soon.



> "Every day, ClickHouse users rely on a service that handles some of the most demanding data workloads out there. But getting those insights into the tools where teams actually make decisions has historically required a lot of glue. We're thrilled that Notion custom agents can now query ClickHouse directly: our shared customers can ask questions in plain language and get real, data\-rich answers back, no SQL required. That means scheduled reports, automated workflows, and live data pulled straight into docs and dashboards. ClickHouse crunches the numbers, Notion makes them actionable."
> 
> 
> \-\- David Rosenberg, Ecosystem Lead, Notion


## Python Client is now v1! [\#](/blog/open-house-2026-day-2#python-client-is-now-v1)


[clickhouse\-connect v1](https://github.com/ClickHouse/clickhouse-connect) is now generally available on PyPI. This is a huge milestone and the first major release of the client. The headline for the initial 1\.0 release is a native async client built from the ground up on top of aiohttp. This replaces the old executor\-based wrapper and has full feature parity with the sync client, including streaming.


You'll also find massive speedups around performance for DateTime types, fixed\-width numerics, Maps, Decimals, and BigDecimals. Along with support for Variant columns that can now be serialized client\-side using their native ClickHouse types.


For projects that have numpy, pandas, pyarrow, or polars installed, cold\-start time improves by 4x. That improvement comes from lazy\-loading optional dependencies rather than importing everything up front.


We have introduced first\-class support for the SQLAlchemy dialect, deepened support for ClickHouse\-specific SQL, and paved the way for Alembic schema migrations, which ship in v1\.1\.0\.


On the compatibility front, this release also adds compatibility for Pandas 3\.x in addition to experimental support for Python 3\.14free\-threading, giving existing clickhouse\-connect users compelling reasons to upgrade


## .NET Stack: generally available on NuGet [\#](/blog/open-house-2026-day-2#net-stack-generally-available-on-nuget)


With the recent stable release 1\.2\.0, [clickhouse\-cs](https://github.com/ClickHouse/clickhouse-cs) now ships a full .NET development stack with four packages on NuGet.


[ClickHouse.EntityFrameworkCore](https://github.com/ClickHouse/ClickHouse.EntityFrameworkCore) adds ORM support, including JOINs, UNIONs, subqueries, DDL generation, and schema migrations. [Serilog.Sinks.ClickHouse](https://github.com/ClickHouse/Serilog.Sinks.ClickHouse) ships with column and cluster fluent configuration for structured logging into ClickHouse. [ClickHouse.Aspire](https://github.com/ClickHouse/ClickHouse.Aspire/) rounds out the stack for teams building cloud\-native .NET applications.[ClickHouse.SemanticKernel](https://github.com/ClickHouse/ClickHouse.SemanticKernel/) connects ClickHouse to the Microsoft AI orchestration ecosystem. Each package is available today for users building in the .NET ecosystem.


## ClickStack announcements [\#](/blog/open-house-2026-day-2#clickstack-announcements)


Following up on yesterday's ClickStack Cloud announcement, we also launched two major additions to ClickStack: **AI Notebooks** and the **ClickStack MCP server**. Both are built around a pretty simple idea: observability workflows shouldn't feel isolated from the way engineers actually debug systems today.


**AI Notebooks**, now public beta in Managed ClickStack, give teams a persistent workspace for investigations. Instead of losing context across dashboards, chats, terminals, and ad hoc queries, engineers can keep queries, charts, notes, and findings together in one place while an investigation evolves.


Most production incidents aren't linear. You follow one lead, hit a dead end, revisit an earlier assumption, compare traces against logs, then try something else. Notebooks are designed to support that kind of workflow without forcing everything into a single chat session or rigid sequence of steps.


![open_house_day2_may2026_image1.png](/uploads/open_house_day2_may2026_image1_a745b3bbd1.png)
At the same time, we're seeing more teams build their own internal agents and automation around observability data using tools like Claude Code, Cursor, and custom SDK\-based systems. The **ClickStack MCP** server is designed for that world and built around the philosophy of "bring your own agents".


Rather than introducing yet another standalone AI interface, the MCP server exposes the same observability tools used internally by Notebooks, but makes them available to external agents. Under the hood, the MCP translates those operations into optimized ClickHouse queries, allowing agents to work with higher\-level semantic endpoints instead of repeatedly rebuilding investigation logic and generating complex SQL from scratch.


![open_house_day2_may2026_image3.png](/uploads/open_house_day2_may2026_image3_d527806633.png)
Compared to the more generic ClickHouse MCP implementation, our internal testing shows the ClickStack MCP server improves efficiency, performance, and investigation accuracy. In our internal testing, investigations were completed up to 25% fewer tool calls, a 2\.5x increase in consistency, and an improvement in evaluation of almost 20%.


For more details, including where we're heading with tighter integration between Notebooks and MCP\-driven workflows over time, check out the [main announcement post](https://clickhouse.com/blog/observability-mcp-server-ai-notebooks).


## What this adds up to [\#](/blog/open-house-2026-day-2#what-this-adds-up-to)


Ten years in, the ecosystem around ClickHouse is healthier than it has ever been and expanding rapidly. The integrations we announced today span ELT, BI, orchestration, language clients, MCP, and AI observability. They close gaps that have been on our list for a long time and open up entirely new categories of things people (and their agents) can build.


The community, our partners, and our customers are all pulling in the same direction. That is what Day 2 was about, and we can't wait to see what you build.


Session recordings will be available shortly. For everything announced on Day 1, start here: [Day 1 ClickHouse Cloud recap](https://clickhouse.com/blog/open-house-2026-day-1).

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-751-get-started-today-sign-up&utm_blogctaid=751)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
