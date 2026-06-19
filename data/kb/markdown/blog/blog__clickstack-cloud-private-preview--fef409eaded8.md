# Introducing ClickStack Cloud: Serverless observability powered by ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Introducing ClickStack Cloud: Serverless observability powered by ClickHouse

![](/_next/image?url=%2Fuploads%2Fmike_shi_5b7145e7d7.jpg&w=96&q=75)[Mike Shi](/authors/mike-shi)May 27, 2026 · 8 minutes read## Summary

- ClickStack Cloud is a fully managed observability service built on ClickHouse, designed for teams that want ClickHouse\-powered observability without operating the underlying infrastructure.
- Teams point their OpenTelemetry Collector at a managed OTLP endpoint and can immediately explore logs, metrics, and traces in the ClickStack UI, with ingestion, buffering, scaling, and storage handled automatically.
- During private preview, we are building automatic schema tuning based on query patterns, with dedicated query compute for agentic workloads planned after preview completes.
Today, we’re announcing the private preview of **ClickStack Cloud**, a turn\-key observability offering built on ClickHouse.


ClickStack Cloud is designed for teams that want the performance, scale, and cost efficiency of ClickHouse for observability, without having to operate their own observability infrastructure.


Send OpenTelemetry data to a managed OTLP endpoint, then explore logs, metrics, and traces in the ClickStack UI. Teams can start investigating telemetry without managing collectors, sizing infrastructure, making scaling decisions, designing schemas, or becoming ClickHouse experts first.


If you want to use ClickHouse for observability, ClickStack Cloud is intended to be the default path: send telemetry data, start investigating, and let the platform handle the operational complexity underneath.

### What to try out ClickStack Cloud?

