# How the D. E. Shaw group powers high\-cardinality observability at scale with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How the D. E. Shaw group powers high\-cardinality observability at scale with ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 15, 2026 · 10 minutes read## Summary

- The D. E. Shaw group uses ClickHouse to power high\-cardinality observability across millions of compute workloads running on its internal grid.
- During evaluations, ClickHouse outperformed alternatives by approximately 7x, enabling reliable long\-term analysis and capacity planning at scale. The production cluster operating with ClickHouse now handles ingestion of over 500k records per second, approximately the same as competitors in the evaluation, in anticipation of expanding throughput to support future projects.
- This enhanced observability provides deeper insight into key business decisions, helping teams evaluate compute efficiency and perform capacity planning. Expansion into tracing workloads shows improved compression and strong query performance gains.
Inside [the D. E. Shaw group](https://www.deshaw.com/), a global investment and technology development firm, millions of compute workloads run each month across a large high\-performance computing infrastructure. Researchers, engineers, and quantitative teams submit jobs ranging from short\-lived experiments to long\-running services, each consuming varying amounts of compute resources.


Understanding how those resources are used helps teams keep systems running smoothly while planning capacity and allocating compute efficiently across the organization. To support that visibility, the firm collects metrics for every task running on the grid, capturing both how much compute a workload requests and how much it ultimately consumes.


These metrics resemble [Prometheus\-style time\-series data](https://clickhouse.com/resources/engineering/what-is-time-series-database): measurements collected over time and labeled with metadata that identifies each task. But there's one important difference. Rather than aggregating metrics at the service or host level, the D. E. Shaw group tracks usage at the level of individual tasks, an approach that introduces [extremely high cardinality](https://clickhouse.com/resources/engineering/high-cardinality-slow-observability-challenge), something they found their existing solution was unable to accommodate.


We caught up with Mike Vasiliou, a Site Reliability Engineer at the D. E. Shaw group, to learn how the team approaches observability at this scale, and how ClickHouse became a key part of making high\-cardinality metrics practical for long\-term analysis and planning. In addition to being a customer, the D. E. Shaw group—through its D. E. Shaw Ventures team—recently invested in ClickHouse through one of its funds.


## Scaling the metrics platform [\#](/blog/deshaw#scaling-the-metrics-platform)


At first, the D. E. Shaw group's previous observability platform stored resource utilization metrics collected from cluster nodes. Each machine sent telemetry using InfluxDB line protocol, allowing teams to monitor usage and visualize performance through dashboards.


As the firm's needs evolved, the team saw an opportunity to improve their metrics platform further, using it to enable longer\-term capacity planning and strategic decision\-making. Their existing setup had served them well, but as data volume and granularity grew, they needed a platform built for a different scale. By preserving a unique task ID for every workload, the system captured the telemetry needed to understand compute usage at a fine level, but over time that approach produced millions of distinct time series. To support both that richness of detail and more expansive historical analysis, the team went looking for a platform designed for the task.


## Choosing ClickHouse [\#](/blog/deshaw#choosing-clickhouse)


The team kicked off an evaluation project to test competing databases capable of handling the D. E. Shaw group's growing high\-cardinality observability workload.


To create an even playing field, engineers benchmarked candidates using identical hardware and datasets, measuring both ingestion throughput and query performance.


"When we compared ClickHouse against competitors," Mike says, "ClickHouse was better pound\-for\-pound in pretty much every performance metric."


The difference was especially stark when it came to ingestion. A single node on a competing solution handled roughly 480,000 samples per second. ClickHouse ingested approximately 3\.5 million samples per second. In production, the D. E. Shaw group's cluster is already operating with throughputs of around 500,000 per second. The team saw ClickHouse's stronger ingestion performance as giving them more room to scale for future use cases.


Query performance reinforced the decision. "Some tested database solutions queries timed out after a minute, but similar ClickHouse queries completed in seconds," Mike says. "We also found that ClickHouse was the right choice for backfilling data." For a system designed to support long\-term analysis and capacity planning, ClickHouse's performance and reliability made it the clear winner.


As with any evaluation, there were tradeoffs. Because existing dashboards relied on Prometheus\-style queries, engineers had to translate workflows into SQL. "That piece of the project was tougher, but it was worth it," Mike says.


## A high\-cardinality observability platform [\#](/blog/deshaw#a-high-cardinality-observability-platform)


After selecting ClickHouse, the team focused on deploying it with minimal disruption to existing workflows.


Rather than changing how metrics are generated across the firm, they preserved the existing ingestion path. Grid nodes still send telemetry using InfluxDB line protocol, while an internal service batches incoming messages and inserts them into ClickHouse. This part of the migration was challenging, as it required a degree of custom development because of their desire to keep the Influx protocol and minimize disruption.


The D. E. Shaw group invested significant engineering effort in backfilling historical data into ClickHouse to support long term capacity planning. They initially attempted to rely on the query API in the previous time\-series platform, but this quickly proved impractical. The API could not deliver data at the required throughput, and the extraction process was neither performant nor resource efficient. They ultimately built custom tooling to read data files directly from disk, transform them into a column\-oriented format, and stream the results into ClickHouse. This approach provided the speed and efficiency needed to migrate large volumes of historical metrics data.


Metrics are organized into resource\-specific tables describing utilization of hardware components. Each record includes a unique task identifier, preserving visibility at the individual workload level. While the unique IDs introduce high entropy that limits compression efficiency for some fields (they still achieve up to 5x compression), they make querying more intuitive for users analyzing compute usage.


Today, the deployment stores roughly 68 TB of compressed metrics data spanning multiple years. The cluster runs across four replicated servers backed by NVMe storage, providing plenty of headroom for growth. The team has now onboarded multiple other datasets to the internal ClickHouse cluster, supporting an average insertion rate of 530k records per second, with spikes to over 1 million records. [Materialized views](https://clickhouse.com/docs/materialized-views) pre\-aggregate data for longer time horizons, powering dashboards used for historical analysis and capacity planning.


## From infrastructure to business impact [\#](/blog/deshaw#from-infrastructure-to-business-impact)


As longer retention and reliable aggregation became possible, observability at the D. E. Shaw group began to extend beyond infrastructure monitoring into operational decision\-making.


Each task running on the compute grid requests a specific allocation, which may be more or less than what it actually consumes. By storing both the requested and utilized amounts, teams can evaluate efficiency at the level of individual workloads or users. "The ability to measure efficiency is key for us," Mike explains, "because it affords a view on utilization rates that extends to allocation decisions."


If workloads consistently request more resources than they use, teams can adjust capacity accordingly. On the flipside, workloads that regularly exceed limits provide clear evidence for increasing quotas or provisioning additional compute.


At scale, the platform provides a shared source of truth about how much compute different models and research workloads consume over time. With this visibility, the firm can more accurately project future capacity needs and plan hardware purchases accordingly.


## Expanding into tracing and beyond [\#](/blog/deshaw#expanding-into-tracing-and-beyond)


Recently, the D. E. Shaw group has begun expanding ClickHouse into additional observability domains, starting with distributed tracing. Using [OpenTelemetry](https://clickhouse.com/resources/engineering/opentelemetry-otel), services now send trace data through centralized collectors that batch and forward events into ClickHouse.


The move to Grafana\-based exploration opens up new possibilities for how the team interacts with trace data. Users can search by service or trace ID, navigate system behavior more intuitively, and analyze large volumes of trace data without sacrificing performance.


ClickHouse's [compression](https://clickhouse.com/docs/data-compression/compression-in-clickhouse) played a big role in making the expansion possible. Trace datasets currently hover around a 12\.5x compression ratio. "The compression is a big deal for us," Mike says. "Relative to other data sources, we can compress more and consequently utilize less hardware."


At the moment, the team is dual\-writing traces, with plans to consolidate workflows once adoption is complete. Along with tracing, engineers are exploring broader event\-data pipelines for structured logs and analytics workloads where schemas are well understood, extending ClickHouse's role beyond metrics storage into a [unified observability platform](https://clickhouse.com/resources/engineering/what-is-observability).


## Getting the most out of ClickHouse [\#](/blog/deshaw#getting-the-most-out-of-clickhouse)


Although Mike cautioned that he doubts "a single observability tool will be the right fit for all use cases," he says that "we found ClickHouse to be a superior tool for enabling a top\-level view and detailed low\-level analysis of our high\-cardinality time\-series metrics data. I think teams seeking high\-performance observability platforms should certainly consider it as a candidate solution."


The key, he explains, is understanding how to take advantage of the system's design. "There are tools that are like an SUV where you'll get decent performance without thinking about it," he says. "ClickHouse is more like a racecar where you can get really, really fast performance, but you do need to put a little bit of effort into thinking about it."


That effort, he adds, isn't about complexity so much as familiarity. Once the team became comfortable with concepts like [MergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree) and [data modeling](https://clickhouse.com/docs/migrations/postgresql/data-modeling-techniques), ClickHouse became a powerful, dependable platform for observability and large\-scale analysis.


For teams facing similar challenges with high\-volume, high\-cardinality data, the D. E. Shaw group's experience shows that with the right design choices and analytical foundation, modern observability at massive scale becomes both practical and sustainable.

### Looking to revamp your observability stack?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-624-looking-to-revamp-your-observability-stack-sign-up&utm_blogctaid=624)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
