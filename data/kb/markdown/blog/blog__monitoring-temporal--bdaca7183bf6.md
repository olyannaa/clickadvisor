# Monitoring Temporal Cloud with ClickStack


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Monitoring Temporal Cloud with ClickStack

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_white_add9f20d0f.png&w=96&q=75)[The ClickStack Team](/authors/the-clickstack-team)Jan 28, 2026 · 4 minutes readWhen your mission\-critical workflows span days, weeks, or even months, every data observability data point counts. That's why we're excited to announce the integration between [ClickStack](https://clickhouse.com/use-cases/observability) and [Temporal Cloud's OpenMetrics endpoint](https://docs.temporal.io/cloud/metrics/openmetrics/), bringing high performance observability to your durable execution platform.


![temporal_dashboard.png](/uploads/temporal_dashboard_ed1d16163e.png)
## What is Temporal? [\#](/blog/monitoring-temporal#what-is-temporal)


Temporal is a durable execution platform that helps developers build reliable applications. Temporal lets you focus on business logic rather than writing complex error handling, retry logic, and state management code to survive failures.
Your business logic runs as a Temporal Workflow, whether that means processing payments, orchestrating agents, or managing long\-running shopping cart experiences. If a server crashes, the network fails, or a service goes down, Temporal automatically recovers and resumes execution exactly where it left off. No lost progress, no orphaned processes.


### What is ClickStack? [\#](/blog/monitoring-temporal#what-is-clickstack)


[ClickStack](https://clickhouse.com/docs/use-cases/observability/clickstack/getting-started) is a cloud\-native observability stack built on ClickHouse for high\-performance storage and querying of logs, metrics, and traces. It’s designed for teams dealing with large volumes of telemetry and high\-cardinality data, where traditional observability platforms either fall over or become cost\-prohibitive.


ClickStack focuses on horizontal scalability, efficient compression, and predictable query performance, even as data volumes grow into the petabyte range. It’s commonly used for log analytics, operational monitoring, and deep investigation of production systems where ingestion rate and retention really matter.

### Get started with ClickStack

Explore the ClickHouse\-powered open source observability stack built for OpenTelemetry at scale.[Get started](https://clickhouse.com/o11y?loc=blog-cta-46-get-started-with-clickstack-get-started&utm_blogctaid=46)ClickStack consists of:


- **HyperDX UI**, a purpose\-built frontend for exploring and visualizing observability data
- **A custom\-built OpenTelemetry Collector**, with an opinionated schema for logs, metrics, and traces
- **ClickHouse**, the high\-performance analytical database at the core of the stack
![YouTube Video: WBe7ZwTRWuQ](/_next/image?url=https%3A%2F%2Fimg.youtube.com%2Fvi%2FWBe7ZwTRWuQ%2Fmaxresdefault.jpg&w=3840&q=75)## Why ClickStack and Temporal Cloud belong together [\#](/blog/monitoring-temporal#why-clickstack-and-temporal-cloud-belong-together)


Running Temporal at scale means managing potentially thousands of concurrent workflows, each with its own activities, timers, and state transitions. When something goes wrong, or when you need to optimize performance, you need to be able to navigate the wealth of observability information coming out of the system.


This is where ClickStack helps. Built on ClickHouse, ClickStack handles the high cardinality metrics that Temporal generates with ease. ClickStack processes queries across Task Queues, Workflow Types, and Namespaces in milliseconds, so you can get to the needle in the haystack quickly.


For teams already running ClickStack, adding Temporal metrics means unified observability. Alternatively, for users running Temporal, ClickStack offers an out\-of\-box open\-source observability solution that users can [get started with in minutes](https://clickhouse.com/docs/use-cases/observability/clickstack/getting-started). Understand how the health of a database affects Task processing backlogs. Track how deployment changes affect Workflow latency. Build dashboards that show the complete picture of your system's health.


## Getting started: Connecting Temporal Cloud to ClickStack [\#](/blog/monitoring-temporal#getting-started-connecting-temporal-cloud-to-clickstack)


The integration uses the [OpenTelemetry Collector's Prometheus receiver](https://opentelemetry.io/docs/collector/configuration/#receivers) to scrape metrics from Temporal Cloud. [Full instructions on how to set up the integration are available](https://clickhouse.com/docs/use-cases/observability/clickstack/integrations/temporal-metrics), but the gist is once you have a Temporal Cloud API Key that has permission to read metrics, you create the configuration file in the OpenTelemetry Collector like this:


```
1receivers:
2  prometheus/temporal:
3    config:
4      scrape_configs:
5      - job_name: 'temporal-cloud'
6        scrape_interval: 60s
7        scheme: https
8        authorization:
9          type: Bearer
10          credentials_file: <TEMPORAL CLOUD API KEY PATH>
11        static_configs:
12          - targets: ['metrics.temporal.io']
13        metrics_path: '/v1/metrics'
14
15processors:
16  resource:
17    attributes:
18      - key: service.name
19        value: "temporal"
20        action: upsert
21
22service:
23  pipelines:
24    metrics/temporal:
25      receivers: [prometheus/temporal]
26      processors: [resource, memory_limiter, batch]
27      exporters: [clickhouse]
```
Once deployed, open the ClickStack UI, HyperDX, and navigate to the Metrics explorer. Search for metrics starting with `temporal_cloud` to confirm data is flowing. You can import the [pre\-built Temporal dashboard](https://clickhouse.com/docs/use-cases/observability/clickstack/integrations/temporal-metrics#dashboards) and immediately visualize Workflow success rates, Actions consumption against your limits, and Task Queue backlogs.


## What's Next [\#](/blog/monitoring-temporal#whats-next)


With Temporal metrics flowing into ClickStack, you can set up alerts on critical thresholds, build custom dashboards for your specific workflow patterns, and correlate workflow performance with the rest of your observability data.


For full configuration details and troubleshooting guidance, check out the [complete documentation](https://clickhouse.com/docs/use-cases/observability/clickstack/integrations/temporal-metrics).


Your durable workflows deserve scalable observability. With ClickStack and [Temporal Cloud](https://temporal.io/cloud) working together, you get both.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
