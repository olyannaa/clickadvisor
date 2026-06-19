---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/view.md)#
topic: create-view-clickhouse-docs
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 16
---

is started immediately after the materialized view is created, unless `EMPTY` is specified in the `CREATE` query. If `EMPTY` is specified, the first refresh happens according to schedule. ### In Replicated DB[​](#in-replicated-db "Direct link to In Replicated DB")

If the refreshable materialized view is in a [Replicated database](/docs/engines/database-engines/replicated), the replicas coordinate with each other such that only one replica performs the refresh at each scheduled time. [ReplicatedMergeTree](/docs/engines/table-engines/mergetree-family/replication) table engine is required, so that all replicas see the data produced by the refresh.

In `APPEND` mode, coordination can be disabled using `SETTINGS all_replicas = 1`. This makes replicas do refreshes independently of each other. In this case ReplicatedMergeTree is not required.

In non\-`APPEND` mode, only coordinated refreshing is supported. For uncoordinated, use `Atomic` database and `CREATE ... ON CLUSTER` query to create refreshable materialized views on all replicas.

The coordination is done through Keeper. The znode path is determined by [default\_replica\_path](/docs/operations/server-configuration-parameters/settings#default_replica_path) server setting.

### Refresh Dependencies[​](#refresh-dependencies "Direct link to Refresh Dependencies")

`DEPENDS ON` synchronizes refreshes of different tables. By way of example, suppose there's a chain of two refreshable materialized views:

```
CREATE MATERIALIZED VIEW source REFRESH EVERY 1 DAY AS SELECT * FROM url(...)
CREATE MATERIALIZED VIEW destination REFRESH EVERY 1 DAY AS SELECT ... FROM source

```

Without `DEPENDS ON`, both views will start a refresh at midnight, and `destination` typically will see yesterday's data in `source`. If we add dependency:

```
CREATE MATERIALIZED VIEW destination REFRESH EVERY 1 DAY DEPENDS ON source AS SELECT ... FROM source

```

then `destination`'s refresh will start only after `source`'s refresh finished for that day, so `destination` will be based on fresh data.

Alternatively, the same result can be achieved with:

```
CREATE MATERIALIZED VIEW destination REFRESH AFTER 1 HOUR DEPENDS ON source AS SELECT ... FROM source

```

where `1 HOUR` can be any duration less than `source`'s refresh period. The dependent table won't be refreshed more frequently than any of its dependencies. This is a valid way to set up a chain of refreshable views without specifying the real refresh period more than once.

A few more examples:

- `REFRESH EVERY 1 DAY OFFSET 10 MINUTE` (`destination`) depends on `REFRESH EVERY 1 DAY` (`source`)
