# How Critical Manufacturing uses ClickHouse to bring real\-time intelligence to the factory floor


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Critical Manufacturing uses ClickHouse to bring real\-time intelligence to the factory floor

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Mar 10, 2026 · 11 minutes read## Summary


div.w\-full \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

Critical Manufacturing uses ClickHouse to power real\-time analytics and operational intelligence, turning billions of shop\-floor events into sub\-second insights. By moving from SQL Server to ClickHouse Cloud, the team enabled fast Kafka\-based ingestion, real\-time dashboards, and scalable analytics with minimal overhead. ClickHouse now powers analytics, data storage, observability, and AI workloads, supported by optimizations like ELT, ReplacingMergeTree, denormalization, and TTL.

Manufacturing doesn't come with a pause button. When an ecommerce or SaaS dashboard lags, it's frustrating. When a factory dashboard lags, it can mean production sitting idle, defects slipping through inspections, or engineers losing precious time chasing the wrong root cause. Even a minute of downtime can cost thousands of dollars if it means teams don't have the accurate, real\-time data they need to make decisions on the factory floor.


That's the world [Critical Manufacturing](https://www.criticalmanufacturing.com/) operates in. The global, Portugal\-based company builds enterprise MES (Manufacturing Execution System) software for high\-tech manufacturers across semiconductors, electronics, medical devices, and industrial equipment. With more than 100 customers across dozens of countries and hundreds of installations worldwide, its platform supports 24/7 operations in factories where "real time" is the baseline.


"Our analytics capabilities directly impact customer productivity and efficiency," says lead software engineer Ricardo Magalhaes, who manages the company's IoT data platform. "We're constantly supporting events streaming from the shop floor."


We caught up with Ricardo to talk about the role of analytics in MES, Critical Manufacturing's journey from legacy stack to [ClickHouse Cloud](https://clickhouse.com/cloud), and how ClickHouse expanded from a single analytics use case into a platform layer across the business.


## The "nervous system" of the factory [\#](/blog/criticial-manufacturing#the-nervous-system-of-the-factory)


If you've spent time around software infrastructure, you've probably heard stories of telemetry pipelines, ad\-tech aggregation, and product analytics at massive scale. Manufacturing is a different ballgame, not because it's any less data\-driven, but because the systems being instrumented are physical.


Ricardo describes MES as "the nervous system of the factory floor." If enterprise planning systems like SAP determine what to make and when to make it, MES is where production becomes reality. It's responsible for tracking every unit through every step, managing equipment and operators, enforcing work instructions and recipes, and capturing the quality signals that determine whether the final product is usable.


In regulated industries like medical devices, MES is also the system of record for compliance and traceability, capturing which materials went into which finished goods, when they were processed, and what happened along the way, often years later.


For Critical Manufacturing, this creates what Ricardo calls "a huge data challenge." Every operator action is an event. Every quality measurement is an event. Every material movement is an event. Multiply that across machines, lines, and facilities, and MES becomes a deluge of millions of events captured minute by minute, machine by machine.


"Our analytics layer has to turn this firehose of data into actionable insights," Ricardo says. "It's extremely demanding in terms of infrastructure, and it has to be fast."


## Outgrowing the old system [\#](/blog/criticial-manufacturing#outgrowing-the-old-system)


Critical Manufacturing's old analytics system ran on Microsoft SQL Server. It worked for many years, but as the company's footprint expanded and customer expectations changed, the legacy approach couldn't scale to meet modern demands.


As Ricardo explains, today's operators have little use for static reports. They expect instant insights with sub\-second queries. They want slice\-and\-dice exploration across multiple lines, year\-to\-date calculations, long\-term historical trends, and ad hoc root\-cause analysis when something changes on the factory floor. "They don't have the patience to wait for a report," he says. "They don't have the patience to wait for anything."


Meanwhile, the rise of Industry 4\.0 is driving data volumes ever higher, pushing systems from millions to billions of records as more machines, sensors, and processes come online.


The result was predictable. Historical queries started taking too long—"sometimes hours," Ricardo says. Real\-time dashboards struggled to keep pace with production events. Tuning indexes and partitions became its own operational burden, as teams battled aggregation jobs and data maintenance work just to keep the system usable. Storage costs climbed as the system accumulated indexes designed to prevent further slowdowns.


As Ricardo puts it, there was nothing inherently broken about the old approach. "We simply outgrew it," he says.


## It all started on Reddit… [\#](/blog/criticial-manufacturing#it-all-started-on-reddit)


By 2022, Critical Manufacturing knew it needed a different approach—one that could ingest event streams, enable real\-time dashboards with sub\-second queries, support high\-volume aggregations, stay cost\-effective at scale, and be easy to maintain.


