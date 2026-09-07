---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"POSETTE
topic: posette-talk-recap-postgres-isn-t-slow-your-storage-is-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 5
total_chunks_in_doc: 6
---

fast but tied to the lifetime of a machine. Losing a node means losing its local copy of the data; instance\-store volumes cannot be snapshotted through the EBS API; and available capacity depends on the selected instance type.

The production architecture presented in the talk addresses this through three main requirements: replicate the database so the service can survive node loss, maintain backups and recovery data outside the individual machines, and plan capacity around the NVMe available on each instance type. Together, these patterns make it possible to run NVMe\-backed PostgreSQL confidently in production.

### High availability with two standbys \#

The first pattern is quorum\-based synchronous replication with two standby candidates. With a configuration such as `ANY 1 (standby1, standby2)`, a transaction can commit after either standby durably acknowledges its WAL rather than waiting for the slower of the two. Placing the nodes across availability zones protects against an AZ failure.

### Continuous backups to Object Storage for durability \#

For durability outside the database nodes, open\-source tools such as WAL\-G can provide physical base backups and continuous WAL archiving. With low\-latency WAL shipping, this architecture can target an RPO measured in seconds and support point\-in\-time recovery within the retention window.

Backups and WAL should also be kept in a separate failure domain, with another regional copy when the recovery plan needs to survive a full regional outage.

### Backups as the recovery foundation \#

Base backups and archived WAL are more than an emergency mechanism: the same recovery history can support point\-in\-time restores, isolated branches, deployment resizing, read\-replica seeding, and disaster recovery.

Backups and replication solve different problems. In the architecture described in the talk, standbys provide rapid failover, while backups protect against corruption, operator error, and cluster\-wide failure; both recovery paths need regular testing.

### Examples from production \#

This pattern is not only theoretical, the talk cites public examples from Instacart, which [has described PostgreSQL on NVMe](https://tech.instacart.com/how-instacart-built-a-modern-search-infrastructure-on-postgres-c528fa601d54) for a latency\-sensitive search workload, and Datadog, which [has discussed local\-NVMe PostgreSQL instances for workloads](https://postgresql.us/events/pgconfus2025/sessions/session/2064/slides/204/) that need them. The recurring pattern is local storage for performance, synchronous replication for availability, and independently stored base backups and WAL archives for recovery.

## The main takeaway \#
