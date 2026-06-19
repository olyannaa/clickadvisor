# Observing in style: How Poizon rebuilt its data platform with ClickHouse Enterprise Edition


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Observing in style: How Poizon rebuilt its data platform with ClickHouse Enterprise Edition

![](/_next/image?url=%2Fuploads%2Fpoizon_c5e3dcb446.jpg&w=96&q=75)PoizonMar 31, 2025 · 13 minutes read![Customer Story blog cover - yellow-2.png](/uploads/Customer_Story_blog_cover_yellow_2_509eee3c28.png)
[Poizon](https://www.dewu.com/) is one of China’s largest ecommerce platforms for luxury goods. Founded in 2015 as a marketplace for sneaker lovers, the platform has expanded over the years to include clothing, handbags, watches, electronics, and more, capturing the attention and loyalty of tens of millions of Gen\-Z and Alpha consumers.


But for Poizon, like many fast\-growing startups, success brought new challenges. The platform’s observability system generates petabytes of trace data and trillions of span records daily, requiring efficient real\-time processing and cost\-effective data storage solutions. Initially built on a traditional storage\-compute integrated architecture, Poizon’s infrastructure struggled to keep up with surging data volumes. Scaling compute and storage resources together became costly and inefficient, while cluster expansions introduced operational complexity and slowed performance during peak shopping periods.


To address these issues, Poizon’s team turned to AliCloud ClickHouse Enterprise Edition (also known as [ClickHouse Cloud](https://www.alibabacloud.com/en/product/clickhouse)) to rebuild their data infrastructure from the ground up. By adopting a storage\-compute separation architecture and integrating technologies like AutoMQ and Kafka with ClickHouse, they developed a cost\-efficient observability platform with the performance and scalability to keep up with their growing user base and data demands.


## Growing pains at scale [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#growing-pains-at-scale)


Poizon’s observability platform uses ClickHouse as the storage engine for trace index data in its distributed tracing system, managing tens of millions of trace records daily. From the beginning, ClickHouse’s exceptional performance and ability to deliver lightning\-fast query responses, even at scale, made it an ideal solution for real\-time analysis and monitoring.


![Poizon arc](/uploads/396323659_40586180_b4d0_4cf5_a28a_6fee1272293a_490159e965.png)
However, as Poizon’s business expanded and data volumes soared, the platform faced dual challenges: ensuring high\-performance, real\-time queries while optimizing storage costs, and managing the growing complexity of cluster maintenance. Despite its early success, the original self\-hosted, open\-source distributed architecture based on cloud disks showed limitations:


### Rising costs [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#rising-costs)


Since 2022, Poizon’s trace data volumes have grown from hundreds of terabytes to several petabytes daily, a 30\-fold increase. This surge intensified the cost pressures of managing hot and cold data storage efficiently, making the old system unsustainable.


### Poor scalability [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#poor-scalability)


As a leading ecommerce platform, Poizon sees huge traffic spikes during major shopping festivals like Singles Day (Double 11\) and 618\. Maintaining stable operations during these surges required frequent cluster expansions. However, these expansions were time\-intensive and disruptive, often requiring paused writes and extensive coordination. The resulting downtime and maintenance workloads made scalability a persistent challenge.


### Limited disaster recovery [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#limited-disaster-recovery)


To control costs, Poizon relied on a single\-replica storage strategy rather than multi\-replica redundancy. While this approach saved money and used fewer resources, it limited the system’s ability to recover from failures. In today’s environment, where stability and data security are paramount, this tradeoff became increasingly unsustainable.


### Complex write load balancing [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#complex-write-load-balancing)


Balancing write requests across nodes added another layer of operational complexity. Every cluster expansion required coordination with upstream services to rebalance data distribution across new nodes. Although this ensured the performance of the expanded cluster, it also required meticulous management, including fine\-tuning data allocation and maintaining balanced write loads, creating overhead for the engineering team.


## The case for ClickHouse Enterprise Edition [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#the-case-for-clickhouse-enterprise-edition)


For Poizon’s team, the question wasn’t whether ClickHouse could handle their real\-time observability needs. It was how to retain its performance advantages while addressing the mounting costs, scalability bottlenecks, and operational complexity.


Recognizing the limits of their self\-hosted setup, Poizon’s engineers began exploring ClickHouse Enterprise Edition (also known as ClickHouse Cloud). They were immediately drawn to its [separation of storage and compute](https://clickhouse.com/docs/en/guides/separation-storage-compute), which offers a more efficient way to manage computing and storage resources. Compared to the Community Edition, the Enterprise Edition introduces advanced features and architecture specially designed for high\-performance data processing, real\-time querying, and storage management.


![Poizon arc](/uploads/poizon_2_3f6c2dd8f5.png)
The core innovation of ClickHouse Enterprise Edition is its storage\-compute separation architecture. By decoupling compute resources from storage, this design offers greater system elasticity and scalability. Storage resources are centrally managed through shared storage solutions like Amazon S3 or Alibaba Cloud OSS, while compute nodes can independently scale up or down based on workload demands. This flexibility makes it easier for an ecommerce platform like Poizon to handle traffic surges during peak shopping events.


The Enterprise Edition also introduces a serverless computing model, allowing the platform to automatically adjust compute resource sizes based on actual load. Unlike traditional fixed\-resource models, this serverless architecture supports elastic scaling, allocating compute resources only when needed. The result is a major reduction in resource costs and better system stability, even during unexpected traffic spikes.


### SharedMergeTree table engine [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#sharedmergetree-table-engine)


The [SharedMergeTree engine](https://clickhouse.com/docs/en/cloud/reference/shared-merge-tree) in ClickHouse Enterprise Edition is a key component for implementing the storage\-compute separation architecture. It optimizes support for shared storage systems like Amazon S3, Google Cloud Storage, MinIO, and Alibaba Cloud OSS. Fully compatible with the community edition’s MergeTree engine, SharedMergeTree makes migrating easy by automatically converting table creation statements written for the community version into those specific to the Enterprise Edition’s engine (as shown in the diagram below). This allows businesses to migrate without the need for DDL modifications.



```

```
CREATE TABLE T (id UInt64, v String)
ENGINE = ReplacingMergeTree
ORDER BY (id);

SELECT engine
FROM system.tables
WHERE name = 'T';

┌─engine────────────────────┐
│ SharedReplacingMergeTree  │
└───────────────────────────┘
```


```

*Automatic conversion of table creation statements to the SharedMergeTree engine.*


Compared to traditional ClickHouse cluster architectures, the SharedMergeTree engine improves data storage and query performance in a number of areas:


#### Support for shared storage [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#support-for-shared-storage)


All data is stored in shared storage, with compute nodes accessing it directly for queries and analysis. This fully decouples storage from computation, removing the need for compute nodes to hold data replicas. The result is less redundancy and more efficient use of resources.


#### Stateless compute nodes [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#stateless-compute-nodes)


Compute nodes no longer store data replicas but instead pull data as needed from shared storage. This makes each compute node "stateless", improving scalability and fault tolerance. During traffic surges, new nodes can be added quickly and start working without the need for data redistribution or migration.


#### Simplified cluster management [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#simplified-cluster-management)


Users no longer need to manage traditional shards or distributed tables. With the SharedMergeTree engine, a single table creation is sufficient, streamlining the cluster management process, reducing maintenance overhead, and improving efficiency.


### Horizontal scaling [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#horizontal-scaling)


For a leading ecommerce platform like Poizon, maintaining high availability during peak traffic periods like holidays and special sales events requires a system that can scale quickly and reliably. ClickHouse Enterprise Edition, powered by the SharedMergeTree engine, delivers minute\-level horizontal scaling. Even during the scaling process, clusters remain fully operational, supporting ongoing read and write activities without disruption.


![Poizon arc](/uploads/Blog_Dewu_202412_V3_0_8cd44768eb.png)
*Metadata synchronization process during ClickHouse horizontal scaling.*


Here’s what horizontal scaling looks like in action:


1. New node (Server\-3\) addition: When more compute power is needed, a new node registers with the cluster’s metadata management system (e.g. Keeper) and starts monitoring metadata changes.
2. Metadata synchronization: The new node then syncs the latest metadata from Keeper without locking the cluster, ensuring other nodes continue operating without interruptions.
3. Immediate query handling: Once synchronization is complete, the new node instantly begins processing queries and accessing data from shared storage, eliminating downtime.


This process helps ClickHouse Enterprise Edition achieve elastic scaling under high load, ensuring the stability of the cluster and uninterrupted business operations.


## Poizon’s new data architecture [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#poizons-new-data-architecture)


With ClickHouse Enterprise Edition’s advanced features, Poizon’s observability platform has been fully optimized for writes, queries, disaster recovery, and elasticity. The result is a highly efficient and high\-performance distributed traceability system.


![Poizon arc](/uploads/poizon_4_f5d8e7bee2.png)
*Poizon’s new data architecture: optimized data processing with batch handling and span structures.*


Upgrading from the self\-hosted ClickHouse Community Edition to the Enterprise Edition has brought a host of meaningful changes and benefits, driven by its separation of storage and compute. One major improvement is the elimination of shards, which removes the need to manage data and write traffic across different nodes and local tables.


In the Enterprise Edition, business write operations now target the cluster as a whole, simplifying the write logic. This change has resolved the headache of balancing traffic and data distribution across shards, streamlining operations and improving efficiency.


### Write optimizations [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#write-optimizations)


ClickHouse Enterprise Edition has allowed Poizon’s team to optimize write operations in multiple ways, balancing workloads across nodes and improving performance and stability.


![poizon_chart_1.png](/uploads/poizon_chart_1_e10afa6785.png)
*Monitoring screen showing 'lines insert per second' in tens of thousands.*


#### Load balancing [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#load-balancing)


With load balancing (LB), write requests are evenly distributed across compute nodes to avoid overloading a single node, improving system stability. The LB uses a round\-robin (RR) mode under normal conditions. However, during cluster version upgrades with batch node restarts, or when a node undergoes fault reconstruction, it automatically switches to weighted round\-robin (WRR) mode to ensure seamless operations without affecting the overall cluster.


#### Performance gains [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#performance-gains)


The Enterprise Edition’s serverless architecture means Poizon can support write speeds of up to 20 million rows per second in a distributed traceability scenario. Large requests, such as writing 400,000 rows, have been optimized to be processed in around one second.


### Query optimization [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#query-optimization)


ClickHouse Enterprise Edition has also delivered improvements in query performance, speeding up response times while demanding fewer resources.


![poizon_char_2.png](/uploads/poizon_char_2_2682732722.png)
*Monitoring screen showing running queries, failed queries, failed inserts, and delayed queries.*


#### Parallel query [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#parallel-query)


The Parallel Replica feature distributes queries to multiple nodes for parallel processing, thereby improving efficiency. In specific scenarios, this parallel approach can increase query speeds by up to 2\.5 times. Overall, the query efficiency of Poizon’s new system is comparable to that of a self\-managed, open\-source ClickHouse setup.



```

```
SELECT trace_id, span_id, duration
FROM span_index
WHERE service = 'order-xxx'
  and startTime between '2024-11-23 16:00:00' and '2024-11-23 17:00:00'
ORDER BY duration DESC
LIMIT 0, 30
SETTINGS max_threads = 16, allow_experimental_parallel_reading_from_replicas = 1;
```


```

*Example query using parallel replicas to optimize distributed query performance.*


#### Index optimization [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#index-optimization)


By adjusting the ORDER BY fields and query order, Poizon’s new architecture ensures maximum index filtering and block optimization, eliminating unnecessary data scans and delivering faster, more efficient query responses.


### Disaster recovery [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#disaster-recovery)


Poizon’s new architecture is built to withstand adversity through distributed Keepers and shared object storage. The result is a more durable, resilient system:


#### Single\-node fault tolerance [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#single-node-fault-tolerance)


The cluster is configured with a default of three Keepers and at least a dual\-node architecture, where each compute node stores a full copy of the metadata. Compute nodes only manage the metadata, while core business data is stored in shared storage. This means a single node failure doesn’t affect data access, as the remaining nodes can continue to provide services.


#### High\-availability storage [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#high-availability-storage)


By using distributed object storage solutions like OSS, the platform achieves high data storage redundancy, improving the system’s ability to recover in case of hardware failures.


### Elastic by design [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#elastic-by-design)


ClickHouse Enterprise Edition’s elastic architecture enables real\-time scaling and major cost savings, solving two of the biggest challenges under Poizon’s previous self\-hosted setup.


![poizon_chart_3.png](/uploads/poizon_chart_3_f763cd487e.png)
*Elastic scaling in action: CCU adjustments based on workload.*


#### Second\-level elastic scaling [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#second-level-elastic-scaling)


The platform automatically adjusts compute resources based on real\-time business load. By monitoring CPU and memory usage, the system makes dynamic decisions and hot\-modifies Pod configurations. Scaling is instantaneous, without the need to restart services.


#### Pay\-as\-you\-go model [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#pay-as-you-go-model)


With the Enterprise Edition’s pay\-as\-you\-go model, compute resources scale up or down independently for each node based on real\-time business demands. This resolves concerns about uneven traffic pressure across nodes and avoids cost redundancy. The system supports granular elastic scaling, with adjustments made in units as small as 1 CCU (approximately 1 core and 4 GB of memory). Billing is synchronized with each scaling event and calculated on a per\-second basis, meaning businesses only pay for the resources they actually use.


On the storage side, the Enterprise Edition uses shared object storage in its pay\-per\-use model. Unlike traditional architectures that require reserving at least 20% of storage capacity to ensure cluster stability, this approach avoids the inefficiencies of uneven data distribution and redundant costs. Combined with the inherently lower price of object storage, this model has helped Poizon reduce storage expenses by more than 70% in large\-scale data scenarios.


## A data platform built for tomorrow [\#](/blog/observing-in-style-how-poizon-rebuilt-its-data-platform-with-clickhouse-enterprise-edition#a-data-platform-built-for-tomorrow)


Poizon's decision to rebuild their observability platform with ClickHouse Enterprise Edition (also known as ClickHouse Cloud) has driven measurable improvements in efficiency, scalability and resilience. With solutions like storage\-compute separation, serverless architecture, and the SharedMergeTree engine, they’ve achieved write speeds of up to 20 million rows per second and cut infrastructure costs by 60%. Ultimately, they’ve turned their biggest data challenges into opportunities, creating a platform that’s faster, smarter, and ready for growth.


As Poizon continues to expand, the strong foundation built with ClickHouse Cloud will ensure their data infrastructure keeps pace with their growing business. From handling petabyte\-scale datasets to supporting the biggest shopping events of the year, they’re poised to meet customer expectations and be a force in the luxury ecommerce market for years to come.


To learn more about ClickHouse and see how it can improve the scalability and performance of your team’s data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
