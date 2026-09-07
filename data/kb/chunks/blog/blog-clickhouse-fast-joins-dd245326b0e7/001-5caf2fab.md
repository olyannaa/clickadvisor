---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-clickhouse-became-fast-at-joins-clickhouse
ch_version_introduced: '5.419'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 11
---

# How ClickHouse became fast at joins \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"How ClickHouse became fast at joins","description":"Over two years of focused join engineering, ClickHouse became 26× faster on the TPC\-H SF100 join\-heavy workload. Here’s how parallel hash joins, runtime filters, lazy column replication, and smarter join planning got us there.","image":"/uploads/How\_Click\_House\_became\_fast\_at\_joins\_3bccb2938f.jpg","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-06\-04T22:25:13\.828Z","dateModified":"2026\-06\-04T22:25:13\.675Z","author":{"@context":"https://schema.org","@type":"Person","name":"Tom Schreiber","url":"https://clickhouse.com/authors/tom\-schreiber","@id":"https://clickhouse.com/authors/tom\-schreiber\#person","image":"/uploads/tom\_schreiber\_headshot\_a0cb0ce627\.jpeg","jobTitle":"Principal Product Marketing Engineer at ClickHouse"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# How ClickHouse became fast at joins

![tom schreiber headshot](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber)Jun 3, 2026 · 20 minutes read
> **TL;DR**  
> 
> Over two years, ClickHouse became **26× faster** on join\-heavy analytical workloads. This post explains the engineering that made joins a first\-class strength.

## Two years of focused join engineering \#

ClickHouse is known for fast analytical queries, high compression, and real\-time performance at scale.

Over the last two years, one major engineering focus has been bringing that same performance profile to join\-heavy SQL queries.

At the [ClickHouse 24\.5 release webinar](https://www.youtube.com/live/dURnKjLuZLg?si=1Bx618RgGfAwN4iP&t=2216), Alexey Milovidov, inventor of ClickHouse, described the direction clearly:

> “From now on, you will see JOIN improvements in every ClickHouse release.”

The chart below shows what that looked like in practice.

![Blog-JOINS-improvements.001.png](/_next/image?url=%2Fuploads%2FBlog_JOINS_improvements_001_be4d4145a8.png&w=2048&q=75)

The first year laid the foundation: faster parallel hash join, smarter planning, aggressive filter pushdown, and local join reordering.

> By 25\.4, the same [TPC\-H](https://clickhouse.com/docs/getting-started/example-datasets/tpch) SF100 join\-heavy workload was already **4\.4× faster** than in 22\.4\.

The second year pushed much further. Between 25\.4 and 26\.4, a new wave of optimizer and execution improvements made the same workload another 6× faster with default settings.

> End to end, ClickHouse is now **26× faster** on TPC\-H SF100 than it was in 22\.4\.

This post explains how we got there. The [companion post](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift) shows what it unlocked: **ClickHouse Cloud now runs TPC\-H for less than a cent**, and competes head\-to\-head with Snowflake, Databricks, BigQuery, and Redshift on SF100\.

## Year one: building the foundation \#

A year ago, at [our first Open House user conference in San Francisco](https://clickhouse.com/blog/highlights-from-open-house-our-first-user-conference), ClickHouse join engineering lead, Robert Schulze, presented the first year of major join\-performance work.
