# How FabFunnel powers real\-time marketing analytics with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How FabFunnel powers real\-time marketing analytics with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2FUser_Story_Idea_Clan_Issue_1204_f842b8922b.jpg&w=96&q=75)![](/_next/image?url=%2Fuploads%2FUser_Story_Idea_Clan_Issue_1204_1_ee7aa995fc.jpg&w=96&q=75)Anmol Jain, Full Stack Developer SDE 2, \& Siddhant Gaba, Python Developer SDE 2, at Idea ClanNov 20, 2025 · 7 minutes readWhat if affiliate marketers could spin up fresh creative on demand, launch hundreds of campaigns in minutes, and automate scaling rules in real time—all from a single dashboard?


That’s the idea behind [FabFunnel](https://fabfunnel.com/), the newest product from [IdeaClan](https://ideaclan.com/), a digital marketing agency. [Launched at Affiliate World Budapest](https://ideaclan.com/fabfunnel-launches-at-affiliate-world-budapest-2025-ideaclan-highlights/) in September 2025, the platform brings campaign launches, reporting, automation, and creative workflows together in one place, with built\-in integrations for Facebook, TikTok, Newsbreak, Google and other ad platforms.


To make that happen, FabFunnel has to continuously stream in spend and revenue data from multiple networks and serve it back to users in real time. That means handling millions of campaign updates, syncing ad spend within minutes, and powering dashboards that need to stay responsive even over long reporting windows. For media buyers managing millions of dollars in quarterly spend, speed and reliability are non\-negotiable.


At a [ClickHouse meetup in Delhi](https://clickhouse.com/videos/gurgaon-meetup-fabfunnel-and-clickhouse-delivering-real-time-marketing-analytics) earlier this year, Idea Clan engineers [Anmol Jain](https://www.linkedin.com/in/anmoljain987) and [Sidhant Gaba](https://www.linkedin.com/in/siddhant-gaba-37a228191/) explained why FabFunnel’s old MySQL\-based reporting architecture couldn’t keep up, and how moving to [ClickHouse Cloud](https://clickhouse.com/cloud) gave them the speed and efficiency they needed to deliver real\-time marketing analytics.



## Hitting the limits of MySQL [\#](/blog/fabfunnel-real-time-marketing-analytics#hitting-the-limits-of-mysql)


Before the migration, FabFunnel’s reporting stack ran entirely on MySQL. Data from Meta, TikTok, Newsbreak, Google and other traffic sources landed in separate tables every 20 to 30 minutes. To keep reports current, the system relied on a clunky cycle of deleting and reinserting rows every 15 to 30 minutes. This worked for small queries, but the pipeline hit a wall as soon as users asked for anything beyond a narrow date range.


Because the schema was normalized, queries relied heavily on joins. That meant slow response times, high CPU usage, and frustration for users running large reports. “When a user queried the last month of data, it would take 11 seconds,” Anmol says. “If they asked for a year of data, the browser would crash because all the merging was done on the client side.” For anyone using a low\-end device, things were even worse.


![User Story Idea Clan Issue 1204 (1).png](/uploads/User_Story_Idea_Clan_Issue_1204_1_19bf1a6a2c.png)
FabFunnel’s previous MySQL\-based architecture: slow, fragile, and congested.


The refresh cycle only added to the pain. Marketing data updates constantly—by the second, not the hour—and MySQL wasn’t built for that pace. “It was very difficult to update the data,” Anmol says. Keeping group\-level metrics accurate meant constant row cycling, which created congestion and left dashboards feeling anything but “real time.”


## Seeking a faster, smarter database [\#](/blog/fabfunnel-real-time-marketing-analytics#seeking-a-faster-smarter-database)


The FabFunnel team knew they needed more than a patch. They needed a database that could handle fast, high\-volume inserts and run aggregations across billions of rows without getting bogged down by joins or client\-side merges. Just as important, it had to deliver sub\-second queries so dashboards would feel instant, not delayed.


Migration also had to be realistic for a small engineering team. A database with familiar syntax and minimal operational overhead was essential. “We wanted something faster with real\-time inserts and analytics,” Anmol explains. “And we wanted something easy to migrate.”


[ClickHouse Cloud](https://clickhouse.com/cloud) emerged as the obvious choice. Its [columnar model](https://clickhouse.com/docs/faq/general/columnar-database) was a natural fit for FabFunnel’s denormalized data, and [SQL compatibility](https://clickhouse.com/docs/sql-reference) made migration and onboarding straightforward. The managed service solved another looming problem: infrastructure. Instead of scaling MySQL servers or wrestling with self\-hosted clusters, the team could rely on ClickHouse Cloud to handle ingestion, storage, and performance tuning at scale.


For a marketing platform defined by speed, FabFunnel’s database decision was as much about efficiency as raw power—and ClickHouse Cloud delivered both.


## Rebuilding with ClickHouse Cloud [\#](/blog/fabfunnel-real-time-marketing-analytics#rebuilding-with-clickhouse-cloud)


Once the decision was made, the first step was rethinking ingestion. In the new setup, spend\-side and revenue\-side data flows continuously through Confluent Kafka into ClickHouse using [ClickPipes](https://clickhouse.com/cloud/clickpipes), the cloud\-native integration engine that makes it easy to ingest massive volumes of data from different sources. Together, Kafka and ClickPipes keep a steady stream of real\-time data coming in from ad platforms and vendors.


![User Story Idea Clan Issue 1204 (2).png](/uploads/User_Story_Idea_Clan_Issue_1204_2_1ee6a96360.png)
FabFunnel’s new ​​ClickHouse\-based architecture: fast, scalable, and reliable.


On the storage side, the team replaced their fragile delete\-and\-insert cycles with [ReplacingMergeTree tables](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree), which automatically keep the freshest record for each key. That change alone cut down on congestion and made it possible to handle updates in real time without slowing down the system.


Next came query speed. To avoid the browser\-side merges and joins that plagued their old setup, the engineers turned to [refreshable materialized views](https://clickhouse.com/docs/materialized-view/refreshable-materialized-view). These pre\-aggregate data into a single reporting table, so user queries no longer have to piece together results on the fly. “We don’t want to merge data after every insert,” Sidhant says—and now they don’t have to.


The new design also introduced a [buffer table](https://clickhouse.com/docs/engines/table-engines/special/buffer) for real\-time click data. This means less dependency on other services and faster syncing with ClickHouse. Spend and revenue data are placed into separate databases for efficiency, then merged downstream to give users a consolidated view without sacrificing performance.


All of these changes combined to turn FabFunnel’s pipeline into a system built for real\-time scale. The architecture ingests continuously, handles heavy concurrent query loads, and delivers sub\-second responses, all while keeping infrastructure overhead low.


## Real\-time at massive scale [\#](/blog/fabfunnel-real-time-marketing-analytics#real-time-at-massive-scale)


The payoff from the migration has been huge. With data pre\-aggregated in ClickHouse Cloud and stored in a single reporting table, queries that once took seconds—or crashed the browser altogether—now return in under a second. “Our query efficiency has improved significantly since moving to ClickHouse,” Sidhant says. “We can now show our clients [real\-time analytics](https://clickhouse.com/resources/engineering/what-is-real-time-analytics).”


The metrics tell the story. In one month, FabFunnel’s system processed 19\.2 million queries, read 11\.67 trillion rows totaling 606 TB of data, and wrote 5\.15 billion rows while consuming just 1\.32 TB of storage. On average, the team now processes 111 million rows in 1\.1 seconds, with queries scanning 1\.7 to 2\.1 GB of data still completing in under a second.


ClickHouse Cloud has also given the team headroom to handle large volumes of concurrent queries—important for a multi\-tenant platform serving affiliates and agencies. And because the managed service scales predictably, FabFunnel can keep growing without worrying about ballooning infrastructure costs.


For users, the benefits are obvious: instant reporting, ad spend synced in minutes, and automation rules that run on fresh data. For Idea Clan’s engineers, it means less time fighting infrastructure and more time building features for affiliates and media buyers.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-11-get-started-today-sign-up&utm_blogctaid=11)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
