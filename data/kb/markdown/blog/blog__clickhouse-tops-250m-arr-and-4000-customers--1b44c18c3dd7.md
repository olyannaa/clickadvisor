# ClickHouse tops $250M ARR and 4,000 customers, launches Claude\-powered agents at Open House 2026


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Company and culture](/blog?category=company-and-culture)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse tops $250M ARR and 4,000 customers, launches Claude\-powered agents at Open House 2026

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 27, 2026 · 7 minutes read*Annual run\-rate revenue more than tripled year\-over\-year; new CostBench benchmark shows ClickHouse Cloud at 23x better cost\-performance than the nearest cloud data warehouse*


**SAN FRANCISCO — May 27, 2026 —** ClickHouse today opened Open House 2026, its second annual user conference, with a set of announcements that mark one of the company's most active quarters since founding. ClickHouse’s serverless cloud offering has crossed over $250 million in annual run\-rate revenue — more than triple a year ago — and added more than 1,000 net new customers since January, bringing its total to 4,000\. To meet the demands of AI\-era workloads, the company also launched ClickHouse Agents, a fully managed agentic analytics service powered by Anthropic's Claude; published CostBench, an open benchmark comparing the major cloud data warehouses on cost\-performance; and introduced House Mates, its first formal partner program.


## Growth [\#](/blog/clickhouse-tops-250m-arr-and-4000-customers#growth)


When ClickHouse closed its $400 million Series D in January 2026, it had just crossed 3,000 customers. One quarter later, it has surpassed 4,000 and ARR has crossed over $250 million, more than tripling year\-over\-year. Recent additions and expansions include Capital One, Lovable, Decagon, Polymarket, and Airwallex, joining a base that includes Anthropic, Meta, Cursor, Sony, Tesla, Memorial Sloan Kettering, Lyft, and Instacart.


The customer speakers at Open House 2026 reflect how broadly ClickHouse now sits in the enterprise stack: Visa, Cisco, Intuit, Shopify, DoorDash, Mercado Libre, Vercel, Weights \& Biases, Zoox, and Jump Trading. Partner speakers and sponsors include Anthropic, AWS, Google, Microsoft, dbt Labs, Fivetran, Temporal, Hex, and Sigma.


"AI workloads demand the performance and cost efficiency ClickHouse was built for, and the last quarter has made that clearer than ever," said Aaron Katz, CEO of ClickHouse. "More than 1,000 new customers and a tripling of ARR within months of our Series D tell us this isn't a cycle, it's a structural shift in what data infrastructure has to do. What we're announcing this week is built to extend that lead as AI moves from experiment to production."


## ClickHouse Agents, powered by Claude [\#](/blog/clickhouse-tops-250m-arr-and-4000-customers#clickhouse-agents-powered-by-claude)


ClickHouse Agents is a fully managed agentic analytics service in ClickHouse Cloud, powered by Claude. It is a no\-code agent builder that lets anyone define, configure, and ship agents grounded in ClickHouse data. Out of the box, it includes a chat interface, a sandboxed code interpreter, shareable artifacts, skills management, memory, and multi\-agent workflows. Agents connect natively to ClickHouse and to any MCP\-compatible third\-party system, drawing context from across an organization's stack, including a native integration with the AWS Agent Registry.


ClickHouse Agents is part of a broader set of product investments aimed at the workloads AI applications generate: high\-concurrency queries, agent\-driven analytics, model\-training telemetry, and end\-to\-end observability of AI systems in production:


- **Managed Postgres** is in public beta, with native integration to ClickHouse analytics, giving AI applications a single platform for transactional state and high\-throughput analytics on the same data.
- **AI observability.** Managed ClickStack is now available as a fully managed service for infrastructure and model\-training observability. Langfuse, acquired in January, provides agent observability — correctness, evaluation, and model\-cost tracking for production AI.
- **Expanded analytics.** Full\-text search is generally available, addressing one of the most common observability and AI\-grounding workloads. Automatic query optimization now puts ClickHouse on par with established warehouses on TPC\-H and other standard JOIN benchmarks.
- **ClickHouse Cloud.** Agentic onboarding takes new users from sign\-up to first production query with no manual schema work. Cross\-region replication is now available for enterprise resiliency.


## CostBench: the AI era runs on cost\-performance [\#](/blog/clickhouse-tops-250m-arr-and-4000-customers#costbench-the-ai-era-runs-on-cost-performance)


AI workloads run at high concurrency and low latency, which makes cost\-performance, not raw speed, the relevant measure for the platforms underneath them. CostBench, launched today, is an open and reproducible benchmark that applies each vendor's real compute billing model to the same analytical workload, producing directly comparable cost\-per\-query results across ClickHouse Cloud, Snowflake, Databricks, BigQuery, and Redshift.


ClickHouse Cloud is the only system that stays in the "Fast \& Low\-Cost" zone across datasets of varying scale. The nearest competitor lands at 23x worse on cost\-performance. The full benchmark, interactive explorer, and methodology are at [clickhouse.com/benchmarks](https://clickhouse.com/benchmarks/?utm_medium=referral&utm_source=press&utm_campaign=clickhouse-tops-250m-arr).


## House Mates: a partner community for the next stage [\#](/blog/clickhouse-tops-250m-arr-and-4000-customers#house-mates-a-partner-community-for-the-next-stage)


ClickHouse also introduced House Mates, its first formal partner community and program. It launches with a founding cohort of more than 25 technology partners and over 35 services, consulting, and channel partners across six continents, including dbt Labs, Fivetran, Sigma, Notion, Temporal, Tiger Analytics, DoIT, Ciklum, and MegazoneCloud. The program is organized across three tracks: Technology, Services, and Reseller, each with three tiers: Ignite, Accelerate, and Prime. Benefits scale with tier and include joint go\-to\-market motions, co\-innovation and integration support, enablement and certifications, incentives, and a dedicated partner portal. More on the House Mates program at [clickhouse.com/partners](https://clickhouse.com/partners?utm_medium=referral&utm_source=press&utm_campaign=clickhouse-tops-250m-arr).


ClickHouse maintains deep partnerships with AWS, Microsoft, and Google Cloud. House Mates extends that foundation across the broader ecosystem, giving customers pre\-built integrations, proven implementation expertise, and clear routes to market for the full ClickHouse Cloud platform, including Langfuse.


"ClickHouse powers some of our most demanding workloads, ingesting over a million events per minute across hundreds of billions of logs to fuel the real time dashboards our customers depend on. Hex's native ClickHouse connector gives us a seamless analytics layer on top of that data, enabling every team at Modal to explore and act on insights without having to ETL a large amount of data into a separate warehouse." said Kenny Ning, Head of Data at Modal. "It is exciting to see the ClickHouse and Hex partnership getting deeper because, for teams like ours that run on both real time and analytical data, a tighter integration between the two means fewer tradeoffs and faster answers for everyone in the organization."


"ClickHouse is one of the fastest\-growing databases in the market, and our customers are building on it because it delivers disruptive cost\-performance," said Mike Palmer, CEO, Sigma. "Entering the House Mates partner program is our commitment to delivering the best runtime layer on top of ClickHouse."


"ClickHouse's real\-time analytics combined with Tiger Analytics' expertise in data science, AI engineering, and data engineering gives customers a strong foundation to modernize their data platforms." said Rajeev Nayar, VP of Data Engineering, Tiger Analytics. "Together, we aim to help organizations accelerate innovation and derive greater value from their data investments."


![Founders_AMS_2025.jpeg](/uploads/Founders_AMS_2025_df2919ac2a.jpeg)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
