# What really matters for performance: lessons from a year of benchmarks


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# What really matters for performance: lessons from a year of benchmarks

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber)Dec 22, 2025 · 11 minutes read## Why benchmarks keep showing up in my work [\#](/blog/what-really-matters-for-performance-lessons-from-a-year-of-benchmarks#why-benchmarks-keep-showing-up-in-my-work)


As the year winds down, I like to zoom out and look at the work I’m proudest of.


I wrote (and helped ship) a lot of ClickHouse content this year, but a bunch of the posts I care about most share the same backbone: **each one has a benchmark behind it**.


![Blog-benchmarks-of-2025.gif](/uploads/Blog_benchmarks_of_2025_a8bcb6547e.gif)
Benchmarks show up again and again in my work because they force clarity. They correct intuition, surface trade\-offs, and sometimes overturn narratives that have stuck around for too long.


Here are a few of my favorites from this year, the ones that surprised me, changed how people think about ClickHouse, or directly impacted how real systems were built. Taken together, they form a loose narrative, from data layout and ingestion, through storage and execution, and finally to cost.


And reading back through them, I kept noticing the same thing: performance comes down to how efficiently an engine moves data end\-to\-end.


## The billion\-docs JSON benchmark [\#](/blog/what-really-matters-for-performance-lessons-from-a-year-of-benchmarks#the-billion-docs-json-benchmark)


This benchmark started with a foundational question: *what does JSON look like when you treat it as columnar data instead of a document blob?*


