---
source: blog
url: https://mp.weixin.qq.com/s/GSvo-7xUoVzCsuUvlLTpCw
topic: august-2024-newsletter
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 4
---

# August 2024 newsletter

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# August 2024 newsletter

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Aug 22, 2024 · 5 minutes readWelcome to the August ClickHouse newsletter, which will round up what’s happened in real\-time data warehouses over the last month.

This month, we have exciting news about PeerDB joining ClickHouse, downsampling time series data, join performance improvements in the 24\.7 release, and more!

## Alexey, ClickHouse creator and CTO, goes on tour! [\#](/blog/202408-newsletter#alexey-clickhouse-creator-and-cto-goes-on-tour)

![Banner Alexey the rockstar.png](/uploads/Banner_Alexey_the_rockstar_ea3688418f.png)
We are excited to share that **Alexey Milovidov, creator and CTO of ClickHouse**, will be delivering a series of technical talks around the world. Please join these events in person to hear him speak and a chance to ask him ANY question about ClickHouse! Space is limited, register below:

- Sun, Aug 25 \- China Meetup, Guangzhou \- [Register](https://mp.weixin.qq.com/s/GSvo-7xUoVzCsuUvlLTpCw)
- Tues, Aug 27 \- VLDB Talk, Guangzhou \- [Schedule](https://vldb.org/2024/?program-schedule)
- Thur, Sept 5 \- San Francisco Meetup (Cloudflare) \- [Register](https://www.meetup.com/clickhouse-silicon-valley-meetup-group/events/302540575)
- Mon, Sept 9 \- Raleigh Meetup (Deutsche Bank) \- [Register](https://www.meetup.com/clickhouse-nc-meetup-group/events/302557230)
- Tues, Sept 10 \- New York Meetup (Rokt) \- [Register](https://www.meetup.com/clickhouse-new-york-user-group/events/302575342)
- Thur, Sept 12 \- Chicago Fireside Chat (Jump Capital) \- [Register](https://lu.ma/43tvmrfw)
- Wed, Sept 18 \- Warsaw AWS Cloud Day \- [Register](https://aws.amazon.com/events/cloud-days/warsaw/)

## Inside this issue [\#](/blog/202408-newsletter#inside-this-issue)

- [Featured community member: Chase Richards](https://clickhouse.com/blog/202408-newsletter#featured-community-member-chase-richards)
- [Upcoming events](https://clickhouse.com/blog/202408-newsletter#upcoming-events)
- [ClickHouse welcomes PeerDB](https://clickhouse.com/blog/202408-newsletter#clickhouse-welcomes-peerdb)
- [Downsampling time series data](https://clickhouse.com/blog/202408-newsletter#downsampling-time-series-data)
- [24\.7 release](https://clickhouse.com/blog/202408-newsletter#247-release)
- [How Maxilect transferred ClickHouse between geographically distant data centers](https://clickhouse.com/blog/202408-newsletter#how-maxilect-transferred-clickhouse-between-geographically-distant-data-centers)
- [Java Client… the SEQUEL?!](https://clickhouse.com/blog/202408-newsletter#java-client-the-sequel)
- [Quick reads](https://clickhouse.com/blog/202408-newsletter#quick-reads)
- [Post of the month](https://clickhouse.com/blog/202408-newsletter#post-of-the-month)

## Featured community member: Chase Richards [\#](/blog/202408-newsletter#featured-community-member-chase-richards)

This month's featured community member is Chase Richards, VP of Engineering at Corsearch.

![202408-featured.png](/uploads/202408_featured_697afc61da.png)
Chase Richards previously led engineering efforts at Marketly from a 2011 start\-up through its acquisition in 2020 by Corsearch.

Chase recently [presented at the Bellevue meetup](/videos/how-corsearch-uses-clickhouse-today) about his experience replacing MySQL with ClickHouse as the backing database for a client\-facing report interface for their search engine protection service. Having done this in 2018, Chase earned his status as a trailblazer in the community.
