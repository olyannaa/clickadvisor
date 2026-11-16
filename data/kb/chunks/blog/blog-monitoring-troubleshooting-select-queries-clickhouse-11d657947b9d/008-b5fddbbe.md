---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Essential
topic: essential-monitoring-queries-part-2-select-queries-clickhouse
ch_version_introduced: '22.13'
last_updated: '2026-11-16'
chunk_index: 8
total_chunks_in_doc: 9
---

BY time_delta DESC ``` ![TOO_MANY_SIMULTANEOUS_QUERIES.png](/_next/image?url=%2Fuploads%2FTOO_MANY_SIMULTANEOUS_QUERIES_ea790eddd2.png&w=2048&q=75) While all of the queries in my cluster have completed in less than a second, this should be reviewed carefully if your ClickHouse service has a large and heavy number of SELECT queries.

If you identified queries that are stuck or failed in the previous query, you can review the `system.stack_trace` table to get more details on the cause with a full stack trace. This information is useful for troubleshooting.

```

SELECT
    thread_id,
    query_id,
    arrayStringConcat(arrayMap((x, y) -> concat(x, ': ', y), arrayMap(x -> addressToLine(x), trace), arrayMap(x -> demangle(addressToSymbol(x)), trace)), '\n') AS n_trace
FROM clusterAllReplicas(default, system.stack_trace)
WHERE query_id IS NOT NULL
SETTINGS allow_introspection_functions = 1


```

![query_stack_trace.png](/_next/image?url=%2Fuploads%2Fquery_stack_trace_d34db7cc9b.png&w=2048&q=75)

When using the ClickHouse SQL\-console, you can double click on each cell to get the full context via an inspector.

## Conclusion \#

In this blog post, we have reviewed different ways to troubleshoot and understand how SELECT queries are behaving in ClickHouse as well as providing the methods to help you to review your improvements and changes. We recommend proactively monitoring the results of these queries and alerting if the behavior is usual, potentially using tools such as Grafana, which has a mature ClickHouse integration and supports alerting. In the next post from this series, we will review queries to monitor and troubleshoot a distributed ClickHouse deployment.

### Get started today

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
