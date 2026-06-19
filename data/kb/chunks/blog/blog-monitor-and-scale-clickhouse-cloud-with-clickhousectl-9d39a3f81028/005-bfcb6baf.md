---
source: blog
url: https://github.com/ClickHouse/clickhousectl
topic: monitor-slas-and-scale-clickhouse-cloud-with-clickhousectl-and-agents
ch_version_introduced: '0.9'
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 6
---

a cron, it's cheap and predictable. But instead of a hard\-coded `scale --num-replicas 4`, you can pass the failure to an LLM, giving it context about the failure, how to investigate, and what remediation options it should consider:

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
