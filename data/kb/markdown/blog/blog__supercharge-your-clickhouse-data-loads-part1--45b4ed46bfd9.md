# Supercharging your large ClickHouse data loads \- Part 1: Performance and resource usage factors


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Supercharging your large ClickHouse data loads \- Part 1: Performance and resource usage factors

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber)Sep 19, 2023 · 16 minutes read![header.png](/uploads/header_d0211623d1.png)
This blog post is part of the `Supercharging your large ClickHouse data loads` series:


- [Tuning a large data load for speed](/blog/supercharge-your-clickhouse-data-loads-part2)
- [Making a large data load resilient](/blog/supercharge-your-clickhouse-data-loads-part3)


## Introduction [\#](/blog/supercharge-your-clickhouse-data-loads-part1#introduction)


ClickHouse is [designed](https://clickhouse.com/docs/en/faq/general/why-clickhouse-is-so-fast) to be fast and resource\-efficient. If you let it, ClickHouse can utilize the hardware it runs on up to the theoretical limits and load data blazingly [fast](https://twitter.com/clickhousedb/status/1702719310945255559?s=46&t=EzUAGZ5p_COplqQSe0ADbg). Or you can reduce the resource usage of large data loads. Depending on what you want to achieve. In this three\-part blog series, we will provide the necessary knowledge plus guidance, and best practices to achieve both resiliency and speed for your large data loads. This first part lays the foundation by describing the basic data insert mechanics in ClickHouse and its three main factors for controlling resource usage and performance. In a [second post](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part2), we will go on a race track and tune the speed of a large data load to the max. In the final closing part of this series, we will discuss measures for making your large data loads robust and resilient against transient issues like network interruptions.


Let's start with exploring the basic ClickHouse data insert mechanics.


## Data insert mechanics [\#](/blog/supercharge-your-clickhouse-data-loads-part1#data-insert-mechanics)


The following diagram sketches the general mechanics of a data insert into a ClickHouse table of the [MergeTree engine](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family) family:
![large_data_loads-p1-01.png](/uploads/large_data_loads_p1_01_c741aed514.png)
The server receives some data portion (e.g., from an [insert query](https://clickhouse.com/docs/en/sql-reference/statements/insert-into)), and ① forms ([at least](/blog/supercharge-your-clickhouse-data-loads-part1#when-the-server-forms-the-blocks)) one in\-memory insert [block](https://clickhouse.com/docs/en/development/architecture#block) ([per](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse#poorly-chosen-partitioning-key) partitioning key) from the received data. The block’s data is [sorted](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes#data-is-stored-on-disk-ordered-by-primary-key-columns), and table engine\-specific [optimizations](https://www.youtube.com/watch?v=QDAJTKZT8y4&t=428s) are [applied](https://clickhouse.com/docs/en/operations/settings/settings#optimize-on-insert). Then the data is [compressed](https://clickhouse.com/docs/en/about-us/distinctive-features#data-compression) and ② written to the database storage in the form of a new data [part](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree#mergetree-data-storage).


Note that there are also [cases](/blog/supercharge-your-clickhouse-data-loads-part1#when-the-client-forms-the-blocks) where the client forms the insert blocks instead of the server.


Three main factors influence the performance and resource usage of ClickHouse’s data insert mechanics: **Insert block size**, **Insert parallelism** and **Hardware size**. We will discuss these factors and the ways to configure them in the remainder of this post.


## Insert block size [\#](/blog/supercharge-your-clickhouse-data-loads-part1#insert-block-size)


### Impact on performance and resource usage [\#](/blog/supercharge-your-clickhouse-data-loads-part1#impact-on-performance-and-resource-usage)


![large_data_loads-p1-02.png](/uploads/large_data_loads_p1_02_b803b7ca13.png)
The insert block size impacts both the [disk file](https://en.wikipedia.org/wiki/Category:Disk_file_systems) [i/o](https://en.wikipedia.org/wiki/Input/output) usage and memory usage of a ClickHouse server. Larger insert blocks use more memory but generate larger and fewer initial parts. The fewer parts ClickHouse needs to create for loading a large amount of data, the less disk file i/o and automatic [background merges](/blog/supercharge-your-clickhouse-data-loads-part1#more-parts--more-background-part-merges) [required](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#data-needs-to-be-batched-for-optimal-performance).
How the insert block size can be configured depends on how the data is ingested. Do the ClickHouse servers themselves pull it, or do external clients push it?


### Configuration when data is pulled by ClickHouse servers [\#](/blog/supercharge-your-clickhouse-data-loads-part1#configuration-when-data-is-pulled-by-clickhouse-servers)


When using an [INSERT INTO SELECT](https://clickhouse.com/docs/en/sql-reference/statements/insert-into#inserting-the-results-of-select) query in combination with an [integration table engine](https://clickhouse.com/docs/en/engines/table-engines/integrations), or a [table function](https://clickhouse.com/docs/en/sql-reference/table-functions), the data is pulled by the ClickHouse server itself:
![large_data_loads-p1-03.png](/uploads/large_data_loads_p1_03_955143fa6a.png)
Until the data is completely loaded, the server executes a loop:
`① Pull and parse the next portion of data and form an in-memory data block (one [per](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse#poorly-chosen-partitioning-key) partitioning key) from it.  
  

② Write the block into a new part on storage.  
  

Go to ①`


In ① the portion size depends on the insert block size, which can be controlled with two settings:


- [min\_insert\_block\_size\_rows](https://clickhouse.com/docs/en/operations/settings/settings#min-insert-block-size-rows) (default: 1048545 million rows)
- [min\_insert\_block\_size\_bytes](https://clickhouse.com/docs/en/operations/settings/settings#min-insert-block-size-bytes) (default: 256 MB)


When either the specified number of rows is collected in the insert block, or the configured amount of data is reached (whatever happens first), then this will trigger the block being written into a new part. The insert loop continues at step ①.


Note that the `min_insert_block_size_bytes` value denotes the uncompressed in\-memory block size (and not the compressed on\-disk part size). Also, note that the created blocks and parts rarely precisely contain the configured number of rows or bytes, as ClickHouse is streaming and [processing](https://clickhouse.com/company/events/query-performance-introspection) data row\-[block](https://clickhouse.com/docs/en/operations/settings/settings#setting-max_block_size)\-wise. Therefore these settings specify minimum thresholds.


### Configuration when data is pushed by clients [\#](/blog/supercharge-your-clickhouse-data-loads-part1#configuration-when-data-is-pushed-by-clients)


Depending on the data transfer [format](https://clickhouse.com/docs/en/interfaces/formats) and [interface](https://clickhouse.com/docs/en/interfaces/overview) used by the client or client library, the in\-memory data blocks are formed by either the ClickHouse server or the client itself. This determines where and how the block size can be controlled. This further also depends on if synchronous or asynchronous inserts are used.


#### Synchronous inserts [\#](/blog/supercharge-your-clickhouse-data-loads-part1#synchronous-inserts)


##### When the server forms the blocks [\#](/blog/supercharge-your-clickhouse-data-loads-part1#when-the-server-forms-the-blocks)


When a client grabs some data and sends it with a [synchronous](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#synchronous-data-inserts-primer) insert query in non\-native format (e.g., the [JDBC driver](https://github.com/ClickHouse/clickhouse-java) [uses](https://github.com/ClickHouse/clickhouse-java#features) [RowBinary](https://clickhouse.com/docs/en/interfaces/formats#rowbinary) for inserts), the server parses the insert query’s data and forms (at least) one in\-memory block ([per](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse#poorly-chosen-partitioning-key) partitioning key) from it, which is written to storage in the form of a part:
![large_data_loads-p1-04.png](/uploads/large_data_loads_p1_04_00ae369460.png)
The insert query’s number of row values automatically controls the block size. However, the maximum size of a block ([per](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse#poorly-chosen-partitioning-key) partitioning key) can be configured with the [max\_insert\_block\_size](https://clickhouse.com/docs/en/operations/settings/settings#settings-max_insert_block_size) rows setting. If a single block formed from the insert query’s data contains more than `max_insert_block_size` rows (default value [is](https://clickhouse.com/docs/en/operations/settings/settings#settings-max_insert_block_size) \~ 1 million rows), then the server creates additional blocks and parts, respectively.


To minimize the number of created (and [to\-be\-merged](/blog/supercharge-your-clickhouse-data-loads-part1#more-parts--more-background-part-merges)) parts, we generally [recommend](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#data-needs-to-be-batched-for-optimal-performance) sending fewer but larger inserts instead of many small inserts by buffering data client\-side and inserting data as batches.


##### When the client forms the blocks [\#](/blog/supercharge-your-clickhouse-data-loads-part1#when-the-client-forms-the-blocks)


The ClickHouse command\-line client ([clickhouse\-client](https://clickhouse.com/docs/en/interfaces/cli)), and some of the programming language\-specific libraries like the [Go](https://clickhouse.com/docs/en/integrations/go), [Python](https://clickhouse.com/docs/en/integrations/python), and [C\+\+](https://clickhouse.com/docs/en/interfaces/cpp) clients, form the insert blocks client side and send them in [native format](https://clickhouse.com/docs/en/interfaces/formats#native) over the [native interface](https://clickhouse.com/docs/en/interfaces/tcp) to a ClickHouse server, which directly writes the block to storage.


For example, if the ClickHouse command\-line client is used for inserting some data:



```
./clickhouse client --host ...  --password …  \
 --input_format_parallel_parsing 0 \
 --max_insert_block_size 2000000 \
 --query "INSERT INTO t FORMAT CSV" < data.csv

```

Then the client by itself parses the data and forms in\-memory blocks ([per](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse#poorly-chosen-partitioning-key) partitioning key) from the data and sends it in native format via the native ClickHouse protocol to the server, which writes the block to storage as a part:
![large_data_loads-p1-05.png](/uploads/large_data_loads_p1_05_210c345b0d.png)
The client\-side in\-memory block size (in a count of rows) can be controlled via the `max_insert_block_size` (default: 1048545 million rows) command line option.


Note that we disabled [parallel parsing](https://github.com/ClickHouse/ClickHouse/blob/d1d2f2c1a4979d17b7d58f591f56346bc79278f8/src/Processors/Formats/Impl/ParallelParsingInputFormat.h#L27) in the example command\-line call above. Otherwise, clickhouse\-client will ignore the `max_insert_block_size` setting and instead squash several blocks resulting from parallel parsing into one insert block.


Also, note that the client\-side `max_insert_block_size` setting is specific to clickhouse\-client. You need to check the documentation and settings of your client library for similar settings.


#### Asynchronous data inserts [\#](/blog/supercharge-your-clickhouse-data-loads-part1#asynchronous-data-inserts)


Alternatively, or in addition to client\-side batching, you can use [asynchronous inserts](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#asynchronous-inserts). With asynchronous data inserts, the blocks are always formed by the server regardless of which client, format, and protocol is used:
![large_data_loads-p1-06.png](/uploads/large_data_loads_p1_06_6f3e4ad9c9.png)
With asynchronous inserts, the data from received insert queries is first put into an in\-memory buffer (see ①, ②, and ③ in the diagram above) and ④ when the buffer is flushed depending on [configuration settings](https://clickhouse.com/docs/en/optimize/asynchronous-inserts) (e.g., once a specific amount of data is collected), the server parses the buffer’s data and forms an in\-memory block ([per](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse#poorly-chosen-partitioning-key) partitioning key) from it, which is ⑤ written to storage in the form of a part. If a single block would contain more than `max_insert_block_size` rows, then the server creates additional blocks and parts, respectively.


### More parts \= more background part merges [\#](/blog/supercharge-your-clickhouse-data-loads-part1#more-parts--more-background-part-merges)


The smaller the configured insert block size is, the more initial parts get created for a large data load, and the more background part merges are executed concurrently with the data ingestion. This can cause resource contention (CPU and memory) and require additional time (for reaching a [healthy](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings#parts-to-throw-insert) number of parts) after the ingestion is finished.


ClickHouse will continuously [merge](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#data-needs-to-be-batched-for-optimal-performance) parts into larger parts until they [reach](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings#max-bytes-to-merge-at-max-space-in-pool) a compressed size of \~150 GiB. This diagram shows how a ClickHouse server merges parts:
![large_data_loads-p1-07.png](/uploads/large_data_loads_p1_07_9943fa1787.png)
A single ClickHouse server utilizes several [background merge threads](https://clickhouse.com/docs/en/operations/server-configuration-parameters/settings#background_pool_size) to execute concurrent [part merges](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#data-needs-to-be-batched-for-optimal-performance). Each thread executes a loop:
`① Decide which parts to merge next, and load these parts as blocks into memory.  
  

② Merge the loaded blocks in memory into a larger block.  
  

③ Write the merged block into a new part on disk.  
  

Go to ①`  

Note that ClickHouse is not necessarily loading the whole to\-be\-merged parts into memory at once. Based on several [factors](https://clickhouse.com/codebrowser/ClickHouse/src/Storages/MergeTree/MergeTreeSettings.h.html#DB::MergeTreeSettingsTraits::Data::vertical_merge_algorithm_min_rows_to_activate), to reduce memory consumption (for the sacrifice of merge speed), so\-called [vertical merging](https://clickhouse.com/codebrowser/ClickHouse/src/Storages/MergeTree/MergeTreeSettings.h.html#DB::MergeTreeSettingsTraits::Data::enable_vertical_merge_algorithm) loads and merges parts by chunks of blocks instead of in one go. Further, note that [increasing](/blog/supercharge-your-clickhouse-data-loads-part1#hardware-size) the number of CPU cores and the size of RAM increases the background merge throughput.


Parts that were merged into larger parts are marked as [inactive](https://clickhouse.com/docs/en/operations/system-tables/parts) and finally deleted after a [configurable](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings#old-parts-lifetime) number of minutes. Over time, this creates a tree of merged parts. Hence the name [merge tree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family) table:
![large_data_loads-p1-08.png](/uploads/large_data_loads_p1_08_5686d39d92.png)
Each part belongs to a specific level indicating the number of merges leading to the part.


## Insert parallelism [\#](/blog/supercharge-your-clickhouse-data-loads-part1#insert-parallelism)


### Impact on performance and resource usage [\#](/blog/supercharge-your-clickhouse-data-loads-part1#impact-on-performance-and-resource-usage-1)


![large_data_loads-p1-09.png](/uploads/large_data_loads_p1_09_107cc90b91.png)
A ClickHouse server can process and insert data in parallel. The level of insert parallelism impacts the ingest throughput and memory usage of a ClickHouse server. Loading and processing data in parallel requires more main memory but increases the ingest throughput as data is processed faster.
How the level of insert parallelism can be configured depends again on how the data is ingested.


### Configuration when data is pulled by ClickHouse servers [\#](/blog/supercharge-your-clickhouse-data-loads-part1#configuration-when-data-is-pulled-by-clickhouse-servers-1)


Some integration table functions like [s3](https://clickhouse.com/docs/en/engines/table-engines/integrations/s3#wildcards-in-path), [url](https://clickhouse.com/docs/en/sql-reference/table-functions/url#globs-in-url), and [hdfs](https://clickhouse.com/docs/en/sql-reference/table-functions/hdfs#globs_in_path) allow specifying sets of to\-be\-loaded\-file names via [glob patterns](https://en.wikipedia.org/wiki/Glob_(programming)). When a glob pattern matches multiple existing files, ClickHouse can parallelize reads across and within these files and insert the data in parallel into a table by utilizing parallel running insert threads (per server):
![large_data_loads-p1-10.png](/uploads/large_data_loads_p1_10_ae85480503.png)
Until all data from all files is processed, each insert thread executes a loop:
`① Get the next portion of unprocessed file data (portion size is based on the configured block size) and create an in-memory data block from it.  
  

② Write the block into a new part on storage.  
  

Go to ①.`


The number of such parallel insert threads can be configured with the [max\_insert\_threads](https://clickhouse.com/docs/en/operations/settings/settings#settings-max-insert-threads) setting. The default value is 1 for OSS and 4 for [ClickHouse Cloud](https://clickhouse.com/cloud).


With a large number of files, the parallel processing by multiple insert threads works well. It can fully saturate both the available CPU cores and the network bandwidth (for parallel file downloads). In scenarios where just a few large files will be loaded into a table, ClickHouse automatically establishes a high level of data processing parallelism and optimizes network bandwidth usage by spawning additional reader threads per insert thread for reading (downloading) more distinct ranges within large files in parallel. For the advanced reader, the settings [max\_download\_threads](https://clickhouse.com/codebrowser/ClickHouse/src/Core/Settings.h.html#DB::SettingsTraits::Data::max_download_threads) and [max\_download\_buffer\_size](https://clickhouse.com/codebrowser/ClickHouse/src/Core/Settings.h.html#DB::SettingsTraits::Data::max_download_buffer_size) may be of interest. This mechanism is currently [implemented](https://clickhouse.com/docs/en/whats-new/changelog/2022#performance-improvement-8) for the [s3](https://github.com/ClickHouse/ClickHouse/pull/35571) and [url](https://github.com/ClickHouse/ClickHouse/pull/35150) table functions. Furthermore, for files that are [too small](https://github.com/ClickHouse/ClickHouse/blob/f5e8028bb12e0e01438e6aeccee426fcd95805c7/src/Storages/StorageS3.cpp#L603) for parallel reading, to increase throughput, ClickHouse automatically [prefetches](https://github.com/ClickHouse/ClickHouse/blob/f5e8028bb12e0e01438e6aeccee426fcd95805c7/src/Storages/StorageS3.cpp#L608) data by pre\-reading such files asynchronously.


#### Parallel servers [\#](/blog/supercharge-your-clickhouse-data-loads-part1#parallel-servers)


Some of the integration table functions featuring glob patterns for loading multiple files in parallel also exist in a cluster version, e.g., [s3Cluster](https://clickhouse.com/docs/en/sql-reference/table-functions/s3Cluster), [hdfsCluster](https://clickhouse.com/docs/en/sql-reference/table-functions/hdfsCluster), and [urlCluster](https://clickhouse.com/docs/en/sql-reference/table-functions/urlCluster). These table functions increase the level of insert parallelism further by utilizing the aforementioned multiple parallel insert threads on multiple servers in parallel:
![large_data_loads-p1-11.png](/uploads/large_data_loads_p1_11_4a860c1a87.png)
The server that initially receives the insert query first resolves the glob pattern and then dispatches the processing of each matching file dynamically to the other servers (and himself).


### Configuration when data is pushed by clients [\#](/blog/supercharge-your-clickhouse-data-loads-part1#configuration-when-data-is-pushed-by-clients-1)


A ClickHouse server can receive and execute insert queries [concurrently](https://clickhouse.com/docs/en/operations/server-configuration-parameters/settings#max_thread_pool_size). A client can utilize this by running parallel client\-side threads:
![large_data_loads-p1-12.png](/uploads/large_data_loads_p1_12_36165c2b97.png)
Each thread executes a loop:
`① Get the next data portion and create an insert from it.  
  

② Send the insert to ClickHouse (and wait for the acknowledgment that the insert succeeded).  
  

Go to ①`


Alternatively, or in addition, [multiple clients](https://clickhouse.com/blog/real-world-data-noaa-climate-data#load-the-data) can send data in parallel to ClickHouse:
![large_data_loads-p1-13.png](/uploads/large_data_loads_p1_13_6ac850dbf2.png)


#### Parallel servers [\#](/blog/supercharge-your-clickhouse-data-loads-part1#parallel-servers-1)


In [ClickHouse Cloud](https://clickhouse.com/cloud), inserts are evenly distributed over multiple ClickHouse servers with a [load balancer](https://clickhouse.com/docs/en/cloud/reference/architecture). Traditional [shared\-nothing](https://en.wikipedia.org/wiki/Shared-nothing_architecture) ClickHouse [clusters](https://clickhouse.com/company/events/scaling-clickhouse) can use a combination of [sharding](https://clickhouse.com/docs/en/architecture/horizontal-scaling) and a [distributed table](https://clickhouse.com/docs/en/engines/table-engines/special/distributed) for load balancing inserts over multiple servers:
![large_data_loads-p1-14.png](/uploads/large_data_loads_p1_14_94303ae6e6.png)


## Hardware size [\#](/blog/supercharge-your-clickhouse-data-loads-part1#hardware-size)


### Impact on performance [\#](/blog/supercharge-your-clickhouse-data-loads-part1#impact-on-performance)


![large_data_loads-p1-15.png](/uploads/large_data_loads_p1_15_4d13a2d2a5.png)
The number of available CPU cores and the size of RAM impacts the
- supported [initial size of parts](/blog/supercharge-your-clickhouse-data-loads-part1#insert-block-size)
- possible level of [insert parallelism](/blog/supercharge-your-clickhouse-data-loads-part1#insert-parallelism)
- throughput of [background part merges](/blog/supercharge-your-clickhouse-data-loads-part1#more-parts--more-background-part-merges)


and, therefore, the overall ingest throughput.


How easily the number of CPU cores and the size RAM can be changed depends on whether the ingestion occurs in ClickHouse Cloud or a traditional shared\-nothing ClickHouse cluster.


### ClickHouse Cloud [\#](/blog/supercharge-your-clickhouse-data-loads-part1#clickhouse-cloud)


Because storage is completely [separated](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#clickhouse-cloud-enters-the-stage) from the ClickHouse servers in [ClickHouse Cloud](https://clickhouse.com/cloud), you [can](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#automatic-cluster-scaling) freely [either](https://clickhouse.com/docs/en/manage/scaling#vertical-and-horizontal-scaling) change the size (CPU and RAM) of existing servers or add additional servers quickly ([without](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#example) requiring any physical resharding or rebalancing of the data):
![large_data_loads-p1-16.png](/uploads/large_data_loads_p1_16_57f6d9e7b9.png)
Additional servers will then automatically [participate](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#example) in [parallel data ingestion](/blog/supercharge-your-clickhouse-data-loads-part1#insert-parallelism) and [background part merges](/blog/supercharge-your-clickhouse-data-loads-part1#more-parts--more-background-part-merges), which can drastically reduce the overall ingestion time.


### Traditional shared\-nothing ClickHouse cluster [\#](/blog/supercharge-your-clickhouse-data-loads-part1#traditional-shared-nothing-clickhouse-cluster)


In a traditional [shared\-nothing](https://en.wikipedia.org/wiki/Shared-nothing_architecture) ClickHouse [cluster](https://clickhouse.com/company/events/scaling-clickhouse), data is stored locally on each server:
![large_data_loads-p1-17.png](/uploads/large_data_loads_p1_17_b4ff9ef0e7.png)
Adding additional servers [requires](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#example) manual configuration [changes](https://clickhouse.com/company/events/scaling-clickhouse) and more time than in ClickHouse Cloud.


## Summary [\#](/blog/supercharge-your-clickhouse-data-loads-part1#summary)


You can let ClickHouse load data blazingly fast by allowing its data insert mechanics to fully utilize the hardware it runs on. Alternatively, you can reduce the resource usage of large data loads. Depending on what your data load scenario is. For this, we have explored how the data insert mechanics of ClickHouse work and how you can control and configure the three main performance and resource usage factors for large data loads in ClickHouse: **Insert block size**, **Insert parallelism**, and **Hardware size**.


With that, we set the scene for our two follow\-up posts turning this knowledge into best practices for fast and resilient large data loads. In the [next post](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part2) of this series, we are going on a race track and making a large data insert 3 times faster than with default settings. On the same hardware.


Stay tuned!

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
