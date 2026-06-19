# How QuickCheck uses ClickHouse to bring banking to the Unbanked


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How QuickCheck uses ClickHouse to bring banking to the Unbanked

![quickcheck.jpg](/_next/image?url=%2Fuploads%2Fquickcheck_0842c62001.jpg&w=96&q=75)Luis RodriguesMay 24, 2022 · 4 minutes read
In this blog post we hear from Luis Rodrigues, the co\-founder and CTO of QuickCheck, a fast\-growing Fintech startup based in Lagos, Nigeria.


In Nigeria, over 60 million Nigerian adults are excluded from banking services and 100 million do not have access to credit. QuickCheck, with the mission of providing financial services to underserved consumers, leverages artificial intelligence to offer app\-based neo\-banking products.


The QuickCheck mobile app has been downloaded by more than 2 million people and has processed over 4\.5 million micro\-credit applications. The team of 150\+ people is located between Nigeria and Portugal.


## **ClickHouse for Multiple Use Cases** [\#](/blog/how-quickcheck-uses-clickhouse-to-bring-banking-to-the-unbanked#clickhouse-for-multiple-use-cases)


QuickCheck started using ClickHouse 2 years ago for multiple use cases including financial data analysis, fraud analysis, and monitoring data. Currently, more than 50 people within the company use dashboards powered by ClickHouse for their daily tasks.


The QuickCheck application analyzes the entire history of a customer’s loans data, using daily snapshots. Hundreds of thousands of rows of data are loaded into ClickHouse daily. On top of this data we perform analysis of portfolio risk and build the financial metrics needed for portfolio analysis.


![quickcheck1.png](/uploads/quickcheck1_bc35b189ad.png)
![quickcheck2.png](/uploads/quickcheck2_31cc6c8054.png)
ClickHouse is also used for our operational dashboards. We aggregate data from different services into ClickHouse and use Metabase for dashboards.


![QuickCheck_UI.webp](/uploads/Quick_Check_UI_854836e406.webp)
Our fraud team uses ClickHouse to collect data for their scoring models. We collect tens of thousands of data points from customers’ phones and other more traditional sources. ClickHouse is used as a way to process all of these SMS messages and extract valuable information used for the scoring and fraud models.


*I love ClickHouse because the team that manages it says* – *it just runs, magically*, *it’s amazing*


## ClickHouse Architecture [\#](/blog/how-quickcheck-uses-clickhouse-to-bring-banking-to-the-unbanked#clickhouse-architecture)


![quickcheck3.png](/uploads/quickcheck3_63e0038fa7.png)
The above diagram shows QuickCheck’s current ClickHouse architecture. Data is in Postgres and gets replicated by Python into ClickHouse. Metabase is on top for the UI. Everybody writes queries in SQL. Some people use machine learning models for data science and fraud detection. They connect directly with SQLAlchemy.


What is also important to mention is that ClickHouse is a column\-oriented database that doesn’t support transactions and updates/deletes are very slow. All transaction data should be kept in Postgres (or another OLTP database) and ClickHouse should be used for what it does best: OLAP queries. However, we are excited about the [transaction support](https://github.com/ClickHouse/ClickHouse/issues/22086) experiments released in [22\.4](https://clickhouse.com/docs/en/whats-new/changelog/) and look forward to experimenting.


## **Instant in ClickHouse vs Forever in Postgres** [\#](/blog/how-quickcheck-uses-clickhouse-to-bring-banking-to-the-unbanked#instant-in-clickhouse-vs-forever-in-postgres)


For me, what matters about ClickHouse is the sheer performance it has. You write an aggregate query across hundreds of thousands of rows and the result is there and if you want to draw a dashboard on that, it’s instant. That is basically the reason why we started using it, for dashboarding.


We realized we had so much data in Postgres, which was taking forever to process, so we started moving it to ClickHouse. It is instant in ClickHouse vs forever in Postgres.


If I try to do a financial analysis of the last year it’s impossible to do in Postgres, the database is going to time out, it will never finish. This happens because we have 100s of millions of rows that store the status and properties of each individual loan every day since it was granted. In ClickHouse it takes less than 5 seconds.


## **ClickHouse Features** [\#](/blog/how-quickcheck-uses-clickhouse-to-bring-banking-to-the-unbanked#clickhouse-features)


The main features of ClickHouse we currently use are:


- Aggregation functions (AVG, SUM, etc) across 100s of millions of rows to create dashboards
- Window and statistical and functions
- Column compression to save on disk space usage


## **Advice to other ClickHouse users** [\#](/blog/how-quickcheck-uses-clickhouse-to-bring-banking-to-the-unbanked#advice-to-other-clickhouse-users)


My advice to others thinking of using ClickHouse is to just try it. If you have queries that are very slow, you should test it in ClickHouse. We are very happy with the performance and with everything.


Visit <https://quickcheck.ng/> for more information.

**ClickHouse Cloud, powered by AWS**

ClickHouse Cloud on AWS uses Amazon Simple Storage Service (Amazon S3\), object storage for scalability, data availability, security, and performance. Amazon Elastic Compute Cloud (Amazon EC2\) is used for high performance and efficiency for data\-intensive workloads. AWS PrivateLink is used for secure connection between ClickHouse Cloud and the customer's VPC. ClickHouse Cloud also integrates with a wide range of other AWS services, including Amazon Managed Streaming for Apache Kafka, Amazon Quicksight, Amazon Relational Database Service, Amazon Glue and Amazon Kinesis.

![](/_next/image?url=%2Fuploads%2Faws_partner_advertising_and_marketing_technology_f168923363.png&w=1080&q=75)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
