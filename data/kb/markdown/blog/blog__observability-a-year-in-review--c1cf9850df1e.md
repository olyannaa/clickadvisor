# Observability \- a year in review


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Observability \- a year in review

![](/_next/image?url=%2Fuploads%2Fmike_shi_5b7145e7d7.jpg&w=96&q=75)[Mike Shi](/authors/mike-shi)Jan 7, 2026 · 9 minutes read## Introduction [\#](/blog/observability-a-year-in-review#introduction)


With the start of the new year, it feels like the right moment to pause and reflect on a year that was pivotal for observability at ClickHouse and for me personally. As Head of Product Management for Observability, my focus throughout 2025 was building ClickStack and working closely with customers, partners, and the broader community to rethink what scalable observability should look like.


In May 2025, we introduced ClickStack with a simple goal: make high\-performance observability on ClickHouse accessible to everyone. Until then, teams either built their own user interfaces on top of ClickHouse or relied on more generic visualization tools like Grafana. By pairing ClickHouse with the HyperDX UI, ClickStack removes that friction and allows teams to immediately benefit from ClickHouse’s compression and fast query execution optimized for logs, traces, and metrics.


For a detailed reflection on what 2025 looked like for ClickStack itself, [see our earlier blog](https://clickhouse.com/blog/clickstack-a-year-in-review-2025).


Here, I want to focus instead on a few broader observations about how the observability landscape shifted over the past year, shaped by my conversations with our users, time spent at conferences, and ongoing discussions across the observability community.

### Learn about ClickStack

Explore the ClickHouse\-powered open source observability stack built for OpenTelemetry at scale.

[Get started](https://clickhouse.com/use-cases/observability?loc=blog-cta-31-learn-about-clickstack-get-started&utm_blogctaid=31)## Volume and cardinality became the hard limits [\#](/blog/observability-a-year-in-review#volume-and-cardinality-became-the-hard-limits)


In 2025, it became clear that volume alone was no longer the primary challenge in observability. While data volumes continued to grow, high cardinality emerged as the more fundamental constraint. Applications now emit more telemetry than ever, but with far greater dimensionality, turning what was once an edge case into the default.


AI workloads accelerated this shift. Model versions, prompts, GPU IDs, shards, tenants, and execution graphs all introduced new labels, compounding cardinality across every signal. Large\-scale training and inference systems, often spanning thousands of GPUs, multiplied telemetry across hardware, network, scheduling, and software layers. The result was an explosion in unique combinations that observability systems were expected to store and query interactively.


This level of cardinality exposed the limits of many existing platforms. Storage systems were no longer just required to ingest data, but to aggregate and query it efficiently at scale. In practice, high cardinality became a huge cost driver for observability users. It’s clear that existing observability data stores are well past their limits and the industry needs to rethink how to scale to current user demands, without requiring users to lose data through sampling and stripping out cardinality.


## Tracing became the dominant signal [\#](/blog/observability-a-year-in-review#tracing-became-the-dominant-signal)


Over the past year, tracing moved from an advanced feature to the primary way engineers reason about complex systems. Asynchronous workflows, queues, streaming pipelines, and agent\-based execution have blurred traditional request boundaries. At the same time, AI workloads introduced non\-determinism and fan\-out patterns that metrics alone could no longer summarize in a meaningful way.


Traces provided the structure that logs and metrics could only hint at. Increasingly, we saw teams consolidate metrics onto traces, using spans as the organizing unit for understanding system behavior. This shift placed new demands on observability platforms, stressing assumptions that were never designed for trace\-first workloads.


Span counts per trace continued to grow, often dramatically \- we regularly engage users with 10k spans per trace. Many teams were forced to rely on aggressive sampling just to keep systems usable. The difference became clear between platforms built with tracing as a first\-class concern and those where tracing was added later as an afterthought.


## OpenTelemetry fully crossed the chasm [\#](/blog/observability-a-year-in-review#opentelemetry-fully-crossed-the-chasm)


By the time we started ClickStack in mid\-2025, we made a deliberate decision to ensure that HyperDX, the UI behind ClickStack, could work with any schema. That flexibility still has real value. In practice, though, we increasingly see users standardizing on OpenTelemetry, with alternative schemas and competing specifications falling away.


New services are now instrumented with OpenTelemetry by default, and legacy systems are steadily being retrofitted. Value is emerging in areas like fast, opinionated instrumentation and data pipelines, with companies such as [Bindplane](https://bindplane.com/) and [Odigos](https://odigos.io/), along with newer projects like [Rotel](https://streamfold.com/), standing out as particularly compelling.


However, OpenTelemetry still has challenges around its adoption \- with complex configurations required out of the box, in\-depth concepts that are difficult to learn on the fly, and standards and best practices that continue to evolve with the project. This is an area our team will help contribute to in the coming year to continue advancing vendor\-neutral standards in observability.


## Open Source adoption accelerated through real migrations [\#](/blog/observability-a-year-in-review#open-source-adoption-accelerated-through-real-migrations)


Since its launch last year, we’ve seen ClickStack adopted by teams migrating from existing observability platforms, rather than purely through greenfield experimentation. That was somewhat unexpected. Open source projects often see early traction from new workloads, with migrations following later. In observability, the pattern appears to have reversed.


The reasons were pragmatic rather than ideological. As tracing volumes and retention periods grew, SaaS pricing models have become harder to justify. Open source offered cost predictability, data ownership, and relief from opaque billing, making it an increasingly attractive option. For many teams, these factors outweighed the appeal of a perfectly polished, all\-in\-one user experience.


At higher data volumes, priorities have shifted. Flexibility in querying and the ability to scale cost\-effectively mattered more than feature completeness. Teams were willing to accept trade\-offs, focusing on strong coverage of core workflows rather than comprehensive but expensive solutions. Running open source observability systems does require work, but for many users in 2025, that effort proved preferable to the costs and constraints of proprietary platforms \- especially for those at larger scale.


## AI SRE advanced, but is still pre\-breakout [\#](/blog/observability-a-year-in-review#ai-sre-advanced-but-is-still-pre-breakout)


Throughout 2025, we engaged with a growing number of vendors promising some form of “agentic SRE.” Companies like [traversal.ai](https://traversal.com) and [resolve.ai](https://resolve.ai) are clearly pushing the space forward, joined by both established players such as [Wild Moose](https://www.wildmoose.ai/) and a wave of new entrants. The pace of experimentation has been impressive.


In our experience, what worked best were co\-pilot\-style workflows focused on summarization, correlation, and guided investigation, while a human stayed in the loop. These interactions felt meaningfully useful rather than gimmicky and robust in production (vs just a great demo) \- [our own internal testing largely reinforced](https://clickhouse.com/blog/llm-observability-challenge) that impression.


There is no clear winner yet. Most tools still fall well short of the reasoning depth and reliability seen in mature code\-focused assistants. The bar to enter the market remains relatively low, but the gaps show quickly: shallow reasoning, fragile context windows, and limited actionability. These systems can think faster than humans, but they do not replace human judgment. The ceiling is clearly visible. While we saw encouraging progress in 2025, it has not been broken yet. 2026 promises to be an important year for this space.


## Data quality emerged as a first\-class question [\#](/blog/observability-a-year-in-review#data-quality-emerged-as-a-first-class-question)


For years, many teams spent most of their energy simply getting observability pipelines to work end to end. By 2025, that work had become significantly easier. OpenTelemetry, along with a maturing ecosystem of agents and pipeline tools, standardized instrumentation and transport and made reliable delivery far more attainable.


That maturity didn’t mean data quality suddenly became important. Some teams had been wrestling with it for years. What changed in 2025 was the scale and urgency of the problem. As observability became easier to adopt, teams found themselves collecting far more telemetry than they could realistically use, while still paying to store and query most of it. Cost pressure made this impossible to ignore. As a result, the conversation shifted. Data quality became more nuanced and, in many ways, harder to answer. Teams stopped asking whether they were missing data and started asking different questions. Can we actually use this telemetry? Is it actionable? Does it help us reach the root cause faster and make better decisions? Most importantly, which signals are worth their cost?


This shift went well beyond schema validation or ingestion correctness. It forced teams to think about usefulness, redundancy, and the cognitive load required to interpret their data. While a few organizations made real progress on this in 2025, the same questions surfaced repeatedly in our conversations. This tension between signal, cost, and usability feels set to become the defining observability battleground of 2026\.


## My final take [\#](/blog/observability-a-year-in-review#my-final-take)


For me, 2025 was the year observability collided with scale, complexity, and AI. Growing volume and cardinality forced vendors toward architectural honesty. Tracing became unavoidable and emerged as the dominant signal. OpenTelemetry solidified the ecosystem, while open source options expanded well beyond the traditional ELK and LGTM stacks, becoming both more diverse and far more scalable.


AI\-driven SRE took its first real steps forward, but it did not yet break through into a standard, production\-ready approach. Deployments still required deep vendor involvement and remained difficult to adopt without significant effort. At the same time, data quality finally became a first\-class conversation, shifting focus away from simply collecting telemetry toward understanding which signals are actually useful.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
