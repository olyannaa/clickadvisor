---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"A
topic: a-look-back-at-2025-demo-development-at-clickhouse-clickhouse
ch_version_introduced: '52.2278'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 5
---

# A look back at 2025 demo development at ClickHouse \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"A look back at 2025 demo development at ClickHouse","description":"Have a look at some of the most notable demos we built this year, and how they help people feel the speed of ClickHouse through real, hands\-on examples.","image":"/uploads/demos\_review\_banner\_95f0a755cc.jpg","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2025\-12\-26T09:13:30\.305Z","dateModified":"2026\-03\-03T12:31:10\.083Z","author":{"@context":"https://schema.org","@type":"Person","name":"Lionel Palacin","url":"https://clickhouse.com/authors/lionel\-palacin","@id":"https://clickhouse.com/authors/lionel\-palacin\#person","image":"/uploads/lio\_headshot\_singapore\_7cc9852011\.jpg","jobTitle":"Senior Product Marketing Engineer at ClickHouse"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# A look back at 2025 demo development at ClickHouse

![lio headshot singapore](/_next/image?url=%2Fuploads%2Flio_headshot_singapore_7cc9852011.jpg&w=96&q=75)[Lionel Palacin](/authors/lionel-palacin)Dec 30, 2025 · 9 minutes readAs the year comes to an end and things slow down a bit, it feels like a good moment to zoom out and look back at the work we did as a team. I spend a lot of my time at ClickHouse working on demos, something I really enjoy, and I thought I would do a review of the most significant demos we built this year.

That idea was reinforced by a conversation I had with my colleague Tom Schreiber before the holidays. He [spends a lot of his time benchmarking ClickHouse](https://clickhouse.com/blog/what-really-matters-for-performance-lessons-from-a-year-of-benchmarks) and he shared a reflection that stuck with me:

> Benchmarks are great for measuring and understanding how fast ClickHouse is, but demos help people actually feel and experience that speed.

That feels very true. Nothing beats a real\-world example that shows how ClickHouse performance makes it possible to build impressive applications at scale. And it's not just us saying this. Customers like Tesla, which has ingested [over a quadrillion rows into ClickHouse](https://clickhouse.com/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse), or GitLab, [which serves sub\-second queries to tens of millions of users](https://clickhouse.com/blog/how-gitlab-uses-clickhouse-to-scale-analytical-workloads), would likely agree.

That's a common theme across the demos featured in this post, and a good place to start looking at what we built this year.

## StockHouse: Real\-time market analytics \#

[StockHouse](https://stockhouse.clickhouse.com/) is a real\-time market analytics application built on live stock and crypto data from [Massive APIs](https://massive.com/). It streams ticks over WebSocket APIs, ingests them into ClickHouse, and renders a dashboard built using [Perspective](https://perspective-dev.github.io/) that updates within milliseconds.
