---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickPipes
topic: clickpipes-for-postgres-now-supports-failover-replication-slots-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 4
---

# ClickPipes for Postgres now supports failover replication slots \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"ClickPipes for Postgres now supports failover replication slots","description":"Learn about how failover\-ready replication slots keep Postgres CDC pipelines running without interruption.","image":"/uploads/clickpipes\_postgres\_failover\_banner\_8d8dc3675d.jpg","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2025\-11\-11T14:09:46\.662Z","dateModified":"2026\-03\-03T12:38:51\.682Z","author":{"@context":"https://schema.org","@type":"Person","name":"Kevin Biju Kizhake Kanichery","url":"https://clickhouse.com/authors/kevin\-biju\-kizhake\-kanichery","@id":"https://clickhouse.com/authors/kevin\-biju\-kizhake\-kanichery\#person","image":"/uploads/Image\_512x512\_4\_929da07148\.jpeg"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# ClickPipes for Postgres now supports failover replication slots

![kevin biju kizhake kanichery](/_next/image?url=%2Fuploads%2FImage_512x512_4_929da07148.jpeg&w=96&q=75)[Kevin Biju Kizhake Kanichery](/authors/kevin-biju-kizhake-kanichery)Nov 11, 2025 · 5 minutes read## Introduction \#

To continue providing maximum reliability and flexibility for all Postgres ClickPipes users, we have now added a toggle to allow creating a logical replication slot with failover enabled. This allows ClickPipes to work seamlessly with high\-availability (HA) to preserve replication slots post\-failover.

## Background \#

Postgres has a feature known as [hot standbys](https://www.postgresql.org/docs/current/hot-standby.html) that allows "read replicas" of a Postgres instance to be spun up for querying. Hot standbys recently gained the ability to perform logical decoding (introduced in Postgres 16, released 2023\), which allows users to move their CDC workloads off their primary instance. However, this was not enough to unlock high availability for CDC, as any slots created were only for that cluster and not replicated in any manner. In Postgres 17 (released 2024\), this was addressed by enabling logical replication failover, which essentially selects slots on the primary instance to be periodically synchronized to one or more standbys in a way that allows logical decoding to resume cleanly after a standby is promoted.

## Why would you want this? \#

Postgres is quintessentially a "core" database for transaction processing, and that has often necessitated high\-availability via standbys (as Postgres is a single\-writer design). However, as query workloads diversify, it is becoming increasingly common to replicate data from Postgres to other sources via CDC to leverage their strengths. Until very recently, while Postgres itself was HA, these pipelines were not. Logical replication failover now makes this a reality.

## Process \#
