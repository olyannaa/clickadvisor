---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Whats
topic: whats-new-in-clickstack-june-july-clickhouse
ch_version_introduced: '0.0'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 12
---

# Whats new in ClickStack \- June \+ July \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"Whats new in ClickStack \- June \+ July","description":"Explore ClickStack’s latest upgrades, from richer trace navigation and Prometheus connectivity to smarter dashboards, quieter alerts, faster filtering and support for exponential histogram metrics.","image":"/uploads/Whats\_new\_Click\_Stack\_June\_July\_26\_8bbb59e8be.jpg","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-08\-10T17:53:42\.798Z","dateModified":"2026\-08\-10T17:53:42\.519Z","author":{"@context":"https://schema.org","@type":"Person","name":"The ClickStack Team","url":"https://clickhouse.com/authors/the\-clickstack\-team","@id":"https://clickhouse.com/authors/the\-clickstack\-team\#person","image":"/uploads/neutral\_avatar\_white\_add9f20d0f.png"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# Whats new in ClickStack \- June \+ July

![neutral avatar white](/_next/image?url=%2Fuploads%2Fneutral_avatar_white_add9f20d0f.png&w=96&q=75)[The ClickStack Team](/authors/the-clickstack-team)Aug 10, 2026 · 22 minutes readWelcome to the June–July edition of What’s New in ClickStack. We’ve bundled two releases into one update, so there’s a little more than usual to cover.

Much of the work in the last 2 months has focused on traces and came directly from user feedback. The waterfall now uses a separate color for each service. A new minimap keeps the shape of the full trace visible while you inspect one part of it, and OpenTelemetry span links appear in the span detail panel, letting you move between traces easily.

For metrics, we added quantile support for exponential histograms, introduced a leaner default schema, and enabled connections to external Prometheus\-compatible endpoints. This takes ClickStack beyond a single\-source observability experience and raises new possibilities for evaluating the TimeSeries Engine and migrating existing Prometheus workloads, which we explore below.

Dashboard filters can now narrow each other, similar to a faceted search. Event patterns are available as a dashboard tile type, and kiosk mode can lock dashboards into a read\-only view for wall displays.

We also changed how filter values are fetched. Autocomplete and filter dropdowns now use ClickHouse text indexes where available instead of scanning the source table.

## New contributors \#

Thank you to our open source contributors and to the users whose feedback shaped many of these features.

[Aryan Inguz](https://github.com/Aryainguz), [Marco Frömbgen](https://github.com/mfroembgen), [heyparth](https://github.com/heyparth1), [kumburovicbranko682\-boop](https://github.com/kumburovicbranko682-boop), [Rachit Mittal](https://github.com/rachit367), [Matt Kaye](https://github.com/mrkaye97), [zoov\-xavier](https://github.com/zoov-xavier), [tsushanth](https://github.com/tsushanth), [Saksham Goyal](https://github.com/Sakshamm-Goyal), [Prince Rawat](https://github.com/rawatprince), [Shuvam Kumar](https://github.com/shuvamk), [Minh Vu](https://github.com/fallintoplace), [Niladri Adhikary](https://github.com/niladrix719), [xob0t](https://github.com/xob0t)
