# What Replo learned optimizing 100\+ billion events in ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# What Replo learned optimizing 100\+ billion events in ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Mar 9, 2026 · 10 minutes read## Summary


div.w\-full \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

Replo uses ClickHouse to power real\-time, in\-product analytics for Shopify merchants running live pages, offers, and A/B tests. The team iterated through multiple data models, learning how precomputation, deduplication, and recomputation boundaries affect real\-time analytics at scale. Today, ClickHouse supports ingestion of 3,000\-5,000 events per second and analysis of 100\+ billion events while keeping dashboards fast and responsive.

Last September, [Replo](https://www.replo.app/) engineer Ryan Voris attended a ClickHouse meetup in San Francisco. Like most meetups, it featured happy customers talking about how they used ClickHouse to scale their data operations. But for Ryan, it left a little something to be desired.


"Everybody was talking about how great ClickHouse is and showing us all their amazing use cases," he says. "But nobody really showed anything like, 'Here's how I messed it up' or 'Here's what I did wrong' or 'Don't do this, it's not a good idea.'"


So when Ryan took the stage at [our last San Francisco meetup](https://clickhouse.com/videos/meetupsf_dec_20254), he decided to do something different. Instead of a neatly packaged case study, he told the true story of how Replo, an AI\-powered page builder trusted by more than 4,000 Shopify merchants, built its [analytics product](https://www.replo.app/product/analytics-and-insights) on ClickHouse, complete with missteps, migrations, and architectural resets.



The result is a system capable of processing and analyzing more than 100 billion events, while keeping dashboards fast, attribution accurate, and analytics usable for online retailers.


## Real\-time analytics for live campaigns [\#](/blog/replo#real-time-analytics-for-live-campaigns)


[Replo Analytics](https://www.replo.app/product/analytics-and-insights) sits directly inside the product. Customers use it to track sessions, purchases, conversion rates, average order value, and A/B test performance across campaigns. When a brand launches a new page or ad, they expect to see [real\-time analytics](https://clickhouse.com/resources/engineering/what-is-real-time-analytics) immediately, not hours later.


Behind the scenes, that translates into a steady stream of frontend events flowing into ClickHouse at anywhere from 3,000 to 5,000 events per second. "We're tracking things like clicks, page views, and purchases," Ryan explains. "Whenever there's a purchase on a page, we record that event and the purchase amount, and we use that to calculate information like average order value, revenue per session, and conversation rates."


Replo's traffic patterns follow predictable rhythms, peaking during the North American workday and tapering off overnight. Expectations, however, never change. Dashboards need to stay responsive. Attribution needs to be correct. And analytics can't introduce the kind of latency that makes a live campaign feel opaque or unreliable.


From the beginning (even before Ryan joined the company), Replo built this system on ClickHouse. There was never much doubt as to whether ClickHouse could handle the volume. The real question became how to model and compute analytics in a way that stayed fast as Replo Analytics grew, usage scaled, and requirements evolved.


## From one table to precomputation [\#](/blog/replo#from-one-table-to-precomputation)


Replo's first analytics pipeline was simple. All events flowed into a single table, and every dashboard query recomputed metrics on the fly.


This worked for a few months, but as usage grew, problems started to appear. Every query, whether it was for the last hour or six months ago, hit the same table and repeated the same calculations. Session\-level metrics were recomputed again and again, even though nothing about those sessions had changed.


The schema itself didn't help either, with what Ryan describes as "a weird kind of nested payload" holding whatever didn't fit elsewhere. "It wasn't very effective," he says. "This eventually failed and we realized we needed a new table."


The next version introduced a clearer structure, starting with a customer\-specific namespace, followed by time and session identifiers. Grouping events by customer and session made it possible to scope queries more tightly and reflect how merchants actually interact with their data. It was a step toward treating analytics as something computed once and reused, rather than endlessly recalculated.


From there, the team introduced a second table to hold precomputed results. The idea was to calculate metrics like total purchase amount or AOV ahead of time, store the results, and make queries cheap. Most events didn't require any computation at all. But as Ryan explains, "sessions that do require computation (ie. purchases) are a little bit more interesting."


To manage that, the team implemented a "mark and unmark strategy," using [SummingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/summingmergetree) to track which sessions needed processing and clearing them once computation was complete. Behind the scenes, a [refreshable materialized view](https://clickhouse.com/docs/materialized-view/refreshable-materialized-view) ran on a fixed cadence, triggering a massive computation function that gathered all the events for each marked session, performed the aggregation, and wrote the final result back to ClickHouse.


It was complex, but it worked. Queries were noticeably faster. "Customers who couldn't use our system before now actually could use our system," Ryan says. There was some additional write\-time delay, but as he puts it, "It still felt like real time." With performance under control and tens of billions of events migrated, the team's confidence grew. As Ryan recalls, "Product owners felt like, 'Hey, this is awesome—let's add more functionality.'"


## Real\-time meets eventual consistency [\#](/blog/replo#real-time-meets-eventual-consistency)


One of the next big feature requests was fractional attribution. Instead of crediting a full purchase to a single page, the team wanted to distribute value across every page a customer interacts with during a session. So if someone visits five pages and spends five dollars, each page gets a dollar. It sounds simple in theory, but in practice, the numbers didn't add up. "We realized something's wrong," Ryan says. "The math didn't make sense."


The underlying logic seemed sound. The system already knew which events belonged to which session, and the team assumed that once events were written, the queried data would reflect a clean, deduplicated view of those sessions. "That's when we discovered merge trees are only *eventually* deduplicated, not immediately deduplicated," Ryan says. "Since we were using real\-time information and intentionally writing duplicates to our database, we were causing our own problem."


Fortunately, ClickHouse provides clauses like [DISTINCT](https://clickhouse.com/docs/sql-reference/statements/select/distinct) and [FINAL](https://clickhouse.com/docs/sql-reference/statements/select/from#final-modifier) to enforce deduplication at query time. Applying them cleaned up the results instantly. With those changes, test data started behaving as expected. On local datasets with a few hundred thousand rows, everything lined up. "Queries were still snappy, migration was easy," Ryan recalls. "It seemed like it was going fine—but as soon we deployed it, everything started slowing down almost immediately."


This time, when the team looked closer, they saw the same sessions being reprocessed over and over again. Nothing was ever getting cleared. "It seems like sessions aren't being unmarked," Ryan wrote to his team in Slack, as the backlog kept growing.


The culprit was the interaction between real\-time recomputation and full\-table deduplication at scale. Queries that had been cheap in testing now required scanning massive datasets, taking longer than the one\-minute refresh window of the materialized view driving recomputation. Each cycle triggered the next before the previous one could finish.


As Ryan puts it, "We kind of shot ourselves in the foot and caused this runaway train on our entire system." At that point, he says, there was only one question: "How do we fix this?"


## The last approach: keeping it small [\#](/blog/replo#the-last-approach-keeping-it-small)


The final solution didn't exactly come easy. "I'd be lying if I said this was the next approach we took," Ryan admits. "We tried to get this to work with 'mark and unmark' for way longer than we should have. And then we tried having dozens of CTEs that were doing all kinds of deduplication and different times to live."


What ultimately fixed things was a reset in how the team thought about time. If analytics needed to be recomputed, it was only because a purchase had just happened. And as Ryan notes, "A customer is never going to make a purchase six months ago—so the data from six months ago we don't care about."


That realization led to a new table designed specifically for live session events. Instead of scanning across the entire historical dataset, this table tracks only the last 40 minutes of activity, and only for purchase\-related events. "This is a tiny bit of data compared to the 100 billion records we have," Ryan says. Clicks and page views still exist elsewhere, but they no longer dictate recomputation.


With the scope narrowed, the processing logic could be simplified as well. The team moved away from deeply nested CTEs and rebuilt the computation around joins inside a single materialized view. The resulting flusher view is more compact, easier to reason about, and far less prone to runaway recomputation.


This time, the system held. Queries stayed fast. Write\-time lag remained around a minute. Migrating historical data took more effort, with scripts required to backfill older events, but that tradeoff was intentional. As Ryan puts it, "That's an easy, containable problem. We can write a script to handle that migration and not expect our live system to be so fault\-tolerant that it automatically self\-heals and fixes things that happened far in the past."


## A scalable foundation for what's next [\#](/blog/replo#a-scalable-foundation-for-whats-next)


Four months later, Replo's analytics architecture is still holding strong. "Everything is still as snappy as it was before," Ryan says.


With the core pipeline stabilized, the team has continued refining how analytics data is modeled and queried. That includes introducing [LowCardinality](https://clickhouse.com/docs/sql-reference/data-types/lowcardinality) columns, materializing frequently accessed fields out of JSON payloads, and moving away from [Nullable](https://clickhouse.com/docs/sql-reference/data-types/nullable) types in favor of simpler defaults.


Ryan is clear that this isn't the end of the road. "We think there's a lot more performance to be gained," he says — and there's no shortage of [ClickHouse query optimizations](https://clickhouse.com/resources/engineering/clickhouse-query-optimisation-definitive-guide) to explore. "We have a lot more we want to do—we just haven't quite gotten to it yet."


In the end, Replo's ClickHouse story doesn't come down to any one optimization or feature. It's about learning where real\-time systems benefit from simplicity, and where being explicit about tradeoffs leads to systems that are easier to reason about, operate, and scale.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-94-get-started-today-sign-up&utm_blogctaid=94)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
