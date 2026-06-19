# MongoDB CDC connector for ClickPipes is now in Public Beta


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# MongoDB CDC connector for ClickPipes is now in Public Beta

![](/_next/image?url=%2Fuploads%2FMarta_Paes_Moreira_no_background_9853166ee2.png&w=96&q=75)[Marta Paes](/authors/marta-paes)Jan 13, 2026 · 6 minutes read## Summary

Replicate data from MongoDB into ClickHouse Cloud in just a few clicks for blazing\-fast analytics on document\-based data. Now with more connectivity options, improved reliability, and support for DocumentDB.

The [ClickPipes MongoDB CDC connector](https://clickhouse.com/cloud/clickpipes) is now in Public Beta! 🚀 


After working with dozens of early access customers during Private Preview, we've added support for **sharded clusters** and **Amazon DocumentDB**, improved **reliability** for production workloads, and made it easier to **securely connect** to private MongoDB deployments.


Whether you're running a one\-time migration or continuously replicating operational data for analytics, the connector delivers up to **100x faster queries** without the overhead of managing custom pipelines.



> [Sign up for ClickHouse Cloud](https://console.clickhouse.cloud/signup) today to try out the [MongoDB CDC connector for ClickPipes](https://clickhouse.com/cloud/clickpipes)!



Here’s what our customers are saying:



> Before using ClickPipes, we relied on multiple tools to replicate MongoDB data into ClickHouse, many of which required constant maintenance or manual intervention. After switching to the MongoDB connector in ClickPipes, those issues disappeared: the initial setup was simple, and once configured, it required no ongoing attention. Using materialized views makes data modeling flexible and easy to evolve.
> 
> 
>   
> 
> Overall, ClickPipes has significantly reduced operational overhead and has worked great to replicate several terabytes of business data a day for analytical workloads. \- [Rapidata](https://www.rapidata.ai)


## What’s new in Public Beta? [\#](/blog/mongodb-cdc-connector-clickpipes-beta#whats-new-in-public-beta)


### Broader platform compatibility [\#](/blog/mongodb-cdc-connector-clickpipes-beta#broader-platform-compatibility)


The MongoDB CDC connector initially launched with support for single [replica sets](https://www.mongodb.com/docs/manual/core/replica-set-members/). We’ve now extended support to [**sharded clusters**](https://www.mongodb.com/docs/manual/core/sharded-cluster-components/), enabling replication from common MongoDB topologies at any scale — whether you're running a single replica set or a distributed deployment with data spread across multiple shards.


We've also added compatibility with **Amazon DocumentDB**, a managed document database service that is API\-compatible with MongoDB. See our [new integration guide](https://clickhouse.com/docs/integrations/clickpipes/mongodb/source/documentdb) for step\-by\-step instructions on how to configure DocumentDB for change stream replication.


### Secure connectivity options [\#](/blog/mongodb-cdc-connector-clickpipes-beta#secure-connectivity-options)


To allow secure connections to MongoDB instances in private networks, which is a table stakes requirement for production environments, you can now configure both **AWS PrivateLink** and **SSH tunneling** when creating a new MongoDB ClickPipe. We've also added support for [X.509 certificate authentication](https://www.mongodb.com/docs/manual/core/security-x.509/), enabling **mutual TLS authentication** between the connector and your MongoDB deployment.


### Production\-readiness [\#](/blog/mongodb-cdc-connector-clickpipes-beta#production-readiness)


We've made significant improvements to reliability and observability based on Private Preview feedback. The connector now handles **data type edge cases** more gracefully (*e.g.* very large floats, dates outside the standard range) and uses enhanced error classification to **automatically retry transient failures** that would previously trigger unnecessary alerts.


We've also refined the initial snapshot phase with smarter batching logic that measures uncompressed data size to **prevent out\-of\-memory issues**. This addresses the most significant operational issue we identified with large\-scale deployments during early access: MongoDB's high JSON compression ratios caused batch sizes to balloon unexpectedly when decompressed during ingestion of very large collections. 💥


## Main features [\#](/blog/mongodb-cdc-connector-clickpipes-beta#main-features)


In addition to these Public Beta improvements, the MongoDB CDC connector provides several core capabilities designed to make real\-time replication from MongoDB to ClickHouse Cloud reliable and performant:


### Real\-time replication [\#](/blog/mongodb-cdc-connector-clickpipes-beta#real-time-replication)


The connector leverages MongoDB's native [Change Streams](https://www.mongodb.com/docs/manual/changestreams/) interface to capture all document changes with low latency, ensuring near real\-time synchronization between MongoDB and ClickHouse Cloud. This combination creates a powerful architecture for modern applications that need both operational flexibility and analytical performance, with up to 100x faster analytics — we’re calling it the *Document Data Stack*.


![image1.png](/uploads/image1_cba4cd460a.png)
Keep your MongoDB clusters focused on serving mission\-critical operational workloads, including high\-throughput CRUD operations and efficient document lookups, while ClickHouse Cloud handles complex analytical queries, reports, and business intelligence workloads without impacting upstream performance.


### Advanced JSON Support [\#](/blog/mongodb-cdc-connector-clickpipes-beta#advanced-json-support)


To preserve MongoDB’s rich document structures and provide high\-precision replication, the connector uses ClickHouse's powerful [native JSON data type](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse). This enables **high\-performance** analytical queries on semi\-structured data, at the same time o**ptimizing compression and reducing storage cost**.


### Fully managed experience [\#](/blog/mongodb-cdc-connector-clickpipes-beta#fully-managed-experience)


The connector is fully integrated into the ClickHouse Cloud experience. It provides **built\-in metrics and monitoring** for visibility into replication health, **detailed logs** for error diagnosis and debugging, **in\-place pipe editing**, and more.


## What’s next? [\#](/blog/mongodb-cdc-connector-clickpipes-beta#whats-next)


As we work towards General Availability (GA), we're focused on making the connector faster and more flexible for production workloads.


- **Parallel snapshot ingestion:** as is, the connector snapshots collections using a single thread, which can lead to a very long initial snapshotting phase. We’re evaluating (logical) partitioning strategies to improve initial load times for large collections.
- **Flattened mode:** we’ll add an option to automatically map top\-level document fields to target columns. This will make it easier to model and query replicated data, while preserving schema evolution capabilities.
- **OpenAPI and Terraform support:** for teams managing infrastructure as code, MongoDB ClickPipes will also be available via Open API and Terraform, similar to other ClickPipe types.


**A note on billing:** usage of MongoDB CDC ClickPipes continues to be **free** until GA. Customers will be notified ahead of the GA launch to review and optimize their ClickPipes usage. You can estimate future costs by referring to [billing for Postgres CDC ClickPipes](https://clickhouse.com/docs/cloud/reference/billing/clickpipes).


## Getting started with the MongoDB CDC connector [\#](/blog/mongodb-cdc-connector-clickpipes-beta#getting-started-with-the-mongodb-cdc-connector)


The MongoDB CDC connector is available to new and existing ClickHouse Cloud customers, in all service tiers. To get started, navigate to the *Data Sources* tab in the ClickHouse Cloud console, configure the connection details for your MongoDB database, and you’re good to go! For step\-by\-step instructions, frequently asked questions, and gotchas, check out the [documentation for MongoDB ClickPipes](https://clickhouse.com/docs/integrations/clickpipes/mongodb).

### Try the MongoDB CDC connector today

Ready to accelerate analytics on MongoDB data? Try the MongoDB CDC connector today and experience a fully managed, native integration experience with ClickHouse Cloud \- the world’s fastest analytics database.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-36-try-the-mongodb-cdc-connector-today-sign-up&utm_blogctaid=36)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
