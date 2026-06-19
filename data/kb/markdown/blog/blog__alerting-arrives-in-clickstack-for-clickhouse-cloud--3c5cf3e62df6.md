# Alerting arrives in ClickStack for ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Alerting arrives in ClickStack for ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fmike_shi_5b7145e7d7.jpg&w=96&q=75)[Mike Shi](/authors/mike-shi)Nov 5, 2025 · 3 minutes read## TLDR;

Alerting is now available in ClickStack for ClickHouse Cloud, bringing feature parity with the open source version and eliminating the need for custom setup.


Users in the private preview can create search\-based or chart\-based alerts directly in the HyperDX UI, across logs, metrics, and traces. Alerts integrate out\-of\-the\-box with Slack, PagerDuty, and webhooks, helping teams respond to spikes in latency, errors, or KPIs in real time.

Back in August, [we announced ClickStack in ClickHouse Cloud](https://clickhouse.com/blog/announcing-clickstack-in-clickhouse-cloud), marking the start of a unified future for observability and analytics. Since then, we’ve been busy onboarding customers, scaling the HyperDX UI to handle petabyte\-scale workloads, and delivering enterprise features.


Today, we're excited to share one of the most requested capabilities \- alerting, which is now available for ClickStack users in ClickHouse Cloud.

## What's new: Alerting in ClickHouse Cloud [\#](/blog/alerting-arrives-in-clickstack-for-clickhouse-cloud#whats-new-alerting-in-clickhouse-cloud)


Users participating in the private preview can now create and manage alerts directly within the HyperDX interface. These alerts work seamlessly across your ClickStack signals:  logs, metrics, and traces, and integrate with the notification tools you already use.


Out\-of\-the\-box, ClickStack alerting supports Slack, PagerDuty, and generic webhooks, giving you the flexibility to connect any system or workflow. Whether you’re monitoring latency spikes, error rates, or business KPIs stored in ClickHouse, alerting helps you take action immediately.


![clickstack-webhook.png](/uploads/clickstack_webhook_9f59806558.png)
## Why alerting matters [\#](/blog/alerting-arrives-in-clickstack-for-clickhouse-cloud#why-alerting-matters)


This release achieves feature parity with open\-source ClickStack, while simplifying setup for ClickHouse Cloud users. There’s no infrastructure to manage, and no custom configuration is required \- alerting just works, right from the Cloud\-hosted ClickStack UI in HyperDX.


We've also made optimizations to the UI and backend services to ensure alert processing scales with the size and performance demands we see in ClickHouse Cloud.

### Get started with ClickStack

Deploy the world’s fastest and most scalable open source observability stack, with one command.
[Get Started](https://clickhouse.com/o11y?loc=blog-cta-4-get-started-with-clickstack-get-started&utm_blogctaid=4)## Alerting in ClickStack [\#](/blog/alerting-arrives-in-clickstack-for-clickhouse-cloud#alerting-in-clickstack)


ClickStack alerting in ClickHouse Cloud offers flexible ways to detect and respond to issues in real time.


Within the HyperDX UI, users can create alerts in two ways \- search\-based or chart\-based.


**Search\-based** alerts let you define a query using either SQL or Lucene syntax, then specify a threshold for the number of matching events over a given time window for a grouping column e.g., Service name. When the count rises above or falls below that threshold for any of the lines produced by the GROUP BY, the alert triggers automatically \- sending an event to the configured Webhook.


![create-clickstack-alert.png](/uploads/create_clickstack_alert_2fc88a80ab.png)
For more advanced use cases, you can build **chart\-based alerts** directly from dashboards, powered by full SQL aggregations. This allows users to leverage any ClickHouse function for rich aggregations and statistical calculations. When a computed metric again exceeds a threshold, an alert can be fired for the chart.


For example, consider our public [ClickPy demo environment](https://clickpy.clickhouse.com), which provides analytics for Python package downloads.


This public\-facing demo has been instrumented with OpenTelemetry tracing to allow us to debug performance issues. Using this data, we can visualize query performance across user interactions in the public application. In this example, we track the 99th percentile of query latency and configure an alert to trigger whenever it exceeds a defined threshold \- signaling that users may be experiencing slower performance.

Loading video...
> Note: to add an alert, the underlying dashboard for the chart must be saved.


## Looking forward: What's next for ClickStack [\#](/blog/alerting-arrives-in-clickstack-for-clickhouse-cloud#looking-forward-whats-next-for-clickstack)


Looking ahead, we’ll continue expanding ClickStack alerting with broader integrations such as email, and more advanced alerting logic, such as anomaly detection, to support richer use cases.


We’re also exploring dedicated compute pools for alerts, allowing users with large\-scale alerting needs to leverage [ClickHouse warehouses](https://clickhouse.com/docs/cloud/reference/warehouses) to isolate alert processing from their primary read and write workloads.


## Conclusion [\#](/blog/alerting-arrives-in-clickstack-for-clickhouse-cloud#conclusion)


Users in the private preview can now explore alerting in ClickStack integration for ClickHouse Cloud and enjoy the same powerful, ClickHouse\-powered alerts available in the open source version.


If you’d like to join the private preview, reach out to your ClickHouse account rep or complete the [interest form](https://clickhouse.com/cloud/clickstack-private-preview).

### Subscribe to our observability newsletter

Stay informed on feature ClickStack releases, roadmap, and community events!Loading form...Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
