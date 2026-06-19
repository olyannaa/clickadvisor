# Postgres managed by ClickHouse is now in beta


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Postgres managed by ClickHouse is now in beta

![Sai Srirampur](/_next/image?url=%2Fuploads%2Fdisplay_pic_copy_5b0aedef94.jpeg&w=96&q=75)[Sai Srirampur](/authors/sai-srirampur)May 27, 2026 · 9 minutes read**TL;DR:** ClickHouse Cloud users can now provision a fully managed Postgres service, backed by local NVMe for up to 10x faster transactions, with native CDC into ClickHouse for real\-time analytics and a unified query layer via pg\_clickhouse. Free until June 15, 2026, with a 50% discount after that for the duration of the beta. CDC and pg\_clickhouse are included at no extra cost.


ClickHouse Cloud users can now provision a fully managed Postgres service backed by local NVMe storage, natively integrated with ClickHouse. Any ClickHouse Cloud user can now provision an enterprise\-grade, fully managed Postgres service powered by local NVMe storage and natively integrated with ClickHouse. We offer a **best\-of\-breed data stack** that combines Postgres for transactional (OLTP) workloads and ClickHouse for analytical (OLAP) workloads, eliminating the traditional complexity of stitching together separate systems and providing a foundation essential for real\-time and AI\-native applications.



