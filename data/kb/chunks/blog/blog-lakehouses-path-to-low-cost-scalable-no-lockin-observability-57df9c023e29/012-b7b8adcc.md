---
source: blog
url: https://clickhouse.com/resources/engineering/data-lakehouse
topic: are-open-table-formats-lakehouses-the-future-of-observability
ch_version_introduced: '1.10'
last_updated: '2026-06-12'
chunk_index: 12
total_chunks_in_doc: 16
---

access to individual keys within semi\-structured data. While still early in adoption, this feature has the potential to reduce unnecessary page reads and improve query efficiency for sparse, semi\-structured data that was previously expensive to filter in Parquet.

![variant_parquet.png](/uploads/variant_parquet_7060ac36b4.png)
*The variant type uses two\-level dictionary encoding: field names are dictionary\-encoded as metadata. This optimizes storage for objects with the same field names. Credit for original diagram: Andrew Lamb \- <https://andrew.nerdnetworks.org/speaking/>*

These improvements won’t address some of the inherent limitations of Parquet, though. Aside from being optimized for large sequential scans on local filesystems, not for fine\-grained point reads or high\-latency object storage such as S3, it lacks many of the optimizations inherent in databases like ClickHouse aimed at reducing and minimizing S3 requests, as well as the means to store columns independently for fast reads e.g. wide parts in ClickHouse.

For workloads that mix real\-time lookups with broad analytical scans, such as observability, Parquet’s row\-group structure and metadata model can become a bottleneck.

As a result, the industry is beginning to explore new file formats that build on Parquet’s strengths while addressing its weaknesses. Emerging alternatives include **[Vortex](https://github.com/vortex-data/vortex)**, **[FastLanes](https://github.com/cwida/FastLanes)**, **[BtrBlocks](https://www.cs.cit.tum.de/fileadmin/w00cfj/dis/papers/btrblocks.pdf)**, and **[Lance](https://lancedb.github.io/lance/)** \- each rethinking aspects of how data is stored, compressed, and accessed. Among these, **Lance** is showing particularly strong momentum.

![formats_stars.png](/uploads/formats_stars_90693c58c9.png)
[Lance takes a different approach](https://blog.lancedb.com/lance-v2/) to layout and access: rather than relying on fixed\-size row groups, it stores data in independently flushed fragments that allow both efficient scans and fine\-grained random reads \- effectively discharging the concept of row groups. Each column can flush pages independently, so columns with high update or append rates no longer need to stay aligned with the rest of the dataset. Sizes can also be aligned with the underlying storage medium to optimize range requests. This design improves concurrency, relying rather on pipeline parallelism, makes it easier to read small subsets of data without decompressing large contiguous blocks, but also eliminates the need to understand group and metadata sizes and how to optimize them for efficiency.
