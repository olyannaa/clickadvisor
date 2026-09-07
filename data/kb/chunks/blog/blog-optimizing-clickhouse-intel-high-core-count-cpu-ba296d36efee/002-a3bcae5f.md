---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Optimizing
topic: optimizing-clickhouse-for-intel-s-ultra-high-core-count-processors-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 2
total_chunks_in_doc: 17
---

utilize the available hardware fully. Bottlenecks for parallel processing like lock contention, cache coherence, non\-uniform memory access (NUMA), memory bandwidth, and coordination overhead become significantly worse as the core count increases. ## **Optimizing for ultra\-high core counts** \#

Over the past three years, I dedicated a part of my professional life to understand and optimize ClickHouse's scalability on Intel Xeon ultra\-high core count processors. My work focused on using various profiling and analysis tools \- including perf, emon, and Intel VTune \- to analyze all 43 ClickBench queries on ultra\-high core count servers systematically, identifying bottlenecks, and optimizing the ClickHouse accordingly.

The results have been exciting: individual optimizations routinely deliver speedups of multiple times for individual queries, in some cases up to 10x. The geometric mean of all 43 ClickBench queries consistently improved between 2% and 10% per optimization. The results demonstrate that ClickHouse can be made to scale very well on ultra\-high core count systems.

## **The core scaling challenge** \#

Beyond single\-thread performance, several key challenges must be addressed to optimize performance in ultra\-high core count systems.

1. **Cache coherence overhead**: Bouncing cache lines costs CPU cycles.
2. **Lock contention**: Amdahl's Law becomes brutal for serialized code sections as little as 1% of the overall code.
3. **Memory bandwidth**: Utilizing the memory bandwidth effectively is a persistent challenge for data\-intensive systems. Proper memory reuse, management and caching becomes critical.
4. **Thread coordination**: The cost of synchronizing threads grows super\-linearly with the number of threads.
5. **NUMA effects**: The memory latency and bandwidth on multi\-socket systems differs for local or remote memory.

This blog post summarizes our optimizations for ClickHouse on ultra\-high core count servers. All of them were merged into the main codeline and they now help to speed up queries in ClickHouse deployments around the globe.

**Hardware setup**: Our work was conducted on Intel's latest generation platforms, including 2 x 80 vCPUs Ice Lake (ICX), 2 x 128 vCPUs Sapphire Rapids (SPR), 1 x 288 vCPUs Sierra Forest (SRF), and 2 x 240 vCPUs Granite Rapids (GNR). SMT (Hyper\-threading) was enabled, except on SRF which doesn't support SMT, and high\-memory\-bandwidth configurations.

**Software setup**: We used perf, Intel VTune, pipeline visualization, and other custom profiling infrastructure.

## **The five optimization areas** \#
