---
source: blog
url: https://clickhouse.com/houseparty/vegas-2024
topic: clickhouse-at-aws-re-invent-2024-product-announcement-roundup
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 5
---

MSK. With Cross\-VPC resource access with AWS PrivateLink and VPC Lattice, you can share individual resources across VPC and account boundaries, or even from on\-premise networks without compromising on privacy and security when going over a public network.

![2_reinvent.png](/uploads/2a_reinvent_bbccb49ee1.png)
Supporting this new PrivateLink feature coincides with our most recent accreditation status as a AWS PrivateLink Service Ready Partner. We went through a stringent validation process with the AWS team to demonstrate our technical capabilities, verification of our solution and security processes, so you can be sure the integration is robust. Our new integration with PrivateLink and VPC Lattice further enhances our dedication to giving you the best and most secure ClickHouse experience on AWS.

👉 **To get started and set up a resource share, you can read the [announcement blog post](https://clickhouse.com/blog/clickpipes-crossvpc-resource-endpoints)** that walks you through how to configure Cross\-VPC resource access through PrivateLink and VPC Lattice.

## Dashboards (Beta) [\#](/blog/reinvent-2024-product-announcements#dashboards-beta)

![3_reinvent.png](/uploads/3_reinvent_b0ed0d0c7f.png)
We are excited to announce the Beta launch of Dashboards in ClickHouse Cloud!

With this new capability, you can use the most powerful real\-time database to visualize and share your data across your organization. ClickHouse Cloud’s SQL console allows users to query data using saved queries. With Dashboards, users can turn saved queries into visualizations, organize visualizations onto dashboards, and interact with dashboards using [query parameters](https://clickhouse.com/docs/en/sql-reference/syntax#defining-and-using-query-parameters).

We hope that ClickHouse Cloud native Dashboards will help you to expand access to your real\-time data.

👉 **To get started follow [the dashboards documentation](https://clickhouse.com/docs/en/cloud/manage/dashboards)**

## Query API Endpoints (GA) [\#](/blog/reinvent-2024-product-announcements#query-api-endpoints-ga)

![4_reinvent.png](/uploads/4_reinvent_7dd1562cc8.png)
We are excited to announce the GA release of Query API Endpoints in ClickHouse Cloud!

Already used in production by customers with thousands of active endpoints serving millions of requests daily, Query API Endpoints allow you to spin up RESTful API endpoints for saved queries in just a couple of clicks and begin consuming data in your application without wrangling language clients or authentication complexity. Our [blog post announcing the beta launch](https://clickhouse.com/blog/automatic-query-endpoints) describes the core functionality in greater detail, but since the initial launch, we have shipped a number of improvements including:

- Reducing endpoint latency, especially for cold\-starts
- Increased endpoint RBAC controls
- Configurable CORS\-allowed domains
- Result streaming
- Support for all ClickHouse\-compatible output formats
