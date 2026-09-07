---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Logging
topic: logging-metrics-and-distributed-tracing-in-net-with-opentelemetry-and-clickstack-clickhouse
ch_version_introduced: '2.21'
last_updated: '2026-09-07'
chunk_index: 8
total_chunks_in_doc: 10
---

![](/_next/image?url=%2Fuploads%2Fdotnet_otel_clickstack_jun2026_image4_d50ce7210a.png&w=2048&q=75) Click through to a group to see individual messages: ![](/_next/image?url=%2Fuploads%2Fdotnet_otel_clickstack_jun2026_image5_95764f6adb.png&w=2048&q=75) Then click on any of those to see the message properties, the trace waterfall, log context, as well as a map of the relevant services. **Log\-to\-Trace Correlation**

Every log line emitted during a traced request automatically carries the trace ID and span ID. In ClickStack, you can click any log line and jump directly to the parent trace, no manual correlation needed. The OTel log exporter handles this automatically.

That also works the other way around: when you're viewing a trace, ClickStack automatically surfaces the logs that were emitted during that trace's execution. And since our db calls are instrumented, that means we also get every database operation in the waterfall as well. This means you don't have to manually search for logs matching a trace ID; they're right there in context. This automatic correlation is one of the biggest advantages of the OTel \+ ClickStack pipeline — you get the full picture without any manual plumbing.

![](/_next/image?url=%2Fuploads%2Fdotnet_otel_clickstack_jun2026_image6_5ae8ddf1bb.png&w=2048&q=75)

### Metrics \#

You can build custom dashboards based on your metrics in ClickStack. The demo comes pre\-loaded with a dashboard allowing us to monitor our order processing service and providing easy access to warning and error logs.

![](/_next/image?url=%2Fuploads%2Fdotnet_otel_clickstack_jun2026_image7_c3dfddfd85.png&w=2048&q=75)

You can also define alerts based on these metrics. ClickStack supports [alerting integrations](https://clickhouse.com/docs/use-cases/observability/clickstack/alerts) with Slack, PagerDuty, or by generic webhook.

### Built\-in dashboards \#

ClickStack also comes with a number of dashboards out of the box. These allow you to monitor ClickHouse, surface the most relevant metrics for your services (auto\-discovered) and database calls, and let you explore Kubernetes events.

The service dashboard highlights your top endpoints, latency, and errors. The data here can be filtered using SQL or Lucene. The service map also automatically discovers the relationship between `order-api` and `payment-service` from the distributed traces. No manual configuration needed.

![](/_next/image?url=%2Fuploads%2Fdotnet_otel_clickstack_jun2026_image8_11e73e4068.png&w=2048&q=75)

Finally, the database tab shows stats for the database operations in our services. Because we're using the EF Core auto\-instrumentation, every query and save operation is captured with standard `db.*` attributes. You can see operation latencies, throughput, and error rates at a glance.

![](/_next/image?url=%2Fuploads%2Fdotnet_otel_clickstack_jun2026_image9_aac1cc77fe.png&w=2048&q=75)

## Production considerations \#
