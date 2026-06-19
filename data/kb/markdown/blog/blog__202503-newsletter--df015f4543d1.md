# March 2025 Newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# March 2025 Newsletter

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Mar 20, 2025 · 8 minutes readWhile the weather in the Northern Hemisphere seems undecided about Spring, there's no confusion about it being time for the March ClickHouse newsletter.


This month, the Postgres CDC connector for ClickPipes went into Public Beta, and we announced general availability for Bring Your Own Cloud on AWS. We’ve got the latest on ClickHouse support for Apache Iceberg, how to build a ClickHouse\-based data warehouse for contact center analytics, visitor segmentation with Theta Sketches, and more!


## Featured community member: Matteo Pelati [\#](/blog/202503-newsletter#featured-community-member-matteo-pelati)


This month's featured community member is Matteo Pelati, Co\-Founder at [LangDB](https://langdb.ai/).


![0_march2025.png](/uploads/0_march2025_dea5945f2b.png)
Before founding LangDB, Matteo held senior leadership positions at Goldman Sachs as Global Head of Product Data Engineering and at DBS Bank as Executive Director of Data Platform Technology, where he led a team of over 130 engineers building bank\-wide data platforms.


LangDB is a full\-featured and managed AI gateway that provides instant access to 250\+ LLMs with enterprise\-ready features. It uses ClickHouse as its foundational data store, where all AI gateway data, traces, and analytics are stored. It also leverages ClickHouse's custom UDF functionality to enable direct AI model calls from SQL queries, seamlessly integrating structured data analytics and AI capabilities.


