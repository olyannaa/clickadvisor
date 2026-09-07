---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Clever
topic: clever-ingests-200x-more-logs-at-the-same-cost-with-clickhouse-cloud-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 6
total_chunks_in_doc: 7
---

[materialized view](https://clickhouse.com/docs/materialized-views) powers IntelliSense\-style autocomplete on log labels. The result, as Jake puts it, is a logging system that engineers can query without having to think about what's running underneath. ## 200x more logs, 0% cost increase \#

With ClickHouse in place, Clever has seen a 10x compression ratio on its 150 TB of monthly logs. And whereas Datadog was indexing just 10% of those logs, ClickHouse indexes all of them, amounting to a 200x increase in searchable log volume.

> "With ClickHouse, we see a compression ratio of 10x and a 200x increase in indexed logs. These logs are easily accessible to all engineers; they don't have to think about whether to go to Grafana, Athena, Datadog, or whatnot. And all of this came at a 0% increase in cost." — Jake Gutierrez, Sr Software Engineer, Clever

For anyone thinking about building something similar, Jake's advice is simple: just start. "Spin up ClickHouse locally and try it yourself," he says. "Even inserting random records into a table or backfilling some logs into a ClickHouse cluster helped me a lot." Jake also suggests running both systems in parallel initially. "That helped us guarantee we were moving to a system that was a step up from what we had," he says.

While Clever built a custom schema tailored to their structured JSON logs, not every team needs to start from scratch. For teams using OpenTelemetry, [ClickStack](https://clickhouse.com/docs/use-cases/observability/clickstack/overview) provides an optimized schema out of the box, designed to handle observability workloads at scales of tens of terabytes per day. Many of the techniques Clever adopted, including extracting frequently queried fields, using data skipping indexes, and optimizing sort order for common access patterns, are the same principles we recommend when tuning ClickStack for larger\-scale deployments.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-1158-get-started-today-sign-up&utm_blogctaid=1158)### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-global-cta&utm_blogctaid=0)

---

Share this post