One evening, Ricardo was browsing Reddit when he stumbled across a /r/dataengineering thread describing a problem that looked much like his own: [time series](https://clickhouse.com/resources/engineering/what-is-time-series-database) at scale, [real\-time analytics](https://clickhouse.com/resources/engineering/what-is-real-time-analytics), and a traditional database that couldn't keep up.


At the time, Ricardo and the team were evaluating the "usual suspects"—Pinot, Druid, Databricks, Snowflake. Each had strengths, but as Ricardo puts it, "Every solution we tried came with heavy dependencies and huge operational overhead."


In the Reddit thread, someone commented: "Try ClickHouse." Ricardo had never heard of it, but he copied the link, emailed it to himself, and downloaded it the next morning.


"By lunchtime, I already had the first MES table created and loaded with production data," he says. "By the end of the day, I had my first [materialized view](https://clickhouse.com/docs/materialized-views) and was reading from a Kafka topic and writing into a [MergeTree table](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree). I was blown away."


Queries that had taken minutes on SQL Server returned in milliseconds. Even better, getting started was "remarkably straightforward," with no heavy dependencies or complex setup. A familiar SQL interface meant his team didn't need to relearn everything from scratch.


"As an engineer, I'm convinced the right tool shouldn't fight you," Ricardo says. "ClickHouse was the perfect fit for what we were doing. It just worked."


## From POC to platform layer [\#](/blog/criticial-manufacturing#from-poc-to-platform-layer)


That first day gave the team a POC, but as Ricardo says, "one day of testing was not enough to bet everything on." So they ran a formal evaluation—and ClickHouse continued to stand out.


[Native Kafka integration](https://clickhouse.com/docs/integrations/kafka) made it easy to move data from streaming topics into ClickHouse. [Columnar storage](https://clickhouse.com/resources/engineering/what-is-columnar-database) and [vectorized query execution](https://clickhouse.com/docs/development/architecture) delivered consistent performance under analytical load. [Compression](https://clickhouse.com/docs/data-compression/compression-in-clickhouse) and [TTL (time\-to\-live)](https://clickhouse.com/docs/guides/developer/ttl) policies enabled better storage efficiency and automated data lifecycle management. And [JSON support](https://clickhouse.com/docs/integrations/data-formats/json/overview) made it possible to handle semi\-structured event payloads without constant schema gymnastics.


After a couple weeks, he scheduled a meeting with his leadership team. He built a small prototype—Kafka in, ClickHouse in the middle, dashboards and queries on top—and walked them through it. His VP of Technology, who understood the challenges the team was facing, immediately got excited. After the meeting, Ricardo gave him access to ClickHouse's query interface so he could play around with it himself.


"He was blown away by the performance," Ricardo says. "He was able to slice and dice data very quickly. He said, 'This is a game\-changer. It will change the way we do analytics.'"


With technical confidence and business buy\-in, ClickHouse moved from POC to production, starting with analytics and quickly expanding across the business.


Today, ClickHouse powers Critical Manufacturing's operational data store for historical data and real\-time analytics. It stores manufacturing equipment telemetry like machine sensor data and state tracking, and supports correlation between shop\-floor events and environmental signals like air quality, humidity, and particle counts.


ClickHouse is also used internally for observability. Application logs, metrics, and traces flow into ClickHouse via [OpenTelemetry](https://clickhouse.com/resources/engineering/opentelemetry-otel), giving teams a unified place to troubleshoot and monitor systems that need to stay online around the clock.


As the company invests in AI\-driven capabilities, ClickHouse has begun to play a role there, too, storing embeddings that support RAG systems inside the product.


"We started with one analytics problem," Ricardo says. "Now, ClickHouse is everywhere."


## Key optimizations along the way [\#](/blog/criticial-manufacturing#key-optimizations-along-the-way)


The team has deployed ClickHouse flexibly across environments, supporting cloud and on\-prem installations to meet the needs of different manufacturers. They've also made a series of key optimizations to maximize performance and efficiency.


One big shift was moving from ETL to ELT. In the old system, transformations happened before loading. A bug in a metric definition could force the team to rerun aggregation pipelines from the beginning, sometimes taking hours or days. With ELT, they keep source data and apply transformations later, inside ClickHouse. "You simply correct your transformation and you're done," Ricardo says, adding that "ELT only works if your database is fast enough to transform at query time—this is one of ClickHouse's superpowers."


A second optimization was using [ReplacingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree) to manage late\-arriving events and duplicates, both of which are common in manufacturing, where devices can go offline and send data in bursts after reconnecting. By designing ordering keys carefully, the team can maintain state tables (current state of an entity) and history tables (full audit trails) while allowing ClickHouse to handle deduplication mechanics.


They've also leaned into [denormalization](https://clickhouse.com/docs/data-modeling/denormalization) to avoid join\-heavy relational query patterns. As Ricardo explains, manufacturing data is naturally relational, and it's common to see queries that require a dozen or more joins. But analytical columnar systems don't always love that shape. The team eliminated multi\-table joins by embedding relationship context into JSON fields, then extracting values at query time, improving performance and simplifying the developer experience.


Finally, [TTL\-based lifecycle automation](https://clickhouse.com/docs/guides/developer/ttl) replaced a patchwork of manual jobs and scripts. Hot data stays fast and accessible, while older data can expire or move to cheaper storage automatically. In environments where data retention, traceability, and cost control matter, that built\-in lifecycle management removes a major operational burden.


## What's next: high availability at scale [\#](/blog/criticial-manufacturing#whats-next-high-availability-at-scale)


A few years into their ClickHouse journey, Critical Manufacturing still has work to do. As Ricardo notes, the company is continuing to move workloads from SQL Server to ClickHouse, with a hard requirement that "if you lose data, it's a disaster."


Next on the roadmap is higher availability and resiliency. That means migrating toward [Replicated\* table engines](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replication) and building confidence in multi\-replica deployments, then expanding into sharding and replication patterns as footprint and customer demand grows.


For Ricardo, the throughline remains the same as that first day he discovered ClickHouse on Reddit. Manufacturing is becoming more connected, more instrumented, and more data\-driven, with every device, machine, and production lot generating signals worth capturing. "The workloads are really shifting, and the frontiers are blurring," he says.


The opportunity lies in what you can do with those signals once they're accessible. And in a world where the factory never stops, the data platform behind it can't stop either.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-97-get-started-today-sign-up&utm_blogctaid=97)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
