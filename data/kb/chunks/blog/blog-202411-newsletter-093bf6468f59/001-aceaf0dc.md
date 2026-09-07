---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"November
topic: november-2024-newsletter-clickhouse
ch_version_introduced: '24.10'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 5
---

# November 2024 newsletter \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"November 2024 newsletter","description":"Welcome to the November ClickHouse newsletter, which will round up what’s happened in real\-time data warehouses over the last month.","image":"/uploads/newsletter2410\_8160351726\.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2024\-11\-21T14:08:25\.678Z","dateModified":"2026\-03\-03T12:38:18\.155Z","author":{"@context":"https://schema.org","@type":"Person","name":"ClickHouse","url":"https://clickhouse.com/authors/clickhouse","@id":"https://clickhouse.com/authors/clickhouse\#person","image":"/uploads/neutral\_avatar\_400804ae96\_5c370e757b.png"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# November 2024 newsletter

![neutral avatar 400804ae96](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Nov 21, 2024 · 7 minutes readWelcome to the November ClickHouse newsletter, which will round up what’s happened in real\-time data warehouses over the last month.

The big news is that Refreshable Materialized Views are production\-ready, and we have an official Docker image!

Alexey Milovidov was a guest on Data Talks on the Rocks, we learn how to simplify queries with dictionaries, and there’s a deep dive on the new JSON data type.

## Inside this issue \#

- [Featured community member](https://clickhouse.com/blog/202411-newsletter#featured-community-member)
- [Upcoming events](https://clickhouse.com/blog/202411-newsletter#upcoming-events)
- [24\.10 Release](https://clickhouse.com/blog/202411-newsletter#2410-release)
- [Alexey Milovidov on Data Talks on the Rocks](https://clickhouse.com/blog/202411-newsletter#alexey-milovidov-on-data-talks-on-the-rocks)
- [Simplifying queries with ClickHouse dictionaries](https://clickhouse.com/blog/202411-newsletter#simplifying-queries-with-clickhouse-dictionaries)
- [Building a financial data pipeline with Alpha Vantage and ClickHouse](https://clickhouse.com/blog/202411-newsletter#building-a-financial-data-pipeline-with-alpha-vantage-and-clickhouse)
- [How we built a new powerful JSON data type for ClickHouse](https://clickhouse.com/blog/202411-newsletter#how-we-built-a-new-powerful-json-data-type-for-clickhouse)
- [ClickHouse Cloud Live Update: November 2024](https://clickhouse.com/blog/202411-newsletter#clickhouse-cloud-live-update-november-2024)
- [Quick reads](https://clickhouse.com/blog/202411-newsletter#quick-reads)
- [Post of the month](https://clickhouse.com/blog/202411-newsletter#post-of-the-month)

## Visit us at AWS re:Invent \#

![aws-reinvent-202411.png](/_next/image?url=%2Fuploads%2Faws_reinvent_202411_0edd3daa88.png&w=2048&q=75)

Are you heading to re:Invent? We are too, and would love to connect with you!

Book a meeting with us beforehand by emailing sales@clickhouse.com, or stop by our booth \#1737 for:

- A chance to meet all three of [our founders](https://clickhouse.com/company/our-story): Aaron, Alexey, and Yury
- Live demos
- Exclusive swag
- And a chat with ClickHouse experts

Don’t miss out – we’re also hosting a ClickHouse House Party with the Chainsmokers. It’ll be one epic night you won’t want to miss! 

![house-party-202411.png](/_next/image?url=%2Fuploads%2Fhouse_party_202411_ba778b3256.png&w=2048&q=75)

[Register for the Chainsmokers party](https://clickhouse.com/houseparty/vegas-2024)

## Featured community member \#

This month's featured community member is Lukas Biewald, co\-founder and CEO at [Weights \& Biases](https://wandb.ai?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter).

![featured-202411.png](/_next/image?url=%2Fuploads%2Ffeatured_202411_c82ec62b60.png&w=2048&q=75)

Lukas has worked in machine learning for 20 years, previously co\-founding Figure Eight with Chris Van Pelt, where they specialized in data labeling for machine learning applications. Appen acquired the company in March 2019\.
