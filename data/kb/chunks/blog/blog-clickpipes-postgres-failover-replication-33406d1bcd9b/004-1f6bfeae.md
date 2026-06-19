---
source: blog
url: https://www.postgresql.org/docs/current/hot-standby.html
topic: clickpipes-for-postgres-now-supports-failover-replication-slots
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 4
---

the same as the UUID of the ClickPipe). This slot is synced from the primary and has synced and failover set to true. This slot is now ready to use when the standby is promoted. ## Conclusion [\#](/blog/clickpipes-postgres-failover-replication#conclusion)

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
