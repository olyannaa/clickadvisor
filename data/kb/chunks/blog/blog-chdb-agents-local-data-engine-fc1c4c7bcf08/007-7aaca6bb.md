---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"chDB
topic: chdb-as-the-agent-s-local-data-engine-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 7
total_chunks_in_doc: 13
---

**stability is a token problem.** ### Why a flaky data call costs *tokens*, not just milliseconds \# When a tool call fails, an agent does not shrug it off the way a microservice does. The documented behavior is:

1. The model receives the error and **retries** — and in an agent loop, *every retry re\-sends the full conversation context to the LLM*. A retry costs a whole context window, not one cheap HTTP round\-trip. [\[6]](#sources)
2. If retries keep failing, the model "gets creative" and **takes a detour** — trying a different query, a different tool, a different plan. More tokens, more latency, for data it already needed.

In production traces this waste is pervasive and usually invisible, because the turn eventually *succeeds* — the cost only shows up on the bill. [\[5]](#sources)

### A concrete detour \#

> A customer\-support agent is mid\-session and needs the user's recent preference history to answer. It issues a query to the warehouse. The warehouse is briefly busy — a `Server busy`, a disk stall, a dropped packet. The model gets the error, **re\-sends its 14k\-token context** and retries. Still slow. It retries again. Then it "reroutes": maybe it queries a different table, or asks for a broader slice and filters in its own head. Several thousand tokens and several seconds later, it has the answer it could have had instantly.
> 
> 
> The same agent backed by chDB calls `sess.query(...)`, gets the rows in **sub\-millisecond time, deterministically, every single time**, and never enters the retry/detour spiral at all.

![](/_next/image?url=%2Fuploads%2Fch_DB_Local_Data_Engine_5_2e7180206b.jpg&w=2048&q=75)

### Think it through: why local is necessarily more stable \#

**A local query is a function call.** Its latency distribution is a tall, narrow spike set by CPU and memory bandwidth — no RTT, no jitter, no packet loss, no server\-side queueing. Its p50 and p99 are practically the same number. **Determinism** is the point: the same speed every time.

**A remote query, however fast the server, still has to cross the wire.** Base RTT \+ jitter \+ the occasional TCP retransmit \+ server\-side contention stack up, which means its p99/p999 is set not by compute but by the worst network event. In other words, the remote tail is **structural** — you can't optimize it away, because it isn't in your process at all.
