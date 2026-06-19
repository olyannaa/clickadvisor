# Scaling SaaS security: Reco’s migration from Postgres to ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Scaling SaaS security: Reco’s migration from Postgres to ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Nov 17, 2025 · 9 minutes readIf you want to secure the modern enterprise, you can’t just look at the cloud. You have to go deeper into the SaaS applications where employees actually live and work.


That’s the idea behind [Reco](https://www.reco.ai/), an AI\-driven SaaS security solution built to discover and protect both the core apps and the long tail of niche tools used inside organizations. “We go further and deeper into your SaaS applications,” says principal data engineer Nir Barak. “Microsoft 365, Salesforce, ServiceNow, Workday—pretty much all your large enterprise applications, and also the small ones like Cursor, Monday, and Gong—we monitor, detect, and respond to potential points of risk in near real\-time.”


Today, Reco supports more than 215 integrations and can discover well over 60,000 applications. Its capabilities include application discovery (core apps, shadow apps, connected GenAI apps and embedded AI), data exposure monitoring, identity and access governance, threat detection and response, and SaaS posture management.


“We do all those things in a single unified platform, which today mostly relies on ClickHouse and its performance,” Nir says. “Our number one priority is to be fast, accurate and able to respond in near real\-time, as there’s no point in building a security system if it takes a week to alert on something that happened 10 minutes ago.”


Nir joined us on a [recent webinar](https://www.youtube.com/watch?v=QvKj8-gtP1Q) to walk through why (and how) Reco made the shift from Postgres to [ClickHouse Cloud](https://clickhouse.com/cloud)—including the scale of the challenges they faced, the technical details of the migration, and the performance wins along the way.


## Hitting the limits of Postgres [\#](/blog/reco-postgres-to-clickhouse-cloud#hitting-the-limits-of-postgres)


Reco’s platform runs at a scale most traditional databases just can’t handle. Every week, it ingests 10 to 12 billion raw JSON events, enriches them, and stores them for analysis. On top of that, the system processes 60 billion row reads and 30 billion row writes daily, and runs continuous background scans across petabytes of historical data for every tenant.


“Postgres just can’t do that—but ClickHouse does it in seconds,” Nir says.


Like many startups, Postgres had served them well in the early days. “It’s great for needle\-in\-a\-haystack queries, like finding a specific ID in a specific table, or doing very selective aggregations and transactional work,” Nir says. “Not so much when you have terabytes of data, hundreds of billions of rows that you have to aggregate and find anomalies for in a very short time frame. That’s where ClickHouse comes in.”


The team tried to balance both worlds by running Postgres and ClickHouse side by side, keeping them in sync through Change Data Capture. “It worked great for a couple of years,” Nir says, “but then we started feeling the pain of maintaining two separate databases.” Schema migrations, real\-time enrichments, and routine updates and deletes all became hurdles, and long\-running VACUUM jobs in Postgres only added to the frustration.


“These kinds of issues just don’t happen with a single source of truth database,” Nir says. The team decided it was time to move away from Postgres and consolidate on ClickHouse.


## Using ClickHouse as a relational database [\#](/blog/reco-postgres-to-clickhouse-cloud#using-clickhouse-as-a-relational-database)


Of course, moving everything onto ClickHouse wasn’t just a matter of swapping databases. Reco had to make sure it could cover the kinds of features expected from an RDBMS—things like row\-level security, upserts, deletes, transactions, and materialized views.


“ClickHouse is not a relational database, and it’s not ACID compliant,” Nir says. “But as we found out, it’s not necessarily something you must have. I’ve yet to see a dealbreaker.”


Some features translated more easily than expected. [Row\-level security](https://clickhouse.com/docs/knowledgebase/row-column-policy) and [role\-based access](https://clickhouse.com/docs/operations/access-rights), for instance, turned out to be even more flexible than in Postgres. For upserts and deletes, Reco adopted engines like [ReplacingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree) and [CollapsingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/collapsingmergetree). They also fine\-tuned settings to handle late\-arriving data that can sometimes cause older rows to “win.”


For transactions, Reco leaned on idempotency and eventual consistency rather than strict ACID guarantees. “Unless you’re in banking or have regulatory requirements, you don’t really need transactions,” Nir says. “It’s okay if things aren’t committed instantly. Eventual consistency is fine at our scale.”


ClickHouse’s [materialized views](https://clickhouse.com/docs/materialized-views) quickly became a cornerstone. Postgres only offered full refreshes, while ClickHouse supports both incremental and [refreshable materialized views](https://clickhouse.com/docs/materialized-view/refreshable-materialized-view). Nir and the team went further, implementing a tenant\-level atomic refresh pattern using [REPLACE PARTITION](https://clickhouse.com/docs/sql-reference/statements/alter/partition#replace-partition) to swap in updates without reprocessing everything.


Even joins proved better than expected. With [dictionaries](https://clickhouse.com/docs/sql-reference/dictionaries) stored in memory, [ordering keys](https://clickhouse.com/docs/integrations/clickpipes/postgres/ordering_keys), and [predicate pushdowns](https://clickhouse.com/docs/operations/settings/settings), joins performed well. “I’m not sure why joins get such a bad rap,” Nir says. “They’re really fast if you know how to use them.”


In the end, what looked like potential trade\-offs turned into opportunities. ClickHouse gave Reco the relational\-style functionality it needed, with the scale Postgres couldn’t provide.


## Optimizing performance and cost [\#](/blog/reco-postgres-to-clickhouse-cloud#optimizing-performance-and-cost)


At Reco’s scale—billions of events and queries each day—even the smallest configuration choices can be the difference between smooth operations and out\-of\-memory errors. Nir shared a few of the tricks the team has used for performance tuning and cost optimization.


One of the most important has been [compute\-compute separation](https://clickhouse.com/blog/introducing-warehouses-compute-compute-separation-in-clickhouse-cloud) in [ClickHouse Cloud](https://clickhouse.com/cloud), which lets analytical workloads run on separate clusters. “We offload all our non\-real\-time, heavy analytical work—materialized view refreshes, very large updates—into a separate warehouse,” Nir says. “That data is automatically synced back to customer\-facing nodes. It solved our out\-of\-memory issues and reduced costs.”


They’ve also reduced their memory footprint by spilling to disk for large operations, using settings like *max\_bytes\_before\_external\_group\_by* and *max\_bytes\_before\_external\_sort*. This prevents memory bottlenecks without slowing down real\-time queries. And a newer feature in [ClickHouse v.25\.6](https://clickhouse.com/blog/clickhouse-release-25-06), *parallel\_distributed\_insert\_select \= 2*, shards aggregations and joins across nodes. “That dropped our resource requirements by a third,” Nir says.


Finally, they’ve leaned on ClickHouse’s [data\-skipping indexes](https://clickhouse.com/docs/optimize/skipping-indexes) to accelerate queries without the overhead of traditional indexing. MinMax indexes handle time\-series data, set indexes take care of low\-cardinality columns, and Bloom filters work for high\-cardinality use cases. “Indexes are really cool,” Nir says, “and surprisingly very, very accurate.”


## ClickHouse as a “bonus” state store [\#](/blog/reco-postgres-to-clickhouse-cloud#clickhouse-as-a-bonus-state-store)


Reco also uses ClickHouse in a less obvious way: as a state store for streaming workloads.


Originally, the team kept state in Spark. But as Nir explains, “Very quickly, we ran out of memory, and with S3 synchronization and checksum issues, the whole thing just became a mess. We were cleaning up corrupt data all the time.” They tried to move to Redis, but, he adds, “it became untenable in terms of cost.”


The turning point came when Nir discovered that [ClickHouse OSS](https://clickhouse.com/docs/getting-started/quick-start/oss) includes an engine called [EmbeddedRocksDB](https://clickhouse.com/docs/engines/table-engines/integrations/embedded-rocksdb). That meant they could pair RocksDB’s high\-performance key\-value store with ClickHouse’s familiar SQL interface, running it all inside Kubernetes.


In the new pipeline, raw responses flow through Kafka into Spark, where they’re transformed into models. Fragmented models loop back into Kafka until they’re complete, while an aggregator writes consolidated models into ClickHouse. From there, Kafka publishes the factual, enriched models back into the pipeline.


![User Story Reco Issue 1198.png](/uploads/User_Story_Reco_Issue_1198_1c795b5365.png)
Reco’s streaming pipeline, with ClickHouse serving as the state store between Kafka and Spark.


“We’ve been running this setup for about two years now, with billions of states and events and just everything,” Nir says. “I hadn’t even thought about it until this week. It just works.”


## Speed, scale, and cost savings [\#](/blog/reco-postgres-to-clickhouse-cloud#speed-scale-and-cost-savings)


For Nir and the Reco team, moving to ClickHouse Cloud has been transformative. What started as a workaround to Postgres’s limits has become the spine of their security platform, powering everything from real\-time dashboards to large\-scale streaming workloads.


Nir sums it up: “We’ve removed more than 90 percent of our workload from Postgres and moved it onto ClickHouse with almost no drawbacks—just advantages. The cost has gone down, the speed has gone up, and the scale of our customers has increased exponentially.”

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-9-get-started-today-sign-up&utm_blogctaid=9)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
