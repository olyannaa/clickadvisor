# Recovering from complete metadata loss in ZooKeeper \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. [ZooKeeper](/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/)
3. Recovering from complete metadata loss in ZooKeeper
# Recovering from complete metadata loss in ZooKeeper

## Problem

Every ClickHouse® user experienced a loss of ZooKeeper one day. While the data is available and replicas respond to queries, inserts are no longer possible. ClickHouse uses ZooKeeper in order to store the reference version of the table structure and part of data, and when it is not available can not guarantee data consistency anymore. Replicated tables turn to the read\-only mode. In this article we describe step\-by\-step instructions of how to restore ZooKeeper metadata and bring ClickHouse cluster back to normal operation.

In order to restore ZooKeeper we have to solve two tasks. First, we need to restore table metadata in ZooKeeper. Currently, the only way to do it is to recreate the table with the `CREATE TABLE DDL` statement.


```
CREATE TABLE table_name ... ENGINE=ReplicatedMergeTree('zookeeper_path','replica_name');

```
The second and more difficult task is to populate zookeeper with information of ClickHouse data parts. As mentioned above, ClickHouse stores the reference data about all parts of replicated tables in ZooKeeper, so we have to traverse all partitions and re\-attach them to the recovered replicated table in order to fix that.

#### Info

Starting from ClickHouse version 21\.7 there is SYSTEM RESTORE REPLICA command[https://altinity.com/blog/a\-new\-way\-to\-restore\-clickhouse\-after\-zookeeper\-metadata\-is\-lost](https://altinity.com/blog/a-new-way-to-restore-clickhouse-after-zookeeper-metadata-is-lost)

## Test case

Let’s say we have replicated table `table_repl`.


```
CREATE TABLE table_repl 
(
   `number` UInt32
)
ENGINE = ReplicatedMergeTree('/clickhouse/{cluster}/tables/{shard}/table_repl','{replica}')
PARTITION BY intDiv(number, 1000)
ORDER BY number;

```
And populate it with some data


```
SELECT * FROM system.zookeeper WHERE path='/clickhouse/cluster_1/tables/01/';

INSERT INTO table_repl SELECT * FROM numbers(1000,2000);

SELECT partition, sum(rows) AS rows, count() FROM system.parts WHERE table='table_repl' AND active GROUP BY partition;

```
Now let’s remove metadata in zookeeper using `ZkCli.sh` at ZooKeeper host:


```
deleteall  /clickhouse/cluster_1/tables/01/table_repl

```
And try to resync ClickHouse replica state with zookeeper:


```
SYSTEM RESTART REPLICA table_repl;

```
If we try to insert some data in the table, error happens:


```
INSERT INTO table_repl SELECT number AS number FROM numbers(1000,2000) WHERE number % 2 = 0;

```
And now we have an exception that we lost all metadata in zookeeper. It is time to recover!

## Current Solution

1. Detach replicated table.


```
DETACH TABLE table_repl;

```
2. Save the table’s attach script and change engine of replicated table to non\-replicated \*mergetree analogue. Table definition is located in the ‘metadata’ folder, ‘`/var/lib/clickhouse/metadata/default/table_repl.sql`’ in our example. Please make a backup copy and modify the file as follows:


```
ATTACH TABLE table_repl
(
   `number` UInt32
)
ENGINE = ReplicatedMergeTree('/clickhouse/{cluster}/tables/{shard}/table_repl', '{replica}')
PARTITION BY intDiv(number, 1000)
ORDER BY number
SETTINGS index_granularity = 8192

```
Needs to be replaced with this:


```
ATTACH TABLE table_repl
(
   `number` UInt32
)
ENGINE = MergeTree()
PARTITION BY intDiv(number, 1000)
ORDER BY number
SETTINGS index_granularity = 8192

```
3. Attach non\-replicated table.


```
ATTACH TABLE table_repl;

```
4. Rename non\-replicated table.


```
RENAME TABLE table_repl TO table_repl_old;

```
5. Create a new replicated table. Take the saved attach script and replace ATTACH with CREATE, and run it.


```
CREATE TABLE table_repl
(
   `number` UInt32
)
ENGINE = ReplicatedMergeTree('/clickhouse/{cluster}/tables/{shard}/table_repl', '{replica}')
PARTITION BY intDiv(number, 1000)
ORDER BY number
SETTINGS index_granularity = 8192

```
6. Attach parts from old table to new.


```
ALTER TABLE table_repl ATTACH PARTITION 1 FROM table_repl_old;

ALTER TABLE table_repl ATTACH PARTITION 2 FROM table_repl_old;

```

If the table has many partitions, it may require some shell script to make it easier.

### Automated approach

For a large number of tables, you can use script [https://github.com/Altinity/clickhouse\-zookeeper\-recovery](https://github.com/Altinity/clickhouse-zookeeper-recovery)
which partially automates the above approach.

Last modified 2024\.07\.30: [Site cleanup, mostly minor changes (a4a9639\)](https://github.com/Altinity/altinityknowledgebase/commit/a4a96398d6e97ac2935110b426947487e2e202d9)
