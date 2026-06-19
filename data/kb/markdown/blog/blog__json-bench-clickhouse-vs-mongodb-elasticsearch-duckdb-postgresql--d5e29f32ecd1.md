# The billion docs JSON Challenge: ClickHouse vs. MongoDB, Elasticsearch, and more


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# The billion docs JSON Challenge: ClickHouse vs. MongoDB, Elasticsearch, and more

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber)Jan 29, 2025 · 56 minutes read## Introduction [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#introduction)


We [took on](https://clickhouse.com/blog/clickhouse-one-billion-row-challenge) Gunnar Morling’s [One Billion Row Challenge](https://github.com/gunnarmorling/1brc) almost exactly a year ago, testing how quickly a 1\-billion\-row text file could be aggregated.


Now, we’re introducing a new challenge: the **One Billion Documents JSON Challenge**, which measures how well databases can store and aggregate a large dataset of semistructured JSON documents.


To tackle this challenge, we needed an efficient JSON implementation. We recently shared an [in\-depth look](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse) at how we built a powerful new JSON data type for ClickHouse from the ground up, showcasing why it’s the optimal implementation of JSON for columnar storage.


In this post, we compare ClickHouse’s JSON implementation to other data stores with JSON support. The results might surprise you.


To achieve this, we developed [JSONBench](https://jsonbench.com/)—a fully reproducible benchmark that loads identical JSON datasets into five popular data stores with first\-class JSON support:


1. **ClickHouse**
2. **MongoDB**
3. **Elasticsearch**
4. **DuckDB**
5. **PostgreSQL**


JSONBench evaluates the storage size of the loaded JSON datasets and the query performance of five typical analytical queries.


Here’s a preview of the [benchmark results](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#benchmark-results) for storing and querying 1 billion JSON documents.


- ClickHouse is **40% more storage efficient** and **2500 times faster at aggregations** than `MongoDB`.


![JSON-Benchmarks.001.png](/uploads/JSON_Benchmarks_001_114bb1d888.png)
- ClickHouse needs **two times less storage space** and is **ten times faster at aggregations** than `Elasticsearch`.


![JSON-Benchmarks.002.png](/uploads/JSON_Benchmarks_002_b6533a4196.png)
- ClickHouse requires **five times less disk space and is nine thousand times faster** than `DuckDB` at analytical queries.


![JSON-Benchmarks.003.png](/uploads/JSON_Benchmarks_003_c305e9705a.png)
- ClickHouse uses **six times less disk space** and is **nine thousand** **times faster** than `PostgreSQL` for analytical queries.


![JSON-Benchmarks.004.png](/uploads/JSON_Benchmarks_004_a3be78fbff.png)
Last but not least, ClickHouse stores JSON documents **20% more compactly** than saving the same documents as `compressed files on disk`, even when using the same compression algorithm.


![JSON-Benchmarks.005.png](/uploads/JSON_Benchmarks_005_a59ea54096.png)
The rest of this blog will first describe our test JSON dataset and provide a brief overview of each benchmark candidate's JSON capabilities (please feel free to [skip](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#benchmark-setup) these if the technical details aren’t of interest). Then, we will explain the benchmark setup, queries, and methodology. Finally, we will present and analyze the [benchmark results](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#benchmark-results).


## The JSON dataset \- a billion Bluesky events [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#the-json-dataset---a-billion-bluesky-events)


Our test JSON dataset consists of a scraped event stream from the [Bluesky](https://bsky.social/about) social media platform. In another post, we detailed [how we retrieved the data](https://clickhouse.com/blog/building-a-medallion-architecture-for-bluesky-json-data-with-clickhouse#reading-bluesky-data) using the Bluesky API. The data is naturally formatted as JSON documents, with each document [representing](https://clickhouse.com/blog/building-a-medallion-architecture-for-bluesky-json-data-with-clickhouse#sampling-the-data) a specific [Bluesky event](https://github.com/bluesky-social/jetstream?tab=readme-ov-file#example-events) (e.g., `post`, `like`, `repost`, etc.).


The benchmark loads the following 8 Bluesky event datasets (① to ⑧ in the diagram below) into each benchmark candidate:
![](/uploads/JSON_Benchmarks_006_028b4d7bcb.png)


## Evaluated systems [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#evaluated-systems)


This section provides an overview of the benchmarked systems' JSON capabilities, data compression techniques, and query acceleration features (such as indexes and caches). Understanding these technical details helps clarify how each system was configured to ensure a fair and accurate comparison in our benchmark.



> You can [skip](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#benchmark-setup) this section if you’re not interested in these details.


### ClickHouse [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#clickhouse)


ClickHouse is a columnar analytical database. In this post, we’re benchmarking it against other candidates to highlight its outstanding capabilities in handling JSON data.


#### JSON support [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-support)


We recently [built](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse) a new powerful JSON data type for ClickHouse with true column\-oriented storage, support for dynamically changing data structures [without](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse#challenge-2-dynamically-changing-data-without-type-unification) type unification and the ability to query individual JSON paths really fast.


#### JSON storage [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-storage)


ClickHouse [stores](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse) the values of each unique JSON path as [native columns](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse#traditional-data-storage-in-clickhouse), allowing high data compression and, as we are demonstrating in this blog, maintaining the same [high query performance](https://benchmark.clickhouse.com/) seen on classic types:


![JSON-Benchmarks.007.png](/uploads/JSON_Benchmarks_007_6ec81b11c0.png)
The diagram above sketches how the values from each unique JSON path are stored on disk in separate (highly compressed) column files (inside a [data part](https://clickhouse.com/docs/en/parts#what-are-table-parts-in-clickhouse)). These columns can be accessed independently, minimizing unnecessary I/O for queries referencing only a few JSON paths.


#### Data sorting and compression [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#data-sorting-and-compression)


The ClickHouse JSON type allows JSON paths to be used as [primary key](https://clickhouse.com/docs/en/guides/best-practices/sparse-primary-indexes) columns. This ensures that ingested JSON documents are stored on disk, within each table part, [ordered](https://clickhouse.com/docs/en/guides/best-practices/sparse-primary-indexes#data-is-stored-on-disk-ordered-by-primary-key-columns) by the values of these paths. Additionally, ClickHouse generates a [sparse primary index](https://clickhouse.com/docs/en/guides/best-practices/sparse-primary-indexes#introduction) to automatically [accelerate](https://clickhouse.com/docs/en/guides/best-practices/sparse-primary-indexes#the-primary-index-is-used-for-selecting-granules) queries that filter on these primary key columns:


![JSON-Benchmarks.008.png](/uploads/JSON_Benchmarks_008_3e7fba21fe.png)
Using JSON subcolumns as primary key columns enables better colocation of similar data within each column file, which can [increase](https://clickhouse.com/docs/en/guides/best-practices/sparse-primary-indexes#optimal-compression-ratio-of-data-files) compression ratios for these column files, provided the primary key columns [are](https://clickhouse.com/docs/en/guides/best-practices/sparse-primary-indexes#optimal-compression-ratio-of-data-files) arranged in ascending order of cardinality. The on\-disk data ordering [also](https://clickhouse.com/blog/clickhouse-faster-queries-with-projections-and-primary-indexes#utilize-indexes-for-preventing-resorting-and-enabling-short-circuiting) prevents resorting and allows short\-circuiting when a query's search sort order matches the physical data order.


#### Flexible compression options [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#flexible-compression-options)


By default, ClickHouse [applies](https://clickhouse.com/docs/en/sql-reference/statements/create/table#column_compression_codec) `lz4` compression in the self\-managed version and `zstd` in [ClickHouse Cloud](https://clickhouse.com/cloud) to each data column file individually, [block\-wise](https://clickhouse.com/docs/en/data-compression/compression-modes#block).


It is also [possible](https://clickhouse.com/docs/en/sql-reference/statements/create/table#column_compression_codec) to define the compression codec(s) per individual column in the `CREATE TABLE` query. ClickHouse supports [general\-purpose](https://clickhouse.com/docs/en/sql-reference/statements/create/table#general-purpose-codecs), [specialized](https://clickhouse.com/docs/en/sql-reference/statements/create/table#specialized-codecs), and [encryption](https://clickhouse.com/docs/en/sql-reference/statements/create/table#encryption-codecs) codecs, which can also be [chained](https://clickhouse.com/blog/optimize-clickhouse-codecs-compression-schema).


For its JSON type, ClickHouse currently supports defining codecs for the whole JSON field (e.g. [here](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/ddl_zstd.sql#L8), we change the codec from the default `lz4` to `zstd`). We are [planning](https://github.com/ClickHouse/ClickHouse/issues/68428) to support specifying codecs also per JSON path.


#### Flexible JSON format options [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#flexible-json-format-options)


ClickHouse supports [over 20 different JSON formats](https://clickhouse.com/docs/en/interfaces/formats) for ingesting data and returning query results.


#### Query processing [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#query-processing)


Due to ClickHouse’s outstanding performance in our [benchmark results](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#benchmark-results), we’ve included a brief explanation of how it handles queries over JSON data.


As mentioned earlier, ClickHouse stores the values of each unique JSON path similarly to traditional data types (e.g. integers), enabling [high\-performance aggregations](https://clickhouse.com/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#high-performance-aggregations-in-clickhouse) over JSON data.


Built for internet\-scale analytics, ClickHouse is [designed](https://youtu.be/ZOZQCQEtrz8?si=XrQ-vMDiHEsgsrYq&t=103) to efficiently filter and aggregate data using the full resources available by fully parallelizing its [90\+](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference) built\-in aggregation functions. This approach can be illustrated with the `avg` aggregation function:


![JSON-Benchmarks.009.png](/uploads/JSON_Benchmarks_009_d2d2163ae6.png)
The diagram above shows how ClickHouse ① processes an `avg` aggregation query referencing two JSON paths `c.a` and `c.b`. Using (only) the corresponding data columns `a.bin` and `b.bin`, ClickHouse processes `N` non\-overlapping data ranges in parallel across `N` CPU cores on a single server. These data ranges are independent of the grouping key and are [dynamically balanced](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf) to optimize workload distribution. This parallelization is made possible through the use of [partial aggregation states](https://clickhouse.com/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#-multi-core-parallelization).


In our benchmark for ClickHouse, we also [track](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/physical_query_plans.sh) the [physical execution plans](https://youtu.be/hP6G2Nlz_cA), introspecting this parallelization approach. For instance, [here](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/_physical_query_plans/_m6i.8xlarge_bluesky_1000m_zstd.physical_query_plans#L15), you can observe how ClickHouse processes the full dataset aggregation from [benchmark query ①](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/queries_formatted.sql#L2) using 32 parallel execution lanes on our [test machine](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#hardware-and-operating-system) with 32 CPU cores.


#### Multi\-node parallelization [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#multi-node-parallelization)


While our benchmark for this blog focuses exclusively on single\-node performance, it’s worth noting for completeness that if the JSON source data of an aggregation query is distributed across multiple nodes (in the form of table shards), ClickHouse seamlessly parallelizes aggregation functions [across](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf) all available CPU cores on all nodes:


![JSON-Benchmarks.010.png](/uploads/JSON_Benchmarks_010_777404b2fb.png)
#### Caches [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#caches)


When performing queries, ClickHouse [uses](https://www.youtube.com/watch?v=-N6N-WKEiLs) different [built\-in caches](https://clickhouse.com/docs/en/operations/caches), as well as the operating system’s page cache. For example, although [disabled by default](https://clickhouse.com/docs/en/operations/settings/settings#use_query_cache), ClickHouse provides a [query result cache](https://clickhouse.com/docs/en/operations/query-cache).


### MongoDB [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#mongodb)


[MongoDB](https://www.mongodb.com/) is one of the most renowned [JSON databases](https://clickhouse.com/engineering-resources/json-database).


#### JSON support [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-support-1)


MongoDB stores all data natively as collections of [BSON](https://www.mongodb.com/resources/basics/json-and-bson) documents, where BSON [is](https://en.wikipedia.org/wiki/BSON) the binary representation of a JSON document.


#### JSON storage [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-storage-1)


MongoDB’s default storage engine, [WiredTiger](https://www.mongodb.com/docs/manual/core/wiredtiger/#wiredtiger-storage-engine), organizes data on disk as blocks that [represent](https://source.wiredtiger.com/11.0.0/arch-data-file.html) pages of a [B\-Tree](https://en.wikipedia.org/wiki/B-tree). The root and internal nodes store keys and references to other nodes, while the leaf nodes hold the data blocks for stored BSON documents:


![JSON-Benchmarks.011.png](/uploads/JSON_Benchmarks_011_1c3970b491.png)
MongoDB allows users to create secondary [indexes](https://www.mongodb.com/docs/manual/indexes/#details) on JSON paths to accelerate queries that filter on those paths. These indexes [are](https://www.slideshare.net/slideshow/mongodb-days-uk-indexing-and-performance-tuning/54794973#2) structured as B\-Trees, with each entry corresponding to an ingested JSON document and storing the values of the indexed JSON paths. These indexes are loaded into memory, enabling the query planner to [quickly](https://www.slideshare.net/slideshow/mongodb-days-uk-indexing-and-performance-tuning/54794973#2) traverse the tree to locate matching documents, which are then loaded from disk for processing.


#### Covered index scans [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#covered-index-scans)


If a query references only indexed JSON paths, MongoDB can satisfy it entirely using the in\-memory B\-Tree index, without loading documents from disk. This optimization, known as a [covered index scan](https://www.slideshare.net/slideshow/mongodb-days-uk-indexing-and-performance-tuning/54794973#2), is triggered by [covered queries](https://www.mongodb.com/docs/manual/core/query-optimization/#covered-query):


![JSON-Benchmarks.012.png](/uploads/JSON_Benchmarks_012_ac6786dc13.png)

> All five of our benchmark queries in MongoDB are covered queries. This is because the [default compound index](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#some-json-paths-can-be-used-for-indexes-and-data-sorting) we [created](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/ddl_zstd.js#L6) for all collections includes every field required by the queries. To follow [best practices](https://www.mongodb.com/docs/manual/core/query-optimization/#performance), we also explicitly [enabled](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#no-tuning) covered index scans.


You can confirm this by examining the [query execution plans](https://github.com/ClickHouse/JSONBench/tree/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/_index_usage). For example, queries on the 1 billion documents collection [show](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/_index_usage/_m6i.8xlarge_bluesky_1000m_zstd.index_usage) only `IXSCAN` stages, with no `COLLSCAN` or `FETCH` [stages](https://www.mongodb.com/docs/manual/reference/explain-results/#explain-output-structure). In contrast, [older plans](https://github.com/ClickHouse/JSONBench/tree/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results_without_covered_index_scans/_index_usage)—before enabling covered index scans—[include](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results_without_covered_index_scans/_index_usage/_m6i.8xlarge_bluesky_1000m_zstd.index_usage) `COLLSCAN` or `FETCH`, indicating that documents were being loaded from disk.


This method depends on the index fitting into memory. On our [test machine](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#hardware-and-operating-system) with 128 GB of RAM, the [27 GB index](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/m6i.8xlarge_bluesky_1000m_zstd.json#L20) for the largest dataset fits easily. In [sharded setups](https://www.mongodb.com/docs/manual/sharding/), however, covered index scans require the index to [include](https://www.mongodb.com/docs/manual/core/query-optimization/#restrictions-on-sharded-collection) the shard key.


#### Data compression [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#data-compression)


WiredTiger [defaults](https://www.mongodb.com/docs/manual/core/wiredtiger/#compression) to block compression with the [snappy](https://google.github.io/snappy/) library for collections and [prefix compression](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-prefix-compression) for B\-Tree indexes. Alternatively, `zstd` compression can be enabled for collections to achieve higher compression rates.


#### Data sorting [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#data-sorting)


MongoDB supports [clustered collections](https://www.mongodb.com/docs/manual/core/clustered-collections/), which store documents in the order of a specified [clustered index](https://www.mongodb.com/docs/manual/reference/method/db.createCollection/#std-label-db.createCollection.clusteredIndex), helping to colocate similar data and improve compression. However, since clustered index keys [must](https://www.mongodb.com/docs/manual/core/clustered-collections/#set-your-own-clustered-index-key-values) be unique and are limited to a maximum size of 8 MB, we couldn’t use them for our test data.


#### Caches [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#caches-1)


MongoDB relies on both the [WiredTiger internal cache](https://www.mongodb.com/docs/manual/core/wiredtiger/#memory-use) and the operating system’s page cache but does not have a query results cache. The WiredTiger cache, which stores recently accessed data and indexes, operates independently of the OS page cache. By default, its size is [set](https://www.mongodb.com/docs/manual/core/wiredtiger/#memory-use) to 50% of the available RAM minus 1 GB. This cache can only be cleared by restarting the MongoDB server.


#### Limitations [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#limitations)


The `time_us` JSON path in our [Bluesky test data](/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#the-json-dataset---a-billion-bluesky-events) contains microsecond\-precision dates. Currently, MongoDB only supports [millisecond](https://www.mongodb.com/docs/manual/reference/method/Date/#behavior) precision, whereas ClickHouse handles [nanoseconds](https://clickhouse.com/docs/en/sql-reference/data-types/datetime64).


Additionally, MongoDB’s aggregation framework lacks a built\-in `COUNT DISTINCT` operator. As a workaround, we use the less efficient [$addToSet](https://www.mongodb.com/docs/manual/reference/operator/aggregation/addToSet/) for benchmark [query ②](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/queries_formatted.js#L31).


### Elasticsearch [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#elasticsearch)


[Elasticsearch](https://www.elastic.co/elasticsearch) is a JSON\-based search and analytics engine.


#### JSON support [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-support-2)


Elasticsearch [receives](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html) all ingested data natively as JSON documents.


#### JSON storage and data compression [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-storage-and-data-compression)


Ingested JSON data in Elasticsearch is indexed and stored in [various](https://github.com/ClickHouse/examples/tree/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing#logical-and-physical-on-disk-data-structures) data structures optimized for specific access patterns. These structures reside within a [segment](https://github.com/ClickHouse/examples/tree/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing#logical-and-physical-on-disk-data-structures), the core indexing unit of [Lucene](https://lucene.apache.org/), the Java library that powers Elasticsearch’s search and analytics capabilities:


![JSON-Benchmarks.013.png](/uploads/JSON_Benchmarks_013_0c4a7cf1a0.png)
① [Stored fields](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-store.html) serve as a document store for returning the original values of fields in query responses. By default, they also store ② [\_source](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html), which contains the original JSON documents ingested. Stored fields are compressed using the algorithm defined by the [index.codec](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html) setting—`lz4` by default or `zstd` for higher compression ratios, albeit with slower performance.


③ [Doc\_values](https://www.elastic.co/guide/en/elasticsearch/reference/current/doc-values.html) store values from ingested JSON documents in a column\-oriented on\-disk structure optimized for analytical queries that aggregate and sort the data. Note that `doc_values` are not compressed with `lz4` or `zstd`. Instead, each column [is](https://lucene.apache.org/core/9_9_0/core/org/apache/lucene/codecs/lucene90/Lucene90DocValuesFormat.html) encoded individually with specialized codecs based on the column values‘ data type, cardinality, etc.


[Here](https://github.com/ClickHouse/examples/tree/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing#logical-and-physical-on-disk-data-structures), we describe the other Lucene segment data structures, such as the ④ `inverted index`, ⑤ `Bkd-trees`, and ⑥ `HNSW graphs` in more detail.


#### The role of \_source [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#the-role-of-_source)


The `_source` field is essential in Elasticsearch OSS for operations like [reindexing](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html) or [upgrading](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-upgrade.html#upgrade-index-compatibility) an index to a new major version and is also useful for queries that return original documents. Disabling `_source` significantly reduces disk usage but removes these capabilities.


In Elasticsearch enterprise tiers, the [synthetic \_source](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html#synthetic-source) feature allows `_source` to be reconstructed on demand from other Lucene data structures.


Our [benchmark queries](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#benchmark-queries) utilize `doc_values` and don’t require `_source`, as they return aggregated values rather than original documents. Therefore, we simulate the storage savings of `synthetic _source` by running benchmarks with `_source` disabled. For comparison, we also tested with `_source` enabled at various compression levels.


#### Configuring Elasticsearch for fair storage comparison [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#configuring-elasticsearch-for-fair-storage-comparison)


As noted earlier, Elasticsearch indexes and stores data in various structures optimized for specific access patterns. Since our benchmark focuses on data aggregations, we configured Elasticsearch to best align with this use case:


- **Minimized inverted index size**: We disabled full\-text search by [mapping](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/config/index_template_no_source_best_compression.json#L53) all strings as [keyword](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) types. This still supports effective filtering for our benchmark queries while also populating `doc_values` for efficient aggregations.
- **Date field mapping**: The ingested documents’ date field was [mapped](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/config/index_template_no_source_best_compression.json#L79) to Elasticsearch’s date type, which [leverages](https://www.elastic.co/blog/numeric-and-date-ranges-in-elasticsearch-just-another-brick-in-the-wall) Lucene’s [Bkd](https://users.cs.duke.edu/~pankaj/publications/papers/bkd-sstd.pdf) trees for range queries on dates.
- **Reduced storage overhead**: We [disabled](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/config/filebeat.yml#L82) all meta\-fields, ensuring only fields from the ingested JSON data are stored. Storage sizes were tested with \_source disabled to simulate synthetic \_source.
- **Index sorting**: We [enabled](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/config/index_template_source_best_compression.json#L28) index sorting using the same fields as [ClickHouse’s sorting key](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/ddl_zstd.sql#L10), optimizing data compression and query performance.
- **Single\-node optimization**: Replicas were [disabled](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/config/index_template_no_source_best_compression.json#L44) since we ran Elasticsearch on a single node.
- **Optimized rollovers and merges**: We [applied](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/config/ilm.json#L7) [best practices](https://www.elastic.co/guide/en/elasticsearch/reference/current/size-your-shards.html#shard-size-recommendation) for index rollovers and merges.


The next diagram summarises our benchmark configuration of Elasticsearch’s data structures:


![JSON-Benchmarks.014.png](/uploads/JSON_Benchmarks_014_16218543f4.png)
Note that disabling `_source` essentially makes the `index.codec` setting ineffective. It doesn’t matter if `lz4` or `zstd` is selected, as there is no data that can be compressed with these algorithms.


#### Data sorting [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#data-sorting-1)


To [improve](https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-disk-usage.html#_use_index_sorting_to_colocate_similar_documents) compression ratios for `stored fields` and `doc_values`, Elasticsearch allows optional configuration of [data sorting](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-index-sorting.html) on disk before compression. Similar to ClickHouse, this sorting also enhances query performance by [enabling](https://github.com/ClickHouse/examples/tree/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing#on-disk-data-ordering) early termination.


#### Caches [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#caches-2)


Elasticsearch processes queries [using](https://www.elastic.co/blog/elasticsearch-caching-deep-dive-boosting-query-speed-one-cache-at-a-time) the operating system’s page cache along with two query\-result caches: the shard\-level [request cache](https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-request-cache.html) and the segment\-level [query cache](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-cache.html).


Additionally, Elasticsearch executes all queries within the Java JVM, typically allocating half of the available physical RAM at startup, [up](https://www.elastic.co/guide/en/elasticsearch/guide/current/heap-sizing.html#compressed_oops) to a 32 GB heap size limit. This limit allows for memory\-efficient [object pointers](https://docs.oracle.com/javase/7/docs/technotes/guides/vm/performance-enhancements-7.html#compressedOop). Any remaining physical RAM beyond this limit is used indirectly for caching disk\-loaded data in the operating system’s page cache.


#### Limitations [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#limitations-1)


Query workloads [commonly](https://clickhouse.com/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#count-aggregations-in-clickhouse-and-elasticsearch) present in large\-scale data analytics and observability use cases almost always use `count(*)` and `count_distinct(...)` aggregations over billions of table rows


To reflect real\-world scenarios, most of our [benchmark queries](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#benchmark-queries) include `count(*)` aggregations, with `query ②` also incorporating a `count_distinct(...)` aggregation.


In Elasticsearch, `count(*)` aggregations are [approximate](https://clickhouse.com/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#elasticsearch) when the data spans multiple [shards](https://github.com/ClickHouse/examples/tree/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing#elasticsearch). Similarly, the ES\|QL [COUNT\_DISTINCT](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html#esql-count_distinct) aggregate function is also approximate, relying on the [HyperLogLog\+\+](https://static.googleusercontent.com/media/research.google.com/fr//pubs/archive/40671.pdf) algorithm.


In contrast, ClickHouse calculates fully accurate results for `count(*) aggregations`. Additionally, ClickHouse offers both [approximate](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/uniq#agg_function-uniq) and [exact](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/uniqexact) versions of the `count_distinct(...)` function. For `query ②`, we opted for the exact version to ensure precision.


The `time_us` JSON path in our [Bluesky test datasets](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#the-json-dataset---a-billion-bluesky-events) contains timestamps with microsecond precision. While Elasticsearch supports storing these timestamps in the [date\_nanos](https://www.elastic.co/guide/en/elasticsearch/reference/current/date_nanos.html) type, its ES\|QL [date and time functions](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html) only work with the [date](https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html) type, which has millisecond precision. As a workaround, we [store](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/config/filebeat.yml#L88) `time_us` in Elasticsearch as a `date` type with reduced precision.


ClickHouse [functions for working with dates and times](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions) can handle dates with nanosecond precision.


### DuckDB [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#duckdb)


[DuckDB](https://duckdb.org/) is a columnar analytical database designed for single\-node environments.


#### JSON support [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-support-3)


DuckDB introduced its JSON support in 2022 through the [JSON logical type](https://duckdb.org/docs/data/json/json_type.html).


#### JSON storage [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-storage-2)


DuckDB [is](https://www.youtube.com/watch?v=bZOvAKGkzpQ) a [columnar database](https://clickhouse.com/engineering-resources/what-is-columnar-database). However, unlike ClickHouse, DuckDB stores JSON data differently. In a DuckDB table with a JSON column, the ingested JSON documents are stored as plain strings rather than being decomposed or optimized for columnar storage:


![JSON-Benchmarks.015.png](/uploads/JSON_Benchmarks_015_08bf8f39b1.png)
DuckDB automatically [creates](https://duckdb.org/docs/guides/performance/indexing.html) [min\-max indexes](https://en.wikipedia.org/wiki/Block_Range_Index) for general\-purpose data type columns, storing the minimum and maximum values for each [row group](https://duckdb.org/docs/guides/performance/how_to_tune_workloads.html#the-effect-of-row-groups-on-parallelism) to accelerate filtering and aggregation queries.


It [also](https://duckdb.org/docs/guides/performance/indexing.html#art-indexes) generates [Adaptive Radix Tree (ART)](https://db.in.tum.de/~leis/papers/ART.pdf) indexes for columns with `PRIMARY KEY`, `FOREIGN KEY`, or `UNIQUE` constraints. ART indexes can be explicitly added to other columns but come with [limitations](https://duckdb.org/docs/guides/performance/indexing.html#art-indexes): they store a secondary data copy, and their effectiveness is limited to point queries or highly selective filters that target roughly 0\.1% or fewer of the rows.


#### Data compression [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#data-compression-1)


DuckDB automatically [applies](https://duckdb.org/docs/internals/storage.html#compression) [lightweight compression algorithms](https://duckdb.org/2022/10/28/lightweight-compression.html) to column data [based](https://www.youtube.com/watch?v=bZOvAKGkzpQ) on types, cardinality, and other factors.


#### Data sorting [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#data-sorting-2)


DuckDB documentation [recommends](https://duckdb.org/docs/guides/performance/indexing.html#the-effect-of-ordering-on-zonemaps) pre\-ordering data during insertion to group similar values, improving compression ratios and enhancing the [effectiveness](https://duckdb.org/docs/guides/performance/indexing.html#the-effect-of-ordering-on-zonemaps) of min\-max indexes. However, DuckDB does not provide automatic data ordering.


#### Caches [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#caches-3)


DuckDB relies on the operating system’s page cache and its [buffer manager](https://duckdb.org/2024/07/09/memory-management.html) to cache pages from its persistent storage.


### PostgreSQL [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#postgresql)


[PostgreSQL](https://www.postgresql.org/) is a well\-established [row\-oriented](https://clickhouse.com/engineering-resources/what-is-columnar-database#row-based-vs-column-based) relational database with first\-class JSON support. We chose it as a representative of row\-based systems to compare its performance and storage capabilities with modern column\-oriented databases like ClickHouse and DuckDB. That said, PostgreSQL is not designed for large\-scale analytical workloads like those tested in JSONBench and is not directly competitive with the other systems in this context.


#### JSON support [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-support-4)


PostgreSQL natively supports JSON data through its JSON and JSONB data types.


Introduced in PostgreSQL 9\.2 (2012\), the [JSON type](https://www.postgresql.org/docs/current/datatype-json.html) stores JSON documents as text, requiring processing functions to reparse the document on each execution, [similar](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#duckdb) to DuckDB’s current logical JSON type.


In 2014, PostgreSQL 9\.4 introduced the [JSONB type](https://www.postgresql.org/docs/current/datatype-json.html), which uses a decomposed binary format similar to MongoDB’s BSON. Due to its improved performance and functionality, JSONB is now the [recommended](https://www.postgresql.org/docs/current/datatype-json.html) option for working with JSON data in PostgreSQL.


#### JSON storage [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-storage-3)


PostgreSQL [is](https://www.postgresql.org/docs/8.1/storage.html) a [row\-based](https://clickhouse.com/engineering-resources/what-is-columnar-database#row-based-vs-column-based) data store and, therefore, stores ingested JSON documents as JSONB tuples sequentially on disk:


![JSON-Benchmarks.016.png](/uploads/JSON_Benchmarks_016_3b37162b4d.png)
Users can [create](https://www.postgresql.org/docs/current/sql-createindex.html) secondary indexes on specific JSON paths to speed up queries filtering on these paths. By [default](https://www.postgresql.org/docs/current/sql-createindex.html), PostgreSQL creates B\-Tree index data structures containing one entry for each ingested JSON document, where each B\-Tree entry stores the values of the indexed JSON paths within the corresponding document.


#### Index\-only scans [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#index-only-scans)


PostgreSQL supports [index\-only scans](https://www.postgresql.org/docs/current/indexes-index-only-scans.html) with B\-tree indexes, [similar](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#covered-index-scans) to MongoDB, for queries referencing only JSON paths stored in the index. However, this optimization is not automatic and [depends](https://www.postgresql.org/docs/current/indexes-index-only-scans.html) on the table’s data being stable, with rows marked as visible in the table’s `visibility map`. This allows the data to be read directly from the index without needing additional checks in the main table.


To verify if PostgreSQL’s query planner used index\-only scans for specific benchmark queries, you can examine the [query execution plans](https://github.com/ClickHouse/JSONBench/tree/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/_index_usage) that our benchmark tracks for PostgreSQL.


#### Data compression [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#data-compression-2)


PostgreSQL stores data row\-wise in 8\-kilobyte [pages](https://en.m.wikipedia.org/wiki/Page_(computer_memory)) on disk, aiming to fill each page with tuples. For optimal storage, tuples are ideally kept under 2 KB. Any tuple larger than 2 KB is processed using [TOAST](https://www.postgresql.org/docs/current/storage-toast.html), which [compresses](https://www.postgresql.org/docs/17/sql-createtable.html#SQL-CREATETABLE-PARMS-COMPRESSION) and splits the data into smaller chunks. Supported compression methods for TOASTed tuples [include](https://www.postgresql.org/docs/17/sql-createtable.html#SQL-CREATETABLE-PARMS-COMPRESSION) `pglz` and `lz4`, while tuples under 2 KB remain uncompressed.


#### Data sorting [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#data-sorting-3)


PostgreSQL supports [clustered tables](https://www.postgresql.org/docs/current/sql-cluster.html), where data is physically reordered based on the tuples of an index. However, unlike ClickHouse and Elasticsearch, PostgreSQL’s compression ratio does not improve with sorted table data. This is because, as explained above, compression is applied per tuple (only for tuples larger than 2 KB), regardless of data order. Additionally, PostgreSQL’s row\-based storage prevents colocating similar data within columns, which could otherwise enhance compression by grouping similar values together.


#### Caches [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#caches-4)


PostgreSQL uses internal caches to speed up data access, including caching [query execution plans](https://www.postgresql.org/docs/current/plpgsql-implementation.html#PLPGSQL-PLAN-CACHING) and [frequently accessed table and index data blocks](https://www.postgresql.org/docs/current/pgbuffercache.html). Like other benchmark candidates, it also leverages the operating system’s page cache. However, PostgreSQL does not provide a dedicated cache for query results.


## Benchmark setup [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#benchmark-setup)


Inspired by [ClickBench](https://benchmark.clickhouse.com/), we created [JSONBench](https://jsonbench.com/)—a fully reproducible benchmark you can set up and run on your own machine in minutes. Detailed instructions are available [here](https://github.com/ClickHouse/JSONBench/?tab=readme-ov-file#usage).


### Hardware and operating system [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#hardware-and-operating-system)


As a test machine per benchmark candidate, we used a dedicated AWS EC2 **m6i.8xlarge** instance with **32 CPU cores**, **128 GB RAM**, and a **10 TB gp3 volume**, running **Ubuntu Linux 24\.04 LTS**.


### Versions of evaluated systems [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#versions-of-evaluated-systems)


We benchmarked the following OSS version of different data stores with first\-class JSON support :


- ClickHouse 25\.1\.1
- MongoDB 8\.0\.3
- Elasticsearch 8\.17\.0
- DuckDB 1\.1\.3
- PostgreSQL 16\.6


### Measurements [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#measurements)


Our benchmark evaluates both **storage size** and **query performance**, testing each system with its **default data compression** setting as well as its **best available compression** option.


Depending on a candidate’s introspection capabilities, we also track:


- **Storage size of indexes**


	- [ClickHouse](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L19) example
	- [MongoDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/m6i.8xlarge_bluesky_1000m_zstd.json#L19) example
	- [PostgreSQL](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/m6i.8xlarge_bluesky_1000m_lz4.json#L19) example
- **Storage size of just the data** without indexes


	- [ClickHouse](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L17) example
	- [MongoDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/m6i.8xlarge_bluesky_1000m_zstd.json#L17) example
	- [PostgreSQL](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/m6i.8xlarge_bluesky_1000m_lz4.json#L17) example
- **Total storage size** (data \+ indexes)


	- [ClickHouse](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L15) example
	- [MongoDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/m6i.8xlarge_bluesky_1000m_zstd.json#L15) example
	- [Elasticsearch](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/m6i.8xlarge_bluesky_no_source_1000m_best_compression.json#L15) example
	- [DuckDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/m6i.8xlarge_bluesky_1000m.json#L15) example
	- [PostgreSQL](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/m6i.8xlarge_bluesky_1000m_lz4.json#L15) example
- **Query execution plans** for all queries (to introspect **index usage**, etc.)


	- ClickHouse [logical plans](https://github.com/ClickHouse/JSONBench/tree/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/_index_usage), [physical plans](https://github.com/ClickHouse/JSONBench/tree/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/_physical_query_plans) examples
	- [MongoDB](https://github.com/ClickHouse/JSONBench/tree/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/_index_usage) examples
	- [DuckDB](https://github.com/ClickHouse/JSONBench/tree/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/_physical_query_plans) examples
	- [PostgreSQL](https://github.com/ClickHouse/JSONBench/tree/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/_index_usage) examples
- **Peak memory usage per query**


	- [ClickHouse](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L36) example


## Benchmark queries [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#benchmark-queries)


For each benchmark candidate, we test the [cold and hot performance](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#cold-and-hot-query-runtimes) of 5 typical analytical queries running sequentially over the [8 configured datasets](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#the-json-dataset---a-billion-bluesky-events).


We formulated these queries in SQL for ClickHouse, DuckDB, and PostgreSQL, and we used equivalent [aggregation pipeline](https://www.mongodb.com/docs/manual/aggregation/#std-label-aggregation-pipeline-intro) queries for MongoDB and equivalent [ES\|QL](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html) queries for Elasticsearch. As proof that these queries are equivalent, we also add links to the results for running these queries over the 1 million JSON documents dataset (as the 1 million JSON docs [data quality](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#approximate-dataset-counts-are-allowed) is at [100% for all systems](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwIiwibWV0cmljIjoicXVhbGl0eSIsInF1ZXJpZXMiOlt0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWVdfQ==)) :


#### Query ① \- Top Bluesky event types [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#query----top-bluesky-event-types)


- [ClickHouse](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/queries_formatted.sql#L2) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/_query_results/_m6i.8xlarge_bluesky_1m_lz4.query_results#L2)
- [MongoDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/queries_formatted.js#L2) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/_query_results/_m6i.8xlarge_bluesky_1m_snappy.query_results#L2)
- [Elasticsearch](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/queries_formatted.txt#L1) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/_query_results/_m6i.8xlarge_bluesky-no_source_best_compression-1m.query_results#L2)
- [DuckDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/queries_formatted.sql#L2) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/_query_results/_m6i.8xlarge_bluesky_1m.query_results#L2)
- [PostgreSQL](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/queries_formatted.sql#L2) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/_query_results/_m6i.8xlarge_bluesky_1m_lz4.query_results#L2)


#### Query ② \- Top Bluesky event types with unique users per event type [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#query----top-bluesky-event-types-with-unique-users-per-event-type)


- [ClickHouse](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/queries_formatted.sql#L12) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/_query_results/_m6i.8xlarge_bluesky_1m_lz4.query_results#L22)
- [MongoDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/queries_formatted.js#L17) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/_query_results/_m6i.8xlarge_bluesky_1m_snappy.query_results#L67)
- [Elasticsearch](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/queries_formatted.txt#L10) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/_query_results/_m6i.8xlarge_bluesky-no_source_best_compression-1m.query_results#L23)
- [DuckDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/queries_formatted.sql#L12) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/_query_results/_m6i.8xlarge_bluesky_1m.query_results#L27)
- [PostgreSQL](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/queries_formatted.sql#L12) version\+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/_query_results/_m6i.8xlarge_bluesky_1m_lz4.query_results#L24)


#### Query ③ \- When do people use BlueSky [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#query----when-do-people-use-bluesky)


- [ClickHouse](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/queries_formatted.sql#L25) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/_query_results/_m6i.8xlarge_bluesky_1m_lz4.query_results#L40)
- [MongoDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/queries_formatted.js#L47) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/_query_results/_m6i.8xlarge_bluesky_1m_snappy.query_results#L150)
- [Elasticsearch](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/queries_formatted.txt#L20) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/_query_results/_m6i.8xlarge_bluesky-no_source_best_compression-1m.query_results#L42)
- [DuckDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/queries_formatted.sql#L25) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/_query_results/_m6i.8xlarge_bluesky_1m.query_results#L50)
- [PostgreSQL](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/queries_formatted.sql#L25) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/_query_results/_m6i.8xlarge_bluesky_1m_lz4.query_results#L44)


#### Query ④ \- Top 3 post veterans [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#query----top-3-post-veterans)


- [ClickHouse](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/queries_formatted.sql#L39) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/_query_results/_m6i.8xlarge_bluesky_1m_lz4.query_results#L48)
- [MongoDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/queries_formatted.js#L85) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/_query_results/_m6i.8xlarge_bluesky_1m_snappy.query_results#L176)
- [Elasticsearch](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/queries_formatted.txt#L30) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/_query_results/_m6i.8xlarge_bluesky-no_source_best_compression-1m.query_results#L51)
- [DuckDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/queries_formatted.sql#L40) version \+  [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/_query_results/_m6i.8xlarge_bluesky_1m.query_results#L61)
- [PostgreSQL](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/queries_formatted.sql#L39) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/_query_results/_m6i.8xlarge_bluesky_1m_lz4.query_results#L54)


#### Query ⑤ \- Top 3 users with the longest activity span [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#query----top-3-users-with-the-longest-activity-span)


- [ClickHouse](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/queries_formatted.sql#L53) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/_query_results/_m6i.8xlarge_bluesky_1m_lz4.query_results#L56)
- [MongoDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/queries_formatted.js#L117) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/_query_results/_m6i.8xlarge_bluesky_1m_snappy.query_results#L193)
- [Elasticsearch](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/queries_formatted.txt#L41) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/_query_results/_m6i.8xlarge_bluesky-no_source_best_compression-1m.query_results#L60)
- [DuckDB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/queries_formatted.sql#L55) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/_query_results/_m6i.8xlarge_bluesky_1m.query_results#L72)
- [PostgreSQL](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/queries_formatted.sql#L56) version \+ [result](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/_query_results/_m6i.8xlarge_bluesky_1m_lz4.query_results#L64)


## Benchmark methodology [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#benchmark-methodology)


In this blog post, we analyzed and compared the storage size of **up to 1 billion ingested Bluesky JSON documents** and the query performance of **five typical analytical queries executed sequentially** on the ingested data.


The evaluation was performed on **five different open\-source data stores**, each operating on a **single node**, following a well\-defined methodology, which we describe below.


### No tuning [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#no-tuning)


Similar to [ClickBench](https://github.com/ClickHouse/ClickBench?tab=readme-ov-file#installation-and-fine-tuning), we use all systems in standard configuration without applying any fine\-tuning measures.


An exception was MongoDB, where we initially got an exception for running [query ②](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/queries_formatted.js#L17):



```
MongoServerError[ExceededMemoryLimit]: PlanExecutor error during aggregation :: caused by :: Used too much memory for a single array. Memory limit: 104857600. Current set has 2279516 elements and is 104857601 bytes.

```

The issue arose due to the [$addToSet](https://www.mongodb.com/docs/manual/reference/operator/aggregation/addToSet/) operator, used as a [workaround](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#limitations) for the missing `COUNT DISTINCT` operator in MongoDB. By default, this operator has a 100 MB limit for the size of in\-memory sets (implemented as arrays), which was exceeded during query execution. To address this, we [increased](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/run_queries.sh#L24) the `internalQueryMaxAddToSetBytes` value.


Additionally, to follow [best practices](https://www.mongodb.com/docs/manual/core/query-optimization/#performance)—similar to the [MongoDB setup in ClickBench](https://github.com/ClickHouse/ClickBench/blob/96994da9b0cd61b04e543224dd89c9de32486415/mongodb/benchmark.sh#L14)—we [enabled](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/run_queries.sh#L36) the [internalQueryPlannerGenerateCoveredWholeIndexScans](https://github.com/mongodb/mongo/blob/8a2f52590d92482624723086b88151c93ee56f1c/src/mongo/db/query/query_knobs.idl?utm_source=chatgpt.com#L285) setting. This allows the query planner to generate [covered index scans](https://staging.clickhouse.com/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#covered-index-scans), ensuring that all five benchmark queries in MongoDB are covered queries. Consequently, the reported query runtimes represent lower bounds, as runtimes without this optimization were significantly slower.


### No query results cache [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#no-query-results-cache)


When query result caches are enabled, systems like Elasticsearch and ClickHouse can instantly serve results by fetching them directly from the cache. While this is efficient, it doesn’t provide meaningful performance insights for our benchmark. To ensure consistency, we disable or clear query result caches after each execution.


### No extracted top\-level fields [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#no-extracted-top-level-fields)


Our goal is to focus solely on testing the performance of JSON data types across different systems. To ensure consistency, each tested system and data configuration is restricted to using a table\* with only a single field of the system’s respective JSON type.


[In](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/ddl_zstd.sql#L1) **ClickHouse**\*\*:



```

```
1CREATE TABLE bluesky (
2    data JSON
3) ORDER BY();
```


```

[In](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/ddl.sql#L1) **DuckDB**:



```

```
1CREATE TABLE bluesky (
2    data JSON
3);
```


```

[In](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/ddl_lz4.sql#L1) **PostgreSQL**:



```

```
1CREATE TABLE bluesky (
2    data JSONB
3);
```


```

\*While we focus on testing JSON data types across different systems, it’s important to note that MongoDB and Elasticsearch are not relational databases and handle JSON data differently.


[In](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/config/index_template_no_source_best_compression.json#L2) **Elasticsearch,** all JSON path leaf values are automatically stored in [multiple data structures](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-storage-and-data-compression) to accelerate query performance.


[In](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/ddl_zstd.js#L1) **MongoDB,** all documents are natively [stored](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-storage-1) as BSON documents, optimized for its document\-based architecture.


\*\*In the linked ClickHouse DDL file, specific JSON paths are defined as primary key columns with necessary type hints provided in the JSON type clause. This differs from systems like DuckDB and PostgreSQL, which use secondary indexes for similar purposes, defined outside the CREATE TABLE statement. See the next section below.


### Some JSON paths can be used for indexes and data sorting [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#some-json-paths-can-be-used-for-indexes-and-data-sorting)


To accelerate the benchmark queries, each system can create an index on the following JSON paths:


- **kind**: the kind path largely [dictates](https://clickhouse.com/blog/building-a-medallion-architecture-for-bluesky-json-data-with-clickhouse) the subsequent structure delivering `commit`, `identity`, and `account` event types
- **commit.operation**: in case of `commit` events \- is it an `create`, `delete`, or `update` event
- **commit.collection**: in case of `commit` events \- the specific Bluesky event, e.g., `post`, `repost`, `like`, etc.
- **did**: the `ID of the Bluesky user` causing the event
- **time\_us**: to simplify handling the [inconsistent path structure](https://clickhouse.com/blog/building-a-medallion-architecture-for-bluesky-json-data-with-clickhouse#challenges-with-bluesky-data) for the Bluesky timestamps, we assume this to be the `event timestamp`, although it is the [time when we scraped the event](https://clickhouse.com/blog/building-a-medallion-architecture-for-bluesky-json-data-with-clickhouse#reading-bluesky-data) from the Bluesky API


In all benchmarked systems except DuckDB and Elasticsearch, we created a single compound index over all aforementioned paths, ordered by cardinality from lowest to highest:



```

```
1(kind, commit.operation, commit.collection, did, time_us)
```


```

[In](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/ddl_zstd.sql#L10) **ClickHouse**, we use a corresponding primary key / sorting key for [creating](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#data-sorting-and-compression) the index:



```

```
1ORDER BY (
2    data.kind,
3    data.commit.operation,
4    data.commit.collection,
5    data.did,
6    fromUnixTimestamp64Micro(data.time_us));
```


```

[In](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/ddl_snappy.js#L6) **MongoDB**, we create a secondary index:



```

```
1db.bluesky.createIndex({
2    "kind": 1,
3    "commit.operation": 1,
4    "commit.collection": 1,
5    "did": 1,
6    "time_us": 1});
```


```

[In](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/ddl_lz4.sql#L5) **PostgreSQL**, we create a secondary index as well:



```

```
1CREATE INDEX idx_bluesky
2ON bluesky (
3    (data ->> 'kind'),
4    (data -> 'commit' ->> 'operation'),
5    (data -> 'commit' ->> 'collection'),
6    (data ->> 'did'),
7    (TO_TIMESTAMP((data ->> 'time_us')::BIGINT / 1000000.0))
8);
```


```

For **DuckDB**, our benchmark queries wouldn’t benefit from the [available index types](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-storage-2), plus, DuckDB doesn’t provide any automatic data sorting.


**Elasticsearch** lacks secondary indexes but automatically stores all JSON path leaf values across [various data structures](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-storage-and-data-compression) to optimize query performance. However, we [use](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/config/index_template_no_source_best_compression.json#L28) the listed JSON paths for [index sorting](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-index-sorting.html), which, as [previously explained](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#data-sorting-1), can greatly improve compression ratios for the on\-disk storage of `stored fields` and `doc_values`.


#### We enable index\-only scans for MongoDB and PostgreSQL [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#we-enable-index-only-scans-for-mongodb-and-postgresql)


Most of our [benchmark queries](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#benchmark-queries) filter on `kind`, `commit.operation`, and `commit.collection` (all three paths within a single query), leveraging the inclusion of these paths in a single compound index.


While `did` and `time_us` are not used as filters in any query, we included them in the index to support index\-only scans in [MongoDB](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#covered-index-scans) and [PostgreSQL](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#index-only-scans), as their query planners rely on these fields being indexed. Additionally, we included `did` and `time_us` in the ClickHouse index to better illustrate differences in disk size between data and indexes.


#### We track query execution plans for validating index usage [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#we-track-query-execution-plans-for-validating-index-usage)


As noted [earlier](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#measurements), we analyze query execution plans based on each system’s introspection capabilities to ensure our benchmark queries effectively use the specified indexes across all candidates.


### Approximate dataset counts are allowed [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#approximate-dataset-counts-are-allowed)


When working with large\-scale JSON datasets, it’s not uncommon for some systems to encounter parsing issues with certain documents. These issues can arise from differences in JSON implementations, edge cases in document formatting, or other unexpected data characteristics.


For this benchmark, we decided that achieving a perfect 100% load rate is unnecessary. Instead, as long as the total number of successfully ingested documents approximately matches the dataset size, the results remain valid for performance and storage comparisons.


In our results, we track the benchmarked dataset size (`dataset_size` field) and the achieved number of loaded documents (`num_loaded_documents` field).


As an example, these are the number of successfully loaded Bluesky JSON documents across all systems for the **1 billion documents** dataset:


- ClickHouse: [999\.999\.258](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L13)
- MongoDB: [893\.632\.990](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/m6i.8xlarge_bluesky_1000m_zstd.json#L13)
- Elasticsearch: [999\.998\.998](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/m6i.8xlarge_bluesky_no_source_1000m_best_compression.json#L13)
- DuckDB: [974\.400\.000](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/m6i.8xlarge_bluesky_1000m.json#L13C27-L13C36)
- PostgreSQL: [804\.000\.000](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/m6i.8xlarge_bluesky_1000m_lz4.json#L13)


In our [JSONBench online dashboard](https://jsonbench.com/), we track the number of successfully loaded Bluesky JSON documents per system as a `Data Quality` metric. Here are the tracked data qualities for the datasets with [1 million](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwIiwibWV0cmljIjoicXVhbGl0eSIsInF1ZXJpZXMiOlt0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWVdfQ==), [10 million](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwMCIsIm1ldHJpYyI6InF1YWxpdHkiLCJxdWVyaWVzIjpbdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlXX0=), [100 million](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwMDAiLCJtZXRyaWMiOiJxdWFsaXR5IiwicXVlcmllcyI6W3RydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZV19), and [1 billion](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwMDAwIiwibWV0cmljIjoicXVhbGl0eSIsInF1ZXJpZXMiOlt0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWVdfQ==) Bluesky JSON documents.


We welcome pull requests to improve document loading methods and minimize parsing issues across systems.


### Cold and hot query runtimes [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#cold-and-hot-query-runtimes)


As with [ClickBench](https://github.com/ClickHouse/ClickBench?tab=readme-ov-file#results-usage-and-scoreboards), we execute each benchmark query three times on every system and data configuration, representing a cold and hot run The runtime of the first run is recorded as the `cold runtime`, while the `hot runtime` is determined as the minimum of the second and third runs.


Before the first run, we clear the OS\-level page cache (for example, [see](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/run_queries.sh#L16C5-L16C40) this process for ClickHouse).


## Benchmark results [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#benchmark-results)


It’s time to dive into the benchmark results—the moment you’ve been waiting for! Following the methodology outlined above, we present the **findings for the 1 billion JSON documents dataset**, focusing on realistic data sizes.


For simplicity and relevance, we only showcase results where data was compressed using the **best available compression option** for each system. This choice not only makes comparisons more straightforward—given that most systems use the same `zstd` algorithm—but also aligns with real\-world Petabyte\-scale scenarios where compression plays a crucial role in reducing storage costs.


We’ve omitted results for the smaller datasets to avoid repetition and because such sizes are less relevant. Platforms like Bluesky, for instance, can generate millions of events per second, making smaller datasets a bit unrealistic.



> For those interested, all results—including those for default compression options and smaller datasets—are available at our [JSONBench online dashboard](https://jsonbench.com/), allowing you to analyze and compare results for all systems conveniently:
> 
> 
> - 1 million JSON docs: [storage sizes](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwIiwibWV0cmljIjoic2l6ZSIsInF1ZXJpZXMiOlt0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWVdfQ==), [cold runtimes](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwIiwibWV0cmljIjoiY29sZCIsInF1ZXJpZXMiOlt0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWVdfQ==), [hot runtimes](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwIiwibWV0cmljIjoiaG90IiwicXVlcmllcyI6W3RydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZV19)
> - 10 million JSON docs: [storage sizes](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwMCIsIm1ldHJpYyI6InNpemUiLCJxdWVyaWVzIjpbdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlXX0=), [cold runtimes](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwMCIsIm1ldHJpYyI6ImNvbGQiLCJxdWVyaWVzIjpbdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlXX0=), [hot runtimes](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwMCIsIm1ldHJpYyI6ImhvdCIsInF1ZXJpZXMiOlt0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWVdfQ==)
> - 100 million JSON docs: [storage sizes](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwMDAiLCJtZXRyaWMiOiJzaXplIiwicXVlcmllcyI6W3RydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZV19), [cold runtimes](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwMDAiLCJtZXRyaWMiOiJjb2xkIiwicXVlcmllcyI6W3RydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZV19), [hot runtimes](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwMDAiLCJtZXRyaWMiOiJob3QiLCJxdWVyaWVzIjpbdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlXX0=)
> - 1 billion JSON docs: [storage sizes](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwMDAwIiwibWV0cmljIjoic2l6ZSIsInF1ZXJpZXMiOlt0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWVdfQ==), [cold runtimes](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwMDAwIiwibWV0cmljIjoiY29sZCIsInF1ZXJpZXMiOlt0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWVdfQ==), [hot runtimes](https://jsonbench.com/#eyJzeXN0ZW0iOnsiQ2xpY2tIb3VzZSAobHo0KSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoenN0ZCkiOnRydWUsIkR1Y2tEQiI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBiZXN0IGNvbXByZXNzaW9uKSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAobm8gc291cmNlLCBkZWZhdWx0KSI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAoYmVzdCBjb21wcmVzc2lvbikiOnRydWUsIkVsYXN0aWNzZWFyY2ggKGRlZmF1bHQpIjp0cnVlLCJFbGFzdGljc2VhcmNoIjp0cnVlLCJNb25nb0RCIChzbmFwcHksIGNvdmVyZWQgaW5kZXgpIjp0cnVlLCJNb25nb0RCICh6c3RkLCBjb3ZlcmVkIGluZGV4KSI6dHJ1ZSwiTW9uZ29EQiAoc25hcHB5KSI6dHJ1ZSwiTW9uZ29EQiAoenN0ZCkiOnRydWUsIlBvc3RncmVTUUwgKGx6NCkiOnRydWUsIlBvc3RncmVTUUwgKHBnbHopIjp0cnVlfSwic2NhbGUiOiIxMDAwMDAwMDAwIiwibWV0cmljIjoiaG90IiwicXVlcmllcyI6W3RydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZV19)


The following presents the [total](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#measurements) storage sizes and analytical query performances for the `1 billion JSON documents` dataset ingested with the system’s `best available compression` option.


### Storage sizes with the best possible compression [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#storage-sizes-with-the-best-possible-compression)


![JSON-Benchmarks.017.png](/uploads/JSON_Benchmarks_017_1e36137288.png)
We will analyze the storage sizes represented in the diagram above, moving sequentially from left to right across the seven bars.


The [Bluesky](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#the-json-dataset---a-billion-bluesky-events) **JSON files** occupy [482 GB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/_files_json/results/_files_bluesky_json_1000m.json#L13) of disk space in uncompressed form, which reduces to [124 GB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/_files_zstd/results/_files_bluesky_zstd_1000m.json#L13) when compressed with `zstd`.


Ingesting these files into **ClickHouse** with `zstd` compression [configured](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/ddl_zstd.sql#L8) results in a total disk size of [99 GB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L15).



> Notably, ClickHouse stores the data smaller than the source files compressed with the same algorithm. As explained [above](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-storage), ClickHouse optimizes storage by storing the values of each unique JSON path as native columns and compressing each column individually. Additionally, when a primary key [is](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#data-sorting-and-compression) used, similar data is grouped per column and sorted, further enhancing the compression rate.


**MongoDB** with `zstd` compression [enabled](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/ddl_zstd.js#L3), requires [158 GB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/m6i.8xlarge_bluesky_1000m_zstd.json#L16) of disk space for storing the JSON data, 40% more than ClickHouse.


**Elasticsearch** was [configured as fairly as possible](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#configuring-elasticsearch-for-fair-storage-comparison) for our benchmark scenario. Without `_source`, Elasticsearch needs [220 GB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/m6i.8xlarge_bluesky_no_source_1000m_best_compression.json#L16) of disk space with [configured](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/config/index_template_no_source_best_compression.json#L12) `zstd` compression, more than twice as much as ClickHouse needs.


As [previously](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#json-storage-and-data-compression) explained, the configured compression algorithm is applied only to `stored fields` like `_source`. Consequently, it becomes ineffective when `_source` is disabled. This can be verified by comparing the [data size](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/m6i.8xlarge_bluesky_no_source_1000m_default_compression.json#L16) for the same Elasticsearch configuration using `lz4` compression.


In case `_source` is [required](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#the-role-of-_source) (e.g. in the OSS version where the enterprise tier `synthetic _source` is not available), we also measured the needed disk space with everything configured as explained above, but with `_source` enabled: [360 GB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/m6i.8xlarge_bluesky_source_1000m_best_compression.json#L16), more than three times more than ClickHouse. With `_source`, using the default `lz4` compression results in higher disk space usage of [455 GB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/m6i.8xlarge_bluesky_source_1000m_default_compression.json#L16).


**DuckDB** has [no](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#data-compression-1) compression algorithm option but automatically applies lightweight compression algorithms. The ingested JSON documents use [472 GB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/m6i.8xlarge_bluesky_1000m.json#L16) of disk space, almost five times more than ClickHouse.


**PostgreSQL** applies compression [only](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#data-compression-2) on “too large” tuples and only per tuple. If almost all tuples, like in our dataset, are below the threshold, the compression is ineffective. With the best available `lz4` compression, the disk space required for storing the ingested JSON data is [622 GB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/m6i.8xlarge_bluesky_1000m_lz4.json#L16), almost identical to the disk space [needed](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/m6i.8xlarge_bluesky_1000m_pglz.json#L16) with the default `pglz` option and over 6 times more than ClickHouse.


Next, we will present the runtimes for running our benchmark queries for each system over this ingested JSON data.


### Aggregation performance of query ① [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#aggregation-performance-of-query-)


This diagram shows the [cold and hot runtimes](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#cold-and-hot-query-runtimes) for running benchmark [query ①](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#query--top-bluesky-event-types) over the 1 billion JSON documents dataset, stored in each system with the best available compression option. Query ① performs a `count` aggregation over the full dataset to calculate the most popular Bluesky event types.


![JSON-Benchmarks.018.png](/uploads/JSON_Benchmarks_018_4572dccd94.png)
We will analyze the runtimes represented in the diagram sequentially from left to right across the 5 sections.


**ClickHouse** runs query ① in [405 milliseconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L29) cold and [394 milliseconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L29) hot. This is a data processing throughput of 2\.47 billion and 2\.54 billion JSON documents per second. For ClickHouse, we could also [track](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#measurements) the query’s peak memory usage per query run, which is [less than 3 MB](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L43) for cold and hot runs.


For **MongoDB**, we enabled [covered index scans](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#covered-index-scans) for all benchmark queries. With that, MongoDB runs query ① in [\~ 16 minutes](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/m6i.8xlarge_bluesky_1000m_zstd.json#L29) cold and hot, which is \~2500 times slower than ClickHouse. With covered index scans, all the data required for the query already resides in memory as part of the index, eliminating the need to load any data from disk. As a result, cold and hot runtimes are virtually identical.


For completeness, we also list the MongoDB runtime for query ① without covered index scans: [\~ 28 minutes](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results_without_covered_index_scans/m6i.8xlarge_bluesky_1000m_zstd.json#L29) cold and hot, 4200 times slower than ClickHouse.


**Elasticsearch** runs the ES\|QL version of query ① in [\~ 5 seconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/m6i.8xlarge_bluesky_no_source_1000m_best_compression.json#L18) cold and hot, 12 times slower than ClickHouse.


**DuckDB** has a runtime of [\~ 1 hour](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/m6i.8xlarge_bluesky_1000m.json#L25) cold and hot for query ①, 9 thousand times slower than ClickHouse.


**PostgreSQL** needs [\~ 1 hour](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/m6i.8xlarge_bluesky_1000m_lz4.json#L29) cold and hot for query ① as well. This is 9 thousand times slower than ClickHouse too.



> ​​**DuckDB** and **PostgreSQL** struggle significantly with JSON data at the billion\-document scale, consistently showing extremely long query execution times. This issue occurs across all five benchmark queries. All systems were tested on the same hardware with default configurations. While we haven’t yet investigated potential bottlenecks, we welcome input or pull requests from experts.


### Aggregation performance of query ② [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#aggregation-performance-of-query--1)


[Query ②](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#query--top-bluesky-event-types-with-unique-users-per-event-type) extends query ① with a filter and an additional `count_distinct` aggregation to annotate the result from query ① with the count of unique users per popular Bluesky event.


![JSON-Benchmarks.019.png](/uploads/JSON_Benchmarks_019_8712fddefd.png)
**ClickHouse** runs query ② in [11\.85 seconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L30) (cold) and [5\.63 seconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L30) (hot). This is:


- 3800 times faster than **MongoDB** ([\~ 6 hours](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/m6i.8xlarge_bluesky_1000m_zstd.json#L30) cold, hot).
- 7000 times faster than **MongoDB** without covered index scan ([\~ 11 hours](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results_without_covered_index_scans/m6i.8xlarge_bluesky_1000m_zstd.json#L30) cold, hot)
- 8 times faster than **Elasticsearch** ([51\.49 seconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/m6i.8xlarge_bluesky_no_source_1000m_best_compression.json#L19) cold, [45\.51 seconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/m6i.8xlarge_bluesky_no_source_1000m_best_compression.json#L19) hot).
- 640 times faster than **DuckDB** ([\~ 1 hour](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/m6i.8xlarge_bluesky_1000m.json#L26) cold and hot)
- 5700 times faster than **PostgreSQL** ([\~ 9 hours](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/m6i.8xlarge_bluesky_1000m_lz4.json#L30) cold and hot)


### Aggregation performance of query ③ [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#aggregation-performance-of-query--2)


[Query ③](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#query--when-do-people-use-bluesky) extracts the hour\-of\-the\-day component from the event timestamps and groups the dataset by it for calculating during which hours of the day specific Bluesky events are most popular.


![JSON-Benchmarks.020.png](/uploads/JSON_Benchmarks_020_4c4fcd7d08.png)
**ClickHouse** runs query ③ in [28\.90 seconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L31) (cold) and [2\.47 seconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L31) (hot). This is:


- 480 times faster than **MongoDB** ([\~ 20 minutes](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/m6i.8xlarge_bluesky_1000m_zstd.json#L31) cold, hot).
- 2100 times faster than **MongoDB** without covered index scan ([\~ 1\.5 hours](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results_without_covered_index_scans/m6i.8xlarge_bluesky_1000m_zstd.json#L31) cold, hot)
- 16 times faster than **Elasticsearch** ([\~ 41 seconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/m6i.8xlarge_bluesky_no_source_1000m_best_compression.json#L20) cold, hot).
- 1400 times faster than **DuckDB** ([\~ 1 hour](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/m6i.8xlarge_bluesky_1000m.json#L27) cold and hot)
- 1400 times faster than **PostgreSQL** ([\~ 1 hour](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/m6i.8xlarge_bluesky_1000m_lz4.json#L31) cold and hot)


### Aggregation performance of query ④ [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#aggregation-performance-of-query--3)


[Query ④](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#query--top-3-post-veterans) performs a `min` aggregation on the dataset to query for the top 3 post veterans i.e. the 3 BlueSky users with the oldest posts.


![JSON-Benchmarks.021.png](/uploads/JSON_Benchmarks_021_2ec0abac90.png)
**ClickHouse** runs query ④ in [5\.38 seconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L32) (cold) and [596 milliseconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L32) (hot). This is:


- 270 times faster than **MongoDB** ([\~ 2\.7 minutes](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/m6i.8xlarge_bluesky_1000m_zstd.json#L32) cold, hot).
- 2800 times faster than **MongoDB** without covered index scan ([\~ 28 minutes](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results_without_covered_index_scans/m6i.8xlarge_bluesky_1000m_zstd.json#L32) cold, hot)
- 14 times faster than **Elasticsearch** ([8\.81 seconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/m6i.8xlarge_bluesky_no_source_1000m_best_compression.json#L21) cold, hot).
- 6000 times faster than **DuckDB** ([\~ 1 hour](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/m6i.8xlarge_bluesky_1000m.json#L28) cold and hot)
- 10000 times faster than **PostgreSQL** ([\~ 1\.75 hours](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/m6i.8xlarge_bluesky_1000m_lz4.json#L32) cold and hot)


### Aggregation performance of query ⑤ [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#aggregation-performance-of-query--4)


[Query ⑤](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#query--top-3-users-with-the-longest-activity-span) returns the top 3 users with the longest activity span on Bluesky by running a `date_diff` aggregation.


![JSON-Benchmarks.022.png](/uploads/JSON_Benchmarks_022_f10b5ed242.png)
**ClickHouse** runs query ⑤ in [5\.41 seconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L33) (cold) and [637 milliseconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/clickhouse/results/m6i.8xlarge_bluesky_1000m_zstd.json#L33) (hot). This is:


- 260 times faster than **MongoDB** ([2\.76 minutes](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results/m6i.8xlarge_bluesky_1000m_zstd.json#L33) cold, hot).
- 2600 times faster than **MongoDB** without covered index scan ([\~ 28 minutes](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/mongodb/results_without_covered_index_scans/m6i.8xlarge_bluesky_1000m_zstd.json#L33) cold, hot)
- 15 times faster than **Elasticsearch** ([\~ 9\.5 seconds](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/elasticsearch/results/m6i.8xlarge_bluesky_no_source_1000m_best_compression.json#L22) cold, hot).
- 5600 times faster than **DuckDB** ([\~ 1 hour](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/duckdb/results/m6i.8xlarge_bluesky_1000m.json#L29) cold and hot)
- 9900 times faster than **PostgreSQL** ([\~ 1\.75 hours](https://github.com/ClickHouse/JSONBench/blob/c7afa7078aed72c55ff4441a2da635424fde7724/postgresql/results/m6i.8xlarge_bluesky_1000m_lz4.json#L33) cold and hot)


## Summary [\#](/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql#summary)


In our benchmark, ClickHouse consistently outperformed all other tested data stores with JSON support, both in storage efficiency and query performance.


For analytical queries, it’s not just faster — it’s thousands of times faster than leading JSON data stores like MongoDB, thousands of times faster than DuckDB and PostgreSQL, and orders of magnitude faster than Elasticsearch. ClickHouse achieves this level of performance while maintaining storage efficiency — JSON documents in ClickHouse are even more compact than compressed files on disk, resulting in lower cost of ownership for large\-scale analytical use cases.


Using the ClickHouse [native JSON data type](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse) gives you the best of both worlds – fast analytical queries and optimal compression on disk, without requiring upfront schema design and refinement. This makes ClickHouse an unparalleled general\-purpose JSON data store—especially for use cases, where events are often in JSON format and cost efficiency and analytical query performance are critical, such as [SQL\-based observability](https://clickhouse.com/blog/evolution-of-sql-based-observability-with-clickhouse).


We hope this post has been an insightful exploration of the features and performance of popular data stores with first\-class JSON support. If you would like to get involved, we warmly invite you to contribute to [JSONBench](https://github.com/ClickHouse/JSONBench/), our open\-source JSON benchmark—whether by refining existing system benchmarks or adding new candidates to the mix and taking on [The Billion Docs JSON Challenge](https://jsonbench.com/)! 🥊

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
