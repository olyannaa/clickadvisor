# ClickStack SQL Charting and Alerting


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickStack SQL Charting and Alerting

![](/_next/image?url=%2Fuploads%2Fdrew_ea86095aa0.png&w=96&q=75)![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Drew Davis](/authors/author) and [Dale McDiarmid](/authors/dale-mcdiarmid)May 13, 2026 · 11 minutes read## Introduction [\#](/blog/clickstack-sql-charting-and-alerting#introduction)


Today, we’re introducing SQL\-based visualizations and SQL\-based alerting in ClickStack. Users can now build charts and alerts using arbitrary ClickHouse SQL queries, unlocking far more advanced analysis directly inside the ClickStack UI.
SQL\-based visualizations enable users to move beyond predefined query builders and fully leverage ClickHouse SQL for dashboards and exploratory analysis. SQL\-based alerting extends this further, allowing anything expressible in SQL to serve as an alert condition, from rolling averages and anomaly detection to grouped statistical checks and custom operational logic.
In this post, we’ll explore why we built these capabilities, how they change the observability workflow, and walk through some examples that demonstrate where SQL\-driven analysis and alerting become especially powerful.


## The first step: SQL\-powered charting [\#](/blog/clickstack-sql-charting-and-alerting#the-first-step-sql-powered-charting)


The journey to SQL\-based charts and alerts started with a simple observation: while query builders are excellent for common workflows, advanced users almost always outgrow them.


As observability use cases mature, teams want to compute rolling baselines, build statistical anomaly detection, correlate events, calculate SLOs, and express logic that doesn’t cleanly map to predefined UI controls. While query builders are useful for getting started, they inevitably trade flexibility for simplicity.


![99th_by_service.png](/uploads/99th_by_service_2a37d86d3b.png)
*Query builders are inherently limited and only ever cover a subset of user query requirements*


Because ClickStack is built on ClickHouse, supporting raw SQL felt like a natural extension of the platform rather than a bolt\-on feature. SQL charts allow users to leverage the same expressive analytical capabilities that make ClickHouse so powerful while still integrating directly into dashboards, filters, and visualizations.


While SQL\-based visualizations can be used for simple charts, their real value lies in helping users move beyond straightforward aggregations and apply richer analytical logic directly within their observability workflows.

### Get started today

Interested in seeing how ClickStack works for your observability data? Get started with ClickStack in ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?intent=o11y&loc=blog-cta-566-get-started-today-sign-up&utm_blogctaid=566)### Example \- Detecting anomalies with rolling baselines [\#](/blog/clickstack-sql-charting-and-alerting#example---detecting-anomalies-with-rolling-baselines)


One of the most common requests from advanced observability teams is the ability to visualize anomalies relative to recent system behavior rather than static thresholds. For example, a checkout endpoint taking 800ms may be normal during peak traffic, but highly abnormal for a lightweight internal service.


With SQL\-based charting, users can build rolling averages and standard deviation baselines directly into their queries using ClickHouse window functions. Instead of visualizing only raw latency, charts can show when latency deviates from its expected range over time for a service.


```
1WITH buckets AS (
2  SELECT
3    toStartOfInterval(
4      Timestamp,
5      INTERVAL {intervalSeconds:Int64} second
6    ) AS ts,
7    ServiceName,
8    quantile(0.95)(Duration) / 1000000 AS p95_latency_ms
9  FROM $__sourceTable
10  WHERE Timestamp >= fromUnixTimestamp64Milli({startDateMilliseconds:Int64})
11    AND Timestamp < fromUnixTimestamp64Milli({endDateMilliseconds:Int64})
12    AND SpanKind = 'Server'
13    AND $__filters
14  GROUP BY
15    ts,
16    ServiceName
17),
18
19baselines AS (
20  SELECT
21    ts,
22    ServiceName,
23    p95_latency_ms,
24    avg(p95_latency_ms) OVER (
25      PARTITION BY ServiceName
26      ORDER BY ts
27      ROWS BETWEEN 12 PRECEDING AND 1 PRECEDING
28    ) AS rolling_avg_latency_ms,
29    stddevPop(p95_latency_ms) OVER (
30      PARTITION BY ServiceName
31      ORDER BY ts
32      ROWS BETWEEN 12 PRECEDING AND 1 PRECEDING
33    ) AS rolling_stddev_latency_ms
34  FROM buckets
35)
36
37SELECT
38  ts,                                      -- Timestamp column
39  ServiceName,                             -- Group name column
40  p95_latency_ms,                          -- Series value column
41  rolling_avg_latency_ms,                  -- Series value column
42  rolling_avg_latency_ms
43    + 3 * rolling_stddev_latency_ms
44      AS upper_bound_latency_ms            -- Series value column
45FROM baselines
46WHERE rolling_avg_latency_ms IS NOT NULL
47ORDER BY ts ASC
48
```
This produces a time\-series chart where ts is used as the timestamp column, ServiceName is treated as the group column, and each numeric column is plotted as a separate series. The chart shows current p95 latency, the rolling average, and an upper statistical boundary for each service.


![sql-chart.png](/uploads/sql_chart_f45569e162.png)
This allows teams to see whether latency is moving outside its recent baseline, rather than relying on a fixed threshold that may be too sensitive for one workload and too permissive for another. This type of analysis is extremely difficult to express in traditional query builders because it requires window functions, historical baselines, percentile calculations, grouped time\-series logic, and multi\-stage query composition. With raw SQL, these workflows become straightforward.


Some astute readers may have noticed that the previous SQL query includes macros for the query time range, dashboard filters, and source table selection. Users coming from Grafana may also find these macros very familiar…


### Allowing dynamic SQL charts [\#](/blog/clickstack-sql-charting-and-alerting#allowing-dynamic-sql-charts)


While static SQL queries are useful, observability dashboards still need to remain dynamic and interactive. Charts need to automatically respond to dashboard time ranges, intervals, and filters, without users having to manually rewrite queries every time the dashboard changes.


This is where query parameters and macros become critical.


Query parameters expose dashboard state directly to the SQL query. These include values such as the dashboard start time, end time, and interval size. They use ClickHouse parameter syntax such as `{startDateMilliseconds:Int64}` and `{intervalSeconds:Int64}` and allow queries to dynamically adapt to the active dashboard context.


Macros build on top of these parameters and provide shorthand expressions for common observability workflows. For example, macros such as `$__filters` and `$__sourceTable` automatically inject dashboard filters and source table references directly into the query. Time\-filtering and bucketing macros further simplify the creation of dynamic time\-series visualizations.


One of our goals when building SQL\-based visualizations was to make the experience feel immediately familiar to existing Grafana and ClickHouse users. As a result, many of the supported macros intentionally mirror the conventions used by the [ClickHouse Grafana plugin](https://github.com/grafana/clickhouse-datasource). In many cases, users can bring existing SQL queries directly from Grafana into ClickStack and have them work with minimal or no modification.


This compatibility is an important design philosophy for us. Teams already invest significant time building operational queries, dashboards, and alerting logic, and we wanted SQL\-based visualizations to integrate naturally into existing workflows rather than forcing users to rewrite everything from scratch.


These macros also ensure that SQL charts remain fully interactive inside dashboards. When a user changes the dashboard time range, applies a filter, or switches the underlying source, the SQL query automatically adapts to reflect the new context.


Considering the previous visualization and query, if we apply a dashboard time range and service\-level filter, the macros automatically inject the corresponding SQL conditions into the query execution while preserving the visualization logic.

Loading video...For users interested in the full list of supported macros and query parameters, see the SQL\-based visualizations documentation: [SQL\-based visualizations documentation](https://clickhouse.com/docs/use-cases/observability/clickstack/dashboards/sql-visualizations?utm_source=chatgpt.com).


### Charting query results [\#](/blog/clickstack-sql-charting-and-alerting#charting-query-results)


While SQL\-based visualizations provide full flexibility over query logic, ClickStack still needs to understand how returned query columns should map onto visualization elements. This mapping depends on both the visualization type and the data types returned by the query itself. For example, for Line and Stacked Bar charts, the first `Date` or `DateTime` column is interpreted as the timestamp axis, with numeric columns plotted as series values, and String, `Map`, and `Array` columns are treated as grouping dimensions, allowing separate lines or bars to be rendered per group.


Other visualization types, such as Pie, Number, and Table charts, use slightly different mapping rules. For a complete breakdown of how query results are interpreted across visualization types, see the documentation section on [how query results are plotted](https://clickhouse.com/docs/use-cases/observability/clickstack/dashboards/sql-visualizations#how-results-are-plotted).


## The next step: SQL\-powered alerting [\#](/blog/clickstack-sql-charting-and-alerting#the-next-step-sql-powered-alerting)


While SQL\-powered charting dramatically expands what users can visualize, SQL\-powered alerting is where the real operational impact emerges.


Last year, we introduced [native alerting support in ClickStack](https://clickhouse.com/blog/alerting-arrives-in-clickstack-for-clickhouse-cloud) with integrations for platforms such as PagerDuty and Incident.io, allowing teams to build alerts directly from searches and charts. This made it easy to define threshold\-based alerts over logs, traces, and metrics directly inside ClickStack.


But ultimately, alerting is only ever as expressive as the query capabilities beneath it.


Traditional threshold alerts work well for straightforward conditions, but observability teams increasingly want to alert on more advanced operational patterns. They want to detect anomalies relative to rolling baselines, identify sudden changes in behavior, correlate multiple signals together, or build alerts based on statistical analysis rather than fixed values.


Historically, this often forced teams to maintain separate tooling, such as Grafana, solely for advanced alerting workflows, even though ClickHouse was already their primary observability datastore.


SQL\-based alerting is the natural evolution of SQL\-powered charting. Once users can express arbitrary analytical logic in SQL visualizations, they can apply that same power directly to alerting.


While SQL alerts can still be used for richer threshold\-based conditions, such as alerting on rolling averages or dynamically calculated baselines, the real power comes from moving the complexity into the query itself rather than the threshold configuration.


![sql-chart-alert.png](/uploads/sql_chart_alert_f3287f11d8.png)
Instead of returning a raw metric and comparing it against a static threshold, SQL queries can encapsulate the entire alerting decision. A query can look back over previous time windows, calculate statistical boundaries, compare historical behavior, and ultimately return a binary result such as 1 or 0, indicating whether an alert condition should fire.


This fundamentally changes how alerting logic can be expressed. Rather than configuring increasingly complex threshold rules, users can leverage the full analytical power of ClickHouse directly inside the query itself.


### Example: anomaly detection with lagging averages [\#](/blog/clickstack-sql-charting-and-alerting#example-anomaly-detection-with-lagging-averages)


For example, consider detecting sudden spikes in error volume relative to historical behavior.
Rather than alerting when error counts exceed a fixed threshold, we can instead calculate a rolling average and standard deviation over previous intervals, then determine whether the current bucket deviates significantly from its recent baseline.


```
1WITH buckets AS (
2  SELECT
3    toStartOfInterval(
4      Timestamp,
5      INTERVAL {intervalSeconds:Int64} second
6    ) AS ts,
7    countIf(StatusCode = 'Error') AS error_count
8  FROM $__sourceTable
9  WHERE Timestamp >= fromUnixTimestamp64Milli({startDateMilliseconds:Int64})
10        - toIntervalSecond({intervalSeconds:Int64} * 30)
11    AND Timestamp < fromUnixTimestamp64Milli({endDateMilliseconds:Int64})
12    AND SpanKind = 'Server'
13    AND $__filters
14  GROUP BY ts
15  ORDER BY ts
16),
17
18baselines AS (
19  SELECT
20    ts,
21    error_count,
22    avg(error_count) OVER (
23      ORDER BY ts
24      ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
25    ) AS rolling_avg,
26    stddevPop(error_count) OVER (
27      ORDER BY ts
28      ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
29    ) AS rolling_stddev
30  FROM buckets
31)
32
33SELECT
34  ts,
35  if(
36    error_count > rolling_avg + (2 * rolling_stddev),
37    1,
38    0
39  ) AS anomaly_detected
40FROM baselines
41WHERE rolling_avg IS NOT NULL
42ORDER BY ts ASC
```
*This query first buckets failed requests into time intervals and calculates the total error count for each interval. It then computes a rolling average and standard deviation across the previous 30 intervals using ClickHouse window functions. Finally, the query compares the current error count against this rolling baseline and returns 1 when the current interval exceeds the rolling average by more than two standard deviations; otherwise returning 0\.*


Here, the SQL query itself fully encapsulates the alerting logic. Rather than visualizing raw error counts and configuring a fixed threshold externally, the query determines whether the current interval represents a statistically significant anomaly relative to recent history.


The alert configuration itself then becomes extremely simple. If the query returns 1, the alert fires.


This approach unlocks a dramatically wider range of alerting strategies because the complexity lives inside SQL rather than inside a constrained alert configuration model.


![threshold_alerting.png](/uploads/threshold_alerting_9dffb1f964.png)
### Alerting on query results [\#](/blog/clickstack-sql-charting-and-alerting#alerting-on-query-results)


SQL\-based alerts work by inspecting the results returned from a SQL query and determining which values should be evaluated against the configured threshold. For time\-series visualizations such as Line and Stacked Bar charts, ClickStack identifies the returned timestamp column as the evaluation bucket and independently evaluates the final numeric column returned by the query for each interval. Any non\-numeric columns are treated as grouping dimensions, allowing alerts to trigger independently per service, environment, or other grouping key. See [our documentation](https://clickhouse.com/docs/use-cases/observability/clickstack/alerts#sql-result-interpretation) for the full rules on when alerts will fire.


Just like SQL\-based visualizations, SQL [alert queries fully support query parameters](https://clickhouse.com/docs/use-cases/observability/clickstack/alerts#query-params) and macros. This ensures alerts remain dynamic and automatically adapt to dashboard time ranges, evaluation intervals, and filters. In most cases, queries should include both interval macros and time\-range filters so that alert evaluations remain scoped to the configured execution window rather than scanning the entire dataset during every alert run.


## Conclusion [\#](/blog/clickstack-sql-charting-and-alerting#conclusion)


SQL\-based alerting is the natural evolution of SQL\-powered charting. Once users can express arbitrary analytical logic inside visualizations, extending those same capabilities into alerting becomes the obvious next step.

### Subscribe to our observability newsletter

Stay informed on ClickStack feature releases, the product roadmap, and observability\-related ClickHouse news.Loading form...Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
