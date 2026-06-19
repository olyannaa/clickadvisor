# How Rokt Achieved Real\-time Reporting with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Rokt Achieved Real\-time Reporting with ClickHouse

![ClickHouse Team](/_next/image?url=%2Fuploads%2Flogo_square_120_2cca16e3e3.png&w=96&q=75)[ClickHouse Editor](/authors/clickhouse-editor)Dec 6, 2022 · 6 minutes read
  

On December 6, 2022, Vadim Semenov, Engineering Manager in charge of Reporting and Analytics at Rokt, presented his team's use case for ClickHouse at the NYC meetup. Rokt is a global marketing technology company that specializes in developing e\-commerce marketing tools to help companies personalize their customer experiences and drive revenue growth.


During the meetup, Semenov discussed the data Rokt collects, including views, clicks, purchases, and various events, and how they use this data to provide different types of reporting, including aggregated data sets, [real\-time reporting](https://clickhouse.com/resources/engineering/what-is-real-time-analytics), and platform effectiveness measurement. Rokt also performs anomaly detection to determine if any issues arise on their end or the client's end.


![Rokt architecture.png](/uploads/Rokt_architecture_fa449f41a4.png)
## Challenges with Reporting Systems [\#](/blog/nyc-meetup-report-real-time-slicing-and-dicing-reporting-with-clickhouse#challenges-with-reporting-systems)


Rokt explained they have different types of users, including internal business analysts, client services or account managers, external users who access their data through their website or APIs, and other systems that use their datasets. The architecture of Rokt's reporting system was complicated, with external events going through Kafka and various Spark streaming and structure streaming applications that push data to a data lake backed by S3\. Batch jobs produce data that was loaded to either Redshift or Elasticsearch.


However, Rokt faced several challenges with their architecture, such as limited customer data slicing and dicing capabilities, resulting in more requests for custom reports. This put pressure on the business analytics (BA) and reporting teams to provide custom reports instead of doing their primary work.


To address these challenges, Rokt needed a new user interface (UI) that provided more group\-by capabilities and filtering. “Our current setup with Elasticsearch wouldn't support it. So we decided to look into other databases on the market that would,” said Semenov. “The other parts about Elasticsearch that we didn't like, is it's not easy to ingest data because you have to basically do pushes, there's no load from S3, there are no joins, so labels must exist somewhere. If you change some label, you have to re\-ingest all the data.”


Semenov explained that there are several issues in querying the data with Elasticsearch. “It's difficult to query as you have to do JSON. You have to have some gateway that would translate your SQL to JSON or just fire JSON queries directly. And overall it leads to data duplications.”


## The Search for a Better Database [\#](/blog/nyc-meetup-report-real-time-slicing-and-dicing-reporting-with-clickhouse#the-search-for-a-better-database)


Rokt looked into other databases that could provide better support, since they faced difficulties with Elasticsearch. Semenov explained they evaluated several alternatives, including Apache Pinot, Druid, Citus Data, StarRocks, Snowflake and ClickHouse.


“Pinot and Druid are more real\-time focussed. There were no joins. I was told that Druid supports it now in some limited capability, and obviously you cannot fire off all kinds of different SQL queries. Snowflake is more of a data warehouse and it's expensive,” said Semenov. “StarRocks claims to be a competitor to ClickHouse, but it's too fresh to use in production, and Citus Data is too Postgres oriented. Microsoft acquired them and they don't plan to support AWS obviously. So we decided to look closer at ClickHouse, and we really like it.”


This led them to benchmark ClickHouse against Redshift. They set up their own cluster with instance SSDs and EBS and found that ClickHouse was three times less expensive than Redshift without cache.


“You can see that ClickHouse outperforms Redshift easily”, said Semenov. The performance of ClickHouse was consistent in returning results, with some spikes possibly related to the network storage. They also tested the performance of ClickHouse with different levels of concurrency, which showed predictable growth and a maximum query time of six seconds, and found that they could fire up to 200 queries per second.


“‘We also looked at the size of the data that we load. On S3 we had different events stored. It was about 500 gigabytes in Parquet gzip, and once we loaded it into ClickHouse, we saw that it only takes about 500 (gigabytes) as well,” Semenov said.


They compared this to the storage required for the same data in Elasticsearch. “For Elasticsearch we've made the same calculation and it turns out it's about six times more, so we can save some money on actual storage,” Semenov said.


Semenov also provided an overview of their current setup, which included ClickHouse nodes in their own autoscaling group, ZooKeeper, and network load balancers and target groups spread across different nodes.


![Rokt overview.png](/uploads/Rokt_overview_f08a1d62c3.png)
## Advantages of ClickHouse Cloud [\#](/blog/nyc-meetup-report-real-time-slicing-and-dicing-reporting-with-clickhouse#advantages-of-clickhouse-cloud)


Semenov discussed they soon plan to migrate to ClickHouse Cloud as it has several advantages for backups and data analytics, mentioning that using ClickHouse Cloud can solve many problems related to replication, sharding, and scalability. He explained that ClickHouse is particularly good at ingesting data from Kafka and using SQL to analyze real\-time data. Additionally, ClickHouse has built\-in dictionaries that make joins easier and reduce the need for API queries to different databases and services.


The NYC ClickHouse meetup was an excellent opportunity to learn about the challenges and solutions in data reporting for a leading e\-commerce company. With ClickHouse, Rokt was able to achieve consistent and predictable results, reduce storage costs, and analyze real\-time data more efficiently.


## More Details [\#](/blog/nyc-meetup-report-real-time-slicing-and-dicing-reporting-with-clickhouse#more-details)


- This talk was given at the [ClickHouse Community Meetup](https://www.meetup.com/clickhouse-new-york-user-group/) in NYC on December 6, 2022
- The presentation materials are available on [GitHub](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup67/Building%20the%20future%20of%20reporting%20at%20Rokt.pdf)
**ClickHouse Cloud, powered by AWS**

ClickHouse Cloud on AWS uses Amazon Simple Storage Service (Amazon S3\), object storage for scalability, data availability, security, and performance. Amazon Elastic Compute Cloud (Amazon EC2\) is used for high performance and efficiency for data\-intensive workloads. AWS PrivateLink is used for secure connection between ClickHouse Cloud and the customer's VPC. ClickHouse Cloud also integrates with a wide range of other AWS services, including Amazon Managed Streaming for Apache Kafka, Amazon Quicksight, Amazon Relational Database Service, Amazon Glue and Amazon Kinesis.

![](/_next/image?url=%2Fuploads%2Faws_partner_advertising_and_marketing_technology_f168923363.png&w=1080&q=75)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
