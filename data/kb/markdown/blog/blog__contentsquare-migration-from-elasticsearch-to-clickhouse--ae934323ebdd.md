# Contentsquare Migration from Elasticsearch to ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Contentsquare Migration from Elasticsearch to ClickHouse

![ContentsquareLogo.png](/_next/image?url=%2Fuploads%2FContentsquare_Logo_90c63458d1.png&w=96&q=75)Ryad ZenineOct 11, 2022 · 8 minutes read*We’d like to welcome Contentsquare as a guest to our blog. Read on to find out why they are using ClickHouse and their journey from Elastic to ClickHouse.*


At Contentsquare, we used to run our main SaaS application on top of Elasticsearch.


5 years ago, we started a migration process to move all our analytics applications to run on top of ClickHouse. We wanted to migrate to improve the horizontal scalability, the stability of our system and the overall efficiency (query time \& cost).


In this blog post, we will tell you a bit more about the migration process and the lessons learned along the way.


## Why did we decide to migrate? [\#](/blog/contentsquare-migration-from-elasticsearch-to-clickhouse#why-did-we-decide-to-migrate)


We had 14 Elasticsearch clusters in production. Each cluster had 30 nodes (3 master nodes). We used `m5.4xlarge` with network attached disks. At the time, we struggled with horizontal scalability as we were not able to put together larger clusters and keep
them stable for our workload.


Given that our clusters were limited in size, it was not possible for us to handle any tenant that would not fit into a single cluster. This imposed a severe limitation on our ability to grow as a company. The amount of traffic we could handle had an upper bound, which means our company growth was slowed down for technical reasons. This was not acceptable to us.


We were left with two choices in order to lift this technical limitation and support the growth of the company:


1. Figure out a way to host each tenant efficiently in a multi\-cluster setup.
2. Migrate to a more scalable piece of technology.


We chose the second option and started to look into OLAP database engines that would fit our requirements:


- Minimal latency for queries.
- Rich query language.
- Fast and efficient with spinning disks.
- Simple to deploy and operate.


After running extensive engineering studies and looking into most of the OLAP databases and processing systems of the market, we found that ClickHouse fit all our requirements and we started to plan the migration.


## Our migration strategy [\#](/blog/contentsquare-migration-from-elasticsearch-to-clickhouse#our-migration-strategy)


Migrating a large codebase, used by thousands of customers in production is easier said than done. We split our migration effort in 3 phases:


- Getting familiar with ClickHouse and building a new product with it
- Mirroring all the existing features withcustom tooling to ensure we did not have any regression.
- Migrating our clients one by one.


![contensquare_timeline.png](/uploads/contensquare_timeline_0aa78d02fd.png)
### Phase 1: Building a new product to get familiar with the technology [\#](/blog/contentsquare-migration-from-elasticsearch-to-clickhouse#phase-1-building-a-new-product-to-get-familiar-with-the-technology)


Instead of migrating an existing product, we started our migration by building a new product on top of ClickHouse. We wanted to get familiar with the technology and run it in production in a safer setup first. This first milestone allowed us to:


- Get familiar with the technology and learn how to use it
- Build automation and CI/CD tooling for ClickHouse deployments
- Setup the alerting and monitoring


Discovering a new tech, tweaking it and building the required tooling took us about 4 months. This phase was invaluable in leveling up the team and becoming comfortable in deploying ClickHouse at a larger scale.


### Phase 2: Migrate existing products [\#](/blog/contentsquare-migration-from-elasticsearch-to-clickhouse#phase-2-migrate-existing-products)


Once that first milestone was successfully achieved, we turned our attention to our main product. We split the team in two: one half would maintain and improve the current stack while the other half would port all the existing features to ClickHouse.


We did the migration of our main product iteratively. We took each existing API endpoint one by one and rewrote them so they would use ClickHouse instead of Elasticsearch. We listened for every query going to the old endpoint, and replayed it on the new endpoint as well. This allowed us to compare, with real production usage, the results of both endpoints, identify bugs and fix them iteratively. Once we considered this endpoint stable, we moved to rewriting the next one.


During all that time, all production queries were still processed by the old Elasticsearch. The new ClickHouse infrastructure wasn’t (yet) used by anyone in production.


