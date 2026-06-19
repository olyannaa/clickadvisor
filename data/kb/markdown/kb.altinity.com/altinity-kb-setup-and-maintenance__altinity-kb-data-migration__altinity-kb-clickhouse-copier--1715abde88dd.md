# clickhouse\-copier \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. [Data Migration](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/)
3. clickhouse\-copier
# clickhouse\-copier

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



---

##### [clickhouse\-copier 20\.3 and earlier](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/altinity-kb-clickhouse-copier/altinity-kb-clickhouse-copier-20.3-and-earlier/)

##### [clickhouse\-copier 20\.4 \- 21\.6](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/altinity-kb-clickhouse-copier/altinity-kb-clickhouse-copier-20.4_21.6/)

##### [Kubernetes job for clickhouse\-copier](/altinity-kb-setup-and-maintenance/altinity-kb-data-migration/altinity-kb-clickhouse-copier/altinity-kb-clickhouse-copier-kubernetes-job/)

Kubernetes job for `clickhouse-copier`

Last modified 2024\.08\.02: [Updated clickhouse\-copier links (b28723c)](https://github.com/Altinity/altinityknowledgebase/commit/b28723ccbd3c7286f0fa09bd236bc216cc4e1681)
