# How Pump uses ClickHouse Cloud to bring cloud costs into focus


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Pump uses ClickHouse Cloud to bring cloud costs into focus

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Dec 2, 2025 · 9 minutes read
div.w\-full \+ p, 
pre \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

Two years ago, *Forbes* called [Pump](http://pump.co) the [“Costco of cloud.”](https://www.forbes.com/sites/davidprosser/2023/10/05/how-pump-promises-to-slash-your-runaway-cloud-computing-costs/) It’s a pretty good analogy: just like Costco buys in bulk to pass discounts on to its members, Pump aggregates cloud usage across its customers to negotiate cheaper commitments from providers like AWS. The platform analyzes past consumption patterns, buys reserved instances and savings plans on behalf of users, and then spreads the savings across the group.


But cost savings only go so far without visibility. A FinOps analyst or engineer might still find themselves staring at AWS Cost Explorer, wondering why a bill suddenly jumped 20 percent or which team spun up a cluster without tagging it properly. “Cost Explorer is good, but it’s not great,” says Joel Walker, founding software engineer at Pump. “It doesn’t give you high\-granularity insight into where your costs are breaking down.”


That gap inspired the team to build Pump View, a cost visibility hub launched earlier this year. It lets teams slice and dice their cloud bills by region, usage type, team, or even custom tags. On the surface, it looks like a simple dashboard. But under the hood, the system is crunching billions of billing records daily, unifying formats from multiple providers, and keeping everything consistent. “All this is driven by ClickHouse,” Joel says.


At an [August 2025 ClickHouse meetup in San Francisco](https://clickhouse.com/jp/videos/meetupsf_august_2025_1), Joel walked through the team’s decision to build Pump View on [ClickHouse Cloud](https://clickhouse.com/cloud), how the architecture works, and the technical challenges they solved along the way.


## Pump’s ClickHouse\-based architecture [\#](/blog/pump#pumps-clickhouse-based-architecture)


When Pump started work on Pump View, the “logical” choice was to build it around Postgres. The company already uses the database extensively, and Joel and the team knew its strengths well. But the scale of the project made that option unrealistic. “We ingest billions of records every day,” he says. “That’s something that Postgres would have a hard time doing.”


As Joel explains, Postgres is “optimized for transactional data—it gives you a consistent view of your data at any point in time.” ClickHouse, by contrast, excels at bulk inserts and analytical queries. One of its biggest advantages is decoupling reads from writes. “When you insert data, it shouldn’t slow down your queries, and when you’re querying, it shouldn’t slow down your inserts,” Joel says. “Also, ClickHouse just scales much better.”


![Pump User Story Issue 1206 (1).jpg](/uploads/Pump_User_Story_Issue_1206_1_0923558cde.jpg)
Pump View’s architecture, with cloud exports from AWS and GCP flowing into ClickHouse.


Pump’s pipeline starts where the cloud providers leave off. AWS publishes detailed cost and usage data every eight hours, dropping it into S3 as Parquet files. Pump kicks off a job whenever those exports land, transforming the data and inserting it into ClickHouse via the [s3 table function](https://clickhouse.com/docs/sql-reference/table-functions/s3). Google Cloud data follows a similar path, and Azure will soon join.


The query pattern is exactly what ClickHouse was built for: sum costs from a massive table, filter by company ID and date range, apply filters for region, service, or usage type, and group results. A customer can drill into spend in us\-west\-2, break it down by EC2 versus S3, and zoom in on a single tagged load balancer.


While ClickHouse handles ingest and query at scale, Postgres still plays an important supporting role. Pump uses it to track which versions of the data are “live,” ensuring customers always see a consistent view even when cloud providers republish billing exports. “It lets us present a unified view of the data, even if we’re in the middle of inserting data or cleaning up older data,” Joel says.


## Solving challenges along the way [\#](/blog/pump#solving-challenges-along-the-way)


Pump’s architecture might look simple on the surface, but making it work at scale meant tackling four big challenges: semi\-sparse records, ingestion volume, atomic updates, and interval queries.


### Challenge \#1: Semi\-sparse records [\#](/blog/pump#challenge-1-semi-sparse-records)


Cloud billing exports are messy. Every line item can have a different set of fields, and user tags are arbitrary key\-value pairs. “AWS is going to have very different fields than GCP,” Joel notes. AWS might tag an EC2 instance with “team\=backend” while GCP adds something totally different. Trying to map that into a rigid schema is painful.


ClickHouse does offer a [Map(K, V)](https://clickhouse.com/docs/sql-reference/data-types/map) type, which can store tags as key\-value blobs. But queries would have to scan the entire map column every time, slowing down performance.


Joel and the team came up with a clever workaround: hash the keys and distribute them across eight string columns, with a matching set of float columns for numeric values. A simple, fast hash function, implemented in both Python and ClickHouse, tells them exactly which column to check for a given key. That cut the I/O footprint by roughly 8x.


It works well—although Joel admits that if they were starting today, they’d probably just use [ClickHouse’s JSON data type](https://clickhouse.com/docs/sql-reference/data-types/newjson), launched shortly after they built the system. “JSON really is the answer here, especially for our use case,” he says, “because a lot of the fields are the same, and so they fit nicely into their own columns.”


### Challenge \#2: Ingestion volume [\#](/blog/pump#challenge-2-ingestion-volume)


The ingestion scale is huge: about 5 billion records a day, or roughly 5 TB of uncompressed data. Each record averages around 990 bytes, and there are about 600 ingestion events every day. Even at that size, Joel says, “This is actually very straightforward with ClickHouse.” Using the [s3 table function](https://clickhouse.com/docs/sql-reference/table-functions/s3), Pump can stream Parquet files straight into their tables with just a bit of transformation.


“ClickHouse is very fast,” Joel says. Each ingestion takes around 40 seconds, and the primary cost table already holds more than 55 billion rows. “It’s not Cloudflare scale,” he jokes, nodding to Jamie Herre’s presentation earlier in the evening, “but it’s something.”


### Challenge \#3: Atomic updates [\#](/blog/pump#challenge-3-atomic-updates)


Cloud billing isn’t static. Every month, AWS republishes cost exports, sometimes adding or deleting records compared to the previous version. “This presents a problem, because how do you ingest this?” Joel asks. Insert before delete, and totals look too high. Delete before insert, and they look too low.


ClickHouse offers features like [ReplacingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree) and [table partitions](https://clickhouse.com/docs/partitions), but neither fit this specific use case. ReplacingMergeTree is built for individual rows, not entire batches. Partitions support atomic swaps, but Pump already had over 5,000 of them—“and that number is only going to grow as we add more customers," Joel says.


Their solution was to rely on Postgres. Pump stores “live” mutation IDs in Postgres, then filters ClickHouse queries based on those IDs. Postgres ensures transactional consistency, while ClickHouse does the heavy lifting of scanning and aggregating. Together, they keep the numbers coherent.


### Challenge \#4: Interval queries [\#](/blog/pump#challenge-4-interval-queries)


The biggest challenge came from the shape of the data itself. “Interval queries are hard,” Joel says. Some billing records represent a one\-hour usage charge. Others cover a three\-year savings plan. To answer a query for a given date range, you need to check both start and end fields. That makes it tough to optimize storage and ordering. As Joel puts it, “It’s a little weird.”


The fix was to normalize records during ingestion. Long records get split into daily slices, while hourly records are rolled up into daily totals. That way, every record in the aggregated table represents exactly one day. Queries no longer need to reason about overlapping intervals. They just filter by record begin date, which is also the column used in the [ORDER BY](https://clickhouse.com/docs/sql-reference/statements/select/order-by). “It cuts down on the data that has to be searched,” Joel says. “And it gives us consistent intervals so our queries can only look at the begin date of the records.”


## What’s next for Pump and ClickHouse [\#](/blog/pump#whats-next-for-pump-and-clickhouse)


Despite all the progress so far, Joel says, “There’s more work to do.” One priority is expanding Pump View beyond AWS and GCP, adding Azure as the next cost data provider.


They also want to shift more functionality into ClickHouse itself. Today, features like text search and autocompletion still live in Postgres. For example, if a user starts typing “us w…”, Postgres suggests the us\-west\-2 region filter. “We want to move that into ClickHouse,” Joel says. “It’s one of our biggest Postgres tables, and ClickHouse will be quite a bit faster.”


Another area they’re rethinking is how aggregations run. Right now, the jobs behave more like “gather” operations, scanning months or even years of raw records to produce daily slices. A scatter\-based approach would flip that model, slicing the data as it comes in and cutting down on heavy backfills later.


Six months after launch, Pump View is already ingesting billions of records a day and powering dashboards for customers across multiple providers. For those teams, visibility is the missing piece that makes their savings real. And with ClickHouse under the hood, Pump has the scale and speed to keep building on that foundation.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-19-get-started-today-sign-up&utm_blogctaid=19)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
