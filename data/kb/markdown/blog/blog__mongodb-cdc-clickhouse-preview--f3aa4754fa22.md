# MongoDB CDC to ClickHouse with Native JSON Support, now in Private Preview


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# MongoDB CDC to ClickHouse with Native JSON Support, now in Private Preview

![](/_next/image?url=%2Fuploads%2Fjoy_gao_5ca85f14b3.png&w=96&q=75)Joy GaoAug 11, 2025 · 5 minutes readToday, we're excited to announce the private preview of the [MongoDB Change Data Capture (CDC) connector](https://clickhouse.com/cloud/clickpipes/mongodb-cdc-connector) in ClickPipes! This enables customers to replicate their MongoDB collections to ClickHouse Cloud in just a few clicks and leverage ClickHouse for blazing\-fast analytics on document\-based data. You can use this connector for both continuous replication and one\-time loads from MongoDB, whether it's running on MongoDB Atlas or self\-hosted instances.


The experience is natively integrated into ClickHouse Cloud through [ClickPipes](https://clickhouse.com/cloud/clickpipes), the built\-in ingestion service of ClickHouse Cloud. This eliminates the need for external ETL tools, which are often expensive and time consuming to configure and manage. This connector is powered by [PeerDB](https://github.com/PeerDB-io/peerdb), maintaining our commitment to open source with no vendor lock\-in.



> You can sign up to the private preview by following [this link.](https://clickhouse.com/cloud/clickpipes/mongodb-cdc-connector)


Following the rollout of our [Postgres](https://clickhouse.com/cloud/clickpipes/postgres-cdc-connector) and [MySQL](https://clickhouse.com/cloud/clickpipes/mysql-cdc-connector) CDC connectors, we've received high demand from customers for MongoDB CDC. The rise of modern applications built on MongoDB's flexible document model, combined with the need for real\-time analytics on JSON\-rich data, made this integration a natural next step in our ClickPipes roadmap.



## Purpose\-built for MongoDB's Document Model and ClickHouse Analytics [\#](/blog/mongodb-cdc-clickhouse-preview#purpose-built-for-mongodbs-document-model-and-clickhouse-analytics)


MongoDB's document\-oriented architecture generates rich, nested JSON data that traditional ETL tools may struggle to handle efficiently. Our MongoDB CDC connector is specifically designed to bridge the gap between MongoDB's flexible schema and ClickHouse's powerful columnar analytics engine.


The connector excels at handling MongoDB's native JSON capabilities, automatically mapping complex nested documents, arrays, and embedded objects into ClickHouse's [native JSON data type](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse), which recently went GA, while maintaining query performance and analytical flexibility.


## Key Features [\#](/blog/mongodb-cdc-clickhouse-preview#key-features)


The MongoDB CDC connector delivers enterprise\-grade performance with features designed to handle the unique needs of document\-based data replication:


**Unmatched Query Performance**: MongoDB excels at operational and transactional workloads with high throughput and low\-latency, and ClickHouse excels at analytical workloads of any scale, delivering real\-time, blazing\-fast query performance. 


**Advanced JSON Data Type Support**: Seamlessly replicate MongoDB's rich document structures using ClickHouse's powerful native JSON data types to keep your operational and analytical systems in sync with low latency and high precision. The connector preserves document structure and enables high\-performance analytical queries on semi\-structured data, while optimizing compression and reducing storage cost.


**Blazing Fast Initial Load (Backfills)**: Replicate terabytes of existing data across multiple MongoDB collections to ClickHouse within a few hours. You can configure the number of parallel threads to migrate multiple tables simultaneously. Soon, we plan to support intra\-table parallelism, using multiple threads to replicate  a single large table.


**Real\-Time Change Streams for low\-latency replication**: Leverages MongoDB's native [Change Streams](https://www.mongodb.com/docs/manual/changestreams/) feature to capture all document changes with latencies as low as a few seconds, ensuring your analytical data stays synchronized with your operational MongoDB database in near real\-time.


**Built\-in Monitoring and Alerting**: Full observability into replication health with metrics for document throughput, replication lag, failed operations, and Change Stream status, all integrated into ClickHouse Cloud's monitoring dashboard.


**No Vendor Lock\-in**: The MongoDB CDC connector is powered by PeerDB, which is fully [open source](https://github.com/PeerDB-io/peerdb/). With the exception of the UI, all components are directly extended from the PeerDB open\-source project, ensuring no vendor lock\-in for our customers.


## MongoDB \+ ClickHouse: The Document Data Stack [\#](/blog/mongodb-cdc-clickhouse-preview#mongodb--clickhouse-the-document-data-stack)


The combination of MongoDB and ClickHouse creates a powerful architecture for modern applications that need both operational flexibility and analytical performance. MongoDB is ideal for the transactional workloads required by modern web and AI applications, while ClickHouse delivers unmatched analytics performance for the same applications, with data stored and queried in native, document\-based JSON models.


![mongo-cdc-diagram-2.png](/uploads/mongo_cdc_diagram_2_f6e8d30ba1.png)
This integration enables several key advantages:


**Operational and Analytical Workload Separation**: Keep your MongoDB clusters focused on serving mission\-critical operational workloads, including high\-throughput CRUD operations and efficient document lookups, while ClickHouse handles complex analytical queries, reports, and business intelligence workloads without impacting operational performance.


**Native JSON Analytics**: Query nested JSON documents using ClickHouse's advanced JSON functions and operators, enabling sophisticated, high\-performance analytics on semi\-structured data.


## How to sign up for Private Preview? [\#](/blog/mongodb-cdc-clickhouse-preview#how-to-sign-up-for-private-preview)


You can sign up for the Private Preview by filling out [the form on this page](https://clickhouse.com/cloud/clickpipes/mongodb-cdc-connector). Our team will reach out to you within a few days and work closely with you to provide early access. Given the anticipated demand, there may be a slight delay, but we'll ensure we connect with you as soon as possible.


The Private Preview entails no cost and is fully free. This is a great opportunity for you to get firsthand experience with the native MongoDB integration in ClickHouse Cloud and directly influence the roadmap. Looking forward to having you onboard!

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
