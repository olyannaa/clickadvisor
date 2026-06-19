# Join me if you can: ClickHouse vs. Databricks vs. Snowflake \- Part 1


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Join me if you can: ClickHouse vs. Databricks vs. Snowflake \- Part 1

![Al Brown](/_next/image?url=%2Fuploads%2Fal_brown_headshot_09ae0cbce6.jpg&w=96&q=75)![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Al Brown](/authors/al-brown) and [Tom Schreiber](/authors/tom-schreiber)Jun 24, 2025 · 10 minutes read## TL;DR

We took a public benchmark that tests join\-heavy SQL queries on Databricks and Snowflake and ran the exact same queries on ClickHouse Cloud.  
  
ClickHouse was **faster and cheaper** at every scale, from 721 million to 7\.2 billion rows.

## ”ClickHouse can’t do joins.” Let’s test that [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#clickhouse-cant-do-joins-lets-test-that)


Let’s be crystal clear upfront: **this is not our benchmark**.


Someone else designed a [coffee\-shop\-themed benchmark](https://github.com/JosueBogran/coffeeshopdatageneratorv2) to [compare cost and performance when running join\-heavy queries on Databricks and Snowflake](https://www.linkedin.com/pulse/databricks-vs-snowflake-gen-1-2-sql-performance-test-day-bogran-ddmhe/), across different compute sizes. The benchmark author shared the full dataset and query suite publicly.


Out of curiosity, we took that same benchmark, loaded the data into ClickHouse Cloud, used similar instance sizes, and ran the original 17 queries. Most queries involve joins, and we didn’t rewrite them (queries 6, 10 and 15 required minor syntax changes to work in ClickHouse SQL dialect).



> We did **no tuning at all**, not for the queries, and not on the ClickHouse side (no changes to table schemas, indexes, settings, etc).


Next time someone says “ClickHouse can’t do joins,” **just send them this blog**.


We’ve spent the past 6 months [making join performance radically better in ClickHouse](https://youtu.be/gd3OyQzB_Fc?si=Fso5oedhSHYYW16L&t=137), and this post is your first look at how far we’ve come. (*Spoiler: it’s really fast. And really cheap. And we’re just getting started.*)


We’ll walk through how we ran the benchmark, how you can run it too, and then walk through the full results across three dataset sizes: 721 million, 1\.4 billion, and 7\.2 billion rows.


Finally, we’ll wrap up with a simple takeaway: ClickHouse can do joins, and it can do it fast.


## How to reproduce it [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#how-to-reproduce-it)


You’ll find everything in the [coffeeshop\-benchmark GitHub repo](https://github.com/ClickHouse/coffeeshop-benchmark/tree/main), including all [17 benchmark queries](https://github.com/ClickHouse/coffeeshop-benchmark/blob/main/clickhouse-cloud/queries.sql), scripts, and [instructions to execute the benchmark](https://github.com/ClickHouse/coffeeshop-benchmark/tree/main/clickhouse-cloud#clickhouse-cloud-benchmark-runner). We’ve also published the [full coffeeshop\-benchmark datasets in a public S3 bucket](https://github.com/ClickHouse/coffeeshop-benchmark/tree/main?tab=readme-ov-file#get-the-data), so you can skip the generation step and jump straight to testing ClickHouse Cloud vs. Snowflake vs. Databricks.


The whole [benchmark is automated](https://github.com/ClickHouse/coffeeshop-benchmark/tree/main/clickhouse-cloud#clickhouse-cloud-benchmark-runner): spin up a ClickHouse Cloud service, set your credentials via environment variables, and run one command with your cluster specs and [price per compute unit](https://clickhouse.com/pricing).


Click a button. Grab a coffee. And your results are ready.


We run each query 5 times and report the fastest run, to reflect warm\-cache performance fairly. [See full results.](https://github.com/ClickHouse/coffeeshop-benchmark/tree/main/clickhouse-cloud/results)

### Ready to try it yourself?

Spin up your own ClickHouse Cloud service in minutes and run the benchmark end\-to\-end. No setup headaches, and $300 in free credits to get you started.[Sign up](https://console.clickhouse.cloud/signUp?loc=global-blog-cta&utm_blogctaid=402)## One dataset, many runs: how we benchmarked at scale [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#one-dataset-many-runs-how-we-benchmarked-at-scale)


To speed up the benchmarking process, we took advantage of [ClickHouse Cloud Warehouses](https://clickhouse.com/blog/introducing-warehouses-compute-compute-separation-in-clickhouse-cloud), a feature that lets you spin up multiple compute services over a single shared dataset.


We ingested the data once, then spun up additional services in different sizes, **varying the number of nodes, CPU cores, and RAM**, to benchmark different hardware and cost configurations.


Because all services in a ClickHouse Cloud Warehouse share the same data, we could run the same benchmark across all configurations at once, without reloading anything.


This also let us test [ClickHouse Cloud’s Parallel Replicas](https://clickhouse.com/docs/deployment-guides/parallel-replicas) feature, where **multiple compute nodes process a single query in parallel** for even faster results.


## Benchmark structure [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#benchmark-structure)


The original benchmark was posted in two parts on LinkedIn ([part 1](https://www.linkedin.com/pulse/databricks-vs-snowflake-sql-performance-test-day-1-721m-bogran-lsboe/) and [part 2](https://www.linkedin.com/pulse/databricks-vs-snowflake-gen-1-2-sql-performance-test-day-bogran-ddmhe/)), using synthetic data that simulates orders at a national coffee chain. It tested three data scales for the main fact table:




| Scale factor | Total rows in fact table (Sales) |
| --- | --- |
| 500m | 721m |
| 1b | 1\.4b |
| 5b | 7\.2b |


All three data scales use the same [star schema](/resources/engineering/real-time-analytics-star-schema-joins) with **three tables**:


- **Sales**: the main fact table (orders)
- **Products**: product dimension
- **Locations**: store/location dimensions


[The benchmark consists of 17 SQL queries](https://github.com/JosueBogran/coffeeshopdatageneratorv2/blob/2a99993b6bca94c0bc04fae7c695e86cd152add1/Performance%20Test%20Queries.sql), most involving **joins** between the fact and one or both dimension tables. All queries were run **sequentially**.


Part 1 of the original benchmark covered the smaller 721 million row scale, and part 2 added results for the 1\.4 billion and 7\.2 billion row scales.


This post mirrors the structure and layout of the original benchmark posts: same queries, same chart style, same order, just re\-run to compare ClickHouse Cloud vs. Snowflake vs. Databricks. For each scale, we report:


- **Total cost** (USD)
- **Total runtime** (seconds)
- **Cost per query** (excluding Q10 \& Q16\)
- **Seconds per query** (excluding Q10 \& Q16\)
- **Cost per query** (Q10 \& Q16 only)
- **Seconds per query** (Q10 \& Q16 only)


Queries 10 and 16 are significantly slower than the other queries and would compress the scale of the other queries on the charts. That’s why the original posts listed them separately.


The original benchmark included both “Clustered” and “Non\-clustered” variants. (Here, “Clustered” means the data was physically sorted and co\-located to improve query performance, especially on large tables.) For consistency, we report only the **Clustered** results here.



> **Methodology \& setup:**  
>   
> In the original benchmark results appear to be hot runs. We run each query 5 times and report the fastest run, to reflect warm\-cache performance fairly.  
>   
> All results shown here are based on the ClickHouse Cloud [Scale tier](https://clickhouse.com/pricing?plan=scale&provider=aws&region=us-east-1&hours=8&storageCompressed=false), using services deployed on AWS in the us\-east\-2 region. The [full results](https://github.com/sdairs/coffeeshop-benchmark/tree/main/clickhouse-cloud/results) also include Enterprise tier costs, which still compare favorably.  
>   
> All services were running ClickHouse 25\.4\.1, with parallel replicas enabled by default.


You’ll find the full chart sets below, presented without further commentary. All context is in the original LinkedIn posts, and we’ll wrap up with a clear takeaway.


In the charts below, ClickHouse Cloud results follow the label format `CH 2n_30c_120g`, where:


- `2n` \= number of compute nodes
- `30c` \= CPU cores per node
- `120g` \= RAM per node (in GB)


All service configurations use 30 cores and 120 GB RAM per node, with 4 service sizes tested: 2, 4, 8, and 16 compute nodes.


The label meanings for Databricks (e.g. `DBX_S`) and Snowflake (e.g. `SF_S_Gen2`) are unchanged and documented in the original posts.


## Results: 500m scale (721m rows) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#results-500m-scale-721m-rows)


This scale uses a seed of 500m orders to generate a total of 721m rows.


### Total cost [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#total-cost)


![total_cost_500m.png](/uploads/total_cost_500m_f80a9e8196.png)

> Each bar also shows the total runtime for all 17 queries, shown in parentheses.


### Total runtime [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#total-runtime)


![total_perf_500m.png](/uploads/total_perf_500m_e8089e6f24.png)

> Each bar also shows the total cost for running all 17 queries, shown in parentheses.


### Cost per query (excluding Q10 \& Q16\) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#cost-per-query-excluding-q10--q16)


![cost_excl_q10_q16_500m.png](/uploads/cost_excl_q10_q16_500m_4b671d6b7d.png)
### Runtime per query (excluding Q10 \& Q16\) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#runtime-per-query-excluding-q10--q16)


![perf_excl_q10_q16_500m.png](/uploads/perf_excl_q10_q16_500m_1a59901ab6.png)
### Cost per query (Q10 \& Q16 only) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#cost-per-query-q10--q16-only)


![cost_q10_q16_500m.png](/uploads/cost_q10_q16_500m_dcfc739459.png)
### Runtime per query (Q10 \& Q16 only) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#runtime-per-query-q10--q16-only)


![perf_q10_q16_500m.png](/uploads/perf_q10_q16_500m_692d360b68.png)
## Results: 1b scale (1\.4b rows) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#results-1b-scale-14b-rows)


This scale uses a seed of 1b orders to generate a total of 1\.4b rows.


### Total cost [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#total-cost-1)


![total_cost_1b.png](/uploads/total_cost_1b_4f6f1ce578.png)

> Each bar also shows the total runtime for all 17 queries, shown in parentheses.


### Total runtime [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#total-runtime-1)


![total_perf_1b.png](/uploads/total_perf_1b_5d6410220b.png)

> Each bar also shows the total cost for running all 17 queries, shown in parentheses.


### Cost per query (excluding Q10 \& Q16\) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#cost-per-query-excluding-q10--q16-1)


![cost_excl_q10_q16_1b.png](/uploads/cost_excl_q10_q16_1b_f7db403624.png)
### Runtime per query (excluding Q10 \& Q16\) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#runtime-per-query-excluding-q10--q16-1)


![perf_excl_q10_q16_1b.png](/uploads/perf_excl_q10_q16_1b_82f8f0e2f9.png)
### Cost per query (Q10 \& Q16 only) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#cost-per-query-q10--q16-only-1)


![cost_q10_q16_1b.png](/uploads/cost_q10_q16_1b_7494c666b8.png)
### Runtime per query (Q10 \& Q16 only) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#runtime-per-query-q10--q16-only-1)


![perf_q10_q16_1b.png](/uploads/perf_q10_q16_1b_deff890467.png)
## Results: 5b scale (7\.2b rows) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#results-5b-scale-72b-rows)


This scale uses a seed of 5b orders to generate a total of 7\.2b rows.


### Total cost [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#total-cost-2)


![total_cost_5b.png](/uploads/total_cost_5b_343416146f.png)

> Each bar also shows the total runtime for all 17 queries, shown in parentheses.


### Total runtime [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#total-runtime-2)


![total_perf_5b.png](/uploads/total_perf_5b_149633e506.png)

> Each bar also shows the total cost for running all 17 queries, shown in parentheses.


### Cost per query (excluding Q10 \& Q16\) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#cost-per-query-excluding-q10--q16-2)


![cost_excl_q10_q16_5b.png](/uploads/cost_excl_q10_q16_5b_18f629315e.png)
### Runtime per query (excluding Q10 \& Q16\) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#runtime-per-query-excluding-q10--q16-2)


![perf_excl_q10_q16_5b.png](/uploads/perf_excl_q10_q16_5b_2a25e25670.png)
### Cost per query (Q10 \& Q16 only) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#cost-per-query-q10--q16-only-2)


![cost_q10_q16_5b.png](/uploads/cost_q10_q16_5b_8fd85933c8.png)
### Runtime per query (Q10 \& Q16 only) [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#runtime-per-query-q10--q16-only-2)


![perf_q10_q16_5b.png](/uploads/perf_q10_q16_5b_1ef9d41592.png)
## What we learned and what’s next [\#](/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance#what-we-learned-and-whats-next)


ClickHouse is fast with joins. Really fast, across all scales.


The 17 queries in this benchmark focus on practical join workloads: 2–3 tables, no tuning, no rewrites. We ran them as\-is to see how ClickHouse stacks up.


- **At 500m scale**, most queries complete in **under 1 second**, with ClickHouse consistently **3–5× faster** than the alternatives. And cheaper.
- **At 1b scale**, ClickHouse joins, aggregates, and sorts **1\.7 billion rows in [just half a second](https://github.com/sdairs/coffeeshop-benchmark/blob/e1837073012e69da25845d45c90a21fa215c2c13/clickhouse-cloud/results/result_v25_4_1_1b_16n_30c_120g_20250620_141435.json#L132)**, while other systems need **5 to 13 seconds**, and still cost more.
- **At 5b scale**, even the heaviest queries finish in **seconds, not minutes**, with ClickHouse staying the fastest and cheapest option overall.


We didn’t do anything special to get these results, no config tweaks, no ClickHouse\-specific tricks. Just a clean run of the original benchmark.



> In [part 2](https://clickhouse.com/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-part-2), we’ll show you how to make it truly fast, the ClickHouse way, with a few powerful tricks up our sleeve.


Behind the scenes, we’ve spent the last 6 months making joins in ClickHouse much faster and more scalable, from improved planning and memory efficiency to better execution strategies.



  
  
And we’re not stopping here.


Next, we’re turning up the difficulty: full [TPC\-H](https://clickhouse.com/docs/getting-started/example-datasets/tpch), up to 8\-way joins.


Want to see how ClickHouse handles the most demanding joins? Stay tuned for our TPC\-H results.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
