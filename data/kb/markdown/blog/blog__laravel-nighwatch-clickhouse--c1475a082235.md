# Inside Laravel Nightwatch’s Observability Pipeline: Real\-Time Event Processing with Amazon MSK and ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Inside Laravel Nightwatch’s Observability Pipeline: Real\-Time Event Processing with Amazon MSK and ClickHouse Cloud

![](/uploads/AWS_blue_3f3adb4c31.svg)![](/uploads/laravel_sm_square_white_e46a51ed54.svg)![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[AWS](/authors/aws), [Laravel](/authors/laravel) and [ClickHouse](/authors/clickhouse)Oct 8, 2025 · 7 minutes read*Initially posted on [AWS blog](https://aws.amazon.com/blogs/big-data/how-laravel-nightwatch-handles-billions-of-observability-events-in-real-time-with-amazon-msk-and-clickhouse-cloud/)*


[Laravel](https://laravel.com/), one of the world's most popular web frameworks, launched its first\-party observability platform,[Laravel Nightwatch](https://nightwatch.laravel.com/), to provide developers with real\-time insights into application performance. Built entirely on AWS managed services and[ClickHouse Cloud](https://clickhouse.com/cloud), the service already processes over one billion events per day while maintaining sub\-second query latency, giving developers instant visibility into the health of their applications.


By combining[Amazon Managed Streaming for Apache Kafka (Amazon MSK)](https://aws.amazon.com/msk/) with ClickHouse Cloud and[AWS Lambda](https://aws.amazon.com/lambda/), Laravel Nightwatch delivers high\-volume, low\-latency monitoring at scale, while maintaining the simplicity and developer experience Laravel is known for.


## The challenge: Delivering real\-time monitoring for a global developer community [\#](/blog/laravel-nighwatch-clickhouse#the-challenge-delivering-real-time-monitoring-for-a-global-developer-community)


The Laravel framework powers millions of applications worldwide, serving billions of requests each month. Each request can generate potentially hundreds of observability events, such as database queries, queued jobs, cache lookups, emails, notifications, and exceptions. For Nightwatch's launch, Laravel anticipated instant adoption from its global community, with tens of thousands of applications sending events around the clock from day one.


Laravel Nightwatch needed an architecture that could:


- Ingest millions of JSON events per second from customer applications reliably.
- Provide sub\-second analytical queries for real\-time dashboards.
- Scale horizontally to handle unpredictable traffic spikes.
- Deliver all of this in a cost\-effective, low\-maintenance manner.


The challenge was to process data on a global scale and provide deep insights into application health without compromising on a straightforward setup experience for developers.



## The solution: A decoupled streaming and analytics pipeline [\#](/blog/laravel-nighwatch-clickhouse#the-solution-a-decoupled-streaming-and-analytics-pipeline)


![blog-laravel-1.png](/uploads/blog_laravel_1_2b8e4a05cc.png)
Laravel Nightwatch implemented a dual\-database, streaming\-first architecture, shown in the preceding figure, that separates transactional and analytical workloads.


- **Transactional workloads** – user accounts, organization settings, billing, and similar workloads run on[Amazon RDS](https://aws.amazon.com/rds/) for PostgreSQL.
- **Analytical workloads** – telemetry events, metrics, query logs, and request traces are handled by ClickHouse Cloud.


### Key components [\#](/blog/laravel-nighwatch-clickhouse#key-components)


The key components of the solution include the following:


1. **Ingestion layer**
	- [Amazon API Gateway](https://aws.amazon.com/gateway) receives telemetry from Laravel agents embedded in customer applications
	- **Lambda** validates and enriches events. Validated and enriched events are published to Amazon MSK, partitioned for scalability
2. **Streaming to analytics**
	- [ClickPipes](https://clickhouse.com/cloud/clickpipes) in ClickHouse Cloud subscribe directly to MSK topics, reducing the need to build and manage extract, transform, and load (ETL) pipelines
	- Materialized views in ClickHouse pre\-aggregate and transform raw JSON into query\-ready formats
3. **Dashboards and delivery**
	- The Nightwatch dashboard, built with Laravel, Inertia, and React, runs on[AWS Fargate for Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html)
	- [Amazon ElastiCache for Redis](https://aws.amazon.com/elasticache/redis/) accelerates session and cache lookups
	- Cloudflare CDN provides low\-latency delivery to global users


## Why Amazon MSK and ClickHouse Cloud? [\#](/blog/laravel-nighwatch-clickhouse#why-amazon-msk-and-clickhouse-cloud)


Nightwatch requires a durable, horizontally scalable, and low maintenance streaming backbone.


With [Amazon MSK Express brokers](https://docs.aws.amazon.com/msk/latest/developerguide/msk-broker-types-express.html), we have achieved over 1 million events per second during load testing, benefiting from low\-latency, elastic scaling, and simplified operations. MSK Express brokers require no storage sizing or provisioning, scale up to 20 times faster, and recover 90% quicker than standard Apache Kafka brokers—all while enforcing best\-practice defaults and client quotas for reliable performance. Its seamless integration with other AWS services—such as Lambda, [Amazon Simple Storage Service (Amazon S3\)](https://aws.amazon.com/s3/), and [Amazon CloudWatch](https://aws.amazon.com/cloudwatch)—made it straightforward to build a resilient, end\-to\-end streaming architecture.


To ingest and transform these events in real time, Nightwatch uses ClickHouse Cloud and its managed integration platform, [ClickPipes](https://clickhouse.com/docs/integrations/clickpipes). ClickHouse Cloud excels at analytical workloads by delivering up to 100 times faster query performance for analytics compared to traditional row\-based databases. Its advanced compression algorithms provide up to 90% storage savings, significantly reducing infrastructure costs while maintaining high performance. With its columnar architecture and optimized execution engine, ClickHouse Cloud can query billions of rows in under 1 second, enabling Laravel Nightwatch to serve real\-time dashboards and analytics at global scale.


By integrating Amazon MSK and ClickHouse using ClickPipes, Laravel also reduced the operational burden of building and managing ETL pipelines, reducing latency and complexity.


## Overcoming challenges [\#](/blog/laravel-nighwatch-clickhouse#overcoming-challenges)


### Testing complexity [\#](/blog/laravel-nighwatch-clickhouse#testing-complexity)


While synthetic benchmarking and test datasets yield useful results, a more realistic workload is required to rigorously test infrastructure and code before deployment to production. The team used Terraform to manage infrastructure alongside application code, creating multiple dev and test environments, and allowing them to test the platform internally with their own applications before each release.


### Multi\-region infrastructure [\#](/blog/laravel-nighwatch-clickhouse#multi-region-infrastructure)


The need to cater to multiple data storage regions also brought challenges\-\-\-with latency, complexity, and cost the foremost concerns. However, the AWS, ClickHouse Cloud, and Cloudflare stack made available a powerful set of networking tools and scaling options. While VPC peering, RDS replication, and global server load balancing did the heavy lifting on the networking side, the ability to scale and right\-size each resource kept costs to a minimum.


### Query performance at scale [\#](/blog/laravel-nighwatch-clickhouse#query-performance-at-scale)


Materialized views, intelligent time\-series partitioning, and specialized ClickHouse codecs helped ensure that queries remained sub\-second even as data volumes grew into the billions. Meanwhile, compute separation allowed distinct workloads to scale separately while accessing the same data, with clusters right\-sized horizontally and vertically depending on the requirements of each load.


## Results [\#](/blog/laravel-nighwatch-clickhouse#results)


Laravel Nightwatch's launch exceeded expectations:


- 5,300 users registered in the first 24 hours
- 500 million events processed on day one
- 97 ms average dashboard request latency
- 760,000 exceptions logged and analyzed in real time


By building on Amazon MSK and ClickHouse Cloud, we were able to scale from zero to billions of events without sacrificing performance or developer experience.


## What's next [\#](/blog/laravel-nighwatch-clickhouse#whats-next)


Laravel plans to expand Nightwatch with:


- **More regions** to cater to customers with data sovereignty requirements outside the US and EU
- **Broader data collection** to provide even deeper insight into customers' applications
- **SOC 2 certification** to cater to customers with tighter compliance requirements
- **More advanced monitoring and analysis** to identify issues before they affect users


The current architecture comfortably supports applications of all sizes, from hobby to enterprise (including a generous free tier), and is designed to handle over one trillion monthly events without performance degradation.


## Conclusion [\#](/blog/laravel-nighwatch-clickhouse#conclusion)


Laravel Nightwatch demonstrates how Amazon MSK, ClickHouse Cloud, and AWS serverless technologies can be combined to build a cost\-effective, real\-time monitoring platform at global scale. By designing for scale from day one, Laravel delivered sub\-second analytics across billions of events, while maintaining the developer\-friendly experience their community expects.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
