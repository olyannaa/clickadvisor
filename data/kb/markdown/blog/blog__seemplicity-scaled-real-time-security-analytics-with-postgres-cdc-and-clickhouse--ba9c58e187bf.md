# How Seemplicity scaled real\-time security analytics with Postgres CDC and ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Seemplicity scaled real\-time security analytics with Postgres CDC and ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 29, 2025 · 8 minutes readToday’s security teams face a paradox: more tools, more data, and yet less clarity. With dozens of scanners, posture managers, and alerting systems in play, the average enterprise team spends more time triaging findings than actually fixing them.


[Seemplicity](https://seemplicity.io/) solves this by acting as the nerve center for remediation. As the industry’s leading RemOps platform, it aggregates findings from over 150 tools—spanning application security, cloud security, vulnerability management, pen testing, and more—and enriches them with internal business context and threat intelligence to help teams take action faster.


“Instead of getting alerts and vulnerabilities from different tools and manually tracking them in spreadsheets or emails, Seemplicity ingests all security findings into a centralized transactional system and then leverages Postgres CDC to seamlessly replicate data into ClickHouse for high\-performance analytics,” says Chief Architect Tal Shargal. “This allows us to quickly prioritize vulnerabilities and automatically generate actionable tasks for the right teams. You can think of it as a smart security workflow platform powered by rapid analytics.”


But scaling always brings challenges. As Seemplicity grew and onboarded larger customers, the limits of its architecture became clear. Postgres couldn’t keep up with the volume of incoming data or the performance demands of their customer\-facing dashboards. The team needed a new foundation—something fast, reliable, and made for real\-time analytics at scale.


We caught up with Tal to hear how Seemplicity rebuilt its backend with [ClickHouse Cloud](https://clickhouse.com/cloud) and PeerDB (now part of [ClickPipes](https://clickhouse.com/cloud/clickpipes)), why visibility matters just as much as speed, and how moving to a modern data stack helped the team grow without losing control.


## Hitting the Postgres bottleneck (and why CDC matters) [\#](/blog/seemplicity-scaled-real-time-security-analytics-with-postgres-cdc-and-clickhouse#hitting-the-postgres-bottleneck-and-why-cdc-matters)


In the beginning, Seemplicity ran entirely on Postgres. The OLTP database handled everything from ingestion to enrichment to dashboard queries, serving as both the operational and analytical backbone of the platform. For a while, it worked. But as the company matured and began working with large customers at higher data volumes, performance began to slip.


“As more customers were onboarded, including very large Fortune 500 companies, we needed to scale up significantly,” Tal says. “We started to think about how to make this pipeline architecture more modern and to make it work on these volumes.”


They were already pushing Postgres hard. “We were doing a lot of upserts and aggregations in Postgres,” Tal explains. “Bloating became an issue. It soon became a real bottleneck: frequent upserts, bloating tables, and ever\-longer dashboard queries.”


Much of the platform’s logic relied on joins across multiple tables that shared a common finding ID. Each tenant had around 16 related tables, cloned per customer—meaning that as Seemplicity scaled to dozens of tenants, the number of tables and joins multiplied quickly. Postgres could support that pattern to a point, but it became increasingly fragile as the number of findings surged, especially with large tenants contributing tens or even hundreds of millions of entities. Frequent updates and long\-running transactions only added to the strain.


“Every day, we were pulling in more data, more updates, more changes,” Tal explains. “At that point the team realized a dedicated CDC pipeline was no longer optional—it was mandatory.”


## Rebuilding around ClickHouse and ClickPipes [\#](/blog/seemplicity-scaled-real-time-security-analytics-with-postgres-cdc-and-clickhouse#rebuilding-around-clickhouse-and-clickpipes)



> “We wanted to keep Postgres as our transactional layer, but we needed something purpose\-built for analytics"


To ease the pressure, the team began rethinking their architecture, starting with how to decouple analytical workloads. “We wanted to keep Postgres as our transactional layer, but we needed something purpose\-built for analytics,” Tal says.


Choosing ClickHouse was fairly straightforward. The team needed sub\-second query performance across billions of rows. After testing it against multiple other solutions, they were confident that ClickHouse, a columnar OLAP database known for its blazing\-fast speed, would deliver.


The hardest (and most critical) problem was moving every Postgres insert, update, and delete into ClickHouse reliably. At first, the team experimented with Debezium, but they wanted to avoid the operational burden and the complexity of a multi\-step pipeline — source connector, Kafka, and target connector — which involved multiple points of failure. Instead, they turned to PeerDB, an open\-source, Postgres\-native CDC solution that was [acquired by ClickHouse in July 2024](https://clickhouse.com/blog/clickhouse-acquires-peerdb-to-boost-real-time-analytics-with-postgres-cdc-integration) and is now part of [ClickPipes](https://clickhouse.com/cloud/clickpipes). It gave them the performance, reliability, and observability they needed, without the headache of managing their own pipelines.


“I’m a fan of managed products,” Tal says. “I knew a managed product built by engineers, whose goal in life is to transform bits from Postgres into ClickHouse, would be better than anything we could do ourselves. I’m 100% sure that if we had tried to implement it on our own, the risk would've been higher, and it would have taken a lot more time to get right.”


![diagram tenants schemas.png](/uploads/diagram_tenants_schemas_756138ffdf.png)
Seemplicity’s current setup includes a multi\-region architecture with several Postgres instances streaming data into ClickHouse through PeerDB. In each region, data first lands in a shared staging database, then gets routed to tenant\-specific databases for isolation and consistency. Every customer has a dedicated schema, making it easier for the frontend to interact with ClickHouse the same way it did with Postgres.


To simplify analytics, Seemplicity uses [materialized views](https://clickhouse.com/docs/materialized-views) and [AggregatingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/aggregatingmergetree) tables. Many of their original Postgres tables (often joined by a shared finding ID) have been consolidated into denormalized tables in ClickHouse, eliminating the need for complex joins at query time. “This helps a lot,” Tal says, “and is another thing we couldn’t have achieved in Postgres.”



> “I knew a managed product built by engineers, whose goal in life is to transform bits from Postgres into ClickHouse, would be better than anything we could do ourselves. I’m 100% sure that if we had tried to implement it on our own, the risk would've been higher, and it would have taken a lot more time to get right.”


## Speed, scale, and peace of mind [\#](/blog/seemplicity-scaled-real-time-security-analytics-with-postgres-cdc-and-clickhouse#speed-scale-and-peace-of-mind)


The migration to ClickHouse has delivered big\-time performance gains. Dashboards and widgets that once took minutes or even timed out in Postgres now return results in “seconds or milliseconds,” Tal says. That responsiveness means Seemplicity can deliver a consistent experience across all tenants, no matter the data volume.


“More importantly,” he adds, “in ClickHouse, it's really easy for me to know what's going on under the hood.” ClickHouse’s transparency—showing how many rows are scanned, how data is pruned, and which parts are being read—makes it easier to optimize queries and direct engineering effort. “It reflects how energy is spent,” Tal says. “Our North Star is to make everything as lean as possible.”


Compression has also been a major win. Seemplicity’s ClickHouse footprint sits at around 10 terabytes—a fraction of their Postgres instance. “I’d guess Postgres is 5 to 6 times bigger,” Tal notes. That space efficiency, plus the ability to stream tens of billions of updates per month, gives them room to grow without worrying about bloat or system strain.


But perhaps the biggest benefit is peace of mind. The combination of ClickHouse and ClickPipes has given the team confidence that their analytics stack won’t break under pressure or demand constant attention. “We can trust it,” Tal says.


## Engineering with confidence [\#](/blog/seemplicity-scaled-real-time-security-analytics-with-postgres-cdc-and-clickhouse#engineering-with-confidence)


Looking ahead, Seemplicity plans to shift even more of its data processing into ClickHouse. Today, most of the platform’s logic still runs in Postgres, but Tal sees an opportunity to simplify. “If we can migrate and implement more features in ClickHouse instead of Postgres, it could save us a lot of complexity and help us resolve bugs,” he says.


That kind of evolution requires a deep understanding of how everything fits together. It’s something Tal cares about deeply, and something he’s worked to instill across the team. “I believe in really knowing the architecture I’m working with,” he says. “I don’t like to take things as obvious and just close my eyes and hope it works. I want to understand what’s happening under the hood. That’s one of my internal truths.”


Ultimately, the goal is to keep improving precision and control. “We need to know that every bit is transferred from Postgres to ClickHouse,” Tal says. With a faster, more scalable analytics engine in place, that vision is looking clearer than ever.



> To try ClickHouse and see how it can improve the speed and scalability of your team’s data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
