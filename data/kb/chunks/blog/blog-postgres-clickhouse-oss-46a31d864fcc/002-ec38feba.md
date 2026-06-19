---
source: blog
url: https://clickhouse.com/blog/postgres-managed-by-clickhouse
topic: postgresql-clickhouse-as-the-open-source-unified-data-stack
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 4
---

analytics queries on ClickHouse directly from PostgreSQL without rewriting any SQL. These four components come together to form the open source unified data stack. Below is a high\-level overview of the stack. ![postgres-oss-diagram-1.jpg](/uploads/postgres_oss_diagram_1_e72845a9a9.jpg) ### Implementing the stack [\#](/blog/postgres-clickhouse-oss#implementing-the-stack)

Running PostgreSQL and ClickHouse side by side is a well established pattern. Many teams use this architecture in production, and GitLab [described it publicly](https://about.gitlab.com/blog/two-sizes-fit-most-postgresql-and-clickhouse/) as early as 2022\. Depending on the workload, the implementation falls into two main patterns, Change data capture or split\-writes.

#### Change data capture (CDC) [\#](/blog/postgres-clickhouse-oss#change-data-capture-cdc)

**Components**: Postgres, ClickHouse, PeerDB and pg\_clickhouse (optional).

This approach is well suited for operational, real\-time analytical workloads where analytics run directly on application data. Common use cases include retail platforms, financial systems, and CSM or CRM applications.

PostgreSQL remains the system of record. All writes go to PostgreSQL, while PeerDB streams inserts, updates, and deletes into ClickHouse using CDC. ClickHouse maintains a near real\-time copy of the data, allowing analytical queries to run on the latest state without adding additional load to the transactional database.

Applications can continue to send both transactional and analytical queries to PostgreSQL thanks to pg\_clickhouse which transparently offloads analytical queries to ClickHouse. This keeps application changes minimal. Alternatively, applications can query ClickHouse directly if needed.

**Customer examples**: [Seemplicity](https://clickhouse.com/blog/seemplicity-scaled-real-time-security-analytics-with-postgres-cdc-and-clickhouse), [Sewer AI](https://clickhouse.com/blog/sewerai-sewer-management-at-scale)

![postgres-oss-diagram-2.jpg](/uploads/postgres_oss_diagram_2_9a4ab8724a.jpg)
### Split\-writes [\#](/blog/postgres-clickhouse-oss#split-writes)

**Components**: PostgreSQL, ClickHouse, and pg\_clickhouse (optional).

This pattern is commonly used for observability or event\-based workloads, where analytical data consists of logs, metrics, or events. These datasets do not require transaction support and are written at high volume.

In this case, analytical data can be written directly to ClickHouse, or routed through PostgreSQL using pg\_clickhouse when minimal application change is preferred. PostgreSQL is not the system of record for this data and does not need to store the full analytical dataset.

Querying follows the same model as the CDC approach. Analytical queries run on ClickHouse, either transparently offloaded from PostgreSQL via pg\_clickhouse or issued directly to ClickHouse.

**Customer examples**: [Langfuse](https://clickhouse.com/blog/langfuse-and-clickhouse-a-new-data-stack-for-modern-llm-applications), [Langchain](https://clickhouse.com/blog/langchain-why-we-choose-clickhouse-to-power-langchain)

![postgre-oss-diagram-3.jpg](/uploads/postgre_oss_diagram_3_4452977ed6.jpg)
## Get started locally [\#](/blog/postgres-clickhouse-oss#get-started-locally)

Whether you're implementing a new application or extending an existing PostgreSQL application, getting started locally is straightforward. The [Getting started guide](https://github.com/ClickHouse/postgres-clickhouse-stack?tab=readme-ov-file#getting-started) explains how to run the stack locally. Once you have it running locally, you can simply connect your application to the [exposed PostgreSQL database instance](https://github.com/ClickHouse/postgres-clickhouse-stack?tab=readme-ov-file#connect-to-postgresql).
