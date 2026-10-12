---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Building
topic: building-an-observability-solution-with-clickhouse-at-dash0-clickhouse
ch_version_introduced: '0.100000'
last_updated: '2026-10-12'
chunk_index: 14
total_chunks_in_doc: 15
---

result column data type as a marker. > As the ClickHouse team invests heavily in JOIN performance, we expect the above recommendations to change and become redundant. Always check the documentation and release posts for the latest improvements.

## Conclusion \#

Dash0's implementation of ClickHouse as the foundational storage layer for our OpenTelemetry\-native observability platform demonstrates the power of a thoughtful database architecture. By leveraging ClickHouse's columnar structure, compression capabilities, and flexible schema design, we've created a system that efficiently handles high\-cardinality telemetry data while maintaining performance at scale. Our approach of implementing strategic primary keys and carefully designing aggregation strategies has proven critical to achieving both speed and storage efficiency.

The operational decisions around storage tiers, and implementation wise the choices for sampling strategies, indexing techniques, and JOIN optimizations reflect our commitment to combine performance with supporting high data volume and cardinality. These engineering choices stem from deep expertise with both observability systems and ClickHouse itself. As we continue to evolve Dash0, the foundation provided by ClickHouse gives us confidence that our platform can scale with our customers' growing observability needs while maintaining the query performance necessary for effective system monitoring and troubleshooting.

### Get started today

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

[View all Blogs](/blog)![isam customer story blog cover white](/_next/image?url=%2Fuploads%2Fi_SAM_Customer_Story_blog_cover_white_9d07b4b15f.jpg&w=750&q=75)User stories### [How iSAM Funds built an options research platform for a 10,000x data problem with ClickHouse Cloud](/blog/isam-market-data-research-platform)

ClickHouse · Oct 9, 2026![clera customer story blog cover yellow](/_next/image?url=%2Fuploads%2FClera_Customer_Story_blog_cover_yellow_608efd06bc.png&w=750&q=75)User stories### [How we migrated Clera’s 500 GB production database to ClickHouse Managed Postgres overnight](/blog/clera-migrates-to-clickhouse-managed-postgres)

Daniel Wintermeyer · Oct 8, 2026![introducing jwt authentication in clickhouse cloud](/_next/image?url=%2Fuploads%2FIntroducing_JWT_authentication_in_Click_House_Cloud_22fed5798e.jpg&w=750&q=75)Product### [Introducing JWT authentication in ClickHouse Cloud](/blog/introducing-jwt-authentication-in-clickhouse-cloud)

ClickHouse team · Oct 8, 2026![why bigquery can t match clickhouse cloud for real time analytics](/_next/image?url=%2Fuploads%2FWhy_Big_Query_can_t_match_Click_House_Cloud_for_real_time_analytics_4baf359921.jpg&w=750&q=75)Engineering### [Why BigQuery can’t match ClickHouse Cloud for real\-time analytics](/blog/clickhouse-vs-bigquery-real-time-performance-per-dollar)

Tom Schreiber and Lionel Palacin · Oct 8, 2026[View all Blogs](/blog)## Follow us
