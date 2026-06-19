---
source: blog
url: https://www.luzmo.com/product/embedded-analytics
topic: building-a-user-facing-dashboard-with-clickhouse-and-luzmo
ch_version_introduced: '5.1'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 8
---

# Building A User\-Facing Dashboard With ClickHouse and Luzmo

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Building A User\-Facing Dashboard With ClickHouse and Luzmo

![](/_next/image?url=%2Fuploads%2Fluzmo_684f03b8a8.png&w=96&q=75)[Luzmo](/authors/luzmo)Jul 17, 2024 · 16 minutes read## Introduction [\#](/blog/building-user-facing-dashboards-with-clickhouse-and-luzmo#introduction)

Modern businesses no longer make decisions based on gut\-feel. In every software or app we use \- even consumer apps like FitBit, Strava, or banking apps \- we expect some sort of dashboard or charts to help us guide our daily decisions.

However, as a software developer, building these user\-facing dashboards can be a frustrating and time\-consuming process. And that’s mostly because of two reasons:

1. It costs a lot of time, expertise and development resources to develop data visualizations and advanced analytics capabilities from scratch.
2. Many SaaS apps rely on a relational database, which isn’t optimal as a data infrastructure for user\-facing analytics. As a result, dashboards load very slowly, hurting your user experience.
3. In this article, you’ll learn how you can overcome both obstacles, using ClickHouse as your analytical database and Luzmo for [embedded data visualizations](https://www.luzmo.com/product/embedded-analytics). In a quick tutorial, we’ll show you how to build the following [user\-facing dashboard](https://app.luzmo.com/s/clickhouse-demo-uk-home-prices-16cn64omlx7s38hr) in just a few minutes that you can embed into your own application!

[![](/uploads/1_clickhouse_dashboard_62a3969883.png)](https://app.luzmo.com/s/clickhouse-demo-uk-home-prices-16cn64omlx7s38hr)

## Why you need an analytical data model for user\-facing analytics [\#](/blog/building-user-facing-dashboards-with-clickhouse-and-luzmo#why-you-need-an-analytical-data-model-for-user-facing-analytics)

Most SaaS companies already use an operational database to run and store their SaaS platform’s transactions. So it’s tempting to think: "Why do I need another database if all our data is already stored in one?"

Unfortunately, using a relational model for analytics can quickly become problematic. Every transaction is stored in a single row, so even when you only need a small subset of information from one or two columns, your database needs to scan entire rows to retrieve it. Queries are slow because they need to process so much data. On top of that, you risk putting too much load on your operational systems, causing downtime for your entire platform.
