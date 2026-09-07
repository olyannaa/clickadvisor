---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"What's
topic: what-s-new-in-clickstack-may-2026-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 7
total_chunks_in_doc: 10
---

information automatically shown when available. Alongside the layout changes, we reworked timeline rendering to provide more consistent axis labels and spacing across different zoom levels, making trace navigation smoother regardless of trace size. ## Service map improvements \#

Since launching the service map last year, we’ve spent a lot of time gathering feedback from users and understanding how service maps fit into real investigation workflows. The challenge has never been drawing a graph, but making the graph useful enough to become the place engineers start when something goes wrong, while also ensuring it remains efficient to compute at ClickHouse scale.

![service_map_improvements.png](/_next/image?url=%2Fuploads%2Fservice_map_improvements_7b89e2da0a.png&w=2048&q=75)

This month, we significantly expanded the information available within the service map. In addition to request counts and error rates, services now display throughput and p50, p95, and p99 latency, making it much easier to identify overloaded or degraded services directly from the topology view.

We also introduced filtering and focusing controls to make the map more practical for larger environments. Users can filter services using a service selector or a Lucene/SQL filter expression, reducing noise and narrowing the graph to the systems they care about. A new Focus action allows any service to become the center of the map, showing only that service and its immediate dependencies. For organizations with dozens or hundreds of services, these additions make it much easier to move from a broad architectural view to a targeted investigation.

## MCP server tool investments \#

Since announcing the ClickStack MCP server at Open House, we’ve continued expanding both the breadth and depth of its observability capabilities. While generic SQL interfaces are powerful, we continue to see that AI agents perform significantly better when given access to higher\-level observability primitives rather than being forced to reconstruct complex investigative workflows from raw queries. The ClickStack MCP server exposes those workflows directly, allowing agents to reason about traces, patterns, anomalies, dashboards, and operational artifacts using tools designed specifically for observability.
