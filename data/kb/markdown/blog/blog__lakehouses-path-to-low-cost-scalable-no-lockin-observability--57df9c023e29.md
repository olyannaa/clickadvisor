# Are open\-table\-formats \+ lakehouses the future of observability?


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Are open\-table\-formats \+ lakehouses the future of observability?

![](/_next/image?url=%2Fuploads%2FMelvyn_00a76a1519.PNG&w=96&q=75)![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Melvyn Peignon](/authors/melvyn-peignon) and [Dale McDiarmid](/authors/dale-mcdiarmid)Oct 16, 2025 · 28 minutes read
> **TL;DR**  
>   
> Lakehouses using open table formats like **Apache Iceberg** and **Delta Lake** are becoming viable for observability, pairing Parquet’s columnar compression and filtering with schema evolution, snapshots, and catalogs.  
>   
> There are challenges for telemetry at scale: partitioning tradeoffs, metadata growth, concurrent writes, Parquet’s limits for semi\-structured data and point lookups, and object storage latency. New work, such as liquid clustering, Parquet's new **VARIANT** type, and emerging formats like **Lance** helps close the gap.


## Lakehouses for observability [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#lakehouses-for-observability)


Over the past five years, a revolution has been underway in how organizations manage and analyze data. Open table formats such as Apache Iceberg and Delta Lake have brought structure to the once\-chaotic world of data lakes for analytics and warehousing. They enable [data lakehouses](https://clickhouse.com/resources/engineering/data-lakehouse) that promise the scalability and low cost of object storage with the semantics of a database.


![table_format_adoption.png](/uploads/table_format_adoption_98adff9c63.png)
Where data lakes once forced users to choose between flexibility and structure, open formats now provide table\-like abstractions on top of simple files, turning collections of data into something that behaves more like a database system. They reduce duplication, **eliminate vendor lock\-in**, and bring database\-level governance and consistency to large, previously unstructured datasets. Crucially, they **decouple storage from compute**, creating a neutral storage layer that **any query engine can attach to**. This allows users to choose the best tool for each workload without being tied to a single vendor or execution engine.


If, like us, you think of observability as just another data problem, it seems natural to ask: **Can we use lakehouses with open table formats for observability workloads?**


More specifically, do they provide the properties we want for the observability use case: **fast reads, flexible schema for semi\-structured events, good compression, low cost long\-term retention, and high throughput ingestion?**


In this post, we explore the strengths of the open table formats used in lakehouses and their underlying technologies, as well as their deficiencies, while also highlighting the encouraging developments that we believe will make these formats an integral part of observability workloads in the future.


### Try ClickStack today
 [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#test)

Deploy the world’s fastest and most scalable open source observability stack, with one command.

[Get started](https://clickhouse.com/docs/use-cases/observability/clickstack/getting-started?loc=blog-o11y-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## Where the lakehouse works for observability [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#where-the-lakehouse-works-for-observability)


Many teams already write logs, traces, or metrics directly to object storage for long\-term retention at low cost. An open table format adds database\-like semantics, making this data queryable by a range of engines, such as ClickHouse, without vendor lock\-in or the need to copy and reprocess it into specialized observability systems. In theory, this approach offers a path to lower compute costs and reduced data duplication \- and the network costs typically associated with moving data, while delivering **low\-cost long\-term retention**. Let's explore the properties of the open table formats suited to hosting observability workloads, starting with the underlying file format \- Parquet.


### Parquet \- a solid columnar foundation [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#parquet---a-solid-columnar-foundation)


[Apache Parquet](https://en.wikipedia.org/wiki/Apache_Parquet) is a columnar file format designed for efficient analytical processing on large datasets. Instead of storing rows together like traditional databases, Parquet stores data by column, allowing queries to read only the fields they need \- **ideal for powering aggregations and charts in observability workloads**. This columnar layout also enables **highly efficient compression**, especially when values are sorted or repeated. Within each column, Parquet applies data\-aware encodings such as run\-length, dictionary, or delta encoding to reduce redundancy and store values more compactly.


![parquet.png](/uploads/parquet_905ec2ac5e.png)
*Example web analytics dataset as Parquet files*
Each column in a Parquet file is divided into column chunks (2\), which hold the data for that column. These column chunks are further split into pages (3\), typically a few megabytes in size, which serve as the unit of I/O during reads. Each page is then compressed at the block level using algorithms like Zstandard (ZSTD) or Snappy, reducing both storage footprint and the amount of I/O on read. Together, this layered design aims to balance **compression efficiency, fast selective reads**, and manageable metadata \- similar principles to those of ClickHouse's own columnar MergeTree engine.


Finally, Parquet groups column chunks into row groups (1\), each representing a horizontal slice of the dataset. These row groups are often the key to parallelism: most query engines process them independently across multiple threads or nodes. The size of each row group is defined by the writer. While most engines parallelize by row group, newer implementations (including ClickHouse's v2 reader) can also parallelize across columns within a page or across multiple files, offering even greater performance, especially on wide tables.


Parquet also includes a rich layer of metadata and statistics that **enable efficient filtering** before data is read as shown below. Each file stores this information in its footer (4\), which describes the schema, encodings, and column\-level min\-max statistics. At the column chunk level (1\), Parquet may include dictionaries used to [encode the column values](https://parquet.apache.org/docs/file-format/data-pages/encodings/) and improve compression while accelerating existence checks. Within those chunks, individual pages (2\) can also hold min/max statistics, allowing **fine\-grained pruning for fast reads**. Finally, Bloom filters are supported at a row group level (3\) for efficiently checking whether a value might exist. These metadata structures let query engines quickly identify which parts of a file are relevant, minimizing I/O and CPU use.


![parquet_structure.png](/uploads/parquet_structure_645d593488.png)

> Parquet's columnar layout, statistics, and use of modern compression algorithms, enables both high compression and efficient filtering. These features make it well suited to observability workloads that pair selective filtering with large scans and aggregations.


### Open table formats \- building on solid foundations [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#open-table-formats---building-on-solid-foundations)


Parquet provides the physical storage foundation for most lakehouse systems but is only a file format, defining data layout without managing changes or coordinating writers. Table formats such as Apache Iceberg and Delta Lake build on Parquet to add essential table semantics: [snapshots](https://iceberg.apache.org/docs/nightly/branching/), [schema evolution](https://iceberg.apache.org/docs/nightly/evolution/), time travel and atomic commits. They introduce [catalogs](https://iceberg.apache.org/docs/nightly/aws/#catalogs) \- metadata services that track table locations, versions, and schema history, such as [Unity](https://www.databricks.com/product/unity-catalog), [AWS Glue](https://aws.amazon.com/glue/) and [Nessie](https://projectnessie.org/). This turns loose collections of files into coherent, mutable tables.


In this discussion, we focus on the features most relevant to observability, where transactional guarantees are less critical and the data is mostly immutable. While there are implementation differences between the table formats, their objectives are consistent. For example purposes, we largely focus on Apache Iceberg.


![iceberg_catalog.png](/uploads/iceberg_catalog_0dfd758300.png)
*Iceberg table format with catalogs*
### Schema evolution [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#schema-evolution)


One of the most valuable capabilities that table formats add is [schema management and evolution](https://iceberg.apache.org/docs/nightly/evolution/). In observability, where telemetry structures change frequently and new attributes appear over time, this flexibility allows data to evolve without rewriting historical files or needing to manage schema management manually through a custom metadata layer. Managing this without a table format requires a query engine (or user) to understand the schema variations and adapt queries. Table formats record schema versions in their metadata, so older data remains queryable even as the schema grows or changes. In summary, this makes querying simpler and more reliable for observability vs "just a bunch of parquet files".


![partitioning.png](/uploads/partitioning_2c913f9001.png)
### Partitioning [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#partitioning)


Tables can be [partitioned by time](https://iceberg.apache.org/docs/nightly/partitioning/), service, or other dimensions, improving query efficiency by letting engines read only the relevant partitions. Combined with additional metadata, such as file\-level and column\-level statistics, these formats enable metadata\-based pruning \- engines can skip entire partitions and files before having to scan Parquet data, reducing both I/O and latency.


### Compaction and sorting [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#compaction-and-sorting)


**Maintaining fast reads** in lakehouse systems depends on two related factors: keeping [data sorted](https://iceberg.apache.org/docs/latest/spark-ddl/#alter-table-write-ordered-by) and minimizing the number of small files. Sorting ensures that similar values are written close together, which **improves compression** and makes file\-and column\-level statistics more effective for filtering. Having too many small files, however, adds significant metadata and I/O overhead. Each file carries its own footer and must be opened, read, and planned separately, increasing latency and reducing scan efficiency. Without consistent ordering and file consolidation, data becomes fragmented, pruning loses effectiveness, and queries are forced to read far more data than necessary.


Achieving this ordering at write time is straightforward in principle but can be more complex in practice. Incoming data must be batched and sorted before being written, ensuring each Parquet file contains values aligned by partition keys such as timestamps or service names. This process often requires coordination through external systems like Kafka, Flink, or Spark, which handle buffering and sorting before writing.


Even if files are written in order, that order degrades over time as new data arrives or late events are ingested. Maintaining locality requires [periodic compaction](https://docs.aws.amazon.com/prescriptive-guidance/latest/apache-iceberg-on-aws/best-practices-compaction.html), where many small or disordered files are merged into larger, well\-sorted ones. Compaction reduces metadata overhead, consolidates deletes and updates, and maintains the data locality that underpins good compression and query performance. In lakehouse environments, this is typically executed by external engines such as Spark or Athena, or handled automatically in managed systems like Databricks through continuous background processes.


![iceberg_compaction.png](/uploads/iceberg_compaction_4adbb2f602.png)
*Users must configure the number of files, their minimum and maximum sizes, and the total bytes in each file group used during compaction to balance performance and resource efficiency.*

> ClickHouse handles both batching and compaction natively. Small inserts from edge agents or telemetry collectors are [automatically batched and sorted](https://clickhouse.com/docs/best-practices/selecting-an-insert-strategy) before being written, ensuring values are co\-located for optimal compression and efficient filtering. A [background merge process](https://clickhouse.com/docs/merges) then continuously combines smaller data parts into larger, ordered files \- transparent to the user.


### Snapshots [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#snapshots)


Features such as [snapshots](https://iceberg.apache.org/spec/?h=snapshots#snapshots) and time travel make table formats attractive for operational observability pipelines. Snapshots capture point\-in\-time versions of a dataset, providing a consistent view across large, distributed writes. This supports reproducible analyses and safe rollbacks when ingestion jobs fail or need reprocessing.


### Table formats and object storage [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#table-formats-and-object-storage)


Object storage underpins the scalability of lakehouses. While these tables could in theory reside on local SSDs, they are almost always hosted on systems like Amazon S3, Azure Blob Storage, or Google Cloud Storage \- the layer that provides effectively **infinite retention at low cost.** Most modern query engines, including ClickHouse, can natively read both Parquet files and their associated table formats directly from object storage, making the combination of open formats and cloud\-native infrastructure remarkably powerful.


While both the file formats and table formats integrate well with object storage, this architecture also surfaces several practical limitations \- ones we’ll explore next.


## Challenges of using open table formats for observability [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#challenges-of-using-open-table-formats-for-observability)


### Choosing a partitioning strategy [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#choosing-a-partitioning-strategy)


Choosing the right [partitioning strategy](https://iceberg.apache.org/docs/1.10.0/docs/partitioning/?h=parti) when working with open table formats is critical. Partitions determine how data is physically organized and how **efficiently queries can target relevant subsets for fast reads**. While ClickHouse also [supports partitioning](https://clickhouse.com/docs/partitions), it allows for a [primary key](https://clickhouse.com/docs/primary-indexes), enabling ordering and filtering at a much finer granularity. Over\-partitioning leads to an explosion of small files, while under\-partitioning forces unnecessarily wide scans. To mitigate these issues, users must handle such problems manually with external processes or use a managed solution such as Databricks and AWS S3 tables. This problem is especially notable when late\-arriving data causes fragmentation in partitions with small files, which later require explicit compaction to restore performance. In contrast, most analytical databases have built\-in [merge processes](https://clickhouse.com/docs/merges) to address these issues transparently.


### Metadata Scaling [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#metadata-scaling)


Metadata scaling and snapshot management present another challenge for lakehouse systems. Each write, schema change, or compaction in formats like Iceberg creates new metadata files that record the table’s state, including manifests, snapshots, and file listings. In **high\-ingest environments such as observability**, these structures can grow to millions of entries, increasing query planning latency, memory use, and lowering insert performance. To control this growth, engines must periodically merge manifests, expire snapshots, and perform garbage collection, which requires coordination and compute resources. Although these maintenance tasks are well understood, they add operational complexity that must be considered at scale.


### Parallel writes [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#parallel-writes)


Table formats provide robust write semantics through **optimistic concurrency control**, allowing multiple writers to safely commit to the same table at once. Each writer works against the latest snapshot of the table, and commits are handled atomically by the catalog; if another writer updates the table first, the later writer retries with the new state. This model is compelling because it brings database\-like isolation to object storage, but at **very high ingestion rates** **common in observability workloads**, contention on the table’s metadata pointer can become a bottleneck, leading to repeated retries and slower commit throughput. Users can mitigate this by batching writes, using partition\-level parallelism so that each writer handles a separate partition or bucket, and periodically compacting small files. Even with these techniques, however, scaling concurrent writes requires more orchestration and tuning than a traditional database, where such coordination is handled transparently by the storage engine itself.


### Parquet as a potential limitation [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#parquet-as-a-potential-limitation)


Although most of the challenges discussed above in open table formats can be mitigated with the right tools or managed services, there are more fundamental challenges in the Parquet file format for observability.


#### Support for semi\-structured data [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#support-for-semi-structured-data)


Some of these constraints stem from its design goals as a static, columnar storage format rather than a dynamic database engine. While highly efficient for structured analytical data, Parquet’s tight coupling between data types and its physical layout makes type evolution difficult and limits the variety of supported types compared to modern database systems. Its handling of semi\-structured data, needed for the dynamic data seen in observability, is limited.


In most engines, working with semi\-structured data in Parquet often requires reading and decompressing entire pages of encoded data just to access a single field, since nested structures ( e.g. [structs](https://parquet-writer.readthedocs.io/en/latest/struct_types.html), [`LIST`](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#lists)) are stored using definition and repetition levels that must be sequentially decoded to reconstruct hierarchy. This approach can make queries over JSON\-like data slow and resource\-intensive, especially when only a few attributes are needed deep in a hierarchy. More importantly, using structs and `LIST` requires the user to know the schema upfront while also ensuring each field has a consistent type. Furthermore, as new fields are encountered, the format’s table schema must be updated \- an expensive metadata operation at scale. Alternatively, JSON can be [encoded as a byte array](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#json) but this requires decoding and reading every value when querying \- infeasible and slow at scale.



> Recently, Parquet has introduced a [`VARIANT`](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#variant) type, which shows promise in addressing these challenges \- see below.


![parquet_vs_clickhouse_json.png](/uploads/parquet_vs_clickhouse_json_dbfb08a45a.png)
*Parquet JSON vs ClickHouse JSON*
In contrast, analytical databases such as ClickHouse [provide more advanced support](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse) for semi\-structured data: JSON fields can be automatically expanded into type\-specific columns at insert time, enabling users to query individual keys without having to scan or parse entire objects \- retaining all the compression, indexing, and filtering benefits of native columnar storage.


#### For large scans, not small reads [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#for-large-scans-not-small-reads)


Parquet is fundamentally optimized for large, sequential scans rather than point reads. Its design favors throughput over latency: data is stored in large, compressed pages within row groups, often spanning tens or hundreds of megabytes. To read even a single record, a query engine must locate the correct row group, fetch the corresponding column chunks, and decompress entire pages (inc. dictionaries) to extract the required values. This process introduces overhead, all of which makes single\-record retrieval slow and costly. In contrast, databases like ClickHouse maintain in\-memory indexes that can pinpoint the exact block containing a value.


This inefficiency is particularly relevant to observability workloads, where point queries are common. When investigating a specific trace or log event, analysts often query by unique identifiers such as `trace_id` or `span_id`. These lookups are high\-selectivity with Parquet’s structure simply not built for this access pattern.


Several workarounds exist, but all involve trade\-offs. External indexes, such as Elasticsearch or key\-value stores, can speed lookups but add infrastructure, complexity, and consistency risks. Partitioning by high\-cardinality keys improves selectivity yet creates many small files and reduces compression efficiency. [Bloom filters](https://parquet.apache.org/docs/file-format/bloomfilter/) narrow searches but still means reading and decompressing full pages. In summary, **high latency point reads represent a limitation for using lakehouses for observability**.


#### Metadata overheads [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#metadata-overheads)


A major challenge with Parquet is metadata overhead and managing row group sizes. Each file's footer stores schema, encoding, compression, and statistics for every column and row group. As datasets widen, or if they use many small row groups, this metadata can grow to tens of megabytes per file. Since the footer must be read and parsed before data access, large metadata directly slows query planning and increases latency. In wide or finely partitioned datasets, engines may spend more time processing metadata than reading data, especially when many files are scanned in parallel over object storage.


Choosing the right row group size is key to balancing performance. Smaller groups provide finer\-grained statistics, enabling better data skipping and parallelism, but each adds metadata and increases footer size, slowing planning. Larger groups reduce metadata and improve scan efficiency, but limit pruning, lower parallelism, and can raise memory use when decompressing wide data. The optimal size depends on the workload and data, and is rarely obvious.


These kinds of optimizations are low\-level and often extremely time\-consuming to get right. They are well beyond the interests or responsibilities of most observability teams, who generally want a storage engine that simply works.


#### Optimizing for object storage [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#optimizing-for-object-storage)


Although Parquet performs exceptionally well on local or distributed file systems, its design exposes weaknesses when used directly on object storage, such as S3\. The format's metadata\-driven structure requires a series of reads \- (1\) the footer to discover schema and row groups, the associated (2\) page group metadata, (3\) page and (4\) column metadata, and finally the data pages themselves.


![parquet_object_storage.png](/uploads/parquet_object_storage_4c261ae077.png)
Each step translates into multiple network round\-trip requests, and because S3 requests have relatively high latency, even a small query can trigger dozens of sequential HTTP range requests before any data is processed. This "request amplification" effect makes Parquet inherently "chatty" on object stores. The situation is compounded by large metadata blocks: detailed statistics and page indexes improve pruning but inflate the amount of non\-data bytes that must be downloaded and parsed during query planning. While engines like ClickHouse mitigate this through asynchronous I/O, aggressive prefetching, and metadata caching, underlying challenges remain for the high\-latency, high\-throughput properties of object storage in order to deliver **fast reads for observability**.


## Innovations are solving problems [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#innovations-are-solving-problems)


Although a lot of the challenges described above may seem complex and difficult to manage, the industry is encouraging moving quickly.


### Table format innovations [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#table-format-innovations)


One of the most notable is progress around compaction and clustering. Modern engines are increasingly automating these tasks, removing much of the manual overhead that once required dedicated Spark jobs. Liquid clustering, introduced by Databricks and now influencing broader ecosystem development, is especially promising. Rather than performing costly full\-table rewrites, it incrementally re\-clusters data in the background, preserving sort order while minimizing write amplification. This keeps data well\-organized and compression\-efficient without constant manual intervention, ensuring that recent writes remain performant for queries.


By design there is no native support for sparse primary or inverted indexes in Iceberg, as used by ClickHouse for more granular pruning. Some proprietary implementations are addressing this gap by adding external or auxiliary index layers to accelerate other access patterns, but these are vendor\-specific and not available as open\-source standards. [Open source projects](https://github.com/indextables/indextables_spark) have emerged recently which aim to address this.


### Parquet improvements and beyond [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#parquet-improvements-and-beyond)


At the file\-format level, Parquet is also evolving to better handle semi\-structured data. The introduction of the [`VARIANT` type](https://github.com/apache/parquet-format/blob/master/VariantEncoding.md) allows a single column to store flexible, nested values \- objects, arrays, or scalars \- within a unified structure. This makes it easier to represent semi structured data like JSON with evolving schemas, optional fields and inconsistent types for the same field name. The format records structural metadata that enables engines to navigate directly to the relevant portions of a record without fully decoding each nested element. Fields and values are encoded separately, in metadata and value columns with dictionary encoding used for the former \- benefiting cases where the JSON fields are often common across events. The type also introduces new more granular types as well as the concept of shredding, where nested or repeated fields are materialized into their own columns to improve query performance \- akin to how the ClickHouse JSON type enables efficient columnar access to individual keys within semi\-structured data. While still early in adoption, this feature has the potential to reduce unnecessary page reads and improve query efficiency for sparse, semi\-structured data that was previously expensive to filter in Parquet.


![variant_parquet.png](/uploads/variant_parquet_7060ac36b4.png)
*The variant type uses two\-level dictionary encoding: field names are dictionary\-encoded as metadata. This optimizes storage for objects with the same field names. Credit for original diagram: Andrew Lamb \- <https://andrew.nerdnetworks.org/speaking/>*


These improvements won’t address some of the inherent limitations of Parquet, though. Aside from being optimized for large sequential scans on local filesystems, not for fine\-grained point reads or high\-latency object storage such as S3, it lacks many of the optimizations inherent in databases like ClickHouse aimed at reducing and minimizing S3 requests, as well as the means to store columns independently for fast reads e.g. wide parts in ClickHouse.


For workloads that mix real\-time lookups with broad analytical scans, such as observability, Parquet’s row\-group structure and metadata model can become a bottleneck.


As a result, the industry is beginning to explore new file formats that build on Parquet’s strengths while addressing its weaknesses. Emerging alternatives include **[Vortex](https://github.com/vortex-data/vortex)**, **[FastLanes](https://github.com/cwida/FastLanes)**, **[BtrBlocks](https://www.cs.cit.tum.de/fileadmin/w00cfj/dis/papers/btrblocks.pdf)**, and **[Lance](https://lancedb.github.io/lance/)** \- each rethinking aspects of how data is stored, compressed, and accessed. Among these, **Lance** is showing particularly strong momentum.


![formats_stars.png](/uploads/formats_stars_90693c58c9.png)
[Lance takes a different approach](https://blog.lancedb.com/lance-v2/) to layout and access: rather than relying on fixed\-size row groups, it stores data in independently flushed fragments that allow both efficient scans and fine\-grained random reads \- effectively discharging the concept of row groups. Each column can flush pages independently, so columns with high update or append rates no longer need to stay aligned with the rest of the dataset. Sizes can also be aligned with the underlying storage medium to optimize range requests. This design improves concurrency, relying rather on pipeline parallelism, makes it easier to read small subsets of data without decompressing large contiguous blocks, but also eliminates the need to understand group and metadata sizes and how to optimize them for efficiency.


![lance_format.png](/uploads/lance_format_e096e66db5.png)
*Credit: LanceDB benefits. Original images are from [https://blog.lancedb.com/lance\-v2](https://blog.lancedb.com/lance-v2)*
Lance also replaces Parquet's rigid encoding system with a plugin\-based architecture, where encodings and statistics are defined as extensions \- data is just stored as bytes and encoded and decoded by plugins. This makes it trivial to add new compression schemes or indexing strategies without modifying the file reader or format specification \- just write a new (de/en)coder. Metadata, such as dictionaries or skip tables, can also be stored at a column or page level \- the former often more appropriate for point lookup queries.


![lance_metadata.png](/uploads/lance_metadata_98ff0b58be.png)
*Credit: LanceDB benefits. Original images are from [https://blog.lancedb.com/lance\-v2](https://blog.lancedb.com/lance-v2)*
Lance may not ultimately be the format used for observability, but along with other emerging approaches it introduces several promising ideas. All of these formats are still early in their lifecycle, and none have yet been tested at the full scale or complexity of production observability pipelines. The key will be ensuring that query engines remain open and format\-agnostic, allowing storage innovation to progress independently and letting the best format succeed on its technical merits.


## ClickHouse and open table formats [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#clickhouse-and-open-table-formats)


We believe that open table formats will ultimately become a central component of [open, cost\-efficient observability architectures](/blog/breaking-free-from-rising-observability-costs-with-open-cost-efficient-architectures), offering long\-term storage for massive telemetry datasets. ClickHouse is uniquely well positioned to support this transition. As a database already proven at scale for storing and querying observability data, it combines the performance characteristics \- fast ingestion, efficient compression, and low\-latency analytics \- that make it a natural fit for integrating with open table formats.


ClickHouse has supported querying Parquet files for many years and [continues to lead in performance](http://bit.ly/3WETHVh) through ongoing [improvements to its Parquet reader](https://clickhouse.com/blog/clickhouse-release-25-08). Recent updates have introduced parallelization across columns within row groups, allowing different columns in the same row group to be read concurrently. This approach fully uses modern multi\-core systems and significantly improves throughput on wide tables. This new reader also merges I/O requests, combining small, adjacent reads into larger, more efficient operations. This is particularly effective on high\-latency object storage, where ClickHouse can pre\-register expected byte ranges and issue fewer, larger read requests to maximize sequential throughput.


![clickbench_parquet.png](/uploads/clickbench_parquet_6b2b16f998.png)
*Clickbench is an independent benchmark for assessing performance of analytical databases over a test data set. In this case, we show only performance over Parquet only.*


Beyond Parquet itself, ClickHouse has expanded its integration with table catalogs and open table formats. It can now query data managed through catalogs such as AWS Glue, Unity Catalog, LakeKeeper, and Nessie, exposing these directly as regular ClickHouse databases with tables.



```

```
1CREATE DATABASE unity
2ENGINE = DataLakeCatalog('https://.cloud.databricks.com/api/2.1/unity-catalog/iceberg')
3SETTINGS catalog_type = 'rest', catalog_credential = ':', warehouse = 'workspace',
4oauth_server_uri = 'https://.cloud.databricks.com/oidc/v1/token', auth_scope = 'all-apis,sql'
```

```

By exposing Iceberg and Delta Lake tables as “just another table” in ClickHouse, existing ClickHouse observability tooling such as ClickStack “just works” out of the box.


Recent releases have also introduced write support for Iceberg and Delta Lake, with growing feature coverage including pruning using statistics and partitions, concurrent reads, time travel, and delete operations. This enables ClickHouse to operate as both a query engine and a writer for open table formats, bringing database\-grade performance to data stored in open, interoperable formats.


In real\-world observability deployments, some users have adopted a dual\-write architecture. Observability data is written both to ClickHouse’s MergeTree tables for hot, real\-time analysis and to open table formats for long\-term cold retention.


![clickhouse_lakes.png](/uploads/clickhouse_lakes_02023f8174.png)
The MergeTree engine combines many of the strengths of lakehouse and open table formats while also addressing and simplifying their challenges in observability use cases. It unifies features such as **automatic background merges** to maintain data locality, **sparse indexing for fast reads**, **schema\-on\-write with JSON support**, and lifecycle management within a single system. This removes the need for users to manage compaction, metadata, or file optimization. Its columnar structure provides **excellent compression**, and **native support for S3** enables **low\-cost long\-term retention**. At the same time, built\-in isolation between inserts and reads ensures high\-throughput ingestion without impacting query performance.


Meanwhile, open table formats provide the durability and cost advantages of object storage. This dual\-write pattern, used by organizations like Netflix, remains popular but introduces inefficiency \- data must be written twice and managed separately.



Looking forward, ClickHouse’s vision is for open table formats and database tables to converge into a single, unified model. In this future, a table stored in an open format would behave like any other ClickHouse table, benefiting from features such as materialized views that users exploit heavily when deploying ClickHouse for storing observability data.


Users would gain the interoperability of open data formats with the performance and manageability of a database engine. This represents the convergence of the database and lakehouse worlds \- one where storage format becomes an implementation detail, and ClickHouse transparently manages performance and layout beneath the surface. For large\-scale observability workloads, this model promises the best of both worlds: open, cost\-efficient storage combined with ClickHouse's [proven ability](https://clickhouse.com/user-stories) to deliver real\-time analytics at PB scale.


## Conclusion [\#](/blog/lakehouses-path-to-low-cost-scalable-no-lockin-observability#conclusion)


In summary, open table formats represent an exciting evolution in how observability data can be stored and accessed \- open, scalable, and increasingly interoperable across query engines. While challenges remain in performance, metadata management, and operational simplicity, innovation across file formats, table standards, and query engines is moving quickly. As these ecosystems mature, databases like ClickHouse are well\-positioned to bridge the gap between the raw scalability of object storage and the low\-latency performance demanded by observability. The convergence of databases and open table formats will ultimately give users the best of both worlds: the openness and cost efficiency of lakes with the speed, reliability, and simplicity of a purpose\-built analytical engine.



> One of the most notable recent developments in lakehouses and observability is [Cloudflare’s announcement of SQL support for querying data on R2 object storage](https://blog.cloudflare.com/cloudflare-data-platform/). Cloudflare plans to extend this to integrate with Logpush, allowing users to transform, store, and query logs natively within its platform.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
