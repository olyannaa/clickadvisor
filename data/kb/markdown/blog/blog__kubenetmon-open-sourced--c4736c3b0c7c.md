# Open sourcing kubenetmon: how we monitor data transfer in ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Open sourcing kubenetmon: how we monitor data transfer in ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U06_DLSR_8_K6_H_4bfdbed89520_512_cbff481702.jpg&w=96&q=75)[Ilya Andreev](/authors/ilya-andreev)Jan 30, 2025 · 26 minutes readIn this blogpost, we announce open sourcing kubenetmon: a tool we use to monitor data transfer in ClickHouse Cloud. You can jump to the project on GitHub here: <https://github.com/ClickHouse/kubenetmon>.


The cloud unlocks many benefits for teams looking to build modern software products: ready\-made infrastructure components, infinite scalability, high cost efficiency, and others. When thinking about cloud costs, many organizations are prudent about their compute and storage usage planning; however, the category that frequently takes third place among cloud bill line items is just as frequently entirely neglected when forecasting cloud costs – the network. This happens, in part, due to how difficult the network is to understand and to meter.


We faced this problem at ClickHouse Cloud too. We run on all 3 major cloud providers – AWS, GCP, and Azure. We operate in many regions for each provider, pushing the number of regions we have infrastructure in into dozens, and that’s excluding our staging and development environments. Each region is typically home to multiple Kubernetes clusters.


Understanding network behavior of such a system is an arduous challenge. The complexity of the data transfer charges associated with this network architecture rises further still.


When it comes to data transfer, cloud providers typically charge you for:


- NAT Gateways;
- Load Balancers;
- Cross\-Availability Zone traffic;
- Egress, where the cost basis depends on which region you egress from and where you egress into;
- Ingress, where the cost basis also depends on which region you ingress into and where the remote is.


We set out to untangle this complexity, and this blog post is going to tell you how.


## The goals [\#](/blog/kubenetmon-open-sourced#the-goals)


When scoping out what kind of visibility into data transfer we wanted to achieve, we identified 3 individual goals:


1. **Forensics:** We wanted to have records of individual L3/L4 connections opened in our infrastructure presented as time series over the duration of the connection. That way, we would be able to understand how throughput fluctuates even for individual long\-running connections. For example, rather than just knowing that there was a connection that started at a particular time and lasted for a particular duration with a particular data transfer volume, we would want to know the rate of data transfer for said connection at a higher granularity, let’s say with per\-minute bandwidth records. With this information, we would be able to answer questions such as *what was the behavior of this connection over time?*
2. **Attribution:** Our infrastructure is multi\-tenant, meaning we run multiple customers’ workloads on the same hardware. This means that to understand our data transfer, we need to see what workloads the connection belongs to, as well as which Availability Zones and pods those workloads are running in. When one of the endpoints of the connection is outside of our infrastructure, we want to know about it as much as possible – whether it is in the same cloud provider and region, and so on. With this information, we would be able to answer questions such as *what workload opened this connection and what was its remote endpoint?*
3. **Metering:** We wanted to account for particularly cost\-sensitive data transfer use cases (such as costly egress to public Internet) by individual workloads. This meant having a long\-retention infrastructure that aggregates cumulative usage of data transfer by workload and by “business” category of the data transfer. With this information, we would be able to answer questions such as *for this particular data transfer spend category, how did we trend over time and what internal or customer usage changes can we attribute trend fluctuations to?*


While there is a lot more you can invent and build around network monitoring, we felt that these specific goals encapsulated well the things *we* specifically were struggling with. For example, while it could in some situations be valuable to see details of application\-level connections and requests (such as DNS, or HTTP), or have an idea of the levels of TCP retransmissions associated with particular connections, gathering such information was out of scope. We focused specifically on L3/L4 longitudinal connection records, workload connection attribution, and aggregate data transfer metering.


