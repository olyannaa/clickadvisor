---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Why
topic: why-strict-memory-overcommit-matters-for-postgres-clickhouse
ch_version_introduced: '30.507'
last_updated: '2026-09-07'
chunk_index: 2
total_chunks_in_doc: 6
---

error: the query fails with `out of memory`, the transaction rolls back, and the remaining connections keep working. This is the setting the Postgres documentation recommends in its chapter on kernel resources. ## Setting the commit limit \#

Strict overcommit is only useful if the limit is in the right place. Too high and the kernel still hands out more than it can back; too low and queries fail while memory sits free. Every server gets an explicit limit in kilobytes rather than the kernel's default ratio:

```
1# /etc/sysctl.d/99-overcommit.conf
2vm.overcommit_memory=2
3vm.overcommit_kbytes=<computed from MemTotal>
```
Copy command
The limit is 80% of the memory that is available for ordinary allocations, plus 2GB. Two details set the size of that first term.

The first is that a quarter of the machine is already reserved as huge pages for `shared_buffers`, and huge pages do not count toward the commit limit. Postgres maps that segment once at startup, outside the accounting the commit limit governs, so the limit is computed against the remaining 75% of RAM rather than the whole machine.

The second is the 80%: what remains has to cover the kernel itself, page tables, the page cache, and every per\-backend allocation Postgres makes at runtime, so the limit deliberately stops short of the memory that is actually there. The 2GB on top is headroom for the sidecar processes that share the box with Postgres, the backup agent and the metrics exporters.

The result is a commit limit of roughly 60% of total RAM plus 2GB, and a kernel that starts returning `ENOMEM` while several gigabytes are still physically free. That gap is the point. The error arrives while there is still memory available to handle the error.

### Get started with ClickHouse Managed Postgres today

Interested in seeing how ClickHouse Managed Postgres works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?intent=pg&loc=blog-cta-1556-get-started-with-clickhouse-managed-postgres-today-sign-up&utm_blogctaid=1556)## Seeing it on real hardware \#
