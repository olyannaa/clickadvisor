# Production Cluster Configuration Guide \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. Production Cluster Configuration Guide
# Production Cluster Configuration Guide

Moving from a single ClickHouse® server to a clustered format provides several benefits:

- Replication guarantees data integrity.
- Provides redundancy.
- Failover by being able to restart half of the nodes without encountering downtime.

Moving from an unsharded ClickHouse environment to a sharded cluster requires redesign of schema and queries. Starting with a sharded cluster from the beginning makes it easier in the future to scale the cluster up.

Setting up a ClickHouse cluster for a production environment requires the following stages:

- Hardware Requirements
- Network Configuration
- Create Host Names
- Monitoring Considerations
- Configuration Steps
- Setting Up Backups
- Staging Plans
- Upgrading The Cluster



---

##### [Backups](/altinity-kb-setup-and-maintenance/cluster-production-configuration-guide/hardening-clickhouse-security/)

##### [Cluster Configuration FAQ](/altinity-kb-setup-and-maintenance/cluster-production-configuration-guide/cluster-configuration-faq/)

##### [Cluster Configuration Process](/altinity-kb-setup-and-maintenance/cluster-production-configuration-guide/cluster-configuration-process/)

##### [Hardware Requirements](/altinity-kb-setup-and-maintenance/cluster-production-configuration-guide/hardware-requirements/)

##### [Network Configuration](/altinity-kb-setup-and-maintenance/cluster-production-configuration-guide/network-configuration/)

Last modified 2024\.07\.30: [Site cleanup, mostly minor changes (a4a9639\)](https://github.com/Altinity/altinityknowledgebase/commit/a4a96398d6e97ac2935110b426947487e2e202d9)
