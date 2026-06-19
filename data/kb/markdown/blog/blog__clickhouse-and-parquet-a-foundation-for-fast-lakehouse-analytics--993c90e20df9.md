# ClickHouse and Parquet: A foundation for fast Lakehouse analytics


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse and Parquet: A foundation for fast Lakehouse analytics

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber)May 7, 2025 · 34 minutes read
> **TL;DR**
> ClickHouse is built to run fast on Parquet, the storage format behind open table formats like Iceberg and Delta Lake, and it has been optimizing for it for years.   
>   
> **This post takes you deep inside the query engine** to show how it queries Parquet files directly (no ingestion required), faster than many systems can query their own native formats, and what’s coming next to make it even faster.  
>   
> It’s the first in a new series on how ClickHouse powers fast Lakehouse analytics from the ground up.  
>   
> **Spoiler: ClickHouse isn’t getting ready for the Lakehouse, it’s already there.**


## A Lakehouse\-ready engine, by accident and by design [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#a-lakehouse-ready-engine-by-accident-and-by-design)


Sometimes, the future catches up with what you were already doing.


ClickHouse wasn’t built for the [Lakehouse](https://en.wiktionary.org/wiki/data_lakehouse) (Iceberg and Delta Lake formats were created when ClickHouse was already a mature DBMS), but it turns out to be a great fit. With first\-class support for Parquet and direct file querying, it has long supported many Lakehouse\-style patterns natively.


The ClickHouse [query engine](https://clickhouse.com/docs/academic_overview#4-query-processing-layer) has always treated querying data in any format, including Parquet, from any location, including object storage, as a core capability. Whether loading data or querying it directly without ingestion, it’s simply how things have always worked.


Today’s Lakehouse architecture puts a name to what ClickHouse has already been doing for years: run anywhere, query anything, and access data from anywhere.


**Run anywhere**: The engine can be [operated](https://www.youtube.com/watch?v=EOXEW_-r10A) in on\-premise, cloud, standalone, or in\-process modes:


![Blog-FormatsReads.001.png](/uploads/Blog_Formats_Reads_001_cca890442c.png)
**Query anything**: While it’s optimized for its native [MergeTree tables](https://clickhouse.com/docs/parts), ClickHouse can also query external formats directly, without ingesting them first. Most databases require you to load files like Parquet into their own native format before running queries. ClickHouse can fully skip that step; the ClickHouse query engine can directly query [over 70 file formats](https://sql.clickhouse.com/?query=U0VMRUNUICogCkZST00gc3lzdGVtLmZvcm1hdHMKV0hFUkUgaXNfaW5wdXQKT1JERVIgQlkgbmFtZTs&chart=eyJ0eXBlIjoibGluZSIsImNvbmZpZyI6eyJ4YXhpcyI6InllYXIiLCJ5YXhpcyI6Ijk5dGhfYXZnX3RlbXAiLCJzZXJpZXMiOiJjb3VudHJ5IiwidGl0bGUiOiJUZW1wZXJhdHVyZSBieSBjb3VudHJ5IGFuZCB5ZWFyIn19&run_query=true&tab=results) out of the box, with no restrictions. You get full SQL support, including joins, window functions, and [160\+ aggregation functions](https://sql.clickhouse.com/?query=U0VMRUNUICogCkZST00gc3lzdGVtLmZ1bmN0aW9ucwpXSEVSRSBpc19hZ2dyZWdhdGUKQU5EIGVtcHR5KGFsaWFzX3RvKQpPUkRFUiBCWSBuYW1l&chart=eyJ0eXBlIjoibGluZSIsImNvbmZpZyI6eyJ4YXhpcyI6InllYXIiLCJ5YXhpcyI6Ijk5dGhfYXZnX3RlbXAiLCJzZXJpZXMiOiJjb3VudHJ5IiwidGl0bGUiOiJUZW1wZXJhdHVyZSBieSBjb3VudHJ5IGFuZCB5ZWFyIn19&run_query=true&tab=results), all **without needing to ingest the data first**. Supported formats include Parquet, JSON, CSV, Arrow, and many more:


![Blog-FormatsReads.002.png](/uploads/Blog_Formats_Reads_002_48fd39f633.png)
**Access data from anywhere**: With [80\+ built\-in integrations](https://sql.clickhouse.com/?query=V0lUSCBib3RoIEFTICgKICAgICAgICBTRUxFQ1QgbmFtZSwgJ1RhYmxlIGZ1bmN0aW9uJyBhcyBjYXRlZ29yeQogICAgICAgIEZST00gc3lzdGVtLnRhYmxlX2Z1bmN0aW9ucyAKICAgIFVOSU9OIEFMTAogICAgICAgIFNFTEVDVCBuYW1lLCAnVGFibGUgZW5naW5lJyBhcyBjYXRlZ29yeQogICAgICAgIEZST00gc3lzdGVtLnRhYmxlX2VuZ2luZXMKKQpTRUxFQ1QgKiAKRlJPTSBib3RoCldIRVJFIAogICAgTk9UIG5hbWUgaWxpa2UgJyVtZXJnZVRyZWUlJyBBTkQKICAgIE5PVCBuYW1lIGlsaWtlICcldmlldyUnIEFORAogICAgTk9UIG5hbWUgaWxpa2UgJyV2YWx1ZXMlJyBBTkQKICAgIE5PVCBuYW1lIGlsaWtlICclemVyb3MlJyBBTkQKICAgIE5PVCBuYW1lIGlsaWtlICclY29zbiUnIEFORAogICAgTk9UIG5hbWUgaWxpa2UgJyVjb3NuJScgQU5ECiAgICBOT1QgbmFtZSBpbGlrZSAnJWJ1ZmZlciUnIEFORAogICAgTk9UIG5hbWUgaWxpa2UgJyVyZXBsaWNhJScgQU5ECiAgICBOT1QgbmFtZSBpbGlrZSAnJWRpc3RyaWJ1dGVkJScgQU5ECiAgICBOT1QgbmFtZSBpbGlrZSAnJWpzb24lJyBBTkQKICAgIE5PVCBuYW1lIGlsaWtlICclcmFuZG9tJScgQU5ECiAgICBOT1QgbmFtZSBpbGlrZSAnJW1lcmdlJSdBTkQKICAgIE5PVCBuYW1lIGlsaWtlICclbnVsbCUnQU5ECiAgICBOT1QgbmFtZSBpbGlrZSAnJW51bWJlcnMlJ0FORAogICAgTk9UIG5hbWUgaWxpa2UgJyVvc3MlJ0FORAogICAgTk9UIG5hbWUgSU4gWydjbHVzdGVyJywgJ2Zvcm1hdCcsICdpbnB1dCcsICdKb2luJywgJ0tlZXBlck1hcCcsICdMb2cnLCAnTWVtb3J5JywgJ1NldCcsICdTdHJpcGVMb2cnLCAnVGlueUxvZyddICAgIApPUkRFUiBCWSBsb3dlcihuYW1lKQ&chart=eyJ0eXBlIjoibGluZSIsImNvbmZpZyI6eyJ4YXhpcyI6InllYXIiLCJ5YXhpcyI6Ijk5dGhfYXZnX3RlbXAiLCJzZXJpZXMiOiJjb3VudHJ5IiwidGl0bGUiOiJUZW1wZXJhdHVyZSBieSBjb3VudHJ5IGFuZCB5ZWFyIn19&run_query=true&tab=results), the engine connects seamlessly to external systems and storage platforms, including S3/GCP/Azure object stores.


These features make ClickHouse a great fit for [data lakes](https://en.wiktionary.org/wiki/data_lake#English), letting you query open table formats like [Apache Iceberg](https://iceberg.apache.org/), which [store](https://iceberg.apache.org/spec/?h=parquet#parquet) data mainly in **Parquet files**, usually on object storage like S3, GCS, or similar:


![Blog-FormatsReads.003.png](/uploads/Blog_Formats_Reads_003_4c59b4fa2d.png)
And thanks to its flexible run modes, the ClickHouse query engine can be deployed wherever your Lakehouse lives: close to your object store, inside multi\-tenant SaaS environments, embedded in Python workflows for interactive analysis in notebooks using pandas dataframes, or even as stateless workers in environments like AWS Lambda.


## Inside the engine: How ClickHouse queries Parquet [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#inside-the-engine-how-clickhouse-queries-parquet)


Let’s take a closer look at how ClickHouse handles one of the Lakehouse’s most important building blocks: [Parquet](https://parquet.apache.org/).


- How effectively can the ClickHouse engine directly query Parquet files today?
- Out of curiosity, how does its performance compare with native MergeTree tables?
- Are there even faster external formats among the 70\+ that ClickHouse supports?
- And what’s coming next to make it even better?


This post answers all of the above and kicks off a new blog series on ClickHouse as a fast, flexible Lakehouse engine. We begin with the **Parquet data layer** that underpins open table formats like Iceberg and [Delta Lake](https://delta.io/).


We’ll start by examining how the current Parquet reader works and what makes it fast. Then, we’ll benchmark its performance on real analytical queries, highlighting both current capabilities and upcoming improvements.


As mentioned in the introduction, the ClickHouse query engine supports direct querying of 70\+ file formats, including Parquet, without ingestion. [Format\-specific readers](https://github.com/ClickHouse/ClickHouse/tree/775b7d30c814bf9f28614b472d4ae8c10b39fa92/src/Processors/Formats/Impl) plug into the engine, as shown below:
![Blog-FormatsReads.004.png](/uploads/Blog_Formats_Reads_004_0fc84417b9.png)


When querying ① external files, the format\-specific reader reads and parses the data, ② converts it into ClickHouse’s in\-memory format, and passes it to the query engine, which ③ processes it into the ④ final result.


In the rest of this section, we’ll focus on the Parquet reader. Combined with the ClickHouse query engine, it’s the key component behind the high performance of direct Parquet file queries.


### How the Parquet reader works today and what’s next [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#how-the-parquet-reader-works-today-and-whats-next)


Fun fact: While MergeTree remains the native data storage format, ClickHouse has been actively tuning and optimizing for Parquet for over three years. It’s all part of our goal to make ClickHouse the fastest engine in the world for querying Parquet at scale.


The [current Parquet reader](https://github.com/ClickHouse/ClickHouse/blob/775b7d30c814bf9f28614b472d4ae8c10b39fa92/src/Processors/Formats/Impl/ParquetBlockInputFormat.h#L14) uses the [Arrow library](https://github.com/apache/arrow/tree/main/cpp) to parse files into [Arrow](https://arrow.apache.org/) format, then [copies](https://github.com/ClickHouse/ClickHouse/blob/775b7d30c814bf9f28614b472d4ae8c10b39fa92/src/Processors/Formats/Impl/ArrowColumnToCHColumn.cpp) the data into ClickHouse’s native in\-memory format for execution. In the next sections, we’ll explore the capabilities of this reader.


A new native Parquet reader is already in the [works](https://github.com/ClickHouse/ClickHouse/pull/78380), designed to eliminate the Arrow layer entirely and read files directly into ClickHouse’s native in\-memory format. It also brings better parallelism and I/O efficiency. The project is fittingly called **Yet Another Parquet Reader**, because, well, it is. This is ClickHouse’s third native Parquet reader implementation. The first (`input_format_parquet_use_native_reader`) was started but never completed. The second (v2\) made it to a [pull request](https://github.com/ClickHouse/ClickHouse/pull/70611), but stalled before reaching production. And now, [v3](https://github.com/ClickHouse/ClickHouse/pull/78380) is underway.



> We could’ve waited to publish this post until the new reader was finished, but benchmarking the current reader gives us a great baseline. In a future follow\-up, we’ll highlight how the new reader improves performance and efficiency.


Parquet file query performance in ClickHouse is primarily determined by two factors:


1. **Level of parallelism**: The more files, and the more non\-overlapping regions within those files, that ClickHouse can read and process in parallel, the higher the throughput and the faster the queries complete.
2. **Degree of I/O reduction**: The less unnecessary work (such as scanning and processing irrelevant data) is done, the faster queries complete.


In the next two sections, we’ll break down how the query engine and current Parquet reader work together to achieve parallelism and I/O reduction, and highlight upcoming improvements in the native reader. We’ll also cover tuning settings that let you influence these behaviors for performance tuning.


### Parallelism: How the engine scales [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#parallelism-how-the-engine-scales)


Before explaining how ClickHouse currently achieves parallelism when querying Parquet files, we first need to briefly look at the physical on\-disk structure of a Parquet file. The way Parquet organizes data fundamentally determines how efficiently the data can be split into independent units of work, and thus how much parallelism can be applied during query execution.


The following diagram shows a simplified view of how data from a web analytics dataset (used later in our benchmark) is [organized](https://parquet.apache.org/docs/file-format/) on disk when stored as Parquet files:


![Blog-FormatsReads.005.png](/uploads/Blog_Formats_Reads_005_3fd2648fb1.png)
In Parquet, our [test dataset](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#benchmark-setup-hardware-dataset-and-software), consisting logically of rows and columns, is stored in one or more **files**. Each file organizes the data hierarchically as follows:


① **Row groups**: The stored data is divided into one or more horizontal partitions called row groups. By default, when Parquet files are written with ClickHouse, each row group contains [1 million rows](https://clickhouse.com/docs/operations/settings/formats#output_format_parquet_row_group_size) or [\~500 MB of data](https://clickhouse.com/docs/operations/settings/formats#output_format_parquet_row_group_size_bytes) (before compression).


② **Column chunks**: Each row group is further divided vertically into column chunks, one for each column in the dataset. Each chunk stores the values for that column across all rows in the row group.


③ **Data pages**: Inside each column chunk, the actual values are stored in data pages. By default, ClickHouse writes data pages of [1 MB](https://clickhouse.com/docs/operations/settings/formats#output_format_parquet_data_page_size) (before compression). A page stores a fixed or variable number of [encoded](https://parquet.apache.org/docs/file-format/data-pages/encodings/) and [compressed](https://parquet.apache.org/docs/file-format/data-pages/compression/) values, depending on the column’s data type and the encoding scheme used.


Note: For readability, the diagram above shows row groups containing six rows and data pages containing three values per column.


With the data layout clear, we can now look at how the ClickHouse query engine, together with the current Parquet reader, parallelizes data processing across available CPU cores to maximize query performance.


ClickHouse doesn’t just run anywhere and query anything, it also **parallelizes almost everything**, especially when querying Parquet. The following diagram shows how different layers of parallelism come together within the Parquet reader and the ClickHouse query engine during query execution:


![Blog-FormatsReads.006.png](/uploads/Blog_Formats_Reads_006_91953859fe.png)
① **Parallel prefetch threads**: Within a Parquet file, the Parquet file reader reads multiple row groups in parallel (*intra\-file*, *inter–row group parallelism*). By default, row group prefetching is [enabled](https://clickhouse.com/docs/operations/settings/formats#input_format_parquet_enable_row_group_prefetch) with four parallel prefetch threads (controlled by the [max\_download\_threads](https://clickhouse.com/docs/operations/settings/settings#max_download_threads) setting) and kicks in either when parsing reaches its maximum parallelism (explained below) or when parsing would otherwise stall, such as when data must first be loaded over a network connection.


② **Parallel parsing threads**: Parsing threads read and parse data from multiple row groups within the same file in parallel (*intra\-file, inter–row group parallelism*). If prefetching is active, they read from the prefetch buffer; otherwise, they read directly from the file. The number of parsing threads (across all file streams, see below) is controlled by the [max\_parsing\_threads](https://clickhouse.com/docs/operations/settings/settings#max_parsing_threads) setting, which by default matches the number of available CPU cores.


③ **Parallel file streams**: Different Parquet files are processed concurrently, each with their own parallel prefetch and parsing threads, to maximize throughput across files (*inter\-file parallelism*). The number of file streams is determined dynamically during query compilation (see below).


④ **Parallel processing lanes**: As data is passed from the Parquet reader component to the query engine [block](https://clickhouse.com/docs/development/architecture#block)\-wise and in a streaming fashion, filtering, aggregation, and sorting happen across independent [lanes](https://clickhouse.com/docs/optimize/query-parallelism#distributing-work-across-processing-lanes) for maximum concurrency (inter\- and intra\-operator parallelism). The number of parallel processing lanes is determined by the [max\_threads](https://clickhouse.com/docs/operations/settings/settings#max_threads) setting, which by default matches the number of CPU cores available to the ClickHouse query engine.


Whether you’re querying many small files or a single large file, ClickHouse automatically balances the Parquet file processing such that query execution remains efficient. To achieve this, the file path pattern used to select Parquet files (e.g. with the [file table function](https://clickhouse.com/docs/sql-reference/table-functions/file)) is resolved during query compilation, and the number of matching files (`num_files`) directly influences the physical query plan:


- Many small files are parsed with one thread per file across many file streams.
- A single large file is parsed with many threads operating in parallel on a single stream.


The calculations for this follow simple rules:


- Number of parallel file streams [\=](https://github.com/ClickHouse/ClickHouse/blob/d66f2f168249888d7672045389350493a05a98fe/src/Storages/StorageFile.cpp#L1677-L1686) `min(max_threads, num_files)`
- The available parallel parsing threads (`max_parsing_threads`) is then evenly spread over the file streams with [this](https://github.com/ClickHouse/ClickHouse/blob/d66f2f168249888d7672045389350493a05a98fe/src/Storages/StorageFile.cpp#L1442) formula: `max(max_parsing_threads / num_files, 1)`
Here, `/` denotes integer division (rounding down), and `max()` ensures that at least one parsing thread is assigned per file.


Let’s briefly look at three examples to see how this balancing of file streams and parsing threads works in practice.


### Parallelism in practice: 3 examples [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#parallelism-in-practice-3-examples)


In the following, we use the [EXPLAIN](https://clickhouse.com/docs/sql-reference/statements/explain#explain-pipeline) clause to inspect the [physical operator plan](https://clickhouse.com/docs/academic_overview#4-2-multi-core-parallelization)—also known as the “query pipeline”—for three different runs of [ClickBench query 11](https://github.com/ClickHouse/ClickBench/blob/f1178a21fbfdf3b2f9c71e7ed1602bb171d0cb2a/clickhouse/queries.sql#L11), executed over a web analytics dataset (used later in our benchmark) stored as Parquet files. This query filters, aggregates, and sorts the data before applying a LIMIT. With the `graph` option, ClickHouse outputs the plan in [DOT](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) format, which can be rendered to a PDF using [Graphviz](https://en.wikipedia.org/wiki/Graphviz).


#### Example 1: One Parquet file, 4 cores [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#example-1-one-parquet-file-4-cores)


As a first example, **we set max\_threads and max\_parsing\_threads to 4** (simulating a 4\-core machine and keeping the plan readable) and use a path pattern matching **exactly one Parquet file**:



```

```
clickhouse local --query "
EXPLAIN Pipeline graph = 1, compact = 0
SELECT MobilePhoneModel, COUNT(DISTINCT UserID) AS u
FROM file('./output/Parquet/100000000/1000000/sorted/zstd/chunk_00.parquet')
WHERE MobilePhoneModel <> ''
GROUP BY MobilePhoneModel
ORDER BY u DESC LIMIT 10
SETTINGS max_threads = 4, max_parsing_threads = 4;
" | dot -Tpdf > pipeline.pdf
```

```

![Blog-FormatsReads.007.png](/uploads/Blog_Formats_Reads_007_e7a34f6398.png)
As you can see, the query engine uses one file stream (based on the `min(max_threads = 4, num_files = 1)` formula), and 4 parallel processing lanes (`max_threads = 4`) for running the query over the data of one Parquet file.


The visualization above flows left to right. A `Resize` operator evenly distributes parsed file data across four processing lanes, where filtering and [partial aggregation](https://clickhouse.com/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#-multi-core-parallelization) is performed. A second `Resize` rebalances the streams to maintain even CPU utilization, crucial when data ranges have different predicate selectivities, which could otherwise overload some lanes and leave others idle. This dynamic redistribution ensures faster lanes assist slower ones, improving overall performance. Sorting proceeds in [three stages](https://clickhouse.com/blog/clickhouse-just-in-time-compiler-jit#clickhouse-compilation-of-sorting):


1. `PartialSortingTransform` sorts individual blocks in each lane.
2. `MergeSortingTransform` maintains a local sorted stream per lane via [2\-way merges](https://en.wikipedia.org/wiki/K-way_merge_algorithm).
3. `MergingSortedTransform` performs a [k\-way merge](https://en.wikipedia.org/wiki/K-way_merge_algorithm) across lanes, followed by a `LIMIT` to produce the final result.


There’s no direct logging or easy way to introspect the number of parallel parsing threads per file. However, based on the [formula in the source code](https://github.com/ClickHouse/ClickHouse/blob/d66f2f168249888d7672045389350493a05a98fe/src/Storages/StorageFile.cpp#L1442): `max(max_parsing_threads / num_files, 1)`, we can infer that with one file and `max_parsing_threads = 4`, multiple row groups are parsed in parallel using four threads.


#### Example 2: Two Parquet files, 4 cores [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#example-2-two-parquet-files-4-cores)


In the second example, we keep `max_threads` and `max_parsing_threads` set to 4 but change the file path pattern to match exactly 2 Parquet files:



```

```
clickhouse local --query "
EXPLAIN Pipeline graph = 1, compact = 0
SELECT MobilePhoneModel, COUNT(DISTINCT UserID) AS u
FROM file('./output/Parquet/100000000/1000000/sorted/zstd/chunk_0{0..1}.parquet')
WHERE MobilePhoneModel <> ''
GROUP BY MobilePhoneModel
ORDER BY u DESC LIMIT 10
SETTINGS max_threads = 4, max_parsing_threads = 4;
" | dot -Tpdf > pipeline.pdf
```

```

![Blog-FormatsReads.008.png](/uploads/Blog_Formats_Reads_008_b0a439b7b2.png)
Now the query engine uses two parallel file streams ( \= `min(max_threads = 4, num_files = 2)` , and 4 parallel processing lanes (`max_threads = 4`) for running the query over the data of two Parquet files.


The number of parallel parsing threads per file stream is 2 instead of 4 though (`max(max_parsing_threads = 4 / num_files = 2, 1)`).


#### Example 3: 100 Parquet files, 32 cores [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#example-3-100-parquet-files-32-cores)


Finally we show an example without artificially restricted `max_threads` and `max_parsing_threads` thresholds. On our [test machine](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#benchmark-setup-hardware-dataset-and-software) with 32 CPU cores both are set to `32` by default. The file path pattern matches all [100](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#generating-files-from-the-dataset) Parquet files of the example dataset:



```

```
clickhouse local --query "
EXPLAIN Pipeline graph = 1, compact = 0
SELECT MobilePhoneModel, COUNT(DISTINCT UserID) AS u
FROM file('./output/Parquet/100000000/1000000/sorted/zstd/chunk_*.parquet')
WHERE MobilePhoneModel <> ''
GROUP BY MobilePhoneModel
ORDER BY u DESC LIMIT 10;
" | dot -Tpdf > pipeline.pdf
```

```

![Blog-FormatsReads.009.png](/uploads/Blog_Formats_Reads_009_9af83ce703.png)
### Scaling out: Cluster\-wide execution [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#scaling-out-cluster-wide-execution)


So far, we’ve shown how a single ClickHouse query engine instance parallelizes Parquet processing across CPU cores. In [parallel cluster engine mode](https://clickhouse.com/blog/clickhouse-release-25-03#automatic-parallelization-for-external-data), the query engine distributes the work across all available CPU cores of all available nodes, scaling parallelism across the entire cluster:


![Blog-FormatsReads.010.png](/uploads/Blog_Formats_Reads_010_49b4ff82b5.png)
The query engine on the initiator node—the server that receives the query—resolves the file glob pattern, connects to engines on the other nodes, and dynamically assigns files. As remote nodes finish processing, they request more files from the initiator until all files are processed.


### What’s next for performance: smarter and finer\-grained parallelism [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#whats-next-for-performance-smarter-and-finer-grained-parallelism)


The [upcoming native Parquet reader](https://github.com/ClickHouse/ClickHouse/pull/78380) not only removes the [Arrow dependency](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#how-the-parquet-reader-works-today-and-whats-next), eliminating the in\-memory copy from Arrow data into ClickHouse’s internal format, saving time and memory, but also enables more fine\-grained and adaptive parallelism:


- **Column\-level parallelism within row groups**: Instead of only processing entire row groups in parallel, the new reader can read different columns from the same row group concurrently, enabling better CPU utilization when fewer row groups are available.
- **Merged I/O requests**: By pre\-registering expected file ranges, the reader can detect small, adjacent I/O operations and merge them into fewer, larger read requests, improving throughput, especially on high\-latency storage.
- **Parallelism\-aware scheduling**: The engine can assign different degrees of parallelism depending on the stage and memory footprint, e.g., using high parallelism for small structures like [Bloom filters](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#io-reduction-what-we-skip-and-how), and more conservative parallelism for bulk column data to reduce memory pressure.


These changes are designed to better exploit system resources and maintain throughput consistency across workloads of varying size and complexity.


With parallelism covered, we now turn to the second key factor for fast Parquet queries in ClickHouse: minimizing unnecessary I/O. The less irrelevant data we scan, parse, or process, the faster queries run. In the next section, we’ll look at the I/O reduction techniques ClickHouse applies today, and those coming soon with the native reader.


### I/O reduction: What we skip, and how [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#io-reduction-what-we-skip-and-how)


To understand how ClickHouse minimizes unnecessary reads, let’s look at the I/O reduction techniques enabled by Parquet’s file structure.


**Column projection**  

Parquet is a columnar format, so the reader and ClickHouse query engine only access the columns needed by a query.


**Compression and encoding**  

By encoding data (e.g., using dictionaries or run\-length encoding) and compressing it column\-by\-column, Parquet reduces the amount of data stored and read from disk. This not only saves space but also speeds up queries. ClickHouse can scan less data, decompress only what’s needed, and skip entire sections based on encoded metadata (see below).


Parquet supports a variety of encoding and compression schemes at the [page](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#parallelism-how-the-engine-scales) level:


- Page encoding: Parquet defines several [encoding schemes](https://parquet.apache.org/docs/file-format/data-pages/encodings/) for efficient value storage. Common examples include dictionary encoding (see below) and run\-length encoding.
- Page compression: After encoding, pages can be [compressed](https://parquet.apache.org/docs/file-format/data-pages/compression/) using algorithms like Snappy, LZ4, and ZSTD to further reduce file size and I/O.


**Predicate pushdown**  

Parquet enables coarse\-grained [predicate pushdown](https://homepages.cwi.nl/~boncz/msc/2018-BoudewijnBraams.pdf) through metadata stored at multiple levels of granularity. This metadata wasn’t shown [earlier](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#parallelism-how-the-engine-scales); the diagram below now includes it, again using our [web analytics dataset](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#parallelism-how-the-engine-scales) for illustration. Again, for clarity, it shows row groups with just six rows and data pages with only three values per column:


![Blog-FormatsReads.011.png](/uploads/Blog_Formats_Reads_011_7333b20d77.png)
Below, we describe the metadata elements added in the diagram above in more detail.


① **Column chunk\-level dictionary filtering**: For low\-cardinality columns, Parquet uses [dictionary encoding](https://parquet.apache.org/docs/file-format/data-pages/encodings/). Each column chunk includes a dictionary page that maps unique values. When queries filter on a specific value, like `WHERE status = 'cancelled'`, readers can check the dictionary first to decide whether the chunk contains that value and can be skipped entirely if not.


② **Page\-level min/max filtering**: Parquet pages can [include statistics](https://github.com/apache/parquet-format/blob/3ce0760933b875bc8a11f5be0b883cd107b95b43/src/main/thrift/parquet.thrift#L691) such as the [minimum and maximum values](https://github.com/apache/parquet-format/blob/3ce0760933b875bc8a11f5be0b883cd107b95b43/src/main/thrift/parquet.thrift#L306) for the column data stored on each page. When queries filter on a specific range, like `WHERE amount > 1000`, readers can use these stats to skip over pages where all values fall below the threshold. This is especially effective on sorted data, where large blocks can often be ruled out early.


③ **Column chunk\-level bloom filters**: Optionally, Parquet files may include a [Bloom filter](https://parquet.apache.org/docs/file-format/bloomfilter/) per column per row group. Readers can use these filters to efficiently check whether a value might exist and skip reading column data when it definitely doesn’t.


④ **Column chunk\-level min/max filtering**: Similar to page\-level stats, Parquet can [store](https://github.com/apache/parquet-format/blob/3ce0760933b875bc8a11f5be0b883cd107b95b43/src/main/thrift/parquet.thrift#L912) min/max statistics at the row group level per column. This allows readers to skip entire columns within a row group if they’re guaranteed to be irrelevant for a query.


So, how much of this does the ClickHouse Parquet reader support today?


The current Parquet reader in ClickHouse supports  

③ **[Bloom filters](https://clickhouse.com/blog/clickhouse-release-25-02#writing-bloom-filters-for-parquet)** (enabled via [input\_format\_parquet\_bloom\_filter\_push\_down](https://clickhouse.com/docs/operations/settings/formats#input_format_parquet_bloom_filter_push_down) setting) and  

④ **[row group–level min/max filtering](https://clickhouse.com/blog/clickhouse-release-23-08#reading-files-faster-michael-kolupaevpavel-kruglov)** (controlled via [input\_format\_parquet\_filter\_push\_down](https://clickhouse.com/docs/operations/settings/formats#input_format_parquet_filter_push_down) setting).


The upcoming native reader will add support for


① dictionary filtering and  

② page\-level min/max filtering.


In addition to these built\-in Parquet optimizations, the new native reader will also integrate ClickHouse\-specific I/O reduction techniques—most notably [PREWHERE](https://clickhouse.com/docs/optimize/prewhere) and [lazy materialization](https://clickhouse.com/blog/clickhouse-gets-lazier-and-faster-introducing-lazy-materialization)—to further reduce unnecessary reads and improve performance.


With that, we’ve covered how the current Parquet reader in ClickHouse achieves performance through parallelism and I/O reduction, and what improvements are on the horizon. Now that we understand how the current Parquet reader works, let’s see how it performs on real\-world analytical queries.


## Benchmarking Parquet query performance [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#benchmarking-parquet-query-performance)


In our previous [FastFormats](https://fastformats.clickhouse.com/) benchmark, we [evaluated](https://clickhouse.com/blog/clickhouse-input-format-matchup-which-is-fastest-most-efficient) how quickly different formats can be ingested into a ClickHouse table when the data is pushed (by a client) to the ClickHouse server.


This time, we look at the flip side: how fast can the ClickHouse query engine query these formats directly, without ever ingesting them:
![Blog-FormatsReads.012.png](/uploads/Blog_Formats_Reads_012_53fcc087da.png)


### Benchmark setup: Hardware, dataset, and software [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#benchmark-setup-hardware-dataset-and-software)


We used the same environment as in the FastFormats benchmark, with the following setup:


- **Hardware**: AWS EC2 m6i.8xlarge instance (32 vCPUs, 128 GiB RAM, 1 TiB gp3 SSD)
- **Dataset**: Anonymized [web analytics dataset](https://clickhouse.com/blog/clickhouse-input-format-matchup-which-is-fastest-most-efficient#dataset) (same as in [ClickBench](https://benchmark.clickhouse.com/))
- **ClickHouse version**: 25\.4\.1 running on Ubuntu Linux 24\.04


### Generating files from the dataset [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#generating-files-from-the-dataset)


We reused the same FastFormats [benchmarking mechanics](https://clickhouse.com/blog/clickhouse-input-format-matchup-which-is-fastest-most-efficient#benchmark-mechanics) to automatically [generate](https://github.com/ClickHouse/examples/blob/2f9f05f7b04a1da6269b6d2c41499a9fa336c25c/blog-examples/FastFormatReads/main.sh#L300) various combinations of:


- File size (and number of files)
- Format (e.g., Parquet, JSON, Arrow, etc.)
- Pre\-sorting (matching the [original table’s sorting key](https://github.com/ClickHouse/ClickBench/blob/f1178a21fbfdf3b2f9c71e7ed1602bb171d0cb2a/clickhouse/create.sql#L108), which benefits some queries)
- Compression (LZ4, ZSTD, or none)


Specifically, for each tested format, we [split](https://github.com/ClickHouse/examples/blob/2f9f05f7b04a1da6269b6d2c41499a9fa336c25c/blog-examples/FastFormatReads/main.sh#L31) the 100 million rows of the dataset into:


- 100 files, each with 1 million rows
- 6 file versions: all combinations of with/without [pre\-sorting](https://github.com/ClickHouse/examples/blob/2f9f05f7b04a1da6269b6d2c41499a9fa336c25c/blog-examples/FastFormatReads/main.sh#L46) and with/without [compression](https://github.com/ClickHouse/examples/blob/2f9f05f7b04a1da6269b6d2c41499a9fa336c25c/blog-examples/FastFormatReads/main.sh#L48) (LZ4, ZSTD)


### Running the queries: ClickBench for files [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#running-the-queries-clickbench-for-files)


We extended the benchmark to automatically [run](https://github.com/ClickHouse/examples/blob/2f9f05f7b04a1da6269b6d2c41499a9fa336c25c/blog-examples/FastFormatReads/main.sh#L227) all [43 official ClickBench queries](https://github.com/ClickHouse/ClickBench/blob/main/clickhouse/queries.sql) sequentially and in isolation on each generated file set, essentially running ClickBench (by [using](https://github.com/ClickHouse/examples/blob/2f9f05f7b04a1da6269b6d2c41499a9fa336c25c/blog-examples/FastFormatReads/run_queries.sh#L46) the [file table function](https://clickhouse.com/docs/sql-reference/table-functions/file)) over file\-based formats. [Like in ClickBench](https://github.com/ClickHouse/ClickBench/tree/main?tab=readme-ov-file#results-usage-and-scoreboards), each query was run [three times](https://github.com/ClickHouse/examples/blob/main/blog-examples/FastFormatReads/run_queries.sh#L24), with the OS page cache [cleared](https://github.com/ClickHouse/examples/blob/2f9f05f7b04a1da6269b6d2c41499a9fa336c25c/blog-examples/FastFormatReads/run_queries.sh#L40) once before the first run. The first run was used for the *cold runtime*; for the *hot runtime*, we took the minimum of the second and third runs.


### Query engine modes [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#query-engine-modes)


To access detailed runtime metrics beyond just execution time and memory usage, we ran all queries using the ClickHouse engine in server mode, i.e., with `clickhouse-client` connecting to a `clickhouse-server` process. While we could have used the engine standalone via `clickhouse-local` for file\-based queries, using the server allowed us to capture rich statistics via the [query log](https://clickhouse.com/docs/operations/system-tables/query_log) system table. Importantly, all queries were still executed directly over the file\-based data; no data was ingested into tables (except for the additional merge tree benchmark, see [below](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#apples-vs-oranges)). And regardless of the engine mode used, it’s always the same query engine and code path under the hood.


### What we measured [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#what-we-measured)


Using the query log, we [tracked](https://github.com/ClickHouse/examples/blob/2f9f05f7b04a1da6269b6d2c41499a9fa336c25c/blog-examples/FastFormatReads/metrics.sql) the following metrics for each query:


- **Runtime**: how long each query took to run
- **Memory usage**: peak memory usage during execution
- **Read rows**: number of rows read from the dataset
- **Read bytes**: total data read from the dataset
- **Threads participating**: number of threads involved in execution
- **Peak threads usage**: max number of threads running concurrently
- **DiskReadElapsedMicroseconds**: time spent [waiting on the read syscall](https://github.com/ClickHouse/ClickHouse/blob/9d60aa01a83346648eae5dc9572530388271f7b0/src/Common/ProfileEvents.cpp#L101)


### Real\-world performance: Parquet vs the rest [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#real-world-performance-parquet-vs-the-rest)


Let’s now see how the current Parquet reader’s parallel processing and I/O reduction optimizations translate into real\-world performance on representative analytical queries. We’ll start by looking at how a single representative ClickBench query performs, then zoom out to the full results across all 43 queries.


#### Apples vs. oranges [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#apples-vs-oranges)


For comparison, we also tested query performance on the same hardware using a native MergeTree table, with the query engine running in server mode.



> We’re aware that comparing Parquet to MergeTree isn’t entirely apples to apples. Parquet is a general\-purpose *file format*, while MergeTree is a purpose\-built *table engine* with deep integration and years of performance tuning. We don’t expect Parquet to outperform MergeTree.


A more direct comparison would be MergeTree vs. open table formats like Iceberg or Delta Lake, which build additional metadata and potentially indexing layers on top of Parquet. But that’s a topic for future posts. Here, we’re focusing on the foundations, how well ClickHouse queries Parquet files directly, and where performance stands today. As we continue investing in these Lakehouse foundations and aim for market\-leading performance, the gap will only keep closing.


#### Query 41: Runtime, parallelism, and I/O [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#query-41-runtime-parallelism-and-io)


The chart below compares 8 selected input formats by cold and hot runtime, number of concurrent processing threads (tracked via `peak_threads_usage` field in the query log), and, most importantly, the amount of data processed to run [ClickBench query 41](https://github.com/ClickHouse/ClickBench/blob/a5a02f0da97461506ac78aa5cea257362690c10a/clickhouse/queries.sql#L41) directly on file\-based data.


Query 41 is a typical analytical workload that filters, aggregates, sorts, and applies a LIMIT. For all formats, the dataset was stored pre\-sorted and ZSTD\-compressed on disk.


As a baseline—though it’s [apples vs. oranges](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#apples-vs-oranges)—we also include results for the same query run on a native MergeTree table with the same pre\-sorted, ZSTD\-compressed layout:


![Blog-FormatsReads.013.png](/uploads/Blog_Formats_Reads_013_83c1f3d7c3.png)
The chart’s main focus is on how much of the total data the query engine had to process to execute the query. The entries in the chart are sorted by cold runtime (fastest first), and three key observations stand out:


1. **MergeTree**: As ClickHouse’s [native format](https://clickhouse.com/docs/parts), MergeTree enables the most aggressive I/O reduction, leveraging the [full stack of optimizations](https://clickhouse.com/blog/clickhouse-gets-lazier-and-faster-introducing-lazy-materialization#the-building-blocks-of-io-efficiency-in-clickhouse), including [PREWHERE](https://clickhouse.com/docs/optimize/prewhere) and [lazy materialization](https://clickhouse.com/blog/clickhouse-gets-lazier-and-faster-introducing-lazy-materialization). In this query, only 19 MiB of data [was](https://github.com/ClickHouse/examples/blob/main/blog-examples/FastFormatReads/clickhouse/results/clickhouse_mergetree_100000000_1746193290.json) processed out of 10 GiB total, thanks largely to the [sparse primary index](https://clickhouse.com/docs/primary-indexes), which efficiently scans index entries for multiple compound primary key predicate columns at once and selects matching row groups based on the physical data order on disk. This results in extremely low query latency, just 30 milliseconds cold and 10 milliseconds hot. Which was [expected](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#apples-vs-oranges) for a highly optimized *table engine*.
2. **Parquet**: When querying Parquet files directly, ClickHouse already cuts I/O roughly in half using [predicate pushdowns](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#io-reduction-what-we-skip-and-how) (min/max stats and Bloom filters). However, current limitations—such as the absence of PREWHERE and lazy materialization—mean there is still room for improvement. Still, it performs well: in this query, 7 GiB out of 14 GiB [was](https://github.com/ClickHouse/examples/blob/main/blog-examples/FastFormatReads/results/parquet_100000000_1000000_sorted_zstd_1746194936.json) processed, and thanks to high parallelism (85 concurrent threads), it completed in 170 milliseconds cold and 140 milliseconds hot, roughly 5× slower than MergeTree, but still very fast for a *file format*.
3. Other formats: Most of the other input formats (e.g., **CSV**, **JSON**, **Arrow**) are primarily intended for easy data loading, or in the case of **Native**, for [efficient inter\-system data transport](https://clickhouse.com/blog/clickhouse-input-format-matchup-which-is-fastest-most-efficient), not for direct analytical querying. As a result, ClickBench query 41 took 30–43 s cold and 29–42 s hot. While it’s technically possible to implement I/O reduction techniques like column projection for these formats, ClickHouse doesn’t currently do so, because these formats aren’t typically considered for direct analytical use at scale. In practice, this means the full dataset (up to 21 GiB) often needs to be scanned and parsed.


#### All 43 queries: Total runtime comparison [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#all-43-queries-total-runtime-comparison)


To complete the picture, the chart below focuses on the total runtimes across *all* 43 ClickBench queries run directly over the same file formats as in the previous chart. To keep things concise, we report only the runtime *sums*. As before, the queried dataset was stored on disk pre\-sorted and ZSTD\-compressed for each format.


For comparison, [just out of curiosity](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#apples-vs-oranges), we again include a native MergeTree table using the same layout as the file\-based formats.



> All results in this chart use the pre\-sorted, ZSTD\-compressed version of each format, as this configuration consistently delivered the fastest runtimes across all tested combinations (with or without pre\-sorting, and with no compression, LZ4, or ZSTD). If you’re curious, we’ve published the full results for all combinations [here](https://github.com/ClickHouse/examples/tree/2f9f05f7b04a1da6269b6d2c41499a9fa336c25c/blog-examples/FastFormatReads/results), along with a [summary chart](/uploads/Blog_Formats_Reads_016_66ce48c3ea.png) for cold runtime *sums*.


![Blog-FormatsReads.014.png](/uploads/Blog_Formats_Reads_014_22d723e649.png)
The total cold runtime sums across all 43 ClickBench queries confirm the same performance pattern seen with query 41:


1. **MergeTree**: With just 113 GiB of data processed across all queries, MergeTree is by far the most efficient, completing in only 28 seconds cold, a result of aggressive I/O reduction using the full stack of native optimizations. As [expected](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#apples-vs-oranges).
2. **Parquet**: Despite currently lacking support for PREWHERE and lazy materialization, the current reader performs well. Thanks to metadata\-based predicate pushdowns and high parallelism (up to 162 concurrent processing threads for a query), it completes the full 43\-query workload in just 56 seconds cold, processing 468 GiB of data. That’s a substantial reduction from the 602 GiB that would have been scanned without any filtering if each of the 43 queries had read the full 14 GiB dataset from disk. While it’s nearly 2× slower than MergeTree (28 s cold), it still delivers fast performance for a *file\-based format*, demonstrating the effectiveness of Parquet’s built\-in optimizations like min/max stats and Bloom filters.
3. Other formats: Formats like **Native**, **Arrow**, **CSV**, and **JSONEachRow** show significantly higher I/O and slower runtimes, taking between 9 and 27 minutes cold to complete the full 43\-query workload. These formats lack predicate pushdowns and ClickHouse\-native I/O reduction features, typically requiring the entire dataset to be scanned and parsed. In comparison, that’s 10–30× slower than Parquet (56 s cold) and 20–60× slower than MergeTree (28 s cold).



> Not shown in the chart above, but perhaps most notably, the ClickHouse query engine, when querying Parquet files directly, outperforms many popular data stores even when they query their own native formats. On identical hardware, engines like Postgres, Elasticsearch, MongoDB, MySQL, and others take significantly longer in both [cold](https://benchmark.clickhouse.com/#eyJzeXN0ZW0iOnsiQWxsb3lEQiI6ZmFsc2UsIkFsbG95REIgKHR1bmVkKSI6ZmFsc2UsIkF0aGVuYSAocGFydGl0aW9uZWQpIjpmYWxzZSwiQXRoZW5hIChzaW5nbGUpIjpmYWxzZSwiQXVyb3JhIGZvciBNeVNRTCI6ZmFsc2UsIkF1cm9yYSBmb3IgUG9zdGdyZVNRTCI6ZmFsc2UsIkJpZ3F1ZXJ5Ijp0cnVlLCJCeUNvbml0eSI6ZmFsc2UsIkJ5dGVIb3VzZSI6ZmFsc2UsImNoREIgKERhdGFGcmFtZSkiOmZhbHNlLCJjaERCIChQYXJxdWV0LCBwYXJ0aXRpb25lZCkiOmZhbHNlLCJjaERCIjpmYWxzZSwiQ0hZVCI6ZmFsc2UsIkNpdHVzIjpmYWxzZSwiQ2xpY2tIb3VzZSBDbG91ZCAoYXdzKSI6ZmFsc2UsIkNsaWNrSG91c2UgQ2xvdWQgKGF6dXJlKSI6ZmFsc2UsIkNsaWNrSG91c2UgQ2xvdWQgKGdjcCkiOmZhbHNlLCJDbGlja0hvdXNlIChkYXRhIGxha2UsIHBhcnRpdGlvbmVkKSI6ZmFsc2UsIkNsaWNrSG91c2UgKGRhdGEgbGFrZSwgc2luZ2xlKSI6ZmFsc2UsIkNsaWNrSG91c2UgKFBhcnF1ZXQsIHBhcnRpdGlvbmVkKSI6ZmFsc2UsIkNsaWNrSG91c2UgKFBhcnF1ZXQsIHNpbmdsZSkiOnRydWUsIkNsaWNrSG91c2UgKHdlYikiOmZhbHNlLCJDbGlja0hvdXNlIjpmYWxzZSwiQ2xpY2tIb3VzZSAodHVuZWQpIjpmYWxzZSwiQ2xpY2tIb3VzZSAodHVuZWQsIG1lbW9yeSkiOmZhbHNlLCJDbG91ZGJlcnJ5IjpmYWxzZSwiQ3JhdGVEQiAodHVuZWQpIjpmYWxzZSwiQ3JhdGVEQiI6ZmFsc2UsIkNydW5jaHkgQnJpZGdlIGZvciBBbmFseXRpY3MgKFBhcnF1ZXQpIjpmYWxzZSwiRGFmdCAoUGFycXVldCwgcGFydGl0aW9uZWQpIjpmYWxzZSwiRGFmdCAoUGFycXVldCwgc2luZ2xlKSI6ZmFsc2UsIkRhdGFiZW5kIjpmYWxzZSwiRGF0YUZ1c2lvbiAoUGFycXVldCwgcGFydGl0aW9uZWQpIjpmYWxzZSwiRGF0YUZ1c2lvbiAoUGFycXVldCwgc2luZ2xlKSI6ZmFsc2UsIkFwYWNoZSBEb3JpcyI6ZmFsc2UsIkRyaWxsIjpmYWxzZSwiRHJ1aWQiOnRydWUsIkR1Y2tEQiAoRGF0YUZyYW1lKSI6ZmFsc2UsIkR1Y2tEQiAobWVtb3J5KSI6ZmFsc2UsIkR1Y2tEQiAoUGFycXVldCwgcGFydGl0aW9uZWQpIjpmYWxzZSwiRHVja0RCIjpmYWxzZSwiRWxhc3RpY3NlYXJjaCI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAodHVuZWQpIjpmYWxzZSwiR2xhcmVEQiI6ZmFsc2UsIkdyZWVucGx1bSI6dHJ1ZSwiSGVhdnlBSSI6ZmFsc2UsIkh5ZHJhIjpmYWxzZSwiU2FsZXNmb3JjZSBIeXBlciAoUGFycXVldCkiOmZhbHNlLCJTYWxlc2ZvcmNlIEh5cGVyIjpmYWxzZSwiSW5mb2JyaWdodCI6ZmFsc2UsIktpbmV0aWNhIjpmYWxzZSwiTWFyaWFEQiBDb2x1bW5TdG9yZSI6ZmFsc2UsIk1hcmlhREIiOmZhbHNlLCJNb25ldERCIjpmYWxzZSwiTW9uZ29EQiI6dHJ1ZSwiTW90aGVyRHVjayI6ZmFsc2UsIk15U1FMIChNeUlTQU0pIjp0cnVlLCJNeVNRTCI6dHJ1ZSwiT2N0b1NRTCI6ZmFsc2UsIk9wdGVyeXgiOmZhbHNlLCJPeGxhIjpmYWxzZSwiUGFuZGFzIChEYXRhRnJhbWUpIjpmYWxzZSwiUGFyYWRlREIgKFBhcnF1ZXQsIHBhcnRpdGlvbmVkKSI6ZmFsc2UsIlBhcmFkZURCIChQYXJxdWV0LCBzaW5nbGUpIjpmYWxzZSwiUGFyc2VhYmxlIChQYXJxdWV0LCBwYXJ0aXRpb25lZCkiOmZhbHNlLCJwZ19kdWNrZGIgKHdpdGggaW5kZXhlcykiOmZhbHNlLCJwZ19kdWNrZGIgKE1vdGhlckR1Y2sgZW5hYmxlZCkiOmZhbHNlLCJwZ19kdWNrZGIiOmZhbHNlLCJwZ19kdWNrZGIgKFBhcnF1ZXQpIjpmYWxzZSwiUG9zdGdyZVNRTCB3aXRoIHBnX21vb25jYWtlIjpmYWxzZSwicGdwcm9fdGFtIChwYXJxdWV0LCBsb2NhbCBzdG9yYWdlKSI6ZmFsc2UsInBncHJvX3RhbSAocGFycXVldCwgbG9jYWwsIHBhcmFsbGVsKSI6ZmFsc2UsInBncHJvX3RhbSAocGFycXVldCwgbG9jYWwgKyBjYWNoZSkiOmZhbHNlLCJwZ3Byb190YW0gKGZlYXRoZXIsIGxvY2FsICsgY2FjaGUpIjpmYWxzZSwiUGlub3QiOnRydWUsIlBvbGFycyAoRGF0YUZyYW1lKSI6ZmFsc2UsIlBvbGFycyAoUGFycXVldCkiOmZhbHNlLCJQb3N0Z3JlU1FMICh3aXRoIGluZGV4ZXMpIjp0cnVlLCJQb3N0Z3JlU1FMIjpmYWxzZSwiUXVlc3REQiI6ZmFsc2UsIlJlZHNoaWZ0IjpmYWxzZSwiU2VsZWN0REIiOmZhbHNlLCJTaWdMZW5zIjpmYWxzZSwiU2luZ2xlU3RvcmUiOmZhbHNlLCJTbm93Zmxha2UiOmZhbHNlLCJTcGFyayI6ZmFsc2UsIlNRTGl0ZSI6dHJ1ZSwiU3RhclJvY2tzIjpmYWxzZSwiVGFibGVzcGFjZSI6ZmFsc2UsIlRlbWJvIE9MQVAgKGNvbHVtbmFyKSI6ZmFsc2UsIlRpbWVzY2FsZSBDbG91ZCI6ZmFsc2UsIlRpbWVzY2FsZURCIChubyBjb2x1bW5zdG9yZSkiOmZhbHNlLCJUaW1lc2NhbGVEQiI6dHJ1ZSwiVGlueWJpcmQgKEZyZWUgVHJpYWwpIjpmYWxzZSwiVW1icmEiOmZhbHNlLCJVcnNhIjpmYWxzZSwiVmljdG9yaWFMb2dzIjpmYWxzZSwiWURCIjpmYWxzZX0sInR5cGUiOnsiQyI6dHJ1ZSwiY29sdW1uLW9yaWVudGVkIjp0cnVlLCJQb3N0Z3JlU1FMIGNvbXBhdGlibGUiOnRydWUsIm1hbmFnZWQiOnRydWUsImdjcCI6dHJ1ZSwic3RhdGVsZXNzIjp0cnVlLCJKYXZhIjp0cnVlLCJDKysiOnRydWUsIk15U1FMIGNvbXBhdGlibGUiOnRydWUsInJvdy1vcmllbnRlZCI6dHJ1ZSwic2VydmVybGVzcyI6dHJ1ZSwiQ2xpY2tIb3VzZSBkZXJpdmF0aXZlIjp0cnVlLCJlbWJlZGRlZCI6dHJ1ZSwiZGF0YWZyYW1lIjp0cnVlLCJZVHNhdXJ1cyI6dHJ1ZSwiYXdzIjp0cnVlLCJhenVyZSI6dHJ1ZSwiYW5hbHl0aWNhbCI6dHJ1ZSwiUnVzdCI6dHJ1ZSwic2VhcmNoIjp0cnVlLCJkb2N1bWVudCI6dHJ1ZSwiR28iOnRydWUsInNvbWV3aGF0IFBvc3RncmVTUUwgY29tcGF0aWJsZSI6dHJ1ZSwicGFycXVldCI6dHJ1ZSwidGltZS1zZXJpZXMiOnRydWUsImxvZ3MiOnRydWUsIlNpZ0xlbnMiOnRydWUsIm9ic2VydmFiaWxpdHkiOnRydWUsImRlZGljYXRlZCI6dHJ1ZX0sIm1hY2hpbmUiOnsiMTYgdkNQVSAxMjhHQiI6dHJ1ZSwiOCB2Q1BVIDY0R0IiOnRydWUsInNlcnZlcmxlc3MiOnRydWUsIjE2YWN1Ijp0cnVlLCJjNmEuNHhsYXJnZSwgNTAwZ2IgZ3AyIjp0cnVlLCJMIjp0cnVlLCJNIjp0cnVlLCJTIjp0cnVlLCJYUyI6dHJ1ZSwiYzZhLm1ldGFsLCA1MDBnYiBncDIiOmZhbHNlLCIxMiB2Q1BVIDQ4R0IiOnRydWUsIjEwIHZDUFUgNDBHQiI6dHJ1ZSwiMTJHaUIsIDEgcmVwbGljYShzKSI6dHJ1ZSwiOEdpQiwgMSByZXBsaWNhKHMpIjp0cnVlLCIxMkdpQiwgMiByZXBsaWNhKHMpIjp0cnVlLCIxMjBHaUIsIDIgcmVwbGljYShzKSI6dHJ1ZSwiMTZHaUIsIDIgcmVwbGljYShzKSI6dHJ1ZSwiMjM2R2lCLCAyIHJlcGxpY2EocykiOnRydWUsIjMyR2lCLCAyIHJlcGxpY2EocykiOnRydWUsIjY0R2lCLCAyIHJlcGxpY2EocykiOnRydWUsIjhHaUIsIDIgcmVwbGljYShzKSI6dHJ1ZSwiMTJHaUIsIDMgcmVwbGljYShzKSI6dHJ1ZSwiMTIwR2lCLCAzIHJlcGxpY2EocykiOnRydWUsIjE2R2lCLCAzIHJlcGxpY2EocykiOnRydWUsIjIzNkdpQiwgMyByZXBsaWNhKHMpIjp0cnVlLCIzMkdpQiwgMyByZXBsaWNhKHMpIjp0cnVlLCI2NEdpQiwgMyByZXBsaWNhKHMpIjp0cnVlLCI4R2lCLCAzIHJlcGxpY2EocykiOnRydWUsImM1bi40eGxhcmdlLCA1MDBnYiBncDIiOnRydWUsIkFuYWx5dGljcy0yNTZHQiAoNjQgdkNvcmVzLCAyNTYgR0IpIjp0cnVlLCJjNS40eGxhcmdlLCA1MDBnYiBncDIiOnRydWUsImM2YS40eGxhcmdlLCAxNTAwZ2IgZ3AyIjp0cnVlLCJYTCI6dHJ1ZSwiSnVtYm8iOnRydWUsIlB1bHNlIjp0cnVlLCJTdGFuZGFyZCI6dHJ1ZSwiMTYgdkNQVSAzMkdCIjp0cnVlLCJkYzIuOHhsYXJnZSI6dHJ1ZSwicmEzLjE2eGxhcmdlIjp0cnVlLCJyYTMuNHhsYXJnZSI6dHJ1ZSwicmEzLnhscGx1cyI6dHJ1ZSwiYzZhLjR4bGFyZ2UsIDcwMGdiIGdwMiI6dHJ1ZSwiUzIiOnRydWUsIlMyNCI6dHJ1ZSwiMlhMIjp0cnVlLCIzWEwiOnRydWUsIjRYTCI6dHJ1ZSwiTDEgLSAxNkNQVSAzMkdCIjp0cnVlLCJjNmEuNHhsYXJnZSwgNTAwZ2IgZ3AzIjp0cnVlLCIxNiB2Q1BVIDY0R0IiOnRydWUsIjQgdkNQVSAxNkdCIjp0cnVlLCI4IHZDUFUgMzJHQiI6dHJ1ZSwiNjQgdkNQVSAyNTZHQiI6dHJ1ZX0sImNsdXN0ZXJfc2l6ZSI6eyIxIjp0cnVlLCIyIjp0cnVlLCIzIjp0cnVlLCI0Ijp0cnVlLCI4Ijp0cnVlLCI5Ijp0cnVlLCIxNiI6dHJ1ZSwiMzIiOnRydWUsIjY0Ijp0cnVlLCIxMjgiOnRydWUsInNlcnZlcmxlc3MiOnRydWUsInVuZGVmaW5lZCI6dHJ1ZX0sIm1ldHJpYyI6ImNvbGQiLCJxdWVyaWVzIjpbdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZV19) and [hot](https://benchmark.clickhouse.com/#eyJzeXN0ZW0iOnsiQWxsb3lEQiI6ZmFsc2UsIkFsbG95REIgKHR1bmVkKSI6ZmFsc2UsIkF0aGVuYSAocGFydGl0aW9uZWQpIjpmYWxzZSwiQXRoZW5hIChzaW5nbGUpIjpmYWxzZSwiQXVyb3JhIGZvciBNeVNRTCI6ZmFsc2UsIkF1cm9yYSBmb3IgUG9zdGdyZVNRTCI6ZmFsc2UsIkJpZ3F1ZXJ5Ijp0cnVlLCJCeUNvbml0eSI6ZmFsc2UsIkJ5dGVIb3VzZSI6ZmFsc2UsImNoREIgKERhdGFGcmFtZSkiOmZhbHNlLCJjaERCIChQYXJxdWV0LCBwYXJ0aXRpb25lZCkiOmZhbHNlLCJjaERCIjpmYWxzZSwiQ0hZVCI6ZmFsc2UsIkNpdHVzIjpmYWxzZSwiQ2xpY2tIb3VzZSBDbG91ZCAoYXdzKSI6ZmFsc2UsIkNsaWNrSG91c2UgQ2xvdWQgKGF6dXJlKSI6ZmFsc2UsIkNsaWNrSG91c2UgQ2xvdWQgKGdjcCkiOmZhbHNlLCJDbGlja0hvdXNlIChkYXRhIGxha2UsIHBhcnRpdGlvbmVkKSI6ZmFsc2UsIkNsaWNrSG91c2UgKGRhdGEgbGFrZSwgc2luZ2xlKSI6ZmFsc2UsIkNsaWNrSG91c2UgKFBhcnF1ZXQsIHBhcnRpdGlvbmVkKSI6ZmFsc2UsIkNsaWNrSG91c2UgKFBhcnF1ZXQsIHNpbmdsZSkiOnRydWUsIkNsaWNrSG91c2UgKHdlYikiOmZhbHNlLCJDbGlja0hvdXNlIjpmYWxzZSwiQ2xpY2tIb3VzZSAodHVuZWQpIjpmYWxzZSwiQ2xpY2tIb3VzZSAodHVuZWQsIG1lbW9yeSkiOmZhbHNlLCJDbG91ZGJlcnJ5IjpmYWxzZSwiQ3JhdGVEQiAodHVuZWQpIjpmYWxzZSwiQ3JhdGVEQiI6ZmFsc2UsIkNydW5jaHkgQnJpZGdlIGZvciBBbmFseXRpY3MgKFBhcnF1ZXQpIjpmYWxzZSwiRGFmdCAoUGFycXVldCwgcGFydGl0aW9uZWQpIjpmYWxzZSwiRGFmdCAoUGFycXVldCwgc2luZ2xlKSI6ZmFsc2UsIkRhdGFiZW5kIjpmYWxzZSwiRGF0YUZ1c2lvbiAoUGFycXVldCwgcGFydGl0aW9uZWQpIjpmYWxzZSwiRGF0YUZ1c2lvbiAoUGFycXVldCwgc2luZ2xlKSI6ZmFsc2UsIkFwYWNoZSBEb3JpcyI6ZmFsc2UsIkRyaWxsIjpmYWxzZSwiRHJ1aWQiOnRydWUsIkR1Y2tEQiAoRGF0YUZyYW1lKSI6ZmFsc2UsIkR1Y2tEQiAobWVtb3J5KSI6ZmFsc2UsIkR1Y2tEQiAoUGFycXVldCwgcGFydGl0aW9uZWQpIjpmYWxzZSwiRHVja0RCIjpmYWxzZSwiRWxhc3RpY3NlYXJjaCI6dHJ1ZSwiRWxhc3RpY3NlYXJjaCAodHVuZWQpIjpmYWxzZSwiR2xhcmVEQiI6ZmFsc2UsIkdyZWVucGx1bSI6dHJ1ZSwiSGVhdnlBSSI6ZmFsc2UsIkh5ZHJhIjpmYWxzZSwiU2FsZXNmb3JjZSBIeXBlciAoUGFycXVldCkiOmZhbHNlLCJTYWxlc2ZvcmNlIEh5cGVyIjpmYWxzZSwiSW5mb2JyaWdodCI6ZmFsc2UsIktpbmV0aWNhIjpmYWxzZSwiTWFyaWFEQiBDb2x1bW5TdG9yZSI6ZmFsc2UsIk1hcmlhREIiOmZhbHNlLCJNb25ldERCIjpmYWxzZSwiTW9uZ29EQiI6dHJ1ZSwiTW90aGVyRHVjayI6ZmFsc2UsIk15U1FMIChNeUlTQU0pIjp0cnVlLCJNeVNRTCI6dHJ1ZSwiT2N0b1NRTCI6ZmFsc2UsIk9wdGVyeXgiOmZhbHNlLCJPeGxhIjpmYWxzZSwiUGFuZGFzIChEYXRhRnJhbWUpIjpmYWxzZSwiUGFyYWRlREIgKFBhcnF1ZXQsIHBhcnRpdGlvbmVkKSI6ZmFsc2UsIlBhcmFkZURCIChQYXJxdWV0LCBzaW5nbGUpIjpmYWxzZSwiUGFyc2VhYmxlIChQYXJxdWV0LCBwYXJ0aXRpb25lZCkiOmZhbHNlLCJwZ19kdWNrZGIgKHdpdGggaW5kZXhlcykiOmZhbHNlLCJwZ19kdWNrZGIgKE1vdGhlckR1Y2sgZW5hYmxlZCkiOmZhbHNlLCJwZ19kdWNrZGIiOmZhbHNlLCJwZ19kdWNrZGIgKFBhcnF1ZXQpIjpmYWxzZSwiUG9zdGdyZVNRTCB3aXRoIHBnX21vb25jYWtlIjpmYWxzZSwicGdwcm9fdGFtIChwYXJxdWV0LCBsb2NhbCBzdG9yYWdlKSI6ZmFsc2UsInBncHJvX3RhbSAocGFycXVldCwgbG9jYWwsIHBhcmFsbGVsKSI6ZmFsc2UsInBncHJvX3RhbSAocGFycXVldCwgbG9jYWwgKyBjYWNoZSkiOmZhbHNlLCJwZ3Byb190YW0gKGZlYXRoZXIsIGxvY2FsICsgY2FjaGUpIjpmYWxzZSwiUGlub3QiOnRydWUsIlBvbGFycyAoRGF0YUZyYW1lKSI6ZmFsc2UsIlBvbGFycyAoUGFycXVldCkiOmZhbHNlLCJQb3N0Z3JlU1FMICh3aXRoIGluZGV4ZXMpIjp0cnVlLCJQb3N0Z3JlU1FMIjpmYWxzZSwiUXVlc3REQiI6ZmFsc2UsIlJlZHNoaWZ0IjpmYWxzZSwiU2VsZWN0REIiOmZhbHNlLCJTaWdMZW5zIjpmYWxzZSwiU2luZ2xlU3RvcmUiOmZhbHNlLCJTbm93Zmxha2UiOmZhbHNlLCJTcGFyayI6ZmFsc2UsIlNRTGl0ZSI6dHJ1ZSwiU3RhclJvY2tzIjpmYWxzZSwiVGFibGVzcGFjZSI6ZmFsc2UsIlRlbWJvIE9MQVAgKGNvbHVtbmFyKSI6ZmFsc2UsIlRpbWVzY2FsZSBDbG91ZCI6ZmFsc2UsIlRpbWVzY2FsZURCIChubyBjb2x1bW5zdG9yZSkiOmZhbHNlLCJUaW1lc2NhbGVEQiI6dHJ1ZSwiVGlueWJpcmQgKEZyZWUgVHJpYWwpIjpmYWxzZSwiVW1icmEiOmZhbHNlLCJVcnNhIjpmYWxzZSwiVmljdG9yaWFMb2dzIjpmYWxzZSwiWURCIjpmYWxzZX0sInR5cGUiOnsiQyI6dHJ1ZSwiY29sdW1uLW9yaWVudGVkIjp0cnVlLCJQb3N0Z3JlU1FMIGNvbXBhdGlibGUiOnRydWUsIm1hbmFnZWQiOnRydWUsImdjcCI6dHJ1ZSwic3RhdGVsZXNzIjp0cnVlLCJKYXZhIjp0cnVlLCJDKysiOnRydWUsIk15U1FMIGNvbXBhdGlibGUiOnRydWUsInJvdy1vcmllbnRlZCI6dHJ1ZSwic2VydmVybGVzcyI6dHJ1ZSwiQ2xpY2tIb3VzZSBkZXJpdmF0aXZlIjp0cnVlLCJlbWJlZGRlZCI6dHJ1ZSwiZGF0YWZyYW1lIjp0cnVlLCJZVHNhdXJ1cyI6dHJ1ZSwiYXdzIjp0cnVlLCJhenVyZSI6dHJ1ZSwiYW5hbHl0aWNhbCI6dHJ1ZSwiUnVzdCI6dHJ1ZSwic2VhcmNoIjp0cnVlLCJkb2N1bWVudCI6dHJ1ZSwiR28iOnRydWUsInNvbWV3aGF0IFBvc3RncmVTUUwgY29tcGF0aWJsZSI6dHJ1ZSwicGFycXVldCI6dHJ1ZSwidGltZS1zZXJpZXMiOnRydWUsImxvZ3MiOnRydWUsIlNpZ0xlbnMiOnRydWUsIm9ic2VydmFiaWxpdHkiOnRydWUsImRlZGljYXRlZCI6dHJ1ZX0sIm1hY2hpbmUiOnsiMTYgdkNQVSAxMjhHQiI6dHJ1ZSwiOCB2Q1BVIDY0R0IiOnRydWUsInNlcnZlcmxlc3MiOnRydWUsIjE2YWN1Ijp0cnVlLCJjNmEuNHhsYXJnZSwgNTAwZ2IgZ3AyIjp0cnVlLCJMIjp0cnVlLCJNIjp0cnVlLCJTIjp0cnVlLCJYUyI6dHJ1ZSwiYzZhLm1ldGFsLCA1MDBnYiBncDIiOmZhbHNlLCIxMiB2Q1BVIDQ4R0IiOnRydWUsIjEwIHZDUFUgNDBHQiI6dHJ1ZSwiMTJHaUIsIDEgcmVwbGljYShzKSI6dHJ1ZSwiOEdpQiwgMSByZXBsaWNhKHMpIjp0cnVlLCIxMkdpQiwgMiByZXBsaWNhKHMpIjp0cnVlLCIxMjBHaUIsIDIgcmVwbGljYShzKSI6dHJ1ZSwiMTZHaUIsIDIgcmVwbGljYShzKSI6dHJ1ZSwiMjM2R2lCLCAyIHJlcGxpY2EocykiOnRydWUsIjMyR2lCLCAyIHJlcGxpY2EocykiOnRydWUsIjY0R2lCLCAyIHJlcGxpY2EocykiOnRydWUsIjhHaUIsIDIgcmVwbGljYShzKSI6dHJ1ZSwiMTJHaUIsIDMgcmVwbGljYShzKSI6dHJ1ZSwiMTIwR2lCLCAzIHJlcGxpY2EocykiOnRydWUsIjE2R2lCLCAzIHJlcGxpY2EocykiOnRydWUsIjIzNkdpQiwgMyByZXBsaWNhKHMpIjp0cnVlLCIzMkdpQiwgMyByZXBsaWNhKHMpIjp0cnVlLCI2NEdpQiwgMyByZXBsaWNhKHMpIjp0cnVlLCI4R2lCLCAzIHJlcGxpY2EocykiOnRydWUsImM1bi40eGxhcmdlLCA1MDBnYiBncDIiOnRydWUsIkFuYWx5dGljcy0yNTZHQiAoNjQgdkNvcmVzLCAyNTYgR0IpIjp0cnVlLCJjNS40eGxhcmdlLCA1MDBnYiBncDIiOnRydWUsImM2YS40eGxhcmdlLCAxNTAwZ2IgZ3AyIjp0cnVlLCJYTCI6dHJ1ZSwiSnVtYm8iOnRydWUsIlB1bHNlIjp0cnVlLCJTdGFuZGFyZCI6dHJ1ZSwiMTYgdkNQVSAzMkdCIjp0cnVlLCJkYzIuOHhsYXJnZSI6dHJ1ZSwicmEzLjE2eGxhcmdlIjp0cnVlLCJyYTMuNHhsYXJnZSI6dHJ1ZSwicmEzLnhscGx1cyI6dHJ1ZSwiYzZhLjR4bGFyZ2UsIDcwMGdiIGdwMiI6dHJ1ZSwiUzIiOnRydWUsIlMyNCI6dHJ1ZSwiMlhMIjp0cnVlLCIzWEwiOnRydWUsIjRYTCI6dHJ1ZSwiTDEgLSAxNkNQVSAzMkdCIjp0cnVlLCJjNmEuNHhsYXJnZSwgNTAwZ2IgZ3AzIjp0cnVlLCIxNiB2Q1BVIDY0R0IiOnRydWUsIjQgdkNQVSAxNkdCIjp0cnVlLCI4IHZDUFUgMzJHQiI6dHJ1ZSwiNjQgdkNQVSAyNTZHQiI6dHJ1ZX0sImNsdXN0ZXJfc2l6ZSI6eyIxIjp0cnVlLCIyIjp0cnVlLCIzIjp0cnVlLCI0Ijp0cnVlLCI4Ijp0cnVlLCI5Ijp0cnVlLCIxNiI6dHJ1ZSwiMzIiOnRydWUsIjY0Ijp0cnVlLCIxMjgiOnRydWUsInNlcnZlcmxlc3MiOnRydWUsInVuZGVmaW5lZCI6dHJ1ZX0sIm1ldHJpYyI6ImhvdCIsInF1ZXJpZXMiOlt0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlXX0=) runtimes to complete the same ClickBench workload over their preferred table layouts.


## [\#](/blog/[slug])


## Wrapping up [\#](/blog/clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics#wrapping-up)


This post took you deep inside the ClickHouse query engine to show how it queries Parquet, the columnar storage format that underpins open table formats like Iceberg and Delta Lake, and where its performance stands today.


We showed that the ClickHouse query engine is Lakehouse\-ready, not just by design, but almost by accident. Its ability to query external files directly, without prior ingestion, has been a core capability from the start.


ClickHouse has been optimized for Parquet for years. Our goal is simple: make it the fastest engine in the world for querying Parquet at scale.


The current Parquet reader already delivers strong performance, applying parallelism across every layer, from file reads and parsing to filtering, sorting, and aggregation, and using metadata like min/max statistics and Bloom filters to skip unnecessary work.


The performance gap is real: ClickHouse already queries Parquet files directly faster than many popular systems do with their own native formats.


And it’s getting faster. A new native Parquet reader is on the way, bringing support for dictionary\-based filtering, page\-level min/max stats, and ClickHouse\-specific optimizations like PREWHERE and lazy materialization.


Finally, we benchmarked Parquet alongside other file formats, and even against native MergeTree. It’s not a direct comparison (Parquet is a file format, MergeTree a purpose\-built table engine), but it’s telling: our query engine’s performance over Parquet came closest to MergeTree. That makes ClickHouse not just fast for Parquet, it makes it a solid foundation for Lakehouse architectures.


**This post is the first in a series. Next, we’ll explore how ClickHouse handles the higher layers of the Lakehouse stack. Yes, those layers already exist. ClickHouse isn’t getting ready for the Lakehouse, it’s already there. Stay tuned.**


![Blog-FormatsReads.015.png](/uploads/Blog_Formats_Reads_015_d3545f5f90.png)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
