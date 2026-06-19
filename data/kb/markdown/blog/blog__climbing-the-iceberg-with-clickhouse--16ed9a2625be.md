# Climbing the Iceberg with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Climbing the Iceberg with ClickHouse

![](/_next/image?url=%2Fuploads%2FMelvyn_00a76a1519.PNG&w=96&q=75)[Melvyn Peignon](/authors/melvyn-peignon)Feb 19, 2025 · 17 minutes read## Introduction [\#](/blog/climbing-the-iceberg-with-clickhouse#introduction)


Reflecting on 2024, one technology stood out consistently: Apache Iceberg and, more broadly, the lakehouse paradigm. This trend was evident through multiple industry developments, starting with the [acquisitions of Tabular by Databricks](https://www.databricks.com/company/newsroom/press-releases/databricks-agrees-acquire-tabular-company-founded-original-creators), the recent [announcement of Amazon S3 Tables from AWS](https://aws.amazon.com/s3/features/tables/) during Re, [the investment that GCP has made](https://cloud.google.com/bigquery/docs/iceberg-tables) to improve the integration between Iceberg and BigQuery/BigLake, and Snowflake’s investment in Iceberg and its support via [the development of Polaris](https://www.snowflake.com/en/blog/introducing-polaris-catalog/).


All of these announcements lead people to wonder:


- **How do your data lake and lakehouse integrate with ClickHouse?**
- **What’s planned for ClickHouse in 2025 in that space?**


This blog article will answer these two questions while referencing architectures we have seen in the field when working with our users. We’ll also walk you through some of the implementation details from our engineering team, and finally, we will go over the roadmap for 2025! 


If you are interested in data lakes, [data lakehouses](https://clickhouse.com/resources/engineering/data-lakehouse), and ClickHouse and would like to be a design partner, gain early access to some of the features mentioned below, or learn more about our upcoming work, complete [this form](https://clickhouse.com/cloud/data-lakehouse-waitlist), and we’ll be in touch soon!


## How can you use ClickHouse with your data lake and lakehouse? [\#](/blog/climbing-the-iceberg-with-clickhouse#how-can-you-use-clickhouse-with-your-data-lake-and-lakehouse)


If you look at some of the earliest pull requests in the ClickHouse repository, you’ll see a strong emphasis on integrating with external systems. Over time, ClickHouse has evolved into a powerful bridge between data lakes and data warehouses, supporting queues, databases, and object stores with compatibility for more than 60 input and output formats. This versatility allows users to benefit from the flexibility of a data lake while maintaining real\-time query performance.


Today, most ClickHouse users adopt this approach, with S3 being one of the most widely used data sources for both loading data and ad\-hoc querying. Features like [s3Cluster](https://clickhouse.com/docs/en/sql-reference/table-functions/s3Cluster) and the recently introduced [S3Queue](https://clickhouse.com/docs/en/engines/table-engines/integrations/s3queue) (also available for GCS and Azure) have made this integration seamless, enabling ClickHouse to either query data in place for exploratory analysis or efficiently ingest it for high\-performance analytics.


As many companies and teams now rethink their data lake and data warehousing strategies, some have already adopted ClickHouse, while others are just beginning to explore how it aligns with their lakehouse ambitions.


There are a few scenarios in which ClickHouse is being used in the context of lakehouse and data lake. We can roughly break them down into three categories:


- Data loading from a data lake/lakehouse to ClickHouse
- Ad hoc and federated queries to data lakes/lakehouses
- Frequent query to data lakes/lakehouses


### Data loading from a data lake to ClickHouse [\#](/blog/climbing-the-iceberg-with-clickhouse#data-loading-from-a-data-lake-to-clickhouse)


As mentioned previously, one of our most popular integrations in ClickHouse is the `s3cluster` and `s3queue` table functions, as well as their equivalents for Google Cloud and Azure Blob Storage. People typically use these functions to load data in ClickHouse either as a one\-time load (using `s3cluster`) or incrementally using `s3queue`. ClickPipes builds on the former of these functions, providing both bulk and incremental loading capabilities from object storage with exactly\-once semantics. 


![s3_lakehouse.png](/uploads/s3_lakehouse_021a6ce87d.png)
  

The diagram above demonstrates one of the most common architectural patterns, used frequently in scenarios where applications need to add data incrementally, e.g. in log and web analytics use cases.
In this scenario, ClickHouse continuously loads the data from the data lake storing it in ClickHouse tables for fast analytics. ClickHouse will frequently poll S3 to check if new data is present. If new files are detected, ClickHouse will automatically read, load, and aggregate all the data into the specified tables. 


This concept can easily be extended to open table formats like Iceberg, Delta, or even Hudi. 


Subsets of data can also be loaded from your data lake into ClickHouse using a double\-write approach. We see this method being used where teams are responsible for their data platform, where the primary goal is to store the majority of the company’s data while ensuring seamless access and usability for various teams, each with its own requirements and tools. Iceberg is particularly useful for this scenario. Data flows through a Kafka topic, with multiple consumers simultaneously loading it into both ClickHouse and Iceberg tables. This approach is ideal for immutable data and append\-only use cases where records remain unchanged over time.


![kafka_iceberg.png](/uploads/kafka_iceberg_2f0bbeaff0.png)
  

### Ad\-hoc and federated queries to data lakes and lakehouses with ClickHouse [\#](/blog/climbing-the-iceberg-with-clickhouse#ad-hoc-and-federated-queries-to-data-lakes-and-lakehouses-with-clickhouse)


Another frequently used pattern we see in the field is when a customer already uses ClickHouse but occasionally needs to run a query on an Iceberg or Delta table or even a set of files on S3\. Assuming this data is not frequently queried, loading it into ClickHouse does not necessarily provide sufficient value. In this case, ClickHouse can also be used to query this data in place, effectively replacing technologies such as Athena. This can be achieved with the [s3cluster](https://clickhouse.com/docs/en/sql-reference/table-functions/s3Cluster), [icebergCluster,](https://clickhouse.com/docs/en/sql-reference/table-functions/icebergCluster) and [deltaLakeCluster](https://clickhouse.com/docs/en/sql-reference/table-functions/deltalakeCluster) functions. While performance in these scenarios doesn’t match that of a native ClickHouse table, where millisecond response times are the norm, the infrequent access patterns generally make second\-order response times acceptable.



> If we consider the previous example, we can easily envision a scenario in which regulatory purposes require being able to check activity related to a specific product or user for X amount of months.


![adhoc_query.png](/uploads/adhoc_query_90a566c0a9.png)
  

These scenarios can obviously be extended to Iceberg, Delta Lake, and even Hudi tables. 
By extension, ClickHouse can be seen as a hot layer and Iceberg as the cold layer. The vast majority of queries are being executed against ClickHouse, while a few queries need to be executed fully against the data lake or federated with the data lake (when information is split across these two storages)


Given ClickHouse’s versatility and integrations, query federation is becoming an increasingly common use case, similar to how Athena is used.


Furthermore, as well as supporting files and open table formats, ClickHouse gives you the ability to query multiple data sources and correlate the results. Typical sources for query federation include:


- PostgreSQL
- MySQL
- Data lake (S3, GCS, Azure)
- ClickHouse Table
- MongoDB


This provides a lot of flexibility, in particular when exploring and handling datasets that are not queried frequently enough to justify storing them in a columnar database like ClickHouse.


We also see use cases where users must correlate and enrich rows in ClickHouse with data that resides in MongoDB and PostgreSQL. In these scenarios, MongoDB and PostgreSQL can be used as [dictionary source](https://clickhouse.com/docs/en/sql-reference/dictionaries#dictionary-sources).


![dictionary_lakehouse.png](/uploads/dictionary_lakehouse_c57d0e0c8e.png)
  

### Frequent queries to data lakes / lakehouses with ClickHouse [\#](/blog/climbing-the-iceberg-with-clickhouse#frequent-queries-to-data-lakes--lakehouses-with-clickhouse)


To better illustrate the last scenario, think of a financial services or crypto company that needs to have access to many different datasets for its research. While these datasets can be accessed via APIs or similar approaches, as data volumes grow and storage costs increase, a typical pattern is sharing the dataset using Iceberg or other open table formats.


You can see an example of this on [Allium’s integration page](https://docs.allium.so/datashares/overview).


Table functions like [icebergCluster](https://clickhouse.com/docs/en/sql-reference/table-functions/icebergCluster) or [deltaLakeCluster](https://clickhouse.com/docs/en/sql-reference/table-functions/deltalakeCluster) allow ClickHouse to query such systems easily. However, this currently has a few limitations.


#### Native format is (currently) faster [\#](/blog/climbing-the-iceberg-with-clickhouse#native-format-is-currently-faster)


Firstly, this approach does not leverage ClickHouse’s optimized internal format, resulting in slower query performance on a data lake compared to data stored natively in ClickHouse. This [gap is common among databases](https://www.linkedin.com/pulse/tpch-test-databricks-vs-fabric-snowflake-pawel-potasinski-oxfsf/) that support open table formats, where internal storage and query engines are tightly optimized together. Additionally, databases that handle both ingestion and querying face broader challenges than pure query engines. In 2025, we aim to reduce the performance gap between ClickHouse’s native format and open standards.


#### Improving data discovery [\#](/blog/climbing-the-iceberg-with-clickhouse#improving-data-discovery)


The second limitation is data discovery. While the concept has been [around for a while](https://en.wikipedia.org/wiki/Apache_Hive), it has recently been revitalized with the rise of recent catalogs that help with discovery and table integration but also manage access and user permissions. Historically, ClickHouse has been unable to automatically discover all the tables managed by a catalog, requiring users to explicitly provide the URL of a Delta or Iceberg table they wish to query. This limitation was a frequent challenge for our users. Acknowledging this limitation, we have [recently added initial support for integrating with the Iceberg REST catalog.](https://github.com/ClickHouse/ClickHouse/pull/71542)


Out of the 3 scenarios listed above, this is probably the scenario for which we need to improve our users' experience the most. Consequently, we have invested engineering time in expanding our integrations to support catalogs. But this is only the first step; we expect to release many additional features and support in the coming months.


## Recent work [\#](/blog/climbing-the-iceberg-with-clickhouse#recent-work)


Here’s a look at our recent work and where we’re focusing our efforts in this space over the coming months.


### Catalog integration [\#](/blog/climbing-the-iceberg-with-clickhouse#catalog-integration)


Even though ClickHouse already supports Iceberg, DeltaLake and Hudi with dedicated table engines, it still requires a direct path to a table to query it. The best way to improve this situation, as noted above, is to integrate with data catalogs. We envision a system where ClickHouse interacts with both the data catalog and the storage to be able to read the right metadata: identifying the path to a table, integrating automatically with any access controls, and reading only the data required.


![catalog_integration.png](/uploads/catalog_integration_415967caa9.png)
  

While we’re in the early stages of development here, we can already demonstrate this concept in action with the [Polaris](https://www.snowflake.com/en/blog/introducing-polaris-catalog/) catalog:


![catalogue_lakehouse.png](/uploads/snowflake_catalog_e92ff3d0c2.gif)
  

In the example above, some tables reside in an Iceberg table within Snowflake, which offers a managed service of Polaris. Starting from version 24\.12, ClickHouse has introduced support for these Iceberg catalogs, enabling users to integrate with a catalog and query it directly from ClickHouse. You can now query your Iceberg\-managed table in Snowflake using ClickHouse via the catalog!


Let’s illustrate this with an example. In the screenshot above, you can see the catalog and its various namespaces. Let’s create the connection to the catalog in ClickHouse:



```

```
CREATE DATABASE catalog
ENGINE = Iceberg('https://********************/polaris/api/catalog/v1')
SETTINGS catalog_type = 'rest', catalog_credential = '*********************', warehouse= 'polarisch'
```

```


```
Elapsed: 0.001 sec. 

```

You can now start the exploration:



```

```
SHOW TABLES
```

```


```
   ┌─────────────────────────────────────────┐
   │ name                                    │
   ├─────────────────────────────────────────┤
1. │ benchmark.notpartitionedwikistats       │
2. │  core.alerts                            │
3. │  core.logs                              │
4. │  hits.dailypartitionned                 │
5. │  hits.notpartitioned                    │
6. │  product.roadmap                        │
7. │  website.logs                           │
   └─────────────────────────────────────────┘

7 rows in set. Elapsed: 2.449 sec.

```

Check the schema of your tables:



```

```
SHOW CREATE TABLE catalog.`product.roadmap`

CREATE TABLE catalog.`product.roadmap`
(
 `feature` Nullable(String),                                                                                     
 `team` Nullable(String),                                                                                        
 `owner` Nullable(String),                                                                                      
 `engineering_lead` Nullable(String)                                                                             
)                                                                                                               
ENGINE = Iceberg('s3://paths/', 'user', '[HIDDEN]')
```

```


```
1 row in set. Elapsed: 0.219 sec.

```

And most importantly, you can query the data using ClickHouse:



```

```
SELECT *
FROM `product.roadmap`
WHERE feature ILIKE '%Lakehouse%'
```

```


```
┌────────────┬──────────┬────────┬──────────────────┐
│ feature	 │ team 	│ owner  │ engineering_lead │
├────────────┼──────────┼────────┼──────────────────┤
│ Lakehouse  │ Samurai  │ Melvyn │ Sasha S.     	│
└────────────┴──────────┴────────┴──────────────────┘

1 row in set. Elapsed: 0.477 sec.

```

Our initial implementation supports the REST catalog, but that’s just the beginning. We plan to add support for the Glue catalog soon, along with Unity catalog for Delta tables.


### Cluster function for lakehouse [\#](/blog/climbing-the-iceberg-with-clickhouse#cluster-function-for-lakehouse)


The existing `s3Cluster` function can already be used to query data lakes. This allows for a cluster to distribute the processing of a query across multiple nodes. Until recently, we didn’t support this feature for Iceberg, Hudi, or Delta Lake. This was [addressed in version](https://github.com/ClickHouse/ClickHouse/pull/72045) 24\.11\. If you didn’t have time to test it, here are some results highlighting the improved performance using a cluster of 3 nodes.



```

```
SELECT count(*) FROM icebergS3Cluster('my_cluster', 's3://path/', '****************', '****************') WHERE (project = 'en') AND (subproject = 'turing')
```

```


```
┌──────────┐
│ count(*) │
├──────────┤
│     146  │
└──────────┘

1 row in set. Elapsed: 907.256 sec. Processed 95.97 billion rows, 2.53 TB (105.78 million rows/s., 2.79 GB/s.)
Peak memory usage: 2.69 GiB.

```

On an non\-optimized and non\-compacted table, the speed\-up scales linearly with the number of nodes in the cluster.



```

```
SELECT count(*) FROM iceberg('s3://path/', '****************', '****************') WHERE (project = 'en') AND (subproject = 'turing')
```

```


```
┌─────────┐
│ count(*)│
├─────────┤
│     146 │
└─────────┘

1 row in set. Elapsed: 2595.390 sec. Processed 95.97 billion rows, 2.53 TB (36.98 million rows/s., 974.86 MB/s.)
Peak memory usage: 2.78 GiB.

```

## Work in progress for open table formats [\#](/blog/climbing-the-iceberg-with-clickhouse#work-in-progress-for-open-table-formats)


As well as investing in catalog support, we are actively improving our support for open table formats.


### Iceberg [\#](/blog/climbing-the-iceberg-with-clickhouse#iceberg)


While Iceberg has a rich ecosystem, regretfully no library has been developed in C\+\+. While this might [change soon](https://github.com/apache/iceberg-cpp), this has made it difficult to support some of the latest features that the Iceberg specification offers such as support for deleted rows.


Over the last year, ClickHouse has made significant progress in expanding its support for Iceberg, with several features already implemented and others still in progress, including:


- Support for [partition pruning](https://github.com/ClickHouse/ClickHouse/pull/72044)
- Support for [schema evolution](https://github.com/ClickHouse/ClickHouse/pull/69445)
- Support for [time travel](https://github.com/ClickHouse/ClickHouse/pull/71072)


On completion of support for Iceberg v2 features, we plan to work on adding support for v3\.


### Delta Lake [\#](/blog/climbing-the-iceberg-with-clickhouse#delta-lake)


One of our key priorities, already in progress, is improving Delta Lake support in ClickHouse. The [Delta Kernel](https://docs.delta.io/latest/delta-kernel.html), initially released as an experimental feature in 2023, is expected to reach GA soon. It comes in two variants: a Java Kernel and a Rust Kernel. For ClickHouse, we’re integrating the Rust Kernel to accelerate future Delta Lake development. Once the Kernel supports writing to Delta tables, ClickHouse will be able to offer write support as well.


In addition to this, we can build on our work with Iceberg to enhance Delta support. As a result, many of the Iceberg features will soon be available for Delta as well. Similar to the Iceberg catalog, we aim to support the Delta catalog (primarily Unity). By leveraging our initial Iceberg catalog implementation, extending support to Delta should be relatively straightforward.


## Roadmap for lakehouses in 2025 [\#](/blog/climbing-the-iceberg-with-clickhouse#roadmap-for-lakehouses-in-2025)


Every year, we publish a [new roadmap for the ClickHouse core](https://github.com/ClickHouse/ClickHouse/issues/74046) database, and 2025 is no exception. While many features are planned, in summary, our focus falls into three key areas:


**1\. Enhancing the user experience for ad\-hoc and frequent queries on data lakes/lakehouses**


- Expanding catalog integrations for Iceberg and Delta
- Full support for Iceberg and Delta\-specific features, including complex data types such as the variant type
- Introducing a metadata caching layer for improved query performance
- Enhancing our Parquet reader for better efficiency


This work is essential for enabling users to easily discover their data within their data lake and make it readily accessible and queryable in ClickHouse. In addition to all the above mentioned features, some work is also planned around improving the distributed query execution when reading the Parquet format. Currently the unit of task distribution is done at the file level. With file sizes often varying, this leads to suboptimal distribution of work. We thus intend to make the unit of distribution more granular by exploiting properties of the Parquet format.


**2\. Improving ClickHouse’s capabilities for working with data lakes/lakehouses**


- Enabling write support for Iceberg and Delta
- Compactions and liquid clustering
- Introducing external materialized views for better query efficiency


Currently, ClickHouse cannot be used as a writer for Iceberg, which presents some limitations. ClickHouse is widely used for data preprocessing, particularly through its extensive support for materialized views. With write support, we will be able to leverage our experience with the MergeTree table engine to implement efficient compaction for Iceberg and Delta tables.


**3\. Iceberg CDC Connector in ClickPipes: Seamlessly replicate Iceberg tables to ClickHouse native tables for real\-time, customer\-facing analytics.**


With the objective of unlocking millisecond query latencies on your data lake tables, this work includes:


- Full support for initial load and Change Data Capture (CDC) on append\-only tables.
- Expanding in later iterations to support for replicating UPDATEs and DELETE operations.
- Fully managed experience on ClickHouse Cloud with inbuilt metrics and monitoring.


Additionally, we will be rolling out cloud\-specific features to simplify data onboarding, improve data access, and optimize cloud resource usage.


As we develop these new capabilities and refine our support for open table formats and lakehouse architectures, we’re working closely with the community to gather feedback and improve the experience.


If you’re interested in becoming a design partner, gaining early access to these features, or learning more about our upcoming work, complete [this form](https://clickhouse.com/cloud/data-lakehouse-waitlist), and we’ll be in touch soon!!


## Conclusion [\#](/blog/climbing-the-iceberg-with-clickhouse#conclusion)


We hope this article has highlighted the many ways ClickHouse can be used with your data lake and lakehouse while offering insight into our vision for this evolving space. As technology matures in that space, we expect ClickHouse to be at the heart of your data lake tooling in the near future. If you are an existing ClickHouse and data lake/lakehouse fan, you should be as excited as we are about the new features expected to be released in 2025\. If you have a feature request or would like to contribute to ClickHouse, make your voice heard and participate in some of the discussions in [GitHub](https://github.com/ClickHouse/ClickHouse) or in [Slack](https://clickhouse.com/slack)!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
