---
source: blog
url: https://clickhouse.com/docs/shards
topic: introducing-multi-stage-distributed-query-execution-in-clickhouse-cloud
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 12
---

# Introducing multi\-stage distributed query execution in ClickHouse Cloud

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Introducing multi\-stage distributed query execution in ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U033_M877_CU_9_2dc2d2d2cf7c_512_e14944ce54.jpeg&w=96&q=75)[Alexander Gololobov](/authors/alexander-gololobov)May 27, 2026 · 19 minutes read
> **TL;DR**  
> Multi\-stage distributed execution gives ClickHouse Cloud a new way to scale one query across many nodes. It repartitions intermediate data between stages, removing key bottlenecks in large joins and high\-cardinality aggregations.  
>   
> Early TPC\-H results show up to 3\.4× speedups for join\-heavy queries while retaining near\-linear aggregation scaling: 7\.4× faster on 8 nodes than on 1 node.

## Scaling one query across many nodes [\#](/blog/multi-stage-distributed-query-execution-clickhouse-cloud#scaling-one-query-across-many-nodes)

ClickHouse has always been able to scale a single query across multiple nodes. In shared\-nothing deployments, users do this with physical sharding and the `Distributed` table engine. In ClickHouse Cloud, parallel replicas brought intra\-query scaling to shared storage.

These mechanisms work well for many analytical queries, but they were not the final answer for modern PB\-scale workloads. They could fan out work across nodes, but they could not freely repartition intermediate results between execution stages. That limited how far ClickHouse could scale high\-cardinality aggregations, and especially large joins.

Multi\-stage distributed query execution is the next step. It gives ClickHouse Cloud a new way to parallelize a single query across the CPU and memory of all available nodes, without the bottlenecks of the previous execution models.

In this post, we introduce the new extension of ClickHouse’s query execution model and walk through how it works. We use a multi\-table join as the running example because joins are among the hardest analytical workloads to scale, but the mechanism is much broader: it is a new foundation for distributed query execution in ClickHouse Cloud.

Before we look at the new mechanics, let’s review what came before and why those approaches weren’t enough for modern PB\-scale workloads.

## Why existing distributed execution was not enough [\#](/blog/multi-stage-distributed-query-execution-clickhouse-cloud#why-existing-distributed-execution-was-not-enough)

The existing distributed execution was useful but not elastic enough for PB\-scale workloads.
