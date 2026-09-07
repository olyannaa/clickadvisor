---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Building
topic: building-clickhouse-cloud-on-microsoft-azure-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 12
total_chunks_in_doc: 12
---

committed contract over a specified period. If your organization has a pre\-committed spend agreement with Azure, you may be able to apply some of that committed spend towards ClickHouse Cloud consumption on Azure. ## Takeaways \& conclusion \#

When we set out to build ClickHouse Cloud on Azure, we expected that, since we’d already built our service on AWS/GCP, we could apply a lot of the learning and architecture to make it easier for Azure. Although many of these did apply, there were quite a few complications and differences in setup that we didn’t expect. In this blog, we’ve discussed some of the important ones like resource organization, resource limits, network setup etc. We also had great help from the Microsoft Azure team in ensuring that we were able to design for scale while following Azure best practices.

We’re also looking forward to seeing some improvements from the Azure platform. For reliability's sake, each ClickHouse Cloud cluster has pods deployed in 3 AZs. However, not all regions in Azure support 3 AZs yet. In the future, this would be a feature from Azure that would help with reliability.

This blog was contributed by Vinay Suryadevara, Timur Solodovnikov, Smita Kulkarni \& Robert Schulze on the ClickHouse Cloud team.

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
