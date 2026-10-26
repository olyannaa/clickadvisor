---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"The
topic: the-agentic-analytics-benchmark-measuring-model-accuracy-and-efficiency-in-analytical-agents-clickhouse
ch_version_introduced: auto
last_updated: '2026-10-26'
chunk_index: 14
total_chunks_in_doc: 16
---

The choice is not simply frontier vs. frontier, nor frontier vs. mid\-tier. You need to assess what level of correctness is tolerable for your use case, and what you are willing to pay for the last few points.

Further, failure\-mode analysis points at where performance could be supported outside of the model. Wrong plan is the most common failure for every model, at 53 to 82% of failures, and the cheap models are not meaningfully worse at the rest of the job. If the plan is the universal bottleneck, then buying a good plan and executing it cheaply is the obvious architecture: put the strongest model where the plan is made, and let a low\-cost model execute it.

We have not benchmarked split\-role architectures yet. It is the follow\-up we are most interested in: can we close enough of the gap that a model at one\-fiftieth of the cost becomes the production default?

## Run this on your own data warehouse \#

[data\-agent\-mnist](https://github.com/ClickHouse/data-agent-mnist) is not intended to be a fixed score for today's models, nor is it tied to usage of ClickHouse. It’s a reusable harness that can be used by anyone to benchmark models against their own environment.

The harness includes an instrumented assistant (any tracing that captures the question, the SQL it ran, and the results), a modeled warehouse schema, and API access to a handful of frontier models for annotation and judging.

There are multiple stages to reproducing the benchmark for yourself, as discussed in this post: mine and curate the traffic; anonymize with hard\-fail verification; reconstruct the schema synthetically and plant every entity the questions reference; recover ground truth by provider\-diverse committee; score with a judge panel that never grades its own family. Each stage is a script, and a full evaluation replays from a single command against a deterministic warehouse.
