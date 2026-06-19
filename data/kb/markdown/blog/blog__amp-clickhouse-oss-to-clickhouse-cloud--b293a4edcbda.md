# From batch processing to streaming: AMP’s data journey from open\-source to ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# From batch processing to streaming: AMP’s data journey from open\-source to ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2FChris_Lawrence_6037f5cdc1.jpg&w=96&q=75)Chris LawrenceJan 20, 2025 · 7 minutes read
  



[AMP](https://useamp.com/) is an ecommerce growth platform that gives Shopify merchants the tools they need to analyze and optimize their store’s performance. Born from a desire to make life easier for online retailers who often manage dozens of disconnected apps, AMP powers some of the biggest brands on Shopify, including Ridge, True Classic, Hydroflask, and more.


AMP’s flagship analytics product, [Lifetimely](https://useamp.com/products/analytics), delivers insights into profit \& loss (P\&L), customer acquisition cost (CAC), lifetime value (LTV), and customer behavior, helping merchants make fast, data\-driven decisions and improve profitability. But as AMP’s user base and platform expanded, so did the demands on their data infrastructure. The increasing complexity and volume of data made it hard to provide the real\-time insights merchants rely on, leading AMP to seek a more scalable, long\-term solution.


Chris Lawrence, Senior Software Engineer at AMP, spoke at an [August 2024 ClickHouse meetup in Melbourne](https://clickhouse.com/videos/amp-from-batch-processing-to-streaming). He shared how the company’s implementation of [ClickHouse Cloud](https://clickhouse.com/cloud) has helped AMP transform their data pipeline from batch processing to real\-time streaming, improving both the speed and reliability of their analytics platform.


## The need for a long\-term solution [\#](/blog/amp-clickhouse-oss-to-clickhouse-cloud#the-need-for-a-long-term-solution)


Before implementing ClickHouse, AMP relied on "a single little Postgres server," Chris says. It handled their data needs early on, but as the AMP platform grew to support thousands of Shopify stores, so did the complexity and scale of their data.


"When you reach a certain size, performance starts to get slow, especially for very real\-time and dynamic reporting," Chris says. "It prevented us from doing a lot of the pre\-processing we need to deliver the fast, detailed reports our merchants really value."


To address these issues, AMP initially added ClickHouse as a supplement to Postgres. "We cloned our entire Postgres instance into ClickHouse just for queries," Chris says, calling it "a hell of a data pipe". This hybrid setup allowed AMP to handle more complex queries and offload pressure from Postgres — but it wasn't a perfect solution.


With the batch processing workflow, data from Shopify stores was pulled into Postgres every couple of hours, and twice a day that data was synced to ClickHouse for querying. This process was "typically quite slow," Chris explains, taking several hours to transfer and process large amounts of data between the two systems.


![diagram_1.png](/uploads/diagram_1_23516d6002.png)
Data freshness became a major problem, especially with AMP's merchants expecting real\-time insights. "Customer obsession is one of our key values; we really want to provide a good experience for our customers," Chris says. "And what is not a good experience is routinely having your data 30 hours out of date due to the amount of time it takes to sync it from Postgres, send it over the wire, and get it into ClickHouse."


The process was also "quite brittle," Chris adds — even a single failure during syncing could cause the system to crash and need to be restarted. "We would routinely have incidents where data is 48 to 72 hours stale," Chris says. New customers installing AMP in their Shopify store would have to wait two to three days before they could see any reporting.


Resource usage was another challenge. The syncing process consumed large amounts of power, requiring a server with over 1\.2 terabytes of RAM to manage the data load. This strain on resources, combined with persistent data freshness issues, led the AMP team to seek a more scalable, long\-term data solution to support their continued growth.


## The move to ClickHouse Cloud [\#](/blog/amp-clickhouse-oss-to-clickhouse-cloud#the-move-to-clickhouse-cloud)


AMP's migration to ClickHouse Cloud was driven by two main goals: keeping data fresh and flexible for customers and building a scalable, real\-time data architecture. 


For merchants, AMP wanted to cut down on reporting delays and make sure data stays accurate. The old system required a full data re\-ingestion from Shopify anytime there was an inconsistency — a process Chris describes as slow, manual, and frustratingly opaque. With ClickHouse Cloud's real\-time setup, AMP can offer insights into inventory, customer behavior, and performance, allowing merchants to act quickly and confidently.


On the technical and "more fun" side, as Chris puts it, AMP aimed to speed up data ingestion with real\-time streaming, enable event replay and data backup, and automate infrastructure management. With Shopify's webhooks and AWS's event\-streaming capabilities, they set out to build a flexible, reproducible data environment managed through infrastructure\-as\-code (IaC).


![diagram_2.png](/uploads/diagram_2_3a618cd04f.png)
AMP's transition to ClickHouse Cloud involved some clever problem\-solving and a few key ClickHouse features. They began by using Shopify webhooks to receive real\-time updates, routing them through Amazon EventBridge and processing them with AWS Lambda. This continuous streaming setup let them move away from outdated batch processing.


For real\-time data updates, AMP used ClickHouse's [ReplacingMergeTree table engine](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree), which allows them to insert updates directly and let ClickHouse manage depublication — helpful for fast, accurate reporting. They did run into one hiccup: inserting data in smaller batches led to bottlenecks, since ClickHouse performs best with larger batches of at least 1,000 rows.


![amp_1.png](/uploads/amp_1_a6e368a904.png)
  

They solved this by adding Amazon Kinesis Data Firehose, which buffers smaller updates into JSON files on S3, reducing inefficiencies before sending data to ClickHouse. They also added [asynchronous inserts](https://clickhouse.com/docs/en/optimize/asynchronous-inserts) — what Chris calls "a really awesome, quite elegant solution" — which temporarily store data in memory before writing it to disk. This eased the load from frequent small inserts, helping AMP maintain efficiency and keep data flowing smoothly.


  

![amp2.png](/uploads/amp2_9815fa59dd.png)
  

Finally, they've made infrastructure management much smoother with the ClickHouse Cloud Terraform provider. With IaC, Chris says, they can create reproducible instances "across all our environments — dev, testing, staging, production, you name it — all in a single click". And with ClickHouse Cloud's monitoring, auto\-scaling, and automatic updates, AMP now has the flexibility to support their growth without the usual infrastructure headaches.
## A future\-friendly data foundation [\#](/blog/amp-clickhouse-oss-to-clickhouse-cloud#a-future-friendly-data-foundation)


Migrating to Clickhouse Cloud has helped AMP redefine its data platform and give Shopify merchants the real\-time insights they need to stay competitive. By moving from a latency\-prone batch processing setup to a continuous streaming architecture, AMP can deliver timely analytics that help merchants make quick, confident, data\-driven decisions.


For Chris and AMP’s engineering team, the move has simplified operations and created a strong and scalable foundation for growth. The new setup offers more straightforward infrastructure management while preserving flexibility, allowing AMP to spin up instances as needed and adapt to fluctuating data loads. Automated monitoring, updates, and scaling mean the team can focus on innovation rather than upkeep.


With ClickHouse Cloud, AMP has built a future\-friendly data foundation that lets them stay true to their commitment to customer obsession, providing merchants with the speed, accuracy, and adaptability they need to thrive in today’s ecommerce landscape.


To learn more about ClickHouse and how it can improve the speed and scalability of your company’s data infrastructure, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/blog/clickhouse-cloud-generally-available).

**ClickHouse Cloud, powered by AWS**

ClickHouse Cloud on AWS uses Amazon Simple Storage Service (Amazon S3\), object storage for scalability, data availability, security, and performance. Amazon Elastic Compute Cloud (Amazon EC2\) is used for high performance and efficiency for data\-intensive workloads. AWS PrivateLink is used for secure connection between ClickHouse Cloud and the customer's VPC. ClickHouse Cloud also integrates with a wide range of other AWS services, including Amazon Managed Streaming for Apache Kafka, Amazon Quicksight, Amazon Relational Database Service, Amazon Glue and Amazon Kinesis.

![](/_next/image?url=%2Fuploads%2Faws_qualified_software_b95bcb6c3e.png&w=1080&q=75)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
