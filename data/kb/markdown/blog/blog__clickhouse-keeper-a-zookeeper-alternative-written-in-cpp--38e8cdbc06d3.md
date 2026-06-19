# ClickHouse Keeper: A ZooKeeper alternative written in C\+\+


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Keeper: A ZooKeeper alternative written in C\+\+

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_white_add9f20d0f.png&w=96&q=75)Tom Schreiber and Derek ChiaSep 27, 2023 · 27 minutes read## Introduction [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#introduction)


ClickHouse is the fastest and most resource\-efficient open\-source database for real\-time applications and analytics. As one of its components, ClickHouse Keeper is a fast, more resource\-efficient, and feature\-rich alternative to ZooKeeper. This open\-source component provides a highly reliable metadata store, as well as coordination and synchronization mechanisms. It was originally developed for use with ClickHouse when it is deployed as a distributed system in a self\-managed setup or a hosted offering like CloudHouse Cloud. However, we believe that the broader community can benefit from this project in additional use cases.


In this post, we describe the motivation, advantages, and development of ClickHouse Keeper and preview our next planned improvements. Moreover, we introduce a reusable benchmark suite, which allows us to simulate and benchmark typical ClickHouse Keeper usage patterns easily. Based on this, we present benchmark results highlighting that ClickHouse Keeper uses **up to 46 times less memory than ZooKeeper ​​for the same volume of data while maintaining performance close to ZooKeeper**.


## Motivation [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#motivation)


