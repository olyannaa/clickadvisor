---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"October
topic: october-2026-newsletter-clickhouse
ch_version_introduced: auto
last_updated: '2026-10-26'
chunk_index: 1
total_chunks_in_doc: 7
---

# October 2026 newsletter \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"October 2026 newsletter","description":"Welcome to the October 2026 ClickHouse newsletter, featuring CostBench results against BigQuery and Databricks, ClickHouse 26\.9, executable UDFs on ClickHouse Cloud, and the latest community news and events.","image":"/uploads/oct2026\_nl\_banner\_eb95f60ffc.png","publisher":{"@type":"Organization","@id":"https://clickhouse.com/\#organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-10\-15T10:07:35\.737Z","dateModified":"2026\-10\-15T10:07:35\.640Z","author":{"@context":"https://schema.org","@type":"Person","name":"Mark Needham","url":"https://clickhouse.com/authors/mark\-needham","@id":"https://clickhouse.com/authors/mark\-needham\#person","image":"/uploads/mark\_needham\_a17c08008e.png"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# October 2026 newsletter

![mark needham](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Oct 15, 2026 · 10 minutes readHello and welcome to another ClickHouse newsletter!

This month brings two more installments in the CostBench series, with Tom Schreiber and Lionel Palacin putting BigQuery and Databricks through their paces on a real\-time analytics workload.

The 26\.9 release adds new boundary conditions to the LIMIT clause that make log analysis easier, and a CREATE TOKEN statement for time\-limited credentials.

Elsewhere, executable user\-defined functions are now generally available on ClickHouse Cloud, and we have Postgres deep dives on memory safety and running on local NVMe storage.

## Featured community member: Hoang Minh V \#

This month's featured community member is Hoang Minh V, Senior Software Developer at shyftplan.

![](/_next/image?url=%2Fuploads%2Foct2026_nl_image1_126e4b6e6d.png&w=2048&q=75)

Hoang is a TU Munich alumnus and has had more than 100 pull requests merged into ClickHouse since May, 48 of which are in the 26\.9 release.

Much of his 26\.9 work went into [PromQL and the `TimeSeries` engine](https://clickhouse.com/blog/introducing-promql?utm_source=clickhouse&utm_medium=email&utm_campaign=202610-newsletter&ref=newsletter). He added a fast path for PromQL aggregations with an empty `by()` modifier, such as `sum by() (m)`, which skips a tag transformation over every input series. He also sped up `TimeSeries` reads and the `timeSeries*ToGrid` aggregate functions, stopped PromQL counting consecutive `NaN` samples as changes, and added support for quoted label names in grouping modifiers.

Outside PromQL, he made `LIMIT BY` stop reading input once a constant grouping key reaches its limit, and fixed more than a dozen edge cases in array, string, and URL functions.

➡️ [Connect with Hoang on LinkedIn](https://www.linkedin.com/in/hmv-io/)

## 26\.9 release \#

![](/_next/image?url=%2Fuploads%2Foct2026_nl_image2_22fff01e9d.png&w=2048&q=75)

The ClickHouse 26\.9 release extends the `LIMIT` clause with `AFTER` and `UNTIL` boundary conditions, which start and stop output based on values in the ordered result.
