---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-and-the-one-trillion-row-challenge-clickhouse
ch_version_introduced: '0.2441'
last_updated: '2026-09-07'
chunk_index: 14
total_chunks_in_doc: 14
---

provision our spot instances with a bid. We simply accepted the spot price for the current hour. If you really want to save a few cents, there is room to lower this price further! ### With MergeTree \#

Finally, we were curious as to how fast this data could be queried in a MergeTree table engine. While loading the data into a table also takes some time (it was [385s on a 300 core ClickHouse Cloud cluster](https://pastila.nl/?01d96b16/59c03d804e73ebc7e79a053a1de41cfd#nldroARcfqhWVlw5Yya3Dw==)), querying the resulting table with a full scan [takes only 16\.5s](https://pastila.nl/?0016d2c3/0573f785ef9cfd65c9385225eadad329#058Y2bMPjTswnEXqPUJ1mQ==) and is overwhelmingly faster than any results of querying parquet files (same cluster [achieves the query in 48s](https://pastila.nl/?000222ca/bca7e332e9269dfda7ac9e9440ca9650#bfqXVm9bEBOrnmrjoY1hHA==))! Note that such a cluster can easily be deployed through the [ClickHouse Cloud API](https://clickhouse.com/docs/en/cloud/manage/api/api-overview), used to run the query, and then be immediately terminated. Credit Alexey Milovidov for these timings.

## Conclusion \#

Expanding on the billion\-row challenge, we’ve shown how ClickHouse allows an even larger 1 trillion dataset to be queried in under 3 minutes for $0\.56!!

We welcome suggestions or alternatives to query this dataset faster and more cost\-efficiently.

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

Sai Srirampur · Sep 2, 2026[View all Blogs](/blog)
