---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"chDB
topic: chdb-durable-layer-for-agent-memory-clickhouse
ch_version_introduced: '3.4'
last_updated: '2026-11-16'
chunk_index: 11
total_chunks_in_doc: 12
---

chDB 4\.4 ships the Python implementation with `chdb[durable]` for S3\-compatible storage, plus `chdb[durable-gcs]` and `chdb[durable-azure]` for native GCS and Azure Blob. Node, Go, and Rust now expose the same object layout and lifecycle through `chdb@3.4.0`, `chdb-go/v2@2.2.0`, and `chdb-rust@2.0.0`.

All of them build on the Durable V1 pieces in `chdb-core` 26\.7\.3: backup, restore, statement classification, `head.json`, WAL, checkpoints, CAS, lease behavior, error categories, and cross\-binding fixtures. An object written by one binding is meant to be recoverable by another binding that speaks the same contract.

For local\-first agent systems, the shape is simple: no database server, no PVC, no replication sidecar, and no remote call on every recall. The database stays embedded. The state survives the machine.

Agent memory may not need a larger context window as much as it needs a local analytical brain that can survive a move.

## Try it next \#

- Install `pip install "chdb[durable]"`, open a namespace on a bucket you own, and attach an existing chDB memory table to it.
- For a clearer runnable example, read the [durable\-agent\-memory cookbook recipe](https://github.com/chdb-io/cookbook/blob/main/durable-agent-memory/README.md).
- For the full Durable contract and implementation details, see [chdb durable docs](https://github.com/chdb-io/chdb/tree/main/docs/durable).
- If you have a use case, question, or design feedback, start a discussion in [chdb\-io/chdb](https://github.com/chdb-io/chdb/issues).
### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-2387-get-started-today-sign-up&utm_blogctaid=2387)### Get started today

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

[View all Blogs](/blog)![jsonbench is back](/_next/image?url=%2Fuploads%2FJSON_Bench_is_back_6ea1528bec.png&w=750&q=75)Engineering### [JSONBench is back, and ClickHouse still leads](/blog/jsonbench-is-back-clickhouse-still-leads)

Tom Schreiber and Mark Needham · Nov 16, 2026![infinitas oct2026 banner yellow](/_next/image?url=%2Fuploads%2Finfinitas_oct2026_banner_yellow_136951726e.png&w=750&q=75)User stories### [How Infinitas Learning uses ClickHouse Managed Postgres to process billions of events for 1\.6M unique learners](/blog/infinitas-learning-clickhouse-managed-postgres)

ClickHouse · Nov 16, 2026![introducing loom agent memory that keeps up with your code](/_next/image?url=%2Fuploads%2FIntroducing_Loom_agent_memory_that_keeps_up_with_your_code_d2c2c52e54.jpg&w=750&q=75)Product### [Introducing Loom: agent memory that keeps up with your code](/blog/introducing-loom-agent-memory-that-keeps-up-with-your-code)
