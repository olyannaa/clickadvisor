# Longbridge Technology simplifies their architecture and achieves 10x performance boost with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Longbridge Technology simplifies their architecture and achieves 10x performance boost with ClickHouse

![](/_next/image?url=%2Fuploads%2FWQ_Liu_ef7f075644.png&w=96&q=75)Wenquan Liu, Longbridge TechnologyMar 17, 2025 · 11 minutes read![savings_longbridge.png](/uploads/savings_longbridge_994e383ba3.png)
## Longbridge Technology [\#](/blog/longbridge-technology-simplifies-their-architecture-and-achieves-10x-performance-boost-with-clickhouse#longbridge-technology)


Longbridge Technology was founded in March 2019 and is a next\-generation social\-driven online brokerage firm based in Singapore. The company is committed to leveraging social media and cutting\-edge financial technology to provide investors with a new generation of online securities services, offering a secure, stable, diverse, and efficient global investment experience. Longbridge helps users connect the complete investment journey, including asset discovery, understanding, and trading, while introducing innovative technological concepts to Hong Kong's fintech industry.


As a leading fintech company, Longbridge Technology provides investors with a one\-stop investment service for global markets, including Hong Kong, U.S., and Singapore stocks. It supports over 32,000 tradable financial products, including stocks, U.S. stock options, exchange\-traded derivatives, ETFs, REITs, and funds, offering investors diverse and efficient global investment opportunities.


## Business Challenge [\#](/blog/longbridge-technology-simplifies-their-architecture-and-achieves-10x-performance-boost-with-clickhouse#business-challenge)


Longbridge’s market data services provide users with ultra\-fast and stable global market data, accessible via an app, the web, a desktop client and an OpenAPI. Delivering real\-time market data across multiple regions, markets, and asset classes poses challenges in historical data storage and cleansing. To ensure timely and accurate market data display, the underlying database must meet the following requirements:


- **High\-speed data ingestion and synchronization:** Market trade data and calculated K\-line data must be insertable at rates up to millions of records per second to maintain real\-time availability.
- **Fast and efficient batch queries:** The market data service primarily requires batch queries and analysis of historical data, along with simple aggregations for key metric calculations. The database must support multiple aggregation functions and return query results within milliseconds.
- **Support for computational functions and Decimal type:** Given the varying precision requirements across different stock markets, the database must natively support the Decimal data type for accurate storage. Additionally, since securities trading involves time\-series data, the database must provide extensive support for time\-based functions.


![longbridge_high_level.png](/uploads/longbridge_high_level_3bdaf6a4ad.png)
## Pain points of the legacy architecture [\#](/blog/longbridge-technology-simplifies-their-architecture-and-achieves-10x-performance-boost-with-clickhouse#pain-points-of-the-legacy-architecture)


In the early stages, Longbridge introduced various storage products, including file storage, PostgreSQL, Redis, and DynamoDB, to meet the business needs and market data requirements at different stages. However, as the business expanded and the demand for historical data increased, issues with the original storage model began to surface, such as poor performance, high costs, and lack of scalability. These issues prompted Longbridge to rearchitect its market data services.


### Original storage architecture [\#](/blog/longbridge-technology-simplifies-their-architecture-and-achieves-10x-performance-boost-with-clickhouse#original-storage-architecture)


Initially, Longbridge used PostgreSQL for data storage in the Hong Kong, China A\-shares, and Singapore markets. However, as the U.S. stock and options businesses grew, PostgreSQL’s limited concurrent write performance became evident. To handle the high read/write demand for U.S. stock and options data, Longbridge introduced Redis and DynamoDB. While Redis improved performance for US intraday stock data, this added complexity.


Eventually, Longbridge established a complex market data storage architecture, as shown in the diagram below: PostgreSQL for historical market data storage, Redis for real\-time market data storage, and DynamoDB for high IO write scenarios, primarily handling large data write operations. In this architecture, market data from different stock exchanges was written to different databases. Due to varying data characteristics and quality requirements across markets, each market and storage model required separate data cleansing, leading to extremely high operational and development costs.


![longbridge_legacy.png](/uploads/longbridge_legacy_721695beb6.png)
### Problems identified [\#](/blog/longbridge-technology-simplifies-their-architecture-and-achieves-10x-performance-boost-with-clickhouse#problems-identified)


As the business expanded, along with the increasing demand for access to more international markets and night trading data, terminal users also required earlier market data for strategy analysis. This further highlighted the performance, cost, scalability, and operational burden issues of the original system:


- **High storage costs with Redis**: The data model was not universal, requiring custom tools for data cleansing and repair, and it had weak query and analytical capabilities.
- **Poor write performance of PostgreSQL**: It could not support U.S. stock and options data ingestion. Additionally, writing in cleansed data from other markets caused high CPU load and slower queries.
- **High complexity of ETL operations**: Differences in data cleansing, analysis, and storage models across markets increased, requiring independent development and adaptation.


