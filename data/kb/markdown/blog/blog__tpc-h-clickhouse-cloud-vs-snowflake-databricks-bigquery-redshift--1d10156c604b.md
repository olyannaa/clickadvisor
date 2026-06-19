# TPC\-H for less than a cent: ClickHouse Cloud vs. Snowflake, Databricks, BigQuery, and Redshift


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# TPC\-H for less than a cent: ClickHouse Cloud vs. Snowflake, Databricks, BigQuery, and Redshift

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U033_M877_CU_9_2dc2d2d2cf7c_512_e14944ce54.jpeg&w=96&q=75)![](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U0_AQPHH_8_WKF_767729e121c5_512_73ae429976.jpeg&w=96&q=75)![](/_next/image?url=%2Fuploads%2Frobert_schulze_fc3979ae99.png&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber), [Mark Needham](/authors/mark-needham), [Alexander Gololobov](/authors/alexander-gololobov), [Andriy Yakovlev](/authors/andriy-yakovlev) and [Robert Schulze](/authors/robert-schulze)Jun 2, 2026 · 11 minutes read
> **TL;DR**  
> On TPC\-H SF100, a single 59\-core ClickHouse Cloud node is competitive on raw runtime against Snowflake, Databricks, BigQuery, and Redshift, while ranking first on cost\-performance. At SF10, it runs all 22 queries for less than one cent.


  

## ClickHouse Cloud joins the TPC\-H comparison [\#](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift#clickhouse-cloud-joins-the-tpc-h-comparison)