![Open Sourcing Kubenetmon Diagram Jan 2025 (1).png](/uploads/Open_Sourcing_Kubenetmon_Diagram_Jan_2025_1_e74ca6cdf3.png)
*Schematic of the main traffic paths that can happen in our cloud. It doesn’t depict East\-West traffic between ClickHouse Server replicas, Servers and Keepers, as well as other workloads we run.*


## Options we considered [\#](/blog/kubenetmon-open-sourced#options-we-considered)


We were confident that our needs weren’t unique to us, so we dove into researching available solutions with respect to gathering this data. Nothing we described above sounded like rocket science, so we naively expected to find many existing solutions that would meet our needs. To our surprise, none of the options we evaluated fit our bill!


We would like to go through the list of options we considered and our thought process when deciding whether to use them.


### Cilium CNI [\#](/blog/kubenetmon-open-sourced#cilium-cni)


We use Cilium in ClickHouse Cloud, which is well\-known to have not only powerful networking capabilities, but also, through Cilium Hubble, advanced observability features. However, it turned out that with Cilium Hubble, you generally have either the ability to get volumetric data with little context, or non\-volumetric data with a lot of context. For example, Cilium’s metrics such as *forward\_bytes* and *forward\_count* would give us the volumetric information that we want, but they lack information about connection endpoints; Cilium separately has very granular information about connections and their endpoints, but the metrics with such labels are not volumetric – they allow you to meter *flow* counts, but the definition of a *flow* in Cilium parlance has nothing to do with connection bandwidth (a *flow* count is incremented for a given connection tuple whenever a new TCP flag is seen, and every N seconds).


Needless to say, many people, including ourselves, are surprised to learn this. The underlying technical constraints that make solving this problem challenging on the Cilium side are very interesting, and we recommend reading up on the comments and issues linked here in the Cilium GitHub project: <https://github.com/cilium/cilium/issues/32193>.


### CSP flow logs [\#](/blog/kubenetmon-open-sourced#csp-flow-logs)


Of course, cloud providers already have the capability to track data transfer and give you insights about it. However, these features can become expensive in and of themselves. Additionally, their capabilities differ across cloud providers, and in some cases they would not provide us with the data we need. For example, in AWS and Azure, we found it difficult to annotate flow logs with custom Kubernetes workload labels. Finally, any postprocessing architecture we would have for our *metering* goal would have to work differently with each individual provider rather than work with a uniform data collection system and schema.


### Cost\-metering solutions [\#](/blog/kubenetmon-open-sourced#cost-metering-solutions)


There are also a lot of projects and businesses out there that help companies monitor and understand their cloud spend, including data transfer spend. Some of these solutions have open\-core components, such as OpenCost. When evaluating these, we found that they are very good at focusing on the FinOps part of the task at hand, but their data representation gives you limited insights when it comes to understanding individual connections and their behavior over time (the *forensics* part of our goalset).


### Do it in ClickHouse! [\#](/blog/kubenetmon-open-sourced#do-it-in-clickhouse)


