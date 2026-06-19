---
source: blog
url: https://github.com/ClickHouse/clickhousectl
topic: monitor-slas-and-scale-clickhouse-cloud-with-clickhousectl-and-agents
ch_version_introduced: '0.9'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 6
---

# Monitor SLAs and scale ClickHouse Cloud with clickhousectl and agents

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Monitor SLAs and scale ClickHouse Cloud with clickhousectl and agents

![Al Brown](/_next/image?url=%2Fuploads%2Fal_brown_headshot_09ae0cbce6.jpg&w=96&q=75)[Al Brown](/authors/al-brown)Jun 5, 2026 · 9 minutes readClickHouse Cloud makes it trivial to automatically scale your infrastructure up and down, horizontally or vertically, in response to resource pressure. But sometimes you want to go further and monitor SLAs on specific queries. Perhaps they're the queries fired off by your frontend app, and it degrades your user\-experience when latency exceeds \>200ms.

This guide shows you how to tag queries so you can calculate SLAs, then use [`clickhousectl`](https://github.com/ClickHouse/clickhousectl) to query and scale ClickHouse Cloud to investigate and fix breaches. You'll also see how you can pass this workflow off to an agent to investigate and remediate for you.

Try out the [runnable example](https://github.com/ClickHouse/examples/tree/main/ai/clickhousectl/agentic-sla-scaling).

## Setup [\#](/blog/monitor-and-scale-clickhouse-cloud-with-clickhousectl#setup)

[Install `clickhousectl`](https://clickhouse.com/docs/interfaces/cli) and use an API key to auth:

```
curl https://clickhouse.com/cli | sh

clickhousectl cloud auth login --api-key "$CLICKHOUSE_CLOUD_API_KEY" --api-secret "$CLICKHOUSE_CLOUD_API_SECRET"

```

Confirm you can see your services. The first column is the service ID you'll use everywhere else:

```
clickhousectl cloud service list

```

## Defining and measuring your SLA [\#](/blog/monitor-and-scale-clickhouse-cloud-with-clickhousectl#defining-and-measuring-your-sla)

First, you need to define your SLA and know how to measure it. An SLA is only useful if it's specific: a percentile, a latency target, and the queries it applies to. For a frontend dashboard, that might be *"p99 under 200 ms for the queries behind the main view"*. That's what we'll use for the example here.

The `system.query_log` records every query a ClickHouse service runs. The trick is to tag your queries so you can easily filter to them. Set [`log_comment`](https://clickhouse.com/docs/operations/settings/settings#log_comment) on the queries you want to track, and they become trivial to isolate later:

```
SELECT event_type, count(), avg(value), quantile(0.9)(value)
FROM events
WHERE event_type = 'purchase'
  AND event_time > now() - INTERVAL 1 DAY
GROUP BY event_type
SETTINGS log_comment = 'frontend-dashboard';

```

With the queries tagged, you can read them back from the log:
