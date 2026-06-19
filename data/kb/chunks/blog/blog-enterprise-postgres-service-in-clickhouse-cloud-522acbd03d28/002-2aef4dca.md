---
source: blog
url: https://clickhouse.com/cloud/postgres
topic: building-an-enterprise-postgres-service-in-clickhouse-cloud
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 4
---

strong availability, while offering lesser fault tolerance than a two\-standby quorum configuration. > An important architectural nuance: our HA standbys are not exposed for reads, ensuring that we prioritize failover readiness and data durability over opportunistic read scaling.

HA standbys are reserved strictly for failover and are not exposed for read traffic. Read traffic on standbys can compete with WAL replay, increasing replication lag, and can delay failover readiness. Long\-running queries on replicas can also interfere with VACUUM and bloat control on primary. We avoid those trade\-offs by keeping standbys focused solely for HA. If you need read scaling, **we provide separate read replicas designed specifically for that purpose**.

## Reliable CDC to ClickHouse (failover\-safe slots) [\#](/blog/enterprise-postgres-service-in-clickhouse-cloud#reliable-cdc-to-clickhouse-failover-safe-slots)

The service comes with native ClickHouse integration with built\-in Change Data Capture (CDC), enabling continuous replication of transactional data into ClickHouse for real\-time analytics. The integration is powered by ClickPipes/PeerDB, a battle tested replication engine supporting 100s of Postgres customers.

> A unique reliability feature of the service is built\-in failover replication slots, preventing resyncs on primary failover.

In most managed Postgres services, logical replication slots are tied to the primary instance. During high\-availability failovers, maintenance events, or scaling operations, these slots can be lost or require manual recreation, interrupting CDC pipelines and potentially forcing full re\-syncs.

Postgres by ClickHouse includes built\-in infrastructure for failover replication slots when syncing data to ClickHouse. These slots are preserved across HA failovers and scaling operations. As a result, CDC pipelines continue running without manual intervention or slot re\-creation when the primary changes, reducing the risk of costly resyncs on large databases.

## Backups, PITR and Forks [\#](/blog/enterprise-postgres-service-in-clickhouse-cloud#backups-pitr-and-forks)

High availability protects you from infrastructure failures. Backups protect you from everything else.

Every Postgres service includes **automatic backups** with support for **point\-in\-time recovery (PITR)** and **forks**. We use **WAL\-G**, a widely adopted open\-source tool, to take full base backups and continuously archive WAL to object storage (S3\-compatible). WAL\-G is well tuned to perform full backups and restores, as well as WAL archival and retrieval, in parallel to meet the high throughput demands of large\-scale workloads. We also use the [`wal-g` daemon](https://github.com/wal-g/wal-g/blob/master/docs/PostgreSQL.md#daemon), as it runs as a persistent process, eliminating per\-WAL process startup overhead and enabling efficient, low\-latency, and reliable WAL shipping under sustained write volumes.
