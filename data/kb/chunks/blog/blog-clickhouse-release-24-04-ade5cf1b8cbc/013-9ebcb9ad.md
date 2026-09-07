---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-24-4-clickhouse
ch_version_introduced: '0.656'
last_updated: '2026-09-07'
chunk_index: 13
total_chunks_in_doc: 14
---

KJFK │ N87527 │ UAL423 │ AAL1424 │ 12 └────────┴──────────┴───────────┴────────┴──────────┴────────────┘ 13 1410 rows in set. Elapsed: 1.937 sec. Processed 63.98 million rows, 2.52 GB (33.03 million rows/s., 1.30 GB/s.) 15Peak memory usage: 2.84 GiB. ``` Copy command 24\.4

```
1┌─origin─┬─leftDest─┬─rightDest─┬─reg────┬─callsign─┬─r.callsign─┐
2 1. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
3 2. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
4 3. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
5 4. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
6 5. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
7 6. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
8 7. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
9 8. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
10 9. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
1110. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
12    └────────┴──────────┴───────────┴────────┴──────────┴────────────┘
13
1410 rows in set. Elapsed: 0.762 sec. Processed 23.22 million rows, 939.75 MB (30.47 million rows/s., 1.23 GB/s.)
15Peak memory usage: 9.00 MiB.
```
Copy command
It's a little bit under three times quicker in 24\.4\.

If you’d like to learn more about how the JOIN performance improvements were implemented, [read Maksim Kita’s blog post](https://www.tinybird.co/blog-posts/clickhouse-joins-improvements) explaining everything.

That’s all for the 24\.4 release. We’d love for you to join us for the 24\.5 release call on 30 May. Make sure you [register so that you’ll get all the details for the Zoom webinar](https://clickhouse.com/company/events/v24-5-community-release-call).

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
