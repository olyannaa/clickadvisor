# How Laminar is using ClickHouse to reimagine observability for AI browser agents


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Laminar is using ClickHouse to reimagine observability for AI browser agents

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Aug 22, 2025 · 7 minutes readToday’s AI agents are doing more than generating text. They’re navigating websites, clicking buttons, and performing tasks on their own. For developers working on browser\-based AI applications, it’s no longer enough to track what an agent *says*. You have to *see what it sees*.


“These kinds of AI agents require a completely new type of observability,” says Robert Kim, co\-founder and CEO of [Laminar](https://www.lmnr.ai/), an open\-source platform for tracing and evaluating AI applications. “We call it browser agent observability.”


Laminar lets developers capture video recording of the browser window synchronized with agent traces, almost like a flight recorder for AI. “They can supervise the browser agent and see exactly what the agent was seeing—how the browser was behaving, the popups, the network errors, and so on,” Robert says.


Every day, Laminar’s platform ingests hundreds of thousands of browser session events and reconstructs them into video\-like sessions. Powering that experience requires a database that’s fast, flexible, and reliable. “ClickHouse is what enables us to do all of this,” Robert says.


We caught up with Robert to learn how Laminar is rethinking observability for the agentic AI era, and why they chose [ClickHouse Cloud](https://clickhouse.com/cloud) as their real\-time data warehouse.


![unnamed (1).jpg](/uploads/unnamed_1_21a151f667.jpg)
## Seeing through the agent’s eyes [\#](/blog/how-laminar-reimagined-observability-for-ai-browser-agents#seeing-through-the-agents-eyes)


Robert and his co\-founder Din Mailibay started Laminar in 2024, joining Y Combinator’s Summer 2024 cohort. At its core, Laminar is an all\-in\-one, open\-source observability and evaluation platform for LLM applications. But the team quickly spotted an opportunity to become the default observability layer for a fast\-emerging category: browser\-based AI agents.


“We talked with a lot of companies building browser agents and realized their biggest pain point was debugging,” Robert says. “They were relying on disjointed screenshots from different steps and windows. It was hard to compile a cohesive picture of what actually happened. That’s when we thought, why not record the entire session as a video, so users can see exactly what the agent saw and did?”


Actually recording video, Robert says, would be “too slow and unbearable for the user experience.” Instead, Laminar captures DOM diffs using RRWeb, a browser recording tool that tracks structural changes in the page. They patch the Playwright framework to inject event listeners into the browser, then use their SDK to stream these events back to the backend. The entire pipeline (written in Rust) is optimized for high\-throughput processing and rapid search.


The result is a full visual trace of the agent’s session. “It’s literally what the agent saw, rendered as a video,” Robert says. “Imagine opening a 30\-minute video on YouTube, and it’s instantly loaded. That’s the experience our users have.”


Currently, Laminar’s observability stack powers many agentic companies, especially in the browser agents space. Laminar is the [default observability platform](https://docs.browser-use.com/development/observability) for the popular browser automation framework Browser Use. And here’s an example of what a trace with a session recording [looks like](https://www.lmnr.ai/shared/traces/98b1e47c-2b8a-64f5-9ab2-7189521e314b).


## “ClickHouse was the obvious choice” [\#](/blog/how-laminar-reimagined-observability-for-ai-browser-agents#clickhouse-was-the-obvious-choice)


Once we switched to ClickHouse, everything just worked. It was incredibly fast.”


When Robert and the team started building Laminar, they didn’t have to think hard about which database to use. They’d worked with ClickHouse in previous startups and knew it was fast, flexible, and powerful enough to handle “an incredible amount of traffic.”


“We honestly didn’t even consider others,” Robert says. “ClickHouse was the obvious choice.”


### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
At first glance, Laminar’s use case might not seem like a natural fit. ClickHouse is traditionally used for analytics, not video\-style trace replay. But the team knew what it could do, and they saw an opportunity to push it further. “We really liked the fast writes and fast reads,” Robert says. “We needed a database that could handle high\-throughput ingestion without adding latency or slowing down the core logic of the application.”


That confidence was reinforced by earlier trials. Before standardizing on ClickHouse, the team had experimented with other databases to support search functionality. “The first version was Postgres\-like, and it was incredibly slow,” Robert says. “Then we tried another open\-source database, but it didn’t work well either. Once we switched to ClickHouse, everything just worked. It was incredibly fast.”


While the team appreciated ClickHouse’s open\-source roots (“all of our tech stack is open\-source,” Robert notes), they ultimately chose to run [ClickHouse Cloud](https://clickhouse.com/cloud). “Even though we like managing infra, we don’t need to manage yet another thing,” he says. “As a small team, ClickHouse Cloud lets us focus on what we care about and offload database management to the people who do it best. Plus, the pricing was great.”


## Performance that feels like magic [\#](/blog/how-laminar-reimagined-observability-for-ai-browser-agents#performance-that-feels-like-magic)


Today, Laminar’s system ingests over 500,000 browser events per day. Thanks to ClickHouse, Robert says, the load “doesn’t affect our infra at all. It’s that smooth.” Since launch, the platform has recorded over 1 billion events and read more than 50 billion (mostly due to developers replaying traces multiple times while debugging).


Agent sessions can last 30 minutes or more, generating hundreds of thousands of DOM diff events. Yet when users load a trace, it opens almost instantly. “This is because we made some ClickHouse magic with highly optimized [tables and partitions](https://clickhouse.com/docs/partitions),” Robert says.


The numbers back it up. Laminar sees P90 insert latencies of 150 milliseconds and P90 selects at just 60 milliseconds. With reads far outpacing writes in their workload, that kind of responsiveness is huge. “We have super, super fast writes, but more importantly super, super fast reads,” Robert says. “And we have an incredible user experience because of that.”


Storage isn’t a bottleneck either. Because Laminar records lightweight DOM diffs instead of raw video, the data is inherently compact. “It’s all div, div, div,” Robert says. ClickHouse’s [columnar compression](https://clickhouse.com/docs/data-compression/compression-in-clickhouse) does the rest, reducing the footprint without compromising performance.


That combination of elite speed and reliability has validated Laminar’s decision to run on ClickHouse Cloud. When a “nasty bug” in their observability SDK triggered more than a billion writes in a single day, the platform scaled automatically. “At that point, we realized ClickHouse just calls more compute when it needs to,” Robert says. “We’ve been really happy that we went straight to ClickHouse Cloud and didn’t bother to self\-host.”


## Observability for the agentic AI era [\#](/blog/how-laminar-reimagined-observability-for-ai-browser-agents#observability-for-the-agentic-ai-era)


As browser\-based agents become more common across AI and automation workflows, Laminar sees a growing opportunity to become the default observability layer for developers working at the edge of this new frontier.


“We want to support as many users as possible who are building and observing browser agents, computer\-using agents, and long\-running agents of all kinds,” Robert says.


That means not only handling more data, but continuing to deliver sub\-second reads, high\-throughput ingestion, and instant replays. With ClickHouse Cloud, Robert and the team are confident they have the foundation to scale observability for the agentic AI era. They have moved all their core trace, dataset, and eval data to ClickHouse and ingest 100s of GB of data daily (millions of traces) due to ClickHouse scalability and their extremely fast Rust backend.


Can ClickHouse Cloud transform your data operations? [Try it free for 30 days.](https://clickhouse.com/cloud)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
