# What’s new in ClickHouse – 2025 roundup


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# What’s new in ClickHouse – 2025 roundup

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 20, 2026 · 21 minutes read2025 has been a transformative year for ClickHouse. We've rolled out major infrastructure improvements, expanded our global footprint, enhanced security and compliance capabilities, and introduced powerful new features that make real\-time analytics faster and easier than ever. Here's a comprehensive look at everything we shipped this year.


## **Infrastructure \& performance: Building for scale** [\#](/blog/clickhouse-2025-roundup#infrastructure--performance-building-for-scale)


**SharedCatalog: A New Foundation for Cloud\-Scale Performance**


One of the most significant architectural improvements we made was introducing SharedCatalog in July. This centralized metadata coordination system fundamentally changed how ClickHouse Cloud manages database and table metadata, delivering several critical benefits:


- Cloud\-scale DDL operations that handle high concurrency with ease
- Resilient deletion and new DDL operations
- Lightning\-fast service spin\-ups and wake\-ups, as stateless nodes now launch without disk dependencies
- Stateless compute that works seamlessly across native ClickHouse formats and open formats like Iceberg and Delta Lake


This architectural shift enables ClickHouse Cloud to scale to unprecedented levels while maintaining the performance users expect.


**Compute\-Compute separation (Warehouses)**


In January, we made Warehouses generally available, introducing true compute\-compute separation. This feature allows you to designate specific warehouses as read\-write or read\-only, giving you flexibility to optimize your architecture for both cost and performance. Whether you're running restartable ETL jobs on single\-replica services or high\-availability production workloads, Warehouses provide the control you need.


**Vertical scaling improvements**


To improve performance and reliability during scaling events, we’ve introduced Make\-Before\-Break vertical scaling. With this enhancement, new replicas come online before old ones are removed, eliminating capacity gaps during transitions. The result: faster, seamless scaling \- especially important when workloads surge and additional resources are needed in real time.


**Single\-replica services**


Single\-replica services arrived for test workloads and non\-HA scenarios within warehouses, providing cost\-effective options for development and ETL use cases.


**Horizontal scaling (GA)**


Manual horizontal scaling has reached general availability, enabling users to scale workloads up to 20 replicas for increased parallelization. When demand subsides, services can scale back down to fewer replicas, giving teams full control to right\-size capacity as needed.


**Graviton**


