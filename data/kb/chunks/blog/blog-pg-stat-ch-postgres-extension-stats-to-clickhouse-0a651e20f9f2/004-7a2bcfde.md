---
source: blog
url: 'https://github.com/ClickHouse/pg_stat_ch):'
topic: pg-stat-ch-a-postgresql-extension-that-exports-every-metric-to-clickhouse
ch_version_introduced: '4.6'
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 13
---

buffer is the hottest data structure in the extension. Every backend process writes to it (producers), and one background worker reads from it (consumer). On a busy 32\-core system, that’s potentially dozens of concurrent writers. Here’s the layout:

```
┌───────────────────────────────────────────┐
│ [Rarely changed]                          │
│   LWLock* lock                            │
│   uint32  capacity                        │
│                                           │
│ ─── CACHE LINE BOUNDARY (64 bytes) ───────│
│                                           │
│ [Producer-hot: many backends write]       │
│   atomic_uint64 head                      │
│   atomic_uint64 enqueued                  │
│   atomic_uint64 dropped                   │
│   atomic_flag   overflow_logged           │
│                                           │
│ ─── CACHE LINE BOUNDARY ──────────────────│
│                                           │
│ [Consumer-hot: bgworker reads/writes]     │
│   atomic_uint64 tail                      │
│   atomic_uint64 exported                  │
│                                           │
│ ─── CACHE LINE BOUNDARY ──────────────────│
│                                           │
│ [Stats: bgworker writes, anyone reads]    │
│   atomic_uint64 send_failures             │
│   TimestampTz   last_success_ts           │
│   TimestampTz   last_error_ts             |
│   char          last_error_text[256]      │
│   atomic_uint32 bgworker_pid              │
└───────────────────────────────────────────┘

```

The PG\_CACHE\_LINE\_SIZE padding between sections is the critical detail. Without it, every time the background worker updates tail, it invalidates the cache line containing head on every producer’s CPU core. That’s **false sharing** — and on multi\-socket systems it can cost 50–100ns per access. With the separation, producer cores and the consumer core work on independent cache lines and never interfere.

The capacity is always a power of 2 (1,024 to 65,536\), so slot addressing uses a bitmask (index \& (capacity \- 1\)) instead of modulo. One fewer division instruction in the hot path.

### Decision 3: no back\-pressure [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#decision-3-no-back-pressure)

There are exactly two ways events can be lost, and both are deliberate:

1. **Queue overflow.** The ring buffer fills up faster than the background worker drains it. New events are dropped — the producer atomically increments a dropped counter and returns in nanoseconds.
2. **Export failure.** The background worker dequeues a batch, then the ClickHouse insert fails. Those events are gone. We don’t re\-enqueue them.

The alternative is back\-pressure. That would mean if ClickHouse slows down or goes offline, PostgreSQL starts feeling it too, and your queries get slower. **For us, that’s a non\-starter.**
