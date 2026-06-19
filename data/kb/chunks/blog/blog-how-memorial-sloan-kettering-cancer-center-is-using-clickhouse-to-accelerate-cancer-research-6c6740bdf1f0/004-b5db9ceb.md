---
source: blog
url: https://www.mskcc.org/
topic: how-memorial-sloan-kettering-cancer-center-is-using-clickhouse-to-accelerate-cancer-research
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 5
---

a six\-month period, the team rebuilt 20 endpoints that filter patients and samples, designing a denormalized schema in ClickHouse tailored to the endpoints' needs. They also used Sling to copy the MySQL schema into ClickHouse for rapid prototyping.

Their mantra during the POC was: "Do not return voluminous data to the web server — keep it in the database and process it there." This led them to create deeply nested SQL queries to push complex filtering and processing directly into ClickHouse. While MyBatis helped structure and modularize their SQL queries, testing and debugging remained a challenge. "A lot of times, when you need to debug something, you just need the whole query," Aaron explains. Without the function\-level unit testing available in Java, the team relied on integration testing with live databases to validate their logic and ensure system performance.

![clickhouse_legacy.png](/uploads/clickhouse_legacy_ab317e58d9.png)
These efforts paid off. By centralizing logic within ClickHouse and optimizing their approach, the team achieved "incredible performance gains" and made queries "10 times faster," Aaron says. The success of the POC showed ClickHouse's potential to transform cBioPortal, supporting near\-real\-time hypothesis testing and accelerating the pace of discovery.

## Scaling cancer research to new heights [\#](/blog/how-memorial-sloan-kettering-cancer-center-is-using-clickhouse-to-accelerate-cancer-research#scaling-cancer-research-to-new-heights)

Modern cancer research demands tools capable of keeping pace with the field's growing complexity. With ClickHouse powering key parts of cBioPortal, researchers have a platform that can handle vast amounts of genomic and clinical data with greater speed and efficiency.

"We've proven that the optimization works," Aaron says, noting that Clickhouse is now in production on cBioPortal's internal portals. "In the next few months, we'll be rolling it out to all the many people around the world who use cBioPortal locally at their institutions."

The team is also planning to fully transition the platform's remaining functionalities to ClickHouse, consolidating their data infrastructure and resolving lingering technical challenges like custom binning logic. This will eliminate the need for multiple databases, simplify cBioPortal's architecture, and deliver new and improved capabilities.

As genomic data continues to grow in volume and complexity, the implementation of ClickHouse will ensure that cBioPortal remains a critical tool for researchers across the globe. With their continued focus on innovation and optimization, Aaron and the MSK team are paving the way for even bigger breakthroughs in cancer research.
