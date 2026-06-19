# Backups \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. [Production Cluster Configuration Guide](/altinity-kb-setup-and-maintenance/cluster-production-configuration-guide/)
3. Backups
# Backups

ClickHouse® is currently at the design stage of creating some universal backup solution. Some custom backup strategies are:

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

Last modified 2024\.08\.13: [Fixed multiple typos here and there (9fb2290\)](https://github.com/Altinity/altinityknowledgebase/commit/9fb2290fbebcd92a3f79a7f321f13960ea89ebec)
