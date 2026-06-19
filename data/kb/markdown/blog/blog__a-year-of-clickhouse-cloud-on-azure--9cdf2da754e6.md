# Agent\-Facing Analytics, Data Lake Support, and More: A Year of ClickHouse Cloud on Azure


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Agent\-Facing Analytics, Data Lake Support, and More: A Year of ClickHouse Cloud on Azure

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 15, 2025 · 18 minutes read![04 (1).png](/uploads/04_1_c29ff2cb5a.png)
Since the [launch of ClickHouse Cloud on Microsoft Azure](https://clickhouse.com/blog/clickhouse-cloud-is-now-generally-available-on-microsoft-azure) last year, the response from developers, data engineers, and architects has been incredible. And this is unsurprising – ClickHouse has been available in open source for over a decade and has been adopted for some of the most demanding production workloads, including Microsoft’s own [petabyte\-scale web analytics product, Clarity](https://clarity.microsoft.com/blog/why-microsoft-clarity-chose-clickhouse).


Now, with ClickHouse available on Azure as a turnkey cloud native database, innovators and builders have tapped into our platform to power interactive data\-driven applications with high\-performance analytical workloads. For example, [Weights \& Biases launched Weave](https://clickhouse.com/blog/weights-and-biases-scale-ai-development), an LLM observability tool, built on ClickHouse Cloud and available on Microsoft Azure, to help developers monitor and scale generative AI apps in production. Similarly, [Astronomer launched Astro Observe](https://clickhouse.com/blog/why-astronomer-chose-clickhouse-to-power-its-new-data-observability-platform-astro-observe), a ClickHouse\-powered observability platform on Microsoft Azure that gives Airflow users real\-time pipeline insights using OpenLineage and AI\-driven diagnostics.


Building on the initial success of these users and use cases, we have doubled down on Azure ecosystem support to make it even easier for Azure customers to leverage ClickHouse Cloud.


The rest of this blog covers our latest product announcements from AI ecosystems and data lake support, to data onboarding and programming language expansion. Finally, we talk about the evolution of our cloud architecture, enterprise security, and compliance.


## Agent\-facing analytics with Azure OpenAI [\#](/blog/a-year-of-clickhouse-cloud-on-azure#agent-facing-analytics-with-azure-openai)


Integrating Azure OpenAI with ClickHouse offers a powerful foundation for real\-time analytics and natural language interaction within the Azure ecosystem. [Agent\-facing analytics](https://clickhouse.com/blog/agent-facing-analytics), where AI applications consume and interpret data to assist users or trigger workflows, benefit greatly from this setup. ClickHouse’s high\-performance, columnar storage engine and ability to handle massive volumes of data with low\-latency queries make it especially well\-suited for powering responsive, data\-hungry applications like these.


![announce1.png](/uploads/announce1_75e47bedf5.png)
With Azure OpenAI’s support for the [Model Context Protocol (MCP)](https://github.com/ClickHouse/mcp-clickhouse/), developers can build structured, multi\-step workflows that guide large language models to query, interpret, and summarize data stored in ClickHouse. Models like GPT\-4\.1, available through Azure OpenAI, are particularly well\-suited for MCP scenarios, as they support function calling, structured reasoning, and tool integration. Because ClickHouse is natively available as a managed service on Azure, all data remains within the Azure environment, ensuring compliance, reducing data movement, and streamlining performance. This integration empowers organizations to build analytics assistants that leverage conversational AI and real\-time data processing without leaving the Azure cloud.


## Azure Data Lake support [\#](/blog/a-year-of-clickhouse-cloud-on-azure#azure-data-lake-support)


In addition to ① having MergeTree, a high\-performance native format for low\-latency queries and high insert throughput, ClickHouse also provides the ability to read and write over 70 different data formats, including ② Parquet, Avro, JSON, as well as open data lake formats like Iceberg and ③ Delta Lake.


Fueled by increasing interest from our users to combine the power of real\-time analytical databases with open table formats, we are focusing on deepening our integration with Azure Data Lake and Databricks on Azure.


![11 (1).png](/uploads/11_1_14cf803cb4.png)
### Querying Delta Lake on Azure [\#](/blog/a-year-of-clickhouse-cloud-on-azure#querying-delta-lake-on-azure)


Delta Lake has been supported by ClickHouse for a while now, but as of [25\.4 release](https://github.com/ClickHouse/ClickHouse/pull/74541), it is available to the Azure ecosystem. You can now use ClickHouse to query the data stored in your Delta Lake table, managed by Databricks or self\-managed Delta Lake tables running in Azure. It is as simple as providing the path to your table and the credentials to access it. This integration will automatically and seamlessly be upgraded over time, leveraging the integration of the [delta kernel](https://delta.io/blog/delta-kernel/) in ClickHouse. To learn more, see our documentation You can read more about it [here](https://clickhouse.com/docs/sql-reference/table-functions/deltalake).


### Databricks Unity Catalog on Azure [\#](/blog/a-year-of-clickhouse-cloud-on-azure#databricks-unity-catalog-on-azure)


Already [available](https://github.com/ClickHouse/ClickHouse/pull/76988) in open source and coming to the Azure managed service [soon](https://github.com/ClickHouse/ClickHouse/pull/80013), the ④ Unity Catalog integration will drastically simplify your experience using ClickHouse and Databricks as a joint data platform, with Databricks providing data lake management at scale and ClickHouse powering real\-time analytics queries on top of that data. Once you connect ClickHouse to the Unity Catalog, you can seamlessly discover tables and securely query the data in your Databricks ecosystem. ee our [guide](https://clickhouse.com/docs/use-cases/data-lake/unity-catalog) for more).


## Data onboarding [\#](/blog/a-year-of-clickhouse-cloud-on-azure#data-onboarding)


We’ve invested heavily in making data onboarding to ClickHouse easy for Azure users, with the goal of improving time to value in building and maintaining applications. [ClickPipes](https://clickhouse.com/cloud/clickpipes), our integration engine for moving massive volumes of data to ClickHouse, supports direct connectors to Azure Blob Storage, Flexible Server for Postgres, and Event Hubs. ClickHouse open source also includes native support for Azure Blob Storage through multiple table functions. Additionally, Azure Data Factory natively supports writing into and reading from ClickHouse.


### ClickPipes Azure Blob Storage support [\#](/blog/a-year-of-clickhouse-cloud-on-azure#clickpipes-azure-blob-storage-support)


Today, we’re excited to announce the **Azure Blob Storage connector for ClickPipes**, now available in Private Preview. This connector allows customers to seamlessly load files from Azure Blob Storage into ClickHouse Cloud. It supports two modes of ingestion: **one\-time loads** and **continuous ingestion** as new files are added to the storage containers.


[You can sign up for the private preview here.](https://clickhouse.com/cloud/clickpipes/azure-blob-storage-connector)


This connector is built to support enterprise\-grade workloads with the following capabilities:


1. **Built for reliability** – Under the hood, it leverages the native `[azureBlogStorageCluster](https://clickhouse.com/docs/sql-reference/table-functions/azureBlobStorageCluster)` table function in ClickHouse, but enhances it with improved reliability and a fully managed experience. Loading billions (or even trillions) of rows from object storage can be error\-prone due to transient network issues—retries aren’t trivial, and handling duplicates is tricky. The connector handles retries automatically and ensures **exactly\-once ingestion**, so you don’t have to worry about data consistency or partial loads.
2. **Secure by design** – It supports ingestion from private buckets, with authentication through connection string, which includes account name and key, or can be specified using the storage account URL. You can also use our Shared Access Signature (SAS) within the connection string for time\-limited access without sharing your storage account key.
3. **Optimized for performance** – The connector dynamically tunes ingestion based on your workload and the size of your ClickHouse instance—for example, by adjusting ingestion parallelism, tuning ClickHouse\-specific settings, and more.
4. **Fully managed experience** – The connector is fully integrated into the ClickHouse Cloud experience. It offers high availability, built\-in metrics and monitoring, including throughput, detailed logs for error diagnosis and debugging, in\-place pipe editing (e.g., adding columns), and more.


**Note:** Continuous ingestion may have some caveats, such as limits on the number of files in the bucket. We'll work with you during the private preview to assist with the implementation.


![Azure Blob Storage.gif](/uploads/Azure_Blob_Storage_8df8563bb7.gif)
### AzureQueue and azureBlobStorage [\#](/blog/a-year-of-clickhouse-cloud-on-azure#azurequeue-and-azureblobstorage)


In addition to the fully managed ClickPipes connector to Azure Blob Storage, it is possible to access Azure Blob storage directly from ClickHouse via the [azureBlobStorage table function](https://clickhouse.com/docs/sql-reference/table-functions/azureBlobStorage) for ad\-hoc queries and the [AzureQueue Table Engine](https://clickhouse.com/docs/engines/table-engines/integrations/azure-queue) for continuous data imports. Introduced in the ClickHouse [24\.7 release](https://github.com/ClickHouse/ClickHouse/pull/65458), AzureQueue will periodically check object storage for new files and load the data into ClickHouse automatically for you. It supports all the formats that ClickHouse supports and will simplify your data loading procedures.


### Azure Flexible Server (Postgres CDC) [\#](/blog/a-year-of-clickhouse-cloud-on-azure#azure-flexible-server-postgres-cdc)


We shipped the Postgres CDC connector for ClickPipes, enabling seamless replication of Postgres databases—whether managed or on\-premise—to ClickHouse Cloud. This connector eliminates the complex, slow, and expensive ETL tools that are not purpose\-built for Postgres. It includes native support for [Azure Flexible Server for Postgres](https://clickhouse.com/docs/integrations/clickpipes/postgres/source/azure-flexible-server-postgres) and comes with many optimizations enabling 10x faster initial loads—transferring terabytes of data in hours instead of days—and latencies as low as a few seconds. It also supports Postgres\-native features such as partitioned tables and complex data types, including arrays, JSONB, and TOAST columns.


The vision of this connector is to seamlessly enable Azure Postgres users to access **"the default data stack"** (Postgres \+ ClickHouse), a stack already embraced by leading companies like [GitLab](https://about.gitlab.com/blog/2022/04/29/two-sizes-fit-most-postgresql-and-clickhouse/), [Cloudflare](https://blog.cloudflare.com/http-analytics-for-6m-requests-per-second-using-clickhouse?glxid=25d1a1c5-1ce0-4589-8305-177654961925&pagePath=%2Fblog%2Fclickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database&origPath=%2Fblog%2Fclickhouse-acquires-peerdb-to-boost-real-time-analytics-with-postgres-cdc-integration&utm_ga=GA1.1.1147851049.1729970044/), and [Instacart](https://tech.instacart.com/real-time-fraud-detection-with-yoda-and-clickhouse-bd08e9dbe3f4), as well as many leading AI companies like [LangChain](https://clickhouse.com/blog/langchain-why-we-choose-clickhouse-to-power-langchain) and [LangFuse](https://langfuse.com/blog/2024-12-langfuse-v3-infrastructure-evolution), to solve most data challenges. This stack empowers businesses to handle transactional and analytical workloads with the right tool for the right job, while still harnessing the flexibility and power of open\-source technologies.


### Azure Event Hubs [\#](/blog/a-year-of-clickhouse-cloud-on-azure#azure-event-hubs)


ClickPipes also includes the Azure Event Hubs source [connector](https://clickhouse.com/docs/integrations/clickpipes/kafka#azure-eventhubs). This allows customers to stream event data in real\-time, with latency as low as a few seconds, from Azure Event Hubs to ClickHouse. It's ideal for use cases like website analytics, IoT device data, and other real\-time analytics where low\-latency ingestion and fast queries with high concurrency are critical.


This connector eliminates the need for external ETL tools, as it’s fully integrated within ClickHouse Cloud. Built specifically for ClickHouse, it features automatic column and type inference, native data\-type mapping, customizable table engines and ordering keys, and performance optimizations like parallel streaming through replicas and tuned ingestion settings for a high\-performance streaming experience.


### Azure Data Factory [\#](/blog/a-year-of-clickhouse-cloud-on-azure#azure-data-factory)


For those preferring Azure Data Factory, it offers a great data integration layer for ingesting data into or reading data from ClickHouse, thanks to its intuitive interface for designing data pipelines.


![announce3.png](/uploads/announce3_ab58153f19.png)
Creating a REST service from Microsoft Azure Data Factory to load data into ClickHouse


If you would like to use Microsoft Data Factory, the most optimal way to get high performance ingestion throughput is to use the REST interface. Find out more about using Azure Data Factory in [our documentation](https://clickhouse.com/docs/integrations/azure-data-factory/http-interface).


## Developer experience [\#](/blog/a-year-of-clickhouse-cloud-on-azure#developer-experience)


### Azure Data Synapse [\#](/blog/a-year-of-clickhouse-cloud-on-azure#azure-data-synapse)


[Azure Synapse Analytics](https://azure.microsoft.com/en-us/products/synapse-analytics) is an integrated service that combines big data, data science, and warehousing to enable fast, large\-scale data analysis. Within Azure Synapse Analytics, you can use our ClickHouse Spark connector to create on\-demand clusters to run data transformations, machine learning, and integrations that interact with ClickHouse and your other services.


![announce4.png](/uploads/announce4_9203680606.png)
Adding the ClickHouse Spark Connector directly into your Synapse Notebook


There are multiple ways to get started: configure the connector as a default package, set it at the Spark pool level, or use it directly in a session. For details on how to get started, read the documentation on [how to add ClickHouse as a catalog](https://clickhouse.com/docs/integrations/azure-synapse).


### chDB .NET [\#](/blog/a-year-of-clickhouse-cloud-on-azure#chdb-net)


chDB, our in\-process OLAP engine powered by ClickHouse, allows users to run ClickHouse\-fast queries, embedded in your application, on local files and object storage. ischDB supports over 60\+ data formats like Parquet, Arrow, and JSON.


![announce5.png](/uploads/announce5_5e0ab31a09.png)
chDB architecture for .NET


Now, thanks to our amazing community member [Andreas Vilinski](https://github.com/vilinski), bindings now exist for [chDB in .NET](https://github.com/chdb-io/chdb-dotnet). This allows users to leverage chDB in your code with a few lines in either C\# or F\# interactive with dotnet fsi.



```

```
1using ChDb;
2
3var result = ChDb.Query("select version()");
4Console.WriteLine(result.Text);
5// 23.10.1.1
6var s = new Session();
7var result = s.Query("select * from system.formats where is_output = 1", "PrettyCompact");
8// ┌─name───────────────────────────────────────┬─is_input─┬─is_output─┬─supports_parallel_parsing─┬─supports_parallel_formatting─┐
9// │ Prometheus                                 │        0 │         1 │                         0 │                            0 │
10// │ PostgreSQLWire                             │        0 │         1 │                         0 │                            0 │
11// │ MySQLWire                                  │        0 │         1 │                         0 │                            0 │
12// │ JSONEachRowWithProgress                    │        0 │         1 │                         0 │                            0 │
13// │ ODBCDriver2                                │        0 │         1 │                         0 │                            0 │
14// ...
15var result = s.Query("DESCRIBE s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/house_parquet/house_0.parquet')");
16Console.WriteLine(result.Text);
```


```

Example of using chDB in C\#



```

```
1#r "nuget: chdb"
2
3open ChDb
4
5// print out result in the PrettyCompact format by default
6let result = ChDb.Query "select version()"
7printfn "%s" result.Text
8// or save result to a text or binary file in any supported format
9let result = ChDb.Query("select * from system.formats where is_output = 1", "CSVWithNames")
10System.IO.File.WriteAllBytes("supported_formats.csv", result.Buf)
```


```

Example of using chDB in F\# interactive


Regardless of what language you’re using, there are bindings available for [Java](https://github.com/chdb-io/chdb-java), [Go](https://github.com/chdb-io/chdb-go), [NodeJS](https://github.com/chdb-io/chdb-node), [Rust](https://github.com/chdb-io/chdb-rust), and [Ruby](https://github.com/chdb-io/chdb-ruby) that you can use within the Azure Ecosystem.


## Business intelligence [\#](/blog/a-year-of-clickhouse-cloud-on-azure#business-intelligence)


We all know the saying: “a picture paints a thousand words.” But dashboards made up of charts and visualizations make a thousand business decisions in real\-time each day. Whether its capturing user behavior and gaining insights into their usage in your application like [Microsoft Clarity](https://clarity.microsoft.com/) or building internal tools for your employees to self service dashboards like the Microsoft WebXT team use for their internal data analytics tool ([watch Satish Manivannan talk about the products](https://clickhouse.com/blog/self-service-data-analytics-for-microsofts-biggest-web-properties)), ClickHouse is chosen because of its capabilities of storing and querying the scale of data they ingest from Microsoft Edge Browser, Bing search, MSN, Microsoft Advertising and Maps.


### Power BI connector [\#](/blog/a-year-of-clickhouse-cloud-on-azure#power-bi-connector)


Power BI is one of the leading business intelligence platforms used by different types of industries and organizations all over the globe. Working closely with our partner, Microsoft, last year, we announced that ClickHouse Power BI Connector was available as an [official data source for Microsoft Power BI](https://clickhouse.com/blog/announcing-clickhouse-connector-tableau).


Our Power BI connector provides support for Power BI (Semantic models and Dataflows) along with Fabric (Dataflow Gen2\), enabling you to build and publish dashboards created from Power BI Desktop. Today, if you would like to use Power BI Service, you will need to create an [on\-premise data gateway](https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-onprem), this is really easy to set up (see How to setup [connectors with an on\-premise data gateway](https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-custom-connectors)). We’re working hard to make this experience even better and would encourage you to [upvote the Microsoft community forum post](https://community.fabric.microsoft.com/t5/Fabric-Ideas/Clickhouse-connector-in-PowerBI-Service/idi-p/4658948).


## Enterprise cloud architecture [\#](/blog/a-year-of-clickhouse-cloud-on-azure#enterprise-cloud-architecture)


Over the past year, ClickHouse Cloud on Azure introduced new [cloud architecture enhancements](https://clickhouse.com/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings) designed to improve its scalability, performance, and resilience. These included compute\-compute separation, which enables multiple compute replicas to independently scale and access shared storage for better workload isolation and parallelism. Additionally, a new "make before break" (MBB) scaling model was introduced, allowing ClickHouse to spin up new nodes before decommissioning old ones during vertical scaling—ensuring minimal query disruption. These changes significantly elevate the platform’s ability to support real\-time analytics at scale on Azure. For enterprise users, new features include scheduled upgrades and advanced disaster recovery options like cross\-region backups.


## Enterprise security [\#](/blog/a-year-of-clickhouse-cloud-on-azure#enterprise-security)


ClickHouse Cloud is built with enterprise\-grade security, including strong passwords with multi\-factor authentication, social authentication, or Single Sign\-On (SSO) for console users, configurable IP filters to restrict inbound traffic to your service, role\-based access with service\-level control, secure APIs for automation, and console\-level activity logs. Additionally, databases require strong passwords, have granular role\-based access, and provide audit logging by default. All data is encrypted at rest and in transit by default for both our console and databases.


In addition to these standard capabilities, we also support [Azure Private Link](https://azure.microsoft.com/en-us/products/private-link) for direct connectivity to your ClickHouse Cloud services, and login with your Microsoft account using Microsoft social login or SSO with [Entra ID](https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-single-sign-on).


Coming soon, we are also developing features to allow customers to securely connect to Azure blob storage using service identities, enabling transparent data encryption with customer\-managed encryption keys for ClickHouse databases on Azure and offering PCI and HIPAA compliant services.


## Azure Marketplace [\#](/blog/a-year-of-clickhouse-cloud-on-azure#azure-marketplace)


Launched on Azure in June 2024, ClickHouse Cloud has seen rapid adoption for real\-time analytics, data warehousing, and observability due to its high\-performance and seamless integration with the Azure ecosystem, including [querying](https://clickhouse.com/docs/en/sql-reference/table-functions/azureBlobStorage) Azure Blob Storage, ingesting data via [ClickPipes](https://clickhouse.com/cloud/clickpipes), and building visualizations with the Microsoft Power BI [connector](https://clickhouse.com/blog/official-microsoft-power-bi-connector).


[ClickHouse Cloud on Azure Marketplace](https://clickhouse.com/blog/clickhouse-cloud-is-now-generally-available-on-microsoft-azure) is also eligible for the Microsoft Azure Consumption Commitment (MACC) program, allowing customers to use existing Azure commitments towards ClickHouse Cloud usage. This simplifies procurement, enables utilization of pre\-committed funds, and covers 100% of ClickHouse Cloud costs with Azure MACC funds, maximizing value and cost\-effectiveness.


## Get started now [\#](/blog/a-year-of-clickhouse-cloud-on-azure#get-started-now)


As we continue to evolve ClickHouse Cloud on Azure, our focus remains on delivering the performance, flexibility, and scale that real\-time analytics teams demand. From architectural improvements like storage\-compute separation to seamless Azure service integrations, we’re committed to making it easier than ever to build fast, efficient analytics solutions in the cloud.


📍 **Come see us at Microsoft Build 2025 — Booth 415** — we'd love to connect and show you what's new.


🚀 **Ready to experience it yourself?** Start your **ClickHouse Cloud trial on Azure** today 
[directly](#) or through [Azure Marketplace](#) and get $300 free credits.


📞 **Want a deeper dive?** [Book a sales meeting or demo](#) to explore how ClickHouse Cloud can fit into your Azure architecture.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
