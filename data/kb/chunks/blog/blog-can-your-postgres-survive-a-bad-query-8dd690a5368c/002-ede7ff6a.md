---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Can
topic: can-your-postgres-survive-a-bad-query-clickhouse
ch_version_introduced: '8.2'
last_updated: '2026-10-12'
chunk_index: 2
total_chunks_in_doc: 11
---

and a plan can have several such nodes at once. Hash\-based nodes get an additional budget multiplier on top from `hash_mem_multiplier`. The Postgres docs clearly state that actual memory use "could be many times the value of `work_mem`."

To demonstrate how tricky query tuning can be, let's consider a simple schema on a database with all default Postgres settings. Just two tables, powering a hypothetical LLM inference service:

```
1CREATE TABLE wm_api_keys (
2  api_key_id uuid         PRIMARY KEY,
3  tier       smallint     NOT NULL,
4  scopes     text[]       NOT NULL,
5  expires_at timestamptz,
6  created_at timestamptz  NOT NULL
7);
8
9CREATE TABLE wm_api_calls (
10  call_id     bigint         PRIMARY KEY,
11  api_key_id  uuid           NOT NULL,
12  called_at   timestamptz    NOT NULL,
13  model_id    smallint       NOT NULL,
14  tokens      integer        NOT NULL,
15  cost_usd    numeric(10,6)  NOT NULL,
16  latency_ms  integer        NOT NULL
17);
```
Copy command
Alongside the OLTP traffic from your API gateway, your customers frequently hit a console per\-key drilldown view backed by a SELECT statement:

```
1SELECT c.api_key_id,
2       sum(c.cost_usd)         AS total_cost_usd,
3       sum(c.tokens)           AS total_tokens,
4       count(*)                AS n_calls,
5       max(c.called_at)        AS last_active_at,
6       avg(c.latency_ms)::int  AS avg_latency_ms
7FROM wm_api_calls c JOIN wm_api_keys k USING (api_key_id)
8WHERE k.tier IN (0, 1, 2)
9GROUP BY c.api_key_id
10ORDER BY total_cost_usd DESC;
```
Copy command
A bit after you launch you have 2000 API keys (congrats!) and they've made a total of 30,000 calls so far. The plan from `EXPLAIN (ANALYZE, BUFFERS, VERBOSE)` is unremarkable; the relevant lines:

```
1Sort
2   Sort Method: quicksort  Memory: 87kB
3   ->  HashAggregate
4         Batches: 1  Memory Usage: 689kB
5         ->  Hash Join
6               ->  Seq Scan on wm_api_calls c
7               ->  Hash
8                     Buckets: 2048  Batches: 1  Memory Usage: 68kB
```
Copy command
Three nodes consume memory: the `Hash` (build side, 68 kB), the `HashAggregate` (689 kB), and the `Sort` (87 kB). These sum up to around 0\.8 MB, comfortably below the default `work_mem` threshold.

*A note on memory accounting: when we say "total memory" in this section we mean the sum of each memory\-using node's peak. Postgres usually holds a node's memory until the end of the query, so we judge this a close\-enough approximation.*
