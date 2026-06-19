# Postgres CDC connector for ClickPipes is now Generally Available


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Postgres CDC connector for ClickPipes is now Generally Available

![Sai Srirampur](/_next/image?url=%2Fuploads%2Fdisplay_pic_copy_5b0aedef94.jpeg&w=96&q=75)[Sai Srirampur](/authors/sai-srirampur)May 29, 2025 · 7 minutes readToday we are thrilled to announce that the [Postgres CDC connector](https://clickhouse.com/cloud/clickpipes/postgres-cdc-connector) for ClickPipes is now generally available. With this customers can easily replicate their Postgres databases to ClickHouse Cloud within just a few clicks.


This announcement represents a major milestone. [PeerDB](https://www.peerdb.io/) — a leading Postgres CDC company we [joined forces](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database) with last year, is now fully integrated into ClickHouse Cloud as the Postgres CDC connector in ClickPipes. The connector is ready to support enterprise\-grade Postgres use cases.



> [Sign up for ClickHouse Cloud](https://console.clickhouse.cloud/signup) today to try out the [Postgres CDC connector for ClickPipes](https://clickhouse.com/docs/integrations/clickpipes/postgres)!



## Postgres \+ ClickHouse \= “the default data stack” [\#](/blog/postgres-cdc-connector-clickpipes-ga#postgres--clickhouse--the-default-data-stack)


Over the past few years, we are seeing a consistent pattern emerge across businesses incl. [GitLab](https://about.gitlab.com/blog/2022/04/29/two-sizes-fit-most-postgresql-and-clickhouse/), [CloudFlare](https://blog.cloudflare.com/http-analytics-for-6m-requests-per-second-using-clickhouse?glxid=25d1a1c5-1ce0-4589-8305-177654961925&pagePath=%2Fblog%2Fclickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database&origPath=%2Fblog%2Fclickhouse-acquires-peerdb-to-boost-real-time-analytics-with-postgres-cdc-integration&utm_ga=GA1.1.1147851049.1729970044/) and [Instacart](https://tech.instacart.com/real-time-fraud-detection-with-yoda-and-clickhouse-bd08e9dbe3f4): Using Postgres and ClickHouse together to solve most of their data challenges.


- **Postgres** serves as the system of record powering transactional web apps.
- **ClickHouse** powers real\-time analytical and reporting workloads, serving as the system of analysis.


This pattern is accelerating in the AI era, with companies like [LangChain](https://clickhouse.com/blog/langchain-why-we-choose-clickhouse-to-power-langchain), [LangFuse](https://langfuse.com/blog/2024-12-langfuse-v3-infrastructure-evolution) and [Vapi](https://neon.tech/blog/vapi-voice-agents-neon) adopting the same architecture. We believe Postgres \+ ClickHouse is becoming the default data stack for modern businesses. We're committed to making that integration magical. The Postgres CDC connector is **the first major step**—enabling seamless, real\-time analytics by bringing your Postgres data into ClickHouse effortlessly.


The image below shows the reference architecture for combining Postgres and ClickHouse using Postgres CDC, with Postgres handling low\-latency transactions and ClickHouse powering blazing\-fast analytics.


![catalogue_lakehouse.png](/uploads/Postgres_Click_House_reference_architecture_61fe52239a.png)
## Some metrics and reference customers [\#](/blog/postgres-cdc-connector-clickpipes-ga#some-metrics-and-reference-customers)


Over the past six months, the connector has gone through an extensive beta phase, evolving rapidly based on user feedback. It now supports **hundreds of mission\-critical workloads**, moving **100TB\+ of data per month** into ClickHouse.


A few reference customers include. [**Ashby**](https://www.ashbyhq.com/)—a top recruitment company in the US, [**Seemplicity**](https://seemplicity.io/) – one of the fastest\-growing cybersecurity startups, and [**AutoNation**](https://www.autonation.com/) – a well\-renowned automotive retailer in the US. Here are a few testimonials from our reference customers.



> “ClickHouse powers Ashby’s customer\-facing analytics, delivering lightning\-fast fully dynamic insights, while Postgres handles core transactions. With Postgres CDC via ClickPipes, we seamlessly replicated terabytes of data—speeding up our real\-time analytics without disrupting operations. Reports that once took minutes now finish within a second. Our enterprise customers' comprehensive recruiting dashboards, which are being filtered and shared in real\-time as they make decisions that impact their organization, are their source of truth. Complementing Postgres with ClickHouse enables us to give them a fully reliable experience and handle even larger data as we scale.” \- [Elenie Godzaridis](https://www.linkedin.com/in/elenie-godzaridis/), Director of Engineering, [Ashby](https://www.ashbyhq.com/)



> “We first tried to implement Postgres CDC in\-house using Debezium but it was way too complex. I knew a managed product built by engineers, whose goal in life is to transform bits from Postgres into ClickHouse, would be better than anything we could do ourselves.” \- [Tal Shargal](https://www.linkedin.com/in/tal-shargal-29388671/), Chief Architect at [Seemplicity](https://seemplicity.io/),  [*read the full customer story*](https://clickhouse.com/blog/seemplicity-scaled-real-time-security-analytics-with-postgres-cdc-and-clickhouse)



  

![Chart.png](/uploads/Chart_7c2a541127.png)
**This graph shows the growth we witnessed in Postgres CDC to ClickHouse usage over the past year,** [**reference**](https://www.linkedin.com/feed/update/urn:li:activity:7310749593296588800/)**.**


## Product Highlights [\#](/blog/postgres-cdc-connector-clickpipes-ga#product-highlights)



  

The Postgres CDC connector is purpose\-built for Postgres and ClickHouse and comes with a vast suite of features. Here are a few noteworthy ones:


1. **10x Faster Initial Loads and Resyncs** – Achieved through [parallel snapshotting](https://blog.peerdb.io/parallelized-initial-load-for-cdc-based-streaming-from-postgres), enabling parallel loading of single large tables. Terabytes of data can now be moved in hours instead of days.
2. **Replication Latencies as Low as 10 Seconds** – The replication slot is [continuously consumed without reconnections](https://clickhouse.com/blog/enhancing-postgres-to-clickhouse-replication-using-peerdb#efficiently-flush-the-replication-slot), and ClickHouse's [ReplacingMergeTree](https://clickhouse.com/blog/postgres-to-clickhouse-data-modeling-tips-v2) ensures minimal end\-to\-end latency.
3. **Automatic Replication of Schema Changes**– [Supports](https://clickhouse.com/docs/integrations/clickpipes/postgres/schema-changes) operations like ADD COLUMN and DROP COLUMN with zero manual intervention.
4. **Table and Column Exclusions** – Allows fine\-grained control for better security (e.g., handling PII) and optimized network throughput.
5. **Secure Connectivity** – Supports [**AWS PrivateLink**](https://clickhouse.com/docs/integrations/clickpipes/aws-privatelink) and [**SSH tunneling**](https://clickhouse.com/docs/integrations/clickpipes/postgres#optional-setting-up-ssh-tunneling) for private, secure connections to source Postgres databases.
6. **Support for Native Postgres Features** – Includes replication for [partitioned tables,](https://blog.peerdb.io/real-time-change-data-capture-for-postgres-partitioned-tables) TOAST columns, and [advanced data types](https://clickhouse.com/docs/integrations/clickpipes/postgres/faq#how-are-postgres-data-types-mapped-to-clickhouse) such as arrays and JSON.
7. **Open API (Beta)** – Enables [programmatic](https://clickhouse.com/docs/integrations/clickpipes/postgres/faq#can-clickpipe-creation-be-automated-or-done-via-api-or-cli) creation and management of pipes. Ideal for ISV applications deploying isolated ClickHouse Cloud \+ ClickPipes environments. [**Terraform**](https://registry.terraform.io/providers/ClickHouse/clickhouse/3.2.0-alpha1/docs/resources/clickpipe) **support coming soon** for easy infrastructure\-as\-code automation.


## Pricing [\#](/blog/postgres-cdc-connector-clickpipes-ga#pricing)


As part of the GA launch—and as [mentioned](https://clickhouse.com/blog/postgres-cdc-connector-clickpipes-public-beta#pricing) earlier during the beta—we’re introducing pricing for the Postgres CDC connector. Our goal is to keep it highly competitive while staying true to our core vision: making it seamless and affordable for customers to connect their Postgres databases to ClickHouse. The connector is **over 5x more cost\-effective** than external ETL tools and similar features in other database platforms. 


Note that pricing will start being metered in monthly bills **beginning September 1st, 2025 for all customers (existing and new) using Postgres CDC ClickPipes**. Customers will have a 3\-month window to optimize costs if needed, though we don’t anticipate most will need to make any changes. For detailed information on the pricing structure, examples, and FAQs, click [here](https://clickhouse.com/docs/cloud/manage/billing/overview#clickpipes-for-postgres-cdc).


## How to try Postgres CDC to ClickHouse [\#](/blog/postgres-cdc-connector-clickpipes-ga#how-to-try-postgres-cdc-to-clickhouse)


You can follow the links below to connect your Postgres databases to ClickHouse Cloud for blazing fast analytics.


- [Ingesting data from Postgres to ClickHouse (using CDC)](https://clickhouse.com/docs/en/integrations/clickpipes/postgres)
- [ClickPipes for Postgres FAQ](https://clickhouse.com/docs/en/integrations/clickpipes/postgres/faq)
- [Try ClickHouse Cloud for free](https://clickhouse.com/docs/en/cloud/get-started/cloud-quick-start)
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
