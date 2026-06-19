---
source: blog
url: https://en.wiktionary.org/wiki/data_lakehouse
topic: clickhouse-and-parquet-a-foundation-for-fast-lakehouse-analytics
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 17
---

data](https://clickhouse.com/docs/operations/settings/formats#output_format_parquet_row_group_size_bytes) (before compression). ② **Column chunks**: Each row group is further divided vertically into column chunks, one for each column in the dataset. Each chunk stores the values for that column across all rows in the row group.

③ **Data pages**: Inside each column chunk, the actual values are stored in data pages. By default, ClickHouse writes data pages of [1 MB](https://clickhouse.com/docs/operations/settings/formats#output_format_parquet_data_page_size) (before compression). A page stores a fixed or variable number of [encoded](https://parquet.apache.org/docs/file-format/data-pages/encodings/) and [compressed](https://parquet.apache.org/docs/file-format/data-pages/compression/) values, depending on the column’s data type and the encoding scheme used.

Note: For readability, the diagram above shows row groups containing six rows and data pages containing three values per column.

With the data layout clear, we can now look at how the ClickHouse query engine, together with the current Parquet reader, parallelizes data processing across available CPU cores to maximize query performance.

ClickHouse doesn’t just run anywhere and query anything, it also **parallelizes almost everything**, especially when querying Parquet. The following diagram shows how different layers of parallelism come together within the Parquet reader and the ClickHouse query engine during query execution:

![Blog-FormatsReads.006.png](/uploads/Blog_Formats_Reads_006_91953859fe.png)
① **Parallel prefetch threads**: Within a Parquet file, the Parquet file reader reads multiple row groups in parallel (*intra\-file*, *inter–row group parallelism*). By default, row group prefetching is [enabled](https://clickhouse.com/docs/operations/settings/formats#input_format_parquet_enable_row_group_prefetch) with four parallel prefetch threads (controlled by the [max\_download\_threads](https://clickhouse.com/docs/operations/settings/settings#max_download_threads) setting) and kicks in either when parsing reaches its maximum parallelism (explained below) or when parsing would otherwise stall, such as when data must first be loaded over a network connection.

② **Parallel parsing threads**: Parsing threads read and parse data from multiple row groups within the same file in parallel (*intra\-file, inter–row group parallelism*). If prefetching is active, they read from the prefetch buffer; otherwise, they read directly from the file. The number of parsing threads (across all file streams, see below) is controlled by the [max\_parsing\_threads](https://clickhouse.com/docs/operations/settings/settings#max_parsing_threads) setting, which by default matches the number of available CPU cores.

③ **Parallel file streams**: Different Parquet files are processed concurrently, each with their own parallel prefetch and parsing threads, to maximize throughput across files (*inter\-file parallelism*). The number of file streams is determined dynamically during query compilation (see below).
