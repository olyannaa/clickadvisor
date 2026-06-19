---
source: kb.altinity.com
url: https://clickhouse.tech/docs/en/sql-reference/statements/alter/partition/#alter_freeze-partition
topic: production-cluster-configuration-guide-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 8
---

# Production Cluster Configuration Guide \| Altinity® Knowledge Base for ClickHouse®

This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-setup-and-maintenance/cluster-production-configuration-guide/).

# Production Cluster Configuration Guide

Production Cluster Configuration Guide- 1: [Backups](#pg-202b7e3651622a4779b38f52cef739a7)
- 2: [Cluster Configuration FAQ](#pg-8064c7d414e643fb87b3e0939260d98f)
- 3: [Cluster Configuration Process](#pg-839cbf636b5f8a35c6823f41977447f7)
- 4: [Hardware Requirements](#pg-3754a72a1a168184ed696d361b761145)
- 5: [Network Configuration](#pg-414e2937f5573cccbd17d35a64e42c62)

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
# 1 \- Backups

BackupsClickHouse® is currently at the design stage of creating some universal backup solution. Some custom backup strategies are:

1. Each shard is backed up separately.
2. FREEZE the table/partition. For more information, see [Alter Freeze Partition](https://clickhouse.tech/docs/en/sql-reference/statements/alter/partition/#alter_freeze-partition)
.
	1. This creates hard links in shadow subdirectory.
3. rsync that directory to a backup location, then remove that subfolder from shadow.
	1. Cloud users are recommended to use [Rclone](https://rclone.org/)
	.
4. Always add the full contents of the metadata subfolder that contains the current DB schema and ClickHouse configs to your backup.
5. For a second replica, it’s enough to copy metadata and configuration.
6. Data in ClickHouse is already compressed with lz4, backup can be compressed bit better, but avoid using cpu\-heavy compression algorithms like gzip, use something like zstd instead.

The tool automating that process: [Altinity Backup for ClickHouse](https://github.com/Altinity/clickhouse-backup)
.

# 2 \- Cluster Configuration FAQ

Cluster Configuration FAQ## ClickHouse® does not start, some other unexpected behavior happening

Check ClickHouse logs, they are your friends:

tail \-n 1000 /var/log/clickhouse\-server/clickhouse\-server.err.log \| less
tail \-n 10000 /var/log/clickhouse\-server/clickhouse\-server.log \| less

## How Do I Restrict Memory Usage?

See [our knowledge base article](http://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-memory-configuration-settings/)
and [official documentation](https://clickhouse.tech/docs/en/operations/settings/query-complexity/#settings_max_memory_usage)
for more information.

## ClickHouse died during big query execution
