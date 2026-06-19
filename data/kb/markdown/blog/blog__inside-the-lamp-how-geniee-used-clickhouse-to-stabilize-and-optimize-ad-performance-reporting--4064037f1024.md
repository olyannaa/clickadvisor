# Inside the lamp: How GENIEE used ClickHouse to stabilize and optimize ad performance reporting


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Inside the lamp: How GENIEE used ClickHouse to stabilize and optimize ad performance reporting

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Oct 3, 2024 · 7 minutes read
  



[GENIEE](https://en.geniee.co.jp/) is on a mission to create a world where anyone can succeed in marketing. Founded in Tokyo in 2010, the company offers a suite of ad tech and digital marketing solutions geared at helping publishers, advertisers, agencies, and app developers optimize their advertising strategies and maximize ad revenue.


In digital marketing, data is the cornerstone of an effective advertising strategy. GENIEE’s clients rely on vast amounts of real\-time data — from impressions and clicks to conversions and costs — to fine\-tune their campaigns and maximize returns. With billions of data points generated daily, GENIEE needs a database management system that can efficiently process, store, and analyze this information. This allows them to deliver accurate, real\-time insights, empowering advertisers to make informed decisions quickly.


Since 2017, ClickHouse has been core to GENIEE’s data operations, serving as its central reporting database. At a [June 2024 meetup in Tokyo](/videos/tokyo-meetup-accelerate-advertising-performance-reporting-with-clickhouse), engineer Takafumi Kataoka described the team’s recent decision to expand their use of ClickHouse to include data aggregation — a move that has led to faster reporting, improved system stability, and lower costs.


## Outgrowing the old system [\#](/blog/inside-the-lamp-how-geniee-used-clickhouse-to-stabilize-and-optimize-ad-performance-reporting#outgrowing-the-old-system)


Until 2021, GENIEE’s ad performance reporting system relied on a combination of Apache Kafka for streaming data and Apache Flink for data aggregation. In this setup, Flink handled the complex task of aggregating large volumes of advertising data, before passing it on to ClickHouse for reporting. However, as the scale of data grew, this system faced several persistent challenges that hampered efficiency and reliability.


One of the biggest issues was the frequent Flink failures. These disruptions caused incomplete or inaccurate reports, often requiring manual intervention from GENIEE’s engineering team to recount and verify data — a labor\-intensive and time\-consuming process. Reporting delays were another problem, with reports taking up to 40 minutes and sometimes longer to generate during peak hours, making it difficult to provide real\-time insights to clients.


![geniee-img1.png](/uploads/geniee_img1_31d67e3976.png)
*GENIEE’s old architecture: Data is streamed via Kafka, aggregated with Flink, and stored in ClickHouse for reporting.*


The old system also demanded extensive server resources, driving up operational costs as the team fought to maintain stability and performance. Engineers had to manually search through logs to diagnose issues, further slowing processes and adding to their workload.


“The situation was not ideal,” Takafumi says. “We wanted to address the root cause of the problem, but it wasn’t easy due to the complexity and scale of our data.”


They realized that to support GENIEE’s long\-term growth and deliver the cutting\-edge ad tech and digital marketing solutions clients expected from them, they needed a more stable and efficient database management solution.


## Choosing ClickHouse over BigQuery [\#](/blog/inside-the-lamp-how-geniee-used-clickhouse-to-stabilize-and-optimize-ad-performance-reporting#choosing-clickhouse-over-bigquery)


As Takafumi and the team set out to overhaul their ad performance reporting system, they looked at several alternatives, including Google BigQuery. But while BigQuery offered some benefits, GENIEE decided the best path was expanding their use of ClickHouse.


One of the main factors behind this decision was the team's familiarity with ClickHouse, which they had been using as their reporting database for several years. This long\-standing relationship and adoption of ClickHouse, including its advanced capabilities, allowed for a smoother transition as they expanded its use to include data aggregation.


Additionally, Takafumi says, ClickHouse offered superior cost efficiency — an important point as the company sought to reduce server resources and operational expenses.


By building on a system they already trusted and knew well, GENIEE was able to make a strategic choice that balanced performance, stability, and cost. The decision to use ClickHouse for both reporting and aggregation allowed them to fully optimize their data operations without the need for an entirely new platform.


“In the end, choosing ClickHouse over BigQuery was the correct decision,” Takafumi says.


## A new, better data architecture [\#](/blog/inside-the-lamp-how-geniee-used-clickhouse-to-stabilize-and-optimize-ad-performance-reporting#a-new-better-data-architecture)


GENIEE’s new data architecture is centered around two ClickHouse clusters — one for log aggregation and one for reporting — working in tandem to streamline and stabilize their data processing. Data flow starts with Kafka, which ingests real\-time data and routes it to ClickHouse for both aggregation and reporting. By centralizing these functions, GENIEE can now process massive amounts of ad performance data quickly and accurately.


![geniee-img2.png](/uploads/geniee_img2_7a7a462af7.png)
*GENIEE’s new architecture: Data is streamed via Kafka, aggregated and parsed with ClickHouse, and stored for real\-time reporting.*


Here’s a closer look at some of the system’s key components:


### Kafka table engine [\#](/blog/inside-the-lamp-how-geniee-used-clickhouse-to-stabilize-and-optimize-ad-performance-reporting#kafka-table-engine)


GENIEE continues to use Kafka for real\-time data ingestion, but now it routes the logs directly into ClickHouse via the [Kafka table engine](/docs/en/integrations/kafka/kafka-table-engine). This streamlined approach means the system can handle large volumes of incoming data with minimal latency.


### Materialized views [\#](/blog/inside-the-lamp-how-geniee-used-clickhouse-to-stabilize-and-optimize-ad-performance-reporting#materialized-views)


ClickHouse’s [materialized views](/docs/en/materialized-view) allow GENIEE to pre\-aggregate ad data like impressions and clicks, reducing query times from hours to minutes. The materialized views trigger automatic data parsing and aggregation, further simplifying the reporting process.


### SummingMergeTree engine [\#](/blog/inside-the-lamp-how-geniee-used-clickhouse-to-stabilize-and-optimize-ad-performance-reporting#summingmergetree-engine)


By leveraging ClickHouse’s [SummingMergeTree](/docs/en/engines/table-engines/mergetree-family/summingmergetree) engine, GENIEE has fully automated the aggregation of metrics like impressions and costs. This allows GENIEE to avoid the manual processing and recounting that plagued their old system.


### Dictionaries and metadata handling [\#](/blog/inside-the-lamp-how-geniee-used-clickhouse-to-stabilize-and-optimize-ad-performance-reporting#dictionaries-and-metadata-handling)


Using ClickHouse’s [dictionaries feature](/docs/en/sql-reference/dictionaries), GENIEE efficiently maps keys to attribute values, particularly for advertiser metadata. This reduces data duplication and speeds up real\-time lookups, further improving the overall efficiency of their data architecture.


## Speed, stability, and scalability [\#](/blog/inside-the-lamp-how-geniee-used-clickhouse-to-stabilize-and-optimize-ad-performance-reporting#speed-stability-and-scalability)


As Takafumi explains, GENIEE’s new ClickHouse\-centered data architecture has delivered a range of benefits across key areas of the business.


Whereas reports used to take hours to generate under the old system, those same queries are now completed in just a few minutes. This means GENIEE’s customers can make faster, more informed decisions, optimizing their advertising strategies and spend in real\-time.


System stability is also much improved. The frequent failures GENIEE experienced with Flink are now a thing of the past. By shifting to ClickHouse’s aggregation engine, GENIEE has simplified its data flow, reducing failure points and increasing system reliability.


Cost efficiency has been another big win, both operationally and financially. ClickHouse’s SummingMergeTree engine has allowed GENIEE to automate metric aggregation, eliminating the need for manual intervention and freeing up engineers to focus on more strategic, high\-value tasks. The new architecture is also far more resource\-efficient, requiring fewer servers and lowering the company’s infrastructure costs.


Overall, the new system has streamlined processes, improved reliability, cut costs, and allowed GENIEE to deliver more timely and valuable insights to their clients.


## Growing with ClickHouse [\#](/blog/inside-the-lamp-how-geniee-used-clickhouse-to-stabilize-and-optimize-ad-performance-reporting#growing-with-clickhouse)


Looking ahead, Takafumi says the team is excited to keep exploring and taking advantage of ClickHouse’s features. One area of focus is improving query performance even further by experimenting with features like projections and optimizing compression algorithms to reduce processing times. They’re also considering migrating from JSON to binary log formats, a move they hope will improve performance and make data processing even more efficient.


With ClickHouse’s flexibility and scalability, GENIEE is well\-positioned to keep growing and delivering faster, more reliable insights to clients. As the business evolves, Takafumi and the team are confident that ClickHouse will remain a cornerstone of their data infrastructure, allowing them to stay ahead as leaders in ad tech and digital marketing.


To learn more about ClickHouse and how it can make your data operations faster and more efficient, [try ClickHouse Cloud free for 30 days](/cloud) or [join our open\-source community](/docs/en/getting-started/quick-start).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