Of course, we also considered implementing simple user\-space functionality in the ClickHouse application itself to track which connections are open to and from ClickHouse. ClickHouse already has a plethora of [system tables](https://clickhouse.com/docs/en/operations/system-tables) where all sorts of useful information is collected; in fact, ClickHouse already collects some network\-related information in system.metrics, e.g. TCPConnection, NetworkReceive, NetworkSend, and so on. What’s even more fantastic is that in ClickHouse Cloud, we already have a system that continuously scrapes and exports anonymized system table data from customer instances, which we call SysEx, so the export of any data transfer records would work out of the box.


There are challenges with this approach, however. First, by definition we would not be able to see any traffic between non\-ClickHouse workloads, of which we have more and more. Secondly, systematically tracking all network on an L3/L4 level in a userspace application is complex and is prone to introduce overly verbose code, since (inbound and outbound) request handling is typically implemented at a higher level than that and is spread throughout the codebase. Finally, this approach leaves no elegant place for the *attribution* part of our task to be implemented, which definitely does not belong in the ClickHouse codebase.


### Non\-Cilium eBPF\-based solutions [\#](/blog/kubenetmon-open-sourced#non-cilium-ebpf-based-solutions)


The last family of options we considered were eBPF\-based tools outside of Cilium. We evaluated projects like [Retina](https://github.com/microsoft/retina), which is tailor\-made for network observability in the cloud and is in fact used under the hood in advanced Azure products. Thanks to eBPF, such solutions generally have very few limitations with regards to what data they have access to, and since they are designed for the very purpose of cloud network observability, they already do the powerful work of annotating connection information with workload labels, just as we want. Repurposing the open source components of the Datadog system\-probe agent would fall under this category, too.


Unfortunately, we ultimately decided not to go down this path out of concerns with mixing eBPF workloads from different vendors where we have limited visibility into how their interoperability is tested (as a reminder, we already run Cilium, which is based on eBPF, and rely on dataplane v2 in GKE, which is also based around Cilium). We felt that the potential blast radius of two such systems developed by external teams misinteracting with each other is too wide, and we would prefer to limit our eBPF exposure in the data transfer path to just Cilium workloads. We felt that the appropriate test and integration harness required to start using this approach would require more work than solving the problem at hand by itself.


Another limitation we would have had to deal with when using some of these solutions is Prometheus, which is the go\-to method of recording observations in the ecosystem (and for a good reason!). However, with a high level of information associated with connections comes a high level of cardinality, which Prometheus makes notoriously expensive to deal with. Ideally, we wanted to avoid relying on a metrics model where possible.


## Our solution [\#](/blog/kubenetmon-open-sourced#our-solution)


After evaluating all of the options above, we decided to implement something in\-house, but we wanted to keep it very simple. We needed to come up with answers to three questions:


1. How do we collect connection data?
2. How do we attribute connections to endpoints?
3. How do we store these connection records?


Here’s what we came up with.


### How do we collect connection data? [\#](/blog/kubenetmon-open-sourced#how-do-we-collect-connection-data)


Enter conntrack! Unsurprisingly, the standard Linux networking stack tracks the state of connections handled by the system. This information is conveniently exposed to users through the well\-named conntrack table. conntrack is a classic part of Linux's netfilter framework and has very good access APIs, for which there are mature libraries in Go and Rust.


What do entries in conntrack (again, this is just a connection tracking table) look like? Here is an example:



```
# conntrack -L
tcp      6 35 TIME_WAIT src=10.1.1.42 dst=10.1.2.228 sport=41442 dport=5555 src=10.1.2.228 dst=10.1.1.42 sport=5555 dport=41442 [ASSURED] mark=0 use=1
tcp      6 431999 ESTABLISHED src=10.1.0.27 dst=10.1.131.55 sport=37670 dport=10249 src=10.1.131.55 dst=10.1.0.27 sport=10249 dport=37670 [ASSURED] mark=0 use=1

```

We can see the connection protocol, endpoint IPs and ports, the current connection state, and some other things. This doesn’t tell us anything about the data transfer volume, though. However, as soon as we enable the “accounting” feature in netfilter, we start getting byte and packet counts for every connection in each direction:



```
# echo "1" > /proc/sys/net/netfilter/nf_conntrack_acct
# conntrack -L
tcp      6 35 TIME_WAIT src=10.1.1.42 dst=10.1.2.228 sport=41442 dport=5555  packets=334368 bytes=106591692 src=10.1.2.228 dst=10.1.1.42 sport=5555 dport=41442 packets=280371 bytes=692287110 [ASSURED] mark=0 use=1
tcp      6 431999 ESTABLISHED src=10.1.0.27 dst=10.1.131.55 sport=37670 dport=10249 packets=20 bytes=21564 src=10.1.131.55 dst=10.1.0.27 sport=10249 dport=37670 packets=11 bytes=2011 [ASSURED] mark=0 use=1

```

It is well\-documented that conntrack has its dangers, in particular when the table becomes overfilled – see, for example, these blogposts by [Cloudflare](https://blog.cloudflare.com/conntrack-tales-one-thousand-and-one-flows/) and [Tigera](https://www.tigera.io/blog/when-linux-conntrack-is-no-longer-your-friend/). This fact is important to keep in mind, but it was not decisive for planning this project, since we had been using conntrack before and it was not for this project that it was being enabled. Additionally, our infrastructure is spread across multiple Kubernetes clusters serving different purposes, and the frontline “proxy” clusters handling the highest concentration of connections per machine are *not* the ones we would be monitoring traffic in – we are most curious about monitoring data transfer (and consequently introducing this new dependency on conntrack) in the clusters running customer workloads, which are distributed enough that in machines on those clusters the conntrack table is only ever barely filled up relative to its allowed size.


The additional [work](https://elixir.bootlin.com/linux/v6.12.1/source/net/netfilter/nf_conntrack_core.c#L953-L959) done by the kernel to count bytes and packets is minimal and was not a performance concern for us. The counters themselves are 8\-byte long, which is more than enough.


In summary, the idea we came to was to enable the accounting feature in the already enabled conntrack in our clusters running customer workloads, then scrape this table with certain periodicity to start monitoring connections; it could so happen that short\-lived connections would go unnoticed by our “scraper” (same goes to the “tail ends” of connections that have just closed) – while we can configure the amount of time residual connection state is kept in the table for after the connection is closed, we didn’t go to such lengths since information lost this way is minimal. When we scrape conntrack, we ask the kernel to atomically reset the counters to zero (which is safe since we know no other systems rely on this information) using a special [setting](https://pkg.go.dev/github.com/ti-mo/conntrack#DumpOptions) in the conntrack API; this lets us assume that the values we scrape are not cumulative and reflect the throughput in the time interval between scrapes.


While the cloud is a fascinating abstraction, at the end of the day you can still rely on the lower\-level Linux primitives!


### How do we attribute connections to endpoints? [\#](/blog/kubenetmon-open-sourced#how-do-we-attribute-connections-to-endpoints)


Let’s assume we now have a daemon that can scrape conntrack entries every few seconds. What’s next? We have endpoint IPs, ports, byte and packet counts, and that’s about it. It’s time to solve our *attribution* problem.


For the next step, we implement labeling logic in our daemon, which at this point we have named *kubenetmon*. In principle, the task is very simple: when we scrape conntrack, we need to ask the Kubernetes API which pod a particular IP is assigned to, pull information that we want about said pod, and call it a day. In fact, it did turn out to be simple – we quickly implemented this proof of concept, and it worked. As you can see in the [open source project](https://github.com/ClickHouse/kubenetmon/tree/main), we had to do some extra work around identifying the connection direction and working around NAT, but overall things worked as we expected. Finally, we also implemented labeling related to endpoints that live outside of our clusters – for example, we track ranges of AWS services, allowing us to identify when a remote belongs to AWS, and if it does, then what region it is running in. This made it possible for us to distinguish inter\-region and intra\-region traffic, for instance.


This proof of concept wasn’t performing well, though. It consumed a lot of RAM, and even worse, put a high load on the Kubernetes API. To address the latter, we chose to use Kubernetes [informers](https://pkg.go.dev/k8s.io/client-go/informers) instead of polling the Kubernetes API every time we needed some information – the informer approach allows us to watch Kubernetes events to build an internal map of the cluster state, so that whenever we need to label a connection, we can use our in\-memory knowledge about the cluster rather than reach out to the API.


Yet we were still not done with the RAM issue. In fact, it had only gotten worse with the migration to the informer model, since we now kept more state in\-memory (duh). It became clear that we could not have a daemon that runs on every node keep track of the entire (rather large) cluster’s state.


At this point, we split *kubenetmon* into two components: *kubenetmon\-agent* and *kubenetmon\-server*. kubenetmon\-agent, a daemon, was kept dead simple – it now did nothing but periodically scrape conntrack and forward the records to kubenetmon\-server over gRPC. kubenetmon\-server, in turn, now hosted all the logic related to labeling connection records received from kubenetmon\-agent with Kubernetes metadata. Since kubenetmon\-server was stateless (in that it didn’t have an identity or any information that had to persist across restarts), we could easily scale out kubenetmon\-servers to multiple replicas if we wanted to.


Combined with the use of informers and careful implementation of endpoint labeling logic, this hub\-and\-spoke architecture left us very happy. kubenetmon\-agent’s memory footprint is typically in the 5\-20 MB range.


At this point, all that was left was building out data storage for all the connection information we have collected.


### How do we store these connection records? [\#](/blog/kubenetmon-open-sourced#how-do-we-store-these-connection-records)


Thankfully, we didn’t have to think long to decide on the final destination for our data – ClickHouse. What is fascinating about ClickHouse is how good it is at handling high\-cardinality data. At no point were we concerned that collecting so many connection attributes would ever be too much. We can slice and dice the data we collect in any way we see fit without fear for performance concerns.


We also already have ClickHouse clusters running internally in each environment where we collect metrics, logs, and other information about our systems. We call these clusters LogHouses.


![Open Sourcing Kubenetmon Diagram Jan 2025.png](/uploads/Open_Sourcing_Kubenetmon_Diagram_Jan_2025_a6caa06fdc.png)
*Schematic of kubenetmon. kubenetmon\-agents run as a minimal\-footprint daemonset on every node, scrape conntrack, and forward conntrack data to kubenetmon\-server over gRPC. kubenetmon\-server annotates the observations with Kubernetes cluster metadata, batches them, and pushes them to LogHouse, our internal ClickHouse analytics cluster.*


Here is the definition of the table we created in LogHouse for network data:



```
CREATE TABLE default.network_flows_0
(
    `date` Date CODEC(Delta(2), ZSTD(1)),
    `intervalStartTime` DateTime CODEC(Delta(4), ZSTD(1)),
    `intervalSeconds` UInt16 CODEC(Delta(2), ZSTD(1)),
    `environment` LowCardinality(String) CODEC(ZSTD(1)),
    `proto` LowCardinality(String) CODEC(ZSTD(1)),
    `connectionClass` LowCardinality(String) CODEC(ZSTD(1)),
    `connectionFlags` Map(LowCardinality(String), Bool) CODEC(ZSTD(1)),
    `direction` Enum('out' = 1, 'in' = 2) CODEC(ZSTD(1)),
    `localCloud` LowCardinality(String) CODEC(ZSTD(1)),
    `localRegion` LowCardinality(String) CODEC(ZSTD(1)),
    `localCluster` LowCardinality(String) CODEC(ZSTD(1)),
    `localCell` LowCardinality(String) CODEC(ZSTD(1)),
    `localAvailabilityZone` LowCardinality(String) CODEC(ZSTD(1)),
    `localNode` String CODEC(ZSTD(1)),
    `localInstanceID` String CODEC(ZSTD(1)),
    `localNamespace` LowCardinality(String) CODEC(ZSTD(1)),
    `localPod` String CODEC(ZSTD(1)),
    `localIPv4` IPv4 CODEC(Delta(4), ZSTD(1)),
    `localPort` UInt16 CODEC(Delta(2), ZSTD(1)),
    `localApp` String CODEC(ZSTD(1)),
    `remoteCloud` LowCardinality(String) CODEC(ZSTD(1)),
    `remoteRegion` LowCardinality(String) CODEC(ZSTD(1)),
    `remoteCluster` LowCardinality(String) CODEC(ZSTD(1)),
    `remoteCell` LowCardinality(String) CODEC(ZSTD(1)),
    `remoteAvailabilityZone` LowCardinality(String) CODEC(ZSTD(1)),
    `remoteNode` String CODEC(ZSTD(1)),
    `remoteInstanceID` String CODEC(ZSTD(1)),
    `remoteNamespace` LowCardinality(String) CODEC(ZSTD(1)),
    `remotePod` String CODEC(ZSTD(1)),
    `remoteIPv4` IPv4 CODEC(Delta(4), ZSTD(1)),
    `remotePort` UInt16 CODEC(Delta(2), ZSTD(1)),
    `remoteApp` String CODEC(ZSTD(1)),
    `remoteCloudService` LowCardinality(String) CODEC(ZSTD(1)),
    `bytes` UInt64 CODEC(Delta(8), ZSTD(1)),
    `packets` UInt64 CODEC(Delta(8), ZSTD(1))
)
ENGINE = SummingMergeTree((bytes, packets))
PARTITION BY date
PRIMARY KEY (date, intervalStartTime, direction, proto, localApp, remoteApp, localPod, remotePod)
ORDER BY (date, intervalStartTime, direction, proto, localApp, remoteApp, localPod, remotePod, intervalSeconds, environment, connectionClass, connectionFlags, localCloud, localRegion, localCluster, localCell, localAvailabilityZone, localNode, localInstanceID, localNamespace, localIPv4, localPort, remoteCloud, remoteRegion, remoteCluster, remoteCell, remoteAvailabilityZone, remoteNode, remoteInstanceID, remoteNamespace, remoteIPv4, remotePort, remoteCloudService)
TTL intervalStartTime + toIntervalDay(90)
SETTINGS index_granularity = 8192, ttl_only_drop_parts = 1

```

Now, how can we use this table? For example, to look at the egress direction of connections opened by ClickHouse Server to external destinations, we would do something like this:



```
SELECT intervalStartTime, sum(bytes)
FROM loghouse.network_flows_0
WHERE direction = 'out' AND localApp = 'clickhouse-server' AND connectionClass != 'INTRA_VPC'
GROUP BY intervalStartTime
ORDER BY intervalStartTime DESC

```

When designing this table and implementing our insert logic in the Go kubenetmon\-server service, we found a few things curious and worth highlighting here:


1. **SummingMergeTree family.** Remember we mentioned that for convenience, we reset conntrack counters on each scrape? Suppose we scrape conntrack every 5 seconds (with some jitter) and want to calculate our throughput at a per\-minute resolution. How do we do that? While we could just insert this raw data into a regular MergeTree and massage SELECT queries to work with it, we use a trick available to us with ClickHouse – we create a [SummingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/summingmergetree) table that automatically sums up all bytes and packets across each unique combination of values of all other keys. Since intervalStartTime is always just toStartOfMinute(timestamp), this effectively computes throughput at a per\-minute resolution, just as we wanted. We keep intervalSeconds always set to 60, but if we wanted to lower the resolution, we could change intervalStartTime to toStartOfFiveMinutes(timestamp) and intervalSeconds to 300, for example.
2. **Primary keys and sorting keys.** The keys in the SummingMergeTree can get a little tricky. By default, in ClickHouse, the primary key and the sorting key are the same thing. However, we wanted to retain the ability to add new columns to our table in the future, and in a SummingMergeTree all “grouping” columns (the columns the tree sums *by*) must be in the sorting key; since the sorting key can be mutable while the primary key is always immutable, we define the two independently, allowing us to mutate the sorting key in the future if we ever add new columns we need to sum by. In effect, the sorting key just enumerates all columns except bytes and packets. The primary key is always a prefix of the sorting key. When it comes to the order of the sorting key, it is best practice to specify lower\-cardinality columns first; however, you want your sorting key to actually reflect the usage of particular fields as filters in your queries, so we start with those low\-cardinality columns that we expect to actually use in our queries on this table.
3. **Async inserts, batching and flushing.** In our inserter (kubenetmon\-server), we build in\-memory batches that we flush when they get either too old or too large (fun fact: we initially had a bug where we would not check the age of the batch unless new data came in, meaning that in low\-traffic environments such as certain dev environments we did not flush batches on time). For inserts, we rely on [async inserts](https://clickhouse.com/docs/en/optimize/asynchronous-inserts), allowing the ClickHouse server to batch data even further before flushing it if it sees so fit. We keep wait\_for\_async\_insert set to true (which is the default) to be confident that data isn’t lost. To avoid blocking our inserter, we run a number of inserter “worker” threads in our kubenetmon\-server, each of which competes for work and accumulates its own batch for insertion.
4. **Deduplication.** While nearly impossible, hypothetically our subsequent batches can repeat each other – what if there was a small number of connections that transferred identical amounts of data throughout a couple scrape intervals? Since we round the observation timestamp down to the minute in intervalStartTime with toStartOfMinute(timestamp), such batches could in theory be seen as duplicates by ClickHouse. To avoid deduplication in such (improbable) situations, we set insert\_deduplication\_token on each insert to a randomly generated UUID, convincing ClickHouse server that none of our batches should ever be deduplicated.


## What we have been able to achieve [\#](/blog/kubenetmon-open-sourced#what-we-have-been-able-to-achieve)


This is it when it comes to implementation! In some environments, we record up to a few million connection observations per minute, and while this sounds like a lot, ClickHouse compresses this data very well and can retrieve it in no time. And thanks to the TTL set in our table definition, the 90\-day retention is enforced automatically. Let’s take a look at how much data we store for just one of our regions:



```
SELECT
    formatReadableQuantity(sum(rows)),
    formatReadableSize(sum(data_compressed_bytes)) AS compressed_size,
    formatReadableSize(sum(data_uncompressed_bytes)) AS uncompressed_size,
    sum(data_compressed_bytes) / sum(data_uncompressed_bytes) AS compression_ratio
FROM system.parts
WHERE (database = 'default') AND (`table` = 'network_flows_0') AND (active = 1);

```


```
Row 1:
──────
formatReadab⋯(sum(rows)): 399.05 billion
compressed_size:          2.66 TiB
uncompressed_size:        86.69 TiB
compression_ratio:        0.030629224420511452
1 row in set. Elapsed: 0.116 sec. 

```

Nearly 400 billion rows compressed from 86\.69 TiB down to just over 3% of the original size, or 2\.66 TiB. We can also check how individual columns compress:



```
SELECT
    name,
    data_compressed_bytes / data_uncompressed_bytes AS compression_ratio,
    formatReadableSize(data_uncompressed_bytes) AS uncompressed_size,
    formatReadableSize(data_compressed_bytes) AS compressed_size
FROM system.columns
WHERE (database = 'default') AND (`table` = 'network_flows_0')
ORDER BY compression_ratio ASC;

```


```
┌─name───────────────────┬─uncompressed_size─┬─compressed_size─┬─pct───┐
│ localApp               │ 6.46 TiB          │ 3.53 GiB        │ 0.05  │
│ remoteApp              │ 1013.12 GiB       │ 900.22 MiB      │ 0.09  │
│ proto                  │ 376.23 GiB        │ 334.46 MiB      │ 0.09  │
│ localCloud             │ 376.23 GiB        │ 334.46 MiB      │ 0.09  │
│ remoteCell             │ 376.23 GiB        │ 334.46 MiB      │ 0.09  │
│ remoteClusterType      │ 376.23 GiB        │ 334.46 MiB      │ 0.09  │
│ localRegion            │ 376.23 GiB        │ 334.46 MiB      │ 0.09  │
│ environment            │ 376.23 GiB        │ 334.46 MiB      │ 0.09  │
│ localClusterType       │ 376.23 GiB        │ 334.46 MiB      │ 0.09  │
│ direction              │ 376.23 GiB        │ 338.19 MiB      │ 0.09  │
│ intervalSeconds        │ 751.00 GiB        │ 797.95 MiB      │ 0.10  │
│ date                   │ 751.00 GiB        │ 809.68 MiB      │ 0.11  │
│ intervalStartTime      │ 1.47 TiB          │ 1.63 GiB        │ 0.11  │
│ remoteCloud            │ 376.23 GiB        │ 419.42 MiB      │ 0.11  │
│ remoteRegion           │ 376.23 GiB        │ 470.13 MiB      │ 0.12  │
│ localNamespace         │ 5.51 TiB          │ 10.88 GiB       │ 0.19  │
│ localInstanceID        │ 12.91 TiB         │ 27.82 GiB       │ 0.21  │
│ localPod               │ 11.38 TiB         │ 31.84 GiB       │ 0.27  │
│ localNode              │ 10.63 TiB         │ 36.97 GiB       │ 0.34  │
│ connectionClass        │ 376.23 GiB        │ 1.93 GiB        │ 0.51  │
│ localCell              │ 376.23 GiB        │ 2.59 GiB        │ 0.69  │
│ remoteCloudService     │ 376.23 GiB        │ 2.90 GiB        │ 0.77  │
│ connectionFlags        │ 15.58 TiB         │ 124.83 GiB      │ 0.78  │
│ localAvailabilityZone  │ 376.23 GiB        │ 5.26 GiB        │ 1.40  │
│ localIPv4              │ 1.47 TiB          │ 21.26 GiB       │ 1.42  │
│ remoteAvailabilityZone │ 376.23 GiB        │ 7.69 GiB        │ 2.04  │
│ remoteNamespace        │ 920.65 GiB        │ 19.25 GiB       │ 2.09  │
│ remoteNode             │ 1.51 TiB          │ 38.91 GiB       │ 2.52  │
│ remoteInstanceID       │ 1.45 TiB          │ 39.86 GiB       │ 2.68  │
│ remotePod              │ 1.61 TiB          │ 48.38 GiB       │ 2.93  │
│ remotePort             │ 751.00 GiB        │ 68.73 GiB       │ 9.15  │
│ packets                │ 2.93 TiB          │ 607.89 GiB      │ 20.24 │
│ localPort              │ 751.00 GiB        │ 189.61 GiB      │ 25.25 │
│ remoteIPv4             │ 1.47 TiB          │ 429.64 GiB      │ 28.60 │
│ bytes                  │ 2.93 TiB          │ 1.01 TiB        │ 34.29 │
└────────────────────────┴───────────────────┴─────────────────┴───────┘

35 rows in set. Elapsed: 0.004 sec.

```

Very nice, although we could probably squeeze out even better performance if we wanted to. ;)


With this data, we have been able to track down pathological cases where we ourselves were periodically running expensive cross\-regional downloads from S3, identify most active cross\-Availability Zone talkers in our infrastructure, and estimate the right guaranteed bandwidth required for our workloads. We also found setups where multi\-terabyte backups were made from ClickHouse into other clouds multiple times a day, costing a lot of money on the egress path, and were able to dig into the cost of supporting services with “proxy” tables (such as with the [MySQL Engine](https://clickhouse.com/docs/en/engines/table-engines/integrations/mysql)) that pull data from remote servers.


## Open sourcing kubenetmon [\#](/blog/kubenetmon-open-sourced#open-sourcing-kubenetmon)


This has been a great project to work on, and given how surprised we were to not find a tool that would have helped us with completing it faster, we decided to open source the result of our work – kubenetmon. You can now find the kubenetmon project publicly available on our GitHub: <https://github.com/ClickHouse/kubenetmon>, with instructions on how to give it a spin. You are very welcome to play around with it, use it for your use cases, or to draw inspiration from it!


Please reach to [ilya.andreev@clickhouse.com](mailto:ilya.andreev@clickhouse.com) or open an issue in the GitHub project if you have any questions or feedback.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
