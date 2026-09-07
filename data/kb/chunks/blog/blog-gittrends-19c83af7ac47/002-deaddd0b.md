---
source: blog
url: 'https://schema.org","@type":"BlogPosting","headline":"GitTrends:'
topic: gittrends-a-google-trends-style-view-of-the-github-ecosystem-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 2
total_chunks_in_doc: 4
---

for open\-source technology. Compare `ClickHouse vs Druid` to see how two analytics databases have traded momentum over time, or track `Claude vs OpenAI` to watch the AI landscape shift in real developer conversations. ![gittrends-21.png](/_next/image?url=%2Fuploads%2Fgittrends_21_d1284e2bdc.png&w=2048&q=75) ### Identify Ecosystems \#

Identify the top repositories driving the conversation around any topic. Is ClickHouse discussed mostly in its own ecosystem, or is it bleeding into data engineering and observability projects? Is OpenAI mentioned across a broad range of repos while Claude is concentrated in a handful?

Knowing where a technology lives tells you as much as knowing how popular it is.

![gittrends-31.png](/_next/image?url=%2Fuploads%2Fgittrends_31_cca45cbdc2.png&w=2048&q=75)

### Drill into the Source \#

Move from a high\-level trend to the actual conversations behind it. Select any repository and explore its underlying activity: the most active contributors, and the most mentioned issues and PRs driving the trend.

![gittrends-41.png](/_next/image?url=%2Fuploads%2Fgittrends_41_81773597ae.png&w=2048&q=75)

## Full\-Text Search at Scale \#

GitTrends is built around a simple idea: search any term in real time, across nearly 10 billion GitHub events with no data transformation. Rather than querying pre\-computed answers, you index the raw text and search it directly at query time. That's the all promise behind the [new full\-text search feature](https://clickhouse.com/blog/full-text-search-ga-release) recently released in ClickHouse. [Simply build a text index on a text column](https://clickhouse.com/docs/engines/table-engines/mergetree-family/textindexes) and use full\-text search.

What makes ClickHouse particularly powerful here is that full\-text Search and aggregation live in the same engine. A single query can search raw text and aggregate results in one pass, with no joins across systems, no data movement, and no latency penalty. That combination is what makes the experience feel instant rather than just fast.

The GitHub events dataset, nearly 10 billion rows of issues, pull requests, and comments, is a deliberate stress test. GitTrends still delivers fast search across all of it.

To highlight the performance of the new full\-text search index, GitTrends includes a live query performance comparison. For any search, you can toggle between using full\-text Search, bloom filter and a full table scan and watch the difference play out in real time. 

It is the clearest demonstration of what the right index buys you at scale.

## Look under the hood \#

GitTrends is fully open and built to be explored at every layer.

### How is the data ingested? \#
