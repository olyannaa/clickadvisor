# How ClickHouse Cloud uses AWS Graviton to boost performance and efficiency


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How ClickHouse Cloud uses AWS Graviton to boost performance and efficiency

![](/_next/image?url=%2Fuploads%2FImage_512x512_1_839aa54f62.jpeg&w=96&q=75)Kaushik Iska \& Francesco CiocchettiJan 27, 2025 · 8 minutes readAt ClickHouse, we place a strong emphasis on speed and efficiency. As developers of a high\-performance, open\-source OLAP database, our goal is to help users extract insights from their data as quickly as possible. This commitment to performance led us to explore ARM architecture, culminating in a recent migration to AWS Graviton processors. In this post, we provide a technical deep dive into that journey, highlighting the challenges we faced, the solutions we implemented, and the improvements in both performance and cost that resulted.


## A history of ARM support in ClickHouse [\#](/blog/graviton-boosts-clickhouse-cloud-performance#a-history-of-arm-support-in-clickhouse)


[Our journey with ARM began in 2016](https://pastila.nl/?00017b4c/03706598582b9fc616403aed35b1b1a4#acdJJpQRUnVGX2vykJKwTg==) with the first ClickHouse builds for AArch64\. Since then, we've been steadily expanding our support and optimization for this architecture.


Early efforts focused on ensuring basic compatibility and expanding platform support. By 2019, we had integrated cross\-compilation into our CI pipeline, allowing us to test on a wider range of ARM\-based systems. This led to benchmarks on various platforms, including AWS Graviton1, Raspberry Pi, Android, and Huawei servers.


In 2021, we broadened our support to include Apple M1 and FreeBSD AArch64, adding tests and packages to our CI to ensure consistent quality. Performance optimization became a key focus in 2022, with the implementation of ARM Neon optimizations and extensive benchmarks on AWS Graviton 2 and 3\. By the end of 2022, AArch64 had reached maturity, and on AWS Graviton3, its performance matched that of mainstream AMD64 processors – achieving production readiness with a full test suite.


Throughout 2023, we focused on tooling and developer experience, adding profiling and introspection tools for AArch64 builds. This paved the way for our 2024 benchmarks on AWS Graviton4 and the successful production rollout of AArch64 in ClickHouse Cloud.


Today, ClickHouse has comprehensive AArch64 support, encompassing:


- Automated builds, packages, and Docker images.
- Full functional test runs.
- Automated performance tests.
- JIT compilation for queries.
- ARM Neon optimizations.
- Query profiling and introspection.


## Why we migrated [\#](/blog/graviton-boosts-clickhouse-cloud-performance#why-we-migrated)


Our decision to migrate to AWS Graviton processors was driven by a desire to leverage the inherent advantages of ARM architecture. Specifically, we aimed to benefit from the better price performance and energy efficiency offered by ARM.


### Evolution of AWS Graviton [\#](/blog/graviton-boosts-clickhouse-cloud-performance#evolution-of-aws-graviton)


![0_graviton.png](/uploads/0_graviton_53874eab9c.png)
Since its debut in 2018, AWS Graviton has seen notable improvements across each generation. Graviton1 introduced 16 Cortex\-A72 cores, while Graviton2 expanded to 64 Neoverse\-N1 cores and faster DDR4 memory. In 2022, Graviton3 upgraded to Neoverse\-V1 cores and DDR5\-4800, refining both performance and efficiency. The latest Graviton4 adds 96 Neoverse\-V2 cores and 12 channels of DDR5\-5600 memory, further increasing throughput and reducing latency.


ARM’s instruction set architecture, characterized by efficient power consumption and streamlined execution, aligns well with the performance needs of data\-intensive applications like ClickHouse.


### Our pre\-migration landscape [\#](/blog/graviton-boosts-clickhouse-cloud-performance#our-pre-migration-landscape)


Before migrating, our AWS environment relied primarily on x86\-based instances like M5 and R5, with storage provided by object storage with ephemeral disks used for caching. Our network was configured for high bandwidth and low latency.


To establish a performance baseline, we meticulously analyzed our existing infrastructure, focusing on CPU utilization, memory usage, and I/O throughput. This analysis helped us identify potential bottlenecks and set realistic performance targets for the migration.


### Preparing for the Migration: A Calculated Approach [\#](/blog/graviton-boosts-clickhouse-cloud-performance#preparing-for-the-migration-a-calculated-approach)


We approached the migration with a focus on thoroughness and risk mitigation. This involved:


- **Compatibility Assessment:** We conducted a comprehensive evaluation to ensure that ClickHouse and all its dependencies were fully compatible with ARM architecture. We had to migrate some instances that were relying on intel only codecs such as `deflate_qpl` and `zstd_qat`.
- **Benchmarking Strategy:** To accurately measure the impact of the migration, we used a [ClickBench “like” benchmark](https://pastila.nl/?000b2ce8/0fd4f785b19f5ddf2f0a7f833ba65d48.html#h0NjIu5roX1bUTxLiJu6cA==) to test performance across both arm64 and amd64\.
- **Risk Analysis and Mitigation:** We proactively identified potential challenges, such as compatibility issues and performance regressions, and developed rollback procedures and contingency plans. We rolled\-out the change across cohorts to further minimize the risk.


## Executing the migration to Graviton [\#](/blog/graviton-boosts-clickhouse-cloud-performance#executing-the-migration-to-graviton)


The migration process involved several key steps:


- **Selecting Graviton Instances:** We carefully chose Graviton instance types based on performance requirements, cost\-performance ratio, and AWS capacity considerations. Due to limitations in the availability of larger Graviton instances, we opted for a mixed instance strategy, combining m7gd and m6gd instances using [AWS Auto Scaling Groups](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html) (ASG) and our custom ClickHouse autoscaler.
- **Addressing Instance Size and Architecture Jumps:** To ensure smooth autoscaling with mixed instance types, we adjusted memory allocation on m6gd instances to match m7gd, preventing unschedulable pods. We also implemented dynamic pod allocation, directing those under 236Gi to ARM instances using a webhook with node selection changes. Furthermore, we overprovisioned capacity and optimized autoscaler logic to manage the "architecture jump" where pods might initially be scheduled on larger x86 instances and then potentially downsized to smaller ARM instances.
- **Data Migration:** This was not necessary due to compute\-storage separation that is inherent to ClickHouse Cloud.


### Current State (Global, January 20, 2025\) [\#](/blog/graviton-boosts-clickhouse-cloud-performance#current-state-global-january-20-2025)


**Instance Type Distribution:**


- m7gd.16xlarge: 30\.03%
- m7g.4xlarge: 23\.06%
- r7g.xlarge: 15\.02%
- r7gd.2xlarge: 10\.63%
- m5d.24xlarge: 7\.14%
- m6gd.16xlarge: 2\.53%
- m5d.8xlarge: 2\.19%
- m5\.2xlarge: 3\.49%
- r6gd.2xlarge: 1\.12%
- Other (includes r5\.xlarge, r5d.2xlarge, m5\.xlarge, and similar): 4\.79%


**Architecture Distribution**:


- amd64: 17\.32%
- arm64: 82\.68%


*Percentage of ClickHouse server and keeper nodes (yellow \= arm64, blue \= amd64\)*


![1_graviton.png](/uploads/1_graviton_1071f52532.png)
*Server Node Distribution (AMD64 vs. ARM64, Excluding 24\.xlarge as it doesn’t have an equivalent in m6 and m7\), remaining 10% in Non\-Graviton Regions due to AWS Capacity*


![2_graviton.png](/uploads/2_graviton_0aa87f4587.png)
### Performance Benchmarking and Analysis: The Results [\#](/blog/graviton-boosts-clickhouse-cloud-performance#performance-benchmarking-and-analysis-the-results)


[Our comprehensive benchmarking plan](https://pastila.nl/?cafebabe/0ff5789e951d51d89cc7696a4d926ad1.html) included diverse workloads, simulating real\-world usage patterns. The results were compelling, we observed an overall \~25% improvement in performance across a wide range of queries.


![3_graviton.png](/uploads/3_graviton_8723f4b2c1.png)
Here are three case studies that demonstrate the performance improvements:


#### Case Study 1: CI Logs Cluster [\#](/blog/graviton-boosts-clickhouse-cloud-performance#case-study-1-ci-logs-cluster)


We tested performance on our CI logs cluster that collects data from all builds and tests \- a system processing approximately 2 million tests daily. The cluster handles:


- 4\.3 trillion rows
- 65 TiB of compressed data
- 1\.39 PiB of uncompressed data


Testing a heavy query that scanned over 1 trillion records showed:


- Pre\-migration: 285\.45 million rows/s, 99\.90 GB/s
- Post\-migration: 316\.99 million rows/s, 110\.93 GB/s
- Result: \~10% performance improvement


The improvement was modest primarily due to being network\-bound when reading from S3, we should rather have used network\-optimized instances.


#### Case Study 2: Public Demo Performance [\#](/blog/graviton-boosts-clickhouse-cloud-performance#case-study-2-public-demo-performance)


Our public demo ([adsb.exposed)](https://adsb.exposed/)) showed more dramatic improvements when comparing:


- r6i.metal: 16\.27 GB/sec
- r8g.24xlarge (Graviton 4\): 26\.71 GB/sec
- Result: 64% performance improvement


#### Case Study 3: ClickBench Performance [\#](/blog/graviton-boosts-clickhouse-cloud-performance#case-study-3-clickbench-performance)


We ran ClickBench \- a standardized benchmark that simulates analytics workloads. Testing used 32 concurrent users with the command `clickhouse-benchmark -c32 -i1000 < queries.sql`. [You can look at the results here](https://pastila.nl/?000b1ba6/c224ddf960900f4f2d0d9e100cef5445.html).




| Instance | QPS | Performance vs Base |
| --- | --- | --- |
| r7i.8xlarge | 2,800 | baseline |
| r7g.8xlarge | 3,500 | \+25% |
| r8g.8xlarge | 4,595 | \+64% |


ClickBench is open and available at <https://benchmark.clickhouse.com/hardware>. Anyone can run these benchmarks on their own hardware and submit results to compare different system configurations. [This presentation](https://presentations.clickhouse.com/2024-aws/index.html) and this [Twitch stream](https://m.twitch.tv/videos/2152236905) also goes over this in more detail.


Additional external benchmarks can be seen here as well: [https://www.phoronix.com/review/aws\-graviton4\-benchmarks/6](https://www.phoronix.com/review/aws-graviton4-benchmarks/6).


#### Graviton4: Performance Improvement from Graviton3 [\#](/blog/graviton-boosts-clickhouse-cloud-performance#graviton4-performance-improvement-from-graviton3)


Our testing on r8g instances in us\-east\-1 comparing Graviton4 to Graviton3 showed:


- 23\-30% better performance on average across query types
- Up to 76% improvement on certain queries
- Performance scaled with additional cores, though not linearly across all workloads


Tests used both r8g.8xlarge and r8g.24xlarge instances to evaluate per\-core performance and scaling characteristics. The improvements were consistent across various query patterns, from simple aggregations to complex analytical workloads.


These results from Graviton4 show significant performance gains beyond our initial migration to ARM architecture.


## Conclusion [\#](/blog/graviton-boosts-clickhouse-cloud-performance#conclusion)


Our journey to AWS Graviton highlights how ARM architecture can substantially improve both performance and efficiency for a data\-intensive workload like ClickHouse. From validating compatibility and revising autoscaling strategies to adjusting CI/CD for multi\-architecture builds, each phase demanded careful planning and execution. The outcome—better query performance, reduced operating costs, and a more adaptable infrastructure—has strengthened our conviction that ARM\-based solutions are ready for prime time.


We hope this technical overview provides useful insights for anyone exploring a similar migration. For those considering an ARM\-based transition, we welcome your questions and feedback, and look forward to continuing the conversation as we further refine and optimize our AArch64 deployments.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
