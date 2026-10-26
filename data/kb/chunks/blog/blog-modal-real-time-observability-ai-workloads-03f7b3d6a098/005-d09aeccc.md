---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-modal-uses-clickhouse-to-power-real-time-observability-for-ai-workloads-clickhouse
ch_version_introduced: auto
last_updated: '2026-10-26'
chunk_index: 5
total_chunks_in_doc: 6
---

latency percentile metrics are calculated directly in ClickHouse. For queue time, Modal subtracts enqueued\_at from started\_at, and then uses aggregate functions like [avg](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/avg) and [quantile](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/quantile) to calculate P50, P90, and P99 values. ## Scaling up—and looking ahead \#

Near the end of his talk, Ro showed a slide with some impressive numbers—19 TB of events ingested, 1 million events per minute, a P90 of \~420 milliseconds—but he had to revise that on the fly. “I actually checked today and it's 2 million events per minute,” he clarified. “So we're growing pretty fast.”

Even as usage scales, Modal has kept things simple. “We don’t use [indexes](https://clickhouse.com/docs/guides/best-practices/sparse-primary-indexes) or [projections](https://clickhouse.com/docs/sql-reference/statements/alter/projection) or [materialized views](https://clickhouse.com/docs/materialized-views),” Ro says. “Now we’re starting to optimize things to get better latency for our customers. And there are certain edge cases that we want to improve.”

Looking ahead, the team is exploring several new features and improvements. As Ro explains, these include a billing API that lets users answer questions like, “For this function, on this day, for this range of function calls—how much did that cost me?” They’re also building a visual function call graph, enhancing support for batched jobs, and continuing to improve performance for real\-time queries.

“We’re focused on making it super easy for customers to understand how their code is running in the cloud,” Ro says. With ClickHouse Cloud, they’re well\-positioned to do just that.

### Get started with ClickStack

Discover the world’s fastest and most scalable open source observability stack, in seconds.

[Try now](https://clickhouse.com/o11y?loc=blog-cta-1424-get-started-with-clickstack-try-now&utm_blogctaid=1424)### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-global-cta&utm_blogctaid=0)

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

[View all Blogs](/blog)![shipsidekick oct2026 banner yellow](/_next/image?url=%2Fuploads%2Fshipsidekick_oct2026_banner_yellow_da09e5fd13.png&w=750&q=75)User stories### [How Shipsidekick replaced Neon with ClickHouse Managed Postgres for 10x faster queries and better reliability](/blog/shipsidekick-neon-to-clickhouse-managed-postgres)

ClickHouse · Oct 23, 2026![langfuse cursor oct2026 banner](/_next/image?url=%2Fuploads%2Flangfuse_cursor_oct2026_banner_be7806b3ee.png&w=750&q=75)Product### [Trace and evaluate Cursor agents with Langfuse, powered by ClickHouse](/blog/cursor-agents-with-langfuse)