ClickHouse completely reimagined JSON storage on top of column\-oriented storage, resulting in unmatched speed, compression, and user experience, [far beyond any existing JSON data store](https://clickhouse.com/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql).


To prove the speed, we created [JSONBench](https://jsonbench.com/): a reproducible benchmark that loads the same real\-world dataset (up to 1B Bluesky events) into multiple systems, then measures storage size, cold/hot query runtimes, and data quality (how many documents were successfully ingested).


In the original billion\-docs run, ClickHouse was orders of magnitude faster while also being smaller on disk (including 20% more compact than storing the same JSON as compressed files on disk).


![JSON_Benchmarks_018_4572dccd94.png](/uploads/JSON_Benchmarks_018_4572dccd94_723f9e64db.png)
![JSON_Benchmarks_017_1e36137288.png](/uploads/JSON_Benchmarks_017_1e36137288_d973fb27eb.png)
We also built a [live online dashboard](https://jsonbench.com/) where you can slice results by dataset size, cold vs. hot, storage, and data quality, plus a toggle for systems that flatten JSON.


![Blog-benchmarks-of-2025.002.png](/uploads/Blog_benchmarks_of_2025_002_b6a31eb399.png)
JSONBench didn’t stop at a blog post. It’s now actively used in the community and regularly receives external pull requests, adding new or updating results for exiting systems.



> **This is one of my favorite benchmarks this year because the results genuinely surprised me.**


ClickHouse was thousands of times faster than traditional JSON data stores like MongoDB, while also using significantly less storage. It completely changed my intuition for what’s possible with analytical queries on JSON.


![JSON.gif](/uploads/JSON_af5ee459cb.gif)
**Side story**: ClickHouse already started from a strong lead in the original JSONBench results. We continued improving the JSON implementation independently, and later shipped [new shared\-data serializations](https://clickhouse.com/blog/json-data-type-gets-even-better) that dramatically improved performance and memory usage for complex JSON workloads. As a result, ClickHouse now leads even further across both cold and hot runs at all dataset sizes, with a significantly larger margin than before.


## The input formats benchmark [\#](/blog/what-really-matters-for-performance-lessons-from-a-year-of-benchmarks#the-input-formats-benchmark)


This benchmark came from a deceptively simple question: *if ClickHouse supports [70\+](https://sql.clickhouse.com/?query=c2VsZWN0ICogZnJvbSBzeXN0ZW0uZm9ybWF0cyBXSEVSRSBpc19pbnB1dCBPUkRFUiBCWSBuYW1lOw&chart=eyJ0eXBlIjoibGluZSIsImNvbmZpZyI6eyJ4YXhpcyI6InllYXIiLCJ5YXhpcyI6Ijk5dGhfYXZnX3RlbXAiLCJzZXJpZXMiOiJjb3VudHJ5IiwidGl0bGUiOiJUZW1wZXJhdHVyZSBieSBjb3VudHJ5IGFuZCB5ZWFyIn19&tab=results&run_query=true) input formats, which ones actually matter for high\-throughput ingestion?*


To [answer that properly](https://clickhouse.com/blog/clickhouse-input-format-matchup-which-is-fastest-most-efficient), we built [FastFormats](https://fastformats.clickhouse.com/), a systematic benchmark that isolates **server\-side ingestion cost** and measures **time, CPU usage, memory usage, and file size** across dozens of formats, batch sizes, compression schemes, and pre\-sorting variants.


The headline result was clear and surprisingly consistent:


- **Native format wins** across essentially all scenarios
- **Compression (LZ4 first, ZSTD when bandwidth matters)** is a no\-brainer
- **Pre\-sorting helps**, but much less than people expect
- **Batch size matters more than almost anything else**


![Blog_Formats_003_93c66d9a7e.png](/uploads/Blog_Formats_003_93c66d9a7e_02f027921c.png)
And, like with JSONBench, we also built a [live FastFormats dashboard](https://fastformats.clickhouse.com/) where you can slice results by format, batch size, compression, pre\-sorting, and metric.


![Blog-benchmarks-of-2025.003.png](/uploads/Blog_benchmarks_of_2025_003_4e01fc06f2.png)

> **This is one of my favorite benchmarks this year because it had direct production impact beyond ClickHouse itself.**


Netflix [describes](https://clickhouse.com/blog/netflix-petabyte-scale-logging) how one of their biggest ingestion wins came *directly* from reading this post and looking at the FastFormats results. After seeing that the **native ClickHouse protocol consistently outperformed RowBinary**, they reverse\-engineered the Go client and implemented **native\-protocol encoding with LZ4** in their Java pipeline. The result: lower CPU usage, better memory efficiency, and a system that now ingests **\~5 PB of logs per day** into ClickHouse.


## The object storage cache benchmark [\#](/blog/what-really-matters-for-performance-lessons-from-a-year-of-benchmarks#the-object-storage-cache-benchmark)


This benchmark started from a practical cloud question: why do analytics systems still feel slow even when throughput looks great on paper?


The answer turned out not to be bandwidth, but **latency**. Object storage can deliver decent throughput, but every read still costs hundreds of milliseconds, and for many analytical queries (small, selective, scattered reads), that latency dominates everything else.


To tackle this, we [built](https://clickhouse.com/blog/building-a-distributed-cache-for-s3) and [benchmarked](https://github.com/ClickHouse/examples/tree/main/blog-examples/caches/hot-data/cloud-distributed-cache) a **distributed cache for ClickHouse Cloud**: a shared, low\-latency caching layer that sits between stateless compute nodes and object storage. Instead of each node warming its own isolated cache, hot table data is cached **once** and reused instantly by all nodes.


The benchmarks compare three setups using the same dataset and queries:


- a self\-managed server with local SSDs,
- ClickHouse Cloud with a traditional per\-node filesystem cache,
- ClickHouse Cloud with the new **distributed cache**.


The results:


- For **throughput\-bound scans**, cold queries ran up to **4× faster than a local\-SSD setup**, thanks to shared caching and parallel fetch across cache nodes.
- For **latency\-sensitive scattered reads**, cold queries matched SSD performance, and hot queries consistently hit **sub\-60 ms memory\-speed latency**—*without any local disks at all*.


  

![Blog_caches_002_4142f575eb.png](/uploads/Blog_caches_002_4142f575eb_3945c50438.png)
  

![Blog_caches_003_5834a2afa1.png](/uploads/Blog_caches_003_5834a2afa1_94db65a5a7.png)
The key insight is that **shared caching \+ elastic, stateless compute beats “fast disks”**, even on cold starts. You get faster warm\-ups, no repeated downloads from object storage, and the ability to scale compute up or down without throwing away hot data.



> **This is one of my favorite benchmarks this year because it shows a real architectural shift**.


Cloud\-native analytics doesn’t have to trade elasticity for performance anymore. You can have both.


## The UPDATEs benchmark [\#](/blog/what-really-matters-for-performance-lessons-from-a-year-of-benchmarks#the-updates-benchmark)


For a long time, one sentence followed ClickHouse around: *“Great for analytics, but you can’t really do frequent fast updates.”*


This [benchmark](https://github.com/ClickHouse/examples/tree/main/blog-examples/clickhouse-fast-updates) is where that narrative finally broke.


Accompanied by a [post](https://clickhouse.com/blog/updates-in-clickhouse-3-benchmarks), we benchmarked **every UPDATE mechanism ClickHouse supports** \- classic mutations, on\-the\-fly mutations, ReplacingMergeTree inserts, and the new [standard SQL UPDATEs, implemented as lightweight updates with patch parts](https://clickhouse.com/blog/updates-in-clickhouse-2-sql-style-updates) \- side by side, on the same dataset, hardware, and queries.


The headline result surprised a lot of people:


- **Standard SQL UPDATEs** in ClickHouse are now **up to 1,000× faster** than classic mutations.
- Bulk updates that used to take **minutes now finish in milliseconds**.
- Single\-row updates land in **tens of milliseconds**, comparable to inserts.


![Blog_updates_Part_3_001_9bb4cf35e5.png](/uploads/Blog_updates_Part_3_001_9bb4cf35e5_eadad60b03.png)

> **This is one of my favorite benchmarks this year because it changes how people think about ClickHouse**.


You can now do **frequent, fast updates using standard SQL**, without giving up analytical performance, and without resorting to engine\-specific workarounds.


## The distributed GROUP BY benchmark [\#](/blog/what-really-matters-for-performance-lessons-from-a-year-of-benchmarks#the-distributed-group-by-benchmark)


This benchmark answers the question: *how far can you scale [the same GROUP BY execution model](https://clickhouse.com/blog/clickhouse-parallel-replicas#how-clickhouse-makes-group-by-fast)?*


GROUP BY sits at the core of nearly every analytical query: powering observability dashboards, fueling conversation\-speed AI, agent\-facing analytics, and everything in between.


ClickHouse Cloud’s [parallel replicas](https://clickhouse.com/blog/clickhouse-parallel-replicas) **can scale a single GROUP BY query across all CPU cores of all available compute nodes.**


To evaluate the performance impact, we [benchmarked](https://github.com/ClickHouse/examples/tree/3b6da4b0d0607d4debe5783021ffd2019058637e/blog-examples/ParallelReplicasBench) raw GROUP BY queries over datasets ranging from **tens of millions to 100 billion and even 1 trillion rows**, running the *same query* while progressively scaling from one node to **hundreds of nodes** in ClickHouse Cloud.


The result feels almost fake the first time you see it:


![t1_414ms.gif](/uploads/t1_414ms_socials_3df382020f.gif)
- **100 billion rows aggregated in \~0\.4 seconds**
- **\~240 billion rows per second**, over **1\.4 TB/s** of throughput
- No pre\-aggregation or data reshuffling


![Parallel_Replicas_004_2e1de3a30e.png](/uploads/Parallel_Replicas_004_2e1de3a30e_352e81c02d.png)

> **This is one of my favorite benchmarks this year because it shows how far technical elegance can scale.**


Like a fountain pen or a well\-designed Unix tool, [ClickHouse does one thing exceptionally well: GROUP BY](https://clickhouse.com/blog/clickhouse-parallel-replicas#why-group-by-is-the-beating-heart-of-analytics). The same execution model runs unchanged from a laptop to the cloud, and this benchmark shows the impact. You can take the operation that defines analytical speed and scale it across a fleet of machines without changing the query or the data model.


## Honourable mention: The cloud warehouse cost–performance benchmark [\#](/blog/what-really-matters-for-performance-lessons-from-a-year-of-benchmarks#honourable-mention-the-cloud-warehouse-costperformance-benchmark)


This benchmark zooms out from features entirely and asks a harder question: how does performance actually turn into cost in the cloud?


It gets an honourable mention because its scope is much broader than the others.


The [benchmark](https://github.com/ClickHouse/examples/tree/main/blog-examples/Bench2Cost) started from a simple observation: headline prices are a terrible proxy for real\-world cost. Different systems bill in different units, mapped to very different compute models, which makes price lists hard to compare, and easy to misinterpret.


To make this concrete, [we compared five major cloud warehouses](https://clickhouse.com/blog/cloud-data-warehouses-cost-performance-comparison) using the same analytical workload at multiple scales, then translated raw runtimes into real costs based on each system’s billing model.




> **This benchmark is one of my favorites this year because it reframes the conversation.**


Instead of arguing about list prices or pricing tiers, it shows that efficiency is the real currency. When you measure cost the same way systems actually bill for it, ClickHouse Cloud consistently delivers the most performance per dollar.


![Blog_Costs_animation01_small_de9ac301cc.gif](/uploads/Blog_Costs_animation01_small_de9ac301cc_603f8a4845.gif)
## What a year of benchmarks taught me [\#](/blog/what-really-matters-for-performance-lessons-from-a-year-of-benchmarks#what-a-year-of-benchmarks-taught-me)


Looking back, the common thread across all this work is the role benchmarks play in cutting through assumptions.


They corrected narratives (“ClickHouse can’t do updates”), exposed trade\-offs (latency vs. throughput, speed vs. cost), and validated architectural bets (columnar JSON, stateless cloud compute). In a few cases, they even escaped the blog and changed how real systems were built.


Over the past year, these benchmarks all pointed to the same conclusion: performance is about how efficiently an engine moves and processes data *end\-to\-end*. In practice, that showed up repeatedly:


- Fancy formats don’t matter without batching.
- Raw bandwidth doesn’t matter without latency control.
- Isolated caches don’t matter on elastic compute.
- The storage model doesn’t matter if updates avoid rewriting large amounts of data.
- More compute nodes don’t matter without a scalable execution model.
- Low list prices don’t matter without execution efficiency.


That’s why benchmarks keep showing up in my work: they’re how these end\-to\-end trade\-offs become visible.


Next year, we’ll ship new features, new architectures, and new claims. And we’ll keep doing the same thing we did here: measure first, publish the results, and use the numbers to guide the conversation.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
