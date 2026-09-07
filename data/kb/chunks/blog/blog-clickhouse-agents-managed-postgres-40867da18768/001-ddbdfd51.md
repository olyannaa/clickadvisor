---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-agents-is-now-available-for-managed-postgres-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 5
---

# ClickHouse Agents is now available for Managed Postgres \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"ClickHouse Agents is now available for Managed Postgres","description":"ClickHouse Agents now connects directly to Managed Postgres, so you can query your operational data in plain English, combine it with ClickHouse in a single request, and get agent\-guided help monitoring, tuning, and migrating your databases.","image":"/uploads/image1\_a3e34189e4\.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-07\-03T08:58:08\.210Z","dateModified":"2026\-07\-03T08:58:08\.111Z","author":{"@context":"https://schema.org","@type":"Person","name":"Amog Iska","url":"https://clickhouse.com/authors/amog\-iska","@id":"https://clickhouse.com/authors/amog\-iska\#person","image":"/uploads/Image\_512x512\_12\_b64458e23d.jpeg","jobTitle":"Software Engineer at ClickHouse"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# ClickHouse Agents is now available for Managed Postgres

![image 512x512 12](/_next/image?url=%2Fuploads%2FImage_512x512_12_b64458e23d.jpeg&w=96&q=75)[Amog Iska](/authors/amog-iska)Jul 2, 2026 · 7 minutes read![image1.png](/_next/image?url=%2Fuploads%2Fimage1_a3e34189e4.png&w=2048&q=75)

## TL;DR: \#

[ClickHouse Agents](https://clickhouse.com/blog/clickhouse-agents-beta) is now available for **Managed Postgres** by ClickHouse. You can explore your Postgres data in plain English, query Postgres and ClickHouse together, and build agents that monitor, tune, and even help migrate your databases. All read\-only by default and secure by design.

ClickHouse Agents, [launched in beta during OpenHouse](https://clickhouse.com/blog/clickhouse-agents-beta) in June 2026, is a fully managed agentic service in ClickHouse Cloud, powered by Claude. You can build agents with no code, grounded in your live data, and ask questions in plain English instead of writing SQL or wiring up tools. Teams use it for everything from self\-serve data exploration to query performance analysis, getting from a question to an answer in seconds.

Under the hood it pairs an agent builder and chat interface with a sandboxed code interpreter. It's built on an open stack: connect to any MCP\-compatible system and bring your own agents, models, and tools, with ClickHouse Cloud as the data foundation and no vendor lock\-in. It's built on [LibreChat](https://clickhouse.com/blog/clickhouse-acquires-librechat), the open\-source AI chat platform that joined ClickHouse through a strategic acquisition and is trusted at scale by companies like [Coinbase](https://x.com/brian_armstrong/status/2070670644577280109) and Shopify.

With this release, that same agentic experience extends to all Managed Postgres services in ClickHouse Cloud. Now devs can query Postgres and ClickHouse together through an agentic interface, aligning with our vision of offering a unified data stack for OLTP and OLAP.

## **Demo** \#
