# clickhouse\-copier \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/altinity-kb-clickhouse-copier/).

# clickhouse\-copier

clickhouse\-copier- 1: [clickhouse\-copier 20\.3 and earlier](#pg-e1f1d825521583c133a8d3bf2a72f6e7)
- 2: [clickhouse\-copier 20\.4 \- 21\.6](#pg-4907e613a878d5b7819f49cc367b9f3f)
- 3: [Kubernetes job for clickhouse\-copier](#pg-092d5c190f9504b9126ab5f7779a2089)

The description of the utility and its parameters, as well as examples of the config files that you need to create for the copier are in the official repo for the [ClickHouse® copier utility](https://github.com/clickhouse/copier/)

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
# 1 \- clickhouse\-copier 20\.3 and earlier

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
# 2 \- clickhouse\-copier 20\.4 \- 21\.6

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
# 3 \- Kubernetes job for clickhouse\-copier

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
