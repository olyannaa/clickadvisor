# ClickHouse Cloud on Google Cloud Now Powered by Google Axion Processors: 30–55% Faster Queries, \~15% Fewer Compute Credits


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Cloud on Google Cloud Now Powered by Google Axion Processors: 30–55% Faster Queries, \~15% Fewer Compute Credits

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Apr 22, 2026 · 7 minutes read## Summary

We are migrating our Google Cloud fleet to Axion C4A instances. The results: 30–55% faster ClickBench queries and \~15% fewer compute credits across production workloads

## **Why Axion, and why now** [\#](/blog/google-axion#why_axion_and_why_now)


The C4A instance family, powered by Google Axion processors, offers higher memory bandwidth, and better performance per watt compared to general\-purpose x86 instances.


There was also a concrete operational reason. Several of our largest Google Cloud customers were hitting the performance ceiling of their existing nodes. One customer in particular was experiencing persistent CPU throttling and the lack of capacity under peak query load. Axion gave us a concrete path forward with faster compute and [local SSDs](https://cloud.google.com/blog/products/compute/first-google-axion-processor-c4a-now-ga-with-titanium-ssd).


## **ClickBench results: Google Cloud takes first place** [\#](/blog/google-axion#clickbench_results_google_cloud_takes_first_place)


[ClickBench](https://benchmark.clickhouse.com/) is our open, reproducible benchmark for analytical query performance. It uses a production\-derived, anonymized web analytics dataset with 100 million rows and 43 queries, covering aggregations, filtering, string operations, and complex multi\-column scans.


Before the Axion migration, the December 2024 ClickHouse Cloud Google Cloud results (publicly available at the link above) recorded a data load time of 1,080 seconds for the 24 GB service tier and 613 seconds for the dev tier on x86\-based N2D instances.


When we migrated the automated ClickBench test environment to Axion C4A instances in March 2026, the step\-change was immediately visible in the benchmark history. Every one of the 43 queries improved by 30\-55% per query, uniformly across the full query set. Load time dropped by roughly half. The shift was so consistent that it showed up as a clear overnight discontinuity in the benchmark trend line.


As of March 11, 2026, ClickHouse Cloud on Google Cloud holds first place on the combined [ClickBench ranking](https://benchmark.clickhouse.com/#system=+%E2%98%81w%7C%EF%B8%8Fr%7CC%20c&type=-&machine=-ca2l%7C6t%7Cg4e%7C6ax%7C6ale%7C3al%7Co%E2%98%818%7Ck12%7Ck16%7Cu%EF%B8%8F4%7C0i%7C23%7C%E2%98%815&cluster_size=-&opensource=-&hardware=+c&tuned=+n&metric=combined&queries=-) \- the best result across all configurations and systems tracked by the benchmark. You can see the current live results at [benchmark.clickhouse.com](https://benchmark.clickhouse.com/).


This tracks with what we observed in earlier controlled benchmarking, where we ran ClickBench across equivalent VM sizes (8 CPUs, 32 GiB memory) comparing C4A\-standard\-8 Axion instances against n2d\-standard\-8 instances at 1, 2, and 3 replicas. The C4A instances outperformed N2D across every replica count \- a consistent advantage rather than a narrow edge on specific query shapes. For compute\-bound analytical workloads, the improvements from C4A on N2D is in the range of 50\-100%, using \~15% fewer compute credits per query on average. For analytical query patterns similar to ClickBench, the benefit is substantially larger.


![](/uploads/axion_apr2026_image3_aa1e5c8261.png)
![](/uploads/axion_apr2026_image2_99a5e3ce49.png)

> "*We had high hopes for the Axion migration, and it exceeded them. CPU throttling that had been a persistent problem under peak load essentially disappeared overnight. Our team noticed the difference immediately \- the cluster just feels stable in a way it didn't before."*
> 
> 
> \-Anders Aagaard *Principal* *Engineer, Nansen*


There is also a subtler benefit: thermal and frequency stability. x86 instances frequently experience clock frequency variation under sustained load, particularly in multi\-tenant environments. Axion Arm\-based cores tend to maintain more consistent throughput. Another difference is that x86 1 physical core \= 2 logical vCPUs, while Axion offers one. For ClickHouse, where query latency is directly tied to how many rows per second the CPU can process, that consistency matters.


## **The migration approach** [\#](/blog/google-axion#the_migration_approach)


We began the Axion migration in our staging environments and internal clusters, and crafted an automated workflow with multiple safety checks and validations along the way.


From there, we expanded to a controlled rollout across Google Cloud regions, coordinating with the Google Cloud team on regional capacity. This gave us the ability to observe and compare services before and after migration within the same time windows, which is essential for clean performance attribution.


Not everyone waited for the automated rollout. A handful of customers on Google Cloud reached out proactively to migrate early. One, a large analytics platform running high\-frequency on\-chain data queries, requested C4A instances ahead of the general schedule. Another, a global enterprise customer running demanding analytics at scale, flagged Axion migration as a top priority and was moved to C4A before the broader rollout. These early migrations gave us production data on Axion performance at scale before the broader rollout.


For services that require migration, the process follows a few checks:


- Is the service running on [SharedCatalog](https://clickhouse.com/blog/clickhouse-cloud-stateless-compute) (our compute\-storage separated storage model)? Services still using legacy attached volumes require an additional step to migrate storage first.
- What is the service's maintenance window? Migrations are scheduled during low\-traffic periods.
- Is the service among the top\-traffic organizations in Google Cloud? These are migrated last, after we've built confidence in the process across a broader set of services.


## **What we observed: fleet\-wide efficiency** [\#](/blog/google-axion#what_we_observed_fleet_wide_efficiency)


To quantify the impact at scale, we analyzed a cohort of 38 services that had completed the x86\-to\-Axion migration and had at least two weeks of stable pre\- and post\-migration data. We controlled for services with significant compute credit variance, services that don't scale, and services with unusual traffic patterns around the migration date.


The result: \~15% improvement in compute credits per query across this cohort. Customers are running the same queries and spending 15% fewer credits after their service moves to Axion.  

That number might sound modest in isolation, but it reflects a conservative and rigorous measurement. We are looking at real production traffic, not a synthetic benchmark. The workloads are diverse \- dashboards, ingest pipelines, ad hoc analytics, API\-backed queries. Not all of them are CPU\-bound; some are dominated by Google Cloud Storage read throughput, where the processor architecture matters less. The fleet\-wide average, therefore, understates the benefit for compute\-heavy workloads.


For services that are primarily CPU\-bound \- complex aggregations, multi\-join queries, heavy decompression \- the improvement is substantially larger. ClickBench makes this concrete.


## **What comes next** [\#](/blog/google-axion#what_comes_next)


The migration is ongoing. We are progressively expanding to all Google Cloud regions where C4A capacity is available, working through the top\-traffic organizations after building a track record of clean migrations across the broader fleet.


Longer term, we expect Axion to become the standard instance type for ClickHouse Cloud on Google Cloud. The performance and efficiency case is clear. The migration tooling is proven.  

For customers on Google Cloud, the migration is transparent. Your data does not move, your queries do not need to change, and the improvement in performance shows up automatically once your service is migrated. We will notify you in advance of your scheduled migration window.


## **Final thoughts** [\#](/blog/google-axion#final_thoughts)


The efficiency gains from Axion are real (\~15% fewer compute credits per query across the fleet and 30–55% faster ClickBench results), the migration was seamless, and the customer impact is tangible. For columnar, compute\-intensive workloads like ClickHouse, modern ARM processors offer a measurable advantage over general\-purpose x86 \- and the data from real customer workloads bears out what the benchmarks predict.


The close collaboration with the Google Cloud Axion team, especially in regional capacity planning and co\-engineering support throughout this rollout, helped accelerate the upgrade.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-458-get-started-today-sign-up&utm_blogctaid=458)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
