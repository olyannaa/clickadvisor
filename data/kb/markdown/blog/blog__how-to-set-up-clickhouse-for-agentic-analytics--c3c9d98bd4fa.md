# How to set up ClickHouse for agentic analytics


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How to set up ClickHouse for agentic analytics

![](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U0_A0_NDKA_733_20c6d25c254b_512_4fefb1f6af.png&w=96&q=75)[Amy Chen](/authors/amy-chen)Feb 23, 2026 · 11 minutes readI started at ClickHouse in December, and I want to tell you about one of my favorite coworkers.


They know what was discussed in Slack. They know which dbt model to query for warehouse adoption. They don’t judge me for asking basic questions like “what’s the difference between control plane and data plane?”


Honestly, they’ll even Google things for me when I’m too lazy.


But they are not perfect.


Sometimes, if they don’t have full context, they will confidently tell me something completely wrong. They have a habit of confusing correlation with causation. Sometimes, they run very expensive queries unnecessarily.


Their name is [DWAINE (Data Warehouse AI Natural Expert)](https://clickhouse.com/blog/ai-first-data-warehouse) and they’re one of our internal AI agents.

### Join the webinar

Join our data warehousing webinar series starting on February 25th on how to transform and serve up your data for data warehousing.
[Register here](https://clickhouse.com/company/events/202602-AMER-data-warehousing-Level2?loc=blog-cta-72-join-the-webinar-register-here&utm_blogctaid=72)## How AI has changed the interface of business analytics [\#](/blog/how-to-set-up-clickhouse-for-agentic-analytics#how-ai-has-changed-the-interface-of-business-analytics)


You probably know a DWAINE too. When an AI agent goes off the rails, it’s not always because the model is dumb.


It could be because:


- It queried raw data rather than curated data.
- It finds five definitions of “revenue.”
- It scanned 3TB because it can.
- It’s competing against other processes for resources and timed out.


Conversational and [agentic analytics](https://clickhouse.com/blog/agent-facing-analytics) have changed the warehouse contract. Stakeholders are skipping dashboards and asking chatbots directly: “What was net revenue in EMEA last quarter?”


If your warehouse wasn’t designed for these new experiences, your AI Agent will show the consequences.


## Data Warehouses now power agents [\#](/blog/how-to-set-up-clickhouse-for-agentic-analytics#data-warehouses-now-power-agents)


What’s interesting is that many of the core tenets of data warehousing haven’t changed. What has changed is *why* they matter.


For dashboarding, stakeholders see answers to existing questions through dashboards that have been curated by a human. Someone who understands the context of the business, and has been setting up your dashboards for years.


With AI agents, stakeholders get free rein to choose their own questions, and the warehouse answers directly. Poor warehouse design now can result in confident misinformation given to stakeholders who assume it is trustworthy.


If your warehouse is going to power conversational analytics, you need to keep the core tenets:


- **Isolate workloads by compute resources, not by duplicating data.** AI queries, dashboards, ingestion, and transformations should not fight over the same machines.
- **Expose only curated data marts to AI.** The model should see stable, canonical definitions. Do not expose raw tables and competing metric logic.
- **Enforce guardrails early and at multiple levels.** Role\-level permissions, resource limits, and schema discipline prevent PII leaks and runaway queries.
- **Optimize for both low latency and accuracy.** No one wants to watch an LLM “think.” And no one wants it to be confidently wrong.


I’m going to give a high\-level overview of how you could set up ClickHouse with these guidelines in mind.


## Understanding the architecture [\#](/blog/how-to-set-up-clickhouse-for-agentic-analytics#understanding-the-architecture)


Open source ClickHouse runs as a single system where storage and compute are tightly coupled. The same machines store your data and run your queries. In ClickHouse Cloud, those responsibilities are separate:


- Storage lives in object storage.
- Compute runs on dedicated CPU and memory clusters, called **services**.


Even though storage and compute are separated under the hood, it still feels like you’re working with one database.


ClickHouse Cloud goes a step further still. Instead of having just one compute cluster, you can create multiple services that all access the same shared storage. This allows you to dedicate resources to specific workloads without having to duplicate data. A group of services is a **warehouse**.


![Architecture diagram](/uploads/diagrams_for_Data_warehousing_Blog_1396_d4f42d12d8.jpg)
In Data Warehousing, it’s important to have separate services for different workloads to ensure you have the right\-sized machines for each workload, controlling both cost and performance. For instance, dashboards and ad hoc queries will likely need smaller compute resources than cleaning up a dataset where you’re iterating over massive data volumes.


For sensitive data, such as PII or separate customer datasets, you may want to use multiple warehouses to isolate it. You can still access that data from another warehouse via the [remote function](https://clickhouse.com/docs/sql-reference/table-functions/remote). But when starting out \- we recommend keeping it simple, start out with one warehouse.


The ClickHouse Cloud warehouse design also supports two different types of services: **read/write** and **read\-only.** While both can read the data, **only a read/write service can write to ClickHouse**. A read\-only service can still export data externally through a table function but can’t change data in ClickHouse. One special concept in warehouses is the primary (also called parent) service. This is the first service you create for the warehouse and will define some key default settings, such as the release channel (how quickly you will be upgraded to ClickHouse versions) and region (all services in a warehouse share the same region), for all subsequent services.


### Set up your Warehouse \& Services [\#](/blog/how-to-set-up-clickhouse-for-agentic-analytics#set-up-your-warehouse--services)


To start out, create four services. You can create them either in the UI or via the API.


- Ingestion Service (Read/Write): For running ingestion pipelines via ClickPipes or self\-managed.
- Transformation Service (Read/Write): For transformation workloads and pipelines
- LLM Service (Read Only): For dashboarding and LLMs
- Development Service (Read/Write): For developers to develop and sandbox with.


![Set up your services](/uploads/diagrams_for_Data_warehousing_Blog_1396_1_43fdcd2ac3.jpg)
When creating the services, we recommend setting these settings:


- Auto\-idling (on all services, including Primary)
- Auto\-scaling
- Backups (for production Services)
- Turn on Gen AI for access to the latest AI features


### Logical schema design [\#](/blog/how-to-set-up-clickhouse-for-agentic-analytics#logical-schema-design)


Now that you have your warehouse, you will want to organize your data for ease of discovery for both humans and machines.


Structure your data into separate databases. ClickHouse supports a two\-part namespace: \<*database\_name*\>.\<*object\_name*\>.


Pick a structure that makes discovery easier based on how your team(s) communicate. A common model is using dimensional or medallion architecture. As an example to guide us through this blog, we will use lightweight dimensional modeling.


- Raw (Ingestion layer)
- Staging (Cleaned and standardized)
- Marts (Curated, aggregated, AI\-ready)



```

```
1create database raw;
2create database staging;
3create database marts;
```

```

For development, you can either create a sandbox database for developers to share or a database per developer. Shared is great for collaboration, especially if you’re iterating together over the same objects, while developer\-specific allows isolation and prevents surprises. For this blog, we will follow through with a developer\-specific database for sandboxing.



```

```
1create database dev_sandbox_achen;
```

```

## Access control [\#](/blog/how-to-set-up-clickhouse-for-agentic-analytics#access-control)


Since all the databases you just created are accessible to all the services you created, you’ll need to set up access controls to implement guardrails.


### Create roles and grant access [\#](/blog/how-to-set-up-clickhouse-for-agentic-analytics#create-roles-and-grant-access)


Create roles to group together different permissions, such as table access. We recommend starting out with at least:


- Developer (able to read from Raw and create/modify in Staging \& Marts databases)
- LLM (able to query only the Marts database tables and views)
- *(optional)* Service\_Role (similar to Developer, for automated processes like orchestration)


Here is some sample SQL to get you started:



```

```
1/* Developer Role Creation & Permissioning */
2create role if not exists developer_role;
3grant select on raw.* to developer_role;
4grant select, insert, alter, create, drop on staging.* to developer_role;
5grant select, insert, alter, create, drop on marts.* to developer_role;
6grant create temporary table on *.* to developer_role;
7
8/* LLM  Role Creation & Permissioning */
9create role if not exists llm_role;
10grant select on marts.* to llm_role;
```

```

### Create Users [\#](/blog/how-to-set-up-clickhouse-for-agentic-analytics#create-users)


Now that you have the roles, you can create users for the databases. *Please note that user management for the ClickHouse Cloud console is separate to user management within the database itself.*



```

```
1/* Developer User Creation & Permissioning */
2create user if not exists amy
3identified with sha256_password by 'Strong_dev_password___1';
4grant developer_role to amy;
5alter user amy default role developer_role;
6grant select, insert, alter, create, drop on dev_sandbox_achen.* to amy;
7
8/* LLM User Creation & Permissioning */
9create user if not exists dwaine_service_user
10identified with sha256_password by 'Strong_llm_password__2';
11grant llm_role to dwaine_service_user;
12alter user dwaine_service_user default role llm_role;
```

```

### Define resource allocation [\#](/blog/how-to-set-up-clickhouse-for-agentic-analytics#define-resource-allocation)


Now, you don’t want your LLM to run wild with a query that is incorrect or taking more resources than desired. To prevent this, apply resource allocations on the role you are giving to your LLM user as guardrails.



```

```
1/* Introduces some resource limitations to LLM */
2alter role llm_role
3settings
4    readonly = 1, /*no mutations*/
5    max_execution_time = 30, /*kill long running queries */ 
6    max_memory_usage = 2000000000, /* limits high memory consumption*/
7    max_rows_to_read = 100000000, /* limit full scans */
8    max_bytes_to_read = 5000000000, /* prevents giant table scans*/
9    max_threads = 4; /* manages CPU explosion */
```

```

There’s a variety of [settings](https://clickhouse.com/docs/operations/settings/query-complexity) you can implement in order to set boundaries on the user, role, session, and query level.


Now that we have the infrastructure up and ready to start, you can jump into the more standard ETL process of ingestion and transformation.


## Ingest data [\#](/blog/how-to-set-up-clickhouse-for-agentic-analytics#ingest-data)


There are a variety of ways you can pull data into ClickHouse. The most popular ways are:


- [**ClickPipes**](https://clickhouse.com/docs/integrations/clickpipes): managed continuous ingestion
- [**Table Functions**](https://clickhouse.com/docs/sql-reference/table-functions)**:** With 80\+ table functions like `s3()` or `postgresql()`, you can access many data sources for either batch or stream ingestion. With just one SQL statement, you can query directly from external sources (no need to create an external table, set up separate permissions to object store, etc).
- [**Data Catalog integrations**:](https://clickhouse.com/docs/use-cases/data-lake) If you’re on ClickHouse version 25\.10\+, you can connect to your open table format data catalog. You can configure it via the UI (via Data Sources) or via SQL. This will give you access to your external iceberg/delta tables just as you would a regular ClickHouse database.


![ClickPipes data sources](/uploads/image2_70ba1b5802.png)
Everything can be set up via the ClickHouse Cloud console or by orchestrating the SQL externally (for table functions). Ingest that data into the Raw database so it’s ready for processing.


### Designing the transformation and consumption layers [\#](/blog/how-to-set-up-clickhouse-for-agentic-analytics#designing-the-transformation-and-consumption-layers)


After you have ingested your data into the raw database, staging and marts is where the fun begins. This is where you will transform your data and create the serving layer, consumable for the AI Agent. This often means:


Staging (Transformation)


- Deduplicate
- Normalize types
- Enforce ordering and define primary keys
- Use incremental materialized views to process new data as it lands and build real\-time pipelines.


Marts (Consumption):


- Curate canonical metrics
- Pre\-aggregate expensive joins
- Remove ambiguity
- Flatten schemas
- Use Refreshable materialized views for recomputing the full result and guarantee consistency for AI


Now there is, of course, much more we can dig into this topic here, including optimizing your queries and how to provide context to your AI Agent about your specific business logic with Skills and documentation. But to keep this short and sweet, look out for a follow\-up.

### Join the webinar

Join our data warehousing webinar series starting on February 25th on how to transform and serve up your data for data warehousing.[Register here](https://clickhouse.com/company/events/202602-AMER-data-warehousing-Level2?loc=blog-cta-73-join-the-webinar-register-here&utm_blogctaid=73)## Finally: Invite the AI in [\#](/blog/how-to-set-up-clickhouse-for-agentic-analytics#finally-invite-the-ai-in)


After setting up your services, defining roles, enforcing guardrails, and building clean staging and marts layers, it’s time to let the AI agent in.


Connect your agent via the [Agentic Data Stack](https://clickhouse.com/ai), MCP, or your own client, and use your read\-only LLM credentials.


Now your stakeholders can start to ask questions like:


- “Who were our 50 most active users this quarter?”
- “Show me retention curves for paid vs organic over the last six months.
- “Why did revenue dip last week?”


Remember, an AI\-ready warehouse isn’t just about chucking a chatbot on top of your warehouse. It’s about meeting the requirements of conversational analytics with the core tenets of data warehousing.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
