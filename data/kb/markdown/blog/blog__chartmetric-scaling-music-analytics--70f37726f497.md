# Behind the music: How Chartmetric is scaling music analytics with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Behind the music: How Chartmetric is scaling music analytics with ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 8, 2026 · 10 minutes read## Summary

Chartmetric uses ClickHouse Cloud to deliver real\-time analytics on billions of rows of music, playlist, and engagement data. They migrated from Postgres and Snowflake to improve speed and reduce storage; queries now run 10\-15x faster at much lower cost. Today, ClickHouse powers a 5\.5B\-row playlist cache that ingests 15M\+ new rows daily, plus LLM\-facing queries using batched WHERE \+ IN filters and projections.

[Chartmetric](https://chartmetric.com/) tracks the pulse of the music industry. Every day, the platform ingests millions of rows of data from streaming services, social media, and music charts, powering dashboards for A\&R teams, reports for record labels, and insights for artists navigating their next move.


By 2024, that data footprint had ballooned into the billions and their systems weren’t scaling fast enough to keep up. [This past March](https://clickhouse.com/blog/chartmetric-uses-clickhouse-to-turn-artist-data-into-music-intelligence), lead engineer Peter Gomez shared how the team tackled the challenge by migrating time\-series workloads from Postgres and Snowflake to [ClickHouse Cloud](https://clickhouse.com/cloud). The move sped up slow queries and cut RDS storage by 10 TB.


Since then, the team has gone even further. ClickHouse now powers production workloads across the company, from LLM\-ready queries to a massive playlist cache pipeline that refreshes every five minutes. What began as a targeted performance fix has evolved into a foundational part of Chartmetric’s real\-time data stack.


At a [September 2025 meetup in Toronto](https://clickhouse.com/videos/toronto-meetupSep1), lead data engineer Umang Sharaf shared what that evolution looks like today. He walked through the team’s architecture, new query patterns, and the tradeoffs of scaling a playlist cache that ingests over 15 million new rows a day.


## Chartmetric’s journey to ClickHouse [\#](/blog/chartmetric-scaling-music-analytics#chartmetrics-journey-to-clickhouse)


Today, Chartmetric handles around 300,000 requests per hour—roughly 80 per second—across a web app, external API, and small public API. The platform tracks more than 12 million artists, 140 million tracks, 45 million albums, and nearly 30 million playlists.


“These numbers are growing rapidly,” Umang says. “The number of artists grew by 13% in just a year as new artists join Spotify, Apple Music, Amazon, and other platforms.”


Before 2024, the team relied on a mix of Postgres, Snowflake, Elasticsearch, and Airflow. Postgres handled core application data and business logic, Snowflake supported analytics, Elasticsearch powered search and filtering, and Airflow orchestrated data pipelines. But none of these systems were built for the scale and flexibility Chartmetric needed.


“Storage was costly, with a lot of infrequent and cold\-access data,” Umang says, noting their AWS Aurora RDS footprint included 28 TB of historical data. Snowflake, which ran 700\+ cache and transform tables daily, was “very expensive and obviously not suitable for our API latency needs.” Elasticsearch, meanwhile, was fast and responsive, but “only for specific use cases—and writing JSON isn’t as easy as writing SQL,” he adds.


Chartmetric’s ClickHouse journey began with a small EC2 instance. “But as we started using it more,” Umang says, “our usage and our infrastructure needs increased.” In summer 2024, they migrated to [ClickHouse Cloud](https://clickhouse.com/cloud). Today, they use multiple warehouses tailored to specific workloads: “one for the application and the API (read\-only), one for data science and analytics, and one for data engineering tasks like sync and ETL,” Umang says.


## The importance of projections [\#](/blog/chartmetric-scaling-music-analytics#the-importance-of-projections)


Back in March, Peter described how migrating time\-series data from Postgres and Snowflake to ClickHouse led to a 10 TB storage reduction and major improvements in query speed. At the Toronto meetup, Umang dove deeper into the challenges and optimizations that followed.


As Umang explains, the issue they faced wasn’t ingest performance. “ClickHouse is very efficient for ingesting new data,” he says. “That part went off without a hitch.”


The real challenge was sync. The tables had been ordered for API access, not for update patterns. In Postgres, B\-tree indexes handled it fine. But in ClickHouse, hourly sync jobs began running into timeouts and memory issues.


The solution was [projections](https://clickhouse.com/docs/sql-reference/statements/alter/projection), which Umang describes as “not quite clustering, not quite indexing… they’re essentially mini\-tables that are maintained directly by ClickHouse—a good hands\-off implementation, so that instead of creating, maintaining, and referencing multiple views from API code, it all just lives within the base table itself.”


One projection surfaces the most recently modified rows. Another is sorted by ISRC, the music industry’s equivalent of a book’s ISBN. These allow precise queries without full scans. The team often uses multiple projections per table depending on workload. And while Umang notes that projections can complicate deletes, the tradeoff is worth it. “This provided huge flexibility compared to Snowflake’s single clustering key,” he says.


With this approach, migrating just eight time\-series tables cut their RDS footprint from 28 TB to 18 TB—a 36% savings. And even queries scanning back to 2016, which frequently timed out after a minute in Postgres and Snowflake, now run in under three seconds.


## Rethinking JOINs with WHERE \+ IN [\#](/blog/chartmetric-scaling-music-analytics#rethinking-joins-with-where--in)


As Chartmetric expanded its use of ClickHouse beyond time\-series workloads, they began creating [flattened, denormalized tables](https://clickhouse.com/docs/data-modeling/denormalization) to support an LLM\-based interface for querying artist and track data. But joining large datasets—track metadata, metrics, playlist history—was easier said than done. “We frequently ran into out\-of\-memory issues,” Umang says.


Earlier this year, Peter shared a few initial lessons about limiting JOIN complexity: pre\-join wherever possible, avoid joining more than one large table per query, and use projections to speed up scans. Still, the team saw room to improve.


The breakthrough came when they shifted to using [WHERE](https://clickhouse.com/docs/sql-reference/statements/select/where) and [IN](https://clickhouse.com/docs/sql-reference/operators/in) filters instead of joins. Rather than joining directly on artist and track tables, they’d first extract a list of relevant track IDs, then use that list to filter the main table. To reduce memory load, they split queries into smaller batches using [LIMIT](https://clickhouse.com/docs/sql-reference/statements/select/limit) and [OFFSET](https://clickhouse.com/docs/sql-reference/statements/select/offset).


The impact was huge. A query pulling track metadata for Taylor Swift’s songs initially scanned 17,000\+ granules and attempted to use nearly 30 GB of memory, resulting in an error. After switching to WHERE \+ IN, the same query scanned fewer than 400 granules, ran in 98 milliseconds, and used just 300 MB of memory.


The team took it further by layering batching on top of those filters. For a query pulling all playlist history for Swift’s tracks since 2016, the raw join took 107 seconds and used 5 GB of memory. After batching, each subquery ran in under 0\.5 seconds using just 44 MB of memory.


“It took 50% less time and over 99% less memory,” Umang says. “In some cases, it was slower than a regular join, but these are overnight queries, so it wasn’t an issue. Reducing memory usage was an important goal for us, and this really helped a lot.”


## Perfecting the playlist cache [\#](/blog/chartmetric-scaling-music-analytics#perfecting-the-playlist-cache)


The playlist cache is one of Chartmetric’s most important and complex tables. It tracks which artists appear across nearly 30,000 playlists, how often, in what position, and across what types (e.g. editorial, algorithmic, branded). It supports filters by artist, track, album, or playlist ID, and stores data going back nearly a decade. Users rely on it to see near real\-time changes, especially on Fridays, when platforms like Spotify refresh top playlists.


At the time of Peter’s talk in March, the table held around 2 billion rows, with more than a million rows added daily. The pipeline ran hourly, with deletion markers generated in Snowflake and synced into ClickHouse. To support this, the team used the [VersionedCollapsingMergeTree engine](https://clickhouse.com/docs/engines/table-engines/mergetree-family/versionedcollapsingmergetree), which let them “invalidate” old rows using a row\_active flag and insert updated versions, without relying on [FINAL](https://clickhouse.com/docs/sql-reference/statements/select/from#final-modifier) queries or background deduplication.


Since then, the system has scaled significantly, and the team has continued to refine it. In July, they moved the entire ingestion pipeline over to ClickHouse. “We’re now able to run it every five minutes, which has scaled very well for us,” Umang says. “In fact, we run it every five minutes, but it frequently takes less than two.”


Today, the playlist cache table holds 5\.5 billion rows and ingests 15 million new records daily. It includes 31 columns covering everything from playlist type to position history, yet the entire compressed table size is just 340 GB. “Compare that to Postgres,” Umang says, “where the raw data with only seven columns took up half a terabyte.”


Query performance has also seen a major leap. Whereas in Postgres queries often timed out around the 60\-second mark, and Snowflake took around 20 seconds for top\-artist queries, those same queries now return in about 1\.5 seconds in ClickHouse, even with complex filters. “That’s been great for our application and the API,” Umang says.


## Fast, flexible, and stackable [\#](/blog/chartmetric-scaling-music-analytics#fast-flexible-and-stackable)


As Umang puts it, “ClickHouse works very well as part of a multi\-system data stack.” Postgres remains essential for maintaining consistency and running complex relational queries, and Snowflake continues to support black\-box analytics—but ClickHouse has proven to be “excellent for time series data,” at a much lower cost.


He calls the VersionedCollapsingMergeTree engine a “game changer” and adds, “A speed\-up from 20 seconds to 1\.5 seconds was very significant.” While they initially struggled with large JOINs, they overcame those challenges using batching and projections. “ClickHouse was very flexible for us,” he says, adding a shoutout to the ClickHouse Cloud support team.


For Chartmetric, the result is a system that’s fast, scalable, and perfectly suited to real\-time analytics, while integrating cleanly alongside other tools in the stack.

### Get started today

Does your team’s data stack need a boost? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-34-get-started-today-sign-up&utm_blogctaid=34)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
