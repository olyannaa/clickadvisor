---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Building
topic: building-an-enterprise-postgres-service-in-clickhouse-cloud-clickhouse
ch_version_introduced: auto
last_updated: '2026-11-09'
chunk_index: 4
total_chunks_in_doc: 5
---

managed by the underlying cloud infrastructure. For environments requiring stronger network isolation, [Private Link support](https://clickhouse.com/docs/cloud/managed-postgres/security#private-link) enables private connectivity between your VPC and the Postgres service, ensuring that database traffic does not traverse the public internet. ## Monitoring \#

The Postgres service comes with built\-in, out\-of\-the\-box metrics that provide visibility into both system health and database performance. Today, it includes 10\+ core metrics, allowing you to monitor CPU usage, memory consumption, disk I/O, storage growth, and network traffic, alongside Postgres\-specific signals such as connections, transaction throughput, cache hit ratios, row activity, and deadlocks.

Loading video...We’re actively expanding operational visibility, including Query Performance Insights and more comprehensive logging.

## Looking Ahead \#

As we execute on **our vision of delivering a unified data stack for OLTP and OLAP by combining Postgres and ClickHouse**, providing an enterprise\-grade experience is a given!

In the coming quarters, we’re expanding the platform’s enterprise readiness across reliability, performance, and operational depth. A few features include support for additional cloud providers (GCP), CDC v2 for close to sub\-second replication into ClickHouse, and Query Performance Insights (QPI) for deeper visibility into query behavior and database internals.

We’re also investing in core platform capabilities such as storage autoscaling, OpenAPI and Terraform support for IaC, one\-click fully managed Postgres\-to\-Postgres migrations, improved operational visibility (e.g., scaling progress), a built\-in intuitive SQL console and more.

Stay tuned.

### Try Postgres managed by ClickHouse

ClickHouse \+ Postgres has become the unified data stack for applications that scale. With Managed Postgres now available in ClickHouse Cloud, this stack is a day\-1 decision.

[Get access](https://clickhouse.com/cloud/postgres?loc=blog-cta-71-try-postgres-managed-by-clickhouse-get-access&utm_blogctaid=71)### Get started today

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

[View all Blogs](/blog)![img 5912](/_next/image?url=%2Fuploads%2FIMG_5912_4fde8778dc.jpg&w=750&q=75)Engineering### [What I learned from a month with WalShadow on ClickHouse Managed Postgres](/blog/a-month-with-walshadow-clickhouse-managed-postgres)

Hidehiko ASAHI · Nov 6, 2026![blog cover 1200x630 14](/_next/image?url=%2Fuploads%2FBlog_Cover_1200x630_14_380a4d0d49.png&w=750&q=75)Engineering### [ClickHouse release 26\.10](/blog/clickhouse-release-26-10)
