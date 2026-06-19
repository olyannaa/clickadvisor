---
source: kb.altinity.com
url: https://altinity.com/clickhouse-upgrade-overview/
topic: system-tables-ate-my-disk-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 3
---

(event_date)` in this case TTL expression `event_date + INTERVAL 14 DAY DELETE` expires all rows at the same time. In this case ClickHouse drops whole partitions. Dropping of partitions is very easy operation for CPU / Disk I/O.

Usual TTL processing (when table partitioned by toYYYYMM and TTL by day) is heavy CPU / Disk I/O consuming operation which re\-writes data parts without expired rows.

You can [add TTL without ClickHouse restart](/altinity-kb-queries-and-syntax/ttl/modify-ttl/)
(and table dropping or renaming):

```
ALTER TABLE system.query_log MODIFY TTL event_date + INTERVAL 14 DAY;

```
But in this case ClickHouse will drop only whole monthly partitions (will store data older than 14 days).

## One more way to configure TTL for system tables

This way just adds TTL to a table and leaves monthly (default) partitioning (will store data older than 14 days).

```
$ cat /etc/clickhouse-server/config.d/query_log_ttl.xml
<?xml version="1.0"?>
<clickhouse>
    <query_log>
        <database>system</database>
        <table>query_log</table>
        <ttl>event_date + INTERVAL 30 DAY DELETE</ttl>
    </query_log>
</clickhouse>

```
💡 For the [clickhouse\-operator](https://github.com/Altinity/clickhouse-operator/blob/master/README.md)
, the above method of using only the `<engine>` tag without `<ttl>` or `<partition>` is recommended, because of possible configuration clashes.

After that you need to restart ClickHouse and *if using old clickhouse versions like 20 or less*, drop or rename the existing system.query\_log table and then CH creates a new table with these settings. This is automatically done in newer versions 21\+.

Last modified 2026\.04\.29: [Update altinity\-kb\-system\-tables\-eat\-my\-disk.md (2800f28\)](https://github.com/Altinity/altinityknowledgebase/commit/2800f28df4622a4c6d907d549bebe44e96a141e9)