To improve storage system efficiency and scalability, Longbridge decided to re\-architect its storage system.


### Choosing a database for market analytics [\#](/blog/longbridge-technology-simplifies-their-architecture-and-achieves-10x-performance-boost-with-clickhouse#choosing-a-database-for-market-analytics)


After deciding to re\-architect its system, Longbridge evaluated several popular time\-series databases, considering the \- nature of market data, performance requirements, and the migration workload from existing systems. The company researched **ClickHouse, TimescaleDB, and TDengine**, comparing them in terms of **functionality, performance, and cost**, as shown in the table below.


![clickhouse_comparisons.png](/uploads/clickhouse_comparisons_f52acee8e6.png)
From the comparison, ClickHouse stood out over TimescaleDB and TDengine by fully meeting the requirements for securities analysis. It supports **150\+ aggregation functions, native Decimal types** for time\-window calculations, and **PostgreSQL\-compatible** table structures. This compatibility allowed Longbridge to migrate existing data from **PostgreSQL, S3, or OSS to ClickHouse,** achieving unified historical data consolidation.


Beyond feature support and migration compatibility, ClickHouse also demonstrated **outstanding performance advantages**, particularly in bulk data ingestion. It easily handled **millions of U.S. stock trades per second**, thanks to its columnar storage, which **provides over 5x compression efficiency**, making it ideal for storing low\-frequency A\-share K\-line data. Due to its high\-performance data processing capabilities and cloud\-native operational advantages, Longbridge ultimately chose ClickHouse for its architecture re\-engineering.


### Proving ClickHouse performance [\#](/blog/longbridge-technology-simplifies-their-architecture-and-achieves-10x-performance-boost-with-clickhouse#proving-clickhouse-performance)


Before officially switching the tech stack, Longbridge conducted performance testing on ClickHouse's bulk data insertion capabilities using 13 years of A\-share market data. The test instance specifications used were **4 CPU cores and 16GB of memory** on a single\-node instance. Considering that different trading scenarios have varying levels of asset activity, Longbridge tested both single\-asset insertion and bulk data insertion scenarios.


In the test, 1\.1 billion records were first inserted into the database, followed by batching 500,000 records into 10 separate batches to test the average write latency. The results showed that the overall **average latency** was around **7 seconds**, demonstrating significant improvements, which clearly outperformed PostgreSQL.


From the validation tests, it is evident that ClickHouse can fully support Longbridge's market data business, meeting both the performance requirements for U.S. stock and options data insertion and the timeliness requirements.


![longbridge_solution.png](/uploads/longbridge_solution_ad5a300dac.png)
## Using ClickHouse on Alicloud [\#](/blog/longbridge-technology-simplifies-their-architecture-and-achieves-10x-performance-boost-with-clickhouse#using-clickhouse-on-alicloud)


After validating bulk data insertion, Longbridge decided to restructure and upgrade its existing architecture. By replacing DynamoDB, PostgreSQL, and Redis model with ClickHouse, Longbridge unified their data storage solution across all markets.


### Data migration [\#](/blog/longbridge-technology-simplifies-their-architecture-and-achieves-10x-performance-boost-with-clickhouse#data-migration)


