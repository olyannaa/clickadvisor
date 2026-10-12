---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Monitoring
topic: monitoring-temporal-cloud-with-clickstack-clickhouse
ch_version_introduced: auto
last_updated: '2026-10-12'
chunk_index: 3
total_chunks_in_doc: 4
---

on how to set up the integration are available](https://clickhouse.com/docs/use-cases/observability/clickstack/integrations/temporal-metrics), but the gist is once you have a Temporal Cloud API Key that has permission to read metrics, you create the configuration file in the OpenTelemetry Collector like this:

```
1receivers:
2  prometheus/temporal:
3    config:
4      scrape_configs:
5      - job_name: 'temporal-cloud'
6        scrape_interval: 60s
7        scheme: https
8        authorization:
9          type: Bearer
10          credentials_file: <TEMPORAL CLOUD API KEY PATH>
11        static_configs:
12          - targets: ['metrics.temporal.io']
13        metrics_path: '/v1/metrics'
14
15processors:
16  resource:
17    attributes:
18      - key: service.name
19        value: "temporal"
20        action: upsert
21
22service:
23  pipelines:
24    metrics/temporal:
25      receivers: [prometheus/temporal]
26      processors: [resource, memory_limiter, batch]
27      exporters: [clickhouse]
```
Copy commandOnce deployed, open the ClickStack UI, HyperDX, and navigate to the Metrics explorer. Search for metrics starting with `temporal_cloud` to confirm data is flowing. You can import the [pre\-built Temporal dashboard](https://clickhouse.com/docs/use-cases/observability/clickstack/integrations/temporal-metrics#dashboards) and immediately visualize Workflow success rates, Actions consumption against your limits, and Task Queue backlogs.

## What's Next \#

With Temporal metrics flowing into ClickStack, you can set up alerts on critical thresholds, build custom dashboards for your specific workflow patterns, and correlate workflow performance with the rest of your observability data.

For full configuration details and troubleshooting guidance, check out the [complete documentation](https://clickhouse.com/docs/use-cases/observability/clickstack/integrations/temporal-metrics).

Your durable workflows deserve scalable observability. With ClickStack and [Temporal Cloud](https://temporal.io/cloud) working together, you get both.

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
