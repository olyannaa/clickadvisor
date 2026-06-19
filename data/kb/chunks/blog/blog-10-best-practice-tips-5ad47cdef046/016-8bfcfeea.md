---
source: blog
url: https://clickhouse.com/blog/introducing-clickhouse-agent-skills
topic: top-10-best-practices-tips-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 16
total_chunks_in_doc: 18
---

With partitioning by month or year, each partition stays within a manageable size range where merging down to a single part is achievable, which is exactly the state where `FINAL` performs best. ## 10\. Optimize your joins [\#](/blog/10-best-practice-tips#optimize_your_joins)

Historically, JOINs in ClickHouse were something users were advised to approach with caution, and the common guidance was to avoid them where possible through denormalization, dictionaries, or materialized views. That advice made sense at the time, but significant engine\-level improvements have made JOINs increasingly viable for high\-concurrency production workloads. The introduction of the Analyzer (query planner) as the default query execution layer brought major improvements to join planning: ClickHouse 24\.4 introduced better predicate pushdown that can deliver 10x query improvements by pushing filter conditions to both sides of a JOIN, version 24\.12 gained the ability to automatically reorder two\-table joins to place the smaller table on the right\-hand side, and 25\.9 extended this to queries joining three or more tables. Combined with a wide selection of join algorithms to cover different memory and performance tradeoffs, JOINs in ClickHouse today are meaningfully more capable and easier to use correctly than they were even a year ago.

That said, JOINs still come with a cost in an analytical database, and a few principles are worth following. For real\-time workloads where millisecond latency matters, aim for a maximum of 3 to 4 joins per query. In addition, denormalization, dictionaries, or pre\-aggregated materialized views are tools worth considering for even faster query performance.

For static or slowly changing lookups it’s recommended to use dictionaries. When enriching a large table with data from a smaller reference table that doesn't change frequently, a dictionary will outperform a regular join. Dictionaries are loaded entirely into memory and accessed via `dictGet`, bypassing the hash join process entirely. On the Amazon reviews dataset enriched with customer metadata, the difference is significant: a regular `JOIN` on 150M rows ran in **2\.3 seconds**, a join against a dictionary table completed **1\.36 seconds**, and `dictGet` took **0\.86 seconds**; Nearly 3x faster than the baseline join, with no change to the underlying data.

![ClickHouse Blog Banner Tips-6.jpg](/uploads/Click_House_Blog_Banner_Tips_6_6243a66bcb.jpg)
## Wrapping Up [\#](/blog/10-best-practice-tips#wrapping_up)
