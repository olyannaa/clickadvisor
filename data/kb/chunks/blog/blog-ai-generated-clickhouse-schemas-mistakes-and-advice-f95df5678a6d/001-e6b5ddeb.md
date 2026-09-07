---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"AI
topic: ai-doesn-t-always-generate-perfect-clickhouse-schemas-yet-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 8
---

# AI doesn’t always generate perfect ClickHouse schemas (yet) \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"AI doesn’t always generate perfect ClickHouse schemas (yet)","description":"This post walks through the common pitfalls we see when AI generates ClickHouse schemas, drawn from real conversations with our Solutions Architecture team and patterns across dozens of customer engagements.","image":"/uploads/aipitfallsbanner\_fe9a5242e1\.jpg","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-03\-08T19:36:27\.874Z","dateModified":"2026\-03\-13T11:05:03\.108Z","author":{"@context":"https://schema.org","@type":"Person","name":"Al Brown","url":"https://clickhouse.com/authors/al\-brown","@id":"https://clickhouse.com/authors/al\-brown\#person","image":"/uploads/al\_brown\_headshot\_09ae0cbce6\.jpg","jobTitle":"Product Marketing Engineer at ClickHouse"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# AI doesn’t always generate perfect ClickHouse schemas (yet)

![Al Brown](/_next/image?url=%2Fuploads%2Fal_brown_headshot_09ae0cbce6.jpg&w=96&q=75)[Al Brown](/authors/al-brown)Mar 13, 2026 · 13 minutes readAsk any LLM to design a ClickHouse table for real\-time event analytics and you'll often get something like this:

```
1CREATE TABLE events
2(
3    event_id UUID,
4    user_id UInt64 CODEC(Delta, ZSTD(3)),
5    event_type LowCardinality(String),
6    timestamp DateTime64(3) CODEC(DoubleDelta, ZSTD(1)),
7    properties JSON,
8    session_id String CODEC(ZSTD(3)),
9    page_url String CODEC(ZSTD(5)),
10    duration_ms UInt32 CODEC(T64, ZSTD(3))
11)
12ENGINE = ReplacingMergeTree(timestamp)
13PARTITION BY toYYYYMM(timestamp)
14ORDER BY (event_type, user_id, timestamp)
15SETTINGS index_granularity = 4096
16
17-- Projection for user-level queries
18ALTER TABLE events ADD PROJECTION user_events
19(
20    SELECT * ORDER BY (user_id, timestamp)
21);
```
Copy command
This looks reasonable at first glance. It's syntactically correct. It uses ClickHouse\-specific features. You *could* drop this straight into production.

But there are many choices in this schema that might not be right for you:

- **Custom partitioning**. This is the single most common giveaway of an AI\-generated schema. Partitioning in ClickHouse is primarily a data management feature, not a query optimization feature.
- **Custom codecs on every column**. ClickHouse's default compression is already excellent, and ideal for most users. Column\-level codec tuning is something to do when you know you really need it.
- **A projection duplicating most of the table**. Projections are a powerful feature, but they come with real costs at scale that we'll cover later. Adding one from day one, before you've even seen production query patterns, is classic over\-optimization.
