---
source: blog
url: 'https://schema.org","@type":"BlogPosting","headline":"pg\_stat\_ch:'
topic: pg-stat-ch-a-postgresql-extension-that-exports-every-metric-to-clickhouse-clickhouse
ch_version_introduced: '4.6'
last_updated: '2026-10-26'
chunk_index: 13
total_chunks_in_doc: 13
---

data stack ClickHouse \+ Postgres has become the unified data stack for applications that scale. With Managed Postgres now available in ClickHouse Cloud, this stack is a day\-1 decision. [Get access](https://clickhouse.com/cloud/postgres?loc=blog-cta-62-try-the-unified-data-stack-get-access&utm_blogctaid=62)## What’s next \# We’re actively working on:

- **Query plan capture**: storing execution plans as separate events
- **Sampling support**: for extremely high\-throughput systems that can’t afford to capture every query
- **[ClickStack](https://clickhouse.com/clickstack) \& Grafana dashboard templates**: pre\-built dashboards for common patterns
- **Production hardening**: stress testing, edge cases, more version coverage

pg\_stat\_ch also pairs naturally with [pg\_clickhouse](https://clickhouse.com/blog/introducing-pg_clickhouse), our extension for querying ClickHouse from PostgreSQL. Push telemetry with pg\_stat\_ch \& query it back via foreign tables without leaving psql.

We’d love your feedback. If you run PostgreSQL in production and care about observability, try pg\_stat\_ch and tell us what works and what’s broken. Join us in our [community Slack](https://clickhouse.com/slack)!

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-global-cta&utm_blogctaid=0)

---

Share this post

- Copy URL
- [![Y Combinator icon](/_next/static/immutable/media/ycombinator.37q2g-no9bowl.svg)](https://news.ycombinator.com/submitlink?u= "Share on Y Combinator")
- [![X icon](/_next/static/immutable/media/x.3nm91lx52ia7n.svg)](https://x.com/intent/tweet?text= "Share on X")
- [![Bluesky icon](/_next/static/immutable/media/bluesky.292c8t8kns7n1.svg)](https://bsky.app/intent/compose?text= "Share on Bluesky")
- [![Facebook icon](/_next/static/immutable/media/facebook.32ysyflv7kktz.svg)](https://www.facebook.com/sharer/sharer.php?u= "Share on Facebook")
- [![LinkedIn icon](/_next/static/immutable/media/linkedin.37911rnwi-sdg.svg)](https://www.linkedin.com/sharing/share-offsite/?url= "Share on LinkedIn")
### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!

## Recent posts

[View all Blogs](/blog)![shipsidekick oct2026 banner yellow](/_next/image?url=%2Fuploads%2Fshipsidekick_oct2026_banner_yellow_da09e5fd13.png&w=750&q=75)User stories### [How Shipsidekick replaced Neon with ClickHouse Managed Postgres for 10x faster queries and better reliability](/blog/shipsidekick-neon-to-clickhouse-managed-postgres)

ClickHouse · Oct 23, 2026![langfuse cursor oct2026 banner](/_next/image?url=%2Fuploads%2Flangfuse_cursor_oct2026_banner_be7806b3ee.png&w=750&q=75)Product### [Trace and evaluate Cursor agents with Langfuse, powered by ClickHouse](/blog/cursor-agents-with-langfuse)

Hande Kafkas and Aditya Chidurala · Oct 22, 2026![openreplay banner yellow](/_next/image?url=%2Fuploads%2Fopenreplay_banner_yellow_87c6388cc3.png&w=750&q=75)User stories### [Front\-end observability at scale: How OpenReplay captures billions of daily events in real time with ClickHouse](/blog/openreplay-front-end-observability-at-scale-clickhouse)

ClickHouse · Oct 21, 2026![vera oct2026 banner](/_next/image?url=%2Fuploads%2Fvera_oct2026_banner_7c4f3bdfd1.png&w=750&q=75)Engineering### [Running ClickHouse on NVIDIA Vera CPU: Is your favorite database up to the challenge?](/blog/clickhouse-performance-on-nvidia-vera)

Robert Schulze · Oct 21, 2026[View all Blogs](/blog)## Follow us

[![X](/_next/static/immutable/media/x.3nm91lx52ia7n.svg)](https://x.com/ClickhouseDB "X")[![Bluesky](/_next/static/immutable/media/bluesky.292c8t8kns7n1.svg)](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/_next/static/immutable/media/slack.2_pspehyws_jz.svg)](/slack "Slack")[![Github](/_next/static/immutable/media/github.3ofxqpa2uzt_a.svg)](https://github.com/ClickHouse/ClickHouse "Github")[![Telegram](/_next/static/immutable/media/telegram.0054ol1lpoidb.svg)](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/_next/static/immutable/media/meetup.2tf1x11zaaepo.svg)](https://www.meetup.com/pro/clickhouse "Meetup")[![RSS](/_next/static/immutable/media/rss.1pu3aqlsglh-q.svg)](/rss.xml "RSS")
