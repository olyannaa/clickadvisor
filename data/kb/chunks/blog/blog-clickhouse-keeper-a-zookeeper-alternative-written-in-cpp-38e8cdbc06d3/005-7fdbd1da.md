---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-keeper-a-zookeeper-alternative-written-in-c-clickhouse
ch_version_introduced: '4.11'
last_updated: '2026-09-07'
chunk_index: 5
total_chunks_in_doc: 14
---

billion │ 5└───┴───────┴──────────────┘ ``` Copy command ### ③ Part merges \# During the data loading, in the background, ClickHouse [executed](https://gist.github.com/tom-clickhouse/05f40f98dbcc6b28be6de3f96668f37b) 1706 part [merges](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#data-needs-to-be-batched-for-optimal-performance), respectively: ``` 1┌─merges─┐ 2│ 1706 │ 3└────────┘ ``` Copy command ### ④ Keeper interactions \#

ClickHouse Cloud completely [separates](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#clickhouse-cloud-enters-the-stage) the storage of data and metadata from the servers. All data parts [are](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#shared-object-storage-for-data-availability) stored in shared object storage, and all metadata [is](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#sharedmergetree-for-cloud-native-data-processing) stored in Keeper. When a ClickHouse server has written a new part to object storage (see ② above) or merged some parts to a new larger part (see ③ above), then this ClickHouse server is using a [multi](https://zookeeper.apache.org/doc/r3.4.3/api/org/apache/zookeeper/ZooKeeper.html#multi(java.lang.Iterable))\-write transaction request for updating the metadata about the new part in Keeper. This information includes the name of the part, which files belong to the part, and where the blobs corresponding to files reside in object storage. Each server has a local cache with subsets of the metadata and [gets](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#sharedmergetree-for-cloud-native-data-processing) automatically informed about data changes by a Keeper instance through a [watch](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkWatches)\-based subscription mechanism.

For our aforementioned initial part creations and background part merges, a total of \~18k Keeper requests were [executed](https://gist.github.com/tom-clickhouse/da9c0faee5f509fb0fae9c4ee5c4d667). This includes \~12k multi\-write transaction requests (containing only write\-subrequests). All other requests are a mix of read and write requests. Additionally, the ClickHouse servers received \~ 800 watch notifications from Keeper:

```
1total_requests:      17705
2multi_requests:      11642
3watch_notifications: 822
```
Copy command
We can [see](https://gist.github.com/tom-clickhouse/36b7e154f47411c5a37c764ae62a3fd8) how these requests were sent and how the watch notifications got received quite evenly from all three ClickHouse nodes:

```
1┌─n─┬─total_requests─┬─multi_requests─┬─watch_notifications─┐
2│ 1 │           5741 │           3671 │                 278 │
3│ 2 │           5593 │           3685 │                 269 │
4│ 3 │           6371 │           4286 │                 275 │
5└───┴────────────────┴────────────────┴─────────────────────┘
```
Copy command
The following two charts visualize these Keeper requests [during](https://gist.github.com/tom-clickhouse/3e3cafe83ed468b6d312ef5461dc3d03) the data\-loading process:
![Keeper-02.png](/_next/image?url=%2Fuploads%2FKeeper_02_0e4fabf14d.png&w=2048&q=75)
We can see that \~70% of the Keeper requests are multi\-write transactions.

Note that the amount of Keeper requests can vary based on the ClickHouse cluster size, ingest settings, and data size. We briefly demonstrate how these three factors influence the number of generated Keeper requests.

#### ClickHouse cluster size \#

If we load the data with 10 instead of 3 servers in parallel, we ingest the data more than 3 times faster (with the [SharedMergeTree](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates)):
