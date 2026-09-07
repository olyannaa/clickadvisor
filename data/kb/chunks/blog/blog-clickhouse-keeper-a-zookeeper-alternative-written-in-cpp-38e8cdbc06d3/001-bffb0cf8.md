---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-keeper-a-zookeeper-alternative-written-in-c-clickhouse
ch_version_introduced: '4.11'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 14
---

# ClickHouse Keeper: A ZooKeeper alternative written in C\+\+ \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"ClickHouse Keeper: A ZooKeeper alternative written in C\+\+","description":"Read about why we built a resource\-efficient alternative for Zookeeper from scratch in C\+\+, what our next big step with it is, and how you can join the Keeper community.","image":"/uploads/cover\_b67663d3a5\.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2023\-09\-26T17:59:33\.922Z","dateModified":"2026\-03\-03T12:30:11\.646Z","author":{"@context":"https://schema.org","@type":"Person","name":"Tom Schreiber and Derek Chia"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# ClickHouse Keeper: A ZooKeeper alternative written in C\+\+

![neutral avatar white](/_next/image?url=%2Fuploads%2Fneutral_avatar_white_add9f20d0f.png&w=96&q=75)Tom Schreiber and Derek ChiaSep 27, 2023 · 27 minutes read## Introduction \#

ClickHouse is the fastest and most resource\-efficient open\-source database for real\-time applications and analytics. As one of its components, ClickHouse Keeper is a fast, more resource\-efficient, and feature\-rich alternative to ZooKeeper. This open\-source component provides a highly reliable metadata store, as well as coordination and synchronization mechanisms. It was originally developed for use with ClickHouse when it is deployed as a distributed system in a self\-managed setup or a hosted offering like CloudHouse Cloud. However, we believe that the broader community can benefit from this project in additional use cases.

In this post, we describe the motivation, advantages, and development of ClickHouse Keeper and preview our next planned improvements. Moreover, we introduce a reusable benchmark suite, which allows us to simulate and benchmark typical ClickHouse Keeper usage patterns easily. Based on this, we present benchmark results highlighting that ClickHouse Keeper uses **up to 46 times less memory than ZooKeeper ​​for the same volume of data while maintaining performance close to ZooKeeper**.

## Motivation \#

Modern [distributed systems](https://en.wikipedia.org/wiki/Distributed_computing) require a shared and reliable [information repository](https://en.wikipedia.org/wiki/Information_repository) and [consensus](https://en.wikipedia.org/wiki/Consensus_(computer_science)) system for coordinating and synchronizing distributed operations. For ClickHouse, [ZooKeeper](https://zookeeper.apache.org/) was initially chosen for this. It was reliable through its wide usage, provided a simple and powerful API, and offered reasonable performance.
