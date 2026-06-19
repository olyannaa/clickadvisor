# How Chartmetric uses ClickHouse to turn artist data into music intelligence


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Chartmetric uses ClickHouse to turn artist data into music intelligence

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 21, 2025 · 10 minutes readFor decades, the music industry has struggled to keep up with the data it generates. Even in the streaming era, artists and labels have often relied on spreadsheets, siloed tools, and manual reports to understand performance and spot trends.


[Chartmetric](https://chartmetric.com/) is changing that. Founded in 2015, the company offers a music analytics platform that pulls together millions of data points—streaming counts, social signals, playlist placements, chart rankings—and turns them into insights. Today, it’s the source of truth for major labels, managers, artists, A\&R teams, live event companies, and brand partners looking to discover talent, track momentum, and measure impact in real time.


But delivering that kind of visibility isn’t easy. As Chartmetric scaled, indexing more than 11 million artists, 140 million tracks, and 26 million playlists across platforms like Spotify, YouTube, Instagram, and TikTok, data volumes soared. Events like Spotify’s “New Music Friday” raised the stakes even higher, with users expecting fresh, accurate insights with every click.


At a [March 2025 meetup in San Francisco](https://www.youtube.com/watch?v=gd1yWbnaalk), lead engineer Peter Gomez shared how ClickHouse Cloud helped Chartmetric keep up—starting with time\-series performance and evolving to support even their most complex, relational workloads.


## Growing up fast [\#](/blog/chartmetric-uses-clickhouse-to-turn-artist-data-into-music-intelligence#growing-up-fast)


Chartmetric began like many startups do: with Postgres at the core. It handled relational workloads well, modeling artists, tracks, albums, playlists, and the intricate links between them. As the product matured, they layered in Snowflake for analytics and Elasticsearch for full\-text search across their growing artist index.


For a few years, this trio held up. “In the beginning, we didn’t have much data,” Peter explains. But as Chartmetric grew, so did the pressure on their infrastructure. Time\-series workloads, like streaming and follower counts, became heavier. Query latency ticked up.


“Customers would click a button and wait a minute or more, and they’d be happy to do it, because that’s less than the week they were used to,” Peter says. “But eventually we heard complaints. Once requests started hitting the 90\-second timeout, it became a nightmare.”


In 2024, the team began experimenting with ClickHouse. They spun up the open\-source version on EC2 to offload some of their heaviest time\-series queries. It improved performance and gave them a glimpse of what a faster, more scalable analytics engine could do.


But self\-hosting came with its own challenges. “We were used to managed services, where monitoring is handled for us,” Peter says. “When we started self\-hosting, I just knew Prometheus and Grafana were important, so I installed them—on the same node.” It was a crash course in metrics, observability, and keeping ClickHouse stable under load. “That was fun,” he adds with a smile.


Things hit a wall when their deployment passed the 8 TB mark. “I had to learn how to do online storage upgrades and deal with all the hassle EBS puts you through,” Peter says. “That’s when we realized, alright, we want a managed service.”


## Migrating to ClickHouse Cloud [\#](/blog/chartmetric-uses-clickhouse-to-turn-artist-data-into-music-intelligence#migrating-to-clickhouse-cloud)


Chartmetric’s migration to [ClickHouse Cloud](https://clickhouse.com/cloud) took less than a day. Peter calls it an “extremely smooth” process, adding, “That was a year ago, so it’s probably even better now.”


The move unlocked a wave of benefits. For one, the team was “blown away” by ClickHouse’s compression. “We’re talking four or five TB down to less than 60 GB, without any manual tuning,” Peter says. “This is just insane and really saves costs.”


Support, too, has beat their expectations. “There’s technical support, but there’s also use case support,” he says. “You can go to them and say: here’s our data, here’s our use case—what do we do? How would *you* do this? They’ll help you design a solution, recommend the right engine, and make optimizations if you have any issues with your queries. It’s a very white\-glove service. This is really nice when nobody on your team knows ClickHouse.”


ClickHouse Cloud also gave them confidence to expand their use cases. Inspired by a talk at a previous ClickHouse meetup, they rolled out OpenTelemetry and began piping logs and metrics directly into ClickHouse. Today, they’re storing over 20 TB of observability data (uncompressed) and querying it live with no performance concerns. “It feels so good to query this live, to get useful information out of it,” Peter says.


More than anything, ClickHouse Cloud has made their lives easier. “The biggest advantage is the hands\-off experience,” Peter says. “You don’t realize how many little things there are until you have to do them, especially when you’re doing them by hand.”


## Making time\-series fly [\#](/blog/chartmetric-uses-clickhouse-to-turn-artist-data-into-music-intelligence#making-time-series-fly)


One of Chartmetric’s first big wins with ClickHouse Cloud came from migrating time\-series tables out of Postgres RDS. These tables tracked metrics like streaming counts, follower growth, and playlist performance. They were updated daily and queried often.


Over time, those queries had become painfully slow in Snowflake and Postgres. Some took over a minute. Others timed out entirely. To speed things up, the team built a custom migration script that converted schema definitions from Snowflake and RDS into ClickHouse DDL. “Man, that script made things fast,” Peter says. It helped automate what would’ve been a complex, tedious process, especially with so many databases to sync.


To make daily syncs even more efficient, they added [projections](https://clickhouse.com/docs/sql-reference/statements/alter/projection) that surfaced the most recent data in each table, no matter how the API queries were ordered. This reduced the overhead of idempotent, retriable logic and minimized the need for full table scans.


The payoff came right away. Queries that once failed now ran in six seconds, with no caching required. And by moving those tables off Aurora, they cut RDS storage by 10 TB. “Not only was it cheap, but it was fast,” Peter says.


## Relational logic, ClickHouse speed [\#](/blog/chartmetric-uses-clickhouse-to-turn-artist-data-into-music-intelligence#relational-logic-clickhouse-speed)


The more ambitious challenge was Chartmetric’s artist\-playlist cache: a massive, highly relational table that tracks when artists appear on playlists, how long they stay, and whether those playlists are editorial, algorithmic, or personalized.


The dataset spans more than two billion rows, with historical activity going back to 2016 and over a million rows added daily. It supports complex querying patterns, letting users filter by artist, track, or album ID, and slice by playlist type. It also requires a complex ingestion model with inserts, updates, and deletes, plus hourly refreshes to support near real\-time use cases.


“This isn’t the type of use case ClickHouse is generally happy with,” Peter says. “But Snowflake was even less happy. And as happy as Postgres would be… two billion rows on Postgres? You do the math. Not happy for us.”


The biggest hurdle was handling deletes. The team built a table in Snowflake to generate deletion markers, then synced them into ClickHouse. Instead of relying on the [FINAL](https://clickhouse.com/docs/sql-reference/statements/select/from#final-modifier) query modifier or background deduplication, they adopted a strict “no duplicates” policy: each record was tagged as active or inactive using a custom row\_active flag. That let ClickHouse safely collapse outdated records using the [VersionedCollapsingMergeTree engine](https://clickhouse.com/docs/engines/table-engines/mergetree-family/versionedcollapsingmergetree), without requiring expensive queries.


Peter calls the solution a “massive success.” Queries that used to take over five minutes in Postgres now run in around two seconds in ClickHouse. “It took a few weeks to figure out, but once we got it working, it was amazing,” he says. “It goes to show that highly relational data *can* work on ClickHouse—you just need to be creative.”


## Not a silver bullet (and that’s okay) [\#](/blog/chartmetric-uses-clickhouse-to-turn-artist-data-into-music-intelligence#not-a-silver-bullet-and-thats-okay)


ClickHouse has become an essential part of Chartmetric’s infrastructure, but it’s not a replacement for everything. “It looks like a silver bullet,” Peter says. “But it’s not. Nothing is.”


That’s especially true when it comes to complex joins. Coming from Snowflake, where massive compute warehouses abstract away the pain, the team had to reset their expectations. In ClickHouse, joins can be expensive and sometimes break entirely. “ClickHouse is non\-relational,” Peter explains. “It looks relational. It lets you type JOIN, but you have to think differently. And if you forget that, you’ll get out\-of\-memory errors—a lot of them.”


His advice: join *before* you get to ClickHouse. Do it in Snowflake, or Postgres, or wherever your pipeline allows. And when that’s not possible, stick to one large table per query and use projections to make the rest manageable.


Projections, in fact, became one of ClickHouse's biggest advantages. Unlike Snowflake, which limits you to a single clustering key per table, ClickHouse allows multiple projections tuned to different access patterns. “It just feels like magic,” Peter says. “We can optimize for syncing and for API performance. We don’t have to compromise anymore.”


There are tradeoffs, of course. Projections don’t support deletes, so they’re best suited for append\-only workloads. But for Chartmetric’s use case—real\-time analytics, observability data, and fast\-growing time series—it’s a trade they’re happy to make.


## Making music data useful, at scale [\#](/blog/chartmetric-uses-clickhouse-to-turn-artist-data-into-music-intelligence#making-music-data-useful-at-scale)


To understand the value Chartmetric delivers, just think of an artist like Taylor Swift. Her catalog spans decades, genres, and audiences. A single track might appear on millions of playlists around the world, each with different curators, update cycles, and ranking logic. Tracking that kind of activity over time—across platforms, formats, and regions—is exactly the sort of data challenge Chartmetric was built to solve.


With ClickHouse, what started as a way to speed up time\-series queries quickly became much more than that. It gave Chartmetric the performance they needed to handle massive datasets, run complex queries faster, and scale without taking on more operational complexity. From streaming counts to observability pipelines to multi\-billion\-row caches like the artist\-playlist table, ClickHouse Cloud helps the team do more with less.


“ClickHouse has been excellent, delightful, wonderful—I can't think of enough words to describe how nice it is for time series data and especially reducing storage costs and improving API performance, which is exactly what we thought it would do,” Peter says.


To see how ClickHouse can speed up your data operations and scale with you, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
