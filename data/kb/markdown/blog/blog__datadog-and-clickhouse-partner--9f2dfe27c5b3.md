# Datadog and ClickHouse partner to bring full\-fidelity data to modern observability


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Datadog and ClickHouse partner to bring full\-fidelity data to modern observability

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jun 10, 2026 · 5 minutes readObservability teams are collecting more data than ever. The rise of AI applications, agentic workflows, and increasingly distributed systems has driven telemetry volumes to levels that would have been difficult to imagine only a few years ago.


As a result, ClickHouse has increasingly become the database of choice for organizations looking to store and analyze observability data at scale, including [OpenAI](https://clickhouse.com/blog/why-openai-uses-clickhouse-for-petabyte-scale-observability), DoorDash, [Anthropic](https://clickhouse.com/blog/how-anthropic-is-using-clickhouse-to-scale-observability-for-ai-era), and Shopify, combining fast query performance with the cost efficiency needed for long\-term retention. At the same time, Datadog has established itself as one of the industry's most popular observability platforms.


Historically, organizations often had to choose between retaining complete telemetry datasets and keeping that data accessible through the tools their teams use every day. Decisions about retention periods, sampling strategies, and storage locations were frequently driven by cost considerations rather than operational requirements.


Today, we're excited to announce a new partnership between ClickHouse and Datadog that helps remove those tradeoffs. With new capabilities now available in Preview, organizations can route logs directly to ClickHouse through Datadog Observability Pipelines and search those logs from the Datadog Log Explorer, combining ClickHouse's economics and performance with the Datadog experience.


## Route logs to ClickHouse with Datadog Observability Pipelines [\#](/blog/datadog-and-clickhouse-partner#route-logs-to-clickhouse-with-datadog-observability-pipelines)


Datadog Observability Pipelines provides a flexible way to collect, process, and route telemetry from a wide range of sources. Supporting open standards, such as OpenTelemetry and OCSF, it enables organizations to centrally manage telemetry while retaining control over where data is stored.


![datadog_to_clickhouse.png](/uploads/datadog_to_clickhouse_28cf8ed604.png)
With a native ClickHouse destination, logs can now be routed directly into ClickHouse through Observability Pipelines. Before data reaches ClickHouse, teams can leverage parsing, enrichment, filtering, transformation, and redaction capabilities to ensure logs are structured consistently and contain the context needed for analysis.


These capabilities complement the OpenTelemetry Collector by providing an easy way to manage enrichment and routing at scale. Organizations can continue using Datadog's extensive collection ecosystem, including integrations and agents, while delivering telemetry into ClickHouse using OpenTelemetry\-compatible schemas.


The result is a flexible observability architecture optimized for high\-volume telemetry. Teams can investigate recent data through Datadog while retaining complete telemetry datasets in ClickHouse, enabling historical analysis, long\-range investigations, and access to full\-fidelity data without changing workflows. [ClickHouse Cloud’s separation of storage and compute](https://clickhouse.com/docs/cloud/reference/shared-merge-tree) allows organizations to retain that data at low cost, scale query resources independently, isolate workloads, and adapt capacity as requirements change without affecting retained data.


## Search ClickHouse logs directly from the Datadog Log Explorer [\#](/blog/datadog-and-clickhouse-partner#search-clickhouse-logs-directly-from-the-datadog-log-explorer)


Storage is only useful if data remains accessible when it is needed.


With federated log search, teams can search logs stored in ClickHouse directly from the Datadog Log Explorer. Logs remain in ClickHouse, eliminating the need to duplicate or re\-ingest data while preserving the workflows engineers already use for troubleshooting and investigation.


This approach provides several advantages.


First, organizations can retain significantly more telemetry for longer periods, ensuring historical data remains available when investigations require it. High\-volume logs that might otherwise be sampled, filtered, or discarded can remain searchable through Datadog while being stored in ClickHouse.


Second, teams can work from a single interface and continue to get the experience they already know with Datadog, combined with the scale and full\-fidelity telemetry retention of ClickHouse. Engineers no longer need to switch between multiple systems depending on where a particular dataset resides.


Finally, data stays where it was originally stored. Queries are executed against ClickHouse directly, avoiding the operational overhead of maintaining duplicate copies of telemetry.


## Bringing together the best of both platforms [\#](/blog/datadog-and-clickhouse-partner#bringing-together-the-best-of-both-platforms)


By combining ClickHouse and Datadog, teams can store and retain far more telemetry data while continuing to investigate, troubleshoot, and search through the workflows they already know. The result is a flexible observability architecture: Datadog provides the collection, user experience, and investigation capabilities that engineering teams rely on every day, while ClickHouse provides a scalable foundation for long\-term telemetry storage and analytics.


This partnership gives customers greater control over where their data lives, how long they retain it, and how they access it, without requiring them to compromise on performance, usability, or access to their data.


## Get started [\#](/blog/datadog-and-clickhouse-partner#get-started)


The native ClickHouse integration for Datadog Observability Pipelines and federated log search from the Datadog Log Explorer are available in Preview.


If you're interested in combining ClickHouse's scalable observability storage with Datadog's observability experience, you can request access to the private preview today via [https://www.datadoghq.com/product\-preview/federated\-search/](https://www.datadoghq.com/product-preview/federated-search/).

### Get started today

Interested in seeing how ClickStack works on your observability data? Get started with Managed ClickStack in ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?intent=o11y&loc=blog-cta-851-get-started-today-sign-up&utm_blogctaid=851)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_appoints_apac_leader_f2c3722e9c.jpg&w=828&q=75)Company and culture### [ClickHouse appoints new leader for Asia Pacific and expands global go\-to\-market leadership team](/blog/clickhouse-appoints-apac-leader-and-expands-global-gtm-leadership)

ClickHouse · Jun 8, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
