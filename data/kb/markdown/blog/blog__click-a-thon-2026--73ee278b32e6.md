# Click\-a\-thon 2026: 24 hours, Bengaluru, and the fastest analytical database on the planet


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Click\-a\-thon 2026: 24 hours, Bengaluru, and the fastest analytical database on the planet

![](/_next/image?url=%2Fuploads%2Fprofile_DL_Skpi_Q9_cef68bf559.jpg&w=96&q=75)[Siddhant Agarwal](/authors/sidagarwal)Jun 4, 2026 · 5 minutes readEvery time you tap your phone, a piece of data is racing somewhere to be counted, joined, scored, and acted on before you've finished the gesture. A fraud check on a payment. A recommendation on a feed. An anomaly alert on a service that's about to fall over. A language model deciding which tool to call next. The window between an event happening and a system doing something useful with it has collapsed from days to seconds.


Now, agents are pushing it even further.


That's where ClickHouse fits in. ClickHouse has become the analytical engine powering the modern internet at serious scale for companies like Cloudflare, Uber, eBay, Lyft, Sony, Cursor, Meta, Lovable, and Instacart. But the reason we're writing this post isn't the database — it's the culture around it. ClickHouse has always been a builder's project, and we want to spend more time in rooms with developers who think like that.


## Meet Click\-a\-thon 2026 [\#](/blog/click-a-thon-2026#meet-click-a-thon-2026)


ClickHouse's first in\-person hackathon in India. Bengaluru. August 1–2, 2026\. Teams of 2 to 4 working tech professionals. Four tracks. 24 hours. A total of ₹10,00,000 prize pool.


**Applications are open at [clickhouse.com/clickathon/india2026](https://clickhouse.com/clickathon/india2026) and close on June 25\.**


![clickathon.jpg](/uploads/1200_x_1200_FINAL_1_0848135c34.jpg)
## Constraints beat roadmaps [\#](/blog/click-a-thon-2026#constraints-beat-roadmaps)


You can read the docs. You can watch the benchmarks. You can scroll through the architecture blog posts. None of it teaches you what a database is actually like to build against.


Twenty\-four hours does. It's long enough to ship something real and short enough that you have to make decisions you'd normally argue about for a week. It forces the question every good engineering project eventually asks: what is the smallest version of this that actually works, and can we get there before we run out of coffee?


The most interesting things being built on ClickHouse right now aren't coming from the obvious places. They're coming from small teams pairing ClickHouse with the rest of the modern open source stack and finding combinations nobody at our office thought to try. We want to see more of that, in the same room, on the same weekend.


## The stack you might want to reach for [\#](/blog/click-a-thon-2026#the-stack-you-might-want-to-reach-for)


Three projects in particular are worth knowing about before you walk in, because they show what the new generation of real\-time and agentic systems actually look like in production.


1. **[ClickStack](https://clickhouse.com/clickstack)** is the open source observability stack built on ClickHouse, combining HyperDX for the UI, OpenTelemetry for ingestion, and ClickHouse itself for storage and querying. Logs, metrics, traces, and session replays all in one place, with sub\-second queries over terabytes. If you're building anything that needs to see itself, ClickStack is the path of least resistance.
2. **[Langfuse](https://langfuse.com)** is the open source LLM observability and evaluation platform built on ClickHouse, which handles billions of traces from production AI applications. If your project involves agents, prompt chains, RAG, or anything LLM\-shaped, Langfuse is what teams reach for when they want to actually understand what their model is doing in production.
3. **[LibreChat](https://librechat.ai)** is the open source ChatGPT\-style interface that supports basically every model provider and an increasingly serious set of agent tooling. Paired with ClickHouse for the analytical layer and Langfuse for the trace layer, you have a complete agentic stack that you can stand up in a single weekend. We've seen teams do exactly that.


This is the stack we'd point a friend toward, and the one we'd love to see you build on.


## Pick your track [\#](/blog/click-a-thon-2026#pick-your-track)


1. **Real\-Time Analytics** — Data that moves fast deserves tools that move faster. Build systems where the gap between an event happening and an insight appearing is measured in seconds, not minutes. Streaming ingestion, materialized views, projections — the whole toolbox is on the table.
2. **Observability** — Logs, traces, and metrics are only useful if they help you find the problem. Build something that actually cuts time to resolution, whether that's a smarter UI on top of ClickStack, a new way to correlate signals across services, or an entirely fresh take on what observability should look like in 2026\.
3. **Data Warehousing** — Large datasets, complex analytical queries, fast results. This track rewards depth. Teams that can design schemas, optimize queries, pick the right primary key, and squeeze performance out of genuinely hard problems will go far.
4. **Agentic AI and Analytics** — Most LLM applications barely scratch the surface of what's possible when you pair language models with a real analytical engine. Build agents that reason over data instead of just retrieving it. Tool\-using agents over ClickHouse, evaluated with Langfuse, served through LibreChat — whatever ambitious thing you've been wanting an excuse to try.


## What are you waiting for? [\#](/blog/click-a-thon-2026#what-are-you-waiting-for)


Working tech professionals. Teams of 2 to 4\. Bengaluru, August 1–2\. With ₹10,00,000 on the table.


Before you apply, read the [participant handbook](https://drive.google.com/file/d/1walCGlp3zUPJedqJj9_s4VEVdBkzGy0I/view). It covers eligibility, event structure, judging, and most of the questions you're about to have. Anything not in there, write to [clickathon\-support@clickhouse.com](mailto:clickathon-support@clickhouse.com).


See you in Bengaluru.

### Apply now

Applications close June 25, shortlists go out the first week of July. Apply now. The team captain applies on behalf of the team.[Apply now](https://clickhouse.com/clickathon/india2026?loc=blog-cta-817-apply-now-apply-now&utm_blogctaid=817)### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
