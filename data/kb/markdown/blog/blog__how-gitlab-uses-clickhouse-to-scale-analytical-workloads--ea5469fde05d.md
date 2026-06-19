# How GitLab serves sub\-second analytics to 50 million users


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How GitLab serves sub\-second analytics to 50 million users

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Oct 21, 2025 · 14 minutes read
> **TLDR;** 
> 
>   
> GitLab needed specialized analytics capabilities that could handle massive scale and deliver sub\-second insights, leading them to build their product analytics platform on ClickHouse. 
> 
>   
> This post traces the journey from early bottlenecks and benchmarks against other database management systems to a full\-scale shift that now powers insights across GitLab.com with ClickHouse Cloud and GitLab Dedicated and self\-managed deployments. 
> 
> 
>   
> 
> The results speak for themselves: queries over 100M rows that once took 30–40 seconds now return in under a second. ClickHouse now powers critical features such as Contribution Analytics and GitLab Duo and SDLC trends, enabling GitLab to track engineering outcomes and AI adoption in real\-time as it standardizes on ClickHouse for analytics company\-wide.


## Introduction [\#](/blog/how-gitlab-uses-clickhouse-to-scale-analytical-workloads#introduction)


[Dennis Tang](https://www.linkedin.com/in/dennis-tang) has been at GitLab since 2018, starting as an engineer focused on platform capabilities before moving into leadership of the Analytics team. Today, as Senior Engineering Manager of the Analytics stage, he oversees multiple teams responsible for the full analytics lifecycle, from instrumentation to customer\-facing insights.



> Internally, GitLab distinguishes between product\-facing analytics and internal business intelligence. While another group owns internal workflows, Dennis’s team focuses on instrumenting and delivering analytics that are surfaced to [their 50 million registered users](https://about.gitlab.com/) across the platform.


As GitLab’s shared SaaS and on\-premise codebase evolved, the demand for real\-time, scalable user\-facing analytics grew significantly. Historically, GitLab used Postgres for analytical and transactional workloads. While Postgres continues to excel at the latter, the team recognized they needed specialized technology optimized for analytical workloads to deliver the performance and scalability their users demand.


That is when ClickHouse entered the picture. Postgres and ClickHouse have each become leaders in their respective domains, forming a powerful pair \- Postgres as the go\-to transactional database trusted for reliability and features, and ClickHouse as the high\-performance, real\-time analytics engine built for scale.


In this post, we explore GitLab's journey with ClickHouse from 2022 to today. What began as an experiment quickly became a foundational part of the platform. Today, ClickHouse powers critical workloads, including Contribution Analytics, GitLab Duo, and SDLC trends reports on GitLab.com. This is the story of how ClickHouse evolved from a side project into the default OLAP database for analytics at GitLab.


## From growing demands to a new analytics foundation [\#](/blog/how-gitlab-uses-clickhouse-to-scale-analytical-workloads#from-growing-demands-to-a-new-analytics-foundation)


GitLab.com runs the same software as its self\-managed deployments. This architectural decision ensures consistency, but it also means that any limitations in the stack affect every user. The scale of analytical data required dedicated infrastructure and even with optimizations like [dedicated shards](https://about.gitlab.com/blog/2022/06/02/splitting-database-into-main-and-ci/) in Postgres for specific features, many dashboards still hovered near GitLab's internal performance threshold of 15 seconds. **Anything slower doesn't ship.** A prime example of this is CI database, which captures all user activity related to continuous integration across the platform.


Dennis and his team knew that if GitLab was going to deliver fast, scalable analytics to their users, especially in a hybrid SaaS/on\-premise environment, they needed a new foundation explicitly built for analytical workloads.


ClickHouse stood out during the evaluation. It wasn’t just faster in benchmarks \- it aligned with GitLab’s architectural principles. As a single binary, it could run anywhere. It scaled effortlessly. And it was open source. That combination made ClickHouse the clear choice to take GitLab’s analytics forward.


The results speak for themselves: queries over 100M rows that once took 30\-40 seconds now return in under a second.


### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## Evaluating the options for analytics [\#](/blog/how-gitlab-uses-clickhouse-to-scale-analytical-workloads#evaluating-the-options-for-analytics)


By the time Dennis joined the internal working group evaluating GitLab's next analytics architecture, the need for specialized analytics technology was already well established. The team had started exploring alternatives capable of handling high ingestion rates, large volumes of historical data, and fast, flexible queries \- all without adding operational complexity.


GitLab's evaluation focused on finding systems that could meet their specific requirements. In testing, ClickHouse significantly outperformed other options in nearly every dimension:


- **Ingestion speed**: ClickHouse loaded metrics orders of magnitude faster, crucial for GitLab’s high\-throughput environments.
- **Storage footprint**: ClickHouse used almost 10x less disk space for the same datasets.
- **Query latency**: At the 95th percentile, ClickHouse queries returned results far faster, with fewer outliers.


The team needed a system that could scale horizontally, minimize operational overhead, and work seamlessly in cloud and self\-managed deployments.


**ClickHouse wasn't just faster \- it was simpler**. As Dennis noted, "We want systems you can run on a laptop if needed."


ClickHouse provided the power of a columnar, distributed database in a single binary. It was open source, easy to deploy, and aligned with GitLab's "satellite service" model \- self\-contained components that scale independently and fit naturally into the existing architecture. And critically, it could support not only metrics but a broader variety of observability and analytics data: logs, events, and more.


This combination of performance, flexibility, and deployment portability made ClickHouse the clear choice. GitLab wasn't just looking for a database \- they were investing in an architectural foundation that could support advanced analytics across their entire platform, at any scale.


## From proof to production [\#](/blog/how-gitlab-uses-clickhouse-to-scale-analytical-workloads#from-proof-to-production)


The analytics initiative that brought ClickHouse into focus wasn't just an infrastructure upgrade. It was a product initiative. Dennis's team was tasked with building a unified analytics platform within GitLab to provide customers with streamlined reporting and insight into how they use the product. The goal was to help users identify opportunities to optimize workflows and unlock value as adoption deepened, all within the same codebase that GitLab customers already run. ClickHouse was the only option that passed all evaluation criteria. [GitLab's Data Insights Platform](https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/data_insights_platform/) outlines the architecture behind this effort.


But moving from a promising benchmark to production wasn't just a matter of swapping databases. GitLab needed to ensure ClickHouse would work not only for GitLab.com, but also for self\-managed and air\-gapped environments used by enterprise and government customers.


Delivering at scale meant GitLab had to solve deployment itself. Before adopting ClickHouse Cloud, the team built and maintained their own [ClickHouse operator, which remains open source to this day](https://gitlab.com/gitlab-org/opstrace/opstrace/-/tree/main/clickhouse-operator?ref_type=heads). While this worked with object storage and scaled horizontally, it came with significant operational overhead. Managing it in production wasn't trivial; this experience shaped GitLab's future approach.


The lesson:



> "Don't self\-manage unless you really have to. We actually built our own operator, got ClickHouse running on object storage, and made it horizontally scalable \- but it was a huge operational burden. For most teams, it’s just not worth the overhead unless you absolutely need to control the environment."
> 
>   
> Dennis Tang, GitLab


ClickHouse Cloud offered the same performance with significantly less effort, accelerating GitLab's delivery. Engineers can prototype locally and then scale their workloads into production without worrying about infrastructure. The team began shifting toward a hybrid model, using ClickHouse Cloud for SaaS environments while retaining the option to run OSS ClickHouse for air\-gapped and on\-premise customers.


With ClickHouse, GitLab's analytics stack was transforming. Features like [Contribution Analytics](https://docs.gitlab.com/user/group/contribution_analytics/#contribution-analytics-with-clickhouse) now deliver sub\-second performance on datasets. The feature surfaces insights into team activity and individual performance, supporting use cases like workload balancing, identifying high performers or those needing support, assessing collaboration patterns, spotting training needs, and enriching retrospectives with real data. These scenarios were always possible in theory, but only ClickHouse made them usable at scale while also reducing operational overhead.


![contribution_analytics.png](/uploads/contribution_analytics_ce9bc636b7.png)
More recently, GitLab has enabled GitLab Duo and SDLC trends, powered by ClickHouse, which deliver instant insights into how AI impacts software delivery performance. The dashboard tracks both traditional DORA metrics, such as deployment frequency, lead time for changes, change failure rate, and time to restore service, as well as AI\-specific indicators, such as Duo seat adoption, code suggestion acceptance rates, and Duo Chat usage. By correlating AI adoption with engineering outcomes, GitLab helps teams quantify the value of GitLab Duo, optimize license utilization, and measure the real\-world impact of AI on development velocity and reliability at scale.


![ai_impact_analysis.png](/uploads/ai_impact_analysis_1ac0f26728.png)

> "We've consistently run into scaling and performance bottlenecks that limited our ability to deliver the kind of analytics features our users needed. ClickHouse gave us the breakthrough we needed to deliver the kind of features we’d been holding back."
> 
>   
> Dennis Tang, GitLab


All these improvements weren't just incremental \- they were the difference between shipping and shelving features. ClickHouse unlocked the ability to meet GitLab's strict performance thresholds without compromise. One example of this is a [hierarchical query](https://gitlab.com/gitlab-com/content-sites/handbook/-/merge_requests/12893/diffs) traversing GitLab's deeply nested data model, which includes organizations, groups, subgroups, and projects \- each with shared business objects such as issues, merge requests, and users. These multi\-layer joins were challenging to optimize for sub\-second performance, often taking 30–40 seconds across 100\+ million rows in Postgres. With ClickHouse, the same query now runs in 0\.24 seconds \- effectively turning an operational bottleneck into a real\-time capability.


As confidence grew, the team made a strategic pivot \- ClickHouse would become the default OLAP engine for analytics across all GitLab deployments, with Postgres continuing to focus on its specialty \- OLTP workloads. 


GitLab's internal benchmarks reinforced the value of this shift. In one POC, the team compared identical queries and saw execution times drop from minutes to milliseconds, without extensive tuning. The difference wasn't just noticeable; it redefined what the team could ship. 


ClickHouse Cloud's SharedMergeTree took this further, unlocking this performance while providing near\-infinite scale with separation of storage and compute through the use of object storage.


## Enabling ClickHouse for everyone [\#](/blog/how-gitlab-uses-clickhouse-to-scale-analytical-workloads#enabling-clickhouse-for-everyone)


Rolling out ClickHouse across GitLab was never just about enabling a single feature or solving a single performance bottleneck; it was about empowering the entire organization. Dennis's long\-term vision is more ambitious: make ClickHouse not just available, but the default for analytics across every GitLab deployment \- GitLab.com, GitLab Dedicated, and self\-managed instances alike.


To support this, GitLab focused on making ClickHouse dead simple to adopt internally. Once configured, features powered by ClickHouse "just work," with no additional setup required. This applies to both cloud and self\-managed users.


A hybrid data access layer dynamically routes queries to either the existing transactional database or ClickHouse, depending on the data range or use case. This abstraction ensures a seamless transition for existing features, allowing GitLab to gradually shift workloads while maintaining the user experience.


All of this reflects a deliberate effort to move beyond isolated wins. GitLab is investing in ClickHouse as a platform\-wide analytics foundation. The goal: deliver fast, scalable insights to every customer, regardless of how or where they run GitLab.


## The strategic shift [\#](/blog/how-gitlab-uses-clickhouse-to-scale-analytical-workloads#the-strategic-shift)


What began at GitLab as a performance improvement became the foundation for a new architecture based on ClickHouse focused on scale, flexibility, and real\-time insight across every part of the analytical product.


That transformation is now powering a broader shift toward an event\-driven, analytics\-first platform. GitLab is building analytics into the core of how the product operates and evolves.


ClickHouse's flexibility was critical to enabling this rollout. GitLab uses TSV over HTTP for ingestion \- a lightweight approach that lets engineers get started without needing specialized tooling. With the team's in\-house [CDC framework, Siphon](https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/siphon/), GitLab is poised to stream over 100 gigabytes per hour of operational analytics into ClickHouse. Combined with the HTTP endpoint, this makes onboarding straightforward. As GitLab's analytics footprint expanded, infrastructure concerns such as resilience and operability became increasingly important. ClickHouse Cloud's built\-in features, including automatic scaling, multi\-AZ support, and seamless backup, have helped the team move faster while reducing operational load. More recent developments, like ["make before break"](https://clickhouse.com/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud) pod rotation, have improved both stability and cost efficiency.


This event\-driven strategic shift unlocks a future where every feature \- whether a DORA dashboard, product usage chart, or AI usage audit \- is powered by a consistent, scalable, and lightning\-fast analytical engine.


**By standardizing analytics on ClickHouse, GitLab is giving its engineers a platform they can build on with confidence, knowing it will perform, scale, and run in any environment their customers operate.**


## Learnings [\#](/blog/how-gitlab-uses-clickhouse-to-scale-analytical-workloads#learnings)


GitLab built its own operator to run ClickHouse on object storage and scale horizontally. Although it was effective, the operational overhead was substantial. For most teams, ClickHouse Cloud offers the same performance with far less complexity, freeing engineers to focus on features rather than infrastructure.


Operational maturity also matters. While GitLab data is largely immutable, **mutations such as deletes and updates still require careful consideration**. For example, knowing when a mass delete has fully completed isn’t always obvious. ClickHouse processes mutations in the background across parts and blocks. While current observability through checking system tables or logs is functional, it is not intuitive. A dedicated "active mutations" dashboard would go a long way in improving visibility here for GitLab.


That said, product maturity continues to evolve quickly. One standout for GitLab was the addition of built\-in **backup functionality**. The team had already started building their own backup tooling when the feature shipped, instantly saving time and effort and eliminating the need for custom scripts.


On the performance front, **materialized views** have become a go\-to optimization tool. GitLab has internal guidelines for when and how to use them, especially when aggregating large volumes of data. While more advanced features, such as **dictionaries and projections,** aren't in heavy use yet, they’re on the roadmap.


Overall, ClickHouse offers incredible speed and flexibility, but teams must still be thoughtful in how they model, operate, and evolve their analytics architecture.


## Looking ahead [\#](/blog/how-gitlab-uses-clickhouse-to-scale-analytical-workloads#looking-ahead)


As GitLab continues to scale its analytics infrastructure, the team is now exploring broader coverage: richer dashboards, deeper observability, and more granular product analytics. This shift will enable GitLab to deliver insights and features that simply weren't feasible on their old stack.


For example, AI agents require fast, low\-latency responses to analytical queries and often generate a high volume of requests \- a workload pattern that traditional transactional databases cannot support efficiently. Servicing these demands requires a column\-oriented, real\-time OLAP database, such as ClickHouse. As GitLab continues building out its unified analytics capabilities, these features open the door for deeper, AI\-native insight generation across the product.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
