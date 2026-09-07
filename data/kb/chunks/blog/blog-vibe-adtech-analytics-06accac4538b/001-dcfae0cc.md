---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-vibe-co-handles-billions-of-ad-impressions-with-clickhouse-cloud-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 6
---

# How Vibe.co handles billions of ad impressions with ClickHouse Cloud \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"How Vibe.co handles billions of ad impressions with ClickHouse Cloud","description":"How Vibe.co scaled from 100 GB to 2 TB of Connected TV ad impression data without rearchitecting anything, by migrating from Postgres to ClickHouse Cloud.","image":"/uploads/Vibe\_Customer\_Story\_Cover\_4458a14374\.jpg","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-06\-25T13:30:44\.974Z","dateModified":"2026\-06\-25T13:30:44\.879Z","author":{"@context":"https://schema.org","@type":"Person","name":"ClickHouse","url":"https://clickhouse.com/authors/clickhouse","@id":"https://clickhouse.com/authors/clickhouse\#person","image":"/uploads/neutral\_avatar\_400804ae96\_5c370e757b.png"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# How Vibe.co handles billions of ad impressions with ClickHouse Cloud

![neutral avatar 400804ae96](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jun 25, 2026 · 9 minutes read## Summary

- [Vibe.co](http://Vibe.co), recently acquired by Walmart, uses ClickHouse Cloud to power real\-time campaign reporting for thousands of Connected TV (CTV) advertisers across billions of ad impressions.
- The team migrated from Postgres after outgrowing its pre\-aggregation architecture. The platform now serves 90\+% of client campaign reports in under 100ms, and has scaled from \~100 GB to over 2 TB without rearchitecting anything.
- They chose ClickHouse Cloud over self\-hosted for operational simplicity, team support, and predictable pricing with separation of storage and compute.
When you stream a show on your Connected TV (CTV), you might notice the ads, but you probably don't think much about how they got there. Behind every ad is a chain of decisions about who to reach, when, on which platform, and at what frequency. For large brands with dedicated media teams, navigating that world has always been complex but at least manageable. For everyone else, it was often out of reach entirely.

[Vibe.co](http://Vibe.co), recently acquired by Walmart, is an all\-in\-one platform with a mission of making CTV advertising accessible to any brand, of any size, in under five minutes. Its customers range from household names to small businesses running their first\-ever TV campaign. What unites them is access to premium streaming inventory through a self\-serve platform that feels familiar to anyone who has ever run a Google or Meta ad.
