# How we built our Internal Data Warehouse at ClickHouse: A year later


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How we built our Internal Data Warehouse at ClickHouse: A year later

![](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U02_HHFZ_0874_2cba508d09c4_512_e984252673.png&w=96&q=75)[Mihir Gokhale](/authors/mihir-gokhale)Sep 10, 2024 · 12 minutes readA year ago, my colleague Dmitry Pavlov described [how we built ClickHouse’s internal data warehouse on ClickHouse Cloud](https://clickhouse.com/blog/building-a-data-warehouse-with-clickhouse), nicknamed “DWH.” This DWH serves internal business analytics and reporting at ClickHouse, Inc. by collecting data from various source systems, processing it according to a data model, and providing access to the data. The original blog post covers several aspects of building DWH like the use of denormalized data marts, implementation of security features, management of the underlying infrastructure, and more.


However, as ClickHouse has grown, its ClickHouse Cloud based DWH has grown with it. In this blog post, I’ll share an update on how the DWH has evolved over the past year to support a more diverse set of users, data sources, and access points. In particular, our continued use of ClickHouse and the incorporation of [dbt](https://www.getdbt.com/product/what-is-dbt) as two primary components in the stack have enabled DWH to support more real\-time data processing into regular batch reporting, a feature that other traditional data warehouses have historically lacked. As a result, we’re able to make better decisions from our data.


## What is a data warehouse? [\#](/blog/building-a-data-warehouse-with-clickhouse-part-2#what-is-a-data-warehouse)


A data warehouse is a centralized repository that stores data collected from disparate sources within an organization to support decision making, typically business decisions. Here’s an overview of our DWH’s architecture.


![01_unnamed (4).png](/uploads/01_unnamed_4_e8a54ce5b4.png)
At present, we have configured nineteen raw data sources with either hourly or daily insert jobs. Uncompressed, around 6 billion rows and 50 TBs of data are written to DWH every day. ClickHouse then compresses and stores this data. At present, we’re storing 470 TBs of data (compressed) collected over the last two years, which has increased 23% over the last 30 days. In a given week, we typically see \~70 unique users who generate at least one SELECT query.


DWH is a business\-critical system in our organization because of the various business units that depend on DWH for data including leadership, product, engineering, marketing, sales, and finance. In addition, the DWH pre\-production environment has been used as a canary to test open\-source ClickHouse releases before performing broader upgrades in ClickHouse Cloud.


## Setting up batch reporting [\#](/blog/building-a-data-warehouse-with-clickhouse-part-2#setting-up-batch-reporting)


The first iteration of our DWH was as a tool to import data from a small number of business systems with relatively small data volumes. After importing this raw data, it was processed to create batch reports like “\# of trials” or “conversions,” which are the foundation of a data warehouse. Batch reporting was largely configured in [Airflow](https://airflow.apache.org/), and we didn’t use dbt at all. However, as we added data sources, defined more complex business metrics, and served more and more internal stakeholders, this approach did not scale. dbt is an open\-source tool used by data engineers and analysts to build data pipelines, allowing teams to write and iterate on modular SQL code used to transform data. Introducing dbt to the stack helped because it centralized transformation logic related to batch reporting in one place.


For example, when we add new data sources, dbt allows us to use time functions to easily join data that is supplied at different times, triggering follow\-on processes when ready. For example, consider the scenario where data from different sources is inserted at different times, say 7 pm and 10 pm, even though the logical timestamp used to JOIN data is one hourly increment, like 7. This logic can be highly custom, and is subject to change based on business needs. Encoding this logic with 19 different data sources is a lot easier when there’s one tool like dbt to track dependencies which also automatically produces lineage graphs as documentation.


In addition, the metrics we defined became more complicated. Simple count()s and sum()s across a date range gave way to window functions and data differencing which filtered on conditions stored in external tables. dbt paired with ClickHouse’s SQL dialect was key to managing this growing complexity as SQL became the way we encoded this business logic. dbt became the foundation of a more scalable way to report batch\-processed business metrics in DWH.


## Incorporating more real\-time data [\#](/blog/building-a-data-warehouse-with-clickhouse-part-2#incorporating-more-real-time-data)


The ability to define complex business metrics as part of batch reporting processes is table stakes for an enterprise data warehouse. ClickHouse, known for its performance over petabyte\-scale datasets, easily handles the data that we throw in. However, where our DWH really excels is in its ability to handle new and unique real\-time data formats that don’t conform to strict schemas or relations (support for which is constantly [improving](https://github.com/ClickHouse/ClickHouse/issues/58392)). Often, these data sources also have much bigger data volumes.


For example, in our DWH, every day, \~4 billion rows are inserted into just one of the tables \- the entire table has close to a trillion rows. To give another example, we import events from Google Analytics which stores event parameters as nested arrays that represent website activity on clickhouse.com. Similarly, offloads from our NoSQL Control Plane database resemble a nested JSON structure with a flexible schema.


With our foundational batch reporting in place, we began to configure more and more real\-time data sources into our reporting. Our users shared feedback that they found this kind of data to be very valuable and more intuitive, even if the data was less structured and required some light processing when running queries (for example, extracting fields from JSON columns). Our Marketing team was able to get a better sense of which pages on our website were most popular. Our Support Engineers were able to diagnose problems with customers’ queries by digging into logs of their recent Cloud activity. Our product team was able to define more custom logic to track conversion events.


![02_unnamed (4).png](/uploads/02_unnamed_4_aaf41defa7.png)
In DWH, we exposed this real\-time data both in its raw format as we imported it, as well as in a transformed state, like aggregations of real\-time events. [ClickHouse’s rich library of functions](https://clickhouse.com/docs/en/sql-reference/functions) and supported data formats made exploring real\-time data in its raw format very easy, meaning users were able to perform ad\-hoc analysis with a SQL client without needing help from data engineers. Creating aggregations of real\-time data was also possible \- we used dbt to define aggregations as real\-time data arrived in DWH, and then stored these aggregates in a separate table. We used dbt because we were already using dbt elsewhere so it was easier to centralize in an existing tool, but these aggregations are also natively configurable in ClickHouse using features like [materialized views](https://clickhouse.com/docs/en/materialized-view). These aggregations are then joined with existing reporting to track metrics like “number of customers with failed queries.”


This setup allows us to configure batch\-reporting style pipelines for real\-time data while preserving the underlying records in the event that deeper investigation is needed. In one environment, ClickHouse Cloud \+ dbt lets our users combine batch\-processed reporting with real\-time data streams.


## Configuring additional access points [\#](/blog/building-a-data-warehouse-with-clickhouse-part-2#configuring-additional-access-points)


In the first iteration of DWH, we configured [Apache Superset](https://superset.apache.org/) as the BI tool for users to access data. Superset provides a number of key features like dashboarding, a SQL client, alerting, and user management in one deployment which was attractive to the team maintaining DWH. Also, it’s open\-source software. However, it had its limitations. Namely, we found Superset’s SQL client to be buggy, which has a very real impact on user experience.


To address this issue, we opened access to DWH using ClickHouse Cloud’s native SQL console. The SQL console was far better for users writing ad\-hoc SQL queries, and for exploring the various database tables and views. We use the ClickHouse Cloud API to manage user access to sensitive data, and use Google Groups to assign roles to users. Several users of DWH shared how using the SQL console was a superior experience to Superset’s native SQL client.


For a more specialized use case beyond writing ad\-hoc queries, we configured a connection with [Growthbook](https://www.growthbook.io/) as a way to run A/B tests using data in our DWH. The connection between Growthbook and ClickHouse Cloud takes a matter of minutes to set up, and provides us with an out\-of\-the\-box tool for analyzing results of A/B tests (which are SELECT queries to the DWH). Growthbook queries the DWH ClickHouse Cloud service directly, which means that running experiments using very raw, log\-level data is surprisingly trivial.


Finally, we set up a data exporter job from ClickHouse Cloud to Salesforce so that our sales team can consume data from DWH directly in Salesforce, our CRM. This connection is a bit trickier to set up because our Salesforce deployment doesn’t support queries from a static IP address, a limitation that would have made the connection less secure. In the end, we ended up pushing data from DWH into an S3 bucket, and then letting Salesforce query this S3 bucket instead.


## Where we want to take DWH next [\#](/blog/building-a-data-warehouse-with-clickhouse-part-2#where-we-want-to-take-dwh-next)


Looking to the future, we’re excited to keep scaling DWH by configuring additional data sources and onboarding more users. To ensure DWH scales, we want to decompose workloads to independently scalable compute groups which we believe will lead to performance improvements and cost savings.


When DWH was first created, we had just one “hourly load DAG” query which was one ETL job scheduled in Airflow that was responsible for incorporating all new data into DWH. This architecture was chosen because we had a limited number of data sources with a simple data model comprising just two entities. However, we quickly realized that this approach was not scalable as we added additional data sources and data models: The insert job was taking too long to execute, and just one error would jeopardize insertion of all data because of dependencies among different data models. After introducing dbt, we refactored this one job into nine different processes and noticed improvements in service reliability. Most of these jobs still run every hour, meaning that our ClickHouse Cloud service has to be running 24x7 to support insertion of new data.


An upcoming ClickHouse Cloud feature that we’re excited for is [compute\-compute separation](https://clickhouse.com/docs/en/cloud/reference/compute-compute-separation). This feature lets us separate DWH’s compute resources into multiple services, each of which can scale up or scale down independently as needed. This means we can have a read\-only service for our BI tool, a 24x7 read\-write service for critical ETL jobs, and a second read\-write service for less critical ETL jobs where data only needs to be refreshed once a day. This second read\-write service can then be scaled down when inactive, yielding considerable cost savings. In this manner, we see potential to decentralize compute resources and make different compute groups work independently of one another.


In the age of AI, I’m also excited to see how we can incorporate AI features into our DWH. ClickHouse Cloud already supports an AI query builder that assists users in writing simple SQL queries. However, in the long term, I’m excited by the prospect of an AI business analyst who can assist users of our DWH that aren’t intimately familiar with SQL. Also, a number of DWH users currently query the DWH to write weekly/monthly/quarterly reports, another process that I’d love to task to an AI by using existing reports and queries to provide context.


## Closing thoughts [\#](/blog/building-a-data-warehouse-with-clickhouse-part-2#closing-thoughts)


At ClickHouse, we begin each week with a leadership meeting to review and discuss the most important metrics for the company. Many of these metrics are reported directly from the DWH. As our organization has scaled, and DWH with it, I’ve realized that data warehouses serve an important role beyond just displaying pretty dashboards and generating reports; Data warehouses are complex, powerful machines that facilitate discussion and spur action by aligning entire organizations of people to a single source of truth. They allow engineers, marketers, sellers, product managers, and executives to consume the same information and make decisions accordingly. For our data warehouse, ClickHouse expands the universe of queryable data by easily enriching batch reports with real\-time data.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
