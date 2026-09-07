---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"AI
topic: ai-is-redrawing-the-database-market-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 2
total_chunks_in_doc: 8
---

products can be built, what insights are accessible to your business. The question worth asking now is not just whether your current platform handles today's workloads, but whether it's the right foundation for what AI\-driven applications actually demand.

In a [previous post](https://clickhouse.com/blog/the-unbundling-of-the-cloud-data-warehouse), I wrote about the unbundling of the cloud data warehouse — how the shift toward interactive, customer\-facing applications exposed the architectural mismatch between batch\-oriented warehouses and real\-time workloads. What I want to describe here is the next wave of that disruption, across three markets: real\-time analytics, data warehousing, and observability.

![Data-platform-AI.png](/_next/image?url=%2Fuploads%2FData_platform_AI_67dafd4b5a.png&w=2048&q=75)

## Real\-time analytics: The dawn of the "best of breed" database \#

**Stakeholders: Developers building next\-generation user\-facing and AI\-powered applications**

Postgres has become the default database for building modern user\-facing applications, because of its superior ability to handle row\-oriented transactional data. This worked fine until applications became genuinely data\-intensive, driven by real\-time dashboards, usage analytics, customer\-facing metrics, event streams with millions of rows per second. For these increasingly analytical workloads, Postgres alone stopped scaling. The queries were too slow, the indexes too expensive, the concurrency too low.

The solution the industry landed on was Postgres \+ ClickHouse: Postgres for transactions and application state, ClickHouse for analytics. This pairing became the de facto modern data stack for any customer\-facing application with serious analytical requirements. ClickHouse evolved to be the obvious choice for analytical workloads: fast ingestion, sub\-second queries on billions of rows, efficient at the concurrency levels customer\-facing applications demand. The data moved from Postgres to ClickHouse via [CDC pipelines](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database), and ClickHouse powered everything from embedded product analytics to customer\-facing dashboards.

Now AI is accelerating the need for a best\-in\-class transactional and analytical base for building modern AI applications and agents that power them. LLM\-based features including AI\-generated insights, anomaly detection, recommendations, and natural language interfaces to product data, require a tighter feedback loop between transactional writes and analytical reads. This is why we are doubling down and [building a native Postgres \+ ClickHouse](https://clickhouse.com/blog/postgres-managed-by-clickhouse) data stack: a single unified experience where Postgres handles transactional workloads and ClickHouse handles analytics, tightly integrated at the engine level via a native extension – for automatic data replication and management and a unified developer experience.
