---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-sony-liv-uses-clickhouse-cloud-to-deliver-live-streaming-analytics-at-billion-row-scale-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 2
total_chunks_in_doc: 6
---

from how individual users are experiencing the stream, to how the service is holding up, to how ads are performing. As VP of Platform Engineering Vaibhav Gupta puts it, “Real\-time operational visibility and user analytics are business critical.”

We caught up with Vaibhav to learn how Sony LIV rebuilt their analytics infrastructure around [ClickHouse Cloud](https://console.clickhouse.cloud/). “The overall goal,” he says, “is to build a cloud\-native, real\-time, highly scalable data platform capable of supporting both business intelligence and operational decision\-making during massive live events.”

## A stack built for batch, not live events \#

Before ClickHouse, Sony LIV’s analytics ecosystem relied on a mix of traditional data warehouse systems, batch pipelines, Elasticsearch\-based observability workflows, BigQuery\-based analytics workloads, and multiple fragmented telemetry stores. “While these systems worked for specific use cases,” Vaibhav says, “we faced several limitations as our scale increased.”

The first was speed. As Vaibhav explains, most pipelines were optimized for batch analytics rather than ultra\-low latency streaming analytics. “During live sports events, operational teams need visibility within seconds, not minutes,” he says.

Cost was also a growing concern. As telemetry volumes climbed into the billions of events per day, storage and query costs “increased significantly,” Vaibhav says, particularly for high\-cardinality observability workloads and long\-retention analytics.

Fragmentation made both problems harder to solve. Playback telemetry, CDN metrics, application events, clickstream data, and ad\-tech events all lived in different systems. Piecing together a coherent picture during a live event meant stitching data from multiple sources, slowly, and often after the moment had passed.

Meanwhile, the team faced major query performance bottlenecks. Ad\-hoc analytical queries over large telemetry datasets, Vaibhav says, became “increasingly slow and expensive,” especially during peak traffic periods.

And then there was live sports traffic itself, which, as Vaibhav explains, doesn’t behave like normal traffic. “Traffic patterns can spike several multiples within minutes after a wicket, goal, or major match event. Existing systems struggled to scale efficiently for these patterns.”

## Finding a system that could do it all \#

The team knew they needed a better solution. They evaluated a handful of analytics and observability platforms, focusing on both operational telemetry and product analytics workloads.
