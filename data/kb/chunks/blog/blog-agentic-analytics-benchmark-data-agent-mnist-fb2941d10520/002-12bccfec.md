---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"The
topic: the-agentic-analytics-benchmark-measuring-model-accuracy-and-efficiency-in-analytical-agents-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 2
total_chunks_in_doc: 14
---

generally proclaim a model as the overall winner, appropriate for anyone. But for agentic analytics, the criteria of the best model is a lot more context\-dependent. We believe most recent models are generally more capable in this area.

While writing this post, Hex released [DataBench](https://hex.tech/blog/databench-agentic-analytics-benchmark/), which aligns very closely with how we see agentic analytics. We highly recommend giving their post a read.

This benchmark aims to not just be a point\-in\-time snapshot of current model capabilities, but a framework that can be used to benchmark model performance against your own data warehouse, and assess which is appropriate for you.

This post explains how we built it, what we found, and how you can build the same thing from your own data warehouse traffic.

![Figure 1](/_next/image?url=%2Fuploads%2Fpass_rate_all_models_1910c0d6a2.png&w=2048&q=75)

*Pass Rate of all 28 models. No mid\- or small\-tier model reaches the top eleven, frontier tier alone does not guarantee it, and an open\-weights model leads.*

[Skip to the results.](#results)

## Agentic analytics vs. text\-to\-SQL \#

Text\-to\-SQL is the translation of a natural\-language question into a single SQL query, given the schema. It is one of the most heavily benchmarked tasks in NLP, and a decade of those benchmarks rests on four shared assumptions:

1. the schema is handed to it up front
2. the model gets one shot
3. there is a single gold query
4. scoring is an execution match against that gold quey

However, agentic analytics drastically challenge the assumptions here in real world use cases. The agent must still turn a natural\-language question into SQL, but the other three assumptions go: it discovers the schema itself, it takes as many turns as it needs, and there is no gold query to match, because the answer is the result set the annotators agreed on.

Agents are able to explore and discover schemas on their own, build a plan, and run multiple queries to formulate an answer. This style of agentic analytics is now in production in many data platforms, including ClickHouse Cloud, and simple text\-to\-SQL is no longer representative of real work.

Benchmarking this loop tests some of the more opaque qualities of LLMs and needs a purpose\-built benchmark. Here are the three requirements we had when designing the benchmark:
