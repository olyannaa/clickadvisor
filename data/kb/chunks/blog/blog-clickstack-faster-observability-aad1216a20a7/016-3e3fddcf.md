---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-clickstack-makes-clickhouse-faster-for-observability-clickhouse
ch_version_introduced: '0.01'
last_updated: '2026-09-07'
chunk_index: 16
total_chunks_in_doc: 16
---

high\-level functions. This approach has several benefits. It allows developers to embed ClickStack directly into their own observability workflows and applications without needing deep ClickHouse expertise. It also provides a more reliable interface for automation and AI\-driven analysis.

Our recently introduced **[Notebooks experience](/blog/clickstack-ai-notebooks)**, currently in private preview, already uses these internal tools. Instead of relying on an LLM to generate complex SQL queries, notebooks call specialized endpoints designed for specific analytical tasks. These endpoints encapsulate the best query strategies for ClickStack, delivering better performance and more predictable results. In practice, this also improves reliability, since large language models are not yet well suited to consistently producing highly optimized ClickHouse SQL.

Over time, we plan to make these tools publicly accessible. External applications will be able to call them directly, or connect through protocols such as **Model Context Protocol (MCP)** to power AI\-driven observability experiences. This will allow developers to build custom tools, assistants, and workflows that inherit the same performance characteristics as the ClickStack interface.

This is an ongoing journey. It involves defining the right abstractions, building stable APIs, and introducing authentication and access controls. But the goal is clear: make the performance benefits of ClickStack available everywhere, enabling anyone to build fast, scalable observability solutions on top of ClickHouse.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-109-get-started-today-sign-up&utm_blogctaid=109)

---

Share this post

- Copy URL
- [![Y Combinator icon](/_next/static/immutable/media/ycombinator.37q2g-no9bowl.svg)](https://news.ycombinator.com/submitlink?u= "Share on Y Combinator")
- [![X icon](/_next/static/immutable/media/x.3nm91lx52ia7n.svg)](https://x.com/intent/tweet?text= "Share on X")
- [![Bluesky icon](/_next/static/immutable/media/bluesky.292c8t8kns7n1.svg)](https://bsky.app/intent/compose?text= "Share on Bluesky")
- [![Facebook icon](/_next/static/immutable/media/facebook.32ysyflv7kktz.svg)](https://www.facebook.com/sharer/sharer.php?u= "Share on Facebook")
- [![LinkedIn icon](/_next/static/immutable/media/linkedin.37911rnwi-sdg.svg)](https://www.linkedin.com/sharing/share-offsite/?url= "Share on LinkedIn")
### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!

## Recent posts

[View all Blogs](/blog)![clickhouse streaming http api](/_next/image?url=%2Fuploads%2FClick_House_Streaming_HTTP_API_7d6978a509.jpg&w=750&q=75)Product### [ClickHouse as a streaming HTTP API](/blog/clickhouse-streaming-http-api)

Mark Needham · Sep 5, 2026![dsn 1310 pipelined sql in clickhouse 26 8](/_next/image?url=%2Fuploads%2FDSN_1310_Pipelined_SQL_in_Click_House_26_8_96921fe4d8.jpg&w=750&q=75)Engineering### [Pipelined SQL in ClickHouse 26\.8](/blog/pipelined-sql-26.8)

Mark Needham · Sep 4, 2026![scheduled upgrades sep2026 banner](/_next/image?url=%2Fuploads%2Fscheduled_upgrades_sep2026_banner_b3cca8371f.jpg&w=750&q=75)Product### [Introducing Scheduled Upgrades in ClickHouse Managed Postgres](/blog/introducing-scheduled-upgrades-in-clickhouse-managed-postgres)

ClickHouse · Sep 3, 2026![blog banner from neon to clickhouse](/_next/image?url=%2Fuploads%2FBlog_Banner_From_Neon_to_Click_House_3ba00e031d.jpg&w=750&q=75)User stories### [From Neon Postgres to ClickHouse Managed Postgres](/blog/neon-to-clickhouse-managed-postgres)

Sai Srirampur · Sep 2, 2026[View all Blogs](/blog)
