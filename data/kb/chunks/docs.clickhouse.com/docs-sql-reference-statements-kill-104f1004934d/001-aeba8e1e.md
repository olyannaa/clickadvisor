---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/kill.md)#
topic: kill-statements-clickhouse-docs
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 2
---

# KILL Statements \| ClickHouse Docs

- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- KILL
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/kill.md)# KILL Statements

There are two kinds of kill statements: to kill a query and to kill a mutation

## KILL QUERY[​](#kill-query "Direct link to KILL QUERY")

```
KILL QUERY [ON CLUSTER cluster]
  WHERE <where expression to SELECT FROM system.processes query>
  [SYNC|ASYNC|TEST]
  [FORMAT format]

```

Attempts to forcibly terminate the currently running queries.
The queries to terminate are selected from the system.processes table using the criteria defined in the `WHERE` clause of the `KILL` query.

Examples:

First, you'll need to get the list of incomplete queries. This SQL query provides them according to those running the longest:

List from a single ClickHouse node:

```
SELECT
  initial_query_id,
  query_id,
  formatReadableTimeDelta(elapsed) AS time_delta,
  query,
  *
  FROM system.processes
  WHERE query ILIKE 'SELECT%'
  ORDER BY time_delta DESC;

```

List from a ClickHouse cluster:

```
SELECT
  initial_query_id,
  query_id,
  formatReadableTimeDelta(elapsed) AS time_delta,
  query,
  *
  FROM clusterAllReplicas(default, system.processes)
  WHERE query ILIKE 'SELECT%'
  ORDER BY time_delta DESC;

```

Kill the query:

```
-- Forcibly terminates all queries with the specified query_id:
KILL QUERY WHERE query_id='2-857d-4a57-9ee0-327da5d60a90'

-- Synchronously terminates all queries run by 'username':
KILL QUERY WHERE user='username' SYNC

```

TipIf you are killing a query in ClickHouse Cloud or in a self\-managed cluster, then be sure to use the `ON CLUSTER [cluster-name]`option, in order to ensure the query is killed on all replicas

Read\-only users can only stop their own queries.

By default, the asynchronous version of queries is used (`ASYNC`), which does not wait for confirmation that queries have stopped.

The synchronous version (`SYNC`) waits for all queries to stop and displays information about each process as it stops.
The response contains the `kill_status` column, which can take the following values:

1. `finished` – The query was terminated successfully.
2. `waiting` – Waiting for the query to end after sending it a signal to terminate.
3. The other values ​​explain why the query can't be stopped.

A test query (`TEST`) only checks the user's rights and displays a list of queries to stop.

## KILL MUTATION[​](#kill-mutation "Direct link to KILL MUTATION")

The presence of long\-running or incomplete mutations often indicates that a ClickHouse service is running poorly. The asynchronous nature of mutations can cause them to consume all available resources on a system. You may need to either:
