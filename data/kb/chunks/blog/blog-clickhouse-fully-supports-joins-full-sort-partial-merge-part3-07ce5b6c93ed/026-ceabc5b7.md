---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-joins-under-the-hood-full-sorting-merge-join-partial-merge-join-mergingsortedtransform-clickhouse
ch_version_introduced: '11.559'
last_updated: '2026-09-07'
chunk_index: 26
total_chunks_in_doc: 27
---

this post’s join query runs. We ran always the same join query joining the same data, with the larger table on the right\-hand side on a node with 30 CPU cores (and therefore `max_threads` set to 30\): ![comparison.png](/_next/image?url=%2Fuploads%2Fcomparison_0078943d0f.png&w=2048&q=75)

① In this run the full sorting merge join skips the sorting and spilling stages because the physical row order of both joined tables matches the join key sort order. Resulting in the fastest execution time and significantly the lowest memory usage.
② With in\-memory sorting of both joined tables the full sorting merge join has the highest memory consumption and with ③ external sorting instead of in\-memory sorting the memory consumption is reduced for the sacrifice of reduced execution speed.
④ The partial merge join always sorts the data of the right table via external sorting. We see that this algorithm has the lowest memory usage from all the join query runs with external sorting. This is what this algorithm is optimized for at the expense of relatively low execution speed. The left table data is also always sorted block\-wise and in\-memory. But ⑤ we can see that the execution speed is worst if the physical row order of the left table does not match the join key order.

In our next post, we will describe ClickHouse’s fastest join algorithm: Direct join.

Stay tuned!

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

ClickHouse · Sep 3, 2026![blog banner from neon to clickhouse](/_next/image?url=%2Fuploads%2FBlog_Banner_From_Neon_to_Click_House_3ba00e031d.jpg&w=750&q=75)User stories### [From Neon Postgres to ClickHouse Managed Postgres](/blog/neon-to-clickhouse-managed-postgres)
