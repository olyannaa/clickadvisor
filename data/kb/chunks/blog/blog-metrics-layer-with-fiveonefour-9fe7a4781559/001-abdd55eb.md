---
source: blog
url: https://github.com/514-labs/financial-query-layer-demo
topic: define-once-use-everywhere-a-metrics-layer-for-clickhouse-with-moosestack
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 8
---

# Define once, use everywhere: a metrics layer for ClickHouse with MooseStack

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Define once, use everywhere: a metrics layer for ClickHouse with MooseStack

![](/_next/image?url=%2Fuploads%2Ffiveonefour_avatar_8b25b9739c.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fnakulbio_3533dbd36d.jpg&w=96&q=75)[Fiveonefour](/authors/fiveonefour) and [Nakul Mishra (AWS)](/authors/nakul-mishra)Mar 13, 2026 · 11 minutes readLet’s say you’re tracking data on revenue in your ClickHouse database. Metrics about revenue might be served up to interested parties in a variety of places: BI tools, custom dashboards, API endpoints, agentic tools, MCP servers, AI chat, etc. Are the numbers the same in every place? Maybe, maybe not. When the same metric is re\-defined in multiple locations (or generated on the fly by an LLM), it's easy for that definition to skew. It happens more often than you might think.

The below example is based on something we saw at one of our customers: their custom chat client vibe\-SQLed a definition of revenue that made sense (sum of `amount`), but didn’t exclude transactions that were incomplete (Figure A: chat overstates revenue). That kind of mistake becomes impossible with a well\-defined metrics layer (Figure B: chat matches actual revenue).

Previous slide\<\-Next slide\-\>![](/_next/image?url=%2Fuploads%2F1_cdd0a13188.png&w=3840&q=75)![](/_next/image?url=%2Fuploads%2F2_0e4864ac05.png&w=3840&q=75)![](/_next/image?url=%2Fuploads%2F1_cdd0a13188.png&w=384&q=75)![](/_next/image?url=%2Fuploads%2F2_0e4864ac05.png&w=384&q=75)*Image 1 shows chat going rogue on the definition of revenue. Image 2 shows how the metrics layer keeps everything consistent.*

When I was at Nike, we had to work hard to make sure this didn’t happen just across our APIs. Now, there’s APIs, dashboard, chats and AI, MCP… The surface area for inconsistency has multiplied.

And what happens when we need to change that definition? We end up with two problems:

1. Metrics need to be consistent everywhere. Same definition, same answer, across chat, APIs, dashboards, and MCP. One mistake kills credibility.
2. Metrics need to be easy to define and change safely. Add a metric once, update it once, and have every surface stay in sync when the schema changes. The developer experience needs to be better than manually crafting all this.