Mateo recently [presented on LangDB at the ClickHouse Singapore meetup](https://clickhouse.com/videos/singapore-meetup-langdb-building-intelligent-applications-with-clickhouse), where he demonstrated how organizations can leverage this integration to build sophisticated AI applications while maintaining complete control over their data infrastructure and analytics pipeline.


➡️ [Follow Mateo on LinkedIn](https://www.linkedin.com/in/matteopelati/)


## Upcoming events [\#](/blog/202503-newsletter#upcoming-events)


It’s just over two months until our biggest event of the year \- [Open House, The ClickHouse User Conference](https://clickhouse.com/openhouse?utm_source=marketo&utm_medium=email&utm_campaign=newsletter) in San Francisco on May 28\-29\.


Join us for a full day of technical deep dives, use case presentations from top ClickHouse users, founder updates, and conversations with fellow ClickHouse users. Whether you're new to ClickHouse or an experienced user, there's something for everyone.


➡️ [Register for Open House](https://clickhouse.com/openhouse?utm_source=marketo&utm_medium=email&utm_campaign=newsletter)


### Global events [\#](/blog/202503-newsletter#global-events)


- [v25\.3 Community Call](https://clickhouse.com/company/events/v25-3-community-release-call) \- Mar 20


### Free training [\#](/blog/202503-newsletter#free-training)


- [In\-Person ClickHouse Developer \- Sydney](https://clickhouse.com/company/events/202503-apj-sydney-inperson-clickhouse-developer) \- March 24\-25
- [Treinamento Presencial ClickHouse Developer \- São Paulo, Brasil](https://clickhouse.com/company/events/202503-latam-sao-paulo-inperson-clickhouse-developer), March 25\-26
- [In\-Person ClickHouse Developer \- Melbourne](https://clickhouse.com/company/events/202503-apj-melbourne-inperson-clickhouse-developer) \- March 27\-28
- [In\-Person ClickHouse Developer Fast Track \- Bangalore](https://clickhouse.com/company/events/202504-apj-bangalore-inperson-developer-fast-track) \- April 1
- [BigQuery to ClickHouse Workshop \- Virtual](https://clickhouse.com/company/events/202504-emea-clickhouse-bigquery-workshop) \- April 1
- [ClickHouse Developer In\-Person Training \- Vienna, Austria](https://clickhouse.com/company/events/202504-emea-vienna-inperson-clickhouse-developer) \- April 7\-8
- [Using ClickHouse for Observability \- Virtual](https://clickhouse.com/company/events/202504-apj-clickhouse-observability) \- April 15
- [ClickHouse Fundamentals \- Virtual](https://clickhouse.com/company/events/202504-emea-clickhouse-fundamentals) \- April 22


### Events in AMER [\#](/blog/202503-newsletter#events-in-amer)


- [ClickHouse Meetup @ Klaviyo](https://www.meetup.com/clickhouse-boston-user-group/events/305882607/?slug=clickhouse-boston-user-group&eventId=300907870&isFirstPublish=true), Boston \- March 25
- [ClickHouse Meetup in São Paulo](https://www.meetup.com/clickhouse-brasil-user-group/events/306385974/) \- March 25
- [ClickHouse Meetup @ Braze](https://www.meetup.com/clickhouse-new-york-user-group/events/305916369/?eventOrigin=group_upcoming_events), New York \- March 26
- [ClickHouse Launching Meetup in DC](https://www.meetup.com/clickhouse-dc-user-group/events/306439995/) \- March 27
- [Google Next](https://clickhouse.com/company/events/2025-04-google-next), Las Vegas \- April 9
- [Open House User Conference](https://clickhouse.com/openhouse?utm_source=marketo&utm_medium=email&utm_campaign=newsletter), San Francisco \- May 28\-29


### Events in EMEA [\#](/blog/202503-newsletter#events-in-emea)


- [ClickHouse Meetup in Zurich](https://www.meetup.com/clickhouse-switzerland-meetup-group/events/306435122/) \- March 24
- [ClickHouse Meetup in Budapest](https://www.meetup.com/clickhouse-hungary-user-group/events/306435234/) \- March 25
- [KubeCon 2025](https://clickhouse.com/company/events/04-2025-kubecon-london), London \- April 1\-4
- [ClickHouse Meetup in Oslo](https://clickhouse.com/company/events/202504-emea-oslo-meetup) \- April 8
- [AWS Summit 2025](https://clickhouse.com/company/events/04-2025-aws-paris), Paris \- April 9
- [AWS Summit 2025](https://clickhouse.com/company/events/2025-04-aws-summit-amsterdam), Amsterdam \- April 16
- [AWS Summit 2025](https://clickhouse.com/company/events/04-2025-aws-london), London \- April 30


### Events in APAC [\#](/blog/202503-newsletter#events-in-apac)


- [ClickHouse Delhi Meetup](https://www.meetup.com/clickhouse-delhi-user-group/events/306253492/), India \- Mar 22
- [ClickHouse Sydney Meetup](https://www.meetup.com/clickhouse-australia-user-group/events/306549810/) \- April 1
- [Latency Conference](https://latencyconf.io/), Australia \- Apr 3\-4
- [TEAMZ Web3/AI Summit](https://web3.teamz.co.jp/en), Japan \- Apr 16\-17


## 25\.2 release [\#](/blog/202503-newsletter#252-release)


![1_march2025.png](/uploads/1_march2025_efc9bd623e.png)
ClickHouse 25\.2 delivers more performance gains for joins. The parallel hash join system has been further optimized to ensure 100% CPU core utilization. Tom Schreiber explains how this was achieved.


The release also introduces Parquet Bloom filters, a new backup database engine, integration with the Delta Rust Kernel, enhanced HTTP streaming capabilities for real\-time data consumption, and more!


➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-25-02)


## Postgres CDC connector for ClickPipes is now in Public Beta [\#](/blog/202503-newsletter#postgres-cdc-connector-for-clickpipes-is-now-in-public-beta)


![2_march2025.png](/uploads/2_march2025_5d2086949f.png)
The Postgres CDC connector for ClickPipes is now in public beta, enabling seamless replication of PostgreSQL databases to ClickHouse Cloud with just a few clicks.


The connector features high\-performance capabilities, including parallel snapshotting for 10x faster initial loads and near real\-time data freshness.


Successful implementations are already running at organizations like Syntage and Neon, handling terabyte\-scale migrations. During the public beta period, this powerful integration tool is available free of charge to all users.


➡️ [Read the blog post](https://clickhouse.com/blog/postgres-cdc-connector-clickpipes-public-beta)


## ClickHouse \& Grafana for High Cardinality Metrics [\#](/blog/202503-newsletter#clickhouse--grafana-for-high-cardinality-metrics)


Tomer Ben David explores how ClickHouse and Grafana can effectively handle high cardinality metrics \- a common challenge when tracking data across numerous unique dimensions like individual user sessions, container IDs, or geographical locations.


The article details how ClickHouse's columnar storage, vectorized query execution, and efficient compression capabilities make it ideal for processing large volumes of granular data. Grafana provides powerful visualization, templating features, and alerting to make this data actionable.


Tomer also offers practical strategies for managing high cardinality, including data aggregation techniques, dimensionality reduction, and pre\-aggregation at the source.


➡️ [Read the blog post](https://medium.com/@Tom1212121/clickhouse-grafana-for-high-cardinality-metrics-4fc3708ba617)


## Climbing the Iceberg with ClickHouse [\#](/blog/202503-newsletter#climbing-the-iceberg-with-clickhouse)


![3_march2025.png](/uploads/3_march2025_9f42276fd5.png)
Melvyn Peignon explores ClickHouse's evolving role in the data lake and lakehouse ecosystem, highlighting three key integration patterns: data loading from data lakes, ad\-hoc querying, and frequent querying of lake data.


He also outlines ClickHouse's 2025 roadmap for lakehouse integration, focusing on three main areas: enhancing user experience for data lake queries through expanded catalog integrations, improving capabilities for working with data lakes, including write support for Iceberg and Delta formats, and developing an Iceberg CDC Connector in ClickPipes.


➡️ [Read the blog post](https://clickhouse.com/blog/climbing-the-iceberg-with-clickhouse)


## How Cresta Scales Real\-Time Insights with ClickHouse [\#](/blog/202503-newsletter#how-cresta-scales-real-time-insights-with-clickhouse)


![4_march2025.png](/uploads/4_march2025_1bf99b75a7.png)
Xiaoyi Ge, Daniel Hoske, and Florin Szilagyi wrote a blog post describing Cresta’s implementation of ClickHouse as its primary data warehouse solution for processing contact center analytics. After migrating from PostgreSQL, it achieved a 50% reduction in storage costs while handling tens of millions of daily records across three dedicated clusters for real\-time aggregation, raw event storage, and observability.


The platform now powers Cresta's Director UI, enabling enterprise customers to query billions of records with flexible time ranges while maintaining responsive performance for real\-time contact center insights.


They also shared key optimization strategies, including careful schema design to align with query patterns, leveraging materialized views for frequent queries, and utilizing ClickHouse's sparse indexes and bloom filters to accelerate specific queries.


➡️ [Read the blog post](https://cresta.com/blog/how-cresta-scales-real-time-insights-with-clickhouse/)


## Announcing General Availability of ClickHouse BYOC (Bring Your Own Cloud) on AWS [\#](/blog/202503-newsletter#announcing-general-availability-of-clickhouse-byoc-bring-your-own-cloud-on-aws)


![5_march2025.png](/uploads/5_march2025_cd7c95fba4.png)
BYOC (Bring Your Own Cloud) on AWS is generally available, allowing enterprises to run ClickHouse Cloud while keeping all their data within their own AWS VPC environment.


This deployment model, part of a five\-year strategic collaboration with AWS, enables organizations to maintain complete data control and security compliance while benefiting from ClickHouse's managed service capabilities.


➡️ [Read the blog post](https://clickhouse.com/blog/announcing-general-availability-of-clickhouse-bring-your-own-cloud-on-aws)


## Postgres to ClickHouse: Data Modeling Tips V2 [\#](/blog/202503-newsletter#postgres-to-clickhouse-data-modeling-tips-v2)


![6_march2025.png](/uploads/6_march2025_461dacaee6.png)
Lionel Palacin and Sai Srirampur provide a comprehensive guide on migrating data from PostgreSQL to ClickHouse using Change Data Capture (CDC). The article explains how ClickPipes and PeerDB enable continuous tracking of inserts, updates, and deletes in Postgres, replicating them to ClickHouse for real\-time analytics while maintaining data consistency through ClickHouse's ReplacingMergeTree engine.


The authors detail several strategies for optimizing performance, including deduplication approaches using the FINAL keyword, views, and materialized views. They also explore advanced topics like custom ordering keys, JOIN optimizations, and denormalization techniques using refreshable and incremental materialized views.


➡️ [Read the blog post](https://clickhouse.com/blog/postgres-to-clickhouse-data-modeling-tips-v2)


## Quick reads [\#](/blog/202503-newsletter#quick-reads)


- Coroot has [added support for the ClickHouse native and ZooKeeper protocols](https://coroot.com/blog/engineering/coroot-v1-7-monitoring-clickhouse-and-zookeeper-with-ebpf/), making it much easier to observe these distributed systems.
- Keshav Agrawal demonstrates [how to build a scalable real\-time data pipeline](https://www.akitmcs.com/post/building-a-real-time-data-pipeline-with-go-kafka-clickhouse-and-apache-superset) combining Go for data generation, Kafka for message queuing, ClickHouse for high\-performance storage, and Apache Superset for visualization, providing a complete solution for processing both streaming and batch data.
- After finding Grafana's Loki inadequate for web log analysis, Scott Laird documents [his migration to ClickHouse](https://scottstuff.net/posts/2025/02/27/caddy-logs-in-clickhouse-via-vector/). His guide provides step\-by\-step instructions for setting up ClickHouse with proper authentication, creating an appropriate schema for Caddy's JSON logs, and configuring Vector as the data pipeline middleware to transform and stream logs into ClickHouse.
- [A tutorial by sateesh.py](https://sateeshpy.medium.com/building-a-scalable-etl-pipeline-data-warehouse-with-apache-spark-minio-and-clickhouse-0154342872e9) demonstrates how to build a modern ETL pipeline combining Apache Spark for data processing, MinIO for S3\-compatible storage, Delta Lake for data storage, and ClickHouse for fast analytical querying, complete with code examples.
- Hellmar Becker demonstrates [how to use ClickHouse's theta sketches for visitor segmentation and set operations](https://blog.hellmar-becker.de/2025/03/09/clickhouse-data-cookbook-visitor-segmentation-with-theta-sketches/%20), efficiently counting unique visitors across different content segments while also performing more complex operations like intersections and unions.


## Post of the month [\#](/blog/202503-newsletter#post-of-the-month)


My favorite post this month was by [Chris Elgee](https://x.com/chriselgee), who likes ClickHouse’s compression functionality.


![7_march2025.png](/uploads/7_march2025_5110d40afa.png)
➡️ [Read the post](https://x.com/chriselgee/status/1894760925527245261)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
