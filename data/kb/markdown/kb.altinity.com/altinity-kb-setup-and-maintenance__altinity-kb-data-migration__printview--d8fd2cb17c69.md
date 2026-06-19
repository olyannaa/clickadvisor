# Data Migration \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/).

# Data Migration

Data Migration- 1: [MSSQL bcp pipe to clickhouse\-client](#pg-995190106d7ed9690cfa9cfd364aec72)
- 2: [Add/Remove a new replica to a ClickHouse® cluster](#pg-11fb2857cf3b2c7a29cb57f3cb63eba6)
- 3: [clickhouse\-copier](#pg-49f38a883c7ec4fc908726a6854c7bbe)
- 3\.1: [clickhouse\-copier 20\.3 and earlier](#pg-e1f1d825521583c133a8d3bf2a72f6e7)
- 3\.2: [clickhouse\-copier 20\.4 \- 21\.6](#pg-4907e613a878d5b7819f49cc367b9f3f)
- 3\.3: [Kubernetes job for clickhouse\-copier](#pg-092d5c190f9504b9126ab5f7779a2089)

- 4: [Distributed table to ClickHouse® Cluster](#pg-775c97dd3622aad5380ef8cd9f7472ad)
- 5: [Fetch Alter Table](#pg-6b8cf3862e661a5ba53de12323896812)
- 6: [Remote table function](#pg-384352a945ec192141ea6fb13e0f518f)
- 7: [Moving ClickHouse to Another Server](#pg-69e50f36eba192534d9f891226a8196a)

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

# 1 \- MSSQL bcp pipe to clickhouse\-client

Export from MSSQL to ClickHouse®## How to pipe data to ClickHouse® from bcp export tool for MSSQL database

### Prepare tables


```
LAPTOP.localdomain :) CREATE TABLE tbl(key UInt32) ENGINE=MergeTree ORDER BY key;

root@LAPTOP:/home/user# sqlcmd -U sa -P Password78
1> WITH t0(i) AS (SELECT 0 UNION ALL SELECT 0), t1(i) AS (SELECT 0 FROM t0 a, t0 b), t2(i) AS (SELECT 0 FROM t1 a, t1 b), t3(i) AS (SELECT 0 FROM t2 a, t2 b), t4(i) AS (SELECT 0 FROM t3 a, t3 b), t5(i) AS (SELECT 0 FROM t4 a, t3 b),n(i) AS (SELECT ROW_NUMBER() OVER(ORDER BY (SELECT 0)) FROM t5) SELECT i INTO tbl FROM n WHERE i BETWEEN 1 AND 16777216
2> GO

(16777216 rows affected)

root@LAPTOP:/home/user# sqlcmd -U sa -P Password78 -Q "SELECT count(*) FROM tbl"

-----------
   16777216

(1 rows affected)

```
### Piping


```
root@LAPTOP:/home/user# mkfifo import_pipe
root@LAPTOP:/home/user# bcp "SELECT * FROM tbl" queryout import_pipe -t, -c -b 200000 -U sa -P Password78 -S localhost &
[1] 6038
root@LAPTOP:/home/user#
Starting copy...
1000 rows successfully bulk-copied to host-file. Total received: 1000
1000 rows successfully bulk-copied to host-file. Total received: 2000
1000 rows successfully bulk-copied to host-file. Total received: 3000
1000 rows successfully bulk-copied to host-file. Total received: 4000
1000 rows successfully bulk-copied to host-file. Total received: 5000
1000 rows successfully bulk-copied to host-file. Total received: 6000
1000 rows successfully bulk-copied to host-file. Total received: 7000
1000 rows successfully bulk-copied to host-file. Total received: 8000
1000 rows successfully bulk-copied to host-file. Total received: 9000
1000 rows successfully bulk-copied to host-file. Total received: 10000
1000 rows successfully bulk-copied to host-file. Total received: 11000
1000 rows successfully bulk-copied to host-file. Total received: 12000
1000 rows successfully bulk-copied to host-file. Total received: 13000
1000 rows successfully bulk-copied to host-file. Total received: 14000
1000 rows successfully bulk-copied to host-file. Total received: 15000
1000 rows successfully bulk-copied to host-file. Total received: 16000
1000 rows successfully bulk-copied to host-file. Total received: 17000
1000 rows successfully bulk-copied to host-file. Total received: 18000
1000 rows successfully bulk-copied to host-file. Total received: 19000
1000 rows successfully bulk-copied to host-file. Total received: 20000
1000 rows successfully bulk-copied to host-file. Total received: 21000
1000 rows successfully bulk-copied to host-file. Total received: 22000
1000 rows successfully bulk-copied to host-file. Total received: 23000
-- Enter
root@LAPTOP:/home/user# cat import_pipe | clickhouse-client --query "INSERT INTO tbl FORMAT CSV" &
...
1000 rows successfully bulk-copied to host-file. Total received: 16769000
1000 rows successfully bulk-copied to host-file. Total received: 16770000
1000 rows successfully bulk-copied to host-file. Total received: 16771000
1000 rows successfully bulk-copied to host-file. Total received: 16772000
1000 rows successfully bulk-copied to host-file. Total received: 16773000
1000 rows successfully bulk-copied to host-file. Total received: 16774000
1000 rows successfully bulk-copied to host-file. Total received: 16775000
1000 rows successfully bulk-copied to host-file. Total received: 16776000
1000 rows successfully bulk-copied to host-file. Total received: 16777000
16777216 rows copied.
Network packet size (bytes): 4096
Clock Time (ms.) Total     : 11540  Average : (1453831.5 rows per sec.)

[1]-  Done                    bcp "SELECT * FROM tbl" queryout import_pipe -t, -c -b 200000 -U sa -P Password78 -S localhost
[2]+  Done                    cat import_pipe | clickhouse-client --query "INSERT INTO tbl FORMAT CSV"

```
### Another shell


```
root@LAPTOP:/home/user# for i in `seq 1 600`; do clickhouse-client -q "select count() from tbl";sleep 1;  done
0
0
0
0
0
0
1048545
4194180
6291270
9436905
11533995
13631085
16777216
16777216
16777216
16777216

```
# 2 \- Add/Remove a new replica to a ClickHouse® cluster

How to add/remove a new ClickHouse replica manually and using `clickhouse-backup`## ADD nodes/replicas to a ClickHouse® cluster

To add some ClickHouse® replicas to an existing cluster if \-30TB then better to use replication:

- don’t add the `remote_servers.xml` until replication is done.
- Add these files and restart to limit bandwidth and avoid saturation (70% total bandwidth):

[Core Settings \| ClickHouse Docs](https://clickhouse.com/docs/en/operations/settings/settings/#max_replicated_fetches_network_bandwidth_for_server)

💡 Do the **Gbps to Bps** math correctly. For 10G —\> 1250MB/s —\> 1250000000 B/s. Change the `max_replicated_*` settings accordingly and add them to a file in `/etc/clickhouse-server/config.d/` (e.g., `config.d/replication-limits.xml`) and restart ClickHouse:

- Nodes replicating from:


```
<clickhouse>
  <max_replicated_sends_network_bandwidth_for_server>50000</max_replicated_sends_network_bandwidth_for_server>
</clickhouse>

```
- Nodes replicating to:


```
<clickhouse>
  <max_replicated_fetches_network_bandwidth_for_server>50000</max_replicated_fetches_network_bandwidth_for_server>
</clickhouse>

```
### Manual method (DDL)

- Create tables `manually` and be sure macros in all replicas are aligned with the ZK path. If zk path uses `{cluster}` then this method won’t work. ZK path should use `{shard}` and `{replica}` or `{uuid}` (if databases are Atomic) only.


```
-- DDL for Databases
SELECT concat('CREATE DATABASE "', name, '" ENGINE = ', engine_full, ';') 
FROM system.databases WHERE name NOT IN ('system', 'information_schema', 'INFORMATION_SCHEMA')
INTO OUTFILE '/tmp/databases.sql' 
FORMAT TSVRaw;
-- DDL for tables and views
SELECT
    replaceRegexpOne(replaceOne(concat(create_table_query, ';'), '(', 'ON CLUSTER \'{cluster}\' ('), 'CREATE (TABLE|DICTIONARY|VIEW|LIVE VIEW|WINDOW VIEW)', 'CREATE \\1 IF NOT EXISTS')
FROM
    system.tables
WHERE engine != 'MaterializedView' and
    database NOT IN ('system', 'information_schema', 'INFORMATION_SCHEMA') AND
    create_table_query != '' AND
    name NOT LIKE '.inner.%%' AND
    name NOT LIKE '.inner_id.%%'
INTO OUTFILE '/tmp/schema.sql' AND STDOUT
FORMAT TSVRaw
SETTINGS show_table_uuid_in_table_create_query_if_not_nil=1;
--- DDL only for materialized views
SELECT
    replaceRegexpOne(replaceOne(concat(create_table_query, ';'), 'TO', 'ON CLUSTER \'{cluster}\' TO'), '(CREATE MATERIALIZED VIEW)', '\\1 IF NOT EXISTS')
FROM
    system.tables
WHERE engine = 'MaterializedView' and
    database NOT IN ('system', 'information_schema', 'INFORMATION_SCHEMA') AND
    create_table_query != '' AND
    name NOT LIKE '.inner.%%' AND
    name NOT LIKE '.inner_id.%%' AND
		as_select != ''
INTO OUTFILE '/tmp/schema.sql' APPEND AND STDOUT
FORMAT TSVRaw
SETTINGS show_table_uuid_in_table_create_query_if_not_nil=1;

```
This will generate the UUIDs in the CREATE TABLE definition, something like this:


```
CREATE TABLE IF NOT EXISTS default.insert_test UUID '51b41170-5192-4947-b13b-d4094c511f06' ON CLUSTER '{cluster}' (`id_order` UInt16, `id_plat` UInt32, `id_warehouse` UInt64, `id_product` UInt16, `order_type` UInt16, `order_status` String, `datetime_order` DateTime, `units` Int16, `total` Float32) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{uuid}/{shard}', '{replica}') PARTITION BY tuple() ORDER BY (id_order, id_plat, id_warehouse) SETTINGS index_granularity = 8192;

```
- Copy both SQL to destination replica and execute


```
clickhouse-client --host localhost --port 9000 -mn < databases.sql
clickhouse-client --host localhost --port 9000 -mn < schema.sql

```
### Using `clickhouse-backup`

- Before proceeding: check if you have `restore_schema_on_cluster` set; if it is, this procedure will drop tables with `ON CLUSTER`, which is not its intention! To verify:


```
$ clickhouse-backup print-config|grep restore_schema_on_cluster
    restore_schema_on_cluster: ""

```
- Using `clickhouse-backup` to copy the schema of a replica to another is also convenient, and if [using Atomic database](/engines/altinity-kb-atomic-database-engine/)
with `{uuid}` macros in [ReplicatedMergeTree engines](https://www.youtube.com/watch?v=oHwhXc0re6k)
.


```
$ sudo -u clickhouse clickhouse-backup create --schema --rbac --named-collections rbac_and_schema
# From the destination replica do this in 2 steps (for safety, keep --env=RESTORE_SCHEMA_ON_CLUSTER=):
$ sudo -u clickhouse clickhouse-backup restore --env=RESTORE_SCHEMA_ON_CLUSTER= --rbac-only rbac_and_schema
$ sudo -u clickhouse clickhouse-backup restore --env=RESTORE_SCHEMA_ON_CLUSTER= --schema --named-collections rbac_and_schema

```
### Using `altinity operator`

If there is at least one alive replica in the shard, you can remove PVCs and STS for affected nodes and trigger reconciliation. The operator will try to copy the schema from other replicas.

### Check that schema migration was successful and node is replicating

- To check that the schema migration has been **successful** query system.replicas:


```
SELECT DISTINCT database,table,replica_is_active FROM system.replicas FORMAT Vertical

```
- Check how the replication process is performing using [https://kb.altinity.com/altinity\-kb\-setup\-and\-maintenance/altinity\-kb\-replication\-queue/](https://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-replication-queue/)


	- If there are many postponed tasks with the message:
```
Not executing fetch of part 7_22719661_22719661_0 because 16 fetches already executing, max 16.                                                                                                      │ 2023-09-25 17:03:06 │            │

```
then it is ok, the maximum replication slots are being used. Exceptions are not OK and should be investigated
- If migration was successful and replication is working, then wait until the replication is finished. It may take some days, depending on how much data is being replicated. After this edit, the cluster configuration xml file for all replicas (`remote_servers.xml`), and add the new replica to the cluster.

### Possible problems

#### **Exception** `REPLICA_ALREADY_EXISTS`


```
Code: 253. DB::Exception: Received from localhost:9000. 
DB::Exception: There was an error on [dl-ny2-vm-09.internal.io:9000]: 
Code: 253. DB::Exception: Replica /clickhouse/tables/3c3503c3-ed3c-443b-9cb3-ef41b3aed0a8/1/replicas/dl-ny2-vm-09.internal.io 
already exists. (REPLICA_ALREADY_EXISTS) (version 23.5.3.24 (official build)). (REPLICA_ALREADY_EXISTS)
(query: CREATE TABLE IF NOT EXISTS xxxx.yyyy UUID '3c3503c3-ed3c-443b-9cb3-ef41b3aed0a8'

```
[The DDLs](/altinity-kb-setup-and-maintenance/altinity-kb-check-replication-ddl-queue/)
have been executed and some tables have been created and after that dropped but some left overs are left in ZK:

- If databases can be dropped then use `DROP DATABASE xxxxx SYNC`
- If databases cannot be dropped use `SYSTEM DROP REPLICA ‘replica_name’ FROM db.table`

#### **Exception** `TABLE_ALREADY_EXISTS`


```
Code: 57. DB::Exception: Received from localhost:9000. 
DB::Exception: There was an error on [dl-ny2-vm-09.internal.io:9000]: 
Code: 57. DB::Exception: Directory for table data store/3c3/3c3503c3-ed3c-443b-9cb3-ef41b3aed0a8/ already exists. 
(TABLE_ALREADY_EXISTS) (version 23.5.3.24 (official build)). (TABLE_ALREADY_EXISTS)
(query: CREATE TABLE IF NOT EXISTS xxxx.yyyy UUID '3c3503c3-ed3c-443b-9cb3-ef41b3aed0a8' ON CLUSTER '{cluster}'

```
Tables have not been dropped correctly:

- If databases can be dropped then use `DROP DATABASE xxxxx SYNC`
- If databases cannot be dropped use:


```
SELECT concat('DROP TABLE ', database, '.', name, ' SYNC;') 
FROM system.tables 
WHERE database NOT IN ('system', 'information_schema', 'INFORMATION_SCHEMA') 
INTO OUTFILE '/tmp/drop_tables.sql' 
FORMAT TSVRaw;

```
### Tuning

- Sometimes replication goes very fast and if you have a tiered storage hot/cold you could run out of space, so for that it is interesting to:
	- reduce fetches from 8 to 4
	- increase moves from 8 to 16

Add these settings to a file in `/etc/clickhouse-server/config.d/` (e.g., `config.d/replication-limits.xml`) and restart ClickHouse:


```
<clickhouse>
  <max_replicated_fetches_network_bandwidth_for_server>625000000</max_replicated_fetches_network_bandwidth_for_server>
  <background_fetches_pool_size>4</background_fetches_pool_size>
  <background_move_pool_size>16</background_move_pool_size>
</clickhouse>

```
- Also to monitor this with:


```
SELECT *
FROM system.metrics
WHERE metric LIKE '%Move%'

Query id: 5050155b-af4a-474f-a07a-f2f7e95fb395

┌─metric─────────────────┬─value─┬─description──────────────────────────────────────────────────┐
│ BackgroundMovePoolTask │     0 │ Number of active tasks in BackgroundProcessingPool for moves │
└────────────────────────┴───────┴──────────────────────────────────────────────────────────────┘

1 row in set. Elapsed: 0.164 sec. 

dnieto-test :) SELECT * FROM system.metrics WHERE metric LIKE '%Fetch%';

SELECT *
FROM system.metrics
WHERE metric LIKE '%Fetch%'

Query id: 992cae2a-fb58-4150-a088-83273805d0c4

┌─metric────────────────────┬─value─┬─description───────────────────────────────────────────────┐
│ ReplicatedFetch           │     0 │ Number of data parts being fetched from replica           │
│ BackgroundFetchesPoolTask │     0 │ Number of active fetches in an associated background pool │
└───────────────────────────┴───────┴───────────────────────────────────────────────────────────┘

2 rows in set. Elapsed: 0.163 sec.

```
- There are new tables in v23 `system.replicated_fetches` and `system.moves` check it out for more info.
- if needed just stop replication using `SYSTEM STOP FETCHES` from the replicating nodes

## REMOVE nodes/Replicas from a Cluster

- It is important to know which replica/node you want to remove to avoid problems. To check it you need to connect to a different replica/node that the one you want to remove. For instance we want to remove `arg_t04`, so we connected to replica `arg_t01`:


```
SELECT DISTINCT arrayJoin(mapKeys(replica_is_active)) AS replica_name
FROM system.replicas

┌─replica_name─┐
│ arg_t01      │
│ arg_t02      │
│ arg_t03      │
│ arg_t04      │
└──────────────┘

```
- After that (make sure you’re connected to a replica different from the one that you want to remove, `arg_tg01`) and execute:


```
SYSTEM DROP REPLICA 'arg_t04'

```
- If by any chance you’re connected to the same replica you want to remove then **`SYSTEM DROP REPLICA`** will not work.
- BTW `SYSTEM DROP REPLICA` does not drop any tables and does not remove any data or metadata from disk, it will only remove metadata from Zookeeper/Keeper


```
-- What happens if executing system drop replica in the local replica to remove.
SYSTEM DROP REPLICA 'arg_t04'

Elapsed: 0.017 sec. 

Received exception from server (version 23.8.6):
Code: 305. DB::Exception: Received from dnieto-zenbook.lan:9440. DB::Exception: We can't drop local replica, please use `DROP TABLE` if you want to clean the data and drop this replica. (TABLE_WAS_NOT_DROPPED)

```
- After DROP REPLICA, we need to check that the replica is gone from the list or replicas:


```
SELECT DISTINCT arrayJoin(mapKeys(replica_is_active)) AS replica_name
FROM system.replicas

┌─replica_name─┐
│ arg_t01      │
│ arg_t02      │
│ arg_t03      │
└──────────────┘

-- We should see there is no replica arg_t04

```
- Delete the replica in the cluster configuration: `remote_servers.xml` and shutdown the node/replica removed.
# 3 \- clickhouse\-copier

clickhouse\-copierThe description of the utility and its parameters, as well as examples of the config files that you need to create for the copier are in the official repo for the [ClickHouse® copier utility](https://github.com/clickhouse/copier/)

The steps to run a task:

1. Create a config file for `clickhouse-copier` (zookeeper.xml)
2. Create a config file for the task (task1\.xml)
3. Create the task in ZooKeeper and start an instance of `clickhouse-copier`

`clickhouse-copier --daemon --base-dir=/opt/clickhouse-copier --config=/opt/clickhouse-copier/zookeeper.xml --task-path=/clickhouse/copier/task1 --task-file=/opt/clickhouse-copier/task1.xml`

If the node in ZooKeeper already exists and you want to change it, you need to add the `task-upload-force` parameter:

`clickhouse-copier --daemon --base-dir=/opt/clickhouse-copier --config=/opt/clickhouse-copier/zookeeper.xml --task-path=/clickhouse/copier/task1 --task-file=/opt/clickhouse-copier/task1.xml --task-upload-force=1`

If you want to run another instance of `clickhouse-copier` for the same task, you need to copy the config file (zookeeper.xml) to another server, and run this command:

`clickhouse-copier --daemon --base-dir=/opt/clickhouse-copier --config=/opt/clickhouse-copier/zookeeper.xml --task-path=/clickhouse/copier/task1`

The number of simultaneously running instances is controlled be the `max_workers` parameter in your task configuration file. If you run more workers superfluous workers will sleep and log messages like this:

`<Debug> ClusterCopier: Too many workers (1, maximum 1). Postpone processing`

### See also

- <https://github.com/clickhouse/copier/>
- Никита Михайлов. Кластер ClickHouse ctrl\-с ctrl\-v. HighLoad\+\+ Весна 2021 [slides](https://raw.githubusercontent.com/ClickHouse/clickhouse-presentations/master/highload2021/copier.pdf)
- 21\.7 have a huge bulk of fixes / improvements. <https://github.com/ClickHouse/ClickHouse/pull/23518>
- [https://altinity.com/blog/2018/8/22/clickhouse\-copier\-in\-practice](https://altinity.com/blog/2018/8/22/clickhouse-copier-in-practice)
- [https://github.com/getsentry/snuba/blob/master/docs/clickhouse\-copier.md](https://github.com/getsentry/snuba/blob/master/docs/clickhouse-copier.md)
- [https://hughsite.com/post/clickhouse\-copier\-usage.html](https://hughsite.com/post/clickhouse-copier-usage.html)
- <https://www.jianshu.com/p/c058edd664a6>
# 3\.1 \- clickhouse\-copier 20\.3 and earlier

clickhouse\-copier 20\.3 and earlier`clickhouse-copier` was created to move data between clusters.
It runs simple INSERT…SELECT queries and can copy data between tables with different engine parameters and between clusters with different number of shards.
In the task configuration file you need to describe the layout of the source and the target cluster, and list the tables that you need to copy. You can copy whole tables or specific partitions.
`clickhouse-copier` uses temporary distributed tables to select from the source cluster and insert into the target cluster.

## The process is as follows

1. Process the configuration files.
2. Discover the list of partitions if not provided in the config.
3. Copy partitions one by one.
	1. Drop the partition from the target table if it’s not empty
	2. Copy data from source shards one by one.
		1. Check if there is data for the partition on a source shard.
		2. Check the status of the task in ZooKeeper.
		3. Create target tables on all shards of the target cluster.
		4. Insert the partition of data into the target table.
	3. Mark the partition as completed in ZooKeeper.

If there are several workers running simultaneously, they will assign themselves to different source shards.
If a worker was interrupted, another worker can be started to continue the task. The next worker will drop incomplete partitions and resume the copying.

## Configuring the engine of the target table

`clickhouse-copier` uses the engine from the task configuration file for these purposes:

- to create target tables if they don’t exist.
- PARTITION BY: to SELECT a partition of data from the source table, to DROP existing partitions from target tables.

`clickhouse-copier` does not support the old MergeTree format.
However, you can create the target tables manually and specify the engine in the task configuration file in the new format so that `clickhouse-copier` can parse it for its SELECT queries.

## How to monitor the status of running tasks

`clickhouse-copier` uses ZooKeeper to keep track of the progress and to communicate between workers.
Here is a list of queries that you can use to see what’s happening.


```
--task-path /clickhouse/copier/task1

-- The task config
select * from system.zookeeper
where path='<task-path>'
name                        | ctime               | mtime           
----------------------------+---------------------+--------------------
description                 | 2019-10-18 15:40:00 | 2020-09-11 16:01:14
task_active_workers_version | 2019-10-18 16:00:09 | 2020-09-11 16:07:08
tables                      | 2019-10-18 16:00:25 | 2019-10-18 16:00:25
task_active_workers         | 2019-10-18 16:00:09 | 2019-10-18 16:00:09


-- Running workers
select * from system.zookeeper
where path='<task-path>/task_active_workers'


-- The list of processed tables
select * from system.zookeeper
where path='<task-path>/tables'


-- The list of processed partitions
select * from system.zookeeper
where path='<task-path>/tables/<table>'
name   | ctime           
-------+--------------------
201909 | 2019-10-18 18:24:18


-- The status of a partition
select * from system.zookeeper
where path='<task-path>/tables/<table>/<partition>'
name                     | ctime           
-------------------------+--------------------
shards                   | 2019-10-18 18:24:18
partition_active_workers | 2019-10-18 18:24:18


-- The status of source shards
select * from system.zookeeper
where path='<task-path>/tables/<table>/<partition>/shards'
name | ctime               | mtime           
-----+---------------------+--------------------
1    | 2019-10-18 22:37:48 | 2019-10-18 22:49:29

```
# 3\.2 \- clickhouse\-copier 20\.4 \- 21\.6

clickhouse\-copier 20\.4 \- 21\.6`clickhouse-copier` was created to move data between clusters.
It runs simple `INSERT…SELECT` queries and can copy data between tables with different engine parameters and between clusters with different number of shards.
In the task configuration file you need to describe the layout of the source and the target cluster, and list the tables that you need to copy. You can copy whole tables or specific partitions.
`clickhouse-copier` uses temporary distributed tables to select from the source cluster and insert into the target cluster.

The behavior of `clickhouse-copier` was changed in 20\.4:

- Now `clickhouse-copier` inserts data into intermediate tables, and after the insert finishes successfully `clickhouse-copier` attaches the completed partition into the target table. This allows for incremental data copying, because the data in the target table is intact during the process. **Important note:** ATTACH PARTITION respects the `max_partition_size_to_drop` limit. Make sure the `max_partition_size_to_drop` limit is big enough (or set to zero) in the destination cluster. If `clickhouse-copier` is unable to attach a partition because of the limit, it will proceed to the next partition, and it will drop the intermediate table when the task is finished (if the intermediate table is less than the `max_table_size_to_drop` limit). **Another important note:** ATTACH PARTITION is replicated. The attached partition will need to be downloaded by the other replicas. This can create significant network traffic between ClickHouse nodes. If an attach takes a long time, `clickhouse-copier` will log a timeout and will proceed to the next step.
- Now `clickhouse-copier` splits the source data into chunks and copies them one by one. This is useful for big source tables, when inserting one partition of data can take hours. If there is an error during the insert `clickhouse-copier` has to drop the whole partition and start again. The `number_of_splits` parameter lets you split your data into chunks so that in case of an exception `clickhouse-copier` has to re\-insert only one chunk of the data.
- Now `clickhouse-copier` runs `OPTIMIZE target_table PARTITION ... DEDUPLICATE` for non\-Replicated MergeTree tables. **Important note:** This is a very strange feature that can do more harm than good. We recommend to disable it by configuring the engine of the target table as Replicated in the task configuration file, and create the target tables manually if they are not supposed to be replicated. Intermediate tables are always created as plain MergeTree.

## The process is as follows

1. Process the configuration files.
2. Discover the list of partitions if not provided in the config.
3. Copy partitions one by one \*\* The metadata in ZooKeeper suggests the order described here.\*\*
	1. Copy chunks of data one by one.
		1. Copy data from source shards one by one.
			1. Create intermediate tables on all shards of the target cluster.
			2. Check the status of the chunk in ZooKeeper.
			3. Drop the partition from the intermediate table if the previous attempt was interrupted.
			4. Insert the chunk of data into the intermediate tables.
			5. Mark the shard as completed in ZooKeeper
	2. Attach the chunks of the completed partition into the target table one by one
		1. Attach a chunk into the target table.
		2. **non\-Replicated:** Run OPTIMIZE target\_table DEDUPLICATE for the partition on the target table.
4. Drop intermediate tables (may not succeed if the tables are bigger than `max_table_size_to_drop`).

If there are several workers running simultaneously, they will assign themselves to different source shards.
If a worker was interrupted, another worker can be started to continue the task. The next worker will drop incomplete partitions and resume the copying.

## Configuring the engine of the target table

`clickhouse-copier` uses the engine from the task configuration file for these purposes:

- to create target and intermediate tables if they don’t exist.
- PARTITION BY: to SELECT a partition of data from the source table, to ATTACH partitions into target tables, to DROP incomplete partitions from intermediate tables, to OPTIMIZE partitions after they are attached to the target.
- ORDER BY: to SELECT a chunk of data from the source table.

Here is an example of SELECT that `clickhouse-copier` runs to get the sixth of ten chunks of data:


```
WHERE (<the PARTITION BY clause> = (<a value of the PARTITION BY expression> AS partition_key))
  AND (cityHash64(<the ORDER BY clause>) % 10 = 6 )

```
`clickhouse-copier` does not support the old MergeTree format.
However, you can create the intermediate tables manually with the same engine as the target tables (otherwise ATTACH will not work), and specify the engine in the task configuration file in the new format so that `clickhouse-copier` can parse it for SELECT, ATTACH PARTITION and DROP PARTITION queries.

**Important note**: always configure engine as Replicated to disable OPTIMIZE … DEDUPLICATE (unless you know why you need `clickhouse-copier` to run OPTIMIZE … DEDUPLICATE).

## How to configure the number of chunks

The default value for `number_of_splits` is 10\.
You can change this parameter in the `table` section of the task configuration file. We recommend setting it to 1 for smaller tables.


```
<cluster_push>target_cluster</cluster_push>
<database_push>target_database</database_push>
<table_push>target_table</table_push>
<number_of_splits>1</number_of_splits>
<engine>Engine=Replicated...<engine>

```
## How to monitor the status of running tasks

`clickhouse-copier` uses ZooKeeper to keep track of the progress and to communicate between workers.
Here is a list of queries that you can use to see what’s happening.


```
--task-path=/clickhouse/copier/task1

-- The task config
select * from system.zookeeper
where path='<task-path>'
name                        | ctime               | mtime           
----------------------------+---------------------+--------------------
description                 | 2021-03-22 13:15:48 | 2021-03-22 13:25:28
status                      | 2021-03-22 13:15:48 | 2021-03-22 13:25:28
task_active_workers_version | 2021-03-22 13:15:48 | 2021-03-22 20:32:09
tables                      | 2021-03-22 13:16:47 | 2021-03-22 13:16:47
task_active_workers         | 2021-03-22 13:15:48 | 2021-03-22 13:15:48


-- Status
select * from system.zookeeper
where path='<task-path>/status'


-- Running workers
select * from system.zookeeper
where path='<task-path>/task_active_workers'


-- The list of processed tables
select * from system.zookeeper
where path='<task-path>/tables'


-- The list of processed partitions
select * from system.zookeeper
where path='<task-path>/tables/<table>'
name   | ctime           
-------+--------------------
202103 | 2021-03-22 13:16:47
202102 | 2021-03-22 13:18:31
202101 | 2021-03-22 13:27:36
202012 | 2021-03-22 14:05:08


-- The status of a partition
select * from system.zookeeper
where path='<task-path>/tables/<table>/<partition>'
name           | ctime           
---------------+--------------------
piece_0        | 2021-03-22 13:18:31
attach_is_done | 2021-03-22 14:05:05


-- The status of a piece
select * from system.zookeeper
where path='<task-path>/tables/<table>/<partition>/piece_N'
name                           | ctime           
-------------------------------+--------------------
shards                         | 2021-03-22 13:18:31
is_dirty                       | 2021-03-22 13:26:51
partition_piece_active_workers | 2021-03-22 13:26:54
clean_start                    | 2021-03-22 13:26:54


-- The status of source shards
select * from system.zookeeper
where path='<task-path>/tables/<table>/<partition>/piece_N/shards'
name | ctime               | mtime           
-----+---------------------+--------------------
1    | 2021-03-22 13:26:54 | 2021-03-22 14:05:05

```
# 3\.3 \- Kubernetes job for clickhouse\-copier

Kubernetes job for `clickhouse-copier`# `clickhouse-copier` deployment in kubernetes

`clickhouse-copier` can be deployed in a kubernetes environment to automate some simple backups or copy fresh data between clusters.

Some documentation to read:

- [https://kb.altinity.com/altinity\-kb\-setup\-and\-maintenance/altinity\-kb\-data\-migration/altinity\-kb\-clickhouse\-copier/](https://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/altinity-kb-clickhouse-copier/)
- <https://github.com/clickhouse/copier/>

## Deployment

Use a kubernetes job is recommended but a simple pod can be used if you only want to execute the copy one time.

Just edit/change all the `yaml` files to your needs.

### 1\) Create the PVC:

First create a namespace in which all the pods and resources are going to be deployed


```
kubectl create namespace clickhouse-copier

```
Then create the PVC using a `storageClass` gp2\-encrypted class or use any other storageClass from other providers:


```
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: copier-logs
  namespace: clickhouse-copier
spec:
  storageClassName: gp2-encrypted
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi

```
and deploy:


```
kubectl -n clickhouse-copier create -f ./kubernetes/copier-pvc.yaml

```
### 2\) Create the configmap:

The configmap has both files `zookeeper.xml` and `task01.xml` with the zookeeper node listing and the parameters for the task respectively.


```
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: copier-config
  namespace: clickhouse-copier
data:
    task01.xml: |
        <clickhouse>
            <logger>
                <console>true</console>
                <log remove="remove"/>
                <errorlog remove="remove"/>
                <level>trace</level>
            </logger>
            <remote_servers>
                <all-replicated>
                    <shard>
                        <replica>
                            <host>clickhouse01.svc.cluster.local</host>
                            <port>9000</port>
                            <user>chcopier</user>
                            <password>pass</password>
                        </replica>
                        <replica>
                            <host>clickhouse02.svc.cluster.local</host>
                            <port>9000</port>
                            <user>chcopier</user>
                            <password>pass</password>
                        </replica>
                    </shard>
                </all-replicated>
                <all-sharded>
                    <!-- <secret></secret> -->
                    <shard>
                        <replica>
                            <host>clickhouse03.svc.cluster.local</host>
                            <port>9000</port>
                            <user>chcopier</user>
                            <password>pass</password>
                        </replica>
                    </shard>
                    <shard>
                        <replica>
                            <host>clickhouse03.svc.cluster.local</host>
                            <port>9000</port>
                            <user>chcopier</user>
                            <password>pass</password>
                        </replica>
                    </shard>
                </all-sharded>
            </remote_servers>
            <max_workers>1</max_workers>
            <settings_pull>
                <readonly>1</readonly>
            </settings_pull>
            <settings_push>
                <readonly>0</readonly>
            </settings_push>
            <settings>
                <connect_timeout>3</connect_timeout>
                <insert_distributed_sync>1</insert_distributed_sync>
            </settings>
            <tables>
                <table_sales>
                    <cluster_pull>all-replicated</cluster_pull>
                    <database_pull>default</database_pull>
                    <table_pull>fact_sales_event</table_pull>
                    <cluster_push>all-sharded</cluster_push>
                    <database_push>default</database_push>
                    <table_push>fact_sales_event</table_push>
                    <engine>
                        Engine=ReplicatedMergeTree('/clickhouse/{cluster}/tables/{shard}/fact_sales_event', '{replica}')
                        PARTITION BY toYYYYMM(timestamp)
                        ORDER BY (channel_id, product_id)
                        SETTINGS index_granularity = 8192
                    </engine>
                    <sharding_key>rand()</sharding_key>
                </table_ventas>
            </tables>
        </clickhouse>        
    zookeeper.xml: |
        <clickhouse>
            <logger>
                <level>trace</level>
                <size>100M</size>
                <count>3</count>
            </logger>
            <zookeeper>
                <node>
                    <host>zookeeper1.svc.cluster.local</host>
                    <port>2181</port>
                </node>
                <node>
                    <host>zookeeper2.svc.cluster.local</host>
                    <port>2181</port>
                </node>
                <node>
                    <host>zookeeper3.svc.cluster.local</host>
                    <port>2181</port>
                </node>
            </zookeeper>
        </clickhouse>        

```
and deploy:


```
kubectl -n clickhouse-copier create -f ./kubernetes/copier-configmap.yaml

```
The `task01.xml` file has many parameters to take into account explained in the repo for [clickhouse\-copier](https://github.com/clickhouse/copier/)
. Important to note that it is needed a FQDN for the Zookeeper nodes and ClickHouse® server that are valid for the cluster. As the deployment creates a new namespace, it is recommended to use a FQDN linked to a service. For example `zookeeper01.svc.cluster.local`. This file should be adapted to both clusters topologies and to the needs of the user.

The `zookeeper.xml` file is pretty straightforward with a simple 3 node ensemble configuration.

### 3\) Create the job:

Basically the job will download the official ClickHouse image and will create a pod with 2 containers:

- clickhouse\-copier: This container will run the clickhouse\-copier utility.
- sidecar\-logging: This container will be used to read the logs of the clickhouse\-copier container for different runs (this part can be improved):


```
---
apiVersion: batch/v1
kind: Job
metadata:
  name: clickhouse-copier-test
  namespace: clickhouse-copier
spec:
  # only for kubernetes 1.23
  # ttlSecondsAfterFinished: 86400
  template:
    spec:
      containers:
        - name: clickhouse-copier
          image: clickhouse/clickhouse-server:21.8
          command:
            - clickhouse-copier
            - --task-upload-force=1
            - --config-file=$(CH_COPIER_CONFIG)
            - --task-path=$(CH_COPIER_TASKPATH)
            - --task-file=$(CH_COPIER_TASKFILE)
            - --base-dir=$(CH_COPIER_BASEDIR)
          env:
            - name: CH_COPIER_CONFIG
              value: "/var/lib/clickhouse/tmp/zookeeper.xml"
            - name: CH_COPIER_TASKPATH
              value: "/clickhouse/copier/tasks/task01"
            - name: CH_COPIER_TASKFILE
              value: "/var/lib/clickhouse/tmp/task01.xml"
            - name: CH_COPIER_BASEDIR
              value: "/var/lib/clickhouse/tmp"
          resources:
            limits:
              cpu: "1"
              memory: 2048Mi
          volumeMounts:
            - name: copier-config
              mountPath: /var/lib/clickhouse/tmp/zookeeper.xml
              subPath: zookeeper.xml
            - name: copier-config
              mountPath: /var/lib/clickhouse/tmp/task01.xml
              subPath: task01.xml
            - name: copier-logs
              mountPath: /var/lib/clickhouse/tmp
        - name: sidecar-logger
          image: busybox:1.35
          command: ['/bin/sh', '-c', 'tail', '-n', '1000', '-f', '/tmp/copier-logs/clickhouse-copier*/*.log']
          resources:
            limits:
              cpu: "1"
              memory: 512Mi
          volumeMounts:
            - name: copier-logs
              mountPath: /tmp/copier-logs
      volumes:
        - name: copier-config
          configMap:
            name: copier-config
            items:
              - key: zookeeper.xml
                path: zookeeper.xml
              - key: task01.xml
                path: task01.xml
        - name: copier-logs
          persistentVolumeClaim:
            claimName: copier-logs
      restartPolicy: Never
  backoffLimit: 3

```
Deploy and watch progress checking the logs:


```
kubectl -n clickhouse-copier logs <podname> sidecar-logging

```
# 4 \- Distributed table to ClickHouse® Cluster

Shifting INSERTs to a standby clusterIn order to shift INSERTS to a standby cluster (for example increase zone availability or [disaster recovery](https://docs.altinity.com/operationsguide/availability-and-recovery/recovery-architecture/)
) some ClickHouse® features can be used.

Basically we need to create a distributed table, a MV, rewrite the `remote_servers.xml` config file and tune some parameters.

Distributed engine information and parameters:
[https://clickhouse.com/docs/en/engines/table\-engines/special/distributed/](https://clickhouse.com/docs/en/engines/table-engines/special/distributed/)

## Steps

### Create a Distributed table in the source cluster

For example, we should have a `ReplicatedMergeTree` table in which all inserts are falling. This table is the first step in our pipeline:


```
CREATE TABLE db.inserts_source ON CLUSTER 'source'
(
    column1 String
    column2 DateTime
    .....
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/inserts_source', '{replica}')
PARTITION BY toYYYYMM(column2)
ORDER BY (column1, column2)

```
This table lives in the source cluster and all INSERTS go there. In order to shift all INSERTS in the source cluster to destination cluster we can create a `Distributed` table that points to another `ReplicatedMergeTree` in the destination cluster:


```
CREATE TABLE db.inserts_source_dist ON CLUSTER 'source'
(
    column1 String
    column2 DateTime
    .....
)
ENGINE = Distributed('destination', db, inserts_destination)

```
### Create a Materialized View to shift INSERTS to destination cluster:


```
CREATE MATERIALIZED VIEW shift_inserts ON CLUSTER 'source'
TO db.inserts_source_dist AS
SELECT * FROM db.inserts_source

```
### Create a ReplicatedMergeTree table in the destination cluster:

This is the table in the destination cluster that is pointed by the distributed table in the source cluster


```
CREATE TABLE db.inserts_destination ON CLUSTER 'destination'
(
    column1 String
    column2 DateTime
    .....
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/inserts_destination', '{replica}')
PARTITION BY toYYYYMM(column2)
ORDER BY (column1, column2)

```
### Rewrite remote\_servers.xml:

All the hostnames/FQDN from each replica/node must be accessible from both clusters. Also the remote\_servers.xml from the source cluster should read like this:


```
<clickhouse>
    <remote_servers>
        <source>   
            <shard>
                <replica>
                    <host>host03</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>host04</host>
                    <port>9000</port>
                </replica>
            </shard>
        </source>
        <destination>   
            <shard>
                <replica>
                    <host>host01</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>host02</host>
                    <port>9000</port>
                </replica>
            </shard>
        </destination>
        <!-- If using a LB to shift inserts you need to use user and password and create MT destination table in an all-replicated cluster config -->
        <destination_with_lb>   
            <shard>
                <replica>
                    <host>load_balancer.xxxx.com</host>
                    <port>9440</port>
                    <secure>1</secure>
                    <username>user</username>
                    <password>pass</password>
                </replica>
            </shard>
        </destination_with_lb>
   </remote_servers>
</clickhouse>

```
### Configuration settings

Depending on your use case you can set the the distributed INSERTs to sync or [async mode](/altinity-kb-queries-and-syntax/async-inserts/)
. This example is for async mode:
Put this config settings on the default profile. Check for more info about the possible modes:

[https://clickhouse.com/docs/en/operations/settings/settings\#insert\_distributed\_sync](https://clickhouse.com/docs/en/operations/settings/settings#insert_distributed_sync)


```
<clickhouse>
    ....
    <profiles>
        <default>
            <!-- StorageDistributed DirectoryMonitors try to batch individual inserts into bigger ones to increase performance -->
            <distributed_directory_monitor_batch_inserts>1</distributed_directory_monitor_batch_inserts>
            <!-- StorageDistributed DirectoryMonitors try to split batch into smaller in case of failures -->
            <distributed_directory_monitor_split_batch_on_failure>1</distributed_directory_monitor_split_batch_on_failure>
        </default>
    .....
    </profiles>
</clickhouse>

```
# 5 \- Fetch Alter Table

Fetch Alter Table# FETCH Parts from Zookeeper

This is a detailed explanation on how to move data by fetching partitions or parts between replicas

### Get partitions by database and table:


```
SELECT
    hostName() AS host,
    database,
    table
    partition_id,
    name as part_id
FROM cluster('{cluster}', system.parts)
WHERE database IN ('db1','db2' ... 'dbn') AND active

```
This query will return all the partitions and parts stored in this node for the databases and their tables.

### Fetch the partitions:

Prior starting with the fetching process it is recommended to check the `system.detached_parts` table of the destination node. There is a chance that detached folders already contain some old parts, and you will have to remove them all before starting moving data. Otherwise you will attach those old parts together with the fetched parts. Also you could run into issues if there are detached folders with the same names as the ones you are fetching (not very probable, put possible). Simply delete the detached parts and continue with the process.

To fetch a partition:


```
ALTER TABLE <tablename> FETCH PARTITION <partition_id> FROM '/clickhouse/{cluster}/tables/{shard}/{table}'

```
The `FROM` path is from the zookeeper node and you have to specify the shard from you’re [fetching the partition](https://clickhouse.com/docs/en/sql-reference/statements/alter/partition#alter_fetch-partition)
. Next executing the DDL query:


```
ALTER TABLE <tablename> ATTACH PARTITION <partition_id>

```
will attach the partitions to a table. Again and because the process is manual, it is recommended to check that the fetched partitions are attached correctly and that there are no detached parts left. Check both `system.parts` and `system.detached_parts` tables.

### Detach tables and delete replicas:

If needed, after moving the data and checking that everything is sound, you can detach the tables and delete the replicas.


```
-- Required for DROP REPLICA
DETACH TABLE <table_name>;  

-- This will remove everything from /table_path_in_z/replicas/replica_name
-- but not the data. You could reattach the table again and
-- restore the replica if needed. Get the zookeeper_path and replica_name from system.replicas

SYSTEM DROP REPLICA 'replica_name' FROM ZKPATH '/table_path_in_zk/';

```
### Query to generate all the DDL:

With this query you can generate the DDL script that will do the fetch and attach operations for each table and partition.


```
SELECT
    DISTINCT
    'alter table '||database||'.'||table||' FETCH PARTITION '''||partition_id||''' FROM '''||zookeeper_path||'''; '
    ||'alter table '||database||'.'||table||' ATTACH PARTITION '''||partition_id||''';'
FROM system.parts INNER JOIN system.replicas USING (database, table)
WHERE database IN ('db1','db2' ... 'dbn') AND active

```
You could add an ORDER BY to manually make the list in the order you need, or use ORDER BY rand() to randomize it. You will then need to split the commands between the shards.

# 6 \- Remote table function

Remote table function## remote(…) table function

Suitable for moving up to hundreds of gigabytes of data.

With bigger tables recommended approach is to slice the original data by some `WHERE` condition, ideally \- apply the condition on partitioning key, to avoid writing data to many partitions at once.


```
INSERT INTO staging_table SELECT * FROM remote(...) WHERE date='2021-04-13';
INSERT INTO staging_table SELECT * FROM remote(...) WHERE date='2021-04-12';
INSERT INTO staging_table SELECT * FROM remote(...) WHERE date='2021-04-11';
....

OR 

INSERT INTO FUNCTION remote(...) SELECT * FROM staging_table WHERE date='2021-04-11';
....

```
### Q. Can it create a bigger load on the source system?

Yes, it may use disk read \& network write bandwidth. But typically write speed is worse than the read speed, so most probably the receiver side will be a bottleneck, and the sender side will not be overloaded.

While of course it should be checked, every case is different.

### Q. Can I tune INSERT speed to make it faster?

Yes, by the cost of extra memory usage (on the receiver side).

ClickHouse® tries to form blocks of data in memory and while one of limit: `min_insert_block_size_rows` or `min_insert_block_size_bytes` being hit, ClickHouse dump this block on disk. If ClickHouse tries to execute insert in parallel (`max_insert_threads > 1`), it would form multiple blocks at one time.  
So maximum memory usage can be calculated like this: `max_insert_threads * first(min_insert_block_size_rows OR min_insert_block_size_bytes)`

Default values:


```
┌─name────────────────────────┬─value─────┐
│ min_insert_block_size_rows  │ 1048545   │
│ min_insert_block_size_bytes │ 268427520 │
│ max_insert_threads          │ 0         │ <- Values 0 or 1 means that INSERT SELECT is not run in parallel.
└─────────────────────────────┴───────────┘

```
Tune those settings depending on your table average row size and amount of memory which are safe to occupy by `INSERT SELECT` query.

### Q. I’ve got the error “All connection tries failed”


```
SELECT count()
FROM remote('server.from.remote.dc:9440', 'default.table', 'admin', 'password')
Received exception from server (version 20.8.11):
Code: 519. DB::Exception: Received from localhost:9000. DB::Exception: All attempts to get table structure failed. Log:
Code: 279, e.displayText() = DB::NetException: All connection tries failed. Log:
Code: 209, e.displayText() = DB::NetException: Timeout: connect timed out: 192.0.2.1:9440 (server.from.remote.dc:9440) (version 20.8.11.17 (official build))
Code: 209, e.displayText() = DB::NetException: Timeout: connect timed out: 192.0.2.1:9440 (server.from.remote.dc:9440) (version 20.8.11.17 (official build))
Code: 209, e.displayText() = DB::NetException: Timeout: connect timed out: 192.0.2.1:9440 (server.from.remote.dc:9440) (version 20.8.11.17 (official build))

```
1. Using remote(…) table function with secure TCP port (default values is 9440\). There is remoteSecure() function for that.
2. High (\>50ms) ping between servers, values for `connect_timeout_with_failover_ms,` `connect_timeout_with_failover_secure_ms` need’s to be adjusted accordingly.

Default values:


```
┌─name────────────────────────────────────┬─value─┐
│ connect_timeout_with_failover_ms        │ 50    │
│ connect_timeout_with_failover_secure_ms │ 100   │
└─────────────────────────────────────────┴───────┘

```
### Example


```
#!/bin/bash

table='...'
database='bvt'
local='...'
remote='...'
CH="clickhouse-client"   # you may add auth here 
settings="  max_insert_threads=20, 
            max_threads=20, 
            min_insert_block_size_bytes = 536870912, 
            min_insert_block_size_rows = 16777216, 
            max_insert_block_size = 16777216,
            optimize_on_insert=0";

# need it to create temp table with same structure (suitable for attach)
params=$($CH -h $remote -q "select partition_key,sorting_key,primary_key from system.tables where table='$table' and database = '$database' " -f TSV)
IFS=$'\t' read -r partition_key sorting_key primary_key <<< $params

$CH -h $local \  # get list of source partitions
-q "select distinct partition from system.parts where table='$table' and database = '$database' "

while read -r partition; do
# check that the partition is already copied
  if [ `$CH -h $remote -q " select count() from system.parts table='$table' and database = '$database' and partition='$partition'"` -eq 0 ] ; then
      $CH -n -h $remote -q "
        create temporary table temp as $database.$table engine=MergeTree -- 23.3 required for temporary table
           partition by ($partition_key) primary key ($primary_key)  order by ($sorting_key);
        -- SYSTEM STOP MERGES temp; -- maybe....
        set $settings;
        insert into temp select * from remote($local,$database.$table) where _partition='$partition'
        -- order by ($sorting_key) -- maybe....
        ;
        alter table $database.$table attach partition $partition from temp
  "
  fi
done

```
# 7 \- Moving ClickHouse to Another Server

Copying Multi\-Terabyte Live ClickHouse to Another ServerWhen migrating a large, live ClickHouse cluster (multi\-terabyte scale) to a new server or cluster, the goal is to minimize downtime while ensuring data consistency. A practical method is to use **incremental `rsync`** in multiple passes, combined with ClickHouse’s replication features.

1. **Prepare the new cluster**
	- Ensure the new cluster is set up with its own ZooKeeper (or Keeper).
	- Configure ClickHouse but keep it stopped initially.
	- For clickhouse\-operator instances, you can stop all pods by CHI definition:


```
spec:
  stop: "true"

```
and attach volumes (PVC) to a service pod.

2. **Initial data sync**

Run a full recursive sync of the data directory from the old server to the new one:


```
rsync -ravlW --delete /var/lib/clickhouse/ user@new_host:/var/lib/clickhouse/

```
Explanation of flags:


	- `r`: recursive, includes all subdirectories.
	- `a`: archive mode (preserves symlinks, permissions, timestamps, ownership, devices).
	- `v`: verbose, shows progress.
	- `l`: copy symlinks as symlinks.
	- `W`: copy whole files instead of using rsync’s delta algorithm (faster for large DB files).
	- –delete: remove files from the destination that don’t exist on the source.If you plan to run several replicas on a new cluster, rsync data to all of them. To save the performance of production servers, you can copy data to 1 new replica and then use it as a source for others. You can start with a single replica and add more after switching, but it will take more time afterward, as additional replicas need to pull all the data.

Add –bwlimit\=100000 to preserve the performance of the production cluster while copying a lot of data.

Consider shards as independent clusters.
3. **Incremental re\-syncs**


	- Repeat the `rsync` step multiple times while the old cluster is live.
	- Each subsequent run will copy only changes and reduce the final sync time.
4. **Restore replication metadata**


	- Start the new ClickHouse node(s).
	- Run `SYSTEM RESTORE REPLICA table_name` to rebuild replication metadata in ZooKeeper.
5. **Test the application**


	- Point your test environment to the new cluster.
	- Validate queries, schema consistency, and application behavior.
6. **Final sync and switchover**


	- Stop ClickHouse on the old cluster.
	- Immediately run a final incremental `rsync` to catch last\-minute changes.
	- Reinitialize ZooKeeper/Keeper database (stop/clear snapshots/start).
	- Run `SYSTEM RESTORE REPLICA table_name` to rebuild replication metadata in ZooKeeper again.
	- Start ClickHouse on the new cluster and switch production traffic.
	- add more replicas as needed

NOTES:

1. To restore metadata on all cluster nodes by a single command, use `ON CLUSTER` modifier for the RESTORE REPLICA command.
2. You can build a script to run restore replica commands over all replicated tables by query:


```
select 'SYSTEM RESTORE REPLICA ' || database || '.' || table || ' ON CLUSTER {cluster} ;'
from system.tables
where engine ilike 'Replicated%'

```
2. If you are using a mount point that differs from /var/lib/clickhouse/data, adjust the rsync command accordingly to point to the correct location. For example, suppose you reconfigure the storage path as follows in /etc/clickhouse\-server/config.d/config.xml.


```
<clickhouse>
    <!-- Path to data directory, with trailing slash. -->
    <path>/data1/clickhouse/</path>
    ...
</clickhouse>

```
You’ll need to use `/data1/clickhouse` instead of `/var/lib/clickhouse` in the rsync paths.

3. ClickHouse Docker container image does not have rsync installed. Add it using apt\-get or run sidecar in k8s or run a service pod with volumes attached.
4. If you running rsync to multiple replicas or planning to use same (Zoo)Keeper ensemble for source and destination ClickHouse servers, you need to remove server uuid file after syncing data with rsync.


```
rm /var/lib/clickhouse/uuid

```
Otherwise, it can lead to hard\-to\-debug replication issues. Replicas will break each other’s sessions with (Zoo)Keeper.
