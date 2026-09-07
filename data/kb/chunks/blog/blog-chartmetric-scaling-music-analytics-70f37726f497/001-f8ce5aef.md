---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Behind
topic: behind-the-music-how-chartmetric-is-scaling-music-analytics-with-clickhouse-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 6
---

# Behind the music: How Chartmetric is scaling music analytics with ClickHouse \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"Behind the music: How Chartmetric is scaling music analytics with ClickHouse","description":"“ClickHouse works very well as part of our multi\-system data stack. It’s excellent for time\-series data, and the VersionedCollapsingMergeTree engine was a game\-changer for us, speeding up queries from 20 seconds in Snowflake to 1\.5 seconds in ClickHouse.”","image":"/uploads/Chartmetric\_User\_Story\_Issue\_1213\_6a102279cd.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-01\-08T14:17:18\.830Z","dateModified":"2026\-03\-03T12:31:12\.644Z","author":{"@context":"https://schema.org","@type":"Person","name":"ClickHouse","url":"https://clickhouse.com/authors/clickhouse","@id":"https://clickhouse.com/authors/clickhouse\#person","image":"/uploads/neutral\_avatar\_400804ae96\_5c370e757b.png"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# Behind the music: How Chartmetric is scaling music analytics with ClickHouse

![neutral avatar 400804ae96](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 8, 2026 · 10 minutes read## Summary

Chartmetric uses ClickHouse Cloud to deliver real\-time analytics on billions of rows of music, playlist, and engagement data. They migrated from Postgres and Snowflake to improve speed and reduce storage; queries now run 10\-15x faster at much lower cost. Today, ClickHouse powers a 5\.5B\-row playlist cache that ingests 15M\+ new rows daily, plus LLM\-facing queries using batched WHERE \+ IN filters and projections.

[Chartmetric](https://chartmetric.com/) tracks the pulse of the music industry. Every day, the platform ingests millions of rows of data from streaming services, social media, and music charts, powering dashboards for A\&R teams, reports for record labels, and insights for artists navigating their next move.

By 2024, that data footprint had ballooned into the billions and their systems weren’t scaling fast enough to keep up. [This past March](https://clickhouse.com/blog/chartmetric-uses-clickhouse-to-turn-artist-data-into-music-intelligence), lead engineer Peter Gomez shared how the team tackled the challenge by migrating time\-series workloads from Postgres and Snowflake to [ClickHouse Cloud](https://clickhouse.com/cloud). The move sped up slow queries and cut RDS storage by 10 TB.

Since then, the team has gone even further. ClickHouse now powers production workloads across the company, from LLM\-ready queries to a massive playlist cache pipeline that refreshes every five minutes. What began as a targeted performance fix has evolved into a foundational part of Chartmetric’s real\-time data stack.
