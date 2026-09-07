---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Observability
topic: observability-a-year-in-review-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 6
---

# Observability \- a year in review \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"Observability \- a year in review","description":"Mike Shi, Head of Observability at ClickHouse, reflects on a pivotal year building ClickStack and learning from users. From cardinality and trace\-first systems to OpenTelemetry and AI SRE, he shares what changed in 2025 and what matters next.","image":"/uploads/o11y\_year\_in\_review\_2757187123\.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-01\-07T10:32:02\.753Z","dateModified":"2026\-03\-03T12:31:11\.958Z","author":{"@context":"https://schema.org","@type":"Person","name":"Mike Shi","url":"https://clickhouse.com/authors/mike\-shi","@id":"https://clickhouse.com/authors/mike\-shi\#person","image":"/uploads/mike\_shi\_5b7145e7d7\.jpg"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# Observability \- a year in review

![mike shi](/_next/image?url=%2Fuploads%2Fmike_shi_5b7145e7d7.jpg&w=96&q=75)[Mike Shi](/authors/mike-shi)Jan 7, 2026 · 9 minutes read## Introduction \#

With the start of the new year, it feels like the right moment to pause and reflect on a year that was pivotal for observability at ClickHouse and for me personally. As Head of Product Management for Observability, my focus throughout 2025 was building ClickStack and working closely with customers, partners, and the broader community to rethink what scalable observability should look like.

In May 2025, we introduced ClickStack with a simple goal: make high\-performance observability on ClickHouse accessible to everyone. Until then, teams either built their own user interfaces on top of ClickHouse or relied on more generic visualization tools like Grafana. By pairing ClickHouse with the HyperDX UI, ClickStack removes that friction and allows teams to immediately benefit from ClickHouse’s compression and fast query execution optimized for logs, traces, and metrics.

For a detailed reflection on what 2025 looked like for ClickStack itself, [see our earlier blog](https://clickhouse.com/blog/clickstack-a-year-in-review-2025).

Here, I want to focus instead on a few broader observations about how the observability landscape shifted over the past year, shaped by my conversations with our users, time spent at conferences, and ongoing discussions across the observability community.

### Learn about ClickStack

Explore the ClickHouse\-powered open source observability stack built for OpenTelemetry at scale.

[Get started](https://clickhouse.com/use-cases/observability?loc=blog-cta-31-learn-about-clickstack-get-started&utm_blogctaid=31)## Volume and cardinality became the hard limits \#