Modern [distributed systems](https://en.wikipedia.org/wiki/Distributed_computing) require a shared and reliable [information repository](https://en.wikipedia.org/wiki/Information_repository) and [consensus](https://en.wikipedia.org/wiki/Consensus_(computer_science)) system for coordinating and synchronizing distributed operations. For ClickHouse, [ZooKeeper](https://zookeeper.apache.org/) was initially chosen for this. It was reliable through its wide usage, provided a simple and powerful API, and offered reasonable performance.


However, not only performance but also resource efficiency and scalability have always been a top [priority](https://clickhouse.com/docs/en/faq/general/why-clickhouse-is-so-fast) for ClickHouse. ZooKeeper, being a Java ecosystem project, did not fit into our primarily C\+\+ codebase very elegantly, and as we used it at a higher and higher scale, we started running into resource usage and operational challenges. In order to overcome these shortcomings of ZooKeeper, we built ClickHouse Keeper from scratch, taking into account additional requirements and goals our project needed to address.


ClickHouse Keeper is a drop\-in replacement for ZooKeeper, with a fully compatible client protocol and the same data model. Beyond that, it offers the following benefits:


- Easier setup and operation: ClickHouse Keeper is implemented in C\+\+ instead of Java and, therefore, [can](https://clickhouse.com/company/events/scaling-clickhouse?utm_source=google.com&utm_medium=paid_search&utm_campaign=19979782024_153259814612&utm_content=655879611258&utm_term=clickhouse_g_c&gclid=Cj0KCQjwuZGnBhD1ARIsACxbAVgLga7td3T2ccBaJ9zCxt4t_A2RQT_5MdK-qqnLVvp0ufgElNk5JSoaAsMtEALw_wcB) run embedded in ClickHouse or standalone
- Snapshots and logs consume much less disk space due to better compression
- No limit on the default packet and node data size (it [is](https://zookeeper.apache.org/doc/r3.4.11/zookeeperAdmin.html#Unsafe+Options) 1 MB in ZooKeeper)
- No [ZXID overflow](https://issues.apache.org/jira/browse/ZOOKEEPER-1277) issue (it forces a restart for every 2B transactions in ZooKeeper)
- Faster recovery after network partitions due to the use of a better\-distributed consensus protocol
- Additional [consistency](https://en.wikipedia.org/wiki/Consistency_model) guarantees: ClickHouse Keeper provides the same consistency guarantees as ZooKeeper \- [linearizable](https://en.wikipedia.org/wiki/Linearizability) writes plus strict ordering of operations inside the same [session](https://zookeeper.apache.org/doc/r3.5.10/zookeeperProgrammers.html#ch_zkSessions). Additionally, and optionally (via a [quorum\_reads](https://clickhouse.com/docs/en/guides/sre/keeper/clickhouse-keeper#configuration) setting), ClickHouse Keeper provides linearizable reads.
- ClickHouse Keeper is more resource efficient and uses less memory for the same volume of data (we will demonstrate this later in this blog)


The development of ClickHouse Keeper [started](https://github.com/ClickHouse/ClickHouse/pull/19580) as an embedded service in the ClickHouse server in February 2021\. In the same year, a standalone mode was [introduced](https://github.com/ClickHouse/ClickHouse/pull/24059), and [Jepsen](https://jepsen.io/) tests were [added](https://github.com/ClickHouse/ClickHouse/pull/21677) \- every 6 hours, we run automated [tests](https://github.com/ClickHouse/ClickHouse/tree/master/tests/jepsen.clickhouse) with several different workflows and failure scenarios to validate the correctness of the consensus mechanism.


At the time of writing this blog, ClickHouse Keeper has been production\-ready for [more](https://clickhouse.com/blog/clickhouse-22-3-lts-released#clickhouse-keeper) than one and a half years and has been deployed at scale in our own [ClickHouse Cloud](https://clickhouse.com/cloud) since its first private preview launch in May 2022\.


In the rest of the blog, we sometimes refer to ClickHouse Keeper as simply “Keeper,” as we often call it internally.


## Usage in ClickHouse [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#usage-in-clickhouse)


Generally, anything requiring consistency between multiple ClickHouse servers relies on Keeper:


- Keeper provides the coordination system for data [replication](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replication) in self\-managed [shared\-nothing](https://en.wikipedia.org/wiki/Shared-nothing_architecture) ClickHouse [clusters](https://clickhouse.com/company/events/scaling-clickhouse)
- Automatic [insert deduplication](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse#5-deduplication-at-insert-time) for replicated tables of the [mergetree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family) engine family is based on block\-hash\-sums [stored](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings#replicated-deduplication-window) in Keeper
- Keeper provides consensus for [part](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree#mergetree-data-storage) names (based on sequential [block](https://clickhouse.com/docs/en/development/architecture#block) numbers) and for assigning part [merges](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#data-needs-to-be-batched-for-optimal-performance) and [mutations](https://clickhouse.com/docs/en/sql-reference/statements/alter#mutations) to specific cluster nodes
- Keeper is used under the hood of the [KeeperMap table engine](https://clickhouse.com/docs/en/engines/table-engines/special/keeper-map) which allows you to use Keeper as consistent key\-value store with linearizable writes and sequentially consistent reads
	- [read](https://clickhouse.com/blog/building-real-time-applications-with-clickhouse-and-hex-notebook-keeper-engine) about an application utilizing this for implementing a task scheduling queue on top of ClickHouse
	- [Kafka Connect Sink](https://github.com/ClickHouse/clickhouse-kafka-connect) uses this table engine as a reliable [state store](https://github.com/ClickHouse/clickhouse-kafka-connect/blob/main/docs/DESIGN.md#storing-state) for [implementing](https://github.com/ClickHouse/clickhouse-kafka-connect/blob/main/docs/DESIGN.md#state-machine) exactly\-once delivery [guarantees](https://github.com/ClickHouse/clickhouse-kafka-connect/blob/main/docs/DESIGN.md#addressing-exactly-once)
- Keeper [keeps track](https://clickhouse.com/blog/clickhouse-release-23-08#streaming-consumption-from-s3-sergei-katkovskiy-kseniia-sumarokova) of consumed files in the [S3Queue table engine](https://clickhouse.com/docs/en/engines/table-engines/integrations/s3queue)
- [Replicated Database engine](https://clickhouse.com/docs/en/engines/database-engines/replicated) stores all metadata in Keeper
- Keeper is used for coordinating [Backups](https://clickhouse.com/docs/en/operations/backup) with the [ON CLUSTER](https://clickhouse.com/docs/en/sql-reference/distributed-ddl) clause
- [User defined functions](https://clickhouse.com/docs/en/sql-reference/functions/udf) can be [stored](https://github.com/ClickHouse/ClickHouse/pull/46085) in Keeper
- [Access control](https://clickhouse.com/docs/en/operations/access-rights) information can be [stored](https://github.com/ClickHouse/ClickHouse/pull/27426) in Keeper
- Keeper is [used](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates) as a shared central store for all metadata in [ClickHouse Cloud](https://clickhouse.com/cloud)


## Observing Keeper [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#observing-keeper)


In the following sections, in order to observe (and later model in a benchmark) some of ClickHouse Cloud’s interaction with Keeper, we load a month of data from the [WikiStat](https://clickhouse.com/docs/en/getting-started/example-datasets/wikistat) data set into a [table](https://gist.github.com/tom-clickhouse/7c88c3a231c602b44382f2ffdf98148c) in a [ClickHouse Cloud service](https://clickhouse.com/docs/en/cloud-quick-start) with 3 nodes. Each node has 30 CPU cores and 120 GB RAM. Each service uses its own dedicated ClickHouse Keeper service consisting of 3 servers, with 3 CPU cores and 2 GB RAM per Keeper server.


The following diagram illustrates this data\-loading scenario:
![Keeper-01.png](/uploads/Keeper_01_a59945bd61.png)


### ① Data loading [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#-data-loading)


Via a data load [query](https://gist.github.com/tom-clickhouse/0c1b4d70c4fbebd7a14eb756d1ebc914), we load \~4\.64 billion rows from \~740 compressed files (one file represents one specific hour of one specific day) in [parallel](https://clickhouse.com/docs/en/sql-reference/table-functions/s3Cluster) with all three ClickHouse servers in \~ 100 seconds. The peak main memory usage on a single ClickHouse server was \~107 GB:



```
0 rows in set. Elapsed: 101.208 sec. Processed 4.64 billion rows, 40.58 GB (45.86 million rows/s., 400.93 MB/s.)
Peak memory usage: 107.75 GiB.

```

### ② Part creations [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#-part-creations)


For storing the data, the 3 ClickHouse servers together [created](https://gist.github.com/tom-clickhouse/6a5ee7bff4ee7e724d0e2c326ab30354) 240 initial [parts](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree#mergetree-data-storage) in [object storage](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#clickhouse-cloud-enters-the-stage). The average number of rows per initial part was \~19 million rows, respectively. The average size was \~100 MiB, and the total amount of inserted rows is 4\.64 billion:



```
┌─parts──┬─rows_avg──────┬─size_avg───┬─rows_total───┐
│ 240.00 │ 19.34 million │ 108.89 MiB │ 4.64 billion │
└────────┴───────────────┴────────────┴──────────────┘

```

Because our data load query utilizes the [s3Cluster](https://clickhouse.com/docs/en/sql-reference/table-functions/s3Cluster) table function, the creation of the initial parts [is](https://gist.github.com/tom-clickhouse/f9c683945ea805062f7f5f63bf8b1389) evenly distributed over the 3 ClickHouse servers of our ClickHouse Cloud services:



```
┌─n─┬─parts─┬─rows_total───┐
│ 1 │ 86.00 │ 1.61 billion │
│ 2 │ 76.00 │ 1.52 billion │
│ 3 │ 78.00 │ 1.51 billion │
└───┴───────┴──────────────┘

```

### ③ Part merges [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#-part-merges)


During the data loading, in the background, ClickHouse [executed](https://gist.github.com/tom-clickhouse/05f40f98dbcc6b28be6de3f96668f37b) 1706 part [merges](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#data-needs-to-be-batched-for-optimal-performance), respectively:



```
┌─merges─┐
│   1706 │
└────────┘

```

### ④ Keeper interactions [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#-keeper-interactions)


ClickHouse Cloud completely [separates](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#clickhouse-cloud-enters-the-stage) the storage of data and metadata from the servers. All data parts [are](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#shared-object-storage-for-data-availability) stored in shared object storage, and all metadata [is](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#sharedmergetree-for-cloud-native-data-processing) stored in Keeper. When a ClickHouse server has written a new part to object storage (see ② above) or merged some parts to a new larger part (see ③ above), then this ClickHouse server is using a [multi](https://zookeeper.apache.org/doc/r3.4.3/api/org/apache/zookeeper/ZooKeeper.html#multi(java.lang.Iterable))\-write transaction request for updating the metadata about the new part in Keeper. This information includes the name of the part, which files belong to the part, and where the blobs corresponding to files reside in object storage. Each server has a local cache with subsets of the metadata and [gets](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#sharedmergetree-for-cloud-native-data-processing) automatically informed about data changes by a Keeper instance through a [watch](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkWatches)\-based subscription mechanism.


For our aforementioned initial part creations and background part merges, a total of \~18k Keeper requests were [executed](https://gist.github.com/tom-clickhouse/da9c0faee5f509fb0fae9c4ee5c4d667). This includes \~12k multi\-write transaction requests (containing only write\-subrequests). All other requests are a mix of read and write requests. Additionally, the ClickHouse servers received \~ 800 watch notifications from Keeper:



```
total_requests:      17705
multi_requests:      11642
watch_notifications: 822

```

We can [see](https://gist.github.com/tom-clickhouse/36b7e154f47411c5a37c764ae62a3fd8) how these requests were sent and how the watch notifications got received quite evenly from all three ClickHouse nodes:



```
┌─n─┬─total_requests─┬─multi_requests─┬─watch_notifications─┐
│ 1 │           5741 │           3671 │                 278 │
│ 2 │           5593 │           3685 │                 269 │
│ 3 │           6371 │           4286 │                 275 │
└───┴────────────────┴────────────────┴─────────────────────┘

```

The following two charts visualize these Keeper requests [during](https://gist.github.com/tom-clickhouse/3e3cafe83ed468b6d312ef5461dc3d03) the data\-loading process:
![Keeper-02.png](/uploads/Keeper_02_0e4fabf14d.png)
We can see that \~70% of the Keeper requests are multi\-write transactions.


Note that the amount of Keeper requests can vary based on the ClickHouse cluster size, ingest settings, and data size. We briefly demonstrate how these three factors influence the number of generated Keeper requests.


#### ClickHouse cluster size [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#clickhouse-cluster-size)


If we load the data with 10 instead of 3 servers in parallel, we ingest the data more than 3 times faster (with the [SharedMergeTree](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates)):



```
0 rows in set. Elapsed: 33.634 sec. Processed 4.64 billion rows, 40.58 GB (138.01 million rows/s., 1.21 GB/s.)
Peak memory usage: 57.09 GiB.

```

The higher number of servers generates more than 3 times the amount of Keeper requests:



```
total_requests:      60925
multi_requests:      41767
watch_notifications: 3468

```

#### Ingest settings [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#ingest-settings)


For our [original](https://gist.github.com/tom-clickhouse/0c1b4d70c4fbebd7a14eb756d1ebc914) data load, run with 3 ClickHouse servers, we configured a max size of \~25 million rows per initial part to speed up ingest speed at the expense of higher memory usage. If, instead, we [run](https://gist.github.com/tom-clickhouse/d67403a4e1663fcbc7f8d8c97ad8df08) the same data load with the [default](https://clickhouse.com/docs/en/operations/settings/settings#settings-max_insert_block_size) value of \~1 million rows per initial part, then the data load is slower but uses \~9 times less main memory per ClickHouse server:



```
0 rows in set. Elapsed: 121.421 sec. Processed 4.64 billion rows, 40.58 GB (38.23 million rows/s., 334.19 MB/s.)
Peak memory usage: 12.02 GiB.

```

And \~4 thousand instead of 240 initial parts [are](https://gist.github.com/tom-clickhouse/6a5ee7bff4ee7e724d0e2c326ab30354) created:



```
┌─parts─────────┬─rows_avg─────┬─size_avg─┬─rows_total───┐
│ 4.24 thousand │ 1.09 million │ 9.20 MiB │ 4.64 billion │
└───────────────┴──────────────┴──────────┴──────────────┘

```

This [causes](https://gist.github.com/tom-clickhouse/05f40f98dbcc6b28be6de3f96668f37b) a higher number of part merges:



```
┌─merges─┐
│   9094 │
└────────┘

```

And we [get](https://gist.github.com/tom-clickhouse/da9c0faee5f509fb0fae9c4ee5c4d667) a higher number of Keeper requests (\~147k instead of \~17k):



```
total_requests:      147540
multi_requests:      105951
watch_notifications: 7439

```

#### Data size [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#data-size)


Similarly, if we [load](https://gist.github.com/tom-clickhouse/4431d998f24304917976e118c2e95b88) more data (with the default value of \~1 million rows per initial part), e.g. six months from the WikiStat data set, then we get a higher amount of \~24 thousand initial parts for our service:



```
┌─parts──────────┬─rows_avg─────┬─size_avg─┬─rows_total────┐
│ 23.75 thousand │ 1.10 million │ 9.24 MiB │ 26.23 billion │
└────────────────┴──────────────┴──────────┴───────────────┘

```

Which [causes](https://gist.github.com/tom-clickhouse/05f40f98dbcc6b28be6de3f96668f37b) more merges:



```
┌─merges─┐
│  28959 │
└────────┘

```

[Resulting](https://gist.github.com/tom-clickhouse/da9c0faee5f509fb0fae9c4ee5c4d667) in \~680k Keeper requests:



```
total_requests:      680996
multi_requests:      474093
watch_notifications: 32779

```

## Benchmarking Keeper [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#benchmarking-keeper)


We developed a benchmark suite coined [keeper\-bench\-suite](https://github.com/ClickHouse/keeper-bench-suite) for benchmarking the typical ClickHouse interactions with Keeper explored above. For this, keeper\-bench\-suite allows simulating the parallel Keeper workload from a ClickHouse cluster consisting of `N` (e.g. 3\) servers:
![Keeper-03.png](/uploads/Keeper_03_53c9cae6a1.png)
We can simulate and benchmark the typical parallel Keeper traffic from `N` ClickHouse servers. This diagram shows the complete architecture of the Keeper Bench Suite, which allows us to set up easily and benchmark arbitrary Keeper workload scenarios:
![Keeper-04.png](/uploads/Keeper_04_3b57f3a2c4.png)
We are using an AWS [EC2](https://aws.amazon.com/pm/ec2/) instance as a benchmark server for executing a [Python script](https://github.com/ClickHouse/keeper-bench-suite/blob/main/benchmark.py) which
`① sets up and starts a 3-node Keeper [cluster](https://zookeeper.apache.org/doc/current/zookeeperStarted.html#sc_RunningReplicatedZooKeeper) by spinning up 3 appropriate (e.g., [m6a.4xlarge](https://aws.amazon.com/ec2/instance-types/m6a/)) EC2 instances, each running one Keeper [docker](https://en.wikipedia.org/wiki/Docker_(software)) container and two containers with [cAdvisor](https://github.com/google/cadvisor) and [Redis](https://redis.io/) (required by cAdvisor) for monitoring the resource usage of the local Keeper container  
  

② starts keeper-bench with a preconfigured workload configurations  
  

③ scrapes the [Prometheus](https://prometheus.io/) endpoints of each cAdvisor and Keeper every 1 second  
  

④ writes the scraped metrics including timestamps into two [tables](https://github.com/ClickHouse/keeper-bench-suite?tab=readme-ov-file#getting-started) in a ClickHouse Cloud service which is the basis for conveniently analyzing the metrics via SQL queries, and [Grafana](https://grafana.com/) dashboards`


Note that both [ClickHouse Keeper](https://github.com/ClickHouse/ClickHouse/pull/43087) and [ZooKeeper](https://zookeeper.apache.org/doc/r3.8.2/zookeeperMonitor.html) directly provide Prometheus endpoints. Currently, these endpoints only have a very small overlap and generally give quite different metrics, which makes it hard to compare them, especially in terms of memory and CPU usage. Therefore, we opted for additional cAdvisor\-based basic container metrics. Plus, running Keeper in a docker container allows us to easily change the number of CPU cores and size of RAM provided to Keeper.


### Configuration parameters [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#configuration-parameters)


#### Size of Keeper [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#size-of-keeper)


We run benchmarks with different docker container sizes for both ClickHouse Keeper and ZooKeeper. E.g. 1 CPU core \+ 1 GB RAM, 3 CPU cores \+ 1 GB RAM, 6 CPU cores \+ 6 GB RAM.


#### Number of clients and requests [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#number-of-clients-and-requests)


For each of the Keeper sizes, we simulate (with the [concurrency](https://github.com/ClickHouse/ClickHouse/tree/master/programs/keeper-bench#general-settings) setting of keeper\-bench) different numbers of clients (e.g., ClickHouse servers) sending requests in parallel to Keeper: E.g. 3, 10, 100, 500, 1000\.


From each of these simulated clients, to simulate both short and long\-running Keeper sessions, we send (with the [iterations](https://github.com/ClickHouse/ClickHouse/tree/master/programs/keeper-bench#general-settings) setting of keeper\-bench) a total number between 10 thousand and \~10 million requests to Keeper. This aims to test whether memory usage of either component changes over time.


#### Workload [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#workload)


We simulated a typical ClickHouse workload containing \~1/3 write and delete operations and \~2/3 reads. This reflects a scenario where some data is ingested, merged, and then queried. It is easily possible to define and benchmark other workloads.


### Measured metrics [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#measured-metrics)


#### Prometheus endpoints [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#prometheus-endpoints)


We use the Prometheus endpoint of cAdvisor for measuring


- Main memory usage ([container\_memory\_working\_set\_bytes](https://github.com/google/cadvisor/blob/release-v0.47/docs/storage/prometheus.md?plain=1#L67))
- CPU usage ([container\_cpu\_usage\_seconds\_total](https://github.com/google/cadvisor/blob/release-v0.47/docs/storage/prometheus.md?plain=1#L30))


We use the Prometheus endpoints of [ClickHouse Keeper](https://github.com/ClickHouse/ClickHouse/pull/43087) and [ZooKeeper](https://zookeeper.apache.org/doc/r3.8.2/zookeeperMonitor.html) for measuring additional (all available) Keeper Prometheus endpoint metric values. E.g. for ZooKeeper, many JVM\-specific metrics (heap size and usage, garbage collection, etc.).


#### Runtime [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#runtime)


We also measure the runtime for Keeper processing all requests based on the minimum and maximum timestamps from each run.


### Results [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#results)


We used the keeper\-bench\-suite to compare the resource consumption and runtime of ClickHouse Keeper and ZooKeeper for our workload. We ran each benchmark configuration 10 times and stored the results in [two tables](https://github.com/ClickHouse/examples/tree/main/keeper-bench-suite#getting-started) in a ClickHouse Cloud service. We used a [SQL query](https://gist.github.com/tom-clickhouse/d156a83202b1b31ab34adc09c9167192) for generating three tabular result tables:


- [mean](https://gist.github.com/tom-clickhouse/e6edb87becb2b03939db06a0c1b0ff13)
- [95th percentiles](https://gist.github.com/tom-clickhouse/e3d9cfae1903f2e457131fa5820a08ea)
- [99th percentiles](https://gist.github.com/tom-clickhouse/a4c2ffbc85463ac9fac64571599365ae)


The columns of these results are described [here](https://gist.github.com/tom-clickhouse/2d3f292ee0aac762251626c7c3156966).


We used `ClickHouse Keeper 23.5` and `ZooKeeper 3.8.` (with bundled `OpenJDK 11`) for all runs.
Note that we don’t print the three tabular results here, as each table contains 216 rows. You can inspect the results by following the links above.


### Example Results [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#example-results)


Here, we present two charts, where we [filtered](https://gist.github.com/tom-clickhouse/0cb1d340efeeea123f592de2e9d6bc3c) the 99th percentile results for rows where both Keeper versions run with 3 CPU cores and 2 GB of RAM, processing the same request sizes sent from 3 simulated clients (ClickHouse servers) in parallel. The tabular result for these visualizations is [here](https://gist.github.com/tom-clickhouse/f7f165ad612ba81088817226e33a431d).


#### Memory usage [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#memory-usage)


![Keeper-05.png](/uploads/Keeper_05_ef049cc5e4.png)
We can see that for our simulated workload, ClickHouse Keeper consistently uses a lot less main memory than ZooKeeper for the same number of processed requests. E.g. for the benchmark run ③ processing 6\.4 million requests sent by 3 simulated ClickHouse servers in parallel, ClickHouse Keeper uses \~46 times less main memory than ZooKeeper in run ④.
For ZooKeeper, we used a 1GiB JVM heap size configuration (`JVMFLAGS: -Xmx1024m -Xms1024m`) for all main runs (①, ②, ③), meaning that the committed JVM memory (reserved heap and non\-heap memory is guaranteed to be available for use by the Java virtual machine) size is \~1GiB for these runs (see the transparent gray bars in the chart above for how much is used). In addition to the docker container memory usage (blue bars), we also measured the amount of (heap and non\-heap) JVM memory actually used within the committed JVM memory (pink bars). There is some slight container memory [overhead](https://stackoverflow.com/a/53624438) (difference of blue and pink bars) of running the JVM itself. However, the actual used JVM memory is still consistently significantly larger than the overall container memory usage of ClickHouse Keeper.


Furthermore, we can see that ZooKeeper uses the complete 1 GiB JVM heap size for run ③. We did an additional run ④ with an increased JVM heap size of 2 GiB for ZooKeeper, resulting in ZooKeeper using 1\.56 GiB of its 2 GiB JVM heap, with an improved runtime matching the runtime of ClickHouse Keeper’s run ③. We present runtimes for all runs above in the next chart.


We can see in the tabular result that (major) garbage collection takes place a few times during the ZooKeeper runs.


#### Runtime and CPU usage [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#runtime-and-cpu-usage)


The following chart visualizes runtimes and CPU usages for the runs discussed in the previous chart (the circled numbers are aligned in both charts):
![Keeper-06.png](/uploads/Keeper_06_04cf699a40.png)
ClickHouse Keeper’s runtimes closely match ZooKeeper’s runtimes. Despite using significantly less main memory (see the previous chart) and CPU.


## Scaling Keeper [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#scaling-keeper)


We [observed](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#observing-keeper) that ClickHouse Cloud often uses multi\-write transactions in interactions with Keeper. We zoom in a bit deeper into ClickHouse Cloud’s interactions with Keeper to sketch two main scenarios for such Keeper transactions used by ClickHouse servers.


### Automatic insert deduplication [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#automatic-insert-deduplication)


![Keeper-08.png](/uploads/Keeper_08_3b3e4bbd75.png)
In the scenario sketched above, server\-2 ① processes data inserted into a table [block](https://clickhouse.com/docs/en/development/architecture#block)\-[wise](https://clickhouse.com/docs/en/operations/settings/settings#max_insert_block_size). For the current block, server\-2 ② writes the data into a new data part in object storage, and ③ [uses](https://github.com/ClickHouse/ClickHouse/blob/776f232ec0b1b19b91d741f8fb76a437548b86c2/src/Storages/MergeTree/EphemeralLockInZooKeeper.cpp#L56) a Keeper multi\-write [transaction](https://zookeeper.apache.org/doc/r3.4.3/api/org/apache/zookeeper/ZooKeeper.html#multi(java.lang.Iterable)) for storing metadata about the new part in Keeper, e.g., where the blobs corresponding to part files reside in object storage. Before storing this metadata, the transaction first tries to store the hash sum of the block processed in step ① in a `deduplication log` znode in Keeper. If the same hash sum value [already](https://github.com/ClickHouse/ClickHouse/blob/776f232ec0b1b19b91d741f8fb76a437548b86c2/src/Storages/MergeTree/EphemeralLockInZooKeeper.cpp#L49) exists in the deduplication log, then the whole transaction [fails](https://github.com/ClickHouse/ClickHouse/blob/776f232ec0b1b19b91d741f8fb76a437548b86c2/src/Storages/MergeTree/EphemeralLockInZooKeeper.cpp#L61) (is rolled back). Additionally, the data part from step ② is deleted because the data contained in that part was already inserted in the past. This automatic insert [deduplication](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse#5-deduplication-at-insert-time) makes ClickHouse inserts [idempotent](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#inserts-are-idempotent) and, therefore, failure\-tolerant, allowing clients to retry inserts without risking data duplication. On success, the transaction triggers child [watches](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkWatches), and ④ all Clickhouse servers [subscribed](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#sharedmergetree-for-cloud-native-data-processing) to events for the part\-metadata znodes are automatically notified by Keeper about new entries. This causes them to fetch metadata updates from Keeper into their local metadata caches.
### Assigning part merges to servers [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#assigning-part-merges-to-servers)


![Keeper-09.png](/uploads/Keeper_09_bef5e28102.png)
When server\-2 decides to merge some parts into a larger part, then the server ① uses a Keeper transaction for marking the to\-be\-merged parts as locked (to prevent other servers from merging them). Next, server\-2 ② merges the parts into a new larger part, and ③ uses another Keeper transaction for storing metadata about the new part, which triggers watches ④ notifying all other servers about the new metadata entries.
Note that the above scenarios can only work correctly if such Keeper transactions are executed by Keeper atomically and sequentially. Otherwise, two ClickHouse servers sending the same data in parallel at the same time could potentially both not find the data’s hash sum in the deduplication log resulting in data duplication in object storage. Or multiple servers would merge the same parts. To prevent this, the ClickHouse servers rely on Keeper’s all\-or\-nothing multi\-write transactions plus its linearizable writes guarantee.


### Linearizability vs multi\-core processing [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#linearizability-vs-multi-core-processing)


The [consensus algorithms](https://betterprogramming.pub/demystifying-consensus-algorithms-and-their-implementations-c52f8aca3020) in ZooKeeper and ClickHouse Keeper, [ZAB](https://zookeeper.apache.org/doc/r3.4.13/zookeeperInternals.html#sc_atomicBroadcast), and [Raft](https://raft.github.io/), respectively, both ensure that multiple distributed servers can reliably agree on the same information. e.g. which parts are allowed to be merged in the example above.


ZAB is a dedicated consensus mechanism for ZooKeeper and has been in development [since](https://dl.acm.org/doi/10.1145/1529974.1529978) at least 2008\.


We chose Raft as our consensus mechanism because of its simple and [easy\-to\-understand](https://raft.github.io/raft.pdf) algorithm and the availability of a lightweight and easy\-to\-integrate [C\+\+ library](https://tech.ebayinc.com/engineering/nuraft-a-lightweight-c-raft-core/) when we started the Keeper project in 2021\.


However, all consensus algorithms are isomorphic to each other. For [linearizable](https://en.wikipedia.org/wiki/Linearizability) writes, (dependent) transitions and the write operations within the transaction must be processed in strict order, one at a time, regardless of which consensus algorithm is used. Suppose ClickHouse servers are sending transactions in parallel to Keeper, and these transactions are dependent because they write to the same znodes (e.g., the `deduplication log` in our example scenario at the beginning of this section). In that case, Keeper can guarantee and implement linearizability only by executing such transactions and their operations strictly sequentially:
![Keeper-10.png](/uploads/Keeper_10_aa840f2251.png)
For this, ZooKeeper implements write request processing using a single\-threaded [request processor](https://github.com/apache/zookeeper/blob/master/zookeeper-server/src/main/java/org/apache/zookeeper/server/SyncRequestProcessor.java), whereas Keeper’s NuRaft implementation uses a single\-threaded [global queue](https://github.com/eBay/NuRaft/blob/v2.0/src/global_mgr.cxx#L252).


Generally, linearizability makes it hard to scale write processing speed vertically (more CPU cores) or horizontally (more servers). It would be possible to analyze and identify independent transactions and run them in parallel, but currently, neither ZooKeeper nor ClickHouse Keeper implements this. This chart (where we filtered the 99th percentile results) highlights this:
![Keeper-07.png](/uploads/Keeper_07_2f3bf2e688.png)
Both ZooKeeper and ClickHouse Keeper are running with 1, 3, and 6 CPU cores and processing 1\.28 million total requests sent in parallel from 500 clients.


The performance of (non\-linearizable) read requests and auxiliary tasks (managing network requests, batching data, etc.) can be scaled theoretically with the number of CPU cores with both ZAB and Raft. Our benchmark results generally show that ZooKeeper is currently doing this better than Clickhouse Keeper, although we are consistently improving our performance ([three](https://github.com/ClickHouse/ClickHouse/pull/43686) [recent](https://github.com/ClickHouse/ClickHouse/pull/47978) [examples](https://github.com/ClickHouse/ClickHouse/pull/53049)).


### Next for Keeper: Multi\-group Raft for Keeper, and more [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#next-for-keeper-multi-group-raft-for-keeper-and-more)


Looking forward, we see the need to extend Keeper to better support the scenarios we described above. So, we are taking a big step with this project – introducing a multi\-group Raft protocol for Keeper.


Because, as explained above, scaling non\-partitioned (non\-sharded) linearizability is impossible, we will focus on [Multi\-group Raft](https://github.com/ClickHouse/ClickHouse/issues/54172) where we [partition](https://tikv.org/deep-dive/scalability/multi-raft/) the data stored in Keeper. This allows more transactions to be independent (working over separate partitions) from each other. By using a separate Raft instance inside the same server for each partition, Keeper automatically executes independent transactions in parallel:
![Keeper-11.png](/uploads/Keeper_11_72b63a9e55.png)
With multi\-Raft, Keeper will be able to enable workloads with much higher parallel read/write requirements, such as for instance, very large ClickHouse clusters with 100s of nodes.


## Join the Keeper community! [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#join-the-keeper-community)


Sounds exciting? Then, we invite you to join the Keeper community.


- [This](https://clickhouse.com/docs/en/guides/sre/keeper/clickhouse-keeper) is how you use Keeper with ClickHouse
- To become a user of Keeper outside of ClickHouse \- check out [this](/clickhouse/keeper) page when to use it or not
- [This](https://clickhouse.com/slack) is where you post questions; you can follow us on [X](https://twitter.com/ClickHouseDB) and [join](https://github.com/ClickHouse/ClickHouse#upcoming-events) our meetups and events.


We welcome contributions to the Keeper codebase. See our roadmap [here](https://github.com/ClickHouse/ClickHouse/labels/comp-keeper), and see our contributor guidelines [here](https://github.com/ClickHouse/ClickHouse/blob/master/CONTRIBUTING.md).


## Summary [\#](/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp#summary)


In this blog post, we described the features and advantages of ClickHouse Keeper \- a resource\-efficient open\-source drop\-in replacement for ZooKeeper. We explored our own usage of it in ClickHouse Cloud and, based on this, presented a benchmark suite and results highlighting that ClickHouse Keeper consistently uses significantly fewer hardware resources than ZooKeeper with comparable performance numbers. We also shared our roadmap and ways you can get involved. We invite you to collaborate!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
