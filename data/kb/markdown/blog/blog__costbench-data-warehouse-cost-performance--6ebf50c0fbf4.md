# Introducing CostBench: an open benchmark for data warehouse cost\-performance


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Introducing CostBench: an open benchmark for data warehouse cost\-performance

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)![](/_next/image?url=%2Fuploads%2Flio_headshot_singapore_7cc9852011.jpg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber) and [Lionel Palacin](/authors/lionel-palacin)May 27, 2026 · 5 minutes read
> **TL;DR**  
> 
> CostBench is an open benchmark for cloud data warehouse cost\-performance: performance\-per\-dollar, not just speed.  
>   
> It helps teams choose the system that delivers the most performance per dollar for real\-time analytical workloads.


  

## Performance alone is only half the story [\#](/blog/costbench-data-warehouse-cost-performance#performance-alone-is-only-half-the-story)


Most benchmarks tell you how fast a query runs. That is useful, but incomplete.



> In cloud data platforms, speed and cost are inseparable.


If warehouse A is faster than warehouse B, A looks better on a performance chart. But if A costs three times more to run, the comparison changes. You might spend the same budget on a larger configuration of B, get more compute, and make B faster than A for less money overall.


That comparison is hard because every platform exposes cost differently: credits, DBUs, slot\-seconds, compute units, RPUs.


![Blog-Bench2Cost.001.png](/uploads/Blog_Bench2_Cost_001_341b09cafb.png)
The unit names differ, but the underlying question is the same:



> How much compute did the system need to finish the workload, and what did that compute cost?


CostBench answers that question directly. It also exposes where cost\-performance breaks: during ingest, while making data query\-ready, or when serving reads.


## Why this matters in the AI era [\#](/blog/costbench-data-warehouse-cost-performance#why-this-matters-in-the-ai-era)


Agentic analytics raises the pressure on every layer of the database.


New data never stops: events, transactions, logs, traces, user activity, fraud signals, operational state. At the same time, users and agents expect fast answers over fresh data.



> If the database is slow, the agent is slow. If the database is expensive, teams start rationing what agents can do: fewer retries, smaller datasets, less context, stale data.


In the AI era, fast and low\-cost has to hold across the full analytics path: continuous ingest, query\-ready preparation, and reads.


![Blog-Bench2Cost.002.png](/uploads/Blog_Bench2_Cost_002_7f4af0a308.png)
**Read\-side pressure** comes from query volume. A single user question can trigger many SQL queries: schema exploration, validation, retries, refinements, drilldowns, and follow\-ups. Each extra query burns compute. At agentic scale, query volume turns directly into cost pressure.


**Write\-side pressure** comes from real\-time freshness: fresh data has to be continuously ingested, compressed, and organized so queries can skip more data. That work burns compute before the first query even runs, and determines how much compute those queries burn later.


## What CostBench measures [\#](/blog/costbench-data-warehouse-cost-performance#what-costbench-measures)


CostBench turns that pressure into a full\-path cost\-performance lens with two measurable dimensions:


- **Read\-side cost\-performance**: how much query performance you get per dollar.
- **Write\-side cost\-performance**: how efficiently each dollar turns fresh ingest into query\-ready data.


Together, they help answer the question that matters when choosing a platform:



> Which system gives you the most performance per dollar for real\-time analytical workloads?


![Blog-Bench2Cost.003.png](/uploads/Blog_Bench2_Cost_003_c9407dbe1a.png)
The first release focuses on the read side: analytical queries over data that has already been loaded. We have also started measuring the write side, beginning with [Snowflake as a contrast point for ClickHouse](https://clickhouse.com/blog/write-side-cost-performance-snowflake-clickhouse). Broader write\-side coverage will follow.


This gives CostBench a simple roadmap: expose whether real\-time cost\-performance holds across the full analytics pipeline, from making fresh data query\-ready to querying it efficiently.


## The first results: read\-side cost\-performance [\#](/blog/costbench-data-warehouse-cost-performance#the-first-results-read-side-cost-performance)


The first CostBench release turns read\-side performance into a comparable performance\-per\-dollar result across major cloud data warehouses.


We compare ClickHouse Cloud, Snowflake, Databricks, BigQuery, and Redshift using 43 production\-derived analytical queries on a real anonymized dataset, then apply [each vendor’s actual compute billing model](https://clickhouse.com/blog/how-cloud-data-warehouses-bill-you) to place every system on the same cost\-performance plane: faster or slower, lower\-cost or higher\-cost.


![Blog-Bench2Cost.004.png](/uploads/Blog_Bench2_Cost_004_66900fe22f.png)
ClickHouse Cloud is the only system that stays in the fast and low\-cost zone as data scales. The nearest competitor is 23× worse in cost\-performance.


That is the value of CostBench: it turns vendor\-specific runtimes and billing models into a result teams can use when choosing a platform.


## Open and reproducible by design [\#](/blog/costbench-data-warehouse-cost-performance#open-and-reproducible-by-design)


CostBench is open because cost\-performance claims should be inspectable.


The benchmark publishes the workload, scripts, configurations, pricing assumptions, raw JSON results, and methodology. If a result looks surprising, you can inspect the setup that produced it.


## Try it yourself [\#](/blog/costbench-data-warehouse-cost-performance#try-it-yourself)


Explore the results on the [ClickHouse benchmark hub](https://clickhouse.com/benchmarks), inspect the raw data, or clone the [CostBench repository](https://github.com/ClickHouse/CostBench) and run the benchmark yourself.


Cost\-performance should not be a black box. CostBench makes it inspectable.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
