# Replication queue \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. Replication queue
# Replication queue


```
SELECT
    database,
    table,
    type,
    max(last_exception),
    max(postpone_reason),
    min(create_time),
    max(last_attempt_time),
    max(last_postpone_time),
    max(num_postponed) AS max_postponed,
    max(num_tries) AS max_tries,
    min(num_tries) AS min_tries,
    countIf(last_exception != '') AS count_err,
    countIf(num_postponed > 0) AS count_postponed,
    countIf(is_currently_executing) AS count_executing,
    count() AS count_all
FROM system.replication_queue
GROUP BY
    database,
    table,
    type
ORDER BY count_all DESC

```
Last modified 2022\.02\.15: [Update altinity\-kb\-replication\-queue.md (614f2d6\)](https://github.com/Altinity/altinityknowledgebase/commit/614f2d6db57bc2c78d2154d2d45d4ecc0f683f55)
