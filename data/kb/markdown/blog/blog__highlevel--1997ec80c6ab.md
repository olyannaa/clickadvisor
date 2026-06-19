# How HighLevel rebuilt its data platform for speed, scale, and simplicity on ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How HighLevel rebuilt its data platform for speed, scale, and simplicity on ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 12, 2026 · 11 minutes read## Summary

HighLevel’s marketing platform uses ClickHouse Cloud to power real\-time lead activity, workflow logs, notifications, and revenue dashboards at massive scale. They migrated key workloads off MySQL, Elasticsearch, Firestore, and a document database, unifying operations and analytics on a single, low\-latency platform. They achieved 88% storage reduction, sub\-200ms queries (down from \~6 seconds in MySQL), and the ability to handle billions of daily events with just a few replicas.

[HighLevel](https://www.gohighlevel.com/) is an all\-in\-one marketing and sales platform that gives customers everything they need to capture, nurture, and close more leads. Today, it’s the operating system for more than 90,000 agencies serving 3 million small businesses, handling around 4 billion API requests and 2\.5 billion message events every day. Behind the scenes, it manages 250 TB of data, powers more than 250 backend services, and serves over a million hostnames.


At that scale, even small inefficiencies become real problems—and for a while, that’s exactly what happened at HighLevel. As usage surged, different parts of the system began hitting limits at different times. Queries slowed. Logs backed up. Workloads that once felt manageable started to reveal the architectural strain beneath the surface. It became clear that the old assortment of databases powering the platform—MySQL, Elasticsearch, Firestore, and a document database—weren’t going to carry them much further.


At our [October 2025 Open House roadshow in Bangalore](https://clickhouse.com/videos/open-house-bangalore-highlevel), HighLevel VP of Engineering Kiran Raparti and Staff Engineer Pragnesh Bhavsar walked through their decision to unify operations and analytics on [ClickHouse Cloud](https://clickhouse.com/cloud), and what that shift has meant across some of their highest\-volume use cases.



## The pains that led them to ClickHouse [\#](/blog/highlevel#the-pains-that-led-them-to-clickhouse)


Before migrating to ClickHouse, HighLevel was running five different data stores. As usage surged, three of those systems—MySQL, Elasticsearch, and a document database—began failing in predictable but increasingly unmanageable ways.


In the case of MySQL, Kiran recalls, “It was at a pace where it was crawling and not responding to any queries.” Reads that should have been instant often took seconds, especially under the weight of 65,000 inserts per second in peak moments.


Elasticsearch posed a different challenge. Its shard layout had to be constantly rebalanced just to stay afloat. “We ended up re\-sharding it so many times, we almost gave up,” Kiran says.


The document database, meanwhile, suffered from severe index sprawl. As workloads grew, so did the number of indexes required—until, as Kiran puts it, “the index size was more than the actual data size.”


The team knew they needed a different foundation. What they wanted, Kiran says, was a database that could deliver “high throughput, low latency, and low operational overhead.” Just as important, it had to provide easier archival and a time\-series\-friendly engine for logs.


Cost, while not a deciding factor, became an unexpected benefit once they eventually adopted [ClickHouse Cloud](https://clickhouse.com/cloud). “We weren’t looking at cost because we wanted to serve customers first, then look at optimizations,” Kiran says. “But cost was a byproduct.”


## Use case \#1: Lead activity [\#](/blog/highlevel#use-case-1-lead-activity)


The first use case Kiran and Pragnesh walked through was lead activity—every click, form fill, quiz response, call, and conversion event flowing through HighLevel’s platform.


For years, all of this data lived in a MySQL table that quietly grew to 11 TB. With 30 million new rows arriving each day and read traffic climbing to 150 queries per second, performance began to suffer. “When a contact or lead has too many activities, it creates latency issues,” Pragnesh explains. “The read could take 50 or 60 seconds, and sometimes even time out.”


Even routine schema changes were painful. Adding a new activity type meant adding a new column, which, on a table of that size, was an operational event in itself. “Forget about indexing,” Pragnesh says. As the dataset grew, maintenance became more and more demanding, yet performance continued to deteriorate.


Moving to ClickHouse Cloud changed things almost immediately. The same 11 TB table compressed down to 1\.3 TB—“a whopping 88% reduction,” Pragnesh says—while the team gained the flexibility of [storage\-compute separation](https://clickhouse.com/docs/guides/separation-storage-compute). “We don’t worry about scaling compute anymore,” he says. “If our traffic is increasing, we just add replicas and we’re good.”


From a performance standpoint, P99 latencies that once exceeded six seconds in MySQL dropped to under 200 milliseconds, and the 5xx timeouts that once plagued the system effectively disappeared. “This is a great achievement for us,” Pragnesh says.


### Use case \#2: Workflow logs [\#](/blog/highlevel#use-case-2-workflow-logs)


Next up was workflow logs, which capture every automation step in a customer campaign. At HighLevel’s scale, those logs add up fast—roughly 1 TB of new data per day (about 600 million rows) and doubling every year. The team initially stored this dataset in their document database, but as Pragnesh says, “We realized in six months that that wouldn’t work at all.”


They migrated the workload to Elasticsearch, but new problems emerged. Storage ballooned to nearly 60 TB. Write throughput was heavy, and scaling required constant node additions—not for CPU or memory, but simply to get past EBS volume limits. “Let’s say today we have 12 nodes,” Pragnesh says. “Next month, I’ll need to add two more nodes just to increase the EBS size, and CPU usage will still stay below 10%.”


With ClickHouse Cloud, that 60 TB dataset shrank to 6\.27 TB—an 88% reduction. And instead of running a dozen (sometimes up to 25\) Elasticsearch nodes, HighLevel now serves the entire workload on just three ClickHouse replicas. With storage and compute separated, scaling is predictable, efficient, and cost\-effective.


## Use case \#3: Notifications [\#](/blog/highlevel#use-case-3-notifications)


Notifications proved to be one of the trickiest migrations—not because the core data changed frequently, but because it *almost* did. As Pragnesh explains, the raw notification objects themselves are immutable, but the *state* around them isn’t. “When a user clicks on a notification, we need to store whether it was read,” he says. “And when a customer is deactivated, we delete all notifications for that user.” That combination—a write\-once event with mutable read/delete metadata—created challenges for their old systems.


Originally, the workload was spread across Firestore and the document database. Firestore stored the raw notifications but couldn’t support the aggregation queries the team needed. So they pushed the most recent three months of notifications into the document database. But as usage grew, it hit vertical scaling limits: more indexes led to more disk IOPS, infrastructure costs climbed to $21,000 per month, and latency jumped even after scaling all the way to a 48\-vCPU M140 instance. “We were just vertically scaling the database,” Pragnesh says. “To solve these problems permanently, we started exploring ClickHouse.”


Designing the right table structure was key to making notifications work in ClickHouse. The team split the workload across three tables: a [MergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree) table for immutable raw notifications, a [ReplacingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree) table for read/delete state, and a third table, populated via [materialized view,](https://clickhouse.com/docs/materialized-views) for location\- and contact\-level deletions. This aligned the data model with real\-world query patterns: timeline fetches, unread counts, and efficient multi\-step joins.


From there, they focused on performance optimizations. Early on, they relied on [FINAL](https://clickhouse.com/docs/sql-reference/statements/select/from#final-modifier) to resolve read/delete status—but as Pragnesh says, “It was creating so much merge work, it was degrading performance.” Switching to [argMax](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/argmax) gave them the same “latest state” logic without triggering expensive merges. They also added [Bloom filters](https://clickhouse.com/docs/sql-reference/statements/select/from#final-modifier) on selective fields and refined their [partitioning](https://clickhouse.com/docs/partitions) strategy, since weekly or biweekly partitions created too many segments, while quarterly partitions were too large. Two\-month partitions gave them the best balance, scanning only what’s needed for the three\-month history users typically view.


With the move to ClickHouse and these subsequent optimizations, storage dropped from roughly 1\.6 TB x 2 across Firestore and the document database to 644 GB in ClickHouse, a 60% reduction. P95 queries that once took 4\-8 seconds during peak hours now return in under 500 milliseconds. And instead of pushing the document database up to a 48\-vCPU M140 instance, the entire workload runs horizontally on just five ClickHouse replicas.


## Use case \#4: Usage summaries, real\-time notifications, and revenue dashboards [\#](/blog/highlevel#use-case-4-usage-summaries-real-time-notifications-and-revenue-dashboards)


The final use case focused on the data behind HighLevel’s agency billing dashboards. In the old architecture, everything flowed through the document database: transactional records were written there first, then a daily cron job re\-inserted those same records into new collections to support downstream queries. The result was predictable but painful: a full day of lag, constant reprocessing, and a database that wasn’t built for analytical workloads. Worse, every new index to support reporting made writes more expensive and further strained the system.


With ClickHouse, the team replaced this entire flow with a much cleaner, real\-time pipeline. In the new setup, events stream into Google Cloud Storage, are ingested into ClickHouse, and feed materialized views that power each dashboard.


Now, more than 70 million batch records and 40 million real\-time records move through the pipeline, with “materialized views on steroids” (as Pragnesh puts it) using [SummingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/summingmergetree) for fast rollups. P95 latencies land between 50 and 100 milliseconds—an enormous improvement over the day\-long delay of the old setup.


## Client\-side observability to monitor all use cases [\#](/blog/highlevel#client-side-observability-to-monitor-all-use-cases)


With so many microservices querying the same ClickHouse clusters, HighLevel needed a clear view of *who* was doing *what*—which service was issuing which query, how often, and with what latency. “We didn’t know which instance or which microservice was calling this, how many API or database calls they were making, or what methods they were using,” Pragnesh says. Without that visibility, debugging was mostly guesswork.


The team built a lightweight client\-side observability layer directly into their Node.js ClickHouse client. They wrapped core database operations—query, insert, exec, and command—with a proxy that emits structured metadata for every call. These events flow into Grafana, where engineers can break down latency histograms, error counts, and query volumes by microservice, table, or operation.


The result is end\-to\-end visibility across all ClickHouse workloads. As Pragnesh says, “It shows what the application is doing, what table it’s touching, and how each query performs.”


## Lessons learned and looking ahead [\#](/blog/highlevel#lessons-learned-and-looking-ahead)


After working through four very different migrations, Kiran and Pragnesh came away with a handful of principles that now guide every new ClickHouse project at HighLevel.


The first is simple: avoid update\-heavy patterns whenever possible. Aside from notifications, where state must change, nearly all data is modeled as immutable, which plays to ClickHouse’s strengths. The second is the importance of getting the schema right. “Every table goes through two or three iterations before it reaches production,” Pragnesh says. [Primary keys](https://clickhouse.com/docs/best-practices/choosing-a-primary-key), [order\-by clauses](https://clickhouse.com/docs/sql-reference/statements/select/order-by), and [partitions](https://clickhouse.com/docs/partitions) are all optimized with real query patterns in mind.


They also stress the value of [bulk inserts](https://clickhouse.com/docs/optimize/bulk-inserts) for keeping merges efficient and ingestion smooth at scale. And finally, observability—across clients, clusters, and queries—is now treated as part of the product, not an afterthought.


Taken together, these lessons reflect a broader shift. What once felt like nonstop “firefighting” across half a dozen systems has become a unified, predictable, high\-performance data platform—one that finally moves at the same pace as HighLevel’s growth.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-35-get-started-today-sign-up&utm_blogctaid=35)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
