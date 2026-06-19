# ClickPipes for Postgres now supports failover replication slots


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickPipes for Postgres now supports failover replication slots

![](/_next/image?url=%2Fuploads%2FImage_512x512_4_929da07148.jpeg&w=96&q=75)[Kevin Biju Kizhake Kanichery](/authors/kevin-biju-kizhake-kanichery)Nov 11, 2025 · 5 minutes read## Introduction [\#](/blog/clickpipes-postgres-failover-replication#introduction)


To continue providing maximum reliability and flexibility for all Postgres ClickPipes users, we have now added a toggle to allow creating a logical replication slot with failover enabled. This allows ClickPipes to work seamlessly with high\-availability (HA) to preserve replication slots post\-failover.


## Background [\#](/blog/clickpipes-postgres-failover-replication#background)


Postgres has a feature known as [hot standbys](https://www.postgresql.org/docs/current/hot-standby.html) that allows "read replicas" of a Postgres instance to be spun up for querying. Hot standbys recently gained the ability to perform logical decoding (introduced in Postgres 16, released 2023\), which allows users to move their CDC workloads off their primary instance. However, this was not enough to unlock high availability for CDC, as any slots created were only for that cluster and not replicated in any manner. In Postgres 17 (released 2024\), this was addressed by enabling logical replication failover, which essentially selects slots on the primary instance to be periodically synchronized to one or more standbys in a way that allows logical decoding to resume cleanly after a standby is promoted.


## Why would you want this? [\#](/blog/clickpipes-postgres-failover-replication#why-would-you-want-this)


Postgres is quintessentially a "core" database for transaction processing, and that has often necessitated high\-availability via standbys (as Postgres is a single\-writer design). However, as query workloads diversify, it is becoming increasingly common to replicate data from Postgres to other sources via CDC to leverage their strengths. Until very recently, while Postgres itself was HA, these pipelines were not. Logical replication failover now makes this a reality.


## Process [\#](/blog/clickpipes-postgres-failover-replication#process)


Although the ClickPipe itself only contains a toggle to enable failover, the entire process of preparing failover slots for use is more complex and has several prerequisites. If you are using Postgres on\-premises, you can configure it using the steps below. If you are running Postgres through a managed provider (such as [AWS RDS](https://aws.amazon.com/rds/) or [Google CloudSQL](https://cloud.google.com/sql?hl=en)), you'll need to work with your provider to ensure that the Postgres configuration settings are correctly tuned. Some providers, such as [PlanetScale for Postgres](https://planetscale.com/postgres), already [support](https://planetscale.com/docs/postgres/integrations/logical-cdc#configure-planetscale-cluster-for-failover) this feature as they perform failovers as part of their periodic maintenance.


1. Your primary and hot standby servers should both be running Postgres 17 or later. Your hot standby should use a physical replication slot to receive changes from the primary (as opposed to WAL archival and restore). Most managed services already set up read replicas in this manner.
2. To ensure your standbys are set up to handle primary crashes, you should have both [synchronous\_standby\_names](https://postgresqlco.nf/doc/en/param/synchronous_standby_names/) and [synchronous\_commit](https://postgresqlco.nf/doc/en/param/synchronous_commit/) set up so that the primary needs to confirm WAL receipt by a standby before acknowledging a commit, ensuring changes are persisted unless both the primary and standby go down. Again, most managed services already have this setup, but adjustments can be made based on the specific guarantees required.
3. You need to enable the settings [hot\_standby\_feedback](https://postgresqlco.nf/doc/en/param/hot_standby_feedback/) and [sync\_replication\_slots](https://postgresqlco.nf/doc/en/param/sync_replication_slots/) on the standby. sync\_replication\_slots tells the standby to start a slotsync worker that synchronizes slots from the primary. This setting, in turn, requires hot\_standby\_feedback for doing this reliably.
4. You need to add the physical replication slot being used by your hot standby to [synchronized\_standby\_slots](https://postgresqlco.nf/doc/en/param/synchronized_standby_slots/) on the primary. This ensures that the standbys confirm receipt of WAL containing changes before they're sent on the logical replication slot being used by the ClickPipe. Without this, it's possible that the standby is "behind" the ClickPipe and is unable to resume properly after failover.
5. When creating the ClickPipe, ensure that you select the option to [create a replication slot with failover enabled](https://clickhouse.com/docs/integrations/clickpipes/postgres/faq#failover-slot).
Loading video...6. After the ClickPipe is created and is in the Running state, query pg\_replication\_slots on the standby to see a slot starting with mirror\_ (the UUID of the slot is the same as the UUID of the ClickPipe). This slot is synced from the primary and has synced and failover set to true. This slot is now ready to use when the standby is promoted.


## Conclusion [\#](/blog/clickpipes-postgres-failover-replication#conclusion)


The ClickPipes team is hard at work improving our existing connectors while delivering more ways to replicate data to ClickHouse. With support for logical replication failover, users can now confidently rely on Postgres ClickPipes to replicate critical data and gain all the advantages of ClickHouse's query performance for real\-time analytics use cases. We also continue to support replicating from hot standbys directly, which can help alleviate some load from the primary for other workloads.


If you'd like to run queries on [ClickHouse Cloud](https://clickhouse.com/cloud) with your data in Postgres, we recommend [ClickPipes for Postgres](https://clickhouse.com/docs/integrations/clickpipes/postgres), which provides reliable, real\-time replication without requiring infrastructure management. Self\-hosted ClickHouse users should consider [PeerDB](https://github.com/PeerDB-io/peerdb), the battle\-hardened CDC tool that powers all Postgres ClickPipes.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-8-get-started-today-sign-up&utm_blogctaid=8)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