We ran the full [TPC\-H](https://clickhouse.com/docs/getting-started/example-datasets/tpch) workload on ClickHouse Cloud, Snowflake, Databricks, BigQuery, and Redshift.


At SF100, that is 100 GB of data, 866M rows, and 22 join\-heavy analytical queries.


The result: ClickHouse Cloud was competitive on raw runtime and ranked first on cost\-performance.


At SF10, the full workload ran in 2\.9 seconds for $0\.009 in compute cost.


Less than one cent.


This post shows the benchmark results. The [companion post](/blog/clickhouse-fast-joins) explains the two years of join engineering behind them.


## Benchmark setup [\#](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift#benchmark-setup)


All benchmark scripts, queries, and result files are available in a public GitHub [repository](https://github.com/ClickHouse/tpc-h-openhouse), so the results can be reproduced and inspected.


### Dataset and runtime measurement [\#](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift#dataset-and-runtime-measurement)


The main comparison uses TPC\-H SF100: 22 queries over 866M rows.


For runtime measurements, we distinguish between cold and hot runs:


**Cold runs**: We did not systematically compare cold\-start performance. Cloud warehouses exhibit different caching behavior, and most do not let users reliably reset OS\-level page cache or restart compute on demand. Because cold conditions cannot be standardized, cold results would not be fair or reproducible.


**Hot runs**: Each query was run three times with result caching disabled. Charts use the fastest hot run. Result caching was disabled, so the benchmark measures query execution, not returning a previously cached result.


### Compared systems [\#](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift#compared-systems)


For **ClickHouse Cloud**, we used one fixed configuration: a single AWS compute node with 59 cores. For the other systems, we selected practical warehouse or serverless capacity configurations, and discuss the closest hardware comparisons later.


- **Snowflake**: Small, Medium, Large, and 4X\-Large Gen2 [warehouses](https://clickhouse.com/blog/how-cloud-data-warehouses-bill-you#snowflake)
- **Databricks (SQL Serverless)**: Small, Medium, Large, and 4X\-Large [warehouses](https://clickhouse.com/blog/how-cloud-data-warehouses-bill-you#databricks-sql-serverless)
- **BigQuery**: 2,000 [slots](https://clickhouse.com/blog/how-cloud-data-warehouses-bill-you#bigquery)
- **Redshift Serverless**: 128 [RPUs](https://clickhouse.com/blog/how-cloud-data-warehouses-bill-you#redshift-serverless)


### Cost calculations [\#](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift#cost-calculations)


For cost calculations, we use the same methodology introduced in our earlier posts on cloud data warehouse [billing](https://clickhouse.com/blog/how-cloud-data-warehouses-bill-you) and [cost\-performance](https://clickhouse.com/blog/cloud-data-warehouses-cost-performance-comparison). We apply each vendor’s public billing model to the measured query runtimes, [assume perfect per\-second compute billing](https://clickhouse.com/blog/cloud-data-warehouses-cost-performance-comparison#a-note-on-metering-granularity) for all systems, and use Enterprise\-tier pricing in comparable US East regions: AWS `us-east` for supported systems and GCP `us-east` for BigQuery.


With that setup, we first look at raw hot runtime.


## TPC\-H SF100: raw hot runtime [\#](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift#tpc-h-sf100-raw-hot-runtime)


[TPC\-H SF100](https://clickhouse.com/docs/getting-started/example-datasets/tpch) consists of **100 GB of data**, **866M rows**, and **22 join\-heavy analytical queries**.


In the diagram below, each bar sums the fastest of three runs for each of the 22 TPC\-H queries. Lower is better.


![Blog-JOINS-results.001.png](/uploads/Blog_JOINS_results_001_43c308f4a0.png)
**ClickHouse Cloud** completed the workload in [19\.8s](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/clickhouse-cloud/results_sf100/aws.1.236_run_01_sf100.json).


**Snowflake** finished in [32\.7s](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/snowflake/results_sf100/snowflake_sf100_small_gen2.json) on a Small warehouse, [22\.9s](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/snowflake/results_sf100/snowflake_sf100_medium_gen2.json) on Medium, [15\.9s](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/snowflake/results_sf100/snowflake_sf100_large_gen2.json) on Large, and [14\.7s](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/snowflake/results_sf100/snowflake_sf100_4xl_gen2.json) on 4X\-Large.


**Databricks** finished in [37\.3s](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/databricks/results_sf100/databricks_sf100_Small.json) on a Small warehouse, [40\.0s](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/databricks/results_sf100/databricks_sf100_medium.json) on Medium, [28\.9s](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/databricks/results_sf100/databricks_sf100_large.json) on Large, and [26\.4s](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/databricks/results_sf100/databricks_sf100_4xlarge.json) on 4X\-Large.


**BigQuery** finished in [26\.2s](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/bigquery/results_sf100/results.json) with 2,000 slots.


**Redshift Serverless** finished in [30\.7s](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/redshift/results_sf100/results.json) with 128 RPUs.


Note that the compute behind these numbers is not identical across systems. ClickHouse Cloud used one Graviton3 compute node with 59 cores and 236 GiB of memory.


For Snowflake and Databricks, we tested multiple warehouse sizes to show how runtime changes as compute scales. The closest hardware reference points to ClickHouse Cloud’s 59\-core node are Snowflake Large Gen2, [understood](https://select.dev/posts/snowflake-warehouse-sizing) to [use](https://medium.com/snowflake-engineering/deep-dive-inside-snowflakes-new-gen2-standard-warehouses-powered-by-aws-graviton3-6aacca73ae2d) 64 AWS Graviton3 cores and 128 GB of memory, and Databricks Large, which [maps](https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior#sizing-and-cluster-provisioning) to 64 Intel Xeon E5\-2686 v4 cores and 488 GiB of memory in the documented classic compute\-plane sizing. We used Databricks SQL [Serverless](https://docs.databricks.com/aws/en/getting-started/high-level-architecture#serverless-workspace-architecture) for the benchmark, but the published warehouse sizing provides a useful reference point.


Also note that systems with serverless capacity models automatically fan out query work across large, pre\-provisioned compute pools: BigQuery used up to 2,000 [slots](https://clickhouse.com/blog/how-cloud-data-warehouses-bill-you#bigquery) in this benchmark, and Redshift Serverless used 128 [RPUs](https://clickhouse.com/blog/how-cloud-data-warehouses-bill-you#redshift-serverless).



> With one 59\-core compute node, **ClickHouse Cloud is competitive** on raw TPC\-H SF100 runtime against major cloud data warehouses, including comparable 64\-core Snowflake and Databricks warehouse configurations and serverless engines that automatically fan out across large pre\-provisioned compute pools far beyond 59 cores.


## Runtime is only half the story [\#](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift#runtime-is-only-half-the-story)


As mentioned above, it is hard to directly compare the compute each system used to run the TPC\-H SF100 workload.


But we can directly compare the [cost](https://clickhouse.com/blog/cloud-data-warehouses-cost-performance-comparison) of running the workload.


The chart below keeps the same runtime bars and overlays the hot\-run compute cost using each vendor’s public [billing model](https://clickhouse.com/blog/how-cloud-data-warehouses-bill-you).


![Blog-JOINS-results.002.png](/uploads/Blog_JOINS_results_002_b4220f44f7.png)
**ClickHouse Cloud** finished the workload in 19\.8s with a compute cost of [$0\.063](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/clickhouse-cloud/results_enriched_sf100/aws.1.236_run_01_sf100.json).


**Snowflake** Large was faster at 15\.9s, but cost [$0\.143](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/snowflake/results_enriched_sf100/snowflake_sf100_large_gen2_enriched.json). Snowflake 4X\-Large was faster again at 14\.7s, but cost [$2\.121](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/snowflake/results_enriched_sf100/snowflake_sf100_4xl_gen2_enriched.json). **Databricks** ranged from [$0\.087](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/databricks/results_enriched_sf100/databricks_sf100_Small_enriched.json) to [$2\.714](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/databricks/results_enriched_sf100/databricks_sf100_4xlarge_enriched.json). **BigQuery** finished in 26\.2s for [$0\.163](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/bigquery/results_enriched_sf100/results_enriched.json), and **Redshift Serverless** in 30\.7s for [$0\.436](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/redshift/results_enriched_sf100/enriched_results.json).


The section below collapses runtime and cost into a single cost\-performance score.


## TPC\-H SF100: cost\-performance ranking [\#](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift#tpc-h-sf100-cost-performance-ranking)


The previous chart showed runtime and cost side by side. Now we combine both into a simple [cost\-performance score](https://clickhouse.com/blog/cloud-data-warehouses-cost-performance-comparison#how-we-measure-overall-cost-performance-ranking):


`cost-performance score = compute cost × runtime`


Lower is better.


That lets us answer the real cloud benchmark question:



> Who gives the most join performance per dollar?


Fast systems score better. Low\-cost systems score better. Slow or expensive systems fall behind quickly. And when a system is both slower and more expensive, the two effects compound.


![Blog-JOINS-results.003.png](/uploads/Blog_JOINS_results_003_cf3d793dd4.png)
**ClickHouse Cloud** ranks first.


The next closest configurations were **Snowflake** Large and Snowflake Medium, both about 2× worse. **Databricks** Small and **BigQuery** with 2,000 slots are at 3× worse. **Databricks** Large and Medium followed at 5× and 6× worse.


At the high end, **Redshift Serverless** was 11× worse, Snowflake 4X\-Large was 25× worse, Databricks 4X\-Large was 57× worse, and BigQuery [On\-demand](https://clickhouse.com/blog/how-cloud-data-warehouses-bill-you#compute-pricing-3) was 67× worse.



> ClickHouse Cloud delivers the best cost\-performance on TPC\-H SF100: lowest score overall, with the nearest tested configurations about 2× worse.


## TPC\-H SF100: per\-query runtime breakdown [\#](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift#tpc-h-sf100-per-query-runtime-breakdown)


For completeness, here is the per\-query runtime breakdown. Each bar shows the fastest of three runs for one of the 22 TPC\-H queries.


![Blog-JOINS-results.004.png](/uploads/Blog_JOINS_results_004_71f35d37c4.png)
The aggregate result is not driven by one outlier. ClickHouse Cloud is consistently competitive across the full query set.


## Scaling down: TPC\-H for less than a cent [\#](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift#scaling-down-tpc-h-for-less-than-a-cent)


SF100 is the main benchmark in this post. But scaling down to SF10 gives us the title moment.


At SF10, the workload contains **86M rows** across the same **22 join\-heavy TPC\-H queries**.


On the same ClickHouse Cloud configuration with one 59\-core compute node, the full hot workload ran in [2\.9s](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/clickhouse-cloud/results_sf10/aws.1.236_run_01_sf10.json) with a compute cost of [$0\.009](https://github.com/ClickHouse/tpc-h-openhouse/blob/main/clickhouse-cloud/results_enriched_sf10/aws.1.236_run_01_sf10.json).


![Blog-JOINS-results.005.png](/uploads/Blog_JOINS_results_005_f2a4c0e257.png)
The chart below collapses runtime and cost into a single cost\-performance score to answer the “Who gives the most join performance per dollar?” question.


![Blog-JOINS-results.006.png](/uploads/Blog_JOINS_results_006_84c9e91fa5.png)
At this scale, **ClickHouse Cloud** wins on both dimensions: it is the fastest tested configuration and the cheapest to run. **Snowflake** was next in terms of cost\-performance, but still **8× worse**. **BigQuery** was **12× worse**, **Redshift** Serverless **27× worse**, and the larger Snowflake and **Databricks** configurations were much further behind.



> At SF10, ClickHouse Cloud runs all 22 TPC\-H queries in 2\.9s for less than one cent, and delivers the best cost\-performance by a wide margin.


## Scaling up: SF1000 and beyond [\#](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift#scaling-up-sf1000-and-beyond)


The SF100 results show where ClickHouse is today: with a single 59\-core compute node, ClickHouse Cloud is competitive on both runtime and cost\-performance against major cloud data warehouses, including systems using larger or more elastic compute configurations.


But SF100 is not the end of the story.


For much larger scale factors, such as **TPC\-H SF1000 and beyond**, join execution needs to scale across multiple nodes properly. That is where the engineering team is focusing next, with [multi\-stage distributed query execution](/blog/multi-stage-distributed-query-execution-clickhouse-cloud) for large distributed joins in ClickHouse Cloud.


That is the next chapter. This one was made possible by the last two years of join engineering.


## How we got here [\#](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift#how-we-got-here)


The results above are the outcome of two years of focused join engineering at ClickHouse.


![Blog-JOINS-results.007.png](/uploads/Blog_JOINS_results_007_7f6820e069.png)
A year into that effort, the same TPC\-H SF100 join\-heavy workload was already **4\.4× faster than in 22\.4**. One year later, it is now **26× faster overall**, with the last year alone contributing another **6× improvement** under default settings.


That progress came from improvements across the stack: faster hash joins, better planning, correlated subquery support, lazy column replication, runtime filters, and statistics\-based join reordering.


The [companion post](/blog/clickhouse-fast-joins) explains the engineering story behind those numbers: how ClickHouse went from “fast, but not for joins” to competitive join performance by default.



> Two years of focused join engineering made ClickHouse 26× faster on the TPC\-H SF100 join\-heavy workload, and that is what made these benchmark results possible.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