If you’re interested in trying ClickStack Cloud, please sign up for the preview program. [Sign up](https://clickhouse.com/cloud/clickstack-cloud-waitlist?loc=blog-cta-799-what-to-try-out-clickstack-cloud-sign-up&utm_blogctaid=799)## Why ClickStack Cloud [\#](/blog/clickstack-cloud-private-preview#why-clickstack-cloud)


Observability data are a natural fit for ClickHouse.


Logs, metrics, and traces are high\-volume, high\-cardinality, time\-series\-heavy datasets. Teams need to search across raw events, aggregate quickly, retain more data for longer, and correlate incidents with what is happening across their systems and business.


ClickHouse has already become a foundation for many modern observability architectures because it can deliver fast queries over large volumes of telemetry at a fraction of the cost of traditional approaches. ClickStack brought that power into a complete observability experience with OpenTelemetry\-native ingest and a purpose\-built UI.


ClickStack Cloud gives teams a fully turn\-key way to use ClickStack, backed by ClickHouse Cloud, without having to operate the underlying ingestion, storage, or query infrastructure themselves.


## Send OpenTelemetry data. Start observing. [\#](/blog/clickstack-cloud-private-preview#send-opentelemetry-data-start-observing)


With ClickStack Cloud, users send OpenTelemetry data to a managed endpoint. From there, ClickStack Cloud handles ingestion, buffering, scaling, storage, and query serving behind the scenes.


In practice, setup can be as simple as pointing your OpenTelemetry Collector at a ClickStack Cloud ingestion endpoint once you start your new ClickStack Cloud service:



```

```
1exporters:
2  otlphttp:
3    endpoint: https://your_service.otel.us-east-2.aws.clickhouse.cloud:4318
4    headers:
5      authorization: ${CLICKSTACK_CLOUD_TOKEN}
```

```

Once data is flowing, users can explore their logs, metrics, and traces all from the ClickStack UI, with integrated authentication and RBAC.


Teams can just focus on understanding and operating their production systems, not operating the systems that store and query their telemetry.


## A fully managed ingestion layer for OpenTelemetry [\#](/blog/clickstack-cloud-private-preview#a-fully-managed-ingestion-layer-for-opentelemetry)


The goal is a simple user experience. The hard part is making it scale seamlessly behind the scenes.


Observability traffic is bursty by nature. Incidents, deployments, cron jobs, customer behavior, and new instrumentation can all quickly change telemetry volume. A managed observability service needs to absorb those changes without asking users to resize infrastructure or debug ingest bottlenecks.


That is where ClickStack Cloud’s managed ingestion layer comes in. Users send telemetry to a managed endpoint, and ClickStack Cloud handles the ingestion path behind the service: buffering, scaling, storage, and delivery into ClickHouse.


Under the hood, telemetry is buffered through a durable event queue backed by object storage. A scalable ingestion layer then allocates resources based on incoming traffic patterns and ingestion pressure.


![ingestion_with_clickstack_cloud.png](/uploads/ingestion_with_clickstack_cloud_d98564d804.png)
For users, the experience stays simple: send OpenTelemetry data to ClickStack Cloud and let the platform manage the path from ingestion to queryable telemetry.


## What we are building during private preview [\#](/blog/clickstack-cloud-private-preview#what-we-are-building-during-private-preview)


ClickStack Cloud is entering private preview with managed ingestion, a serverless query experience, and the ClickStack UI for logs, metrics, and traces.


During private preview, we are focused on two areas that matter for high\-volume observability workloads: separating ingestion and query resources, and automatically tuning the underlying datastore, ClickHouse, based on how teams actually use it.


Observability systems have two very different jobs. They need to continuously ingest high\-volume telemetry data while serving fast, interactive queries for dashboards, investigations, and ad hoc analysis. These workloads do not scale the same way.


ClickStack Cloud builds on ClickHouse Cloud’s architecture, which separates compute and storage, allowing write infrastructure to scale independently of query infrastructure. During the private preview, we are refining how the system dynamically responds to each user's workload characteristics, such as ingestion pressure, query concurrency, and data density.


The goal is to let teams grow their observability workloads without having to size clusters, split services, or tune infrastructure themselves.


## Automatic tuning for observability workloads [\#](/blog/clickstack-cloud-private-preview#automatic-tuning-for-observability-workloads)


Observability workloads evolve as systems and teams change, which means the shape of the data that matters can shift quickly. A field that was rarely used last month might become central to every dashboard this month, while a new service can introduce attributes that teams begin relying on in their day\-to\-day investigations.


During the private preview, we are working on systems that can learn from common query patterns and automatically optimize telemetry data over time. Planned areas of automatic tuning include:


- Materializing frequently queried fields
- Adjusting primary keys based on common filters
- Adding materialized views for frequent access patterns
- Adding indexes for common dashboards and investigations


During private preview, we’ll refine these systems alongside design partners and early adopters based on real\-world feedback and usage


![](/uploads/clickstack_cloud_intro_may2026_image5_2d229af760.png)
The intent is straightforward: bring ClickHouse\-level performance to observability users without requiring every team to design schemas, tune indexes, or understand ClickHouse's internals.


## Built for agentic observability workloads [\#](/blog/clickstack-cloud-private-preview#built-for-agentic-observability-workloads)


As teams adopt AI agents for debugging, reliability, and operational analysis, observability systems will need to support workloads that look very different from traditional dashboards.


Dashboards usually run a known set of queries on a predictable cadence. Agents behave differently. They may issue many exploratory queries, test hypotheses across logs, metrics, and traces, move between raw events and aggregate views, and keep searching until they find the source of a problem.


This kind of workload does not fit well with observability platforms that rely on application\-level query caps, pre\-aggregates, rate limits, or fixed concurrency limits to control cost.


To support these exploratory workloads, we plan to let users attach dedicated query compute to their telemetry data for agentic and high\-volume analytical workloads. Instead of being limited by shared query capacity, teams would be able to provision the compute they need and run intensive analysis directly against their telemetry data.


![clickstack_cloud_intro_may2026_image3.png](/uploads/clickstack_cloud_intro_may2026_image3_8b7b2de915.png)
This gives teams more control: more compute when they need it, stronger isolation from their primary interactive observability experience, and a clearer relationship between query\-heavy agentic workloads and the infrastructure that serves them.


This capability is currently under active development and is expected to become available following the completion of the private preview.


## Who ClickStack Cloud is for [\#](/blog/clickstack-cloud-private-preview#who-clickstack-cloud-is-for)


ClickStack Cloud is for teams that want ClickHouse\-powered observability without operating observability infrastructure directly.


Our existing Managed ClickStack offering remains the right fit for teams that want direct control and management over schemas, ingestion pipelines, workload isolation, schema tuning, and compute sizing. For many large\-scale users, that control is essential, allowing users to achieve market\-leading cost efficiency.


ClickStack Cloud is designed for teams that want a more turn\-key path:


- Send OpenTelemetry data to a managed observability service
- Investigate logs, metrics, and traces without running ClickHouse infrastructure
- Avoid sizing ingestion, storage, and query components themselves
- Keep telemetry data close to the broader analytical workloads they run on ClickHouse
- Use ClickHouse as an observability backend without becoming ClickHouse operators


If your team wants the speed and efficiency of ClickHouse for logs, metrics, and traces, but does not want to manage the underlying infrastructure, ClickStack Cloud is built for you.


![clickstack_cloud_intro_may2026_image1.png](/uploads/clickstack_cloud_intro_may2026_image1_9f330af200.png)

> Pricing for ClickStack Cloud has not been finalized yet, but our philosophy is clear: it should be simple, predictable, and cost\-efficient at scale. We intend to finalize pricing during the private preview stage over the coming months.


## Join the private preview [\#](/blog/clickstack-cloud-private-preview#join-the-private-preview)


ClickStack Cloud is available today in private preview.


Private preview spots are limited. If you are interested in using ClickStack Cloud, sign up for the [preview program](https://clickhouse.com/cloud/clickstack-cloud-waitlist) and tell us about your observability workload.


We are looking for teams that want to send OpenTelemetry data, explore logs, metrics, and traces in ClickStack, and give feedback on the managed ClickStack Cloud experience.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
