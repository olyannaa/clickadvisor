# Building Chronicle: How Temporal supercharged their observability with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Building Chronicle: How Temporal supercharged their observability with ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Nov 14, 2024 · 8 minutes read## Introduction [\#](/blog/building-chronicle-how-temporal-supercharged-their-observability-with-clickhouse#introduction)


[Temporal](https://temporal.io/) is a durable execution platform that helps businesses build scalable applications without sacrificing productivity or reliability. Founded by two longtime collaborators with over 15 years of experience building mission\-critical platforms for developers, Temporal launched in 2019 as an open\-source solution for managing complex, long\-running workflows. Since then, it has been embraced by over 1,500 users across a range of industries, including innovative companies like Netflix, Nvidia, Datadog, OpenAI — and, of course, ClickHouse.


As the company grew and introduced a SaaS offering, Temporal Cloud, in 2022, the team recognized the need for advanced observability tools to monitor their multi\-tenant architecture and support the platform’s expansion. In particular, they needed a system that could handle massive datasets efficiently and deliver real\-time insights without driving up costs.


At an [August 2024 meetup in Seattle](https://clickhouse.com/videos/supercharged-observability-clickhouse), Sean Gillespie, staff software engineer at Temporal, explained how the team built an innovative new observability system, which they called Chronicle. With help from ClickHouse, they’ve been able to keep data queries fast and infrastructure costs low, all while scaling to meet growing demand.


## The challenges of modern observability [\#](/blog/building-chronicle-how-temporal-supercharged-their-observability-with-clickhouse#the-challenges-of-modern-observability)


Observability is crucial for understanding the health of a cloud\-based system — but it comes with challenges, especially in highly multi\-tenant environments like Temporal Cloud.


At its core, observability depends on the ability to collect and analyze logs, metrics, and traces to gain insights into system performance and user experience. “Observability isn’t just about understanding bugs and outages,” Sean says, [quoting](https://charity.wtf/2024/08/07/is-it-time-to-version-observability-signs-point-to-yes/) Honeycomb.io founder Charity Majors. “It’s about proactively understanding our software and how users are experiencing it, through the raw data we can collect and query efficiently thanks to ClickHouse.”


For Temporal, the initial challenge was handling the cardinality problem — caused by the need to track unique values, such as tenant IDs, which grow exponentially with the number of tenants. In multi\-tenant systems, every combination of tenant and system metric multiplies the dataset, leading to ballooning storage requirements and slower query performance.


“In our case, if you have a bunch of tenants coming into your system, and you add new nodes to accommodate the new tenants, then the amount of metrics your system produces grows quadratically,” Sean says. “This was a huge problem for us.”


Adding to the complexity was the need to slice data by tenant and environment to quickly identify and address issues affecting specific customers. Sean and the Temporal team realized that scaling observability in this way would require a totally new approach — one that could efficiently manage and query such vast amounts of data in real time.


## Building Chronicle with ClickHouse [\#](/blog/building-chronicle-how-temporal-supercharged-their-observability-with-clickhouse#building-chronicle-with-clickhouse)


In 2023, Temporal began building their new observability system, Chronicle. They chose ClickHouse, a column\-oriented OLAP database, for its advantages over traditional time\-series databases like Prometheus and Graphite, and for what Sean describes as ClickHouse’s reputation as a “pretty spectacular piece of technology.”


According to Sean, one of the team’s two main goals at the start of the project was removing field cardinality as a scaling concern. “We want our observability system to embrace cardinality and ingest as much data as it possibly can,” he says.


Temporal’s other primary objective was enabling new query patterns that were previously impossible. “This is really important for our developer success organization,” Sean says. “We want to dive in and see exactly the types of problems our customers are having.”


At the Seattle meetup, Sean shared more about three key components of Chronicle: distributed tables, schema optimization, and write\-read aggregation.


## Distributed tables [\#](/blog/building-chronicle-how-temporal-supercharged-their-observability-with-clickhouse#distributed-tables)


One of Chronicle’s most important features is its use of [distributed tables](https://clickhouse.com/docs/en/engines/table-engines/special/distributed) within ClickHouse. Temporal operates across 14 regions globally, but to manage costs, they consolidate their observability data into five centralized hubs, each with a dedicated [ClickHouse Cloud](https://clickhouse.com/cloud) service.


By leveraging AWS PrivateLink, they minimize egress charges when data needs to move between zones — which can run anywhere from two to nine cents per gigabyte for all bandwidth leaving a particular region. Instead, queries are pushed to the regions where the data resides, allowing for efficient data processing without moving large amounts of data across regions.


“We’re trying to keep our data stationary, within the availability zone in which it was created, so that we aren’t billed for data transfer every time data leaves it,” Sean says. “The system is designed to get data into ClickHouse as cheaply as possible.”


## Schema optimization [\#](/blog/building-chronicle-how-temporal-supercharged-their-observability-with-clickhouse#schema-optimization)


Chronicle’s schema was carefully designed to optimize for Temporal’s most common queries. Logs are organized using sorting keys based on cluster, namespace, and timestamp, which ensures that queries targeting specific tenants or environments can be executed efficiently. This structure means Temporal can maintain high performance even when running complex, investigative queries across large datasets.


As Sean explains, “This choice of ordering key has provided really solid performance for investigative\-style queries,” making it easier to drill down into specific logs or metrics. This schema\-first approach has been key in helping Chronicle scale alongside Temporal’s growing customer base.


## Write\-time aggregation [\#](/blog/building-chronicle-how-temporal-supercharged-their-observability-with-clickhouse#write-time-aggregation)


Temporal also benefits from ClickHouse’s support for [materialized views](https://clickhouse.com/docs/en/materialized-view), which allow for both write\-time and read\-time aggregation. While many observability tools opt for read\-time aggregation due to its flexibility, Temporal strategically relies on both. Write\-time aggregation is used for dashboards that need to load quickly, delivering real\-time responses to common queries, while read\-time aggregation is used for more exploratory queries.


For example, with ClickHouse, queries related to request durations — such as heat maps that show latency patterns — can be rendered in under 50 milliseconds, enabling better system monitoring and leading to what Sean calls “true real\-time performance.”


“We use this to optimize common dashboard queries, such that dashboards load almost instantaneously,” he says. “We can do this because the ClickHouse materialized view operation is relatively cheap in the grand scheme of ClickHouse ingestion compute.”


## A major performance boost [\#](/blog/building-chronicle-how-temporal-supercharged-their-observability-with-clickhouse#a-major-performance-boost)


Since implementing Chronicle with ClickHouse, Temporal has seen a number of big wins. Their ingestion system now processes up to 150,000 rows per second, with individual CPU cores handling up to 60,000 rows per second at peak efficiency. Sean says [async inserts](https://clickhouse.com/docs/en/cloud/bestpractices/asynchronous-inserts) have been “wildly important,” explaining: “We’ve found that by using async inserts with a five\-second wait period, we can ingest substantially more data with the same compute profile.”


Beyond ingestion speed, the system has delivered “extremely fast” query performance, with write\-aggregated tables returning results in under 200 milliseconds — especially valuable for real\-time monitoring dashboards. Chronicle has also shown impressive data compression capabilities, with its largest table achieving a 36\.59x compression ratio (which Sean points out is “three times what the ClickHouse website advertises”) largely due to the efficient handling of tenant IDs and other low\-cardinality strings.


Finally, Sean highlights the team’s satisfaction with the overall system optimization: “The write\-time aggregation for ClickHouse has been particularly impressive for its query performance, making our internal dashboards appear really snappy.”


## The road ahead [\#](/blog/building-chronicle-how-temporal-supercharged-their-observability-with-clickhouse#the-road-ahead)


Building on the success of Chronicle, Temporal continues to explore ways of enhancing its observability. One potential area for improvement, Sean notes, is moving towards schemaless ingestion, which could reduce the overhead of managing table schemas as new data sources are onboarded. Another idea Temporal is exploring is the possibility of separating compute pools for querying and ingestion. This change would ensure that heavy queries don’t disrupt the ingestion process, leading to even greater system stability.


“I’m super excited about our use of ClickHouse at Temporal,” Sean says. As they continue to innovate, the team is confident that ClickHouse will remain a cornerstone of their observability strategy. Its flexibility and performance have already been crucial to scaling Chronicle, and the database promises to support the platform’s continued growth, allowing them to handle ever\-increasing data volumes with unmatched speed, efficiency, and scalability.


Want to learn more about ClickHouse and see how it can bring real\-time observability to your organization? [Try ClickHouse Cloud free for 30 days.](https://clickhouse.com/cloud)

**ClickHouse Cloud, powered by AWS**

ClickHouse Cloud on AWS uses Amazon Simple Storage Service (Amazon S3\), object storage for scalability, data availability, security, and performance. Amazon Elastic Compute Cloud (Amazon EC2\) is used for high performance and efficiency for data\-intensive workloads. AWS PrivateLink is used for secure connection between ClickHouse Cloud and the customer's VPC. ClickHouse Cloud also integrates with a wide range of other AWS services, including Amazon Managed Streaming for Apache Kafka, Amazon Quicksight, Amazon Relational Database Service, Amazon Glue and Amazon Kinesis.

![](/_next/image?url=%2Fuploads%2Faws_qualified_software_b95bcb6c3e.png&w=1080&q=75)[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
