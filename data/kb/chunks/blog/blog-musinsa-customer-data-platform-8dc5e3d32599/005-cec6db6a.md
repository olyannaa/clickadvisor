---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-musinsa-scaled-its-audience-engine-with-clickhouse-cloud-and-reduced-tco-by-71-4-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 5
total_chunks_in_doc: 6
---

Previously, the team relied on Databricks Auto Loader, an external stage running on a separate Spark cluster. With [ClickPipes](https://clickhouse.com/cloud/clickpipes), ClickHouse Cloud’s native ingestion layer, they can integrate data directly into ClickHouse, reducing operational overhead and Databricks costs. ![](/_next/image?url=%2Fuploads%2Fmusinsa_2_cfe8497013.jpg&w=2048&q=75)

*Before and after: Databricks Auto Loader on an external Spark cluster gave way to ClickPipes, which ingests directly into ClickHouse Cloud and hands off to materialized views and storage.*

“ClickPipes enables real\-time data ingestion from a variety of sources,” Minyoung says. “With just a simple configuration, you can easily set up real\-time pipelines without the hassle of manual setup.”

> That ease of use becomes increasingly more important as we support more services. With ClickPipes, we can easily scale up with minimal effort, saving operational and overall ingestion costs.
> 
> 
> — Minyoung Choi, Data Engineer, Musinsa

## More time for what matters \#

With the migration to [ClickHouse Cloud](https://clickhouse.com/cloud), Musinsa’s storage costs fell sharply, compute scaled to each workload instead of one overloaded cluster, and ingestion moved inside ClickHouse.

“Ultimately, these improvements in ClickHouse Cloud helped us use fewer infrastructure resources and let us focus on our core business logic,” Minyoung says. “By simplifying our infrastructure, we were able to focus on developing CDP business logic and shift our attention from operational issues to product development.”

For anyone thinking about upgrading their database, her recommendation is clear: “Depending on your team's operational capabilities, if you're looking to reduce the burden of managing a self\-hosted ClickHouse, ClickHouse Cloud is a great choice.”

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-1488-get-started-today-sign-up&utm_blogctaid=1488)### Get started today

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
