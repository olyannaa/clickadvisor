# DDLWorker and DDL queue problems \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-setup-and-maintenance/altinity-kb-ddlworker/).

# DDLWorker and DDL queue problems

Finding and troubleshooting problems in the `distributed_ddl_queue`- 1: [There are N unfinished hosts (0 of them are currently active).](#pg-7f5f8971a74cdc0af853041c9dd18c8f)

DDLWorker is a subprocess (thread) of `clickhouse-server` that executes `ON CLUSTER` tasks at the node.

When you execute a DDL query with `ON CLUSTER mycluster` section, the query executor at the current node reads the cluster `mycluster` definition (remote\_servers / system.clusters) and places tasks into Zookeeper znode `task_queue/ddl/...` for members of the cluster `mycluster`.

DDLWorker at all ClickHouse® nodes constantly check this `task_queue` for their tasks, executes them locally, and reports about the results back into `task_queue`.

The common issue is the different hostnames/IPAddresses in the cluster definition and locally.

So if the initiator node puts tasks for a host named Host1\. But the Host1 thinks about own name as localhost or **xdgt634678d** (internal docker hostname) and never sees tasks for the Host1 because is looking tasks for **xdgt634678d.** The same with internal VS external IP addresses.

## DDLWorker thread crashed

That causes ClickHouse to stop executing `ON CLUSTER` tasks.

Check that DDLWorker is alive:


```
ps -eL|grep DDL
18829 18876 ?        00:00:00 DDLWorkerClnr
18829 18879 ?        00:00:00 DDLWorker

ps -ef|grep 18829|grep -v grep
clickho+ 18829 18828  1 Feb09 ?        00:55:00 /usr/bin/clickhouse-server --con...

```
As you can see there are two threads: `DDLWorker` and `DDLWorkerClnr`.

The second thread – `DDLWorkerCleaner` cleans old tasks from `task_queue`. You can configure how many recent tasks to store:


```
config.xml
<yandex>
    <distributed_ddl>
        <path>/clickhouse/task_queue/ddl</path>
        <pool_size>1</pool_size>
        <max_tasks_in_queue>1000</max_tasks_in_queue>
        <task_max_lifetime>604800</task_max_lifetime>
        <cleanup_delay_period>60</cleanup_delay_period>
    </distributed_ddl>
</yandex>

```
Default values:

**cleanup\_delay\_period** \= 60 seconds – Sets how often to start cleanup to remove outdated data.

**task\_max\_lifetime** \= 7 \* 24 \* 60 \* 60 (in seconds \= week) – Delete task if its age is greater than that.

**max\_tasks\_in\_queue** \= 1000 – How many tasks could be in the queue.

**pool\_size** \= 1 \- How many ON CLUSTER queries can be run simultaneously.

## Too intensive stream of ON CLUSTER command

Generally, it’s a bad design, but you can increase pool\_size setting

## Stuck DDL tasks in the distributed\_ddl\_queue

Sometimes [DDL tasks](/altinity-kb-setup-and-maintenance/altinity-kb-ddlworker/)
(the ones that use ON CLUSTER) can get stuck in the `distributed_ddl_queue` because the replicas can overload if multiple DDLs (thousands of CREATE/DROP/ALTER) are executed at the same time. This is very normal in heavy ETL jobs.This can be detected by checking the `distributed_ddl_queue` table and see if there are tasks that are not moving or are stuck for a long time.

If these DDLs are completed in some replicas but failed in others, the simplest way to solve this is to execute the failed command in the missed replicas without ON CLUSTER. If most of the DDLs failed, then check the number of unfinished records in `distributed_ddl_queue` on the other nodes, because most probably it will be as high as thousands.

First, backup the `distributed_ddl_queue` into a table so you will have a snapshot of the table with the states of the tasks. You can do this with the following command:


```
CREATE TABLE default.system_distributed_ddl_queue AS SELECT * FROM system.distributed_ddl_queue;

```
After this, we need to check from the backup table which tasks are not finished and execute them manually in the missed replicas, and review the pipeline which do `ON CLUSTER` command and does not abuse them. There is a new `CREATE TEMPORARY TABLE` command that can be used to avoid the `ON CLUSTER` command in some cases, where you need an intermediate table to do some operations and after that you can `INSERT INTO` the final table or do `ALTER TABLE final ATTACH PARTITION FROM TABLE temp` and this temp table will be dropped automatically after the session is closed.

# 1 \- There are N unfinished hosts (0 of them are currently active).

There are N unfinished hosts (0 of them are currently active).Sometimes your Distributed DDL queries are being stuck, and not executing on all or subset of nodes, there are a lot of possible reasons for that kind of behavior, so it would take some time and effort to investigate.

## Possible reasons

### ClickHouse® node can’t recognize itself


```
SELECT * FROM system.clusters; -- check is_local column, it should have 1 for itself

```

```
getent hosts clickhouse.local.net # or other name which should be local
hostname --fqdn

cat /etc/hosts
cat /etc/hostname

```
### Debian / Ubuntu

There is an issue in Debian based images, when hostname being mapped to 127\.0\.1\.1 address which doesn’t literally match network interface and ClickHouse fails to detect this address as local.

<https://github.com/ClickHouse/ClickHouse/issues/23504>

#### Previous task is being executed and taking some time

It’s usually some heavy operations like merges, mutations, alter columns, so it make sense to check those tables:


```
SHOW PROCESSLIST;
SELECT * FROM system.merges;
SELECT * FROM system.mutations;

```
In that case, you can just wait completion of previous task.

### Previous task is stuck because of some error

In that case, the first step is to understand which exact task is stuck and why. There are some queries which can help with that.


```
-- list of all distributed ddl queries, path can be different in your installation
SELECT * FROM system.zookeeper WHERE path = '/clickhouse/task_queue/ddl/';

-- information about specific task.
SELECT * FROM system.zookeeper WHERE path = '/clickhouse/task_queue/ddl/query-0000001000/';
SELECT * FROM system.zookeeper WHERE path = '/clickhouse/task_queue/ddl/' AND name = 'query-0000001000';
-- 22.3
SELECT * FROM system.zookeeper WHERE path like '/clickhouse/task_queue/ddl/query-0000001000/%' 
ORDER BY ctime, path SETTINGS allow_unrestricted_reads_from_keeper='true'
-- 22.6
SELECT path, name, value, ctime, mtime 
FROM system.zookeeper WHERE path like '/clickhouse/task_queue/ddl/query-0000001000/%' 
ORDER BY ctime, path SETTINGS allow_unrestricted_reads_from_keeper='true'

-- How many nodes executed this task
SELECT name, numChildren as finished_nodes FROM system.zookeeper
WHERE path = '/clickhouse/task_queue/ddl/query-0000001000/' AND name = 'finished';

┌─name─────┬─finished_nodes─┐
│ finished │              0 │
└──────────┴────────────────┘

-- The nodes that are running the task
SELECT name, value, ctime, mtime FROM system.zookeeper 
WHERE path = '/clickhouse/task_queue/ddl/query-0000001000/active/';

-- What was the result for the finished nodes 
SELECT name, value, ctime, mtime FROM system.zookeeper 
WHERE path = '/clickhouse/task_queue/ddl/query-0000001000/finished/';

-- Latest successfull executed tasks from query_log.
SELECT query FROM system.query_log WHERE query LIKE '%ddl_entry%' AND type = 2 ORDER BY event_time DESC LIMIT 5;

SELECT
    FQDN(),
    *
FROM clusterAllReplicas('cluster', system.metrics)
WHERE metric LIKE '%MaxDDLEntryID%'

┌─FQDN()───────────────────┬─metric────────┬─value─┬─description───────────────────────────┐
│ chi-ab.svc.cluster.local │ MaxDDLEntryID │  1468 │ Max processed DDL entry of DDLWorker. │
└──────────────────────────┴───────────────┴───────┴───────────────────────────────────────┘
┌─FQDN()───────────────────┬─metric────────┬─value─┬─description───────────────────────────┐
│ chi-ab.svc.cluster.local │ MaxDDLEntryID │  1468 │ Max processed DDL entry of DDLWorker. │
└──────────────────────────┴───────────────┴───────┴───────────────────────────────────────┘
┌─FQDN()───────────────────┬─metric────────┬─value─┬─description───────────────────────────┐
│ chi-ab.svc.cluster.local │ MaxDDLEntryID │  1468 │ Max processed DDL entry of DDLWorker. │
└──────────────────────────┴───────────────┴───────┴───────────────────────────────────────┘


-- Information about task execution from logs.
grep -C 40 "ddl_entry" /var/log/clickhouse-server/clickhouse-server*.log

```
### Issues that can prevent task execution

#### Obsolete Replicas

Obsolete replicas left in zookeeper.


```
SELECT database, table, zookeeper_path, replica_path zookeeper FROM system.replicas WHERE total_replicas != active_replicas;

SELECT * FROM system.zookeeper WHERE path = '/clickhouse/cluster/tables/01/database/table/replicas';

SYSTEM DROP REPLICA 'replica_name';

SYSTEM STOP REPLICATION QUEUES;
SYSTEM START REPLICATION QUEUES;

```
[https://clickhouse.tech/docs/en/sql\-reference/statements/system/\#query\_language\-system\-drop\-replica](https://clickhouse.tech/docs/en/sql-reference/statements/system/%5c#query_language-system-drop-replica)

#### Tasks manually removed from DDL queue

Task were removed from DDL queue, but left in Replicated\*MergeTree table queue.


```
grep -C 40 "ddl_entry" /var/log/clickhouse-server/clickhouse-server*.log

/var/log/clickhouse-server/clickhouse-server.log:2021.05.04 12:41:28.956888 [ 599 ] {} <Debug> DDLWorker: Processing task query-0000211211 (ALTER TABLE db.table_local ON CLUSTER `all-replicated` DELETE WHERE id = 1)
/var/log/clickhouse-server/clickhouse-server.log:2021.05.04 12:41:29.053555 [ 599 ] {} <Error> DDLWorker: ZooKeeper error: Code: 999, e.displayText() = Coordination::Exception: No node, Stack trace (when copying this message, always include the lines below):
/var/log/clickhouse-server/clickhouse-server.log-
/var/log/clickhouse-server/clickhouse-server.log-0. Coordination::Exception::Exception(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, Coordination::Error, int) @ 0xfb2f6b3 in /usr/bin/clickhouse
/var/log/clickhouse-server/clickhouse-server.log-1. Coordination::Exception::Exception(Coordination::Error) @ 0xfb2fb56 in /usr/bin/clickhouse
/var/log/clickhouse-server/clickhouse-server.log:2. DB::DDLWorker::createStatusDirs(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::shared_ptr<zkutil::ZooKeeper> const&) @ 0xeb3127a in /usr/bin/clickhouse
/var/log/clickhouse-server/clickhouse-server.log:3. DB::DDLWorker::processTask(DB::DDLTask&) @ 0xeb36c96 in /usr/bin/clickhouse
/var/log/clickhouse-server/clickhouse-server.log:4. DB::DDLWorker::enqueueTask(std::__1::unique_ptr<DB::DDLTask, std::__1::default_delete<DB::DDLTask> >) @ 0xeb35f22 in /usr/bin/clickhouse
/var/log/clickhouse-server/clickhouse-server.log-5. ? @ 0xeb47aed in /usr/bin/clickhouse
/var/log/clickhouse-server/clickhouse-server.log-6. ThreadPoolImpl<ThreadFromGlobalPool>::worker(std::__1::__list_iterator<ThreadFromGlobalPool, void*>) @ 0x8633bcd in /usr/bin/clickhouse
/var/log/clickhouse-server/clickhouse-server.log-7. ThreadFromGlobalPool::ThreadFromGlobalPool<void ThreadPoolImpl<ThreadFromGlobalPool>::scheduleImpl<void>(std::__1::function<void ()>, int, std::__1::optional<unsigned long>)::'lambda1'()>(void&&, void ThreadPoolImpl<ThreadFromGlobalPool>::scheduleImpl<void>(std::__1::function<void ()>, int, std::__1::optional<unsigned long>)::'lambda1'()&&...)::'lambda'()::operator()() @ 0x863612f in /usr/bin/clickhouse
/var/log/clickhouse-server/clickhouse-server.log-8. ThreadPoolImpl<std::__1::thread>::worker(std::__1::__list_iterator<std::__1::thread, void*>) @ 0x8630ffd in /usr/bin/clickhouse
/var/log/clickhouse-server/clickhouse-server.log-9. ? @ 0x8634bb3 in /usr/bin/clickhouse
/var/log/clickhouse-server/clickhouse-server.log-10. start_thread @ 0x9609 in /usr/lib/x86_64-linux-gnu/libpthread-2.31.so
/var/log/clickhouse-server/clickhouse-server.log-11. __clone @ 0x122293 in /usr/lib/x86_64-linux-gnu/libc-2.31.so
/var/log/clickhouse-server/clickhouse-server.log- (version 21.1.8.30 (official build))
/var/log/clickhouse-server/clickhouse-server.log:2021.05.04 12:41:29.053951 [ 599 ] {} <Debug> DDLWorker: Processing task query-0000211211 (ALTER TABLE db.table_local ON CLUSTER `all-replicated` DELETE WHERE id = 1)

```
Context of this problem is:

- Constant pressure of cheap ON CLUSTER DELETE queries.
- One replica was down for a long amount of time (multiple days).
- Because of pressure on the DDL queue, it purged old records due to the `task_max_lifetime` setting.
- When a lagging replica comes up, it’s fail’s execute old queries from DDL queue, because at this point they were purged from it.

Solution:

- Reload/Restore this replica from scratch.

#### DDL path was changed in Zookeeper without restarting ClickHouse

Changing the DDL queue path in Zookeeper without restarting ClickHouse will make ClickHouse confused. If you need to do this ensure that you restart ClickHouse before submitting additional distributed DDL commands. Here’s an example.


```
-- Path before change:
SELECT *
FROM system.zookeeper
WHERE path = '/clickhouse/clickhouse101/task_queue'

┌─name─┬─value─┬─path─────────────────────────────────┐
│ ddl  │       │ /clickhouse/clickhouse101/task_queue │
└──────┴───────┴──────────────────────────────────────┘

-- Path after change
SELECT *
FROM system.zookeeper
WHERE path = '/clickhouse/clickhouse101/task_queue'

┌─name─┬─value─┬─path─────────────────────────────────┐
│ ddl2 │       │ /clickhouse/clickhouse101/task_queue │
└──────┴───────┴──────────────────────────────────────┘

```
The reason is that ClickHouse will not “see” this change and will continue to look for tasks in the old path. Altering paths in Zookeeper should be avoided if at all possible. If necessary it must be done *very carefully*.
