---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Building
topic: building-a-unified-data-platform-with-clickhouse-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 8
---

# Building a Unified Data Platform with ClickHouse \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"Building a Unified Data Platform with ClickHouse","description":"Read how Synq effectively built a unified data platform leveraging the power of ClickHouse, accomplishing a seamless integration of both operational and analytical use cases.","image":"/uploads/Synq\_banner\_a5fa263a4a.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2023\-07\-28T09:21:43\.884Z","dateModified":"2026\-03\-03T12:30:05\.570Z","author":{"@context":"https://schema.org","@type":"Person","name":"Petr Janda, founder of Synq"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# Building a Unified Data Platform with ClickHouse

![synq 128](/_next/image?url=%2Fuploads%2FSynq_128_d2a31debe1.png&w=96&q=75)Petr Janda, founder of SynqJul 28, 2023 · 13 minutes read
  

*We're excited to introduce Petr Janda, the founder of Synq who recently spoke at the ClickHouse Meetup in London on May 25th, 2023\. In his talk, Petr delved into the process of building user\-facing and internal applications with ClickHouse.*

*Now, as a guest contributor, Petr extends on his talk in this comprehensive blog post. Read how his team at Synq built a unified data platform with ClickHouse, skillfully merging operational and analytical needs.*

Data powers every software system.

Its complexity, variety, dramatically increasing volumes, and demanding use cases spawned the development of specialized data systems—some focused on low latency operational use cases, others on analytical queries spanning large\-scale datasets. As a result, technology stacks often split into analytical and operational systems that develop separately.

Analytical systems have evolved rapidly in the last decade—from Hadoop to cloud products like Redshift and later Snowflake or BigQuery. But despite their ability to elastically scale and process nearly unlimited amounts of data (as long as you have enough dollars to pay the bill), they were not designed for typical operational use cases with low latency requirements.

But does it have to be this way? What would our systems look like if we built both operational and analytical use cases around a unified data platform?

We thought hard about these questions as we started Synq a year ago. Fast forward to today, we power our entire user\-facing application, our internal analytics, data reliability monitoring alerts, in\-application analytics, and machine learning models that train on a continuous stream of data from a single data platform—ClickHouse.

## Finding the *Right* Platform \#
