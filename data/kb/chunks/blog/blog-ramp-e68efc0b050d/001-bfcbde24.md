---
source: blog
url: "https://schema.org\",\"@type\":\"BlogPosting\",\"headline\":\"\u201CJust"
topic: just-olap-it-how-ramp-rebuilt-its-analytics-platform-on-clickhouse-cloud-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 5
---

# “Just OLAP it”: How Ramp rebuilt its analytics platform on ClickHouse Cloud \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"“Just OLAP it”: How Ramp rebuilt its analytics platform on ClickHouse Cloud","description":"Building a Postgres\-to\-Kafka\-to\-ClickHouse pipeline, enabling millisecond\-speed reporting across 50,000 customers.","image":"/uploads/Ramp\_User\_Story\_Issue\_1219\_55fe4f58e6\.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-01\-20T14:09:15\.236Z","dateModified":"2026\-03\-03T12:31:16\.130Z","author":{"@context":"https://schema.org","@type":"Person","name":"ClickHouse","url":"https://clickhouse.com/authors/clickhouse","@id":"https://clickhouse.com/authors/clickhouse\#person","image":"/uploads/neutral\_avatar\_400804ae96\_5c370e757b.png"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# “Just OLAP it”: How Ramp rebuilt its analytics platform on ClickHouse Cloud

![neutral avatar 400804ae96](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 20, 2026 · 7 minutes read## Summary

div.w\-full \+ p, 
pre \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

Ramp uses ClickHouse Cloud to power real\-time, customer\-facing analytics like AI\-powered spend insights and proactive budget controls. After struggling to support large enterprise customers, they migrated from Postgres to ClickHouse, turning 40\+ second queries into millisecond responses. They built a Postgres\-to\-Kafka\-to\-ClickHouse pipeline with denormalized enrichers, enabling millisecond\-speed reporting across 50,000 customers.

[Ramp](https://ramp.com/)’s engineers have a saying: “Just OLAP it.” It’s shorthand for what’s become second nature: whenever a route is slow or a dashboard starts to lag, they reach for ClickHouse.

“We’ve done this hundreds of times,” says Ryan Delgado, Director of Engineering and self\-proclaimed “ClickHouse enthusiast.” He leads Ramp’s data platform team, which is focused on building infrastructure and tools to help Ramp realize business value from their data. “We use ClickHouse a bunch. It’s been a game\-changer for us.”

Today, ClickHouse powers a wide range of customer\-facing analytics at Ramp, from AI\-powered spend insights to proactive budget controls. But two years ago, none of that existed.

Ryan joined us at our recent [Open House Roadshow in New York City](https://clickhouse.com/blog/open-house-roadshow-nyc-videos), where he shared how the team built a high\-performance OLAP platform on [ClickHouse Cloud](https://clickhouse.com/cloud), replacing Postgres bottlenecks with real\-time pipelines and helping Ramp scale its analytics.

## Ramp’s journey to ClickHouse Cloud \#

With more than 50,000 customers, Ramp offers a modern finance operations platform that helps businesses control spend, automate accounting, and manage vendors from a single place.

“Our goal is to enable companies to reduce spend, while at the same time automating away the tedium that’s historically existed with back\-office finance,” Ryan says.
