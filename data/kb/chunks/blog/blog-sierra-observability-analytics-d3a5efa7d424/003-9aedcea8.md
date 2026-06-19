---
source: blog
url: https://clickhouse.com/resources/engineering/what-is-observability
topic: how-sierra-uses-clickhouse-to-bridge-observability-and-analytics
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 6
---

On one side is observability, optimized for speed and system health. SREs and DevOps teams monitor latency, errors, and alerts. Infrastructure engineers manage deployments and plan for capacity. Security and compliance teams handle audits and scan for anomalies.

On the other side is analytics, focused on longer\-term trends and user behavior. Product managers look at feature adoption and experiment results. Data analysts run segmentation and attribution reports. Executives track top\-line KPIs and forecast business performance.

These workflows are deeply interdependent, but they’ve rarely shared the same underlying systems. As Arup explains, “split stacks were a workaround, not a requirement”—a response to the technical limitations that existed before solutions like ClickHouse.

Observability stacks need millisecond query times and near\-zero ingestion lag. “We want queries to be fast, because we want to evaluate every minute if errors are above threshold,” he says. “And we want to know if the error happened within the last minute, not if it happened 10 minutes ago.” That often means limiting dimensionality, dropping high\-cardinality fields, and optimizing for fast alerts rather than deep exploration.

Analytics systems, by contrast, usually prioritize flexibility over speed, supporting complex joins, richer context, and long\-term storage. At most companies, the result is two different pipelines, two sets of dashboards, and two different ways of understanding what’s happening.

## Building the bridge with ClickHouse [\#](/blog/sierra-observability-analytics#building-the-bridge-with-clickhouse)

For Sierra, separating observability and analytics didn’t make sense. Because they use outcome\-based pricing, an HTTP error on a customer return API doesn’t just affect uptime; it impacts whether a user gets their issue resolved and whether the company gets paid.

“If the system is down and the transaction fails, we escalate to a human and don’t charge for that transaction,” Arup explains. “That’s a system metric directly tied to a business outcome.”

Rather than treat observability and analytics as different islands with competing priorities, Sierra began thinking of them as one unified data challenge—two views on the same event stream.

ClickHouse made that shift possible. Arup points to features like [columnar storage](https://clickhouse.com/docs/faq/general/columnar-database), [vectorized query execution](https://clickhouse.com/docs/development/architecture), and [materialized views](https://clickhouse.com/docs/materialized-views), saying: “All of those techniques let us run really, really fast queries at scale.” He also highlights ClickHouse’s “amazing real\-time ingestion,” with live dashboards and alerts made easier by integrations with [Kafka](https://clickhouse.com/docs/integrations/kafka), [Kinesis](https://clickhouse.com/docs/integrations/clickpipes/kinesis), and [S3](https://clickhouse.com/docs/integrations/s3).
