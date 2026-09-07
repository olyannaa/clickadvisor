---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"What's
topic: what-s-new-with-monitoring-in-postgresql-19-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 2
total_chunks_in_doc: 7
---

reasoning in the commit message: > If someone is stuck behind a lock for more than a second, that is almost always a problem that is worth a log entry. ## Different log verbosity per process type \#

`log_min_messages` has always been a single global knob. If you wanted `DEBUG2` output from the checkpointer, you got `DEBUG2` from everything and good luck finding the line you care about.

Starting with PostgreSQL 19, `log_min_messages` accepts a comma\-separated list of `process type:level` pairs, plus one mandatory level that applies to every process type not listed. A bare level is still valid, so the old syntax keeps working.

```
1-- DEBUG2 for the checkpointer, DEBUG1 for autovacuum, WARNING for everything else
2ALTER SYSTEM SET log_min_messages = 'warning, checkpointer:debug2, autovacuum:debug1';
```
Copy command
The recognized process types are `archiver`, `autovacuum`, `backend`, `bgworker`, `bgwriter`, `checkpointer`, `checksums`, `ioworker`, `postmaster`, `slotsyncworker`, `startup`, `syslogger`, `walreceiver`, `walsender`, `walsummarizer` and `walwriter`. Note that `autovacuum` covers both the launcher and the workers.

## Separate logging for autoanalyze \#

Until now, `log_autovacuum_min_duration` controlled log output for both VACUUM and ANALYZE runs by autovacuum. These are very different operations: autoanalyze runs are typically much shorter, so a threshold tuned to catch slow vacuums silently discards almost all ANALYZE activity.

PostgreSQL 19 adds `log_autoanalyze_min_duration`, which controls log output for ANALYZE. `log_autovacuum_min_duration` now only controls VACUUM logging. Both default to `10min`, accept `0` (log everything) and `-1` (disable). You can also set per\-table overrides:

```
1-- For this table log every autoanalyze, regardless of the global setting
2ALTER TABLE events SET (log_autoanalyze_min_duration = 0);
```
Copy command
**Upgrade notes:** If your tooling parses autovacuum logs, remember that after the upgrade `log_autovacuum_min_duration` alone no longer reports analyze runs. And if you’re displaying log parameters in a UI, consider making `log_autoanalyze_min_duration` visible as well.

## WAL full\-page write bytes to VACUUM and ANALYZE logging \#
