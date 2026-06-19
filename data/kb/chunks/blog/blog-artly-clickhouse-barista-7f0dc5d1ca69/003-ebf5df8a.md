---
source: blog
url: https://artly.coffee/
topic: scaling-craft-coffee-how-clickhouse-powers-artly-s-barista-bots
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 5
---

very well," Tong says. If the team wanted to analyze coupon usage across user cohorts or measure customer retention across orders and locations, they had to engineer workarounds—writing custom scripts, reshaping ingestion pipelines, or duplicating data across indexes.

The more they wanted to learn from their data, the more engineering time it took for a small team focused on growth, and that overhead became unsustainable. They needed a more flexible, resilient system built for the kinds of questions they actually wanted to ask.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## Why they chose ClickHouse [\#](/blog/artly-clickhouse-barista#why-they-chose-clickhouse)

When Artly started evaluating databases, ClickHouse quickly rose to the top. "We compared multiple OLAP databases, and in the end we chose ClickHouse," Tong says. He highlights its support for SQL as a key reason: "It’s very flexible and great for our use cases."

The new setup is powerful and refreshingly straightforward. AWS Glue moves data from DynamoDB to S3, and then into ClickHouse. Grafana sits on top for data visualization. This means no more convoluted ingestion pipelines, no more janky workarounds, and most importantly, no more limitations on what the team can ask of their data.

![artly-blog-3.png](/uploads/artly_blog_3_6cb8d7304d.png)
AWS Glue syncs data from DynamoDB to S3 to ClickHouse, with Grafana on top for dashboards.
"We can query in a very flexible way," Tong explains. "We can join tables. We can use nested queries. We can filter on multiple columns."

He describes ClickHouse as high\-performing and "very comprehensive." Unlike the time\-series databases they tested, ClickHouse supports both time\-series and non\-time\-series use cases. This is a big advantage for a team like Artly that works with robotic telemetry and customer purchase data side by side.

It's also been low\-maintenance from day one. "After we set up the platform, we didn't have to do any extra maintenance," Tong says. "We just monitor some metrics. It's very good. There's been no issue in our production environment."

"And the pricing is very affordable compared to other alternatives," he adds.

## Faster, cheaper, and more flexible [\#](/blog/artly-clickhouse-barista#faster-cheaper-and-more-flexible)
