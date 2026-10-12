---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Memory
topic: memory-safety-for-postgres-extensions-in-c-c-clickhouse
ch_version_introduced: auto
last_updated: '2026-10-12'
chunk_index: 2
total_chunks_in_doc: 4
---

even in a background worker will lead to the Postgres postmaster process having to restart everything in fear that shared memory has been corrupted. Each of these extensions took a different strategy around memory safety. ## pg\_clickhouse \#

For pg\_clickhouse we have completely eradicated the use of C\+\+. This involved replacing [clickhouse\-cpp](https://github.com/clickhouse/clickhouse-cpp) with an entirely new C library, [clickhouse\-c](https://github.com/ClickHouse/clickhouse-c), which we recently wrapped in another library, [pg\-clickhouse\-c](https://github.com/ClickHouse/pg-clickhouse-c), in order to consolidate postgres logic while keeping clickhouse\-c a general\-purpose library. clickhouse\-c was designed to be transport\-agnostic, supporting [Native](https://clickhouse.com/docs/reference/formats/Native) format outside Native protocol, so now the HTTP driver shares much of its decoding/encoding logic with the binary driver by using Native format over HTTP. For HTTP we use libcurl, which offers a low level enough interface to play nice with Postgres's environment.

For example, previously in `binary.cpp`, `make_datum` converted a ClickHouse String with:

```
1auto s = std::string(col->AsStrict<ColumnString>()->At(row));
2ret = PointerGetDatum(cstring_to_text_with_len(s.data(), s.size()));
```
Copy command
`cstring_to_text_with_len` allocates a Postgres text value with `palloc`. If that allocation fails, Postgres raises ERROR and jumps to its error handler, bypassing `s`'s destructor. Surrounding C\+\+ try/catch cannot catch this jump.

## pg\_re2 \#

For pg\_re2 C\+\+ is scoped to [re2\_wrapper.cpp](https://github.com/ClickHouse/pg_re2/blob/main/src/re2_wrapper.cpp). All C\+\+ allocations happen within C\+\+ try/catch, \& it doesn't call into postgres C code. Separation of concerns is sufficient for this encapsulation to draw a clean line between the two systems.

## pg\_chdb \#

pg\_chdb reuses pg\-clickhouse\-c for decoding/encoding native blocks. Originally it loaded [libchdb](https://clickhouse.com/docs/chdb/) into the background worker, but eventually moved libchdb into a separate helper executable. Isolating libchdb is the point: its C\+\+ runtime, threads, allocations, and failures live outside a Postgres backend or managed background worker. The backend forks and execs this helper, so it remains a descendant of postmaster, but postmaster does not manage it as a background worker. This helper only needs enough information to run a ClickHouse query \& exchange Native blocks, so it has no need for postgres headers. A libchdb crash can then fail the calling operation without itself triggering Postgres cluster crash recovery.

## pg\_stat\_ch \#
