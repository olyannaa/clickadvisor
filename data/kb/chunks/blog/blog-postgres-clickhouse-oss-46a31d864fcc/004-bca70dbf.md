---
source: blog
url: https://clickhouse.com/blog/postgres-managed-by-clickhouse
topic: postgresql-clickhouse-as-the-open-source-unified-data-stack
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 4
---

handling failures often become the limiting factors rather than the architecture itself. We recently [launched a managed version of the unified data stack](https://clickhouse.com/blog/postgres-managed-by-clickhouse) that delivers the same architecture as a single, integrated experience under one ClickHouse Cloud account.

Deployment, scaling, upgrades, and reliability are handled by the platform, removing the need to operate clusters or data pipelines manually. PostgreSQL by ClickHouse connects directly to ClickHouse through [ClickPipes](https://clickhouse.com/cloud/clickpipes), the managed alternative to PeerDB. Managed PostgreSQL also comes with the pg\_clickhouse extension preinstalled and configured, allowing analytical queries to be offloaded to ClickHouse without rewriting applications.

### Get started with our native Postgres Service

To try ClickHouse's native Postgres service, sign up for Private Preview using this link.

[Sign up](https://clickhouse.com/cloud/postgres?loc=blog-cta-44-get-started-with-our-native-postgres-service-sign-up&utm_blogctaid=44)## A new baseline [\#](/blog/postgres-clickhouse-oss#a-new-baseline)

PostgreSQL and ClickHouse are not competing databases. They are complementary systems designed for different workloads.

With mature CDC and query offload tooling, using both from the start no longer requires complex pipelines or duplicated application logic. PostgreSQL remains the system of record for transactions, while ClickHouse handles analytical queries efficiently as data volume and query complexity grow.

**The default open data stack is no longer a single database. It is PostgreSQL for transactions, ClickHouse for analytics, and a clean, well\-defined bridge between the two.**

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
