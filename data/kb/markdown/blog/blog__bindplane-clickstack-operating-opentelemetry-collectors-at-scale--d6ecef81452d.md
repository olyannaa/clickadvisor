# Bindplane \+ ClickStack: Operating OpenTelemetry collectors at scale


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Bindplane \+ ClickStack: Operating OpenTelemetry collectors at scale

![](/_next/image?url=%2Fuploads%2FBindplane_icon_white_c04f9895a4.png&w=96&q=75)The Bindplane TeamJan 8, 2026 · 7 minutes read## Introduction [\#](/blog/bindplane-clickstack-operating-opentelemetry-collectors-at-scale#introduction)


ClickStack has already proven it can [operate at the extreme end of observability scale](https://clickhouse.com/blog/netflix-petabyte-scale-logging). Customers are ingesting telemetry at gigabytes per second and storing hundreds of petabytes in ClickHouse. At that level, the hard problem is often no longer query performance or storage efficiency, it’s [operating the fleets of OpenTelemetry Collectors](https://bindplane.com/solutions) required to feed [ClickHouse](https://clickhouse.com/) reliably.


Reaching those ingestion volumes typically means running large numbers of agent\-mode collectors close to application workloads and routing telemetry through centralized gateway\-mode collectors. As fleets grow, so does the operational overhead. Deployments become slower, configuration drift creeps in, upgrades get riskier, and troubleshooting turns into guesswork across thousands of collectors. Because ClickHouse ingestion scales directly with the number of collectors pushing data, collector management quickly becomes the bottleneck.


This is where the [Bindplane](https://bindplane.com/) \+ [ClickStack](https://clickhouse.com/use-cases/observability) integration comes in. It pairs ClickStack’s proven ingestion and analytical performance with centralized, OpenTelemetry\-native collector management. **The goal is simple: make it easier to run ClickStack at scale without turning collector management into a full\-time job.**


![bindplane_clickhouse.png](/uploads/bindplane_clickhouse_ef2016a24c.png)
## What is ClickStack? [\#](/blog/bindplane-clickstack-operating-opentelemetry-collectors-at-scale#what-is-clickstack)


ClickStack is a cloud\-native observability stack built on ClickHouse for high\-performance storage and querying of logs, metrics, and traces. It’s designed for teams dealing with large volumes of telemetry and high\-cardinality data, where traditional observability platforms either fall over or become cost\-prohibitive.


ClickStack focuses on horizontal scalability, efficient compression, and predictable query performance, even as data volumes grow into the petabyte range. It’s commonly used for log analytics, operational monitoring, and deep investigation of production systems where ingestion rate and retention really matter.


ClickStack consists of:


- **HyperDX UI**, a purpose\-built frontend for exploring and visualizing observability data
- **A custom\-built OpenTelemetry Collector**, with an opinionated schema for logs, metrics, and traces
- **ClickHouse**, the high\-performance analytical database at the core of the stack
![YouTube Video: WBe7ZwTRWuQ](/_next/image?url=https%3A%2F%2Fimg.youtube.com%2Fvi%2FWBe7ZwTRWuQ%2Fmaxresdefault.jpg&w=3840&q=75)### Learn about ClickStack

Explore the ClickHouse\-powered open source observability stack built for OpenTelemetry at scale. [Get started](https://clickhouse.com/use-cases/observability?loc=blog-cta-33-learn-about-clickstack-get-started&utm_blogctaid=33)## What is Bindplane? [\#](/blog/bindplane-clickstack-operating-opentelemetry-collectors-at-scale#what-is-bindplane)


[Bindplane](https://bindplane.com/) is an OpenTelemetry\-native telemetry pipeline built to [solve the operational side of telemetry](https://bindplane.com/use-case-demo). OpenTelemetry standardizes how data is collected and transported, but it doesn’t solve how you manage thousands of collectors safely and consistently. That’s the gap Bindplane fills.


Bindplane lets you collect, refine, and route metrics, logs, and traces from any source to any destination, while giving you centralized control over how collectors are configured, deployed, and upgraded.


Bindplane provides:


- Centralized management for thousands to over one million OpenTelemetry Collectors
- Visual configuration editing with safe, one\-click rollouts
- Pipeline intelligence and processor recommendations
- Real\-time filtering, sampling, enrichment, and data reduction
- 80\+ sources and 40\+ destinations across observability and security
- Vendor\-neutral, BYOC\-friendly control over your entire telemetry pipeline


It’s designed for teams running telemetry across cloud, hybrid, and on\-prem environments who need to scale without losing control.


## Why use Bindplane with ClickStack? [\#](/blog/bindplane-clickstack-operating-opentelemetry-collectors-at-scale#why-use-bindplane-with-clickstack)


While ClickStack addresses the data problem of observability, solving classic challenges around high cardinality, fast aggregations, and low\-latency queries with an integrated UI, operating observability at scale introduces a separate set of operational challenges.



> At scale, observability is as much an operational challenge as it is a data problem.


ClickStack is proven at extreme ingestion and storage volumes, with customers pushing gigabytes per second and managing hundreds of petabytes, but reaching these levels requires large fleets of agents distributed across edge environments and centralized gateways. As those fleets grow, deployment, configuration, upgrades, and consistency quickly become a major burden.


Bindplane addresses this challenge by centralizing agent orchestration and pipeline management. It simplifies rollouts and ongoing operations, making it far easier to run ClickStack reliably at enterprise scale. This value applies equally to open source users managing their own agents today and to ClickHouse Cloud users who need enterprise\-grade control as their workloads continue to grow.


## Bindplane now works with ClickStack [\#](/blog/bindplane-clickstack-operating-opentelemetry-collectors-at-scale#bindplane-now-works-with-clickstack)


With this integration, Bindplane can collect, transform, and route telemetry to ClickStack using OpenTelemetry standards. ClickStack becomes a first\-class destination inside a centrally managed telemetry pipeline.


This enables:


- **Simple setup** using Bindplane’s native ClickStack destination — no custom exporters or hand\-built configs
- **Automatic resource detection and enrichment** applied consistently before data reaches ClickStack
- **Fan\-out routing**, so the same telemetry streams can be sent to ClickStack and other observability or SIEM platforms at the same time
- **Full pipeline visibility**, including collector health, throughput, and end\-to\-end performance


At scale, ClickHouse performance is only as good as the collectors feeding it. Bindplane centralizes collector orchestration across large fleets, making deployments, configuration changes, and upgrades far easier to operate as ingestion grows. This matters for users running their own collector fleets and need enterprise\-grade collector management as their ClickStack deployments expand.


This is an important step forward for embedding both Bindplane and ClickStack into the broader OpenTelemetry ecosystem.


## Try Bindplane with ClickStack [\#](/blog/bindplane-clickstack-operating-opentelemetry-collectors-at-scale#try-bindplane-with-clickstack)


Follow these steps to get started:


1. Log in to your Bindplane account
2. Navigate to **Library**
3. Click **Add Destination**
4. Select **ClickStack** from the list
5. Authenticate and **configure connection** details
6. Give the **ClickStack Destination** a name


![bindplane_add_clickstack.png](/uploads/bindplane_add_clickstack_385dec0273.png)
### Create a configuration in Bindplane [\#](/blog/bindplane-clickstack-operating-opentelemetry-collectors-at-scale#create-a-configuration-in-bindplane)


Once your integration is connected, you can build a configuration to process and route telemetry:


1. Go to **Configurations** → **Create Configuration**
2. Give it a name, select the Agent Type, and Platform
3. Add a telemetry generator source to simulate traffic
4. Add the **ClickStack Destination**


![bindplane_configuration.png](/uploads/bindplane_configuration_2ed3faf4cd.png)
5. **Add an Agent ([BDOT Collector](https://docs.bindplane.com/readme/install-your-first-collector))** to the configuration
6. **Start a Rollout** to validate the configuration


![bindplane_adding_route.png](/uploads/bindplane_adding_route_cbda12de95.png)
7. From here, you can **add processors** for filtering, sampling, masking, enrichment, batching, and more, shaping telemetry before it ever hits ClickHouse.


![bindplane_add_processors.png](/uploads/bindplane_add_processors_7040a24ba6.png)
### Observe or monitor telemetry in ClickStack [\#](/blog/bindplane-clickstack-operating-opentelemetry-collectors-at-scale#observe-or-monitor-telemetry-in-clickstack)


As soon as the configuration is rolled out, telemetry starts flowing into ClickStack from your managed collector fleet. Because Bindplane handles enrichment and transformation upstream, the data arriving in ClickStack is consistent, structured, and ready for analysis.


You can now:


- View logs, metrics, and traces in ClickStack
- Build dashboards and alerts on top of high\-volume datasets
- Troubleshoot services end\-to\-end using correlated telemetry
- Analyze enriched telemetry processed consistently across your fleet


ClickStack focuses on what it does best; **ingestion, storage, and fast analytical queries**.


Bindplane **handles the operational complexity of running and managing fleets of collectors** feeding it. Together, they make scaling observability about data volume, not operational pain.


![ClickStack_data_bindplane.png](/uploads/Click_Stack_data_bindplane_981600829a.png)
## What's Next? [\#](/blog/bindplane-clickstack-operating-opentelemetry-collectors-at-scale#whats-next)


We're continuing to expand the Bindplane integration ecosystem to help teams build scalable, vendor\-neutral telemetry pipelines. Want to see a specific integration added? **Let us know in the [Bindplane Slack Community](https://www.launchpass.com/bindplane/free)!**


**[Try the Bindplane \+ ClickStack integration today](https://app.bindplane.com/login).**


**[For further information on this integration, you can read the documentation.](https://clickhouse.com/docs/use-cases/observability/clickstack/integration-partners/bindplane)**

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