> [Sign up for ClickHouse Cloud today to get started with Postgres managed by ClickHouse](https://console.clickhouse.cloud/signUp?intent=PG)


You get a high\-performance Postgres service backed by local NVMe with up to 10x faster transactional performance. Using native CDC, you can sync data from Postgres to ClickHouse in just a few clicks for [100x faster analytics](https://benchmark.clickhouse.com/). With a unified query layer powered by the [pg\_clickhouse](https://clickhouse.com/blog/introducing-pg_clickhouse) extension, you can build applications that combine transactions and analytics, without managing separate systems. And all of this comes at a cost\-effective price point, so you never have to compromise on a fast and reliable data foundation for building your apps.


## AI needs the “best\-of\-breed” data stack [\#](/blog/postgres-managed-by-clickhouse-beta#ai-needs-the-best-of-breed-data-stack)


[AI workloads are collapsing the traditional divide between transactional and analytical databases.](https://clickhouse.com/blog/ai-redrawing-database-market#real-time_analytics) Applications that once ran predictable, hard\-coded queries now generate unpredictable bursts of agent\-driven requests that need answers from both sides of the stack. At the same time, data volumes, concurrency, and performance expectations are growing exponentially, while security and reliability have become more critical than ever.


That’s why best\-of\-breed matters more than ever: Postgres for OLTP and ClickHouse for OLAP. It’s also why thousands of AI\-native companies have already converged on this architecture.


![postgres_beta_may2026_image1.png](/uploads/postgres_beta_may2026_image1_4ffdd4d2c0.png)
Our vision for Postgres managed by ClickHouse is simple: make it easy for developers to build AI\-native applications on the unified data stack by eliminating the overhead of stitching together Postgres and ClickHouse through external pipelines, custom application logic, and operational complexity.


## Customers [\#](/blog/postgres-managed-by-clickhouse-beta#customers)


We announced the private preview of Postgres managed by ClickHouse earlier this year, and thousands of companies have already joined the waitlist, with many already running multi\-terabyte, mission\-critical production workloads.


Customers have migrated from RDS, Aurora, CloudSQL, Neon, PlanetScale Postgres, and more, while others have built entirely new AI\-native applications. These workloads span cybersecurity, fintech, retail, real estate, social media, and beyond—all powered by a deeply integrated platform that unifies OLTP and OLAP with Postgres and ClickHouse.


Here are a few raw testimonials from our reference customers.


### **Physical Intelligence** [\#](/blog/postgres-managed-by-clickhouse-beta#physical-intelligence)


*Scaling AI workloads and annotation pipelines, migrated from RDS*


“ClickHouse helped us move off RDS and build a data platform that can support our growing AI workloads. We use Postgres for OLTP and ClickHouse for OLAP in the ClickHouse Cloud platform, giving researchers, training pipelines, and agents fast access to the same data foundation… As our annotation volume grows 10x and continues toward billions of annotations, ClickHouse gives us the platform headroom to keep scaling...”


### **Sterling Labs** [\#](/blog/postgres-managed-by-clickhouse-beta#sterling-labs)


*Running 8\.5 TB of hot Postgres data on NVMe, migrated from Aurora.*


“Postgres managed by ClickHouse has been an incredible fit for us as we migrated from Aurora and scaled our production workload... We’re now running around 8\.5 TB of hot data in Postgres, and enjoy the super low\-latency offered by the NVMe drives…The performance has been simply impressive...”


### **Quinto Andar** [\#](/blog/postgres-managed-by-clickhouse-beta#quinto-andar)


*Using Postgres as a universal interface for analytics*


“With pg\_clickhouse, ClickHouse becomes a plug\-and\-play database for virtually any third\-party tool.. Instead of being forced into the overhead of BigQuery or Snowflake just to satisfy an integration like Hightouch, we can now expose key datasets directly through Postgres... It’s the best of both worlds: ClickHouse’s raw performance with the ubiquitous compatibility of Postgres.”


### **DoControl** [\#](/blog/postgres-managed-by-clickhouse-beta#docontrol)


*Simplifying cybersecurity data pipelines at scale,*


“We moved multiple multi\-terabyte workloads from RDS and Aurora to Postgres managed by ClickHouse with hands\-on support from the ClickHouse team.Given the scale and complexity of our cybersecurity data sources, reliability and price\-performance were critical… Postgres managed by ClickHouse lets us move Postgres workloads more easily, use ClickPipes, and bring data into ClickHouse without the operational complexity we originally expected.”


Other reference customers we’d like to call out include Y Combinator companies like Trainy.ai and EndClose, AI safety companies like Mpathic, AI\-native inventory management companies like Prediko, and many more power the next generation of AI\-native applications on Postgres managed by ClickHouse.


## **Product** [\#](/blog/postgres-managed-by-clickhouse-beta#product)


Postgres managed by ClickHouse brings together high\-performance OLTP and real\-time OLAP into a single, deeply integrated platform. At the core of the platform are three foundational capabilities:


- **NVMe\-backed Postgres** delivering up to 10x faster transactional performance
- **Native CDC into ClickHouse** for real\-time analytics without external pipelines
- **pg\_clickhouse**, a unified query layer that allows applications to span transactions and analytics


Together, these capabilities eliminate the operational complexity of stitching together Postgres and analytical infrastructure manually, making it simpler to build real\-time and AI\-native applications.

Loading video...### **Fully managed migrations with ClickPipes** [\#](/blog/postgres-managed-by-clickhouse-beta#fully-managed-migrations-with-clickpipes)


Migrating production Postgres workloads is one of the hardest parts of adopting a new platform. With fully managed migration workflows powered by [ClickPipes](https://clickhouse.com/docs/cloud/managed-postgres/migrations/clickpipes), customers can move workloads from RDS, Aurora, CloudSQL, Neon, and other providers with minimal downtime and operational overhead.


Customers can continuously replicate data in real time, simplify cutovers, and avoid building custom migration infrastructure themselves, a capability that has quickly become one of the most loved aspects of the platform among customers running production workloads.


### **Enterprise\-grade Postgres for production workloads** [\#](/blog/postgres-managed-by-clickhouse-beta#enterprise-grade-postgres-for-production-workloads)


Postgres managed by ClickHouse includes the operational capabilities customers expect to run mission\-critical applications at scale, including:


- High availability with up to two standbys
- Point\-in\-time recovery and database branching
- Read replicas for scaling read\-heavy workloads
- 90\+ PostgreSQL extensions
- Enterprise\-grade security with Private Link
- Integrated monitoring, logs, and [Query Insights](https://clickhouse.com/blog/postgres-query-insights-clickhouse-cloud)
- Prometheus\-compatible metrics
- Agent\-based access with `clickhousectl`
- Infrastructure as Code via OpenAPI
- And more!


And this is just the beginning. We’re building toward a fully unified operational and analytical data platform for real\-time and AI\-native applications.


For detailed documentation on the above features, you can visit our official docs [here](https://clickhouse.com/docs/cloud/managed-postgres).


## Pricing [\#](/blog/postgres-managed-by-clickhouse-beta#pricing)


Postgres managed by ClickHouse is designed to be cost\-effective, so developers never have to compromise on a fast, reliable data foundation powered by Postgres and ClickHouse. We’ve priced the service to deliver some of the most competitive pricing compared to alternative managed Postgres offerings. This excludes the price\-performance benefits you get from local NVMe storage.


The service remains free until usage metering begins on June 15, 2026\. During Beta, all plans include a 50% discount as part of our commitment to early customers.



> For exact pricing, visit [the Pricing Calculator](https://clickhouse.com/pricing?service=postgres#pricing-calculator) to find the best configuration and pricing for your workload.


Native CDC via ClickPipes and the pg\_clickhouse extension are included at no additional cost, aligning with our vision for a unified OLTP \+ OLAP platform powered by Postgres and ClickHouse.


The platform supports more than 50 local NVMe\-backed VM configurations, ranging from 1 vCPU / 8 GB RAM / 59 GB NVMe deployments starting at approximately $32/month to clusters with 96 vCPUs / 768 GB RAM / 60 TB NVMe storage. This provides the flexibility to support everything from lightweight developer workloads to compute\-intensive and storage\-heavy production deployments.


During Beta, backups and network egress are also included at no additional cost.


As we move toward General Availability, pricing and packaging may evolve. Please refer to the pricing [documentation](https://clickhouse.com/docs/cloud/managed-postgres/pricing) for additional details and disclaimers.


## Get Started [\#](/blog/postgres-managed-by-clickhouse-beta#get-started)


Postgres managed by ClickHouse is available today in Beta on ClickHouse Cloud!

### Get started today

Sign up for ClickHouse Cloud to provision your first NVMe\-backed Postgres service, set up native CDC into ClickHouse, and start querying across both with pg\_clickhouse. 

Every new account includes $300 in free credits.[Sign up](https://console.clickhouse.cloud/signup?intent=PG&loc=blog-cta-737-get-started-today-sign-up&utm_blogctaid=737)Visit the [Postgres managed by ClickHouse page](https://clickhouse.com/cloud/postgres) to learn more, or jump into the [documentation](https://clickhouse.com/docs/cloud/managed-postgres) to start building.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