We upgraded the fleet to ARM architecture. We have seen significant performance gains and overall efficiency with the new architecture. Read more about the migration and performance comparisons [here](https://clickhouse.com/blog/graviton-boosts-clickhouse-cloud-performance%20).


## **Global expansion: ClickHouse everywhere** [\#](/blog/clickhouse-2025-roundup#global-expansion-clickhouse-everywhere)


We significantly expanded our global presence in 2025, adding support for multiple new regions:


- **AWS**: Israel (Tel Aviv), Seoul (Asia Pacific), and Middle East (UAE)
- **GCP**: Japan (asia\-northeast1\)
- **Azure**: UAE North (private region)


These additions bring ClickHouse Cloud closer to users around the world, reducing latency and enabling compliance with local data residency requirements.


**Bring Your Own Cloud (BYOC) for AWS now generally available**


ClickHouse Cloud now supports [**Bring Your Own Cloud (BYOC) on AWS**](https://clickhouse.com/cloud/bring-your-own-cloud), enabling customers to deploy a fully managed ClickHouse service directly within their own VPC. This model delivers the best of both worlds: the operational simplicity of a managed cloud service combined with the security, compliance, and isolation of your own AWS environment. BYOC for AWS is designed for organizations with strict data residency, security, and compliance requirements, providing full control over data, access policies, and cloud infrastructure without the burden of managing ClickHouse yourself.


## **Developer Experience: Making analytics easier** [\#](/blog/clickhouse-2025-roundup#developer-experience-making-analytics-easier)


We spent a lot of time focusing on end\-to\-end developer and user experiences this past year. From Terraform provider improvements to brand new in\-console dashboarding capabilities, we continue to lower the barrier of entry and expand the ways our community can use ClickHouse.


**Terraform Provider Enhancements**


Our [ClickHouse Cloud Terraform provider](https://registry.terraform.io/providers/ClickHouse/clickhouse/latest) now supports the ability to add tags to services making it easier to organize services by team, project, environment, or other use cases.


In addition, our new [Clickhouse Database Operations provider](https://registry.terraform.io/providers/ClickHouse/clickhousedbops/latest) reached 64k downloads! This database operations provider allows you to manage database users, roles, and privileges as code, compatible with both cloud and self\-managed deployments. This provider also now supports configuring additional database user settings, giving you greater control over how users interact with and consume database resources.


**Query API Endpoints (GA)**


Query Endpoints reached general availability, allowing you to turn saved SQL queries into RESTful API endpoints with just a few clicks. Endpoint latency has been reduced, with significant improvements to cold starts. Result streaming and support for all ClickHouse compatible outputs expand the ways you can leverage query endpoints. They’re also much more secure with GA – with new enhanced RBAC controls, configurable CORs domain and the ability to safely execute arbitrary SQL.


**SQL console improvements**


SQL console continues to evolve for all your in\-console querying needs. You can now share your queries with teammates in your organization with more granular permissions. Understanding why your queries are performing poorly got much better with Query Insights, making it easier to optimize and debug your queries. In addition to insights, the number of visualizations you can create from a query continues to grow with the latest addition being heatmap charts.


**Dashboards**


To date, ClickHouse seamlessly integrates with your favorite business intelligence and visualization tools. This year, visualizations available from saved queries have been extended and native dashboarding capabilities were introduced. You can create, organize and share your visualizations with dashboards with all of the visualization types already available through saved queries.


## **AI\-powered features \& The Agentic Data Stack** [\#](/blog/clickhouse-2025-roundup#ai-powered-features--the-agentic-data-stack)


2025 was a big year for our AI story. We’ve added a number of new features to augment your ClickHouse experience and introduced a new open\-source, composible stack for agentic analytics.


**SQL autocomplete \& Ask AI**


SQL console now has AI\-powered autocomplete workflows embedded in the query experience. It helps fix incorrect or broken queries and also offers optimization suggestions based on your schema. Not sure where to start with SQL? You can also generate SQL from natural language.


Taking this concept even further, this is now a co\-pilot like experience in the Cloud console called Ask AI. Here you can interact with your data just by chatting with it. From generating SQL queries, engaging with our knowledge base and documentation to generating charts and doing a deeper analysis.


**ClickHouse MCP Server**


One of our fastest growing ways to integrate with ClickHouse is our [MCP server](https://github.com/ClickHouse/mcp-clickhouse/issues). In fact, we leverage it in house to provide our Ask AI experience. It’s been exciting to see our community build new innovative applications, agentic and analytical workflows leveraging this integration point. Our MCP is entirely open\-source and open for requests and contributions.


**The Agentic Data Stack**


With the acquisition of LibreStack, we now recommend the [agentic data stack](https://clickhouse.com/blog/librechat-open-source-agentic-data-stack) as the best way to build agentic analytics applications and workflows with ClickHouse. With this technology stack you can easily embed [AgentHouse](https://llm.clickhouse.com/) experiences into your own applications, expanding adoption of your data and the value it provides.


## **ClickStack** [\#](/blog/clickhouse-2025-roundup#clickstack)


ClickHouse’s high\-performance engine enables real\-time observability at massive scale. Innovative companies like [OpenAI](https://clickhouse.com/blog/why-openai-uses-clickhouse-for-petabyte-scale-observability), and [Netflix](https://clickhouse.com/blog/netflix-petabyte-scale-logging) choose ClickHouse for Observability at unprecedented scale.



This year marked a major milestone for observability at ClickHouse with the launch and rapid evolution of ClickStack, the open source observability stack for OpenTelemetry at scale, built natively on ClickHouse. ClickStack brings logs, traces, metrics, and session replay together into a single, high\-performance platform designed for scale, cost efficiency, and deep exploratory analysis.


Since its launch, ClickStack has matured quickly with steady improvements across ingestion, querying, and user experience, making it easier to run observability workloads directly alongside your analytical data.


Key highlights include:


- A unified data model for logs, traces, metrics, and sessions, enabling fast cross\-signal correlation without data silos
- Native ClickHouse storage and query execution optimized for high\-cardinality telemetry, with performance enhancements like native JSON support, time\-window query prioritization, and intelligent use of Materialized Views to keep queries fast at scale
- Tight integration with ClickHouse Cloud, allowing teams to analyze observability and business data together in one platform
- Continuous UI and workflow enhancements in the HyperDX interface, including service maps, improved trace exploration, and faster dashboards
- Built\-in alerting and visualization capabilities to support day\-to\-day operational monitoring and incident response


ClickStack reflects our broader approach to observability: treating telemetry as analytical data first, and giving teams the performance and flexibility they need to explore it without tradeoffs.


Check out ClickStack's full 2025 story in this half\-year recap [here](https://clickhouse.com/blog/clickstack-a-year-in-review-2025).


## **Security \& compliance: Enterprise\-grade protection** [\#](/blog/clickhouse-2025-roundup#security--compliance-enterprise-grade-protection)


The company size, scale, and needs of our customers continues to grow and we continue to invest in the features, compliance and security needs to meet them where they are. In 2025 we made some big investments to help our enterprise customers be more successful with ClickHouse.


**New Enterprise Tier**


A dedicated Enterprise tier was introduced, designed to meet the most demanding workloads and organizational requirements. This new tier provides industry\-specific security and compliance features, advanced controls over hardware configurations and upgrade schedules, and enhanced disaster recovery capabilities for mission\-critical deployments. Enterprise customers can also leverage slow\-release channels to defer upgrades and thoroughly test new versions before rolling them out to production.


**HIPAA and PCI Compliance**


ClickHouse Cloud has expanded its compliance offerings to support organizations in regulated industries. We now offer HIPAA\-compliant services across multiple regions on both AWS and GCP, with services requiring a Business Associate Agreement to ensure proper handling of protected health information. For Enterprise customers processing payment card data, PCI compliance is available in select AWS regions.


**Security enhancements**


We've significantly strengthened our security capabilities with several key enhancements. Enterprise customers can now set up SAML SSO through a self\-service interface, while support for Customer Managed Encryption Keys (CMEK) has been extended to GCP, alongside our existing AWS offering. Transparent Data Encryption (TDE) is now available for both AWS and GCP deployments and introduced API key IP filters to restrict access to specific network locations.


**Access control improvements**


Our role\-based access control system has been refined to provide more granular permission management. New roles include Member, Service Admin, and Service Read Only for delegating operational responsibilities, and a dedicated Billing role. In addition to existing permissions, this new level of granularity allows organizations to grant the appropriate access levels to different practitioners. Enterprise customers gained the ability to set up SAML SSO which allows users to select a default role for newly assigned SAML users and configure custom session timeout settings.


## **Data integration: Connecting your data** [\#](/blog/clickhouse-2025-roundup#data-integration-connecting-your-data)


In 2025 we introduced a number of ways to ingest, build and interact with your data. From new CDC ClickPipes to official language clients for real\-time applications, the ClickHouse ecosystem continues to evolve and expand.


**ClickPipes Expansions**


ClickPipes, our managed data ingestion service, saw major growth in both adoption and new data sources in 2025\.


- **MySQL CDC**: new connector for continuous replication from MySQL and MariaDB for real\-time analytics
- **MongoDB CDC**: new connector for continuous replication from MongoDB for real\-time analytics
- **Postgres CDC**: improved performance and support for new Postgres features like failover replication slots
- **Amazon Kinesis**: support for real\-time ingestion from Amazon Kinesis Data Streams
- **Azure Blob Storage**: one\-time and continuous ingestion from ABS containers for data lake analytics


**ClickPipe enhancements**


In addition to these new sources, there have been plenty of noteworthy improvements to our ClickPipes offering. We enhanced ClickPipes observability with new [in\-console monitoring dashboards](https://clickhouse.com/blog/clickpipes-flexible-scaling-monitoring) and Prometheus metrics reporting. ClickPipes management is now simpler at scale via Open API and Terraform support, providing better integration with existing developer workflows and making operations like pipe scaling self\-service.


To support secure enterprise deployments, [AWS PrivateLink](https://clickhouse.com/docs/integrations/clickpipes/aws-privatelink) connectivity is now available with cross\-region support and SSH tunneling for private network connections. Still on the security side, we expanded authentication options to include IAM for AWS\-based services, as well as custom certificates for Kafka ClickPipes. For S3 ClickPipes, we added [unordered mode](https://clickhouse.com/blog/clickpipes-s3-unordered-mode) to allow for more flexible file ingestion patterns. This year, we plan to extend many of these features to other cloud providers, with support for native authentication and private networking options also for GCP and Azure in the roadmap.


**Connector ecosystem**


Outside of our managed ClickPipes service, we invested in a number of connectors and tooling for ingestion, analysis, and development.


To better support our Spark community, we've expanded our integration capabilities. An official [AWS Glue connector](https://clickhouse.com/docs/integrations/glue) is now available on the AWS Marketplace, making it easier to build data pipelines in AWS environments. Support for Spark 4\.0 and full Databricks compatibility were added, making it easier to integrate with the latest Spark ecosystem tools.


We expanded our support for managed data pipelines with two new integrations. Our [Fivetran connector](https://clickhouse.com/docs/integrations/fivetran) is now beta, providing access to over 500 data sources and support for history mode. For GCP\-heavy organizations, the [Google Dataflow template](https://clickhouse.com/docs/integrations/google-dataflow/dataflow) makes it easy to replicate BigQuery data to ClickHouse. For our Azure\-invested customers, it is now much easier to integrate with [Azure Data Factory](https://clickhouse.com/docs/integrations/azure-data-factory/table-function) through Azure Data Lake and Blob Storage.


Our streaming options have received several important updates. We introduced an official [Apache Flink connector](https://github.com/ClickHouse/flink-connector-clickhouse) for large\-scale, real\-time data processing workflows. Partnering with Confluent, we've launched a managed version of the [ClickHouse Kafka sink](https://docs.confluent.io/cloud/current/connectors/cc-clickhouse-sink-connector/cc-clickhouse-sink.html) on Confluent Cloud, making it easier to push data to ClickHouse from existing pipelines and added additional metrics for measuring performance to [clickhouse\-kafka\-connect](https://clickhouse.com/docs/integrations/kafka/clickhouse-kafka-connect-sink#monitoring).


We continue to invest in data visualization tools for analysis of your ClickHouse data. Earlier in 2025, native support was added for [Tableau Desktop](https://clickhouse.com/docs/integrations/tableau) and [Tableau Online](https://clickhouse.com/docs/integrations/tableau-online).


**Language clients**


Outside of our Cloud Console, the most popular way to interact with ClickHouse is through our language clients. We've expanded our list of official [language clients](https://clickhouse.com/docs/integrations/language-clients) to better serve our growing developer community. Rust developers can now use [clickhouse\-rs](https://github.com/ClickHouse/clickhouse-rs), while C\# and .NET developers now have [clickhouse\-cs](https://github.com/ClickHouse/clickhouse-cs) for easier integration into Microsoft\-based technology stacks.


Our official Python client, [clickhouse\-connect](https://github.com/ClickHouse/clickhouse-connect/), has been enhanced with support for Pandas 2\.0 and Polars for high\-performance DataFrame operations. The [clickhouse\-odbc](https://github.com/ClickHouse/clickhouse-odbc/) received an upgrade with a new network stack for better performance, enhanced support for ClickHouse data types, and an improved experience for downstream tools like PowerBI.


## **Monitoring \& observability** [\#](/blog/clickhouse-2025-roundup#monitoring--observability)


We take a pragmatic approach to observability in ClickHouse Cloud, providing comprehensive built\-in dashboards and alerts for users who need them, while making it easy to integrate with existing monitoring stacks for those who prefer their own tools.


Let's start with what's new in the built\-in experience.


**Service Monitoring Enhancements**


ClickHouse Cloud introduced several monitoring enhancements in 2025 to help users understand query performance and system health.


The Advanced Observability Dashboard was introduced in November 2024, providing comprehensive system health monitoring through built\-in visualizations accessible in the ClickHouse Cloud console. Throughout 2025, we enhanced the underlying metrics that power it, adding histogram\-based latency tracking (25\.4\), ZooKeeper operation statistics (25\.10\), and automated CPU/memory alerts (25\.10\). In October, the dashboard's metric displays were improved to show maximum utilization rather than averages, better surfacing underprovisioning issues.


The Resource Utilization Dashboard was introduced in May 2025 and delivers granular visibility into CPU, memory, and data transfer consumption.


Query insights is a tool that gives ClickHouse Cloud users a turnkey way to view and interpret the query log. It was released in July 2024, and in 2025, we enhanced it with script\-level query tracking (showing exact line numbers where queries originate), detailed UDF usage tracking in the query log for better visibility into custom function performance, and filter/index operation visibility to pinpoint performance bottlenecks.


**Notifications**


We expanded our Cloud notification system with Slack integration, bringing the total supported channels to three (Slack, in\-console, and email) for billing events, scaling operations, service version upgrades, and ClickPipes monitoring.


ClickPipes notifications include automatic failure alerts with self\-serve recovery steps, as well as configurable replication slot threshold warnings for Postgres CDC. Additionally, per\-replica CPU and memory utilization metrics (July 2025\) help users understand workloads and plan resizing operations.


Organization admins can customize notification delivery through a centralized notification center with service\-level category and severity controls.


**Prometheus Endpoint \& Mixin**


We released the Prometheus API endpoint to GA with organization\-level metrics federation that automatically aggregates data from all services and supports filtered metric collection to optimize payload size. The endpoint supports histogram and multi\-dimensional metrics for advanced latency tracking and failure analysis, with filtered metric collection to optimize payload size.


Our [official Prometheus/Grafana mix\-in](https://clickhouse.com/blog/monitor-with-new-prometheus-grafana-mix-in) (May 2025\) provides the same internal dashboards that their engineering teams use to monitor cloud instances, available for import from grafana.com or GitHub with a simple scrape config setup.


## **Backup \& recovery** [\#](/blog/clickhouse-2025-roundup#backup--recovery)


We reached general availability with several backup capabilities.


With Configurable Backups, customers can now configure backup policies based on frequency, retention, and schedule. The new External Backups feature goes further, allowing backups to be exported directly to your organization’s own cloud storage \- supporting AWS S3, Google Cloud Storage, and Azure Blob Storage. This means you can bring your own compliance and security to backup operations.


Backup processes are now up to 6x faster. These deliverables reflect months of collaboration between our engineering and product teams, focused on building a backup experience that’s both flexible and performant.


## **Database updates \& new features** [\#](/blog/clickhouse-2025-roundup#database-updates--new-features)


ClickHouse releases a new open\-source version monthly. This steady cadence allows us to ship database improvements incrementally. New features typically start behind settings flags for early adopters, then graduate to default once they've proven stable in production. What might take years in traditional release cycles happens in months here.



> You can see release posts for every release via the links below:  
> 
> [25\.1](https://clickhouse.com/blog/clickhouse-release-25-01), [25\.2](https://clickhouse.com/blog/clickhouse-release-25-02), [25\.3 LTS](https://clickhouse.com/blog/clickhouse-release-25-03), [25\.4](https://clickhouse.com/blog/clickhouse-release-25-04), [25\.5](https://clickhouse.com/blog/clickhouse-release-25-05), [25\.6](https://clickhouse.com/blog/clickhouse-release-25-06), [25\.7](https://clickhouse.com/blog/clickhouse-release-25-07), [25\.8 LTS](https://clickhouse.com/blog/clickhouse-release-25-08), [25\.9](https://clickhouse.com/blog/clickhouse-release-25-09), [25\.10](https://clickhouse.com/blog/clickhouse-release-25-10), [25\.11](https://clickhouse.com/blog/clickhouse-release-25-11), [25\.12](https://clickhouse.com/blog/clickhouse-release-25-12)


Each release includes improvements across the database. Rather than catalog every change, we've highlighted three key areas where ClickHouse made significant strides in 2025: expanding search capabilities to handle modern AI and text workloads, delivering breakthrough performance optimizations, and deepening integration with data lake ecosystems.


**Modern search capabilities**


[Vector similarity search](https://clickhouse.com/docs/engines/table-engines/mergetree-family/annindexes) reached general availability in 25\.8 with production\-ready features including binary quantization, which significantly reduces memory consumption and accelerates index building, alongside lower query latency through reduced storage reads and CPU usage. In 25\.10, ClickHouse introduced the QBit data type for vector embeddings, enabling runtime tuning of search precision.


[Full\-text search](https://clickhouse.com/blog/clickhouse-full-text-search) in ClickHouse underwent significant evolution across the 25\.x releases, culminating in a complete redesign of the inverted index in 25\.10 that enables handling datasets that don't fit in RAM. This release also brought faster index building for documents with mostly infrequent tokens, and the text index now supports Array and Map values in addition to String columns.


**Apache Iceberg and data lakes**


Apache Iceberg support evolved from read\-only to a fully bidirectional integration throughout the 25\.x releases. ClickHouse 25\.8 introduced write operations, enabling `INSERT` into existing Iceberg tables, along with positional and equality delete handling for proper delete semantics. The integration added schema evolution for complex types and `ALTER DELETE` mutations. In 25\.10, `ALTER UPDATE` support and distributed write operations completed the read/write parity.


Delta Lake now supports `INSERT` operations on existing Delta Lake tables. Additionally, the new `system.delta_lake_metadata_log` system table provides visibility into Delta Lake metadata files, helping troubleshoot integration issues.


[Microsoft OneLake](https://clickhouse.com/blog/clickhouse-integrates-with-microsoft-onelake) integration brings native support for querying Iceberg tables in Microsoft Fabric's OneLake, enabling unified analytics across enterprise data sources without data movement. ClickHouse 25\.10 also introduced support for Apache Paimon, expanding compatibility to this emerging open table format.


**Query performance and optimization**


[Lazy materialization](https://clickhouse.com/blog/clickhouse-gets-lazier-and-faster-introducing-lazy-materialization) (25\.4\) defers reading column data until actually needed, dramatically reducing I/O and memory usage. Instead of eagerly loading all columns upfront, ClickHouse now tracks which data should be read and materializes it only when the query requires it.


[Lightweight UPDATE operations](https://clickhouse.com/blog/clickhouse-gets-lazier-and-faster-introducing-lazy-materialization) change how ClickHouse handles updates by using a "patch\-part" mechanism that writes only modified values, plus targeting metadata to small patch parts, rather than rewriting entire columns like traditional mutations.


## **Looking ahead** [\#](/blog/clickhouse-2025-roundup#looking-ahead)


2025 was a year of massive growth and innovation for ClickHouse, including foundational infrastructure improvements like SharedCatalog, new capabilities such as Warehouses, and comprehensive security features. This progress has resulted in a database and platform that scales for the most demanding real\-time analytics.


Heading into 2026, we will maintain this momentum by expanding our global reach, deepening our ecosystem, and pushing the boundaries of real\-time analytics. This trajectory is supported by our recent [Series D funding](https://clickhouse.com/blog/clickhouse-raises-400-million-series-d-acquires-langfuse-launches-postgres) round and strategic investments to LLM observability through our recent acquisition of Langfuse and an [NVMe based Postgres service](https://clickhouse.com/cloud/postgres) for real\-time applications.

### Want to see our progress?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-39-want-to-see-our-progress-sign-up&utm_blogctaid=39)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
