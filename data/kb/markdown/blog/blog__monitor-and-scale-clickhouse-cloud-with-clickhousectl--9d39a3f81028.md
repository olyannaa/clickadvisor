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



```
clickhousectl cloud service query --id "$SERVICE_ID" --query "
  SELECT event_time, query_duration_ms
  FROM clusterAllReplicas(default, system.query_log)
  WHERE type = 'QueryFinish'
    AND log_comment = 'frontend-dashboard'
  ORDER BY event_time DESC
  LIMIT 10"

```

Once you can see them, measuring the SLA is just an aggregation. Compute the p99 latency for exactly that workload over the last five minutes:



```
clickhousectl cloud service query --id "$SERVICE_ID" --query "
  SELECT
      toUInt64(quantile(0.99)(query_duration_ms)) AS p99_ms,
      count() AS queries
  FROM clusterAllReplicas(default, system.query_log)
  WHERE event_time > now() - INTERVAL 5 MINUTE
    AND type = 'QueryFinish'
    AND log_comment = 'frontend-dashboard'"

```

## Investigating a breach [\#](/blog/monitor-and-scale-clickhouse-cloud-with-clickhousectl#investigating-a-breach)


A breached SLA tells you that latency went up, but not why. There are two places to look, and they answer different questions. Sometimes it's a simple case of CPU/Memory being over\-utilised. Other times the hardware stats look fine, and you need to dig a little deeper into whats going on inside the database.


### Inside the database [\#](/blog/monitor-and-scale-clickhouse-cloud-with-clickhousectl#inside-the-database)


The first signal lives in ClickHouse itself. `system.query_log` doesn't just help you with the SLA query, you can ask questions about everything else that ran alongside it, too. That helps you to understand if something about the workload is changing.


Bucketing volume and latency by minute is a good place to start:



```
clickhousectl cloud service query --id "$SERVICE_ID" --query "
  SELECT
      toStartOfMinute(event_time) AS minute,
      count() AS queries,
      toUInt64(quantile(0.99)(query_duration_ms)) AS p99_ms
  FROM clusterAllReplicas(default, system.query_log)
  WHERE event_time > now() - INTERVAL 30 MINUTE
    AND type = 'QueryFinish'
    AND log_comment = 'frontend-dashboard'
  GROUP BY minute
  ORDER BY minute"

```

A common case can be an increase in query volume/concurrency. As your application grows, more users are actively viewing their dashboard, firing off more queries at the same.


If query volume climbed in lockstep with p99, you probably have a concurrency problem. If p99 rose while volume stayed flat, something *else* is competing for resources, and you can widen the same query (drop the `log_comment` filter, group by `log_comment` or `query_kind`) to find the heavy queries, ingestion, or merges crowding out your dashboard.


### System metrics [\#](/blog/monitor-and-scale-clickhouse-cloud-with-clickhousectl#system-metrics)


