# otel.fyi \- OTel Collector docs made simple


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# otel.fyi \- OTel Collector docs made simple

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_white_add9f20d0f.png&w=96&q=75)[The ClickStack Team](/authors/the-clickstack-team)Apr 17, 2026 · 5 minutes read## Summary

Frustrated with how hard it is to navigate the OpenTelemetry Collector docs, we ended up building our own search\-first interface just to get work done. It proved useful enough that we’ve decided to make it public.


[otel.fyi](https://otel.fyi) is a search\-first site for OpenTelemetry Collector docs, making it easy to quickly find and understand configuration for receivers, processors, exporters, and extensions without digging through scattered documentation.

OpenTelemetry has become the standard for collecting and routing observability data. At the center of this ecosystem is the OpenTelemetry Collector, a vendor\-neutral service that can be deployed in multiple roles across your architecture.


It can run as an agent, sitting close to your workloads to collect logs, traces, and metrics from applications, containers, and infrastructure. It can also operate as a gateway, receiving telemetry from many agents, processing and enriching that data, and routing it to one or more backends. This flexibility is what enables vendor interoperability and gives teams control over how data flows through their systems.


Unfortunately, the collector documentation can be hard to navigate in practice.


Much of the Collector’s functionality lives in contrib packages. These are maintained separately from the core project, and their documentation typically exists in individual repositories as README.md files rather than in a single, unified site. The result is a fragmented experience where users are often forced to jump between folders, search with GitHub code search, and piece together configuration details manually.


## From internal frustration to a simple tool [\#](/blog/otel-fyi#from_internal_frustration_to_a_simple_tool)


This challenge became hard to ignore. Mike, our Product lead for Observability, decided we needed something better. Not a replacement for the official docs, but a faster way to work with them.


Armed with his best friend Claude, he set about implementing what was, at its core, a fairly simple idea.


Take the existing documentation across the OpenTelemetry Collector ecosystem, extract the useful parts, and present them in a consistent, searchable format. Something optimized for how people actually configure the Collector day to day.


In practice, that meant parsing contrib repositories, pulling out configuration examples, and normalizing how receivers, processors, exporters, and extensions are presented. The goal was not completeness for its own sake, but usability. Reduce the time spent digging through README files and make the important details immediately accessible.


*\> While the Collector docs aren’t ideal for human navigation, they’re highly structured under the hood, with consistent organization that makes extracting key metadata and configuration blocks straightforward.*


## A Search\-First Experience for the Collector [\#](/blog/otel-fyi#a_search_first_experience_for_the_collector)


The result is [**otel.fyi**](https://otel.fyi).


![otelfy_apr2026_image2.png](/uploads/otelfy_apr2026_image2_83b73fab1a.png)
It’s a simple site designed around one core workflow: finding the component you need, fast.


You can search across receivers, processors, exporters, and extensions, and immediately get a structured view of each. Instead of digging through long README files, you see the key information upfront, along with configuration examples pulled directly from the source.


Everything is normalized into a consistent format. No more guessing where a config block might be buried or how one component differs from another. The goal is to reduce the time from “I need to configure this” to “I have a working config.”


## Built for how people actually use OpenTelemetry [\#](/blog/otel-fyi#built_for_how_people_actually_use_opentelemetry)


We built otel.fyi primarily for ourselves, because we needed something lightweight and fast, focused on the practical task of assembling Collector configurations without constantly jumping between repositories and README files, and as we started relying on it day to day, it became clear it could be useful beyond our own workflows.


Rather than keeping it internal, it made sense to make it available more broadly and see if it helps others working with OpenTelemetry in the same way.


## What’s next [\#](/blog/otel-fyi#whats_next)


Search is just the starting point, and we’re already thinking about how to make this more useful in practice, including adding an AI assistant to help guide configuration, answer questions, and reduce the amount of context switching required when working with the Collector.


For now, the focus is simply on making the OpenTelemetry Collector easier to work with, based on the workflows we deal with every day.


We’ve found it genuinely useful in our own work, and if you’re spending time configuring OpenTelemetry, there’s a good chance you will too. Explore it at [otel.fyi](https://otel.fyi).

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-413-get-started-today-sign-up&utm_blogctaid=413)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
