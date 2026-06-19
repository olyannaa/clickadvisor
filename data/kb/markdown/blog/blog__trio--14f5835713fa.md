# “A generational leap”: How Trio unified payment analytics and cut storage by 88% with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# “A generational leap”: How Trio unified payment analytics and cut storage by 88% with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Apr 17, 2026 · 9 minutes read## Summary

Trio uses ClickHouse as a single source of truth for payment analytics, supporting reconciliation, compliance reporting, and operational and customer dashboards. At 243M\+ payments in H1 2025 and 1B\+ events daily, ClickHouse delivered "generational" speed with minimal tuning and cut storage by 88%. They use a sliding window approach with refreshable materialized views and ReplacingMergeTree to handle late, duplicate, and out\-of\-order events.

[Trio](https://www.trio.com.br/en) is a Brazilian fintech that processes high\-volume electronic payments. As the business scaled and expanded its portfolio with the 2025 acquisition of PayBrokers, a leading payment processor in the gaming and lottery sector, it had to turn a fast\-moving stream of payment activity into data teams could rely on across operations and finance.


In the first half of 2025 alone, Trio processed over 243 million payments, with each payment generating hundreds of downstream signals, including logs and system events. At that volume, analytics becomes part of the payment machine itself—how teams monitor performance, reconcile transactions, and produce financial views they can stand behind.


At a [November 2025 ClickHouse meetup in São Paulo](https://clickhouse.com/videos/trio-meetup-brazil), Trio team members Fabricio Epaminondas (Head of Engineering), Eurico Nicacio (Head of CloudOps and IT), and Filipe Coelho (Data Specialist) walked through how they’re scaling analytics on [ClickHouse Cloud](https://clickhouse.com/cloud), why they made specific ingestion choices, and what they’ve learned along the way.



## The need for a single source of truth [\#](/blog/trio#the-need-for-a-single-source-of-truth)


In payments, “analytics” means something different than it does in most other businesses. In SaaS, being a few events off on traffic or error rates is tolerable—you still get value from the chart. Finance doesn’t work that way. “You can’t tell the client he has R$101\.95 if he has R$101\.94,” Fabricio says.


That’s because the outputs aren’t just internal dashboards. “How we use the data, reconcile it, how we prepare the financial and accounting summaries—all of that has legal implications,” Fabricio says. “There’s compliance involved, federal laws, anti\-money laundering policies, a series of regulatory mechanisms that need to be well\-organized.”


In other words, the numbers have to be fast, but they also have to be explainable—traceable back to their source, consistent across teams and systems.


As Trio grew, meeting that standard became harder. Filipe explains that the company wasn’t working from a single database or a single source of truth. “We had a situation where we needed to bring disparate systems—both deactivated legacy systems and legacy systems that were still active—into a single point of view,” he says. “At the same time, we had to generate analytical data and historical series from a huge volume of financial transactions, and the systems where those transactions lived weren’t designed for that kind of workload.”


Trio needed an analytical foundation that could unify those sources, keep up with the firehose of events, and still produce outputs the business could stake its reporting on. “We found a solution in [ClickHouse](https://clickhouse.com/cloud) to solve this problem,” Filipe says.


## Trio’s ClickHouse\-based architecture [\#](/blog/trio#trios-clickhouse-based-architecture)


Trio uses ClickHouse across a range of functions, from internal operations and reporting to financial reconciliation, compliance, and customer\-facing analytics.


On the operations side, the team pipes telemetry into ClickHouse and uses Grafana to monitor platform activity in real time. Eurico notes that when Trio first started, newer ClickHouse observability features like [ClickStack](https://clickhouse.com/clickstack) didn’t exist yet, so they built their own pattern around tools they already trusted. “Grafana is a great friend of ours,” he says.


Cloud applications—mainly Elixir, with additional services in TypeScript—run on AWS and interact with several transactional and operational data sources, including Tiger Data, Postgres, MongoDB, and Amazon S3\. From there, data moves along two main paths: streaming through Redpanda for messaging\-driven events, and batch through Airflow for scheduled loads. ClickHouse sits in the middle as the analytical layer, feeding Grafana, Hex, and Trio’s own applications, with views consumed by FinOps and DevOps teams, as well as customers.


![Trio’s ClickHouse-based architecture for streaming, batch ingestion, and analytics tools](/uploads/Trio_User_Story_Issue_1256_0_24fc643f0a.jpg)
When it came to ingestion, the team had to decide between [ClickPipes](https://clickhouse.com/cloud/clickpipes), ClickHouse’s native ingestion service, and a custom ETL approach. While Fabricio notes that “ClickPipes makes things much easier,” especially when you want to stand up ingestion quickly and let ClickHouse handle more of the shaping downstream, Trio opted for a custom solution, with Redpanda topics feeding a dedicated ETL service that pre\-processes events, structures the payloads, and then inserts clean, typed records into ClickHouse.


The reason came down to operability under change. With schema drift, evolving event formats, and dependencies between events, Trio wanted more control over how data gets shaped before it lands, without needing to pause and recover a pipeline mid\-stream. “There’s no better or worse here,” Fabricio says. “ClickHouse is very good in either case.”


## The sliding window solution [\#](/blog/trio#the-sliding-window-solution)


Financial systems have a way of making clean diagrams complicated. Payment events arrive late. Some arrive twice. Others show up out of order because a downstream system retried delivery, or because an upstream incident left gaps that get filled in afterward.


Trio ran into this when building [real\-time metrics](https://clickhouse.com/resources/engineering/what-is-real-time-analytics) on top of their messaging flows. A Pix payment might “complete” after its first event was recorded, or a confirmation could arrive seconds or even minutes after an earlier record had been counted. Treat the first event as final and your totals swing retroactively—annoying\-but\-tolerable in software, a non\-starter in finance.


The team’s first instinct was to use [refreshable materialized views](https://clickhouse.com/docs/materialized-view/refreshable-materialized-view) to re\-run aggregations as new events arrived. The problem was, if you recompute the entire view every time late data shows up, you’re doing a lot of expensive work for small corrections. “Raw refreshable views will rematerialize everything,” Fabricio says. “That’s very heavy.”


So Trio kept the idea but narrowed the scope. Instead of keeping the full dataset perfectly current on every refresh, they focused on correcting the recent past. The pattern is what’s known as a sliding window: every few minutes, they recalculate a recent time range (e.g. “last four hours, every five minutes”) so late events and duplicates get folded into the right totals without forcing a rebuild of history.


![A sliding window keeps recent metrics correct while older time buckets become immutable](/uploads/Trio_User_Story_Issue_1256_1_928ec0cb80.jpg)
Refreshable materialized views drive those periodic recomputations, and [ReplacingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree) handles deduplication when replays cause the same logical record to be inserted more than once. They also paid close attention to [partitioning](https://clickhouse.com/docs/partitions) to avoid expensive global merges.


The result is a system that behaves the way finance needs it to. Recent data stays correct even when the stream arrives late or repeats itself. Older buckets become effectively immutable once they’ve stabilized. Reporting stays free of gaps or inconsistencies, and performance holds up as the dataset grows. “With this, we can work with over 1 billion data points smoothly within the day, from ledgers, and keep them renewed without major problems,” Fabricio says.


## “A generational leap” [\#](/blog/trio#a-generational-leap)


For Trio, the benefits of ClickHouse showed up in a few ways at once.


One was simply consolidation. Rather than maintaining separate analytical islands tied to individual systems, they centralized the analytical layer. “All the sources are brought into one place,” Filipe explains. “You manage everything within the cloud itself. It becomes the single source of truth for all analytical issues of the company.”


Storage also dropped dramatically—around 88% compared to their previous setup, thanks to ClickHouse’s [columnar storage](https://clickhouse.com/docs/faq/general/columnar-database) and [compression](https://clickhouse.com/docs/data-compression/compression-in-clickhouse).


Then there was speed, which Filipe describes less as an optimization than a true step\-change. “In terms of speed, ClickHouse is truly undisputed,” he says. “It’s a generational leap compared to what we had, even with minimal tuning.”


That speed changed how teams work day to day. Instead of waiting for answers or rationing which queries are “worth” running, analytics became something they could use in tighter feedback loops. “We stopped banging our heads against the wall,” Filipe says, “and started spending more time actually analyzing the data.”


It also made migrations less painful. “Something that would normally take eight hours of head\-scratching to organize a schema, the ClickHouse ingestion process solves in minutes,” Filipe says. Even when Trio migrated roughly 5 billion rows—some tables with more than 70 columns—ClickHouse didn’t flinch. “It received the data and basically didn’t even complain,” he says. “This was a big problem for us every time we had to work with those older databases. It was and is a life\-changing experience.”


## What’s next for Trio and ClickHouse [\#](/blog/trio#whats-next-for-trio-and-clickhouse)


What the team described in São Paulo is phase one: get high\-stakes financial analytics onto an architecture that can unify disparate sources, ingest at streaming scale, and stay correct even when events arrive late or out of order.


Now the focus shifts from making it work to making it cleaner—filling in missing layers, tightening orchestration, and taking advantage of features and improvements ClickHouse has added since Trio first started. That includes revisiting [ClickPipes](https://clickhouse.com/cloud/clickpipes) and newer telemetry\-focused capabilities. The team is also experimenting with local\-mode workflows to rehearse ingestion and operational procedures outside production before applying them in the cloud.


The goal, as volume grows and the platform expands, is an analytical foundation that’s easier to run, easier to change, and easier to trust.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-397-get-started-today-sign-up&utm_blogctaid=397)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
