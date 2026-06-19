# Speed meets scale: How ClickHouse helps Tydo deliver lightning\-fast customer analytics


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Speed meets scale: How ClickHouse helps Tydo deliver lightning\-fast customer analytics

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Nov 18, 2024 · 7 minutes read[Tydo](https://www.tydo.com/) is a customer intelligence platform that helps ecommerce brands turn their data into intelligence. With best\-in\-class analytics that uncover actionable insights into customers and purchasing patterns, the platform offers a complete data warehouse built for AI\-powered customer insights — with no engineer required.


For [Tydo’s platform](https://www.tydo.com/high-growth-enterprise) to provide clients with lightning\-fast, actionable insights and recommendations across multiple channels, it needs a database that’s fast, scalable, and capable of processing high\-dimensional datasets. This robust data infrastructure, combined with ongoing support from Tydo’s data science team, allows brands and partners to make informed decisions, optimize their marketing strategies, and drive business growth.


At an [August 2024 meetup in Los Angeles](https://www.youtube.com/watch?v=EU9ClnKIbO0), Tydo co\-founder and CTO Manav Kohli explained the company’s decision to adopt ClickHouse for their customer segmentation platform and key AI products — from their reasons for switching from Postgres and BigQuery to improvements in speed, scalability, and cost\-efficiency since switching to ClickHouse Cloud.


## Database growing pains [\#](/blog/speed-meets-scale-how-clickhouse-helps-tydo-deliver-lightning-fast-customer-analytics#database-growing-pains)


Tydo originally launched in 2020 as a standardized analytics solution for Shopify merchants. As the company grew to support over 2,000 customers, integrate a broader range of data sources, and serve increasingly large ecommerce brands, its data requirements became more complex. To meet these evolving needs, Tydo continuously invested in more sophisticated data infrastructure to support its growth.


Initially, the company relied on Postgres to manage their data. As an affordable option that allowed Tydo to get off the ground quickly, it met their needs early on. However, while Postgres was “good for smaller workloads,” according to Manav, the database struggled to keep up as data volumes and query complexity grew. Its row\-based structure proved inefficient when processing the large, columnar datasets required by enterprise brands, and its high latency made it hard to deliver real\-time insights.


To address some of these issues, Manav and the team experimented with BigQuery. But while BigQuery offered cheaper storage and was user\-friendly for data analysts, it wasn’t ideal for real\-time analytics or application backends. As Manav explains, “BigQuery is pretty good at querying a lot of data in a reasonable amount of time, but you’re not going to get sub\-second latency like you get with ClickHouse.” The team also found that while BigQuery scaled better than Postgres, the high cost of frequent queries made it an “expensive” option for the real\-time, high\-dimensional analysis they needed.


## A better database solution [\#](/blog/speed-meets-scale-how-clickhouse-helps-tydo-deliver-lightning-fast-customer-analytics#a-better-database-solution)


To keep scaling and serving larger, data\-intensive workloads, the Tydo team knew they needed a more performant, scalable, and cost\-effective database solution. After reviewing their options, they chose ClickHouse for its ability to handle high\-dimensional datasets while delivering sub\-second query performance.


“One of the reasons we were so excited to use ClickHouse is it’s just so much faster than other databases,” Manav says.


As Manav explains, ClickHouse outperformed Postgres and BigQuery when managing analytics\-driven tables, a crucial part of Tydo’s customer segmentation and insights. The [ReplacingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree) engine promised to optimize data storage by streamlining updates and managing rapidly changing data, while [sparse indexing](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes) would allow for lightning\-fast querying, especially for large\-scale analytics.


ClickHouse’s columnar storage also meant Tydo could store and process data more efficiently by targeting specific columns needed for each query, reducing both storage costs and query times. The result was high throughput — the ability to handle large volumes of data quickly and efficiently — without the latency issues that plagued their earlier databases.


In the end, ClickHouse’s speed, scalability, and cost\-efficiency, driven by advanced data compression, made it the perfect solution for Tydo’s growing data needs.


## Built for flexibility and accuracy [\#](/blog/speed-meets-scale-how-clickhouse-helps-tydo-deliver-lightning-fast-customer-analytics#built-for-flexibility-and-accuracy)


At the core of Tydo’s data infrastructure is a pipeline that ingests, processes, and analyzes data from over 200 sources. ClickHouse sits atop the stack as the primary database powering customer segmentation and AI applications. Data flows through an Extract, Load, Transform (ELT) process, loading raw data into Tydo’s warehouse before applying the necessary transformations.


![Tydo-01.png](/uploads/Tydo_01_0f001efecb.png)
Another key part of Tydo’s infrastructure is the domain\-specific language (DSL) layer built on top of ClickHouse, which exposes data models to various services across the platform. This DSL supports fast, flexible querying via APIs while integrating AI\-driven segmentation and insights powered by LLMs. Although LLMs are powerful, they can sometimes produce inaccuracies or hallucinations if not grounded in actual data. To counter this, Tydo’s DSL ensures that the AI relies only on validated core data models from ClickHouse, avoiding any speculative outputs. By linking LLM insights directly to structured data, Tydo minimizes the risk of hallucinations, ensuring that all AI\-driven insights are accurate and data\-based.


![Tydo-02.png](/uploads/Tydo_02_f08062f812.png)
## Speed, scale, and savings [\#](/blog/speed-meets-scale-how-clickhouse-helps-tydo-deliver-lightning-fast-customer-analytics#speed-scale-and-savings)


Since adopting ClickHouse, Tydo has seen huge improvements in both performance and scalability. Thanks to ClickHouse’s powerful architecture and features, the platform now delivers sub\-second filtering and aggregation, allowing Tydo to offer lightning\-fast insights with unmatched speed. This means clients can access data much faster — crucial for large ecommerce brands who need to make swift, data\-driven decisions.


“ClickHouse allows us to provide really fast analytics to our customers, which is exciting and something we couldn't get with our earlier database options,” Manav says.


Tydo has also seen improved cost\-efficiency, thanks to ClickHouse’s ability to handle large volumes of high\-dimensional data at a lower cost than solutions like BigQuery. The new infrastructure’s high\-throughput performance allows Tydo to process vast datasets quickly, reducing both latency and operating expenses.


ClickHouse’s scalability and parallelism ensure that Tydo can continue to grow without worrying about performance bottlenecks. As Manav explains, their analysts now have easier access to data, making it easier to query and generate insights for large ecommerce brands without the burden of heavy technical overhead.


Last but not least, according to Manav, is exposing data models in ClickHouse across multiple products, increasing flexibility. This allows different tools, products, and services within Tydo’s ecosystem to tap into the same core data insights, streamlining operations and enabling more targeted, actionable outcomes for clients.


## The road ahead with ClickHouse [\#](/blog/speed-meets-scale-how-clickhouse-helps-tydo-deliver-lightning-fast-customer-analytics#the-road-ahead-with-clickhouse)


With ClickHouse as the backbone of its customer segmentation and AI applications, Tydo is primed to continue scaling and delivering value to large ecommerce brands and partners. The improvements in speed, cost\-efficiency, and scalability have allowed Manav and the team to streamline operations and offer real\-time insights that were previously out of reach.


ClickHouse’s flexibility ensures that Tydo can keep innovating by incorporating more AI\-driven features and delivering personalized, actionable recommendations. As the company’s client base expands and customer intelligence gets more complex, Tydo remains ahead of the curve with a robust data infrastructure that promises to support long\-term growth while delivering accurate, real\-time analytics to brands around the world.


To learn more about how ClickHouse can improve the speed, scalability, and cost\-efficiency of your data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

**ClickHouse Cloud, powered by AWS**

ClickHouse Cloud on AWS uses Amazon Simple Storage Service (Amazon S3\), object storage for scalability, data availability, security, and performance. Amazon Elastic Compute Cloud (Amazon EC2\) is used for high performance and efficiency for data\-intensive workloads. AWS PrivateLink is used for secure connection between ClickHouse Cloud and the customer's VPC. ClickHouse Cloud also integrates with a wide range of other AWS services, including Amazon Managed Streaming for Apache Kafka, Amazon Quicksight, Amazon Relational Database Service, Amazon Glue and Amazon Kinesis.

![](/_next/image?url=%2Fuploads%2Faws_partner_advertising_and_marketing_technology_f168923363.png&w=1080&q=75)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
