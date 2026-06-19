---
source: blog
url: https://en.wiktionary.org/wiki/data_lakehouse
topic: clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 17
---

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
