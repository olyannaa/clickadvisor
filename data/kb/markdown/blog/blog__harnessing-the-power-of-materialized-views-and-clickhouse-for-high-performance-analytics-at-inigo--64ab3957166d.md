# Harnessing the Power of Materialized Views and ClickHouse for High\-Performance Analytics at Inigo


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Harnessing the Power of Materialized Views and ClickHouse for High\-Performance Analytics at Inigo

![](/_next/image?url=%2Fuploads%2F247935571_003ade6a_76b4_4f48_b6f3_84bdede021e6_5423d093c8.png&w=96&q=75)Ruslan Scherbin, Senior Software Engineer, InigoJun 23, 2023 · 11 minutes readIn this guest blog post, Ruslan Shcherbin, Senior Software Engineer from [Inigo](https://inigo.io/), shares his experience of exploring various database alternatives and eventually choosing ClickHouse paired with Materialized Views to handle their high\-performance analytics needs.


Inigo is a pioneering company in the GraphQL API management industry, specializing in comprehensive security and governance at scale. Their platform empowers API and platform teams to fully control, manage, and secure GraphQL deployments by providing immediate visibility, security, access control, compliance, and continuous delivery. In addition to its security features, Inigo offers key developer experience enhancements and workflow efficiencies, ultimately enabling organizations to expedite GraphQL API development, lower costs, and improve end\-user experiences.


## Overview [\#](/blog/harnessing-the-power-of-materialized-views-and-clickhouse-for-high-performance-analytics-at-inigo#overview)


At Inigo, we were seeking a database solution that could handle a high volume of raw data for analytics. After exploring various alternatives, including SQLite, Snowflake and PostgreSQL, we decided to [experiment with Materialized Views](https://clickhouse.com/blog/using-materialized-views-in-clickhouse) using ClickHouse on a relatively slow machine. In this post, we share our findings after loading billions of rows of data and conducting measurements.


We process and analyze billions of GraphQL API requests at Inigo. Live incoming API data allows us to create aggregated views on high cardinality data, generate alerts, and create dashboards based on extensive data.


![ClickHouse_Inigo__3_analytics.png](/uploads/Click_House_Inigo_3_analytics_7417851102.png)
## Database Alternatives for Large\-Scale Analytics [\#](/blog/harnessing-the-power-of-materialized-views-and-clickhouse-for-high-performance-analytics-at-inigo#database-alternatives-for-large-scale-analytics)


Before arriving at ClickHouse, we tried several other databases:


1. Snowflake \- too slow and costly for our needs. While it performs well for processing in\-house data, it becomes quite expensive when handling real\-time customer data within a product, which negatively impacts the product's unit economics. The lack of a local Snowflake emulator further complicates development, as it prevents running continuous unit tests against the database. Additionally, the user interface did not align with our preferred database usage due to the Snowflake UI dashboard being more geared toward queries on a single table. Since each service had its own separate table, we had to obtain and hardcode table names in the UI. This made it impossible to retrieve data from all tables using a single query in the user interface.
2. PostgreSQL \- an excellent transactional database, but unsuitable for large analytic workloads. We were able to get it to work with around 100K rows, but past that, the indexes were growing out of control and the cost of running a PostgreSQL cluster didn’t make sense. There was significant performance degradation once we hit the 100K \- 1M rows mark. However, we acknowledge that this comparison might be unfair, given that PostgreSQL's OLTP nature is not ideally suited for this use case.


## Why ClickHouse? [\#](/blog/harnessing-the-power-of-materialized-views-and-clickhouse-for-high-performance-analytics-at-inigo#why-clickhouse)


Our choice fell on ClickHouse for several reasons. ClickHouse is a columnar database specifically designed to handle high volumes of data while providing fast query execution. Materialized views in ClickHouse allow datasets to be pre\-aggregated which can significantly improve the performance of analytical queries. Furthermore, ClickHouse's ability to automatically manage and update materialized views as new data is ingested simplifies the maintenance process, making it an attractive choice for those seeking an efficient and powerful analytical database solution.


The open\-source nature of ClickHouse and the ability to run it as a simple binary or docker on our laptops were major attractions. The convenience of local testing, combined with its scalability, convinced us that ClickHouse was the ideal choice for our needs.


## Inigo’s ClickHouse Setup [\#](/blog/harnessing-the-power-of-materialized-views-and-clickhouse-for-high-performance-analytics-at-inigo#inigos-clickhouse-setup)


Our current ClickHouse setup is a single database where nearly every Inigo service has its own table, with some tables containing billions of rows of data. It runs on 4 vCPUs, 32GB RAM for the development environment and 16 vCPUs, 128GB RAM for the production environment.


Setting up ClickHouse was challenging, as understanding the nuances of each index, sharding, and materialized views required considerable effort. However, the end result has been a system capable of loading and querying vast amounts of analytics data in a scalable manner, both in terms of hardware cost and engineering development time.


![ClickHouse_Inigo__2_diagram.png](/uploads/Click_House_Inigo_2_diagram_4ad6a8f342.png)
## Materialized Views in ClickHouse [\#](/blog/harnessing-the-power-of-materialized-views-and-clickhouse-for-high-performance-analytics-at-inigo#materialized-views-in-clickhouse)


Given that we have billions of rows in some of our raw tables, we strive to minimize joins whenever possible. Instead, we have consolidated the data into several materialized views, each grouping the data into distinct time window buckets. As a result, most of the time, we are querying thousands of aggregated rows instead of millions of raw data rows, resulting in faster real\-time filtering.


### Creating Materialized View in ClickHouse [\#](/blog/harnessing-the-power-of-materialized-views-and-clickhouse-for-high-performance-analytics-at-inigo#creating-materialized-view-in-clickhouse)


Our raw tables all contain a timestamp column `observed_at`.


We then aggregate the data rows into specified intervals for the materialized tables. For example, if the interval is 1 minute, we use the [`toStartOfInterval(observed_at, INTERVAL 1 minute)`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions#tostartofintervaltime_or_data-interval-x-unit--time_zone) function to aggregate data into one minute intervals. Each row in the materialized views contains several raw data values, all corresponding to a particular minute based on the `observed_at` column.


By creating materialized views with different intervals, such as 6 minutes, 40 minutes, and 3 hours, we can further enhance query performance and enable more efficient data analysis across various timeframes.


We exclude all columns containing unique data, such as trace\_id, from materialized views. When we need to filter by trace\_id, we query the raw data. It is worth noting that raw data queries are reasonably quick in ClickHouse, as ClickHouse can efficiently sift through a large number of rows in real\-time using the appropriate index for each column.


### Grouping Data in ClickHouse [\#](/blog/harnessing-the-power-of-materialized-views-and-clickhouse-for-high-performance-analytics-at-inigo#grouping-data-in-clickhouse)


In our analytics, we primarily use GROUP BY queries to obtain data. While standard queries and materialized view queries use the same SQL syntax, there is a slight modification in the way they handle counting. Instead of using `count()` to count the rows, materialized view queries use `sum(calls)` with the derived column `calls`. The column `calls` is created by using the function `count()` aliased as `calls` in the materialized view definition. This change allows us to aggregate the count of rows from the materialized view, resulting in more efficient querying and better performance.


### Understanding the Merge and State Suffix in ClickHouse [\#](/blog/harnessing-the-power-of-materialized-views-and-clickhouse-for-high-performance-analytics-at-inigo#understanding-the-merge-and-state-suffix-in-clickhouse)


In ClickHouse, the `-State` and `-Merge` suffixes are used with aggregation functions to handle intermediate aggregation states and merge them efficiently. These suffixes are particularly useful when working with distributed databases or when we need to combine aggregated results from multiple sources.


The State suffix: The aggregation functions with the State suffix return an intermediate aggregation state rather than the final result. These intermediate states are stored in a compact binary format that represents the aggregation in progress.


For example, if we want to calculate the 95th (0\.95\) and 99th (0\.99\) percentiles of a column called `server_process_time`, we can use the `quantilesState(value)` function. This function returns the intermediate state of the quantiles calculation, which we can store in a separate table or combine with other intermediate states. We utilize these state functions in our materialized views, storing their output in summarized tables.


The Merge suffix: The aggregation functions with the Merge suffix take the intermediate aggregation states produced by their corresponding State functions and merge them to produce the final aggregation result. This is useful when we have multiple intermediate states that we need to combine into a single aggregated result.


For instance, to obtain the 99th percentile of the aggregated `server_process_time`, we would use `quantileMerge(0.99)(quantiles_server_process_time)`, where `quantiles_server_process_time` is the intermediate state resulting from the `quantilesState` function used in the materialized view. We show a complete example below:



```
--- receiving table for the inserts
CREATE TABLE query_data
(
`observed_at` DateTime64(3),
`sidecar_process_time` Float64,
`server_process_time` Float64
)
ENGINE=MergeTree()
ORDER BY (observed_at);


CREATE MATERIALIZED VIEW query_data_mv
ENGINE = AggregatingMergeTree()
ORDER BY (observed_at)
AS SELECT
toDateTime64(toStartOfInterval(observed_at, INTERVAL 1 MINUTE), 3) as observed_at,
quantilesState(0.95, 0.99)(sidecar_process_time) as quantiles_sidecar_process_time,
quantilesState(0.95, 0.99)(server_process_time) as quantiles_server_process_time
FROM query_data
GROUP BY observed_at;

INSERT INTO query_data (observed_at, sidecar_process_time, server_process_time) VALUES (toDateTime('2023-06-15 19:09:01'), 0, 0), (toDateTime('2023-06-15 19:09:09'), 100, 1000) (toDateTime('2023-06-15 19:19:01'), 0, 0), (toDateTime('2023-06-15 19:19:09'), 100, 1000);

--we query the materialized views underlying table with merge functions
SELECT
observed_at,
quantileMerge(0.95)(quantiles_sidecar_process_time) as p95_sidecar_process_time,
quantileMerge(0.99)(quantiles_sidecar_process_time) as p99_sidecar_process_time,
quantileMerge(0.95)(quantiles_server_process_time) as p95_server_process_time,
quantileMerge(0.99)(quantiles_server_process_time) as p99_server_process_time
FROM query_data_mv
GROUP BY observed_at;

```

While we are still working on recreating large materialized views, we believe we're on the path to a promising solution.


## Results and Benefits of Using ClickHouse and Materialized Views [\#](/blog/harnessing-the-power-of-materialized-views-and-clickhouse-for-high-performance-analytics-at-inigo#results-and-benefits-of-using-clickhouse-and-materialized-views)


1. We utilize Materialized View queries in nearly all aspects of our app, with the exception of one table with Raw data and any queries that involve filtering by a unique field.
2. Switching to use Raw data when necessary is straightforward. We employ the same SQL files in our queries, with minor modifications made for Materialized Views.
3. There's a significant difference in data size. For instance, Raw data covers up to a week, while Materialized Views can accommodate up to a month's data:
![Results1.png](/uploads/Results1_9d8bf85802.png)
4. Less load on the database and faster operation of the entire App due to the smaller size of MV tables
5. We can write migrations not only in SQL files, but also in Go, which is more convenient for us as we often migrate multiple tables simultaneously. Detailed example [here](https://pastila.nl/?01bf5e0e/66b1c33a692b7390381d15ab61b9e202).
6. ClickHouse’s strong typing simplifies our migration logic which historically needed to allow for weaker typing guarantees in NoSQL solutions.
7. The convenience of Test\-Driven Development (TDD) is enhanced by the speed of our independent integration tests.


We've encountered no issues when using Materialized Views, both with standalone instances and within a clustered environment.


## Performance Results of Using ClickHouse and Materialized Views [\#](/blog/harnessing-the-power-of-materialized-views-and-clickhouse-for-high-performance-analytics-at-inigo#performance-results-of-using-clickhouse-and-materialized-views)


1. The database is now faster than our Golang code, allowing us to use pooling and improving our UI responsiveness.
2. Confidence in query speed, enables us to identify issues outside the database, such as in tracing extensions.


## Using ClickHouse Cloud [\#](/blog/harnessing-the-power-of-materialized-views-and-clickhouse-for-high-performance-analytics-at-inigo#using-clickhouse-cloud)


The scalability of this solution is dependent on a variety of factors, one of the most important being the setup of the scaling architecture. ClickHouse offers a cloud service with 720 GiB RAM, 180 vCPU, and 10 TB of data, indicating its potential for handling significant workloads. We have been able to easily scale to 1 billion rows, and that number continues to grow.


Looking ahead, we are excited about the ClickHouse Cloud offering. Although we began using ClickHouse before this was available and devoted significant time to configuring and managing shards and disks, we anticipate moving some of our self\-hosted workloads to the cloud.


## Conclusion [\#](/blog/harnessing-the-power-of-materialized-views-and-clickhouse-for-high-performance-analytics-at-inigo#conclusion)


ClickHouse has been an excellent choice for our large\-scale analytics needs. Even though it has certain complexities, such as the absence of transactions, these are substantially overshadowed by its benefits. The speed, capacity to handle vast amounts of data, and features like Materialized Views make ClickHouse a robust tool for analytics. Overall, ClickHouse when paired with Materialized Views, has proven to be an impressive solution. We highly recommend it for organizations seeking a high\-performance analytics solution.


## Learn More [\#](/blog/harnessing-the-power-of-materialized-views-and-clickhouse-for-high-performance-analytics-at-inigo#learn-more)


Visit: <https://inigo.io/>

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
