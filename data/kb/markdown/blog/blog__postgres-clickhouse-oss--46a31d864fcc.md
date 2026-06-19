# PostgreSQL \+ ClickHouse as the Open Source unified data stack


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# PostgreSQL \+ ClickHouse as the Open Source unified data stack

![](/_next/image?url=%2Fuploads%2Flio_headshot_singapore_7cc9852011.jpg&w=96&q=75)[Lionel Palacin](/authors/lionel-palacin)Jan 27, 2026 · 8 minutes readWe [recently launched a managed service that brings PostgreSQL and ClickHouse](https://clickhouse.com/blog/postgres-managed-by-clickhouse) together as a single, unified data stack. The goal is simple: let teams run transactional and analytical workloads side by side without stitching together multiple systems or maintaining complex pipelines. This launch reflects a pattern we have seen repeatedly in production. PostgreSQL remains the system of record, while ClickHouse handles analytics at scale.



> Start with PostgreSQL, scale with ClickHouse.


In this post, we step back from the managed service and focus on its open source foundations. We show how to build the same unified data stack using open source components, how the integration works in practice, and how to offload analytics to ClickHouse without rewriting applications or rebuilding pipelines.



## Introducing an open source data stack [\#](/blog/postgres-clickhouse-oss#introducing-an-open-source-data-stack)


The Open Source unified data stack, [available on Github](https://github.com/ClickHouse/postgres-clickhouse-stack), is simple and built on top of four open source components:


- [Postgres](https://github.com/postgres/postgres) is the primary database of the data stack acting as the system of records and handling all transactional workload.
- [ClickHouse](https://github.com/ClickHouse/ClickHouse) is a purpose\-built open source analytical database of the data stack. As data volume grows, this is the preferred database to handle analytical workload.
- [PeerDB](https://github.com/PeerDB-io/peerdb) is an open source tool to stream data from PostgreSQL to Data warehouse, including ClickHouse. It uses change data capture (CDC) to replicate inserts, updates, and deletes into ClickHouse in near real\-time.
- [pg\_clickhouse](https://github.com/ClickHouse/pg_clickhouse) is an open source postgres extension that runs analytics queries on ClickHouse directly from PostgreSQL without rewriting any SQL.


These four components come together to form the open source unified data stack. Below is a high\-level overview of the stack.


![postgres-oss-diagram-1.jpg](/uploads/postgres_oss_diagram_1_e72845a9a9.jpg)
### Implementing the stack  [\#](/blog/postgres-clickhouse-oss#implementing-the-stack)


Running PostgreSQL and ClickHouse side by side is a well established pattern. Many teams use this architecture in production, and GitLab [described it publicly](https://about.gitlab.com/blog/two-sizes-fit-most-postgresql-and-clickhouse/) as early as 2022\. Depending on the workload, the implementation falls into two main patterns, Change data capture or split\-writes.


#### Change data capture (CDC) [\#](/blog/postgres-clickhouse-oss#change-data-capture-cdc)


**Components**: Postgres, ClickHouse, PeerDB and pg\_clickhouse (optional).


This approach is well suited for operational, real\-time analytical workloads where analytics run directly on application data. Common use cases include retail platforms, financial systems, and CSM or CRM applications.


PostgreSQL remains the system of record. All writes go to PostgreSQL, while PeerDB streams inserts, updates, and deletes into ClickHouse using CDC. ClickHouse maintains a near real\-time copy of the data, allowing analytical queries to run on the latest state without adding additional load to the transactional database.


Applications can continue to send both transactional and analytical queries to PostgreSQL thanks to pg\_clickhouse which transparently offloads analytical queries to ClickHouse. This keeps application changes minimal. Alternatively, applications can query ClickHouse directly if needed.


**Customer examples**: [Seemplicity](https://clickhouse.com/blog/seemplicity-scaled-real-time-security-analytics-with-postgres-cdc-and-clickhouse), [Sewer AI](https://clickhouse.com/blog/sewerai-sewer-management-at-scale)


![postgres-oss-diagram-2.jpg](/uploads/postgres_oss_diagram_2_9a4ab8724a.jpg)
### Split\-writes [\#](/blog/postgres-clickhouse-oss#split-writes)


**Components**: PostgreSQL, ClickHouse, and pg\_clickhouse (optional).


This pattern is commonly used for observability or event\-based workloads, where analytical data consists of logs, metrics, or events. These datasets do not require transaction support and are written at high volume.


In this case, analytical data can be written directly to ClickHouse, or routed through PostgreSQL using pg\_clickhouse when minimal application change is preferred. PostgreSQL is not the system of record for this data and does not need to store the full analytical dataset.


Querying follows the same model as the CDC approach. Analytical queries run on ClickHouse, either transparently offloaded from PostgreSQL via pg\_clickhouse or issued directly to ClickHouse.


**Customer examples**: [Langfuse](https://clickhouse.com/blog/langfuse-and-clickhouse-a-new-data-stack-for-modern-llm-applications), [Langchain](https://clickhouse.com/blog/langchain-why-we-choose-clickhouse-to-power-langchain)


![postgre-oss-diagram-3.jpg](/uploads/postgre_oss_diagram_3_4452977ed6.jpg)
## Get started locally [\#](/blog/postgres-clickhouse-oss#get-started-locally)


Whether you're implementing a new application or extending an existing PostgreSQL application, getting started locally is straightforward. The [Getting started guide](https://github.com/ClickHouse/postgres-clickhouse-stack?tab=readme-ov-file#getting-started) explains how to run the stack locally. Once you have it running locally, you can simply connect your application to the [exposed PostgreSQL database instance](https://github.com/ClickHouse/postgres-clickhouse-stack?tab=readme-ov-file#connect-to-postgresql).


At that point, it is no different than running it with your own PostgreSQL instance. You might stop here while your application is running just fine on PostgreSQL only. Then once you need to improve the analytical workload performance, it is very simple to do:


1. [Create a database in ClickHouse](https://github.com/ClickHouse/postgres-clickhouse-stack?tab=readme-ov-file#create-the-clickhouse-database) for replicated tables.
2. [Replicate data](https://github.com/ClickHouse/postgres-clickhouse-stack?tab=readme-ov-file#replicate-data-from-postgresql-to-clickhouse) from PostgreSQL using PeerDB.
3. [Configure](https://github.com/ClickHouse/postgres-clickhouse-stack?tab=readme-ov-file#configure-clickhouse-foreign-data-wrapper) the pg\_clickhouse extension.
4. Direct queries to the pg\_clickhouse tables via  your [PostgreSQL connection string](https://github.com/ClickHouse/postgres-clickhouse-stack?tab=readme-ov-file#configure-application-to-use-clickhouse-for-analytical-queries).


The application still relies on PostgreSQL as the primary database, making the required changes to the application code very minimal, just a new connection option. Note that you can also connect your application [directly to ClickHouse](https://github.com/ClickHouse/postgres-clickhouse-stack?tab=readme-ov-file#connect-directly-to-clickhouse) if that works better for you.


The project provides an [end to end example](https://github.com/ClickHouse/postgres-clickhouse-stack?tab=readme-ov-file#sample-application) with a sample application that initially runs the entire workload in PostgreSQL. A script migrates the analytical workload in just a few steps.


## When to start with the stack [\#](/blog/postgres-clickhouse-oss#when-to-start-with-the-stack)


Starting with this setup makes sense when:


- PostgreSQL is your primary database
- Analytical queries are part of the product, not just offline reporting
- You expect data volume or query complexity to grow


As growth timelines shrink, waiting to "outgrow" PostgreSQL often means reacting under pressure. Starting with PostgreSQL and ClickHouse together avoids a disruptive transition. But even if you adopt the stack later, PostgreSQL remains the main interface, keeping changes contained.


## From open source to production\-ready [\#](/blog/postgres-clickhouse-oss#from-open-source-to-production-ready)


The open source data stack provides a strong foundation, but many production environments require managed services with clear operational boundaries and predictable behavior. Running and upgrading databases, operating replication pipelines, and handling failures often become the limiting factors rather than the architecture itself.


We recently [launched a managed version of the unified data stack](https://clickhouse.com/blog/postgres-managed-by-clickhouse) that delivers the same architecture as a single, integrated experience under one ClickHouse Cloud account.


Deployment, scaling, upgrades, and reliability are handled by the platform, removing the need to operate clusters or data pipelines manually. PostgreSQL by ClickHouse connects directly to ClickHouse through [ClickPipes](https://clickhouse.com/cloud/clickpipes), the managed alternative to PeerDB. Managed PostgreSQL also comes with the pg\_clickhouse extension preinstalled and configured, allowing analytical queries to be offloaded to ClickHouse without rewriting applications.

### Get started with our native Postgres Service

To try ClickHouse's native Postgres service, sign up for Private Preview using this link.

[Sign up](https://clickhouse.com/cloud/postgres?loc=blog-cta-44-get-started-with-our-native-postgres-service-sign-up&utm_blogctaid=44)## A new baseline [\#](/blog/postgres-clickhouse-oss#a-new-baseline)


PostgreSQL and ClickHouse are not competing databases. They are complementary systems designed for different workloads.


With mature CDC and query offload tooling, using both from the start no longer requires complex pipelines or duplicated application logic. PostgreSQL remains the system of record for transactions, while ClickHouse handles analytical queries efficiently as data volume and query complexity grow.


**The default open data stack is no longer a single database. It is PostgreSQL for transactions, ClickHouse for analytics, and a clean, well\-defined bridge between the two.**

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
