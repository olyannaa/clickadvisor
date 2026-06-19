---
source: blog
url: https://clickhouse.com/cloud/clickpipes/postgres-cdc-connector)**
topic: postgres-cdc-connector-for-clickpipes-is-now-in-private-preview
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 4
---

into ClickHouse and keeping millions of daily orders synced with just seconds of latency. We're really excited about PeerDB's native integration into ClickHouse Cloud via ClickPipes and all of the opportunities it opens up for us.” \- **[SpotOn](https://www.spoton.com/)**

> “We already reduced our Postgres to ClickHouse snapshot times from 10\+ hours down to 15 minutes with PeerDB. Combining ClickHouse’s powerful analytics natively with PeerDB’s real\-time data capture capabilities will greatly simplify our data processing workflows. This integration will enable us to build analytical applications faster, giving us a competitive edge in the market.” \- **[Vueling](https://www.vueling.com/)**

Without further ado, here is the demo of Postgres CDC connector in ClickPipes:

## Postgres \+ ClickHouse, a powerful data stack [\#](/blog/postgres-cdc-connector-clickpipes-private-preview#postgres--clickhouse-a-powerful-data-stack)

Using ClickHouse and PostgreSQL through a seamless CDC integration creates a powerful data stack by combining PostgreSQL's robust transactional capabilities with ClickHouse's high\-performance analytics. CDC ensures real\-time synchronization, allowing ClickHouse to handle fast queries on massive datasets without burdening PostgreSQL. This integration delivers real\-time insights and scalable analytics, making it an ideal solution for modern, data\-driven workflows. Below are a few main advantages of this architecture:

1. **Full workload isolation:** You can continue building your OLTP application on Postgres and your OLAP application on ClickHouse, with complete workload isolation—analytics will not affect your transactional workload.
2. **No compromises on features:** It also allows you to build your applications using the full capabilities and features (e.g., SQL coverage, performance, etc.) of both Postgres and ClickHouse, each optimized for a specific workload.

We believe customers derive the most value in solving real\-world data problems by leveraging purpose\-built databases like Postgres and ClickHouse as they were designed, with full flexibility, rather than relying on alternatives that retrofit one database engine into another, compromising the full feature set of each. We are observing a clear [trend](https://x.com/kiwicopple/status/1851638636590035054) towards the Postgres \+ ClickHouse architecture among real\-world customers.

## Key Benefits of the Postgres CDC connector [\#](/blog/postgres-cdc-connector-clickpipes-private-preview#key-benefits-of-the-postgres-cdc-connector)

The Postgres CDC connector in ClickPipes is purpose\-built for Postgres and ClickHouse, ensuring a fast, simple and a cost effective replication experience. Here are some key benefits for customers:

### Blazing Fast Performance [\#](/blog/postgres-cdc-connector-clickpipes-private-preview#blazing-fast-performance)
