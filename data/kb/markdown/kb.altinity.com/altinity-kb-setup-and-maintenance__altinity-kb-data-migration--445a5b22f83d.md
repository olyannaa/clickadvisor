# Data Migration \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. Data Migration
# Data Migration

## Export \& Import into common data formats

Pros:

- Data can be inserted into any DBMS.

Cons:

- Decoding \& encoding of common data formats may be slower / require more CPU
- The data size is usually bigger than ClickHouse® formats.
- Some of the common data formats have limitations.

#### Info

The best approach to do that is using clickhouse\-client, in that case, encoding/decoding of format happens client\-side, while client and server speak clickhouse Native format (columnar \& compressed).

In contrast: when you use HTTP protocol, the server do encoding/decoding and more data is passed between client and server.

## remote/remoteSecure or cluster/Distributed table

Pros:

- Simple to run.
- It’s possible to change the schema and distribution of data between shards.
- It’s possible to copy only some subset of data.
- Needs only access to ClickHouse TCP port.

Cons:

- Uses CPU / RAM (mostly on the receiver side)

See details of both approaches in:

[remote\-table\-function.md](http://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/remote-table-function/)

[distributed\-table\-cluster.md](http://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/distributed-table-cluster/)

## Manual parts moving: freeze / rsync / attach

Pros:

- Low CPU / RAM usage.

Cons:

- Table schema should be the same.
- A lot of manual operations/scripting.

#### Info

With some additional care and scripting, it’s possible to do cheap re\-sharding on parts level.See details in:

[rsync.md](http://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/rsync/)

## clickhouse\-backup

Pros:

- Low CPU / RAM usage.
- Suitable to recover both schema \& data for all tables at once.

Cons:

- Table schema should be the same.

Just create the backup on server 1, upload it to server 2, and restore the backup.

See [https://github.com/Altinity/clickhouse\-backup](https://github.com/Altinity/clickhouse-backup)

[https://altinity.com/blog/introduction\-to\-clickhouse\-backups\-and\-clickhouse\-backup](https://altinity.com/blog/introduction-to-clickhouse-backups-and-clickhouse-backup)

## Fetch from zookeeper path

Pros:

- Low CPU / RAM usage.

Cons:

- Table schema should be the same.
- Works only when the source and the destination ClickHouse servers share the same zookeeper (without chroot)
- Needs to access zookeeper and ClickHouse replication ports: (`interserver_http_port` or `interserver_https_port`)


```
ALTER TABLE table_name FETCH PARTITION partition_expr FROM 'path-in-zookeeper'

```
[alter table fetch detail](http://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/fetch_alter_table/)

## Using the replication protocol by adding a new replica

Just make one more replica in another place.

Pros:

- Simple to setup
- Data is consistent all the time automatically.
- Low CPU and network usage should be tuned.

Cons:

- Needs to reach both zookeeper client (2181\) and ClickHouse replication ports: (`interserver_http_port` or `interserver_https_port`)
- In case of cluster migration, zookeeper need’s to be migrated too.
- Replication works both ways so new replica should be outside the main cluster.

Check the details in:

[Add a replica to a Cluster](http://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/add_remove_replica/)

## See also

### Github issues

<https://github.com/ClickHouse/ClickHouse/issues/10943>
<https://github.com/ClickHouse/ClickHouse/issues/20219>
<https://github.com/ClickHouse/ClickHouse/pull/17871>

### Other links

<https://habr.com/ru/company/avito/blog/500678/>



---

##### [MSSQL bcp pipe to clickhouse\-client](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/mssql-clickhouse/)

Export from MSSQL to ClickHouse®

##### [Add/Remove a new replica to a ClickHouse® cluster](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/add_remove_replica/)

How to add/remove a new ClickHouse replica manually and using `clickhouse-backup`

##### [clickhouse\-copier](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/altinity-kb-clickhouse-copier/)

##### [Distributed table to ClickHouse® Cluster](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/distributed-table-cluster/)

Shifting INSERTs to a standby cluster

##### [Fetch Alter Table](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/fetch_alter_table/)

##### [Remote table function](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/remote-table-function/)

##### [Moving ClickHouse to Another Server](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/rsync/)

Copying Multi\-Terabyte Live ClickHouse to Another Server

Last modified 2025\.10\.23: [remove clickhouse\-copier section (d1c5eb3\)](https://github.com/Altinity/altinityknowledgebase/commit/d1c5eb31ec14f10fcdac31f472cb737a60eda864)
