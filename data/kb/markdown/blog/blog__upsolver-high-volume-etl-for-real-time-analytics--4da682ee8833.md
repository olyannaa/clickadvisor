# Upsolver: High Volume ETL for Real\-Time Analytics with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Upsolver: High Volume ETL for Real\-Time Analytics with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fupsolver_logo_f319ac4af6.png&w=96&q=75)UpsolverApr 30, 2024 · 12 minutes read
> We're excited to welcome Upsolver as a guest on our blog today. In the data world, where ClickHouse often deals with billions of rows per second for inserts, finding an ETL tool that can handle this efficiently and affordably is always noteworthy. That's why we were so excited when Upsolver shared their approach to integrating with ClickHouse. They've managed to demonstrate ETL row throughputs that are hugely impressive, while still delivering rich transformation capabilities, and importantly, at a cost that makes sense. Let's take a closer look at their work and what it means for data processing with ClickHouse.


[Upsolver](https://upsolver.com), the easy button for high\-scale data ingestion and transformation, is excited to announce support for [ClickHouse Cloud](https://clickhouse.com) as a destination. The new integration allows customers to reliably ingest large amounts of data in near real\-time from databases, files, and streaming sources into ClickHouse Cloud. Upsolver automatically detects changes in the source, and streams only changed rows into ClickHouse making it 50x to 100x faster and more cost\-effective than existing ETL and CDC solutions.


Our customers regularly use Upsolver to deliver high\-volume, nested streaming data, commonly in the order of 1\-2 million events per second, with **peaks that are 2x \- 5x this**. [Read what customers are saying](https://www.upsolver.com/case-studies?nav_bar=customers). Similarly, [customers use ClickHouse Cloud](https://clickhouse.com/use-cases) to process, store, and analyze billions of rows in seconds.


## The challenge of performing ETL at scale [\#](/blog/upsolver-high-volume-etl-for-real-time-analytics#the-challenge-of-performing-etl-at-scale)


ClickHouse is the fastest and most efficient open\-source database for real\-time analytics, data\-driven apps, and increasingly, low\-latency AI use cases. Users derive the most benefit from ClickHouse when the data is loaded into one of its many specialized table engines. While solutions exist for the challenge of loading large volumes, performing transformations and filtering at scale introduces further challenges for users.


The main capabilities needed for performing ETL at scale with ClickHouse are:


1. **A simple high\-performance architecture** \- An architecture which minimizes the number of systems and components data must traverse
2. **Streaming ingestion and transformations** \- Capabilities for transforming and filtering data reliably and efficiently
3. **Comprehensive monitoring of ingestion jobs** \- Deep monitoring into data and ingestion tasks is required. This also accelerates issue resolution.


Upsolver provides all of these capabilities as we describe in detail below.


## A simple high\-performance architecture [\#](/blog/upsolver-high-volume-etl-for-real-time-analytics#a-simple-high-performance-architecture)


Out\-of\-the\-box, ClickHouse offers numerous [connectors](https://clickhouse.com/docs/en/integrations) to popular sources, and [ClickPipes](https://clickhouse.com/cloud/clickpipes) for managed continuous ingestion in ClickHouse Cloud. Some connectors are developed and managed by the ClickHouse team, some by 3rd party vendors, and others by the community.


As mentioned previously, the key to high performance and reliable ETL and CDC is a simple architecture; loading only what’s required, performing efficient filtering and transformations, and providing actionable observability. Therefore, identifying, testing, and implementing the right solution for your use case can be daunting. In particular, as data volumes and throughput increase, it becomes increasingly difficult to ensure data is delivered exactly once in a correct and consistent format.


With Upsolver, ClickHouse Cloud users have the option to directly connect to operational sources, monitor for new events and transform raw event data in\-flight, all while Upsolver automatically scales up and down to match demand.


This makes it possible to simplify your architecture by eliminating Debezium for CDC, queues, and notification scripts for continuous file loading or complex transformations to handle incremental loading, updating, and deleting of rows.


ClickHouse Cloud users are always looking for simple, highly scalable, reliable, and cost\-effective solutions to stream data from multiple sources into ClickHouse whilst performing complex transformations prior to insertion. Upsolver’s [ClickHouse connector](https://docs.upsolver.com/reference/sql-commands/connections/create-connection/clickhouse) does just this, and more.


## Streaming ingestion and transformations [\#](/blog/upsolver-high-volume-etl-for-real-time-analytics#streaming-ingestion-and-transformations)


It’s common practice to create a raw staging zone external to your data warehouse of choice where you can filter, transform, and enrich your data prior to sending it to their preferred destinations.


In order to implement this design, users need a cost\-efficient tool capable of providing not only sufficiently powerful filtering and processing capabilities but also one that is able to scale to the TB volumes seen in warehouses.


Upsolver meets all of these requirements allowing warehouse users to declare two types of jobs:


[Ingestion jobs](https://docs.upsolver.com/reference/sql-commands/jobs/create-job/ingestion) allow you to bring data from a source, convert it to columnar format (Parquet or ORC), partition it and stage it in an object store such as Amazon S3\. Users then have the flexibility to either load data directly into ClickHouse or another target of their choice.


[Transformation jobs](https://docs.upsolver.com/reference/sql-commands/jobs/create-job/transformation) allows you to read from a staging table in S3, created by an ingestion job. Using SQL users can then filter, transform and manipulate the rows in near real\-time. Transformation jobs can be assembled into a pipeline that finally streams the results into a ClickHouse table.


### Simple configuration [\#](/blog/upsolver-high-volume-etl-for-real-time-analytics#simple-configuration)


Upsolver makes it simple for users to build the above production\-grade ingestion jobs with minimal learning curve. Ingestion jobs can be created easily using either a UI or via SQL. Users can integrate Upsolver into their CI/CD process and automate pipeline changes using the SDK and APIs. [Get started using the wizard](https://docs.upsolver.com/quickstarts/data-ingestion-wizard/using-the-wizard).


![upsolver.png](/uploads/upsolver_eec7e29909.png)
For users comfortable in SQL, jobs can be defined in a familiar DDL syntax. The following is a simple example showing how to create a connection to ClickHouse Cloud and a job that continuously reads objects from S3 and loads them into a ClickHouse table.



```
CREATE CLICKHOUSE CONNECTION my_ch_connection
CONNECTION_STRING = 'http://x.us-east-1.aws.clickhouse.cloud:8123/prod_db'
USER_NAME = 'username'
PASSWORD = 'password';

CREATE SYNC JOB load_iceberg_from_s3
DEDUPLICATE_WITH = (COLUMNS = (event_id), WINDOW = 12 HOURS)
AS COPY FROM S3 raw_s3_landingzone_connection
  location = 's3://landingzone/partner/'
INTO CLICKHOUSE my_ch_connection.prod_db.target_tbl;

```

## Comprehensive monitoring \& fully managed data synchronization [\#](/blog/upsolver-high-volume-etl-for-real-time-analytics#comprehensive-monitoring--fully-managed-data-synchronization)


Upsolver automatically keeps sources and targets in sync, evolves schemas, and ensures proper data type matching. It automatically recovers from connectivity and network hiccups and minimizes impact from traffic spikes. In addition, Upsolver ensures duplicates are removed and late arriving data is seamlessly incorporated. [Learn how this is done](https://docs.upsolver.com/articles/get-started/understanding-sync-and-non-sync-jobs).


Monitoring ingestion jobs and observing data quality and health is offered in a single place. Upsolver’s real\-time job monitoring and data observability lets users quickly detect and fix job or data\-related issues. Users can monitor and alert on connectivity failures, schema changes, and changes in the rate of processing volume. Even more complex alerts can be created which detect the uniqueness of column values and ensure user\-defined data quality expectations are met. [Learn more about data observability](https://docs.upsolver.com/reference/monitoring/datasets).


![upsolver_metrics.png](/uploads/upsolver_metrics_db135377e2.png)
## Testing continuous ingestion performance [\#](/blog/upsolver-high-volume-etl-for-real-time-analytics#testing-continuous-ingestion-performance)


High volume, continuous data ingestion is a common use case for many ClickHouse Cloud customers, we wanted to evaluate how quickly Upsolver can load **44\.7B** rows which are divided into 68,783 files, totaling around 480GB (about 7 MB per file).


For this test, we demonstrate the speed at which Upsolver can continuously load new data into ClickHouse, not accounting for a one time historical backfill. To do this, we created a job similar to the one shown above (`load_orders_to_clickhouse`). Upsolver is a stream processing system, so it attempts to load data in event order. Once the execution plan is created, Upsolver begins to read files, breaks up rows into chunks and loads the chunks into a MergeTree table.


We used a 3\-node 360 GiB RAM, 96vCPU ClickHouse Cloud cluster and a 16\-node r6i.24xlarge node with 96vCPU and 760GiB of RAM for Upsolver. By default, Upsolver uses AWS EC2 SpotSPOT instances so the cost per instance was only $3\.60/hr/instance.


The following graph shows the Upsolver tasks that copy files from S3, parse the rows, and load them into ClickHouse. On average, copy tasks took around 3\.5 minutes. The job started copying data at 15 and finished at 17, a run time of 108 minutes or **1 hour and 48 minutes** to load 44\.7B rows. At $3\.60/hr/instance, the total cost to load 44\.7B rows was only **$100\.**


![insert_performance_upsolver.png](/uploads/insert_performance_upsolver_3c28cc40b8.png)
Upsolver automatically detects changes in the source, and streams only changed rows into ClickHouse. Orchestration and task scheduling is handled internally, eliminating the need for external tools like Airflow or AWS Lambda. [Learn more](https://docs.upsolver.com/reference/sql-commands/jobs/create-job/transformation/insert) about transformation jobs.


## When to use Upsolver with ClickHouse Cloud [\#](/blog/upsolver-high-volume-etl-for-real-time-analytics#when-to-use-upsolver-with-clickhouse-cloud)


Upsolver is purpose\-built to make it easy for users to reliably move high volume, high throughput data between operational and analytical systems. Upsolver and ClickHouse are often used in the following four use cases.


### Streaming ETL → Clickhouse Cloud [\#](/blog/upsolver-high-volume-etl-for-real-time-analytics#streaming-etl--clickhouse-cloud)


Upsolver supports direct streaming from Apache Kafka (self\-managed), Confluent, Amazon Kinesis or Amazon MSK into ClickHouse tables. Oftentimes, application events are streamed at a rate of 1000’s per second, with more extreme rates in ad\-tech and gaming exceeding 1,000,000’s per second. Should you need to perform transformations and filtering on this data prior to insertion, Upsolver is unique in its ability to address these requirements.


![Upsolver - streaming ETL.png](/uploads/Upsolver_streaming_data_e650bd139b.png)
### Object storage (S3\) → Clickhouse Cloud [\#](/blog/upsolver-high-volume-etl-for-real-time-analytics#object-storage-s3--clickhouse-cloud)


You can use Upsolver to continuously load batch\-produced data available in object stores, like Amazon S3, into ClickHouse tables. This data often comes from partners, is exported from legacy systems, or is generated by security, infrastructure, and system logging and tracing tools. In these use cases, users typically wish to filter and prepare (fix timestamps, remove bad rows, enrich, etc.) terabytes of data before loading and merging rows into ClickHouse as quickly and as cost\-efficiently as possible.


![Upsolver - object storage.png](/uploads/Upsolver_object_storage_3be8ad6b77.png)
### Ingestion into Clickhouse Cloud \+ Iceberg [\#](/blog/upsolver-high-volume-etl-for-real-time-analytics#ingestion-into-clickhouse-cloud--iceberg)


While ClickHouse is a very fast and capable real\-time database, many companies use a range of tools to perform analytics and train ML models using structured and semi\-structured data. To serve these use cases, they must store raw events in the lakehouse using [Apache Iceberg](https://iceberg.apache.org/). The Iceberg table format makes it easy to organize and manage large amounts of structured data in object stores. It also makes it easy to rearrange and evolve large datasets to better meet business needs without costly rewriting of data files. Once in the lake, tables are accessible from ClickHouse, Jupyter notebooks with Python, and other modern processing engines like Apache Spark and Flink.


![Upsolver - ingestion into CH + Iceberg.png](/uploads/Upsolver_ingestion_into_CH_Iceberg_10803c4f42.png)
### Change Data Capture (CDC) [\#](/blog/upsolver-high-volume-etl-for-real-time-analytics#change-data-capture-cdc)


ClickHouse allows users to query their data in place, like S3 or MySQL without first loading into native tables; this is also known as query federation. Furthermore, users can extract data, ad\-hoc, from external systems and insert it into ClickHouse native tables for fast analysis. However, these approaches come with limitations and are not ideal for keeping native tables up to date as the source data changes.


To solve this problem, Upsolver allows users to stream source changes (CDC) from operational databases into the Iceberg lakehouse and ClickHouse. Upsolver ensures these events are transformed and prepared in an appropriate format to exploit ClickHouse [CollapsingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/collapsingmergetree#table_engine-collapsingmergetree) or [VersionedCollapsingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/versionedcollapsingmergetree#versionedcollapsingmergetree) table engines that implement the CDC update/delete logic. Upsolver adds additional columns such as IS\_DELETED and EVENT\_TIME as well as allowing you to include computed fields that aid in implementing efficient CDC for ClickHouse.


## Packing a ton of value [\#](/blog/upsolver-high-volume-etl-for-real-time-analytics#packing-a-ton-of-value)


Upsolver’s high\-volume connector for ClickHouse Cloud enables users to unify their data ingestion and movement, simplifying their architecture and delivering fast, reliable, and high quality data to ClickHouse, Iceberg lakehouse and operational systems. The new integration allows customers to reliably ingest large amounts of data in near real\-time from databases, files and streaming sources 50X \- 100X faster and significantly cheaper than alternative solutions.


[Try Upsolver for 14 days, completely free!](https://www.upsolver.com/ingestion-signup?utm_page=clickhouse)

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