The second signal is resource pressure. To see whether the service is actually saturated, look at its metrics. ClickHouse Cloud exposes a [Prometheus\-compatible endpoint](https://clickhouse.com/docs/integrations/prometheus) per service. `clickhousectl` can help you take a quick peek:



```
clickhousectl cloud service prometheus "$SERVICE_ID" --filtered-metrics true

```

The snapshot is enough to get an idea of current state. For trends over time, point a standing Prometheus scraper at the same endpoint.


Pay particular attention to these metrics:




| Resource | Metric(s) | How to read it |
| --- | --- | --- |
| **CPU** | `ClickHouseAsyncMetrics_CGroupUserTimeNormalized` \+ `ClickHouseAsyncMetrics_CGroupSystemTimeNormalized`, vs. `ClickHouseAsyncMetrics_CGroupMaxCPU` | Sum the two normalized values to get cores in use. \~1\.0 \= one core saturated; approaching `CGroupMaxCPU` \= CPU maxed out. |
| **Memory** | `ClickHouseAsyncMetrics_CGroupMemoryUsed` ÷ `ClickHouseAsyncMetrics_CGroupMemoryTotal` | Fraction of the memory limit in use. Approaching 1\.0 \= memory pressure. |
| **Concurrency** | `ClickHouseMetrics_Query` | Queries executing right now, a quick proxy for how busy the service is. |


The state of the service helps you determine the right action to take. High concurrency with low memory suggests that you add replicas, we just need more cores to spread query concurrency over. Memory pinned near the limit on every replica suggests you need bigger replicas.


## Scaling with clickhousectl [\#](/blog/monitor-and-scale-clickhouse-cloud-with-clickhousectl#scaling-with-clickhousectl)


`cloud service scale` allows you to scale a ClickHouse Cloud service horizontally and vertically:



```
clickhousectl cloud service scale "$SERVICE_ID" \
  --min-replica-memory-gb 8 \
  --max-replica-memory-gb 16 \
  --num-replicas 3

```

`--num-replicas` is the horizontal dimension (how many replicas run in parallel). The `--min-replica-memory-gb` and `--max-replica-memory-gb` flags control vertical scaling. ClickHouse Cloud has native auto\-scaling that can vertically scale replicas when it sees resource pressure. Set them apart to let Cloud scale replicas up and down automatically; set them equal to fix the replica size. The example above runs 3 replicas, each free to scale between 8 and 16 GB.


## A simple cron [\#](/blog/monitor-and-scale-clickhouse-cloud-with-clickhousectl#a-simple-cron)


You could put this inside a simple cron:



```
#!/usr/bin/env bash
set -euo pipefail
SERVICE_ID="<your-service-id>"
SLA_MS=200

p99=$(clickhousectl cloud service query --id "$SERVICE_ID" --format TSV --query "
  SELECT toUInt64(quantile(0.99)(query_duration_ms))
  FROM clusterAllReplicas(default, system.query_log)
  WHERE event_time > now() - INTERVAL 1 MINUTE
    AND type = 'QueryFinish'
    AND log_comment = 'frontend-dashboard'")

if (( p99 > SLA_MS )); then
  echo "SLA breached: p99=${p99}ms > ${SLA_MS}ms. Scaling out"
  clickhousectl cloud service scale "$SERVICE_ID" --num-replicas 4
else
  echo "OK: p99=${p99}ms"
fi

```

Run it once a minute, and it can give you a super simple way to give your application some breathing room. But you'll have to think about the rest of the flow, too. Scaling back down if pressure eases, scaling further when needed, deciding between horizontal or vertical scaling, and so on.


## Using agents to investigate and remediate [\#](/blog/monitor-and-scale-clickhouse-cloud-with-clickhousectl#using-agents-to-investigate-and-remediate)


If you want to go beyond hard\-coded heuristics, it's an interesting use case for agents.


A cron might still be the right way to run the SLA\-check every minute. But if the SLA is breached, an agent can help to reason about what action to take.


The ClickHouse agent skills can help your agent to better use ClickHouse and `clickhousectl`. You can install them easily using `clickhousectl` itself:



```
clickhousectl skills --agent claude

```

The check itself can stay a cron, it's cheap and predictable. But instead of a hard\-coded `scale --num-replicas 4`, you can pass the failure to an LLM, giving it context about the failure, how to investigate, and what remediation options it should consider:



```
if (( p99 > SLA_MS )); then
  read -r -d '' PROMPT <<EOF || true
The 'frontend-dashboard' query latency SLA on ClickHouse Cloud service $SERVICE_ID
has just breached: p99 over the last minute is ${p99}ms against a ${SLA_MS}ms target.

You're the on-call agent. Work out WHY the SLA is breaching, then remediate it by
applying exactly one scaling action to the service. Let the evidence drive the choice.

What you have to work with (clickhousectl only):
  - SQL against the service's system tables. system.query_log is the richest source:
    one row per query, with its timing and memory use, each tagged with the workload
    it belongs to in the log_comment column ('frontend-dashboard' is the SLA workload):
      clickhousectl cloud service query --id $SERVICE_ID --format TSV --query "<SQL>"
  - Live resource pressure from Prometheus (CPU, memory, query concurrency, merges):
      clickhousectl cloud service prometheus $SERVICE_ID --filtered-metrics true

Your two scaling levers. Apply only ONE, whichever the root cause calls for:
  - Replica count:  clickhousectl cloud service scale $SERVICE_ID --num-replicas N
  - Replica size:   clickhousectl cloud service scale $SERVICE_ID --min-replica-memory-gb M --max-replica-memory-gb M

General advice on which scaling pattern to use:
- Prefer scaling vertically if cause is unclear.
- Scale vertically if latency is likely caused by resource contention from other queries.
- Scale horizontally if latency is caused by an increase in query concurrency or write throughput.

Apply one action, then explain the evidence you relied on and why that lever fits.
EOF

  printf '%s' "$PROMPT" | claude -p --model sonnet --allowedTools "Bash(clickhousectl:*)"
fi

```

### Use your own scaling policy [\#](/blog/monitor-and-scale-clickhouse-cloud-with-clickhousectl#use-your-own-scaling-policy)


You can take this further with your own rules and guidelines for scaling. Perhaps you want to guide the model not to scale beyond X replicas, or give it additional guidance on exactly what to look for (and how).


Creating a context file in Markdown, or encoding it inside a custom agent skill, is a great way to guide the agent towards more desirable behaviour.


### Auditing [\#](/blog/monitor-and-scale-clickhouse-cloud-with-clickhousectl#auditing)


Every action performed via `clickhousectl` lands in the ClickHouse Cloud activity log, so you get an audit trail for free:



```
clickhousectl cloud activity list

```

## Get clickhousectl [\#](/blog/monitor-and-scale-clickhouse-cloud-with-clickhousectl#get-clickhousectl)


Everything in this guide uses [`clickhousectl`](https://github.com/ClickHouse/clickhousectl), the ClickHouse CLI for local and cloud. It's the single tool for taking a project from your laptop to production: spinning up ClickHouse locally, building against it, and managing the Cloud service it eventually runs on.


Install with:
`curl https://clickhouse.com/cli | sh`

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
