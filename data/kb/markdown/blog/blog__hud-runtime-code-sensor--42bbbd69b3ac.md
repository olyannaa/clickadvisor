# How Hud is building the first runtime code sensor with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Hud is building the first runtime code sensor with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Nov 10, 2025 · 10 minutes read[Hud](https://www.hud.io/) bills itself as the “world’s first runtime code sensor,” a system that runs in live production and dynamically gathers context to understand how code behaves at both the function level and the business level. Traditional observability relies on manual logs and traces, resulting in data\-heavy systems that too often don’t have the right piece of information when something goes wrong. Hud took a different approach. Their vision was a sensor that follows the execution of every code flow at the function level, sending only small aggregated data during steady state—but when something goes wrong, switching gears to collect the deep forensic data engineers need to understand and resolve the issue.


“We don’t just provide you with a stream of data, and we don’t just alert you to the fact that something happened,” says Hud co\-founder and CTO May Walter. “We have opinions about whether something is wrong or not, and when it isn’t we provide you with root cause context automatically.”


But delivering on that promise is easier said than done, especially when negligible production footprint is a key requirement. Hud’s runtime SDKs emit significant volumes of function\-level telemetry, which must be processed, correlated with metadata in real time, and kept version\-aware across continuous deployments. While this is a fraction of what traditional observability solutions would send, Hud wanted to do it in the most performant and efficient way possible. From its very first release, Hud has relied on [ClickHouse Cloud](https://clickhouse.com/cloud) to power that architecture.


We caught up with May, along with head of engineering Almog Freizeit and software engineer Ilan Shamir, to learn how Hud built a new model for understanding code behavior in production, the architectural shifts that made it possible, and the results they’re seeing today.


## Changing the equation in observability [\#](/blog/hud-runtime-code-sensor#changing-the-equation-in-observability)


Hud was founded in 2023 by a team of engineers who had led large development organizations and kept running into the same problems. As May puts it, “Even though observability is a huge market, it still sucks, and when production is on fire often no one knows why. It’s difficult to imagine a future of AI\-generated code using the classic observability approach.”


The problem wasn’t a lack of data; if anything, it was too much of it. Existing observability tools were built to collect as much information as possible, but they often lack the specific data engineers need right then and there. Dashboards are full of charts, alerts fire constantly, and terabytes of logs pile up. In the heat of an incident, the critical clue could be buried anywhere, or missing because no one thought in advance about this particular scenario. “In the right moment, it’s very hard to find that needle in the haystack,” May says.


Thinking about the future of software engineering, Hud was created to flip that equation. Instead of overwhelming teams with tons of raw data, the founders envisioned a system that could spot when behavior actually degraded, point straight to the relevant function or code version, and automatically pull together the forensic context to fix it.


That mission has become even more urgent with the accelerated adoption of AI coding agents and the industry’s desire to have them write code that can be safely shipped to production. With code being generated and deployed faster than ever, May and her team saw the stakes rising. “As much as agentic adoption grows, this problem is going to become a thousand times worse,” she says. “How can agents be expected to generate production\-safe code if they don’t have a feedback loop for how that code actually behaves in production?”


## Choosing ClickHouse (and ClickHouse Cloud) [\#](/blog/hud-runtime-code-sensor#choosing-clickhouse-and-clickhouse-cloud)


Like a lot of startups, Hud’s first prototype started out on Postgres. It was the fastest and safest way to validate the idea, but it didn’t take long to realize that a row\-based database couldn’t support what the team wanted to do.


“Quite early on, we understood that we really needed a [columnar architecture](https://clickhouse.com/docs/faq/general/columnar-database) in order to be able to look across different functions and versions over time,” May says. “We were familiar with ClickHouse, mostly from blogs and other materials, and trying it out was easy enough.” After prototyping a few other columnar databases, they decided ClickHouse was the best fit.


High cardinality was a deciding factor. “One of our biggest challenges is that we want to not only observe data in terms of the regular high\-cardinality situations, but we actually want to identify degradations,” May explains. “If someone just deployed a change, I don’t just want to know if something’s fine—I want to know if this change is helpful or harmful to the deployment.”


“When looking at other solutions, we saw that high cardinality was usually discouraged,” Ilan adds. “ClickHouse, on the other hand, does support high cardinality with telemetry data. We definitely take advantage of that in many, many areas.”


Flexibility mattered, too. Running on [ClickHouse Cloud](https://clickhouse.com/cloud) gave Hud the speed to move quickly without worrying about database operations. And because they had the option to self\-host later, they could still support enterprise customers with on\-prem requirements. For a young company in a dynamic space, that combination of speed today and choice tomorrow was attractive.


## Hud’s ClickHouse\-based architecture [\#](/blog/hud-runtime-code-sensor#huds-clickhouse-based-architecture)


Once ClickHouse was in place as the core telemetry database, Hud’s next challenge was designing an ingestion pipeline that could reconcile telemetry with metadata in real time.


Their first approach paired ClickHouse with a Node.js service and a Redis state machine. Redis temporarily held partial state while Node.js coordinated enrichment, matching telemetry with metadata once it arrived. It worked well enough to get the product to market, but it came with overhead. Before long, network round\-trips and memory pressure started to show.


“We had built a pretty complex architecture around other technologies,” Almog says. “As we added more customers and usage scaled, we realized we can count on ClickHouse for more pieces of the puzzle, and we redesigned enrichment to run inside ClickHouse. This eliminated coordination overhead and gave us a cleaner, faster pipeline.”


The breakthrough came when Hud pulled enrichment into ClickHouse itself. Using [Null engine tables](https://clickhouse.com/docs/engines/table-engines/special/null) and [dictionaries](https://clickhouse.com/docs/sql-reference/dictionaries), they made enrichment in\-memory and declarative. Then, with [ReplacingMergeTree tables](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree), they added a queue\-like buffer so telemetry could be ingested right away and joined with metadata once available, with outdated rows expiring automatically. The buffer was especially critical because telemetry often arrived before the corresponding metadata, and Hud needed a way to reconcile the two streams without losing data.


In the new ingestion pipeline, telemetry flows into raw tables, passes through enrichment logic, and is either committed directly or held briefly in a buffer until metadata arrives. Metadata is written into live and archival MergeTree tables with defined retention windows, giving Hud both speed and historical depth.


![User Story Hud Issue 1197.jpg](/uploads/User_Story_Hud_Issue_1197_3bc8fa0f3e.jpg)
“We had to employ some sophisticated techniques to make it work,” Ilan says. “It’s a pretty unique solution.”


Almog calls the rearchitecture “a really big step in the way of supporting scale.” By consolidating ingestion and enrichment inside ClickHouse, she says, the team “drastically improved the scale, stability, and latency of our system.”


## Impact across the board [\#](/blog/hud-runtime-code-sensor#impact-across-the-board)


Today, Hud ingests hundreds of megabytes per second of raw JSON, which compresses down to tens of MB/s once stored in ClickHouse. Their ClickHouse Cloud deployment holds more than 11 terabytes of telemetry data.


Even at this scale, engineers can query function\-level telemetry across deployments and detect degradations within minutes of a release. The ability to track changes against baselines, rather than relying on thresholds, makes detections more accurate and actionable.


The rearchitecture has brought major gains in stability and performance. By removing Redis and consolidating enrichment inside ClickHouse, Hud cut out costly network calls and memory bottlenecks. The pipeline is now simpler and more predictable, with the database itself handling both ingestion and reconciliation. The result is lower latency, better scalability, and a much smoother developer experience.


Most importantly, Hud can express production problems in terms engineers immediately understand: functions, versions, and services. Business\-level issues can be traced back to specific code paths, and every incident comes with the supporting context. And that context isn’t just surfaced in dashboards; Hud makes it available directly in the IDE, where engineers (and increasingly AI agents) can act on it immediately. That bridge between business impact and engineering detail is what makes the product unique.


## What’s next for Hud and ClickHouse [\#](/blog/hud-runtime-code-sensor#whats-next-for-hud-and-clickhouse)


With the ingestion bottleneck behind them, Hud is focused on optimizations. Plans include giving users more control, like supporting multiple time resolutions in queries so teams can zoom in or out depending on what they’re analyzing. They’re also exploring tiered levels of cardinality, letting lightweight queries skip the overhead of full\-detail data.


Cost optimization is another priority. As the product scales, the team is refining its schema design and resource usage to keep things efficient. ClickHouse Cloud’s scalability means they can make those adjustments without having to rethink their architecture.


Deployment flexibility matters too. ClickHouse Cloud is their go\-to for speed, but Hud still has the option to self\-host for enterprise customers who require it. That way, the product can serve both fast\-moving startups and larger organizations with stricter requirements.


Looking ahead, May, Almog, Ilan, and the team remain focused on delivering visibility into how the code behaves in production the way engineers actually think. By continuing to expand their use of ClickHouse, not just as a telemetry store but as the engine for ingestion and enrichment, they’ve built a platform that combines scale, speed, and clarity.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-7-get-started-today-sign-up&utm_blogctaid=7)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
