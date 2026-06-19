# ALTER TABLE ... MODIFY QUERY Statement \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [ALTER](/docs/sql-reference/statements/alter)- VIEW
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/view.md)# ALTER TABLE ... MODIFY QUERY Statement

You can modify `SELECT` query that was specified when a [materialized view](/docs/sql-reference/statements/create/view#materialized-view) was created with the `ALTER TABLE ... MODIFY QUERY` statement without interrupting ingestion process.


This command is created to change materialized view created with `TO [db.]name` clause. It does not change the structure of the underlying storage table and it does not change the columns' definition of the materialized view, because of this the application of this command is very limited for materialized views are created without `TO [db.]name` clause.


**Example with TO table**



```
CREATE TABLE events (ts DateTime, event_type String)
ENGINE = MergeTree ORDER BY (event_type, ts);

CREATE TABLE events_by_day (ts DateTime, event_type String, events_cnt UInt64)
ENGINE = SummingMergeTree ORDER BY (event_type, ts);

CREATE MATERIALIZED VIEW mv TO events_by_day AS
SELECT toStartOfDay(ts) ts, event_type, count() events_cnt
FROM events
GROUP BY ts, event_type;

INSERT INTO events
SELECT DATE '2020-01-01' + interval number * 900 second,
       ['imp', 'click'][number%2+1]
FROM numbers(100);

SELECT ts, event_type, sum(events_cnt)
FROM events_by_day
GROUP BY ts, event_type
ORDER BY ts, event_type;

┌──────────────────ts─┬─event_type─┬─sum(events_cnt)─┐
│ 2020-01-01 00:00:00 │ click      │              48 │
│ 2020-01-01 00:00:00 │ imp        │              48 │
│ 2020-01-02 00:00:00 │ click      │               2 │
│ 2020-01-02 00:00:00 │ imp        │               2 │
└─────────────────────┴────────────┴─────────────────┘

-- Let's add the new measurement `cost`
-- and the new dimension `browser`.

ALTER TABLE events
  ADD COLUMN browser String,
  ADD COLUMN cost Float64;

-- Column do not have to match in a materialized view and TO
-- (destination table), so the next alter does not break insertion.

ALTER TABLE events_by_day
    ADD COLUMN cost Float64,
    ADD COLUMN browser String after event_type,
    MODIFY ORDER BY (event_type, ts, browser);

INSERT INTO events
SELECT Date '2020-01-02' + interval number * 900 second,
       ['imp', 'click'][number%2+1],
       ['firefox', 'safary', 'chrome'][number%3+1],
       10/(number+1)%33
FROM numbers(100);

-- New columns `browser` and `cost` are empty because we did not change Materialized View yet.

SELECT ts, event_type, browser, sum(events_cnt) events_cnt, round(sum(cost),2) cost
FROM events_by_day
GROUP BY ts, event_type, browser
ORDER BY ts, event_type;

┌──────────────────ts─┬─event_type─┬─browser─┬─events_cnt─┬─cost─┐
│ 2020-01-01 00:00:00 │ click      │         │         48 │    0 │
│ 2020-01-01 00:00:00 │ imp        │         │         48 │    0 │
│ 2020-01-02 00:00:00 │ click      │         │         50 │    0 │
│ 2020-01-02 00:00:00 │ imp        │         │         50 │    0 │
│ 2020-01-03 00:00:00 │ click      │         │          2 │    0 │
│ 2020-01-03 00:00:00 │ imp        │         │          2 │    0 │
└─────────────────────┴────────────┴─────────┴────────────┴──────┘

ALTER TABLE mv MODIFY QUERY
  SELECT toStartOfDay(ts) ts, event_type, browser,
  count() events_cnt,
  sum(cost) cost
  FROM events
  GROUP BY ts, event_type, browser;

INSERT INTO events
SELECT Date '2020-01-03' + interval number * 900 second,
       ['imp', 'click'][number%2+1],
       ['firefox', 'safary', 'chrome'][number%3+1],
       10/(number+1)%33
FROM numbers(100);

SELECT ts, event_type, browser, sum(events_cnt) events_cnt, round(sum(cost),2) cost
FROM events_by_day
GROUP BY ts, event_type, browser
ORDER BY ts, event_type;

┌──────────────────ts─┬─event_type─┬─browser─┬─events_cnt─┬──cost─┐
│ 2020-01-01 00:00:00 │ click      │         │         48 │     0 │
│ 2020-01-01 00:00:00 │ imp        │         │         48 │     0 │
│ 2020-01-02 00:00:00 │ click      │         │         50 │     0 │
│ 2020-01-02 00:00:00 │ imp        │         │         50 │     0 │
│ 2020-01-03 00:00:00 │ click      │ firefox │         16 │  6.84 │
│ 2020-01-03 00:00:00 │ click      │         │          2 │     0 │
│ 2020-01-03 00:00:00 │ click      │ safary  │         16 │  9.82 │
│ 2020-01-03 00:00:00 │ click      │ chrome  │         16 │  5.63 │
│ 2020-01-03 00:00:00 │ imp        │         │          2 │     0 │
│ 2020-01-03 00:00:00 │ imp        │ firefox │         16 │ 15.14 │
│ 2020-01-03 00:00:00 │ imp        │ safary  │         16 │  6.14 │
│ 2020-01-03 00:00:00 │ imp        │ chrome  │         16 │  7.89 │
│ 2020-01-04 00:00:00 │ click      │ safary  │          1 │   0.1 │
│ 2020-01-04 00:00:00 │ click      │ firefox │          1 │   0.1 │
│ 2020-01-04 00:00:00 │ imp        │ firefox │          1 │   0.1 │
│ 2020-01-04 00:00:00 │ imp        │ chrome  │          1 │   0.1 │
└─────────────────────┴────────────┴─────────┴────────────┴───────┘

-- !!! During `MODIFY ORDER BY` PRIMARY KEY was implicitly introduced.

SHOW CREATE TABLE events_by_day FORMAT TSVRaw

CREATE TABLE test.events_by_day
(
    `ts` DateTime,
    `event_type` String,
    `browser` String,
    `events_cnt` UInt64,
    `cost` Float64
)
ENGINE = SummingMergeTree
PRIMARY KEY (event_type, ts)
ORDER BY (event_type, ts, browser)

-- !!! The columns' definition is unchanged but it does not matter, we are not querying
-- MATERIALIZED VIEW, we are querying TO (storage) table.
-- SELECT section is updated.

SHOW CREATE TABLE mv FORMAT TSVRaw;

CREATE MATERIALIZED VIEW test.mv TO test.events_by_day
(
    `ts` DateTime,
    `event_type` String,
    `events_cnt` UInt64
) AS
SELECT
    toStartOfDay(ts) AS ts,
    event_type,
    browser,
    count() AS events_cnt,
    sum(cost) AS cost
FROM test.events
GROUP BY
    ts,
    event_type,
    browser

```

**Example without TO table**


The application is very limited because you can only change the `SELECT` section without adding new columns.



```
CREATE TABLE src_table (`a` UInt32) ENGINE = MergeTree ORDER BY a;
CREATE MATERIALIZED VIEW mv (`a` UInt32) ENGINE = MergeTree ORDER BY a AS SELECT a FROM src_table;
INSERT INTO src_table (a) VALUES (1), (2);
SELECT * FROM mv;

```


```
┌─a─┐
│ 1 │
│ 2 │
└───┘

```


```
ALTER TABLE mv MODIFY QUERY SELECT a * 2 as a FROM src_table;
INSERT INTO src_table (a) VALUES (3), (4);
SELECT * FROM mv;

```


```
┌─a─┐
│ 6 │
│ 8 │
└───┘
┌─a─┐
│ 1 │
│ 2 │
└───┘

```

## ALTER TABLE ... MODIFY REFRESH Statement[​](#alter-table--modify-refresh-statement "Direct link to ALTER TABLE ... MODIFY REFRESH Statement")


`ALTER TABLE ... MODIFY REFRESH` changes refresh parameters of a [Refreshable Materialized View](/docs/sql-reference/statements/create/view#refreshable-materialized-view), including the schedule, dependencies, randomization, and [refresh settings](/docs/sql-reference/statements/create/view#refresh-settings).



```
ALTER TABLE [db.]name MODIFY REFRESH EVERY|AFTER ... [RANDOMIZE FOR ...] [DEPENDS ON ...] [SETTINGS ...]

```

The schedule (`EVERY` or `AFTER`) is mandatory: the statement replaces *all* refresh parameters at once. Any clause not specified — `RANDOMIZE FOR`, `DEPENDS ON`, or `SETTINGS` — is removed or reset to defaults. To change only refresh settings, repeat the current schedule.



```
-- Change the schedule.
ALTER TABLE rmv MODIFY REFRESH EVERY 30 MINUTE;

-- Change retry settings (schedule must be repeated).
ALTER TABLE rmv MODIFY REFRESH EVERY 1 HOUR
SETTINGS refresh_retries = 5,
         refresh_retry_initial_backoff_ms = 500,
         refresh_retry_max_backoff_ms = 60000;

-- Add or keep a dependency.
ALTER TABLE rmv MODIFY REFRESH EVERY 6 HOUR DEPENDS ON other_rmv;

-- Drop the dependency by omitting `DEPENDS ON`.
ALTER TABLE rmv MODIFY REFRESH EVERY 6 HOUR;

```

Limitations:


- `ALTER TABLE ... MODIFY SETTING` is not supported on materialized views; refresh settings can only be changed via `MODIFY REFRESH`.
- Adding or removing `APPEND` is not supported.
- The `all_replicas` refresh setting cannot be changed after the view is created.


The full list of refresh settings is documented in [Refresh Settings](/docs/sql-reference/statements/create/view#refresh-settings). Refresh status, including the currently applied settings, is visible in [`system.view_refreshes`](/docs/operations/system-tables/view_refreshes).

[PreviousPROJECTION](/docs/sql-reference/statements/alter/projection)[NextALTER TABLE ... MODIFY COMMENT](/docs/sql-reference/statements/alter/comment)- [ALTER TABLE ... MODIFY REFRESH Statement](#alter-table--modify-refresh-statement)
Was this page helpful?
