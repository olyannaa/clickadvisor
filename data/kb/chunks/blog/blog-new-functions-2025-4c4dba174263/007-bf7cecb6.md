---
source: blog
url: 'https://clickhouse.com/blog/semantic-versioning-udf):'
topic: new-functions-you-might-have-missed-in-2025
ch_version_introduced: '25.1'
last_updated: '2026-06-12'
chunk_index: 7
total_chunks_in_doc: 7
---

long it’s been since each of those times ``` ``` 1WITH toDateTime('2025-12-17 12:32:12') AS currentTime 2SELECT arrayJoin( 3 timeSeriesRange( 4 '2025-06-01 00:00:00'::DateTime, 5 '2025-06-01 00:01:00'::DateTime, 6 10 7)) AS ts, 8 formatReadableTimeDelta(now() - ts) AS timeAgo; ``` ```

```
┌──────────────────ts─┬─timeAgo────────────────────────────────────────────────┐
│ 2025-06-01 00:00:00 │ 6 months, 16 days, 14 hours, 10 minutes and 41 seconds │
│ 2025-06-01 00:00:10 │ 6 months, 16 days, 14 hours, 10 minutes and 31 seconds │
│ 2025-06-01 00:00:20 │ 6 months, 16 days, 14 hours, 10 minutes and 21 seconds │
│ 2025-06-01 00:00:30 │ 6 months, 16 days, 14 hours, 10 minutes and 11 seconds │
│ 2025-06-01 00:00:40 │ 6 months, 16 days, 14 hours, 10 minutes and 1 second   │
│ 2025-06-01 00:00:50 │ 6 months, 16 days, 14 hours, 9 minutes and 51 seconds  │
│ 2025-06-01 00:01:00 │ 6 months, 16 days, 14 hours, 9 minutes and 41 seconds  │
└─────────────────────┴────────────────────────────────────────────────────────┘

```
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
