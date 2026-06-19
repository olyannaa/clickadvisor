# How Nava helped ELO cut infrastructure costs by 87% by migrating from Elasticsearch to ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Nava helped ELO cut infrastructure costs by 87% by migrating from Elasticsearch to ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Apr 20, 2026 · 10 minutes read## Summary

Nava used ClickHouse to build a real\-time payments monitoring platform for ELO, one of Brazil's largest card networks, processing 22 million transactions per day. Migrating from Elasticsearch to ClickHouse reduced storage from 12 TB to 2 TB and cut annual infrastructure costs by 87% from R$900,000 to R$120,000\. ClickHouse delivers 5x faster aggregations and sub\-2\-second end\-to\-end latency, powering 300 real\-time dashboards refreshing every five seconds.

[Nava](https://nava.com.br/) was founded in Brazil in 1995 to help large organizations build and manage data center infrastructure. But infrastructure without visibility is only half the picture, and it wasn't long before the company developed its own monitoring and observability products to complement the environments it was building.


The pivot into financial services came in 2012, when Itaú, one of Brazil's largest banking groups, approached Nava to ask for help monitoring the flow of payments through their network. As data engineer and architect Lucas Souza recalls, "With our expertise in observability and monitoring, combined with their domain knowledge, we took on this challenge and decided to create something new—real\-time business monitoring for the payments industry."


It was a turning point. Word spread quickly through Brazil's financial sector, and other players in the payments and credit space came looking for the same capabilities. Today, Nava monitors transactions across more than a dozen companies in the payments space, accounting for around 90% of all card transactions in Brazil.


At a [November 2025 ClickHouse meetup in São Paulo](https://clickhouse.com/videos/nava-elasticsearch-migration), Lucas told the story of how Nava helped one of those companies—[ELO](https://www.elo.com.br/), a major Brazilian card network—migrate its analytics infrastructure from Elasticsearch to ClickHouse, cutting costs by 87% and transforming how it monitors 22 million daily transactions.


## How Lucas discovered ClickHouse [\#](/blog/nava#how-lucas-discovered-clickhouse)


Lucas's personal ClickHouse journey began nearly a decade before it made its way to ELO. As a Microsoft SQL Server specialist who spent years speaking at conferences in Brazil and abroad, he used SQL Server as his benchmark for everything.


But around 2014 to 2016, Nava was handling ingestion volumes that pushed relational databases to their limits. "Anyone who works with relational databases knows that if you're ingesting 8,000 or 10,000 records per second, you'll have data page contention," Lucas says.


In\-memory solutions helped, but their licensing costs made them impractical to offer competitively to smaller clients. "I needed to find a solution that would meet my niche's needs, that wouldn't compromise performance, that would be as efficient as SQL Server, and that would have low or zero risk," Lucas says.


He evaluated RocksDB, MariaDB, and several other databases before a contact at Percona pointed him toward ClickHouse. It made a strong impression. "ClickHouse is on a different level," he says. "The first time you have contact with it, its performance is absurd."


Coming from a SQL Server background, Lucas had the technical depth to stress\-test what he was seeing. ClickHouse held up on every count—compression ratios, query speed, SQL support. He said to himself, "I've found the solution to my problems."


## The limits of Elasticsearch [\#](/blog/nava#the-limits-of-elasticsearch)


For the next several years, Lucas and the Nava team built out their ClickHouse expertise internally, waiting for the right opportunity to deploy it into production.


That opportunity arrived in the form of ELO, one of Brazil's leading payment networks. The company processes around 22 million financial transactions every day—over 260 per second—accumulating more than 8 billion transaction records each year.


At the time, Nava was providing ELO visibility into those transactions through a platform built on Elasticsearch, hosted on Google Cloud Platform. But as transaction volumes grew and ELO demanded more from their dashboards, the limitations became harder to ignore.


"The main issue was cost," Lucas says, "both in terms of storage requirements and infrastructure expenses." The Elasticsearch setup required 12 TB of storage and was running up an annual infrastructure bill of R$900,000\.


Performance was unreliable, too. Complex aggregations over large date ranges would routinely slow to a crawl, and the team found themselves re\-indexing the cluster multiple times a week just to keep pace with demand.


Finally, there was the complexity of the EQL syntax. "Elasticsearch's query language is not user\-friendly," Lucas says. "It's a verbose language, a tedious language." Every new dashboard required specialist knowledge; this created a bottleneck as ELO's operations teams waited on developers every time they needed a new view of their data.


## Migrating to ClickHouse [\#](/blog/nava#migrating-to-clickhouse)


While years of internal testing had built confidence in ClickHouse, Nava had never deployed it in production. Lucas knew that proposing it as the foundation for ELO's monitoring infrastructure was a big step. He made the call anyway.


"We have to take risks all the time," he says. "If you don't take risks and trust in what you do, you'll never get out of your comfort zone, you'll never get anywhere."


The migration preserved the core of ELO's existing data pipeline. Transaction data continues to flow into Kafka, where Nava's custom ETL tool, Dataflow, enriches it against data dictionaries and business rules before loading it into ClickHouse for querying and visualization. What changed was everything downstream of that ingestion layer.


The ClickHouse cluster was deployed on Kubernetes using the Altinity operator, giving Nava fine\-grained control over configuration and enabling zero\-downtime updates. The cluster runs across four nodes (two shards and two replicas) distributed across ELO's two primary data centers in São Paulo and Rio de Janeiro. Using ClickHouse's [distributed table engine](https://clickhouse.com/docs/engines/table-engines/special/distributed), transactions are routed to the appropriate shard based on site ID, balancing the ingestion load across both locations and doubling the read capacity available for dashboard queries.


Several optimizations were layered on top. [ZSTD and LZ4 compression codecs](https://clickhouse.com/docs/data-compression/compression-in-clickhouse) dramatically reduced storage requirements. [LowCardinality](https://clickhouse.com/docs/sql-reference/data-types/lowcardinality) data types were applied across string columns with fewer than 10,000 distinct values, improving both compression and query speed. [Materialized views](https://clickhouse.com/docs/materialized-views) pre\-aggregate common query patterns, and [projections](https://clickhouse.com/docs/data-modeling/projections)—essentially pre\-computed execution plans—were added for the date\-range comparison queries that had previously caused performance problems in Elasticsearch.


Perhaps the most immediately felt change for ELO's teams was the shift to standard SQL. Where EQL had required specialist knowledge and slowed dashboard development, ClickHouse's [ANSI SQL support](https://clickhouse.com/docs/sql-reference) meant that analysts at any level could query the data and build visualizations without a steep learning curve.


## Cheaper, faster, and easier to use [\#](/blog/nava#cheaper-faster-and-easier-to-use)


The difference pre\- and post\-migration is like night and day. Storage dropped from 12 TB to 2 TB, and ELO's annual infrastructure bill fell from R$900,000 to R$120,000, an 87% reduction. As Lucas puts it, "The smaller the data, the faster it can be transmitted, the faster the access, the greater the amount of data I bring into memory, and the less infrastructure is used."


ClickHouse's query performance tells a similar story. Aggregations that took seconds in Elasticsearch now complete in milliseconds—5x faster on full dataset aggregations, 6x faster on filtered queries, and 9x faster on pre\-aggregated data. "The performance is undeniably superior to any other database we evaluated," Lucas says.


ELO now runs approximately 300 operational dashboards around the clock, each refreshing every five seconds. "It takes two seconds from the moment data arrives in Kafka until the moment that data is displayed in my visualization," Lucas says.


The business case for that speed becomes clear when you consider what delayed visibility actually costs. If a payments link goes down in a specific region and ELO's preferred network stops processing, merchants automatically fail over to a secondary network at a higher fee rate. Without real\-time monitoring, that situation might go undetected for days—long enough to affect settlement costs and merchant relationships. With ClickHouse\-powered dashboards, ELO's operations team can identify a drop in transaction volume at a specific site within seconds and escalate before merchants or cardholders even notice a problem.


ELO has become one of Nava's most vocal advocates as a result. "Today, ELO is practically rolling out the red carpet for us because of the cost they've saved by moving away from Elasticsearch," Lucas says. "At the events they attend, they speak highly of ClickHouse. Why? Because they reduced costs, their application increased in performance, and the ease of creating dashboards is absurdly more productive because of the query language."


## Monitoring financial services across Brazil [\#](/blog/nava#monitoring-financial-services-across-brazil)


Since the ELO migration, Nava has applied ClickHouse across a growing roster of financial services clients, with each adding to the team's depth of experience with the platform.


One of the most demanding recent projects was a migration that involved moving nearly 20 billion records out of MongoDB and into ClickHouse. "Mongo wouldn't stay online because of the sheer amount of document data it had," Lucas explains. "Without needing to do a full replacement, by simply consolidating this data, aggregating it, and using the latest date, the performance was already 10 to 15 times higher."


Nava is also beginning to explore [ClickHouse Cloud](https://clickhouse.com/cloud) for clients who want the performance benefits of the platform without the operational overhead of managing their own cluster. One client, currently running a large Snowflake environment, is evaluating a migration of their analytical workloads to ClickHouse Cloud. As Lucas puts it, "Snowflake is a great product, but the cost of maintaining this data is very high compared to ClickHouse."


For Lucas, five years of production experience with ClickHouse has only deepened his confidence in the platform. "Every single feature we've tested has always been useful in some scenario," he says. What started as a calculated risk on an unfamiliar database has become Nava's go\-to solution for high\-volume analytical workloads, and the foundation of a monitoring capability that now touches nearly every card transaction in Brazil.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-429-get-started-today-sign-up&utm_blogctaid=429)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
