---
source: blog
url: https://clickhouse.com/cloud/distributed-cache-waitlist
topic: building-a-distributed-cache-for-s3
ch_version_introduced: '150.96'
last_updated: '2026-06-12'
chunk_index: 9
total_chunks_in_doc: 15
---

often matching or exceeding local SSD performance. High\-throughput instances can reach up to 100 Gbps (12\.5 GB/s), and specialized configurations can go even further. Here’s how the network layer compares to other storage tiers on latency and throughput:

| Layer | Latency | IOPS | Throughput |
| --- | --- | --- | --- |
| S3 | 500 ms | 5K | 2 GB/sec |
| SSD | 1 ms | 100K | 4 GB/sec |
| Network | 100–250 µs |  | 1\.5–12\.5 GB/sec |
| Memory | 250 ns | 100M | 100 GB/sec |


Thanks to these characteristics, the distributed cache, accessed over the network, delivers latencies that fall neatly between SSD and memory. And like the local filesystem cache before it, it **solves the core bottleneck** of object storage: latency.

**It also scales.** Because hot table data is now **distributed across multiple cache nodes**, ClickHouse can fetch blocks in **parallel**, maximizing throughput. With enough nodes, this **compound throughput** can rival memory speeds, **tens or even hundreds of GB/sec** (more on how this works in a bit).

Like its predecessor, the distributed cache brings hot data closer to the query engine, first to SSDs, then straight into compute node RAM, powering the low\-latency execution real\-time analytics demand.

### Built for stateless compute [\#](/blog/building-a-distributed-cache-for-s3#built-for-stateless-compute)

This architecture allows ClickHouse compute nodes to be diskless, stateless machines, while the distributed cache nodes are disk\-optimized and purpose\-built to manage and serve hot data at high throughput with low latency.

### Per\-zone deployment [\#](/blog/building-a-distributed-cache-for-s3#per-zone-deployment)

The distributed cache runs per availability zone to avoid cross\-zone traffic and its costs. It can operate as zone\-local (lower latency) or cross\-zone (higher hit rate, but more latency and cost). The cache is shared across multiple ClickHouse Cloud services, but each is fully isolated with proper authentication and encryption.

### Beyond table data [\#](/blog/building-a-distributed-cache-for-s3#beyond-table-data)

The distributed filesystem cache also serves the same additional roles as the local cache did before: caching table metadata (like secondary data skipping indexes and mark files), storing temporary data (e.g., spill\-to\-disk), and caching external files (including data lake table files).

### How it works [\#](/blog/building-a-distributed-cache-for-s3#how-it-works)
