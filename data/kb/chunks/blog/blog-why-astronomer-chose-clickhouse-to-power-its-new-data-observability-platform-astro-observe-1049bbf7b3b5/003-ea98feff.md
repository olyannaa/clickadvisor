---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Why
topic: why-astronomer-chose-clickhouse-to-power-its-new-data-observability-platform-astro-observe-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 3
total_chunks_in_doc: 6
---

"This is a problem we care a lot about solving, because all of our customers run into this. Observe takes the root\-cause\-analysis process from hours to seconds, which frees up hours per week of those data engineers’ time."

Launched in late 2024, Astro Observe was designed to eliminate the guesswork. Instead of relying on scattered logs and manual troubleshooting, it provides a single, centralized view of workflow health. Teams can instantly see what failed, when it happened, and what downstream jobs were affected, without piecing together data from multiple systems. It also helps track SLAs and data freshness, sending alerts before minor issues snowball into major problems and ensuring key processes stay on schedule.

![astronomer.png](/_next/image?url=%2Fuploads%2Fastronomer_e9dc0a8229.png&w=2048&q=75)

By turning Airflow monitoring into a proactive process, Astro Observe reduces downtime and frees engineers from endless troubleshooting cycles. But for Astronomer, making this vision a reality required a database capable of handling billions of real\-time events with low query latency and minimal maintenance. That’s when they turned to [ClickHouse Cloud](https://clickhouse.com/cloud).

## Choosing the right database \#

Astronomer initially built a data lineage product on Amazon RDS for PostgreSQL, provisioning a separate database for each customer to keep workloads isolated. This setup worked fine at smaller stages, but as event volumes grew, it became harder to manage. Query performance degraded over time, particularly for analytical queries spanning large time ranges or requiring complex aggregations. The team also had to carefully limit the amount of stored data since retaining too much could negatively impact performance.

Around the same time, Julian met Ryan Delgado, Ramp’s Director of Engineering, at a ClickHouse event. They discussed Ramp’s recent adoption of ClickHouse for their real\-time analytics use cases. "We were looking for something that solved similar problems," Julian says. Based on a strong endorsement from Ryan and ClickHouse’s reputation for lightning\-fast query speeds, the Astronomer team decided to give it a try.

Their tests confirmed that ClickHouse could handle large\-scale event ingestion while maintaining sub\-second query performance, even across billions of records. Queries that had been computationally expensive in Postgres ran much faster, and the system supported high\-throughput workloads without the need for extensive tuning.

Along with improving performance, ClickHouse Cloud simplified operations, providing a fully managed service and eliminating the need for infrastructure management.
