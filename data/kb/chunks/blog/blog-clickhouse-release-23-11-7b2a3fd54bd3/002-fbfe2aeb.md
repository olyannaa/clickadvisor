---
source: blog
url: https://clickhouse.com/docs/en/whats-new/changelog#-clickhouse-release-2311-2023-12-06
topic: clickhouse-release-23-11
ch_version_introduced: '0.057'
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 8
---

code. We are pleased to announce that this feature has been significantly improved since its experimental release and is now production ready! To celebrate, our [YouTube celebrity Mark](https://www.youtube.com/playlist?list=PL0Z2YDlm0b3gcY5R_MUo4fT5bPqUQ66ep) has prepared a video: ### Column Statistics for PREWHERE [\#](/blog/clickhouse-release-23-11#column-statistics-for-prewhere)

#### Contributed by Han Fei [\#](/blog/clickhouse-release-23-11#contributed-by-han-fei)

[Column statistics](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree#column-statistics) are a new experimental feature that enables better query optimization in ClickHouse. With this feature, you can let ClickHouse create (and automatically update) statistics for columns in tables with a MergeTree\-family engine. These statistics are stored inside the table’s parts in a small single `statistics_(column_name).stat` file, which is a generic container file for different types of statistics for every column that has statistics enabled. This ensures lightweight access to column statistics. As of today, the only type of column statistics supported are [t\-digests](https://github.com/tdunning/t-digest). Additional types are [planned](https://github.com/ClickHouse/ClickHouse/issues/55065), though.

One first example where column statistics enable better optimizations is the column processing order in multi\-stage `PREWHERE` filtering. We sketch this with a figure:

![column_stats.png](/uploads/column_stats_7a0d061d29.png)
The query in the top left corner of the figure has a `WHERE` clause which consists of multiple `AND`\-connected filter conditions. ClickHouse has an optimization that tries to evaluate the filters with the least possible amount of data scanned. This optimization is called [multi\-stage PREWHERE](https://clickhouse.com/blog/clickhouse-release-23-02#multi-stage-prewhere--alexander-gololobov), and it is based on the idea that we can read the filter columns sequentially, i.e. column by column, and with every iteration, check only the blocks that contain at least one row that "survived" (\= matched) the previous filter. The number of blocks to evaluate for each filter decreases monotonically.

Not surprisingly, this optimization works best when the filter that produces the smallest number of surviving blocks is evaluated first \- in this case, ClickHouse needs to scan only a few blocks to evaluate the remaining filters. Of course, it is not possible to know how many blocks with matching rows survive each filter, so ClickHouse needs to make a guess to determine the optimal order in which the filters are executed. With column statistics, ClickHouse is able to estimate the number of matching rows / surviving blocks much more precisely, and therefore, multi\-stage PREWHERE as an optimization becomes more effective.
