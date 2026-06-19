---
source: blog
url: https://www.mintlify.com/
topic: mintlify-boosts-nps-30-and-saves-60-with-real-time-analytics-on-clickhouse-cloud
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 6
---

# Mintlify boosts NPS 30% and saves 60% with real\-time analytics on ClickHouse Cloud

\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Mintlify boosts NPS 30% and saves 60% with real\-time analytics on ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Apr 14, 2026 · 10 minutes read## Summary

Mintlify uses ClickHouse Cloud to give tens of thousands of companies real\-time visibility into how tens of millions of developers engage with their content. After replacing PostHog with ClickHouse, dashboard load times dropped from tens of seconds to sub\-one\-second, driving an estimated 30% NPS improvement. ClickHouse Cloud requires zero ongoing maintenance and runs at 60% lower cost than PostHog, with an architecture built to scale well beyond Mintlify's current size.

[Mintlify](https://www.mintlify.com/) is the intelligent knowledge platform powering help centers, support centers, and developer documentation sites for companies like Anthropic, Microsoft, Coinbase, and Perplexity, serving tens of millions of developers each month.

Over the past year, the company has seen a major shift in who—or what—is reading those docs. Traffic that was once 90% human and 10% AI crawlers is now split evenly, and Mintlify expects AI agents to account for 90% of all traffic by the end of 2026\.

As tools like ChatGPT, Claude, and Cursor increasingly rely on documentation, Mintlify's customers need fast, reliable insight into how both humans and agents are engaging with their content, so they can make informed decisions about what to improve. But as usage grew, serving that data quickly and reliably turned out to be harder than expected.

"Prior to using ClickHouse, opening the analytics page in the Mintlify dashboard could take tens of seconds to load," says engineering manager Nicholas Khami. "After using ClickHouse, we've gotten that latency down to sub\-one\-second—it's almost instant."

We caught up with Nick to learn why Mintlify migrated from PostHog, what made them choose [ClickHouse Cloud](https://clickhouse.com/cloud), and how it's helping them scale to meet a future dominated by AI agents.

## Outgrowing PostHog [\#](/blog/mintlify#outgrowing-posthog)
