# How we built the Internal Data Warehouse at ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How we built the Internal Data Warehouse at ClickHouse

![](/_next/image?url=%2Fuploads%2Fdmitry_03503caafa.jpg&w=96&q=75)[Dmitry Pavlov](/authors/dmitry-pavlov)Jul 19, 2023 · 20 minutes readAt ClickHouse, we see our mission as providing our customers and users with a blazing\-fast cloud analytical database that can be used for internal and customer\-facing analytics. [ClickHouse Cloud](https://clickhouse.cloud/signUp) allows our customers to store and process virtually unlimited amounts of data, which helps them make data\-driven decisions. Making decisions based on facts, and not on assumptions, is crucial for most successful businesses today.


Of course, we follow the same approach inside our team. Developing and operating our cloud database product generates a massive amount of data that can be used for capacity planning, pricing, understanding our customers' needs better, and financial reporting. Tens of data sources, hundreds of terabytes, and around one hundred BI and ad\-hoc users… And guess what \- we are using ClickHouse Cloud for handling this :)


In this post, I will share how our internal Data Warehouse (DWH) is built, the stack we use, and how our DWH will be evolving in the next few months.


## Requirements and data sources [\#](/blog/building-a-data-warehouse-with-clickhouse#requirements-and-data-sources)


We [launched](https://clickhouse.com/blog/building-clickhouse-cloud-from-scratch-in-a-year) ClickHouse Cloud in Private Preview in May 2022, and at the same time, we realized that we want to understand our customers better: how they use our service, which struggles they have, how we can help them, and how we can make our pricing affordable and reasonable for them. For this, we needed to collect and process data from multiple internal data sources: the Data Plane, which is responsible for running customer’s database pods, the Control Plane, which is responsible for customer\-facing UI and database operations, and AWS Billing, which gives us exact costs for running customers’ workloads.


There was a short period of time when our VP Product, Tanya Bragin, did a manual analysis of our customers' workloads in Excel using lookups on a daily basis. It was a shame for me as an ex DWH architect that she had to struggle like this, so as a result the first concept of the internal DWH was born.


In designing the system, we had a number of critical tasks that we aimed to support our internal stakeholders, a handful of which are listed below.




| Internal team | Tasks |
| --- | --- |
| Product team | Tracking conversion and retention rates, feature usage, services size, usage and finding most common problems. Doing deep ad\-hoc analysis. |
| Operations team | Tracking approximate revenue and providing access to some Salesforce data in read\-only mode to most of the company |
| Sales team | Viewing particular customer setup and usage: how many services, how much data, common problems, etc. |
| Engineering team | Tuning our autoscaler, tracking query error rate and DB features usage |
| Support team | Viewing a particular customer setup: services, usage, amount of data, etc |
| Marketing team | Tracking top\-of\-funnel conversion rates, customer acquisition cost and other marketing metrics |
| Costs saving team | Analyzing our CSP costs and proactively optimizing our CSP commitments |
| CI\-CD team | Tracking CI\-CD costs |



**Note: in our internal data warehouse we don’t collect, store, or process any part of our customer’s data (most of which is encrypted) such as the table data, query text, network data, etc. For example, for query analysis, we only collect a list of the used functions, query runtime, memory used and some other meta information. We never collect the query data or query text.**


To accomplish this, we laid out a plan to ingest data from tens of sources, including the following.




| Data source | Type and size | Data |
| --- | --- | --- |
| Control Plane | **DocumentDB** \~5 collections \~500 Mb per hour | Database services meta information: type, size, CSP region, state, financial plan, scaling settings, etc. |
| Data Plane | **ClickHouse Cloud** \~5 tables \~15 Gb per hour | Database system information: metrics stats, query stats, table stats, pod allocation, etc. |
| [AWS CUR](https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html) | **S3 bucket** 1 table \~1 Gb per hour | Our costs and usage for AWS infrastructure that runs our service |
| [GCP Billing](https://cloud.google.com/billing/docs/how-to/export-data-bigquery) | **BigQuery** 1 table \~500 Mb per hour | Our costs and usage for GCP infrastructure that runs our service |
| [Salesforce](https://www.salesforce.com/) (CRM) | **Custom** \~30 tables \~1 Gb per hour | Information about customers' accounts, usage plans, subscriptions, discounts, regions, leads and support issues |
| [M3ter](https://www.m3ter.com/) (metering software) | **Custom API** 2 APIs \~500 Mb per hour | Accurate usage information and bills |
| Galaxy | **ClickHouse Cloud** 1 table | Galaxy is our event\-based observability and monitoring system for our Control Plane / UI Layer |
| [Segment](https://segment.com/) | **S3 Bucket** 1 Table | Some additional marketing data |
| [Marketo](https://business.adobe.com/africa/products/marketo/adobe-marketo.html) | **Custom** | Sent email meta information |
| [AWS Public prices](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/price-changes.html) | **Custom API** 3 tables | Prices for every AWS SKU in every region |
| [GCP Prices](https://cloud.google.com/billing/docs/how-to/pricing-table) | **CSV files** | Prices for every GCP SKU in every region |



Given our primary objectives, we made a few assumptions:
- At our current stage, one\-hour granularity in our data is enough. Meaning, we can collect and store aggregates for every hour.
- For now, we don’t need to use the CDC (or “change data capture”) approach, as it makes the DWH infrastructure much more expensive. Traditional direct load / ETL should satisfy our needs. If these data sources are subject to updates, we can perform a complete data reload.
- As we have a great scalable and fast database, we don’t need to perform ETL transformations outside of the database. Rather, we instead use ClickHouse directly to perform transformations using SQL. This works great.
- At ClickHouse, we are open\-source by our nature, so we want all our stack to have only open source components. We also love to contribute.
- As we have very different types of data sources, we will need multiple tools and approaches for extracting data from these sources. At the same time, we need a standardized intermediate storage.


However, one of our other initial assumptions proved incorrect. We had assumed that, because our data structure was not so complex, it would be enough for us to have only two logical layers in the DWH \- the raw layer and a “data mart” layer. This was a mistake. In reality, we needed a third intermediate layer storing internal business entities. We will explain it below.


## Architecture [\#](/blog/building-a-data-warehouse-with-clickhouse#architecture)


As a result, we came up with the following architecture:


![dwh_architecture_v2.png](/uploads/dwh_architecture_v2_40c61f64f6.png)
1. From a high\-level, our stack can be described as:


	- **[ClickHouse Cloud](https://clickhouse.cloud/signUp)** as the main database
	- **[Airflow](https://airflow.apache.org/)** as a scheduler (an open source scheduling tool)
	- **AWS S3** as an intermediate storage for RAW data
	- **[Superset](https://superset.apache.org/)** as internal BI \& AD\-HOC tool
2. We use different tools and approaches to capture data from data sources to multiple S3 buckets:


	- For Control Plane, Data Plane, Segment and AWS CUR, we use the data source’s native functionality to export data
	- For GCP billing, we use BigQuery [export queries](https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements) to export data to GCS, from where it can be ingested by the [ClickHouse S3 table function](https://clickhouse.com/docs/en/sql-reference/table-functions/s3)
	- For Salesforce, we use [AWS AppFlow](https://docs.aws.amazon.com/appflow/latest/userguide/salesforce.html)
	- For capturing data from M3ter, we wrote our own application. Originally it was written in Kotlin, later we migrated it to Python
	- For Galaxy (which is presented by a ClickHouse Cloud cluster), we use the [ClickHouse S3 table function](https://clickhouse.com/docs/en/sql-reference/table-functions/s3) to export data to S3
	- For Marketo, we use [Fivetran](https://fivetran.com/docs/applications/marketo)
	- Finally, as AWS and GCP prices change very rarely, we decided not to automate its load but created some scripts that help us manually update CSP prices if needed
3. For large fact tables, we collect hourly increments. For dictionaries and tables that can not only receive new rows, but also updates, we use the “replace” approach (i.e. we download the entire table every hour).
4. Once hourly data is collected in the S3 bucket, we use the [ClickHouse s3 table function](https://clickhouse.com/docs/en/sql-reference/table-functions/s3) to import data to the ClickHouse database. The S3 table function scales across replicas and works great on large amounts of data.
5. From the S3 bucket, data is inserted into the RAW layer in the database. This layer has the same table structure as the sources.
6. After a series of transformations run by Airflow (including joins), data from raw tables is inserted into the MART tables \- these tables represent business entities and satisfy the needs of our internal stakeholders.


When performing transformations, many temporary tables are used. In fact, most of the transformed results are at first written to a staging table, and only then are they inserted into the target table. Though such an approach introduces some complexity, it also gives us the required flexibility of reusing the increment data. This allows a single increment part to be used multiple times without recalculating it or rescanning the target table. Staging tables have unique names for every Airflow [DAG](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html) (Directed acyclic graphs) run.
7. Finally, the Superset BI tool allows our internal users to query MART tables as well as build charts and dashboards:


![superset_dwh.png](/uploads/superset_dwh_22240649f0.png)
*Example Superset dashboard. Note: for illustration purposes, sample data with fake numbers is presented.*
### Idempotency [\#](/blog/building-a-data-warehouse-with-clickhouse#idempotency)


Most of the tables that we use in ClickHouse use [ReplicatedReplacingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree) engines. This engine allows us not to care about duplicates in tables \- records with the same key will be squashed and only the last record retained. This also means that we can insert the data for one particular hour as many times as it is required \- only one last version of every row will survive. We also use ClickHouse’s feature “[FINAL](https://clickhouse.com/docs/en/sql-reference/statements/select/from)” when the table is used in further transformations to achieve consistency, so, for example, the `sum()` function doesn’t calculate a row twice.


When combined with Airflow jobs/DAGs that are tolerant to running multiple times for the same period, our pipeline is fully idempotent and can be safely re\-executed without resulting in duplicates. More details on internal Airflow design will be given below.


### Consistency [\#](/blog/building-a-data-warehouse-with-clickhouse#consistency)


By default, ClickHouse provides eventual consistency. This means that if you successfully run a insert query it doesn’t guarantee that the new data is in all ClickHouse replicas. This is sufficient for real time analytics, but unacceptable for the DWH scenario. Imagine, for instance, that you insert data into a staging table. The insert successfully completes and your ELT process starts to execute the next query that reads from the staging table… and you get only partial data.


However, ClickHouse offers a different mode for use cases where consistency is more important than instant availability of inserted data on the first node. To guarantee that the insert query does not return “success” until all replicas have the data, we run all insert queries with a setting `insert_quorum=3` (we have three nodes in our cluster). We don’t use the “auto” setting because when one node goes down (for example, when a ClickHouse upgrade is performed), it will still be possible for the two remaining nodes to accept inserts. Once the restarted node is available, there can be missing inserted data in this node for some time. So for us it is better to get an error (`Number of alive replicas (2) is less than requested quorum (3/3).. (TOO_FEW_LIVE_REPLICAS`) when inserting data in less than three replicas. As restarts due to upgrades are quite fast, queries are usually successful when Airflow retries after an error.


Of course, such an approach doesn’t guarantee that uncommitted parts from previous failed inserts are not visible for a query, but this is not a problem as we support idempotency as described in the previous part. Another solution would be to run all ELT processes using only one replica, but this can limit performance.


### Internal infrastructure design [\#](/blog/building-a-data-warehouse-with-clickhouse#internal-infrastructure-design)


Given our scale, we need our DWH infrastructure to be simple, easy to operate and easy to scale. After running an internal PoC directly on AWS EC2, we migrated all our infrastructure components to Docker.


![internal_infra_design_v2.png](/uploads/internal_infra_design_v2_e508dc1279.png)
- We have separate machines for the Airflow web server, Airflow worker, and Superset. All components are packed in Docker containers
- On Airflow machines, we additionally run a container every 5 seconds that synchronizes the repository containing our DAGs code, ELT queries, and some configuration files with a folder located on the machines
- We use the Superset dashboards and alerts features, so we have a scheduler and worker containers for Superset
- All Airflow and Superset components are synchronized through a Redis instance that runs on a separate machine. Redis stores the execution state of job runs and worker code for Airflow, cached query results for Superset and some other service information
- We use AWS RDS for PostgreSQL as an internal database for Airflow and Superset
- We have two environments running independently with their own ClickHouse Cloud instances, Airflow and Superset installations in different regions
- Though one environment is named Preprod, and the other one is Prod, we keep Preprod consistent so we are be able to switch if Prod is unavailable


Such a setup allows us to make releases safely and easily:


1. Developer creates a branch from a dev or production branch
2. Developer makes changes
3. Developer creates a PR to the Preprod branch
4. Once the PR is reviewed and approved, changes go to the Preprod Airflow instance, where they are tested
5. Once the changes are ready to be released to prod, a PR from Preprod to Prod branch is performed


### Airflow internal design [\#](/blog/building-a-data-warehouse-with-clickhouse#airflow-internal-design)


Initially, we were thinking about creating a sophisticated DAG system with many dependencies. Unfortunately, none of the existing options of DAG dependency mechanics can work with the desired architecture (which is quite a common problem in Airflow):


- Airflow does not allow dataset names to change across executions. [Newly introduced datasets](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/datasets.html) therefore can’t use temporary names. If we use a static dataset name the downstream DAG will be run only once for the last increment.
- Triggers can work for us, but using triggers will add too much complexity to our setup. Having 10\-20 DAGs with triggers, looks like a dependency nightmare from an operating perspective.


We thus ended up with the following structure:


- Separate DAGs for loading data from data source to S3 (for example, M3ter \-\> S3\)
- A single huge main DAG that does all the transformations when data is delivered to S3


![dwh_dag_v2.png](/uploads/dwh_dag_v2_a3808e90b0.png)
The main advantage of such an approach is that it combines both having all required dependencies clearly listed in the main DAG’s tasks, and the ability to build entities not connected to a failed dataset.


### Security [\#](/blog/building-a-data-warehouse-with-clickhouse#security)


As our internal DWH system stores sensitive data, including PII and financial information, security must be the foundation of our architecture. For this, we have implemented some basic rules and a set of frameworks on how we operate the DWH.


#### General rules [\#](/blog/building-a-data-warehouse-with-clickhouse#general-rules)


- Different data must be accessible by different users according to the company’s role model, and it should be done automatically
- Separating permissions should be done on the **database** level (not on the BI side!)
- Network access restrictions should be presented on all levels (from using Okta for the BI tool to IP filtering)


#### Implementation [\#](/blog/building-a-data-warehouse-with-clickhouse#implementation)


We use Google groups to control internal user permissions. This allows us to use existing internal company groups, and also allows group owners (who can be presented by a non\-technical person that doesn't care about SQL) to control access to different data. Groups can be nested.
For example:


- [general\_data@clickhouse.com](mailto:general_data@clickhouse.com)
	- [company@clickhouse.com](mailto:company@clickhouse.com)
- [financial\_data@clickhouse.com](mailto:financial_data@clickhouse.com)
	- [thor@clickhouse.com](mailto:thor@clickhouse.com)
	- [ironman@clickhouse.com](mailto:ironman@clickhouse.com)
	- [thehulk@clickhouse.com](mailto:thehulk@clickhouse.com)
	- [scrooge@clickhouse.com](mailto:scrooge@clickhouse.com)
- [hr\_data@clickhouse.com](mailto:hr_data@clickhouse.com)
	- [captain\_clickhouse@clickhouse.com](mailto:captain_clickhouse@clickhouse.com)
	- [chip@clickhouse.com](mailto:chip@clickhouse.com)
	- [superman@clickhouse.com](mailto:superman@clickhouse.com)


For matching Google groups with exact permissions, we use a system table that connects the:


- Google group name
- Database name
- Table name
- Array of columns
- Filter (for example, “where organization\=’clickhouse’”)
- Access type (SELECT, INSERT)


We also have a script that does the following:


1. Gets a recursive list of groups and users
2. Creates (actually, replaces) these users in the database with a unique password
3. Creates roles corresponding to Google groups
4. Assigns roles to users
5. Grants permissions to roles according to permission table with “WITH REPLACE OPTION” clause \- this will remove all other grants that could be done manually for some reason


On the Superset side, we use the [DB\_CONNECTION\_MUTATOR](https://github.com/apache/superset/blob/b544993048583f77b2472bf4654b7abec7f8eaed/superset/config.py#L1042) function to substitute the database username with the Superset user when a query is sent to the DB. We also have Google Oauth enabled in Superset. That means, in the DB\_CONNECTION\_MUTATOR we have everything we need to make Superset connect with the desired username and password:



```
def DB_CONNECTION_MUTATOR(uri, params, username, security_manager, source):
    # Only enable mutator on clickhouse cloud endpoints
    if not uri.host.lower().endswith("clickhouse.cloud"):
        return uri, params
    user = security_manager.find_user(username=username)
    
    generated_username = str(user.email).split('@')[0] + '--' + str(user.username)
    uri.username = generated_username
    # Password generation logic - hidden in this example
    uri.password = ...
    return uri, params

```

The above means that Superset uses a unique database username for every user, with a unique set of permissions that are controlled by Google groups.


### GDPR Compliance [\#](/blog/building-a-data-warehouse-with-clickhouse#gdpr-compliance)


ClickHouse Cloud users can ask us to delete all their personal data including name, email and other information. Of course, in this case we also delete this information from the DWH. The coolest thing here is that we don’t need to run any updates or deletes in ClickHouse tables. Because our engine leaves only one last record for every key value, all we need to do is to insert a new version of row with deleted users data. It will take a few hours for old rows to disappear, but GDPR standards give you from 3 to 30 days for data removal based on the scenario. So the full algorithm is:


1. Find a special flag in one of the source system that this ID should be masked/deleted
2. Select all records from the table with this ID
3. Mask required fields
4. Insert the data back to the table
5. Run “optimize table … final” command to be sure old records are deleted from disk
6. When a new hourly increment is coming we perform a join to the list of deleted IDs. This means if for some reason user’s PII information has not been fully removed yet, we will automatically mask this data


## Improvements and plans for future [\#](/blog/building-a-data-warehouse-with-clickhouse#improvements-and-plans-for-future)


Though in general we are satisfied with our DWH, there are some things that we plan to change in the upcoming months:


### Third logical layer [\#](/blog/building-a-data-warehouse-with-clickhouse#third-logical-layer)


The idea of having only two logical layers, unfortunately, doesn’t work. We found that for calculating really complex metrics that can be backfilled and that need data from 5\+ data sources, we have to create dependencies between different marts. Sometimes this even involves recursive dependencies. To solve this, we need to introduce an intermediate layer called the Detail Data Store, or DDS. It will store some internal business entities like account, organization, service, etc. This layer will not be available for end users, but it will help us to remove dependencies between marts.


### DBT [\#](/blog/building-a-data-warehouse-with-clickhouse#dbt)


Airflow is a good scheduler, but we need a tool that will take care of many other things: reloading data marts completely if needed, QA, data describing and documentation, and others. For that, we plan to integrate Airflow with DBT. As we run all our data infrastructure in Docker containers, it is quite easy to create a separate DBT container for our needs that will be triggered by Airflow DAGs.


### Naming conventions [\#](/blog/building-a-data-warehouse-with-clickhouse#naming-conventions)


Though from the beginning we knew that we must follow some rules in how we name tables, fields and charts, we didn’t invest too many resources in this. As a result, we now have quite confusing namings that don’t allow users to understand the purpose of a particular table or field. We need to make it clearer.


## Resources [\#](/blog/building-a-data-warehouse-with-clickhouse#resources)


ClickHouse is a relatively young company, so our DWH team is relatively small and has only 3 members:


- Data Engineer \- builds and maintains the infrastructure
- Product Analyst \- helps users with getting insights, building charts and understanding the data
- Team Lead \- spends only \~30% time on DWH tasks


As for the infrastructure, we use two environments with separate ClickHouse Cloud services. Each service has 3 nodes (aka replicas, but all replicas are accepting queries). Memory usage for our ClickHouse services is \~200 Gb. While we don’t pay for these services as we are part of ClickHouse Cloud team, we researched competitors pricing and performance and believe that another cloud analytical database would be much more expensive in our case.


In addition, our infrastructure includes 8 EC2 machines and an S3 bucket with raw data. In total, these services cost about \~$1,500 per month.


## Overall results [\#](/blog/building-a-data-warehouse-with-clickhouse#overall-results)


Our DWH has been operating for more than one year. We have \>70 monthly active users, hundreds of dashboards, and thousands of charts. Altogether, users run \~40,000 queries per day. This chart shows the number of queries per day, and the breakdown is per user. System and ELT users excluded:


![dwh_usage.png](/uploads/dwh_usage_68b88d8640.png)
*Yep, our users work on weekends, too*


We store \~115 Tb of uncompressed data in \~150 tables, but because of ClickHouse’s efficient compression the actual stored data is only \~13 Tb.


![dwh_data_size.png](/uploads/dwh_data_size_69b018f167.png)
*Week over week growth of the amount of data in our DWH. February spike represents an internal experiment that needed all data to be duplicated.*


## Summary [\#](/blog/building-a-data-warehouse-with-clickhouse#summary)


In one year we have deployed a DWH based on open\-source technology that delivers an experience our users love. While our DWH makes it easy to work with data, we also see a lot of improvements and changes that we need to make to move forward. We believe that our usage of ClickHouse Cloud proves that it can be used to build a robust DWH.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
