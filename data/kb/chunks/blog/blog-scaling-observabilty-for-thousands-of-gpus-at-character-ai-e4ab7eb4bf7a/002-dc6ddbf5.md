---
source: blog
url: https://clickhouse.com/docs/use-cases/observability/clickstack/getting-started?loc=blog-o11y-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog
topic: scaling-observability-at-character-ai-thousands-of-gpus-10x-logs-and-50-lower-cost-with-clickstack
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 8
---

on, but no dedicated observability stack. As the only SRE for 8–9 months, responsible not just for inference infrastructure but also for mobile and web, he needed a simple and cost\-effective observability solution. ## Inside Character.AI infrastructure [\#](/blog/scaling-observabilty-for-thousands-of-gpus-at-character-ai#inside-characterai--infrastructure)

Character.AI runs one of the most demanding AI platforms in production today \- handling thousands of queries per second and 1 million concurrent connections, powered by thousands of GPUs across many Kubernetes clusters hosted in multiple cloud providers. Observability is fundamental to providing an operational service and also challenging due to the use of multiple cloud providers across multiple regions.

When Mustafa Yildirim joined, he inherited an impressive but fragmented infrastructure. Logs were split between multiple providers, which made debugging difficult, querying slow, and costs unpredictable.

The logs originate from a wide range of sources: backend microservices, mobile and web apps, and inference infrastructure. Backbone services create around 60% of logs and huge amounts of data \- unsampled and raw, these produce around 300 trillion log lines or 450 PB of raw text alone per month! Other microservices provide the remaining log data.

With a small team managing this system, simplicity and scalability are crucial. Mustafa made the decision early that logs needed to be sampled intelligently \- errors and warnings are stored in full, but info\-level logs from the backbone service are sampled at 1 in 10,000\. Other services follow a 1% sampling rate for info log level. This still produces around 50 billion log entries per month.

Mustafa's philosophy is clear here: retaining debug logs in production is rarely justified. If you need debug logs to solve an issue, the problem likely requires deeper investigation in staging. Instead, error logs should provide enough signal to identify, isolate, and reproduce the issue in staging, where full verbosity is enabled.

> "If you’re sending debug logs at our scale, you’re insane."

Thanks to this thoughtful design decision, Mustafa's team has ensured that centralized logging remains cost\-effective despite managing some of the largest scales seen in production AI systems today.

## Introducing ClickStack at Character.AI [\#](/blog/scaling-observabilty-for-thousands-of-gpus-at-character-ai#introducing-clickstack-at-characterai)