![contentsquare_steps.png](/uploads/contentsquare_steps_0329552df6.png)
### Phase 3: Migrating the customers [\#](/blog/contentsquare-migration-from-elasticsearch-to-clickhouse#phase-3-migrating-the-customers)


Once we had migrated and tested all endpoints to ClickHouse, we were comfortable migrating customers to our new infrastructure. We once again took great care into not moving every customer at once, to have enough time and resources to identify potential issues.


We initially moved one customer. Then another. Then a few more. And over a period of 6 months, all our customers were migrated and our Elasticsearch clusters could be shut down. We’re proud to say that this careful planning allowed us to suffer exactly zero regression during the migration.


## Our experience since the migration [\#](/blog/contentsquare-migration-from-elasticsearch-to-clickhouse#our-experience-since-the-migration)


ClickHouse turned out to be 11 times cheaper (in infrastructure cost) and allowed us to have a 10x performance improvement in our p99 for queries. As a consequence, we have been able to allow our clients to query up to 3 months of historical data instead of 1 as we previously had. We also bumped the retention period to 13 months, as it was now technically viable to do so.


### Our ClickHouse setup [\#](/blog/contentsquare-migration-from-elasticsearch-to-clickhouse#our-clickhouse-setup)


While migrating to ClickHouse we made two major adaptations to our architecture to make sure we could take full advantage of what ClickHouse had to offer.


First, we designed a custom ingestion component in order to lower the overhead of insertions on the main ClickHouse cluster. Second, we decided to represent our queries as abstract syntax trees. This allowed us to build a query optimiser that would take advantage of some hypothesis implied by our data model.


### Ingestion pipeline [\#](/blog/contentsquare-migration-from-elasticsearch-to-clickhouse#ingestion-pipeline)


We insert data in each shard individually but we make sure to do it in a way that is compatible with the sharding key defined in our distributed tables. Doing so reduces the amount of I/O the cluster has to do to manage an insertion.


As a consequence, we had to build a dedicated component that we call `clickin` that handles the insertions for us. `clickin` reads from a Kafka topic; data in the Kafka topic is partitioned with the sharding key of the table in ClickHouse. Partition assignment is therefore static.


Given that we already built a component to minimize I/O overhead of insertions, we also took the opportunity to implement another optimization. `clickin` takes the input data and transforms it into ClickHouse native format using a `clickhouse-local` instance before sending it to the cluster. This allows us to save some CPU on our clusters as the data arrives in the most efficient format for ClickHouse.


![contentsquare_architecture.png](/uploads/contentsquare_architecture_9c375acee4.png)
### Query Optimizer [\#](/blog/contentsquare-migration-from-elasticsearch-to-clickhouse#query-optimizer)


We chose from the start to build a library that allows us to build and manipulate ClickHouse queries as abstract syntax trees. We needed to adopt this approach because most of our queries are dynamic and composed on the fly using building blocks that our users select. This design choice allowed us to build a query optimiser that does several important transformations for us:


- It propagates partition key and sort key conditions to all the subqueries
- It propagates `distributed_group_by_no_merge` settings to nested subqueries when applicable
- It merges subqueries together when applicable
- It simplifies some redundant/useless algebraic expressions before generating the query.


Those optimizations yield a 10x speedup increase on our 5% slowest queries.


![contentsquare_queries.png](/uploads/contentsquare_queries_4795324bc4.png)
## Lesson Learned: takeaways for a smooth migration [\#](/blog/contentsquare-migration-from-elasticsearch-to-clickhouse#lesson-learned-takeaways-for-a-smooth-migration)


- Don’t take the migration as an opportunity to fix functional bugs. This will make your non\-regression testing a nightmare and slow you down
- Invest in automation for non\-regression testing
- Backups are not seamless yet, we had to build a small tool that does backups. We leverage a technique described [here](https://clickhouse.com/docs/en/operations/backup/#manipulations-with-parts).
- ClickHouse is very very fast but does very little query optimisation for you.
	- Invest as much time as needed to understand MergeTree engines and how queries are executed.
	- Make sure all the data about your entities are in a single shard. This will allow you to use `distributed_group_by_no_merge = 1` and reduce network I/O.
	- Make sure you can shut down all the processes that write to a table easily, you will need to do that before making a schema change.


Moving from Elasticsearch to ClickHouse was a long journey, but this is one of the best tech decisions we ever took. We have no regrets and this unleashed potential for new features, growth and easier scaling.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
