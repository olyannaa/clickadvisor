---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Asynchronous
topic: asynchronous-data-inserts-in-clickhouse-clickhouse
ch_version_introduced: '16.55'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 14
---

# Asynchronous Data Inserts in ClickHouse \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"Asynchronous Data Inserts in ClickHouse","description":"Read about how using asynchronous data inserts can simplify your scenario by shifting the batching of data from the client side to the server side.","image":"/uploads/header\_a48bd3b2ed.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-04\-24T13:48:45\.550Z","dateModified":"2026\-04\-24T13:48:45\.402Z","author":{"@context":"https://schema.org","@type":"Person","name":"Tom Schreiber and Tony Bonuccelli"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# Asynchronous Data Inserts in ClickHouse

![neutral avatar](/_next/image?url=%2Fuploads%2Fneutral_avatar_3226961af3.png&w=96&q=75)Tom Schreiber and Tony BonuccelliAug 1, 2023 · 30 minutes readClickHouse is [designed to be fast](https://clickhouse.com/docs/en/faq/general/why-clickhouse-is-so-fast) not just for queries but also for inserts. ClickHouse [tables](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family) are intended to receive millions of row inserts per second and store substantial (100s of Petabytes) volumes of data. A very high ingest throughput traditionally requires appropriate client\-side data [batching](https://clickhouse.com/docs/en/optimize/bulk-inserts).

In this post, we will describe the motivation and mechanics behind an alternative way of ingesting data with high throughput: ClickHouse asynchronous data inserts shift the batching of data from the client side to the server side and support use cases where client\-side batching is not feasible. We will look under the hood of asynchronous inserts and use an example application simulating realistic scenarios to demonstrate, benchmark, and tune traditional synchronous and asynchronous inserts with different settings.

## Synchronous data inserts primer \#

With traditional [inserts](https://clickhouse.com/docs/en/sql-reference/statements/insert-into) into tables of the [merge tree engine](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family) family, data is [speedily](https://clickhouse.com/docs/en/about-us/distinctive-features#real-time-data-updates) written to the database storage in the form of a new data [part](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree#mergetree-data-storage) synchronously to the reception of the insert query. The following diagram illustrates this:
![async_inserts_01.png](/_next/image?url=%2Fuploads%2Fasync_inserts_01_1eee7d9d75.png&w=2048&q=75)
When ClickHouse ① receives an insert query, then the query’s data is ② immediately (synchronously) written in the form of (at [least](https://clickhouse.com/docs/en/operations/settings/settings#settings-max_insert_block_size)) one new data part ([per](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse#poorly-chosen-partitioning-key) partitioning key) to the database storage, and after that, ③ ClickHouse acknowledges the successful execution of the insert query

In parallel (and in any order) ClickHouse [can](https://clickhouse.com/docs/en/operations/server-configuration-parameters/settings#max_thread_pool_size) receive and execute other insert queries (see ④ and ⑤ in the diagram above).

## Data needs to be batched for optimal performance \#
