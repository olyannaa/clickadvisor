# ClickPipes for Amazon Kinesis


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickPipes for Amazon Kinesis

![](/_next/image?url=%2Fuploads%2FRyadh_d50dc0546c.png&w=96&q=75)[Ryadh Dahimene](/authors/ryadh-dahimene)May 13, 2024 · 4 minutes read[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-header&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. To learn more about our volume\-based discounts, [contact us](/company/contact?loc=blog-cta-header) or visit our [pricing page](/pricing?loc=blog-cta-header).

Welcome to [launch week](https://clickhouse.com/launch-week/may-2024)! We're going to be announcing a new feature of ClickHouse Cloud every day this week. So let's get to it.


First up, we’re excited to announce the beta release of our Amazon Kinesis connector for ClickPipes.
As one of our most requested integrations, it offers a hassle\-free way to ingest data from Kinesis Data Streams into a ClickHouse Cloud service.


![select-data-source.png](/uploads/select_data_source_fa04ed344a.png)
We've also made a short video showing how this all works, which you can view below.



## The “Need for Stream” [\#](/blog/clickpipes-amazon-kinesis#the-need-for-stream)


The Amazon Web Services (AWS) cloud ecosystem offers powerful building blocks for setting up sophisticated data architectures and pipelines. Data can take various forms and come from different mediums, from object storage to databases and streaming systems. At ClickHouse, ClickPipes represents our commitment to meeting our users where they are. By offering managed data ingestion capabilities, we free up users to focus on their analytics use cases instead of building and maintaining complex data pipelines.


For example, we recently announced the batch data loading connector for Amazon S3, which allows users to reliably load large data batches and historical uploads. Today, with the Amazon Kinesis connector for ClickPipes, AWS users can complete the picture with near real\-time data streaming capabilities, unlocking event\-based use cases and pipelines while keeping their architectural footprint minimal.


![kinesis.gif](/uploads/kinesis_dd7e924579.gif)
## Lambda, Kappa architectures? Fewer Greek letters, more insights [\#](/blog/clickpipes-amazon-kinesis#lambda-kappa-architectures-fewer-greek-letters-more-insights)


The Lambda Architecture combines batch and stream processing for historical and real\-time data, while Kappa Architecture simplifies this by relying only on stream processing, eliminating batch processing layers ([source](https://www.kai-waehner.de/blog/2021/09/23/real-time-kappa-architecture-mainstream-replacing-batch-lambda/)). Whether handling streaming or batch data, this architecture is greatly simplified in ClickHouse Cloud, with ClickPipes providing seamless ingestion into an efficient storage engine with rich query execution capabilities. Treat your static buckets or real\-time streams as data sources that will automatically be kept in sync by ClickPipes, allowing you to focus on deriving insights from the data. This represents an additional step towards enabling the [real\-time data warehouse](https://clickhouse.com/blog/the-unbundling-of-the-cloud-data-warehouse) use case, unifying data at the warehouse level.


![rtdwh.png](/uploads/rtdwh_39cce2d0ca.png)
## Under the hood: A focus on reliability [\#](/blog/clickpipes-amazon-kinesis#under-the-hood-a-focus-on-reliability)


ClickPipes for Kinesis leverages our existing streaming ingestion infrastructure for Apache Kafka to ingest Kinesis Data Streams. Our Kinesis consumer implementation differs from Kafka in two main ways: Checkpointing is done on the consumer side for Kinesis. To support this we write reading checkpoints (called SequenceNumbers) to the customer’s ClickHouse DB instances leveraging the ClickHouse key\-value store [KeeperMap](https://clickhouse.com/docs/en/engines/table-engines/special/keeper-map). Additionally, to read Kinesis streams, ClickPipes reads concurrently through multiple shards provided by the Kinesis stream. Shards have fixed throughput and hard limits, so Kinesis scales itself by adding and removing shards. We consistently check the number of shards and read each shard as it scales.


![clickpipes-kinesis-arch.png](/uploads/clickpipes_kinesis_arch_d9a3dd424e.png)
## An ever\-growing ecosystem of managed connectors [\#](/blog/clickpipes-amazon-kinesis#an-ever-growing-ecosystem-of-managed-connectors)


It has been a busy quarter for the ClickPipes team. After adding Avro support for our set of Kafka connectors, the release of the batch data loading connector for Amazon S3 and Google Cloud Storage (GCS), and now the Amazon Kinesis support, the ClickPipes ecosystem continues its expansion both in\-depth and breadth. Coming next in our roadmap:


- PostgreSQL Change Data Capture (CDC) connector for ClickPipes
- Continuous mode for the batch data loading connector for Amazon S3 and Google Cloud Storage (allows monitoring a remote bucket and ingesting newly added files)
- Offset control for the ClickPipes Kafka Connector
- ClickPipes duplication (allowing the creation of new ClickPipes from an existing configuration)
- ClickPipes public API
- Improved observability and notification


This is far from a representative list of what the next quarters will bring. As always, we encourage you to share your use cases and requirements to help shape our roadmap. Please feel free to reach out to us!

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
