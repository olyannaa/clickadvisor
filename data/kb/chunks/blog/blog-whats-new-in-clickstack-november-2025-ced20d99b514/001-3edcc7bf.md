---
source: blog
url: https://github.com/jwhitaker-gridcog)**
topic: what-s-new-in-clickstack-november-25
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 6
---

# What's new in ClickStack. November '25\.

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# What's new in ClickStack. November '25\.

![](/_next/image?url=%2Fuploads%2Fmike_shi_5b7145e7d7.jpg&w=96&q=75)[Mike Shi](/authors/mike-shi)Dec 4, 2025 · 9 minutes readWelcome to the November edition of What’s New in ClickStack, the open\-source observability stack built for ClickHouse. Each month, we highlight new ClickHouse features and HyperDX UI improvements that work together to make observability faster, easier to use, and more capable than ever.

This release introduces Service Maps, integration with incident.io, root span filtering, searching within traces, line chart comparisons, and new controls for highlighting specific attributes.

## New contributors [\#](/blog/whats-new-in-clickstack-november-2025#new-contributors)

Building an open\-source observability stack is a team sport \- and our community makes it possible. A big thank you to this month's new contributors! Every contribution, big or small, helps make ClickStack better for everyone.

**[jwhitaker\-gridcog](https://github.com/jwhitaker-gridcog)**
**[alok87](https://github.com/alok87)** 
**[hiasr](https://github.com/hiasr)**
**[dhtclk](https://github.com/dhtclk)**
**[beefancohen](https://github.com/beefancohen)**

## Service Maps [\#](/blog/whats-new-in-clickstack-november-2025#service-maps)

Service Maps are now available in beta, bringing one of the most requested features in ClickStack to life. Service Maps give teams a high\-level view of how their services interact, showing the flow of requests between components and surfacing traffic patterns and failures. They help turn raw traces into an intuitive picture of system behavior, making it easier to understand dependencies and spot issues across distributed architectures.

![image10.png](/uploads/image10_c88d9a0ffc.png)
In ClickStack, we always prefer to present features in context rather than just as isolated screens, so you’ll find Service Maps integrated throughout the ClickStack experience. Although on the left panel you can explore your full service graph to see how everything connects, you’ll also encounter Service Maps in other contexts \- for example, when viewing an individual trace. Next to the columns in the trace waterfall, a focused map appears, showing how that specific request moved between services, giving you a visual representation of the path without breaking your investigative flow.
