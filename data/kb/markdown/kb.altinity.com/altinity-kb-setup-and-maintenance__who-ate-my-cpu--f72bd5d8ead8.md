# Who ate my CPU \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. Who ate my CPU
# Who ate my CPU

Queries to find which subsytem of ClickHouse® is using the most of CPU.## Merges


```
SELECT
    table,
    round((elapsed * (1 / progress)) - elapsed, 2) AS estimate,
    elapsed,
    progress,
    is_mutation,
    formatReadableSize(total_size_bytes_compressed) AS size,
    formatReadableSize(memory_usage) AS mem
FROM system.merges
ORDER BY elapsed DESC

```
## Mutations


```
SELECT
    database,
    table,
    substr(command, 1, 30) AS command,
    sum(parts_to_do) AS parts_to_do,
    anyIf(latest_fail_reason, latest_fail_reason != '')
FROM system.mutations
WHERE NOT is_done
GROUP BY
    database,
    table,
    command

```
## Current Processes


```
select elapsed, query from system.processes where is_initial_query and elapsed > 2

```
## Processes retrospectively


```
SELECT
    normalizedQueryHash(query) hash,
    current_database,
    sum(ProfileEvents['UserTimeMicroseconds'] as userCPUq)/1000 AS userCPUms,
    count(),
    sum(query_duration_ms) query_duration_ms,
    userCPUms/query_duration_ms cpu_per_sec, 
    argMax(query, userCPUq) heaviest_query
FROM system.query_log
WHERE (type = 2) AND (event_date >= today())
GROUP BY
    current_database,
    hash
ORDER BY userCPUms DESC
LIMIT 10
FORMAT Vertical;

```
Last modified 2025\.04\.27: [Update who\-ate\-my\-cpu.md (2e8a36a)](https://github.com/Altinity/altinityknowledgebase/commit/2e8a36a4d709b95ca226726ec2954c5f5531edf1)
