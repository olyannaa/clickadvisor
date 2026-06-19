# How Respan is scaling LLM observability with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Respan is scaling LLM observability with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Apr 6, 2026 · 8 minutes read## Summary

- Respan uses ClickHouse Cloud to power high\-throughput LLM observability across 50 million daily events.
- After outgrowing Postgres at 50\-100 writes per second, the team migrated ingestion and analytics to ClickHouse Cloud.
- Incremental materialized views and trace aggregations keep dashboards fast even as datasets scale into the billions of rows.
[Respan](https://www.respan.ai/) (formerly Keywords AI) is building an AI gateway with built\-in observability. Designed for LLM applications running in production, the platform routes requests across models and providers while giving teams visibility into performance, evaluations, and prompt management.


Part of YC’s W24 cohort, the company quickly gained traction with thousands of developers, and traffic grew from a few hundred requests per day to roughly 30 million requests per day, or close to one billion requests per month. Alongside live LLM calls, cached requests also generate observability data, pushing overall event volume even higher.


Today, Respan processes around 50 million events per day. At that scale, activity is constant. "There are thousands of events going through our pipeline as we speak," said co\-founder and CTO Raymond Huang at a [December 2025 meetup in San Francisco](https://clickhouse.com/videos/meetupsf_dec_20251).


At the meetup, Raymond walked through a live demo showing how Respan’s backend evolved from a simple Postgres\-based setup to [ClickHouse Cloud](https://clickhouse.com/cloud), which now powers high\-throughput ingestion, fast analytics, and production\-grade LLM observability.


## From Postgres to ClickHouse [\#](/blog/respan-ai-llm-observability#from-postgres-to-clickhouse)


Respan is a lean team with a true startup mentality. "We move fast and we build fast," Raymond says. Early on, the platform’s backend reflected that scrappy mindset: a Django app backed by Postgres, logging each request as it arrived. "One request comes in, it goes into Postgres, and we store it," Raymond explains. "It’s that simple."


At low volumes, the approach worked. The system handled tens of events per second without trouble, and the mental model was easy to reason about. But as workloads climbed into the 50 to 100 requests per second range, transactions started to contend with one another.


Postgres was behaving exactly as it should, serializing work to preserve correctness, but under steady write pressure, each insert had to complete its transaction and be recorded in the write\-ahead log before subsequent writes could proceed. As Raymond puts it, “Things start to pile up, and from there they escalate quickly.”


There was a clear mismatch between Postgres’s transactional model and the demands of real\-time observability at scale. Squeezing more out of their current setup wasn’t an option, so the team decided to look for a better solution. They found it in ClickHouse Cloud.


"We decided to move to ClickHouse," Raymond says. "That helped significantly. We can now easily handle the scale that we couldn’t before."


## Designing logs for sustained ingestion [\#](/blog/respan-ai-llm-observability#designing-logs-for-sustained-ingestion)


As they began migrating to ClickHouse, the team focused on getting the schema right. They knew it could handle the write volume, but only if the data model supported it.


Logs were designed to be compact and structured, storing only the fields that would actually be queried or aggregated. Metrics and metadata—latency, throughput, routing time, cost—are written as typed columns optimized for analytical workloads.


Larger text fields, like prompt inputs and model outputs, are deliberately truncated before ingestion. The goal isn’t to capture full transcripts, but to preserve enough context for debugging and analysis without letting row size grow unchecked.


"We don’t store big data in ClickHouse because memory efficiency is important," Raymond says. "We store minimal information so we can keep each message small and the ingestion rate as high as possible."

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-329-get-started-today-sign-up&utm_blogctaid=329)## Building fast analytics with materialized views [\#](/blog/respan-ai-llm-observability#building-fast-analytics-with-materialized-views)


Ingesting data at scale is only useful if the analytics layer can keep up. Respan's customers expect dashboards that load quickly and support common slices of data without delay. To make that happen, the team relies heavily on [incremental materialized views](https://clickhouse.com/docs/materialized-view/incremental-materialized-view).


Raw logs are first aggregated into minute\-level windows, partitioned by organization, then cascaded into hourly rollups. Each materialized view targets a specific dimension—organization and API key, customer identifier, environment, deployment or model—so dashboards query pre\-aggregated data instead of scanning raw logs.


"This way, we don’t have to recompute all the aggregations," Raymond says. "That saves us a lot of query power."


By aggregating early and limiting recomputation, the team keeps query costs predictable and avoids full\-table scans as the dataset grows. “With this breakdown, we can easily grab data and have optimal performance,” Raymond adds.


## Separating real\-time metrics from user metadata [\#](/blog/respan-ai-llm-observability#separating-real-time-metrics-from-user-metadata)


Not every query needs to be real\-time. Some dashboards require sorting and joining against user\-level metadata—customer IDs, names, email addresses—alongside aggregated metrics. Grouping by every metadata column would make queries heavier and more expensive, especially as row counts grow.


Instead, the team uses [refreshable materialized views](https://clickhouse.com/docs/materialized-view/refreshable-materialized-view) for this layer of analytics. These views aggregate the necessary fields and refresh on a fixed cadence—every 10 minutes in Raymond’s demo—rather than updating on every insert.


"The user data doesn’t have to be real\-time," Raymond explains. By separating high\-frequency metrics from slightly delayed metadata, the system avoids wide [GROUP BY](https://clickhouse.com/docs/sql-reference/statements/select/group-by) clauses and keeps joins efficient.


Everything is written into [MergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree) tables, partitioned by time, so queries can filter aggressively before joining. The result is dashboards that remain fast and sortable, even when combining behavioral metrics with user attributes.


## Traces without expensive reconciliation [\#](/blog/respan-ai-llm-observability#traces-without-expensive-reconciliation)


Understanding complex LLM workflows doesn’t end with logs. Respan also supports tracing to show how individual requests move through the system. Each trace is composed of spans, which may arrive out of order in distributed environments.


Rather than enforcing strict ingestion order, the system encodes relationships directly in the data. Spans reference their parents, and those relationships are resolved analytically at query time. "Everything can be asynchronous as long as eventually they meet each other in the database," Raymond says. By avoiding coordination at write time, the pipeline remains fully asynchronous.


When building trace aggregations, the team is equally deliberate. They avoid using the [FINAL](https://clickhouse.com/docs/sql-reference/statements/select/from#final-modifier) modifier, which can force ClickHouse to recompute and merge large portions of a table at query time. Instead, trace metrics such as span counts, token usage, cost, and error rates are computed using aggregate functions. Functions like [argMax](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/argmax) allow the system to select the latest point\-in\-time values without triggering expensive full\-table processing. The result is trace analytics that remain predictable and memory\-efficient as span volume grows.


## A system that’s easier to operate at scale [\#](/blog/respan-ai-llm-observability#a-system-thats-easier-to-operate-at-scale)


As Respan’s system scaled, operational simplicity became increasingly important. One of ClickHouse’s biggest strengths, Raymond says, is the simplicity of its [indexing model](https://clickhouse.com/docs/guides/best-practices/sparse-primary-indexes), which reduces what engineers have to manage day to day.


"This enables me to sort really quickly without having to worry about index\-tree structure," he says. "I only have to worry about if the partition is right and whether the querying data fits into the memory. If it doesn’t, I just scale the instance—it’s that simple."


That predictability extends to everyday workflows like log search. Even without relying on advanced full\-text search features, straightforward string queries can scan tens of millions of rows in sub\-second time. As Raymond says, "That’s pretty impressive."


Today, ClickHouse underpins Respan’s observability stack from ingestion through customer\-facing analytics. Most importantly, it provides a solid foundation that scales with the product, without forcing constant architectural revisions as usage grows.


"Big shoutout to the ClickHouse team," Raymond says. "We built one of the best products in the LLM observability space—this wouldn’t have been possible without ClickHouse’s support."

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
