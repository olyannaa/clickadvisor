---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"May
topic: may-2025-newsletter-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 3
total_chunks_in_doc: 6
---

May 29 - [AWS Summit Sydney](https://clickhouse.com/company/events/2025-06-APJ-AWSSummit-Sydney) \- June 4\-5 - [Tokyo Meetup \- AI Night!](https://www.meetup.com/clickhouse-tokyo-user-group/events/307689645/) \- June 5 - [KubeCon \+ CloudNativeCon Japan](https://clickhouse.com/company/events/2025-06-APJ-Tokyo-KubeCon-Japan) \- June 16\-17 - [AWS Summit Japan](https://clickhouse.com/company/events/2025-06-APJ-AWSSummit-Tokyo) \- June 25\-26 ## 25\.4 release \# ![0_may.png](/_next/image?url=%2Fuploads%2F0_may_8f18386369.png&w=2048&q=75)

It’s difficult to pick my favorite feature in the 25\.4 release, but if I must, I’d go for lazy materialization. This optimization defers reading column data until needed, resulting in much faster queries. More on that in the next section!

MergeTree tables on read\-only disks can now refresh their state and load new data parts, which effectively lets us create a ClickHouse\-native data lake. Also included in this release is CPU slot scheduling, which lets you cap the number of threads running concurrently for a given workload.

Finally, there’s a nice quality\-of\-life update in [clickhouse\-local](https://clickhouse.com/docs/operations/utilities/clickhouse-local): tables in the default database persist!

➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-25-04)

## ClickHouse gets lazier (and faster): Introducing lazy materialization \#

![1_may.png](/_next/image?url=%2Fuploads%2F1_may_2efada319d.png&w=2048&q=75)

The lazy materialization functionality has been given the Tom Schreiber treatment, i.e., a super in\-depth article breaking down how it works and the use cases it will help with.

Tom starts with ClickHouse’s existing building blocks of I/O efficiency and runs a real\-world query through them, layer by layer, until lazy materialization kicks in and dramatically optimizes performance.

➡️ [Read the blog post](https://clickhouse.com/blog/clickhouse-gets-lazier-and-faster-introducing-lazy-materialization)

## Why Microsoft Clarity chose ClickHouse \#

![2_may.png](/_next/image?url=%2Fuploads%2F2_may_9e6f34ff9b.png&w=2048&q=75)

Microsoft Clarity is a free analytics tool that helps website and app owners understand user interactions through visual snapshots and user interaction data. It provides heatmaps, session recordings, and insights.

When Microsoft decided to offer Clarity as a free public service, it needed to revamp its infrastructure. The original proof\-of\-concept using Elasticsearch and Spark couldn't handle the anticipated scale of millions of projects and hundreds of trillions of events. The system was slow, had low ingestion throughput, and would be prohibitively expensive at scale.

They turned to ClickHouse as a solution, and in the blog, they describe why they made that choice, what problems it has helped solve, and the challenges they encountered along the way.

➡️ [Read the blog post](https://clarity.microsoft.com/blog/why-microsoft-clarity-chose-clickhouse/)

## Introducing AgentHouse \#

![3_may.png](/_next/image?url=%2Fuploads%2F3_may_0f0842e7a2.png&w=2048&q=75)

Dmitry Pavlov announced AgentHouse, a chat\-based demo environment where you can interact with ClickHouse datasets using the Claude Sonnet Large Language Model.