During the data migration process, Longbridge used [ClickHouse's external table feature](https://clickhouse.com/docs/sql-reference/table-functions/s3) to migrate historical data stored in DynamoDB, via AliClouds OSS object storage, and used [Aliyun's Yaocai Data Transmission Service (DTS)](https://www.alibabacloud.com/en/product/data-transmission-service?_p_lc=1&spm=a3c0i.7911826.6791778070.260.6a323870UgfJkM) for the migration of data from PostgreSQL to ClickHouse. By leveraging DTS's built\-in capabilities, such as multi\-table merge, Longbridge was able to complete some business transformations during the synchronization process. Overall, DTS provided excellent migration performance, stable links, and after verification, the data was fully consistent, ensuring smooth business migration and data synchronization:


- **No business transformation required**. DTS created full and incremental synchronization links, using Aliyun's PolarDB MySQL as an intermediary. This allowed seamless data synchronization from AWS Aurora PostgreSQL to Aliyun ClickHouse, with DTS automatically creating the same\-named tables on the destination side without the need for user intervention to modify table creation statements.
- **Stable and efficient link**: DTS’s full migration achieved a speed of **275MB/s** and **137,000 RPS**, while incremental migration reached **50MB/s** and **200,000 RPS**, enabling stable and efficient migration of large volumes of historical market data across years and multiple markets.
- **Supports multi\-table merging**: With DTS's built\-in multi\-table merging capabilities, 128 sub\-tables in PostgreSQL containing historical trade data were merged and stored into a single table in the destination ClickHouse database.
- **Supports field type conversion**: During synchronization, DTS supports modifying the source database’s field formats. This feature enabled the upgrade of **varchar** fields in PostgreSQL to **Decimal** fields in ClickHouse.


![dynamo_clickhouse_longbridge.png](/uploads/dynamo_clickhouse_longbridge_7e1f6ff727.png)
### New architecture on ClickHouse [\#](/blog/longbridge-technology-simplifies-their-architecture-and-achieves-10x-performance-boost-with-clickhouse#new-architecture-on-clickhouse)


The re\-structured architecture is shown in the diagram below. As can be seen, in addition to the Singapore, Hong Kong, and A\-shares data originally stored in PostgreSQL, all data has been migrated to ClickHouse. Moreover, the U.S. stock and options data, previously stored in Redis and DynamoDB, has also been consolidated into ClickHouse. Thanks to the unification of the data storage technology stack, the target endpoints for different market data writes and the source endpoints for data queries have been standardized. As a result, the upstream data writing and data cleaning processes have been significantly simplified. The specific changes are as follows:


- **Historical market data storage is unified in ClickHouse**: Data previously stored in PostgreSQL for the Shanghai and Shenzhen markets, Hong Kong Stock Exchange, and Singapore Stock Exchange, along with data stored in DynamoDB and Redis for U.S. stocks, options, and historical market data, has all been migrated to **ClickHouse on Alicloud**. By leveraging ClickHouse’s columnar storage advantages, the storage compression rate was improved by approximately **5 times**, significantly reducing storage costs. Additionally, thanks to ClickHouse’s superior write performance, the write speed per table was improved **10 times** compared to PostgreSQL, effortlessly supporting concurrent writing of millions of U.S. stock and options data points.
- **Intra\-day market data storage was optimized with ClickHouse**: The storage solution was upgraded from **Redis\-only** to a **Redis \+ ClickHouse hybrid storage**. Redis remains the primary storage medium for real\-time market data, while ticker\-level data writes have been upgraded to ClickHouse, reducing the storage costs for real\-time market data.
- **Market data analysis using ClickHouse reduced development workload**: By utilizing ClickHouse’s built\-in aggregation functions, the previously scheduled tasks for statistical calculations were replaced. This allowed for seamless writing of all market transaction details, back\-testing of data, and simple analytical calculations. This reduction in the complexity of data analysis and cleaning significantly simplified the business process.


![clickhouse_new_architecture.png](/uploads/clickhouse_new_architecture_c6e4d796d5.png)
## Business value [\#](/blog/longbridge-technology-simplifies-their-architecture-and-achieves-10x-performance-boost-with-clickhouse#business-value)


![business_result.png](/uploads/business_result_1d230bb49d.png)
Currently, Longbridge has replaced its original architecture of DynamoDB, PostgreSQL, and Redis with scheduled tasks by ClickHouse. This transition simultaneously meets the three key requirements: high\-concurrency data writing, low\-cost storage, and support for simple analysis and back\-testing. It has simplified the technology stack, significantly reduced the development and operational pressure, and also brought about a substantial performance improvement. The specific results are as follows:


- **Storage Costs Reduced by 4x**: The original PostgreSQL instance had a data volume of 500GB, even without including U.S. stock and options data. After migrating to ClickHouse, leveraging its columnar storage and various compression algorithms, only 100GB is needed to store data for all markets, leading to a reduction in storage costs by over 4 times.
- **Write Performance Improved by 10x**: Without any optimization to batch\-writing logic, the original single\-table data writing speed in ClickHouse is 10 times faster than PostgreSQL, easily supporting the concurrent write load of millions of U.S. stock options. It is expected that further performance improvement will be possible with optimizations to the batch\-writing logic.
- **Business Complexity Greatly Reduced**: ClickHouse’s built\-in window and aggregation functions replaced the old architecture, eliminating the need to query 128 PostgreSQL tables and perform code\-based statistical calculations for back\-testing and analysis. This change reduced the data management complexity by 128 times, increased the amount of data queried per request by over 300%, and reduced the technology stack from three systems to just one.


## Summary [\#](/blog/longbridge-technology-simplifies-their-architecture-and-achieves-10x-performance-boost-with-clickhouse#summary)


With the help of ClickHouse, Longbridge Technology has achieved unified structure and storage for the fundamental data of multiple markets and asset types in its market data business. By leveraging ClickHouse, Longbridge has implemented rich data analysis and back\-testing functions. In the fields of quantitative back\-testing, data cleaning, and data analysis, Longbridge is continuously launching new products and innovations. The company also looks forward to expanding its real\-time business analysis capabilities using ClickHouse as the foundation.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
