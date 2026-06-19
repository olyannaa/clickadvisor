---
source: blog
url: https://www.youtube.com/live/dURnKjLuZLg?si=1Bx618RgGfAwN4iP&t=2216
topic: how-clickhouse-became-fast-at-joins
ch_version_introduced: '5.419'
last_updated: '2026-06-12'
chunk_index: 6
total_chunks_in_doc: 11
---

build one in\-memory hash table. ③ During the probe phase, `orders` rows, the left side of the join, are streamed in parallel and routed to the corresponding hash table for lookup. #### The problem: wasted probe\-side work [\#](/blog/clickhouse-fast-joins#the-problem-wasted-probe-side-work)

Note that in step ②, only a subset of customer keys is inserted into the hash tables during the build phase. However, in step ③, ClickHouse still processes all orders rows. For orders whose customer was removed by the customer filter, the lookup can never succeed. Those rows still consume CPU and memory bandwidth before the join rejects them.

#### The idea: filter probe rows before lookup [\#](/blog/clickhouse-fast-joins#the-idea-filter-probe-rows-before-lookup)

Runtime filters address exactly this wasted work.

While ClickHouse builds the hash tables (in DRAM) from the filtered customer rows, it also creates a compact filter (bloom filter or min/max values) from the join keys that actually made it into the build side. In our example, that means only customer keys that survived c\_nation \= 'DE'.

That filter is applied to the orders side before the hash\-table lookup. If an orders row has an o\_custkey that is not present in the filtered build side, ClickHouse can discard it early instead of routing it into the join.

The runtime filter is much smaller than the hash tables themselves, so it can stay close to the CPU, typically in L1 or L2 cache.

#### How runtime filters fit into the query pipeline [\#](/blog/clickhouse-fast-joins#how-runtime-filters-fit-into-the-query-pipeline)

The updated pipeline looks like this:

![Blog-JOINS-improvements.007.png](/uploads/Blog_JOINS_improvements_007_1cf7d0baf0.png)
The updated pipeline adds two steps:

② While reading the filtered customer rows, ClickHouse builds a runtime filter from their join keys.

④ Before probing the hash tables, ClickHouse applies that runtime filter to the orders rows.

⑤ Only rows that pass the runtime filter continue to the hash\-table lookup.

The parallel hash join structure stays the same, but many probe\-side rows are removed before the expensive lookup.

This keeps the parallel hash join structure unchanged, but removes probe\-side rows that could never match. In selective joins, this can significantly reduce CPU work and memory bandwidth.

#### How it appears in the query plan [\#](/blog/clickhouse-fast-joins#how-it-appears-in-the-query-plan)

We can see this in the logical query plan with EXPLAIN plan.

First, with runtime pre\-filtering disabled:
