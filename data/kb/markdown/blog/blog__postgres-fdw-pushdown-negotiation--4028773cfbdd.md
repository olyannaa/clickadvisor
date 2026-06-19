# Postgres FDW: Pushdown is a negotiation


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Postgres FDW: Pushdown is a negotiation

![](/_next/image?url=%2Fuploads%2FImage_512x512_1_839aa54f62.jpeg&w=96&q=75)![](/_next/image?url=%2Fuploads%2FImage_512x512_1_8bc569c360.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2FImage_from_Slack_3_99e6dde6b4.png&w=96&q=75)[Kaushik Iska](/authors/kaushik-iska), [David Wheeler](/authors/david-wheeler) and [Philip Dubé](/authors/philip-dube)May 14, 2026 · 20 minutes readPostgres [extensions](https://www.postgresql.org/docs/current/extend-extensions.html) add functionality that Postgres itself does not include. Examples include [PostGIS](https://postgis.net/) for geospatial data, [pgvector](https://github.com/pgvector/pgvector) for embeddings, and [TimescaleDB](https://github.com/timescale/timescaledb) for time\-series. Via extensions the Postgres ecosystem distributes new functionality; just `CREATE EXTENSION` to hook into Postgres internals, and thereafter the user mostly forgets about it.


[Foreign Data Wrapper](https://www.postgresql.org/docs/current/ddl-foreign-data.html) extensions, also known as “FDW”s, teach Postgres how to read (and sometimes write) data outside of Postgres. Simply declare a foreign table:



```

```
1CREATE FOREIGN TABLE events (...)
2SERVER my_clickhouse OPTIONS (table 'events');
```

```

Then `SELECT * FROM events` resembles a query against any other table. Internally, Postgres asks the FDW to fetch the data from elsewhere.


[pg\_clickhouse](https://github.com/ClickHouse/pg_clickhouse), the FDW we maintain, fetches data from [ClickHouse](https://clickhouse.com/). While people often rely on the [unified data stack](https://clickhouse.com/blog/postgres-clickhouse-oss) — Postgres for transactional data and ClickHouse for analytics — pg\_clickhouse executes SQL queries on both systems. As we worked on it for the past 6 months, we found that a single question drives most of the engineering work: how much of a query do we send across the wire as SQL versus how many rows do we drag back as data?


That question encompasses the meaning of [pushdown](https://whatisdatabase.com/optimizing-database-performance-with-pushdown-techniques): how much work can we “push down” to the remote service? The answer seems simple: “send everything!” — the `WHERE` clause, the `GROUP BY`, the `LIMIT`. But a closer examination reveals the complexity: Some clauses we can send. Some we can almost send — if we rewrite them. Some we used to send but stopped, because they returned the wrong results. And some clauses can never be sent by any FDW, regardless of the engineering one throws at them.


We’ve found the process of making these determinations highly iterative.


To demonstrate, let’s examine the impact of that iteration on a single query: what gets pushed down, what doesn't, and how we continuously modified the code in response to the question.


The goal is to illuminate the inner workings of an FDW for people who’ve heard of FDWs but don’t know how they work in detail. Whether you're a Postgres user curious about ClickHouse, a ClickHouse user curious about Postgres, or someone thinking about writing an FDW yourself, we hope you find this exercise edifying.


## The query that takes 80 ms or 4 minutes [\#](/blog/postgres-fdw-pushdown-negotiation#the-query-that-takes-80-ms-or-4-minutes)


This query ranks the busiest web events in the last week for the US, UK, and DE, by country and event name. It reports volume, unique users, premium share, p95 latency, and each event’s rank by country, returning the top 100 rows overall to provide a small snapshot and avoid streaming raw events.



```

```
1SELECT
2  u.country,
3  e.event_name,
4  count(*) AS n,
5  count(DISTINCT e.user_id) AS unique_users,
6  count(*) FILTER (WHERE e.properties->>'tier' = 'premium') AS premium_count,
7  percentile_cont(0.95) WITHIN GROUP (ORDER BY e.duration_ms) AS p95_ms,
8  ROW_NUMBER() OVER (PARTITION BY u.country ORDER BY count(*) DESC) AS rank_in_country
9FROM events_ch e JOIN users_ch u USING (user_id)
10WHERE e.ts >= now() - interval '7 days'
11  AND u.country IN ('US', 'UK', 'DE')
12  AND e.properties->>'platform' = 'web'
13GROUP BY u.country, e.event_name
14ORDER BY n DESC
15LIMIT 100;
```

```

`events_ch` and `users_ch` are foreign tables backed by ClickHouse. With every clause in this query pushed down, it returns 100 rows in roughly 80 ms.


If a single clause fails to push down, the query takes minutes. We built support for pushing down the window function, the percentile, the JSON access, and the FILTER aggregate; but each was, at some earlier point, not yet pushed down. When an operation cannot be pushed down, the rest of the query can't push down either; rows that should have been aggregated remotely must stream back to Postgres so it can aggregate them locally. The wire ends up carrying tens to hundreds of millions of rows instead of 100\.


Pushdown looks like a feature, but it’s really an agreement between two SQL grammars, revised for every Postgres release. This explains why the pg\_clickhouse release notes often look like corrections: revoking incorrect array\-function pushdown, adding safer functions like `levenshtein` and `soundex`, and respecting planner invariants like [EvalPlanQual](https://github.com/postgres/postgres/blob/901ed9b/src/backend/executor/execMain.c#L2649-L2676) even when the remote could move faster.


## What the FDW actually negotiates [\#](/blog/postgres-fdw-pushdown-negotiation#2-what-the-fdw-actually-negotiates)


An FDW does not send the original Postgres query to the remote database; doing so causes errors where the SQL dialects differ. But ideally, It also does not pull every row back unless it has to (as simple FDWs like [file\_fdw](https://www.postgresql.org/docs/current/file-fdw.html) do), because although the results would be correct, execution would be slow.


![Diagram showing how a Foreign Data Wrapper sits between an application and a remote database, forwarding SQL queries and returning data rows](/uploads/2026_05_14_12_09_23_7401c62d71.png)
Postgres does not directly decide that a scan, join, aggregate, sort, or limit can be executed in ClickHouse. Instead, it asks the FDW to contribute foreign paths to the planner via the FDW planning callbacks. pg\_clickhouse registers these planning callbacks:



```

```
1routine->GetForeignRelSize    = clickhouseGetForeignRelSize;
2routine->GetForeignPaths      = clickhouseGetForeignPaths;
3routine->GetForeignPlan       = clickhouseGetForeignPlan;
4routine->GetForeignJoinPaths  = clickhouseGetForeignJoinPaths;
5routine->GetForeignUpperPaths = clickhouseGetForeignUpperPaths;
```

```

`GetForeignPaths`, `GetForeignJoinPaths`, and `GetForeignUpperPaths` tell the planner what can be pushed down. If the planner selects one of those paths, `GetForeignPlan` builds the plan and generates the ClickHouse SQL.


These callbacks are just entry points; pg\_clickhouse’s callback functions verify that each clause or expression can be translated without changing the result. Of course it started out quite simple: just a few clauses and expressions inherited from the original fork from [postgres\_fdw](https://www.postgresql.org/docs/current/postgres-fdw.html). Thus pg\_clickhouse initially pushed down `count(*)` but not `count(*) FILTER (...)`, couldn’t push down `percentile_cont` or JSON predicates like `properties->>'platform'`: because it did not know how.


Thus, pushdown is not a yes/no decision for a whole query, but constitutes a series of smaller decisions: does Postgres expose the hook, can pg\_clickhouse translate the expression, and can ClickHouse execute it with the same meaning?


## The progression: one query, every step we've shipped [\#](/blog/postgres-fdw-pushdown-negotiation#3-the-progression-one-query-every-step-weve-shipped)


To answer the question, "why doesn’t X push down?" let’s look at one realistic query and walk it through everything pg\_clickhouse has shipped. Same query, seven steps. Each step pushes down more to ClickHouse; Postgres must evaluate what remains after pulling back the rows it needs to do so.


Each step examines the same query. Lines marked ✓ push down at that step; lines marked ✗ remain local. Each step also marks a real date in our history, when the relevant pushdown landed in the codebase, or when we expect to ship it. Each step demonstrates what the query plan looked like as of that date.


### Step 1: scan \+ simple WHERE [\#](/blog/postgres-fdw-pushdown-negotiation#step-1-scan-simple-where)


Inherited from the original clickhouse\_fdw via initial port [`e5035bc`](https://github.com/ClickHouse/pg_clickhouse/commit/e5035bc) (October 2, 2025\). Available in pg\_clickhouse since v0\.1\.0 (December 9, 2025\).


The starting point is deliberately small: pg\_clickhouse only pushes down predicates it can translate with confidence. Comparisons like `>=`, membership checks like `IN`, and simple timestamp arithmetic are safe to push down because Postgres and ClickHouse have clear equivalents for them. In other words, those filters run in ClickHouse rather than collecting all the rows to evaluate in Postgres.



```

```
1SELECT
2  u.country,                                                                -- ✗
3  e.event_name,                                                             -- ✗
4  count(*) AS n,                                                            -- ✗
5  count(DISTINCT e.user_id) AS unique_users,                                -- ✗
6  count(*) FILTER (WHERE e.properties->>'tier' = 'premium') AS …,           -- ✗
7  percentile_cont(0.95) WITHIN GROUP (ORDER BY e.duration_ms) AS …,         -- ✗
8  ROW_NUMBER() OVER (PARTITION BY u.country ORDER BY count(*)) AS …         -- ✗
9FROM events_ch e                                                            -- ✓ scan only
10  JOIN users_ch u USING (user_id)                                           -- ✗
11WHERE e.ts >= now() - interval '7 days'                                     -- ✓
12  AND u.country IN ('US','UK','DE')                                         -- ✓
13  AND e.properties->>'platform' = 'web'                                     -- ✗
14GROUP BY u.country, e.event_name                                            -- ✗
15ORDER BY n DESC                                                             -- ✗
16LIMIT 100                                                                   -- ✗
```

```

At this point, only the base\-table filters push down. The SQL translator (internally called a “deparser”) emits one remote scan for `events` with the timestamp predicate, and one remote scan for `users` with the country predicate. It sends these two separate queries to ClickHouse and collects the results. Everything that combines rows or changes their shape, including the join, grouping, aggregates, window function, sort, and limit, runs inside Postgres against those retrieved rows. Thus the wire must carry every matching `events` row from the last seven days, plus every matching `users` row, before Postgres can reduce the result to 100 rows.


The point is that even the simplest pushdown is already a translation problem: `now()` can be pushed down as `now()`, while `interval '7 days'` is translated as `7 * 86400`. Those mappings live in [src/custom\_types.c](https://github.com/ClickHouse/pg_clickhouse/blob/main/src/custom_types.c), where pg\_clickhouse records the expressions it knows how to translate safely for ClickHouse. The steps outlined below expand that vocabulary from base filters to joins, aggregates, windows, and limits.


### Step 2: \+ JOIN pushdown [\#](/blog/postgres-fdw-pushdown-negotiation#step-2-join-pushdown)


Inner\-JOIN deparse came from the original clickhouse\_fdw, but the inherited cost estimates were placeholders, and the Postgres planner often pulled rows back to join locally rather than push. Commit [`b345682`](https://github.com/ClickHouse/pg_clickhouse/commit/b345682) (December 1, 2025\) replaced them with row\-count\-based estimates and cost\-based scans higher than join paths, so the planner reliably picks the pushed plan. Plus [`6a297ec`](https://github.com/ClickHouse/pg_clickhouse/commit/6a297ec) (Nov 13, 2025\) for `join_use_nulls` outer\-join semantics. All shipped in v0\.1\.0 (December 9, 2025\).


At this step pg\_clickhouse stops treating `events_ch` and `users_ch` as two independent remote scans. Since both tables live on the same ClickHouse server and the join condition has a ClickHouse equivalent, the FDW can ask ClickHouse to make the join before any joined rows cross the wire.



```

```
1SELECT ...                                                         -- ✗ (still)
2FROM events_ch e                                                   -- ✓
3  JOIN users_ch u USING (user_id)                                  -- ✓ joins push
4WHERE e.ts >= now() - interval '7 days'                            -- ✓
5  AND u.country IN ('US','UK','DE')                                -- ✓
6  AND e.properties->>'platform' = 'web'                            -- ✗ stays local
7GROUP BY u.country, e.event_name                                   -- ✗
8ORDER BY n DESC                                                    -- ✗
9LIMIT 100                                                          -- ✗
```

```

The remote SQL is now roughly `SELECT * FROM events ALL INNER JOIN users USING (user_id) WHERE …`. The `ALL` keyword is deliberate: ClickHouse's default join can return only one matching row, while a Postgres inner join returns all matches. Emitting `ALL INNER JOIN` preserves Postgres semantics. The JSON predicate still cannot be translated at this point, so it is left out of the remote `WHERE` and applied locally to the returned rows.


Postgres enabled this kind of join pushdown in 9\.6 (commit [`e4106b25287`](https://github.com/postgres/postgres/commit/e4106b25287), 2016, Etsuro Fujita). Previously, FDWs had to hook deeper into the planner to accomplish join pushdown.


For our query, this single step reduces query time from roughly 30 minutes to 30 seconds, because the join filters rows before they leave the remote.


### Step 3: \+ GROUP BY \+ simple aggregates \+ ORDER BY \+ LIMIT [\#](/blog/postgres-fdw-pushdown-negotiation#step-3-group-by-simple-aggregates-order-by-limit)


Also inherited via [`e5035bc`](https://github.com/ClickHouse/pg_clickhouse/commit/e5035bc). GROUP BY, basic aggregates (`count`, `sum`, `min`, `max`, `avg`), ORDER BY, and LIMIT all pushdown since v0\.1\.0 (December 9, 2025\).


This step emphasizes result\-shaping work: grouping rows, computing basic aggregates, sorting the grouped result, and applying the final limit. Postgres exposes these operations as “upper” planning stages, and the FDW can offer a remote version of each stage when the whole stage can be represented in ClickHouse. Aggregate pushdown arrived in Postgres 10 (commit [`7012b132d07`](https://github.com/postgres/postgres/commit/7012b132d07)); ORDER BY and LIMIT pushdown followed in Postgres 12\.


Still, at this point pg\_clickhouse cannot push down all of the operations: The grouping stage must encompass the entire SELECT list, and it hasn’t been wired to push down three expressions:


- `count(*) FILTER (WHERE e.properties->>'tier' = 'premium')`: the FILTER body contains a JSON op without a pushdown mapping
- `percentile_cont(...) WITHIN GROUP (ORDER BY ...)`: ClickHouse has an equivalent function, but pg\_clickhouse hasn’t mapped it
- `ROW_NUMBER() OVER (...)`: window functions have not been mapped to ClickHouse equivalents at all


Note that grouped pushdown is all\-or\-nothing for a given grouped result. So even though `count(*)`, `count(DISTINCT)`, `GROUP BY`, `ORDER BY`, and `LIMIT` are individually fine, the grouped part of this particular query still remains local.



```

```
1SELECT
2  u.country, e.event_name,                                          -- ✗ grouped result blocked
3  count(*) AS n,                                                    -- ✗ blocked
4  count(DISTINCT e.user_id) AS unique_users,                        -- ✗ blocked
5  count(*) FILTER (WHERE e.properties->>'tier' = 'premium') AS …,   -- ✗ FILTER body has JSON
6  percentile_cont(...) AS p95_ms,                                   -- ✗ no mapping yet
7  ROW_NUMBER() OVER (...) AS rank_in_country                        -- ✗ window not remote yet
8FROM events_ch e                                                    -- ✓
9  JOIN users_ch u USING (user_id)                                   -- ✓
10WHERE e.ts >= ... ✓ AND u.country IN (...)                          -- ✓
11  AND e.properties->>'platform' = 'web'                             -- ✗
12GROUP BY u.country, e.event_name                                    -- ✗ blocked
13ORDER BY n DESC                                                     -- ✗ blocked
14LIMIT 100                                                           -- ✗ blocked
```

```

A simpler subset of this query (drop the FILTER, percentile, and ROW\_NUMBER) would push down fully at this point:



```

```
1-- The subset that DOES push down at Step 3:
2SELECT u.country, e.event_name, count(*) AS n, count(DISTINCT e.user_id) AS unique_users
3FROM events_ch e JOIN users_ch u USING (user_id)
4WHERE e.ts >= now() - interval '7 days' AND u.country IN ('US','UK','DE')
5GROUP BY u.country, e.event_name
6ORDER BY n DESC LIMIT 100;
```

```

That subset deparses as a single ClickHouse SELECT statement, with `count(DISTINCT e.user_id)` emitted as a ClickHouse `count(DISTINCT user_id)`. The full, richer query needs three more steps to fully land.


### Step 4: \+ ordered\-set aggregates (`percentile_cont` → `quantile`) [\#](/blog/postgres-fdw-pushdown-negotiation#step-4-ordered-set-aggregates)


Commit [`087cfdc`](https://github.com/ClickHouse/pg_clickhouse/commit/087cfdc) (November 10, 2025\), in v0\.1\.0\. Previously, `percentile_cont` blocked the upper rel for any query that used it.


This step teaches pg\_clickhouse one more aggregate translation: Postgres `percentile_cont(p) WITHIN GROUP (ORDER BY x)` can be expressed as ClickHouse `quantile(p)(x)`. This change removes the percentile from the list of blockers. The allow list remains narrow: for example, pg\_clickhouse still refuses `string_agg(... ORDER BY ...)` because ClickHouse's closest equivalent does not preserve the same within\-group ordering semantics.



```

```
1SELECT
2  ...                                             -- ✗ still blocked
3  percentile_cont(...) AS p95_ms,                 -- ✓ now shippable
4  ROW_NUMBER() OVER (...) AS rank_in_country      -- ✗ window not remote yet
5FROM ...                                          -- (everything else unchanged from Step 2-3)
```

```

The `percentile_cont` function becoming individually shippable is necessary but not sufficient. The grouped result still can't be pushed down because two blockers remain: FILTER\-with\-JSON and the ROW\_NUMBER window function.


But take note of the recurring pattern over the course of these steps: a translation lifts one pushdown blocker at a time, but pushdown of the full query occurs only when all such blockers have been resolved. This explains how a stream of single\-translation changes to pg\_clickhouse, individually modest, compound over time to suddenly push down a full query that previously ran entirely locally.


### Step 5: \+ JSON sub\-column access (`->`, `->>`) [\#](/blog/postgres-fdw-pushdown-negotiation#step-5-json-sub-column-access)


Commits [`0b4c03e`](https://github.com/ClickHouse/pg_clickhouse/commit/0b4c03e) (April 2, 2026\) and [`669924a`](https://github.com/ClickHouse/pg_clickhouse/commit/669924a) (April 3\), in v0\.1\.6 / v0\.2\.0\. Previously, every `->`/`->>`/`jsonb_extract_path` was a local filter; even `e.properties->>'platform' = 'web'` couldn't pushdown.


This step adds JSON field access to the shared vocabulary. A Postgres JSON accessor expression like `e.properties->>'platform'` now translates to the ClickHouse sub\-column expression `e.properties.platform`, so JSON predicates need no longer wait for rows to be fetched back to Postgres.



```

```
1SELECT
2  u.country, e.event_name,                                          -- ✗ still blocked (window)
3  count(*) AS n, count(DISTINCT e.user_id) AS unique_users,         -- ✗ blocked (window)
4  count(*) FILTER (WHERE e.properties->>'tier' = 'premium') AS …,   -- ✓ FILTER body now lifts
5  percentile_cont(...) AS p95_ms,                                   -- ✓
6  ROW_NUMBER() OVER (...) AS rank_in_country                        -- ✗ window still blocks
7FROM events_ch e                                                    -- ✓
8JOIN users_ch u USING (user_id)                                     -- ✓
9WHERE ...
10  AND e.properties->>'platform' = 'web'                             -- ✓ JSON qual lifts
11GROUP BY u.country, e.event_name                                    -- ✗ still blocked
12ORDER BY n DESC                                                     -- ✗ blocked
13LIMIT 100                                                           -- ✗ blocked
```

```

Two things change at once:


- The `properties->>'platform' = 'web'` predicate ships as `properties.platform = 'web'`, so ClickHouse can filter those rows before sending them back.
- The filtered aggregate `count(*) FILTER (WHERE properties->>'tier' = 'premium')` pushes down as `countIf(properties.tier = 'premium')`, using ClickHouse's conditional aggregate form.


The grouped result still does not push down, but now there is only one blocker left: `ROW_NUMBER`.


### Step 6: \+ window functions [\#](/blog/postgres-fdw-pushdown-negotiation#step-6-window-functions)


Commit [`0caf913`](https://github.com/ClickHouse/pg_clickhouse/commit/0caf913) (April 2, 2026, same day as JSON sub\-column access), in v0\.1\.6 / v0\.2\.0\. Previously, any `OVER (...)` clause blocked the upper rel.


This step lets pg\_clickhouse offer a remote plan for window functions. `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LEAD`, `LAG`, `FIRST_VALUE`, `LAST_VALUE`, `NTH_VALUE`, and `MIN/MAX OVER` all run in ClickHouse when their partition keys and order keys can also be translated.


Here pg\_clickhouse exceeds the pushdown of its ancestor, `postgres_fdw`, which does not push down window functions. But ClickHouse executes them quickly and close to the data, a benefit that greatly outweighs the overhead of translating the functions.



```

```
1SELECT
2  u.country,                                                        -- ✓
3  e.event_name,                                                     -- ✓
4  count(*) AS n,                                                    -- ✓
5  count(DISTINCT e.user_id) AS unique_users,                        -- ✓
6  count(*) FILTER (WHERE e.properties->>'tier' = 'premium') AS …,   -- ✓
7  percentile_cont(0.95) WITHIN GROUP (ORDER BY e.duration_ms) AS …, -- ✓
8  ROW_NUMBER() OVER (PARTITION BY u.country ORDER BY count(*)) AS …,-- ✓
9FROM events_ch e                                                    -- ✓
10  JOIN users_ch u USING (user_id)                                   -- ✓
11WHERE e.ts >= now() - interval '7 days'                             -- ✓
12  AND u.country IN ('US','UK','DE')                                 -- ✓
13  AND e.properties->>'platform' = 'web'                             -- ✓
14GROUP BY u.country, e.event_name                                    -- ✓
15ORDER BY n DESC                                                     -- ✓
16LIMIT 100                                                           -- ✓
```

```

No impediments to pushdown remain. The join, grouping, aggregates, window function, ordering, and limit all become one ClickHouse query. What used to be a Postgres plan with separate Limit / Sort / WindowAgg / Group / Join / Scan / Scan nodes collapses into a single foreign scan whose remote SQL looks roughly like:



```

```
1-- What lands on the ClickHouse wire:
2SELECT
3  u.country,
4  e.event_name,
5  count(*) AS n,
6  count(DISTINCT e.user_id) AS unique_users,
7  countIf(e.properties.tier = 'premium') AS premium_count,
8  quantile(0.95)(e.duration_ms) AS p95_ms,
9  ROW_NUMBER() OVER (PARTITION BY u.country ORDER BY count(*) DESC) AS rank_in_country
10FROM events e
11  ALL INNER JOIN users u USING (user_id)
12WHERE e.ts >= now64(9, 'UTC') - INTERVAL 7 DAY
13  AND u.country IN ('US','UK','DE')
14  AND e.properties.platform = 'web'
15GROUP BY u.country, e.event_name
16ORDER BY n DESC
17LIMIT 100;
```

```

(Approximate; the exact `count(DISTINCT)` and `countIf` deparse have edge cases not shown here.)


The wire carries 100 rows. Postgres receives them and returns them. Compared to Step 1, where the wire carried tens of millions of rows, the difference is several orders of magnitude.


### Historical context [\#](/blog/postgres-fdw-pushdown-negotiation#historical-context)


The reaction we sometimes see, "I'm surprised this expression wasn't pushed down from day one," is what you get when you look at the list of v0\.2 changes without the context of history. Walking the query through that history surfaces a few facts that a simple list of changes does not, to whit:


- Pushdown is granular. Each clause must be independently negotiated. A clause that looks "obvious" can fail to push down because of a single sub\-expression: `count(*) FILTER (WHERE json_op)` waits on the JSON op even though count and FILTER are individually fine.
- Pushdown is all\-or\-nothing at the upper\-rel level. A grouped query can only be pushed down if the whole grouped relation can be represented safely in ClickHouse SQL. One unsupported aggregate or sub\-expression can block the entire grouped plan. Put another way, adding support for a small missing translation can unlock pushdown for the full query.
- Most "improvements" are translations, not new features. `percentile_cont`, `ROW_NUMBER`, `->>`. Postgres has them, ClickHouse has them. What was missing was the deparser code connecting the two grammars. Such improvements resemble new capabilities, but internally they're just new mappings in `custom_types.c` and the code to translate them.
- Some pushdowns get revoked. Both pg\_clickhouse and `postgres_fdw` have lists of pushdowns that were removed because they turned out to leak. In our v0\.2\.0 we revoked pushdown for `array_dims`, `array_lower` and friends. On the postgres\_fdw side, [`8cfbac1492b`](https://github.com/postgres/postgres/commit/8cfbac1492b) (PG 17\) refused `FETCH FIRST n WITH TIES`; [`5c571a34d0e`](https://github.com/postgres/postgres/commit/5c571a34d0e) (PG 18\) refused LIMIT pushdown where backward cursor scans would be required. This is the system working: better to pull back when we can't get the semantics right than to ship wrong rows fast.


If the deparse contract is violated, we error rather than guess


## Conclusion [\#](/blog/postgres-fdw-pushdown-negotiation#4-conclusion)


Pushdown looks binary from the outside: either a clause runs remotely, or it does not. Inside an FDW, it’s a contract. Postgres has to expose the right planner hook, pg\_clickhouse has to translate the expression without changing its meaning, and ClickHouse has to support the same semantics. If any part of that chain is missing, the safe answer is to keep the work local or to fail loudly.


Hence FDW work often looks incremental from the outside. JSON sub\-columns, percentile\_cont, filtered aggregates, window functions, join semantics, DML support: each represents a small agreement between two SQL systems. But once the last blocker to pushdown lifts, the effect is not small. A query that used to stream millions of rows into Postgres can collapse into a single ClickHouse SELECT that returns 100 rows.


Pushdown is not a race to ship every clause remotely. Some translations are added. Some are revoked. Some wait on Postgres planner support. Some wait on ClickHouse engine behavior. And some should never be pushed at all, because the remote system cannot honestly promise the same answer Postgres would produce.


The work is not to make ClickHouse pretend to be Postgres. The work is to decide, clause by clause, where the two systems can agree.


Every byte kept off the wire is a byte that all three parties have agreed to omit.

### Try Postgres managed by ClickHouse

ClickHouse \+ Postgres has become the unified data stack for applications that scale. With Managed Postgres now available in ClickHouse Cloud, this stack is a day\-1 decision.[Get access](https://clickhouse.com/cloud/postgres?loc=blog-cta-589-try-postgres-managed-by-clickhouse-get-access&utm_blogctaid=589)
pre code { white\-space: pre !important; }
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
