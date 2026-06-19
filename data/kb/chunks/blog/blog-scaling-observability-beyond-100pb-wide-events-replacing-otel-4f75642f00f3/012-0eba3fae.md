---
source: blog
url: https://clickhouse.com/blog/building-a-logging-platform-with-clickhouse-and-saving-millions-over-datadog
topic: scaling-our-observability-platform-beyond-100-petabytes-by-embracing-wide-events-and-replacing-otel
ch_version_introduced: '1728437333.011701'
last_updated: '2026-06-12'
chunk_index: 12
total_chunks_in_doc: 21
---

without ever needing to worry about breaking or reconfiguring the user interface. By combining HyperDX's powerful UI and session replay capabilities with LogHouse's massive data repository, we have created a unified and adaptable observability experience for our engineers.

![hypdx-1.png](/uploads/hypdx_1_061a1fbb5e.png)
![hyperdx-2.png](/uploads/hyperdx_2_32705dc4b0.png)
It is worth emphasizing that Grafana still has its place in our observability stack. Our internal Grafana\-based application has some distinct advantages, particularly in how it handles routing and query scoping. Users are required to specify the namespace (effectively a customer service) they intend to query. Behind the scenes, the application knows exactly where data for each service resides and can route queries directly to the appropriate ClickHouse instance within LogHouse. This minimizes unnecessary query execution across unrelated services and helps keep resource usage efficient.

This is especially important in our environment, where we operate LogHouse databases across many regions. As our previous blog post described, efficiently querying across these distributed systems is critical for performance and reliability. We’re currently exploring how we might push this routing logic to ClickHouse itself, allowing HyperDX to benefit from the same optimization..so stay tuned.

In addition to its routing capabilities, Grafana remains the home for many of our long\-standing dashboards and alerts, particularly those built on Prometheus metrics. These remain valuable, and migrating them is not currently a priority. For example, kube\_state\_metrics has almost become a de facto standard for cluster health monitoring. These high\-level metrics are well suited for alerting, even if they are not ideal for deep investigation. For now, they continue to serve their purpose effectively.

For now, the two tools serve complementary purposes and coexist effectively within our observability stack.

## Embracing high cardinality observability [\#](/blog/scaling-observability-beyond-100pb-wide-events-replacing-otel#embracing-high-cardinality-observability)

*Store everything, aggregate nothing*

The development of SysEx has brought more than just technical gains. It has driven a cultural shift in how we think about observability. By unlocking access to system tables that were previously unavailable, where only standard output logs had been captured, we have embraced a model centered on wide events and high cardinality data.

Some refer to this as Observability 2\.0\. **We simply call it LogHouse combined with ClickStack.**
