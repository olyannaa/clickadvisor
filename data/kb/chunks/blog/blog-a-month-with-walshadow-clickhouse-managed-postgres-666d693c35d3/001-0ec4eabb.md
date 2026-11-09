---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"What
topic: what-i-learned-from-a-month-with-walshadow-on-clickhouse-managed-postgres-clickhouse
ch_version_introduced: auto
last_updated: '2026-11-09'
chunk_index: 1
total_chunks_in_doc: 15
---

# What I learned from a month with WalShadow on ClickHouse Managed Postgres \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"What I learned from a month with WalShadow on ClickHouse Managed Postgres","description":"Hidehiko ASAHI shares a month of WalShadow private\-preview testing, comparing replication latency with ClickPipes and checking data correctness, schema changes, and recovery.","image":"/uploads/IMG\_5912\_4fde8778dc.jpg","publisher":{"@type":"Organization","@id":"https://clickhouse.com/\#organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-11\-06T16:16:22\.200Z","dateModified":"2026\-11\-06T16:16:22\.094Z","author":{"@context":"https://schema.org","@type":"Person","name":"Hidehiko ASAHI","url":"https://clickhouse.com/authors/hidehiko\-asahi","@id":"https://clickhouse.com/authors/hidehiko\-asahi\#person","image":"/uploads/hidehiko\_asahi\_35c07c20a7\.png","jobTitle":"Database engineer and AWS Community Builder"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# What I learned from a month with WalShadow on ClickHouse Managed Postgres

![hidehiko asahi](/_next/image?url=%2Fuploads%2Fhidehiko_asahi_35c07c20a7.png&w=96&q=75)[Hidehiko ASAHI](/authors/hidehiko-asahi)Nov 6, 2026 · 20 minutes read
> This is a guest post from Hidehiko ASAHI, a database engineer at an IT company in Japan and an AWS Community Builder

> **Note:** Everything in this post was tested with WalShadow in Private Preview during September and October 2026, and all numbers reflect that environment at the time. Defaults and behavior may change before general availability.

## Summary \#

- When you analyze Postgres changes in ClickHouse, how low you can keep the replication delay is a key design consideration
- Batching writes at a fixed interval lets you trade replication delay against write frequency by tuning that interval, up to the write rate the pipe can process. Reading the WAL directly, which is possible because ClickHouse manages both sides of the stack, kept the delay nearly constant as I increased the write rate
- The application wrote only to Postgres, and replication continued through schema changes and operational events without any manual intervention. Using the destination tables comes with a few caveats that stem from how WalShadow works
- Issues I reported during the Private Preview were fixed, and I was able to confirm each fix using the same steps

## How this started \#

A while ago, I deployed the open\-source `walshadow` on EC2 myself and used it to replicate from Postgres to ClickHouse Cloud. A member of the ClickHouse team saw that and reached out, and I got the chance to try the managed WalShadow built into ClickHouse Managed Postgres in Private Preview.
