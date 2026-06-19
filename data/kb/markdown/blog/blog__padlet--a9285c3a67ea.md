# How Padlet uses ClickHouse Cloud to power real\-time classroom analytics


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Padlet uses ClickHouse Cloud to power real\-time classroom analytics

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Mar 30, 2026 · 9 minutes read[Padlet](https://padlet.com/) builds tools that help teachers turn lessons, prompts, and activities into something students can engage with directly. The product is inherently visual, designed to make classroom materials feel approachable rather than formal or rigid. It's all in service of a mission the company describes as "making software for a good education."


"We believe a good education is when kids learn to be curious and creative, and when they learn to collaborate," says Zoheb Jamal, Padlet's VP of Growth. "We want to make a product that teachers can use to make visually stunning content that kids find fun and engaging."


Today, Padlet is used in 242 of 246 countries worldwide. "There are still four holdouts," Zoheb jokes. "We're confident we're going to get them." As that reach expanded to tens of millions of unique users, the team began to see a growing gap between how teachers wanted to use classroom data and how analytics were being delivered.


Zoheb spoke at our [recent ClickHouse meetup in Singapore](https://clickhouse.com/jp/videos/singapore-meetup-padlet-25sep25), where he shared how Padlet used [ClickHouse Cloud](https://clickhouse.com/cloud) to build a real\-time analytics stream, giving teachers immediate insight into how students are engaging, rather than waiting on delayed reports.



## Why real\-time matters in the classroom [\#](/blog/padlet#why-real-time-matters-in-the-classroom)


For teachers using Padlet in the classroom, questions naturally started to come up around engagement. Were students interacting with a lesson? Which activities were resonating? How long were students spending on a page? For a long time, getting answers meant writing to Padlet and waiting for someone to crunch the numbers and send back a snapshot.


"That's not great," Zoheb says. "Imagine you want to know how much money you have in your bank account, and you have to write an email to your bank and get a number back two days later. That's the kind of poor experience we wanted to fix."


So the team focused on giving teachers access to a small set of core metrics on demand. The goal was less about advanced reporting and complex dashboards, and more about letting teachers see what was happening as lessons unfolded.


At Padlet's scale, however, delivering that experience came with real technical constraints. The product serves around 40 million unique monthly users, generating billions of events. "If the event volume was any lower, we could have just used a simple solution like Postgres," Zoheb says. "That's probably the only time I wish we had fewer users."


There was a clear gap between what teachers needed and what Padlet's existing stack was built to support. "What we needed was a more robust solution," Zoheb says.


## What Padlet needed from an analytics system [\#](/blog/padlet#what-padlet-needed-from-an-analytics-system)


As they kicked off their search for a new database, Padlet put together a simple rubric covering both functional and non\-functional requirements.


On the functional side, real\-time was non\-negotiable. "If a teacher is doing an activity in the classroom, we want them to get numbers then and there, not a day later," Zoheb says.


Speed mattered just as much. "By fast, I mean you click and get results," Zoheb says. Performance, he explains, is a core focus across the product, with a "dedicated speed team" whose sole job is to keep Padlet fast. "There was no way I could have shipped a slow analytics service under the radar," he jokes.


Operationally, the bar was just as high. With a team of around 65 people and no dedicated data team, Padlet wanted something that would largely run on autopilot. "We didn't want to maintain servers, we didn't want to do patches, we didn't want to manage pipelines," Zoheb says. "We just wanted to set up a solution and then let it run."


Cost was another factor. Padlet wasn't looking for the cheapest possible option, but they did want something that would remain affordable as usage grew. As Zoheb puts it, "We wanted something sustainable, which we could use today and continue to afford in the future."


Finally, longevity mattered. The team had been burned before by analytics and BI tools that were abandoned or shut down after an acquisition. "We needed something that would at least last us through the 21st century," Zoheb says. "So just 70 to 80 more years."


## Why Padlet chose ClickHouse Cloud [\#](/blog/padlet#why-padlet-chose-clickhouse-cloud)


Over the course of a few weeks, the team ran a series of POCs to see which options could deliver. In the end, Zoheb says, "ClickHouse ticked all the boxes."


Ingestion speed stood out first. ClickHouse delivered "crazy\-fast ingestion," making it possible to support live classroom use cases without lag or batching delays. "That's what you need for real\-time—the ability to ingest all those events very quickly," Zoheb says.


Query performance was another plus. The team was drawn to ClickHouse's specialized engines like [MergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree) and [AggregatingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/aggregatingmergetree), which store data compactly and prune aggressively at query time, so only a small subset of data needs to be loaded into memory. Strong support for [materialized views](https://clickhouse.com/docs/materialized-views) added what Zoheb calls a "further boost in our performance."


Running infrastructure in\-house was never the plan, so Padlet chose [ClickHouse Cloud](https://clickhouse.com/cloud). "It's been running on autopilot for the past year," Zoheb says. When the team did encounter an early issue tied to [partitioning](https://clickhouse.com/docs/partitions), it was identified and resolved quickly. "That's the kind of turnkey solution we're looking for, and that's what we got with ClickHouse."


The managed service is reasonably priced, Zoheb adds, and getting started was straightforward. "When we wanted to try it, we didn't have to talk to a sales team," he says.


ClickHouse's maturity sealed their decision. Open\-sourced more than a decade ago, the database is now used by many of the world's largest companies for [real\-time analytics](https://clickhouse.com/resources/engineering/what-is-real-time-analytics). As Zoheb puts it, "That gave us confidence we can continue to use this product for a while—if we do the implementation right."


## Padlet's ClickHouse\-based analytics pipeline [\#](/blog/padlet#padlets-clickhouse-based-analytics-pipeline)


With ClickHouse Cloud in place, Padlet got to work wiring up its real\-time pipeline. Rather than starting from scratch, the team built on top of their existing event infrastructure, extending it where needed and keeping the overall design simple.


Padlet already tracked core interactions like page views and visits, but engagement time required a different approach. Instead of relying on complex client\-side logic to infer whether a student was actively engaging with a page, they opted for a simpler, more reliable model based on "heartbeat" events. Every 30 seconds, an active session emits a small event, with each event representing a fixed slice of engagement time.


Those engagement events are ingested into ClickHouse using [ClickPipes](https://clickhouse.com/cloud/clickpipes), ClickHouse's native ingestion service. The team chose ClickPipes to avoid standing up and maintaining additional infrastructure, and to keep ingestion simple. "It was easy to set up and quite cost\-effective," Zoheb says. Existing view and visitor events continue to flow through Padlet's internal event pipeline, with both streams converging in ClickHouse for analysis.


![](/uploads/Padlet_User_Story_Issue_1249_86a2a47bad.png)
*Padlet's event pipeline feeding ClickHouse for views, engagement time, and unique visitors.*


Once the data lands in ClickHouse, Padlet relies on materialized views to keep queries fast and predictable. Views and engagement time are pre\-aggregated by date, while unique visitors rely on [HyperLogLog](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/uniqcombined) sketches for efficient aggregation across time ranges. "We didn't do any fancy maths," Zoheb says. "ClickHouse has this natively available, so using it was a breeze."


From initial setup to production, the entire pipeline came together in about a month. "We're fortunate to have a great engineering team, and we also got a very solid product in ClickHouse," Zoheb says. "That's how we were able to move so quickly."


## Blazing\-fast and built for what's next [\#](/blog/padlet#blazing-fast-and-built-for-whats-next)


Ultimately, Padlet's goal wasn't to build a sprawling analytics system, but something fast, reliable, scalable, and easy to operate. The results speak for themselves.


As Zoheb shared at the [Singapore meetup](https://clickhouse.com/jp/videos/singapore-meetup-padlet-25sep25), Padlet ingested roughly 8 billion events into ClickHouse in a single month. The system now supports around 14 requests per second (up from their original goal of 10\) with a median query latency of 45 milliseconds and a P99 response time of 690 milliseconds. For teachers, engagement data feels like a natural extension of the lesson itself, not something that arrives after the moment has passed. "When someone clicks it, they're going to see results immediately," Zoheb says.


Looking ahead, Padlet plans to expand its analytics well beyond this first version. As new features and AI\-driven tools roll out across the product, teachers are asking for deeper insight into how those features are being used and how students are interacting with them. "We intend to use ClickHouse to power pretty much all of these use cases," Zoheb says.


With ClickHouse Cloud, what began as a way to surface a few core metrics has grown into a real\-time analytics layer that remains lightweight enough for a small team to operate. As Padlet continues to grow, ClickHouse is set to remain a central part of how the company—and the teachers who rely on it every day—understand and improve learning in the moment.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-281-get-started-today-sign-up&utm_blogctaid=281)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
