---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-we-configure-huge-pages-in-clickhouse-managed-postgres-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 4
total_chunks_in_doc: 5
---

| | 100 | 3\.06 GB | 58 MB | | 200 | 6\.12 GB | 111 MB | The `huge_pages = 'on'` behavior is equally visible. With no pool reserved, Postgres refuses to start and says why:

```
1FATAL:  could not map anonymous shared memory: Cannot allocate memory
2HINT:  This error usually means that PostgreSQL's request for a shared
3memory segment exceeded available memory, swap space, or huge pages.
```
Copy command
Throughput moves too, though less dramatically than the memory: select\-only pgbench at 100 clients ran 373,083 TPS on 4KB pages and 418,087 TPS on 2MB huge pages, a 12% difference on an otherwise identical box. The structural change is in the memory: page tables that scale linearly with connections versus page tables that stay flat.

## The takeaway \#

Huge pages turn shared\_buffers from a per\-connection page\-table tax into a flat, translation\-friendly cache. Reserving the pool before fragmentation, running `huge_pages = 'on'` so a broken setup fails at boot instead of degrading silently, and sizing the segment to the reservation with the numbers the postgres binary itself reports are what make the configuration hold in production rather than only on a fresh box.

### Try Postgres managed by ClickHouse

ClickHouse \+ Postgres has become the unified data stack for applications that scale. With Managed Postgres now available in ClickHouse Cloud, this stack is a day\-1 decision.

[Sign up](https://clickhouse.com/cloud/postgres?loc=blog-cta-1323-try-postgres-managed-by-clickhouse-sign-up&utm_blogctaid=1323)### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-global-cta&utm_blogctaid=0)

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
