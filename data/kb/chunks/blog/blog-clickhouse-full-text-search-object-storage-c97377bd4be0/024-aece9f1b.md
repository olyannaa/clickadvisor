---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Building
topic: building-high-performance-full-text-search-for-object-storage-clickhouse
ch_version_introduced: '13.501'
last_updated: '2026-09-07'
chunk_index: 24
total_chunks_in_doc: 25
---

on support for indexing JSON columns, faster evaluation of LIKE and regular expression patterns, improved text processing, and phrase search, where the index not only knows whether a token appears in a row, but also where it appears.

With that look at what’s coming next, let’s see what the new text index already delivers today, and what this means for ClickHouse Cloud users.

## What this means for ClickHouse Cloud users \#

After multiple iterations and significant performance work, the text index in ClickHouse now delivers the same high\-performance full\-text search whether data is stored on local disks or on object storage.

The new index layout favors sequential access patterns and allows many predicates to be resolved directly from the index without reading the indexed text columns from disk.

In ClickHouse Cloud, the new index benefits from the same architecture that powers other large\-scale workloads. [Parallel replicas](https://clickhouse.com/blog/clickhouse-parallel-replicas) can fan out full\-text queries across many nodes, the [distributed cache](https://clickhouse.com/blog/building-a-distributed-cache-for-s3) keeps hot index data close to compute, and shared object storage allows all nodes to access the same index files without reshuffling data.

The result is that full\-text search scales the same way as the rest of ClickHouse Cloud: add nodes, and queries get faster.

Stay tuned for the benchmarking post, where we compare the new text index with traditional text search engines and show why it replaces the older Bloom filter–based approach for text\-heavy workloads.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

---

Share this post

- Copy URL
- [![Y Combinator icon](/_next/static/immutable/media/ycombinator.37q2g-no9bowl.svg)](https://news.ycombinator.com/submitlink?u= "Share on Y Combinator")
- [![X icon](/_next/static/immutable/media/x.3nm91lx52ia7n.svg)](https://x.com/intent/tweet?text= "Share on X")
- [![Bluesky icon](/_next/static/immutable/media/bluesky.292c8t8kns7n1.svg)](https://bsky.app/intent/compose?text= "Share on Bluesky")
- [![Facebook icon](/_next/static/immutable/media/facebook.32ysyflv7kktz.svg)](https://www.facebook.com/sharer/sharer.php?u= "Share on Facebook")
- [![LinkedIn icon](/_next/static/immutable/media/linkedin.37911rnwi-sdg.svg)](https://www.linkedin.com/sharing/share-offsite/?url= "Share on LinkedIn")
### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!

## Recent posts

[View all Blogs](/blog)![clickhouse streaming http api](/_next/image?url=%2Fuploads%2FClick_House_Streaming_HTTP_API_7d6978a509.jpg&w=750&q=75)Product### [ClickHouse as a streaming HTTP API](/blog/clickhouse-streaming-http-api)

Mark Needham · Sep 5, 2026![dsn 1310 pipelined sql in clickhouse 26 8](/_next/image?url=%2Fuploads%2FDSN_1310_Pipelined_SQL_in_Click_House_26_8_96921fe4d8.jpg&w=750&q=75)Engineering### [Pipelined SQL in ClickHouse 26\.8](/blog/pipelined-sql-26.8)

Mark Needham · Sep 4, 2026![scheduled upgrades sep2026 banner](/_next/image?url=%2Fuploads%2Fscheduled_upgrades_sep2026_banner_b3cca8371f.jpg&w=750&q=75)Product### [Introducing Scheduled Upgrades in ClickHouse Managed Postgres](/blog/introducing-scheduled-upgrades-in-clickhouse-managed-postgres)
