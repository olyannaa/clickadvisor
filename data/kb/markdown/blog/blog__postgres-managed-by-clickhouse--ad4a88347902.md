# Fast, scalable, enterprise\-grade Postgres natively integrated with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Fast, scalable, enterprise\-grade Postgres natively integrated with ClickHouse

![Sai Srirampur](/_next/image?url=%2Fuploads%2Fdisplay_pic_copy_5b0aedef94.jpeg&w=96&q=75)![](/_next/image?url=%2Fuploads%2FImage_512x512_1_839aa54f62.jpeg&w=96&q=75)[Sai Srirampur](/authors/sai-srirampur) and [Kaushik Iska](/authors/kaushik-iska)Jan 22, 2026 · 10 minutes readToday, we're announcing a fast, scalable and an enterprise\-grade managed Postgres service natively integrated with ClickHouse, [built for real\-time and AI\-driven applications](https://clickhouse.com/resources/engineering/managed-postgres-for-ai-and-real-time-apps). We are offering a **Unified Data Stack** that brings transactional and analytical workloads together without traditional complexity. By combining Postgres for transactions with ClickHouse for analytics, teams get best\-in\-class performance and scalability on an open\-source foundation while significantly reducing operational overhead.


Developers get a high\-performance, scalable Postgres service backed by local NVMe storage, delivering up to 10X faster performance for fast\-growing workloads that are mostly disk\-bound. In just a few clicks, using native CDC capabilities, they can sync transactional data in Postgres to ClickHouse to make it analytics\-ready, unlocking up to [100X faster analytics](https://benchmark.clickhouse.com/#system=+lik%7CgQ&type=-&machine=-ca2l%7C6t%7Cg4e%7C6ax%7Cae-l%7C6ale%7Cg-l%7C3al&cluster_size=-&opensource=-&hardware=-&tuned=+n&metric=combined&queries=-). With a unified query layer powered by the [pg\_clickhouse](https://github.com/ClickHouse/pg_clickhouse) Postgres extension, they can build applications that seamlessly span transactions and analytics without managing separate systems.

### Get started with our native Postgres Service

To try ClickHouse's native Postgres service, sign up for Private Preview using this link.[Sign up](https://clickhouse.com/cloud/postgres?loc=blog-cta-398-get-started-with-our-native-postgres-service-sign-up&utm_blogctaid=398)This demo showcases how the various pieces come together to form a Unified Data Stack powered by Postgres and ClickHouse.



To achieve this, we're partnering with [Ubicloud](https://www.ubicloud.com/), an open\-source cloud company that offers one of the fastest Postgres services and whose [founding team](https://www.ubicloud.com/about-ubicloud) has a track record of delivering world\-class Postgres at Citus Data, Heroku, and Microsoft.



> Noah Pryor, the CTO of [Beehiiv](https://www.beehiiv.com/), a large ClickHouse customer, shared excitement for this launch, "We’re excited to see ClickHouse entering the Postgres ecosystem. At Beehiiv, we rely heavily on both Postgres and ClickHouse to power our mission\-critical, customer\-facing applications. We’ve invested significant effort in integrating these technologies, so a tighter, more native integration between them would materially simplify our architecture."


## Why Postgres managed by ClickHouse [\#](/blog/postgres-managed-by-clickhouse#why-postgres-managed-by-clickhouse)


### Postgres, built for performance and scale [\#](/blog/postgres-managed-by-clickhouse#postgres-built-for-performance-and-scale)


Across thousands of fast growing AI\-driven companies using Postgres, performance and scalability consistently emerge as challenges. Common issues include slower ingestion (mainly updates), slower vacuums, increased tail latency for reads and writes, long\-running, slow transactions causing lock contention and sudden WAL spikes, among others. In most cases, these issues stem from limited disk IOPS and suboptimal disk latency. With unlimited IOPS, Postgres can operate more efficiently than it does today on most other managed Postgres services.


Postgres managed by ClickHouse is an enterprise\-grade managed Postgres service backed by NVMe storage. The NVMe storage is physically colocated with compute, delivering orders of magnitude lower disk latency and higher IOPS than alternatives such as EBS\-backed volumes, which require a network round trip for disk access. As a result, disk access latency can be on the order of microseconds rather than milliseconds. For fast\-growing Postgres workloads that are primarily throttled by disk IOPS and latency, we expect up to 10X speedups at the same cost and hardware profile compared to other Postgres providers.



> *"We're excited that ClickHouse is offering a native Postgres service to complement its core OLAP database. NVMe\-backed Postgres performance, combined with seamless integration with CDC and pg\_clickhouse for fast analytics, makes it very compelling for us to build our fast\-growing applications."* \- Aditya Maru, Co\-founder, [Blacksmith.sh](http://blacksmith.sh)


The image below shows the reduction in P99 latency for disk\-bound workloads when moving from traditional Postgres to NVMe\-backed Postgres.


![postgres-launch-1.png](/uploads/postgres_launch_1_5e02d22e1a.png)
#### Ubicloud's NVMe\-backed Postgres stood out [\#](/blog/postgres-managed-by-clickhouse#ubiclouds-nvme-backed-postgres-stood-out)


To select the best architecture, we evaluated many Postgres providers as potential partners. Ubicloud stood out by offering a reliable Postgres service backed by NVMe storage that addressed the same customer challenges we observed and outperformed other providers by orders of magnitude in real\-world benchmarks. We plan to share a detailed blog post on our evaluation process in the future.


We evaluated alternative architectures, including separating storage and compute, and found that object\-storage\-backed Postgres is not well suited for OLTP workloads, where consistent and predictable latency and throughput are essential. Object storage works well for analytics, but its higher latency and coarse\-grained I/O make it challenging to support transactional patterns. We’ll dive deeper into this trade\-off in a follow\-up blog post.


### Deeply integrated with ClickHouse [\#](/blog/postgres-managed-by-clickhouse#deeply-integrated-with-clickhouse)


Developers can natively integrate their Postgres with ClickHouse to enable 100x faster analytics. It comes with two critical features enabling this integration. These features are central to powering the Unified Data Stack, combining Postgres for transactions and ClickHouse for analytics with no overhead.


The diagram below depicts the Unified Data Stack, highlighting Postgres for OLTP, ClickHouse for OLAP, continuous replication between the two, and a unified query layer via the `pg_clickhouse` extension.


![postgres-launch-2.png](/uploads/postgres_launch_2_5b8721a622.png)
### Postgres to ClickHouse replication [\#](/blog/postgres-managed-by-clickhouse#postgres-to-clickhouse-replication)


Seamlessly replicate Postgres data to ClickHouse in real time to make it analytics\-ready. We support both an initial load to migrate existing data to ClickHouse and CDC for incremental syncs. This feature is powered by the Postgres CDC connector in [ClickPipes](https://clickhouse.com/docs/integrations/clickpipes/postgres), which is battle\-tested by 100s of enterprise customers moving 100s of TB per month.


We plan to offer additional features for more native CDC, including sub\-second replication latency, replication of ongoing transactions using logical replication v2 for reliable slot flushing, etc. all of which will be exclusive to our native Postgres service.


### pg\_clickhouse: unified query layer for OLTP and OLAP [\#](/blog/postgres-managed-by-clickhouse#pg_clickhouse-unified-query-layer-for-oltp-and-olap)


Every Postgres service comes with the [pg\_clickhouse](https://clickhouse.com/blog/introducing-pg_clickhouse) Postgres extension, which enables users to query ClickHouse directly from Postgres. It allows Postgres to act as a unified query layer, powering not just transactions but also analytics using ClickHouse internally, making it easy for developers to build applications.


`pg_clickhouse` provides comprehensive query pushdown to ClickHouse for efficient query execution, including support for FILTERs, JOINs, SEMI\-JOINs, aggregations, functions and more. Currently, 14 of 22 TPC\-H queries are fully pushed down, delivering over 60x performance improvements compared to standard Postgres.


We will continue expanding pushdown support to more complex queries, including CTEs, window functions, and beyond, all with the goal of enabling users to build fast analytics from the Postgres layer itself while still leveraging the power of ClickHouse.


Users can seamlessly create foreign tables in Postgres that point to ClickHouse tables under the hood and start powering analytics using these foreign tables. As we evolve `pg_clickhouse`, we'll work toward making this experience as UX\-friendly as possible, including auto\-creating foreign tables for replicated data, auto\-routing transactions and analytics to the appropriate engines (Postgres or ClickHouse), and more.


### Enterprise\-grade Postgres [\#](/blog/postgres-managed-by-clickhouse#enterprise-grade-postgres)


#### Reliability without compromise [\#](/blog/postgres-managed-by-clickhouse#reliability-without-compromise)


Our native Postgres service provides enterprise\-grade reliability from day one. We offer strong high availability (HA), allowing a primary with up to two standby instances across different availability zones (AZs) using quorum\-based replication. These standby instances are dedicated to HA and auto\-failover; they are not exposed as read replicas, as that could impact HA guarantees. Read scaling is handled via separate read replicas (details [here](https://clickhouse.com/docs/cloud/managed-postgres/read-replicas)).


For disaster recovery, every service comes with automatic backups that support forks and point\-in\-time recovery. The backups run on [WAL\-G](https://github.com/wal-g/wal-g), a well\-known open\-source Postgres tool that handles full backups and continuous WAL archiving to object storage like S3\. WAL\-G was [originally created](https://www.citusdata.com/blog/2017/08/18/introducing-wal-g-faster-restores-for-postgres/) by Daniel Farina, co\-founder of Ubicloud, during his time at Citus Data, another testament to the quality of the team we're partnering with.


#### Built on ClickHouse Cloud trust [\#](/blog/postgres-managed-by-clickhouse#built-on-clickhouse-cloud-trust)


It is built to meet the same high standards for security, privacy, and compliance as ClickHouse Cloud. As part of a unique partnership, Ubicloud runs entirely within AWS accounts owned by ClickHouse Cloud and is subject to the same security, privacy, and governance controls applied across the platform. It already includes core capabilities such as SAML/SSO, IP allow\-listing, data encryption at rest and in transit, as well as PrivateLink (available via a support ticket), with plans to further align and unify with the advanced features offered by ClickHouse Cloud over time.


### Open source first [\#](/blog/postgres-managed-by-clickhouse#open-source-first)


The managed Postgres service is built on an open source first philosophy. [Postgres](https://github.com/postgres/postgres) and [ClickHouse](https://github.com/ClickHouse/ClickHouse) are both open\-source databases with large, thriving communities. Every component that integrates Postgres and ClickHouse is open source, from the [pg\_clickhouse](https://github.com/ClickHouse/pg_clickhouse) extension that enables a unified query layer to [PeerDB](https://github.com/PeerDB-io/peerdb), which powers real\-time CDC and replication.


[Ubicloud](https://github.com/ubicloud/ubicloud), our strategic partner on the managed Postgres service, is also an open source company, deeply aligned with this philosophy This was a major factor in choosing the right partner. We are jointly contributing to the open\-source ecosystem to deliver a world\-class Postgres to the community, and this collaboration is already underway. [Here](https://github.com/ubicloud/ubicloud/pulls?q=is%3Apr+author%3Aserprex) are a few key contributions from the ClickHouse team to the Ubicloud open\-source repository.


This open source foundation ensures there is no vendor lock\-in, giving developers full control, transparency, and long\-term flexibility over their data stack.


## Try Postgres managed by ClickHouse [\#](/blog/postgres-managed-by-clickhouse#try-postgres-managed-by-clickhouse)

### Get started with our native Postgres Service

To try ClickHouse's native Postgres service, sign up for Private Preview using this link.[Sign up](https://clickhouse.com/cloud/postgres?loc=blog-cta-399-get-started-with-our-native-postgres-service-sign-up&utm_blogctaid=399)Our team will reach out within a day and work closely with you to provide early access. **The private preview is fully free and entails no cost.**


It is currently available on AWS in 10 public regions, with over 50 NVMe\-backed configurations ranging from 2 vCPUs / 8 GB RAM / 118 GB disk to 96 vCPUs / 768 GB RAM / 60 TB storage. We plan to expand to additional regions and other cloud service providers, including GCP and Azure, in the near future. The offering includes all standard managed service features, including high availability, forks, read replicas, PgBouncer, upgrades, and more, along with deep integration with ClickHouse.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
