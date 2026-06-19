---
source: blog
url: https://clickhouse.com/blog/clickhouse-fully-supports-joins-part1
topic: choosing-the-right-join-algorithm
ch_version_introduced: '23.5'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 10
---

# Choosing the Right Join Algorithm

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Choosing the Right Join Algorithm

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber)Jun 27, 2023 · 22 minutes read![header.png](/uploads/header_051b18afd6.png)
This blog post is part of a series:

- [Join Types supported in ClickHouse](https://clickhouse.com/blog/clickhouse-fully-supports-joins-part1)
- [ClickHouse Joins Under the Hood \- Hash Join, Parallel Hash Join, Grace Hash Join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2)
- [ClickHouse Joins Under the Hood \- Full Sorting Merge Join, Partial Merge Join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-full-sort-partial-merge-part3)
- [ClickHouse Joins Under the Hood \- Direct Join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-direct-join-part4)

In the previous three posts, we did a deep dive on the 6 different join algorithms that have been developed for ClickHouse. In this final post, we will summarize and directly compare the execution times and memory usage of all ClickHouse join algorithms. Based on this, we will provide decision trees as well as a join type support overview that you can use for deciding which join algorithm fits best into your specific scenario.

## Overview of ClickHouse join algorithms [\#](/blog/clickhouse-fully-supports-joins-how-to-choose-the-right-algorithm-part5#overview-of-clickhouse-join-algorithms)

The following 6 join algorithms have been developed for ClickHouse so far:

- [Direct join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-direct-join-part4#direct-join)
- [Hash join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-part2#hash-join)
- [Parallel hash join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-part2#parallel-hash-join)
- [Grace hash join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2#grace-hash-join)
- [Full sorting merge join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-part3#full-sorting-merge-join)
- [Partial merge join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-part3#partial-merge-join)

These algorithms dictate the manner in which a join query is planned and executed. By [default](https://clickhouse.com/docs/en/operations/settings/settings#settings-join_algorithm), ClickHouse is using the direct or the hash join algorithm, based on used [join type](https://clickhouse.com/blog/clickhouse-fully-supports-joins-part1#join-types-supported-in-clickhouse) and [strictness](https://clickhouse.com/blog/clickhouse-fully-supports-joins-part1#join-types-supported-in-clickhouse) and [engine](https://clickhouse.com/docs/en/engines/table-engines) of the joined tables. Alternatively, ClickHouse can be configured to [adaptively](https://clickhouse.com/docs/en/about-us/distinctive-features#adaptive-join-algorithm) choose and dynamically change the join algorithm to use at runtime, depending on resource availability and usage: When [join\_algorithm](https://clickhouse.com/docs/en/operations/settings/settings#settings-join_algorithm) is set to `auto`, ClickHouse tries the hash join algorithm first, and if that algorithm’s [memory limit](https://clickhouse.com/docs/en/operations/settings/query-complexity#settings-max_bytes_in_join) is violated, the algorithm is switched on the fly to partial merge join. You can observe which algorithm was chosen via [trace logging](https://clickhouse.com/docs/knowledgebase/send_logs_level). ClickHouse also allows users to [specify](https://clickhouse.com/docs/en/operations/settings/settings#settings-join_algorithm) the desired join algorithm themselves. This chart gives an overview of the ClickHouse join algorithms based on their relative memory consumption and execution time:
![algorithms.png](/uploads/algorithms_caf4c65123.png)
