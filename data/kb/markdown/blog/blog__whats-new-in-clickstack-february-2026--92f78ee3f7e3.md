# What's new in ClickStack. February '26\.


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# What's new in ClickStack. February '26\.

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_white_add9f20d0f.png&w=96&q=75)[The ClickStack Team](/authors/the-clickstack-team)Mar 12, 2026 · 17 minutes readWelcome to the February edition of What’s New in ClickStack.


Each month, we share the latest updates across ClickStack, from platform enhancements to new features designed to make observability faster, simpler, and more powerful. February brings major improvements to both Cloud and open source, including new query workflows, enhanced metrics exploration, performance optimizations, and expanded alerting options.


A big thank you to our open source contributors, as well as to our users whose feedback helps shape these features and make ClickStack better for everyone.


## New contributors [\#](/blog/whats-new-in-clickstack-february-2026#new-contributors)


As always, a huge thank you to our open source contributors, including those who jumped in for the first time this month to help improve ClickStack for everyone.


[AdityaPimpalkar](https://github.com/AdityaPimpalkar) [Rajin9601](https://github.com/Rajin9601)[mlsalcedo](https://github.com/mlsalcedo) [themavik](https://github.com/themavik) [Misfits09](https://github.com/Misfits09) [Bre77](https://github.com/Bre77) [alex\-clickhouse](https://github.com/alex-clickhouse) [adri](https://github.com/adri) [mxmCherry](https://github.com/mxmCherry)


If code contributions are not your thing, we welcome documentation improvements, ideas, feature suggestions, bug reports, and general feedback. Every contribution, big or small, helps make the stack better for the entire community.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-98-get-started-today-sign-up&utm_blogctaid=98)## External API for ClickHouse Cloud [\#](/blog/whats-new-in-clickstack-february-2026#external-api-for-clickhouse-cloud)


For many teams, configuration as code is a hard requirement. The [ClickStack API](https://clickhouse.com/docs/use-cases/observability/clickstack/api-reference) has been available in open source for some time, and it has quickly become essential for enterprises that need to manage dashboards and alerts at any scale. This month, we are excited to bring that same capability to ClickHouse Cloud.


With ClickStack resources now available in the ClickHouse Cloud OpenAPI, you can manage dashboards, alerts, sources, and webhooks directly through the Cloud API. Observability configuration can live alongside your application code, flow through CI and CD pipelines, and remain consistent across development, staging, and production environments.


For example, listing all dashboards for a service is now as simple as:



```

```
1curl -X GET \
2  'https://api.clickhouse.cloud/v1/organizations/{organizationId}/services/{serviceId}/clickstack/dashboards' \
3  --user '<keyId>:<keySecret>' \
4  -H 'Content-Type: application/json'
```

```

No separate credentials are required. Existing ClickHouse Cloud API keys with the appropriate permissions work out of the box.


This is the first step toward fully automated, production\-grade observability workflows in ClickStack. We continue to expand resource coverage and Terraform support is planned. For full details and examples, see the [dedicated announcement](https://clickhouse.com/blog/clickstack-api) and [API reference](https://clickhouse.com/docs/use-cases/observability/clickstack/api-reference).


## ClickStack embedded in ClickHouse [\#](/blog/whats-new-in-clickstack-february-2026#clickstack-embedded-in-clickhouse)


This month, we made getting started with ClickStack easier than ever. With ClickHouse 26\.2, the ClickStack UI is embedded directly in the ClickHouse binary. Download ClickHouse or start a Docker container, open <http://localhost:8123/clickstack>, and you are ready to explore.



This embedded version is designed for local development, learning, and experimentation. It gives you a simple way to visualize your own observability data or even inspect ClickHouse itself using its internal logs and system tables.


![](/uploads/clickstack_feb2026_image1_3ef1e34fb9.png)
While it is not intended for production deployments, it is a powerful way to understand query performance, diagnose local issues, and explore how your instance behaves, all from a built\-in UI that ships with ClickHouse out of the box.


If you are curious how we package the UI directly into the ClickHouse binary without significantly increasing its size, adding only around 4\.1 MB, while integrating cleanly into the ClickHouse build system, we recommend reading the full [announcement blog post](https://clickhouse.com/blog/clickstack-embedded-clickhouse).


## Raw SQL tables [\#](/blog/whats-new-in-clickstack-february-2026#raw-sql-tables)


One of the most consistent pieces of feedback we hear is simple: “I just want to write SQL and chart it.”


From day one, ClickStack has focused on making visualizations easy to build. Line and bar chart builders, number tiles, pie charts (see below), search views, markdown, and guided workflows are all designed to help users create powerful dashboards without needing to write SQL. But every wizard has limits. Simplification makes common tasks fast, yet it can also hide some of the underlying power.


Because ClickStack is powered by ClickHouse, it sits on top of a fully featured, SQL compliant engine with a rich set of [analytical and aggregation functions](https://clickhouse.com/docs/sql-reference/aggregate-functions). That flexibility is one of its biggest strengths. Over the coming months, we will begin exposing native SQL across visualization types, giving users the choice between the builder for convenience and raw SQL for full control.


We are starting with tables. In the table visualization, users can now switch between the default Builder mode and a new SQL mode. From there, you can write a native SQL query directly, including referencing built\-in time range parameters for start and end timestamps.



> When the chart is added to a dashboard, the time variables are automatically injected, so your query stays dynamic and aligned with the selected time window.


This unlocks far more than simply writing longer or more complex queries than the table builder allows. The builder is intentionally opinionated. For tables, it focuses on grouping by a column and calculating metrics across the remaining fields. That works well for common workflows, but it cannot express more advanced analytical patterns.


With raw SQL, users can now join across datasets, correlate signals, and compute derived metrics that span multiple tables. For example, you might join logs to traces to compare total log volume, error counts, and average latency in a single result set.



```

```
1WITH
2  Traces AS (
3    SELECT
4      ServiceName,
5      avg(Duration) AS avg_duration,
6      quantile(0.99)(Duration) AS p99_duration
7    FROM otel_v2.otel_traces
8    WHERE
9      Timestamp >= fromUnixTimestamp64Milli({startDateMilliseconds:Int64})
10      AND Timestamp < fromUnixTimestamp64Milli({endDateMilliseconds:Int64})
11    GROUP BY ServiceName
12  ),
13  Errors AS (
14    SELECT
15      ServiceName,
16      countIf(SeverityText = 'error') AS error_log_count
17    FROM otel_v2.otel_logs
18    WHERE
19      TimestampTime >= fromUnixTimestamp64Milli({startDateMilliseconds:Int64})
20      AND TimestampTime <= fromUnixTimestamp64Milli({endDateMilliseconds:Int64})
21      AND SeverityText = 'error'
22    GROUP BY ServiceName
23  )
24SELECT
25  coalesce(Traces.ServiceName, Errors.ServiceName) AS ServiceName,
26  avg_duration,
27  p99_duration,
28  error_log_count
29FROM Traces
30FULL OUTER JOIN Errors
31  ON Traces.ServiceName = Errors.ServiceName
32ORDER BY ServiceName
33LIMIT 200;
```

```

![](/uploads/clickstack_feb2026_image4_27bbe951f5.png)

> In raw SQL mode, users select just a connection. There's no need to specify a data source, unlike the Query Builder, with users free to query across multiple data sources at once.


Or consider a lightweight service map style view. A self JOIN on spans can show request counts between service pairs, total errors, and percentage error rates (also available visually within [our service map feature](https://clickhouse.com/blog/whats-new-in-clickstack-november-2025#service-maps)). This kind of relationship analysis would be extremely difficult to model coherently in a visual builder, but is straightforward in SQL:



```

```
1WITH
2  ServerSpans AS (
3    SELECT TraceId AS traceId,
4           SpanId AS spanId,
5           ServiceName AS serviceName,
6           ParentSpanId AS parentSpanId,
7           StatusCode AS statusCode
8    FROM otel_v2.otel_traces
9    WHERE SpanKind IN ('Server', 'Consumer', 'SPAN_KIND_SERVER', 'SPAN_KIND_CONSUMER') AND
10     Timestamp >= fromUnixTimestamp64Milli({startDateMilliseconds:Int64})
11      AND Timestamp < fromUnixTimestamp64Milli({endDateMilliseconds:Int64})
12  ),
13  ClientSpans AS (
14    SELECT TraceId AS traceId,
15           SpanId AS spanId,
16           ServiceName AS serviceName,
17           ParentSpanId AS parentSpanId,
18           StatusCode AS statusCode
19    FROM otel_v2.otel_traces
20    WHERE SpanKind IN ('Client', 'Producer', 'SPAN_KIND_CLIENT', 'SPAN_KIND_PRODUCER') AND 
21    Timestamp >= fromUnixTimestamp64Milli({startDateMilliseconds:Int64})
22      AND Timestamp <= fromUnixTimestamp64Milli({endDateMilliseconds:Int64})
23  )
24SELECT
25  ServerSpans.serviceName AS serverServiceName,
26  ClientSpans.serviceName AS clientServiceName,
27  count(*) * 10 AS requestCount,
28  countIf(ServerSpans.statusCode = 'Error') AS error_count,
29  round(error_count / requestCount, 3) AS `% error count`
30FROM ServerSpans
31LEFT JOIN ClientSpans
32  ON ServerSpans.traceId = ClientSpans.traceId
33  AND ServerSpans.parentSpanId = ClientSpans.spanId
34WHERE ClientSpans.serviceName IS NULL
35   OR ServerSpans.serviceName != ClientSpans.serviceName
36GROUP BY serverServiceName, clientServiceName
37ORDER BY serverServiceName, clientServiceName;
```

```

![](/uploads/clickstack_feb2026_image6_5a88b2c3c7.png)
This is the first step toward combining the simplicity of guided builders with the full expressiveness of SQL, giving advanced users the freedom to unlock everything ClickHouse can do. Stay tuned over the following months to see SQL being exposed in other visualizations.


## Metric Attribute Explorer [\#](/blog/whats-new-in-clickstack-february-2026#metric-attribute-explorer)


ClickStack has long supported OpenTelemetry metrics (similar to Prometheus in concept), stored as separate tables per data type, such as gauges and counters. While this model is flexible and powerful, discovering how to work with metrics and their associated labels has often required a degree of trial and error.


In this release, we have made metric discovery more intuitive. Users typically know which metric they want to plot and can select it using autocomplete as before. Now, once a metric is selected, they can expand an associated attributes panel that displays the labels available for that specific metric. Instead of guessing which labels exist, users can immediately see and select them.

Loading video...In the example above, we first plot an average of the `k8s.pod.memory.working_set (Gauge)` metric. We're immediately told this has 44 associated attributes. We expand the attributes panel and select the `k8s.deployment.name` label. From there, the label can either be applied as a filter to narrow the chart or added as a group to break the metric down by Kubernetes deployment. In this case, we group by deployment to compare working set size across services.


This streamlined flow removes much of the guesswork from metrics exploration. Users no longer need to manually experiment to discover which labels are available for grouping or filtering. Charting OpenTelemetry metrics becomes a more direct, visual process, focused on insight rather than label discovery.


## Pie charts [\#](/blog/whats-new-in-clickstack-february-2026#pie-charts)


One of the most frequent requests we receive is for a broader set of visualization types. Expanding charting capabilities has been on our backlog for some time, and over the coming months we will continue closing those gaps, prioritizing the visualizations users ask for most.


Pie charts are one of the more [controversial chart types in analytics](https://www.ataccama.com/blog/why-pie-charts-are-evil), yet they remain a popular choice in observability. While they are not suited to every scenario, they can still be effective for showing proportional breakdowns, such as status codes, error categories, or request distribution across services.


Pie charts are now available in the latest version of ClickStack. To build one, users simply select a metric to define the slice size and then choose a group by field to determine how the slices are segmented. The distinct values of that field form each slice of the chart. As with other visualizations, filters can be applied to narrow the dataset before rendering.


![](/uploads/clickstack_feb2026_image3_c4dfca64e0.png)
Pie charts are supported across traces, logs, and OpenTelemetry metrics, and they benefit from the same [accelerated materialized view support](https://clickhouse.com/docs/use-cases/observability/clickstack/materialized_views) introduced earlier this year. This ensures that even high\-volume breakdowns remain responsive and performant.


## Settings for even faster querying [\#](/blog/whats-new-in-clickstack-february-2026#settings-for-even-faster-querying)


We are constantly looking for ways to improve query performance in ClickStack. Sometimes that means leveraging the [right access patterns](https://clickhouse.com/blog/whats-new-in-clickstack-september-2025#chunking-time-windows) or ensuring users can [exploit features such as materialized views](https://clickhouse.com/docs/use-cases/observability/clickstack/materialized_views). Often, however, it just comes down to ensuring the correct query settings and optimizations are applied when appropriate.


The ClickHouse core team ships performance improvements and new optimizations in every release. Tracking these changes and ensuring ClickStack takes advantage of them is an ongoing priority. Recent updates in ClickHouse have unlocked meaningful performance gains, and we now enable several of these optimizations when appropriate and when they are supported by the underlying ClickHouse version.


The following optimizations are now automatically applied where appropriate.


### Top N Queries [\#](/blog/whats-new-in-clickstack-february-2026#top-n-queries)


Top N queries are everywhere in observability. “Show me the latest logs.” “Give me the top error messages.” “List the slowest requests.” These patterns typically look like `ORDER BY … LIMIT N`, and they are especially common in log search and ranking\-style dashboards.


ClickHouse has recently introduced powerful optimizations that treat Top\-N as a first\-class query pattern. In 25\.12, support for skip\-index\-driven Top\-K filtering was added via the `use_skip_indexes_for_top_k` setting. This allows ClickHouse to use min/max metadata from data skipping indexes to eliminate entire granules before any rows are read. Instead of scanning a full table and then sorting, the engine can prune large portions of data up front. In benchmarks for ClickStack, this has delivered 2x to 3x improvements for typical log search style queries, and in some cases much more.



ClickStack now enables `use_skip_indexes_for_top_k = 1` by default when supported, along with `query_plan_max_limit_for_top_k_optimization` (set to `100000`) to allow the optimization to kick in for sufficiently large result scans. When the `ORDER BY` aligns with the table’s ordering key, pruning is highly effective because granules can be skipped purely based on metadata.



> When the sort column is not part of the ordering key, ClickHouse can still apply a dynamic Top\-N threshold during execution, skipping granules that cannot improve the result set via `use_top_k_dynamic_filtering = 1`, delivering up to 2x improvements in some real\-world log searches depending on data distribution and predicates; however, this is **not yet enabled** globally in ClickStack because features such as Event Patterns rely on functions like `rand()` that are incompatible with the optimization. We plan to enable it selectively in the near future.


These settings turn many Top\-N queries into a metadata pruning problem rather than a full table scan. As datasets grow and cold cache scenarios become more common, avoiding unnecessary reads at the granule level becomes increasingly impactful, and ClickStack now takes advantage of this automatically.


For a deep dive on these features, we recommend our [dedicated blog post.](https://clickhouse.com/blog/clickhouse-top-n-queries-granule-level-data-skipping)


### Faster skip indices [\#](/blog/whats-new-in-clickstack-february-2026#faster-skip-indices)


ClickStack already relies heavily on ClickHouse [data skipping indexes](https://clickhouse.com/docs/optimize/skipping-indexes/examples) to accelerate common observability workloads. Bloom filter indexes power fast text search across logs. Minmax indexes are widely used to accelerate numeric range queries, especially on timestamps and other high cardinality fields. Users are [encouraged to exploit these indices](https://clickhouse.com/docs/use-cases/observability/clickstack/performance_tuning#adding-skip-indices) if they need to perform schema optimization.


Before ClickHouse 25\.9, skip indexes such as minmax, set, bloom filter, vector, and more [recently text](https://clickhouse.com/blog/full-text-search-ga-release) were evaluated up front, before any table data was read. This sequential approach had a few important drawbacks. Queries with LIMIT still had to scan the entire index before execution could begin. There was an initial startup delay while index analysis completed. In some cases, scanning the index itself could cost more than processing the data.


ClickHouse 25\.9 introduced streaming evaluation of secondary indexes. Instead of scanning the entire index first, ClickHouse now interleaves index checks with data reads. When the engine is about to read a granule, it first consults the corresponding index entry. If the index shows the granule can be skipped, it is never read. If not, the granule is processed while index evaluation continues for subsequent granules. For LIMIT queries, execution stops as soon as enough rows are found, and both index checks and data reads halt immediately.


This change removes startup delays and avoids unnecessary work. In testing on a 1 billion row table with a bloom filter index larger than 2 GiB, a simple LIMIT 1 query ran more than 4x faster with streaming indexes enabled, dropping from around 10 seconds to roughly 2\.4 seconds.


This feature is controlled by the `use_skip_indexes_on_data_read` setting (defaults to 1 from 25\.12\) but enforced by ClickStack from 25\.9\.


Read the [full deep\-dive on streaming support for skip indices](https://clickhouse.com/blog/clickhouse-release-25-09#streaming-for-secondary-indices).


### Using skip indices for disjunctions [\#](/blog/whats-new-in-clickstack-february-2026#using-skip-indices-for-disjunctions)


Prior to 25\.12, skip indexes were applied primarily to simple predicates or conjunctions such as AND clauses, allowing ClickHouse to prune granules and reduce unnecessary data reads. Disjunctions, such as OR conditions, did not benefit from index pruning. With newer releases, skip indexes can now also be applied to disjunctive queries, enabling pruning even when queries contain OR logic.


This behavior is controlled by `use_skip_indexes_for_disjunctions`, which is enabled by default. As a result, ClickStack automatically benefits from improved pruning and reduced data scans for a wider range of real\-world query patterns.


### Lazy materializations [\#](/blog/whats-new-in-clickstack-february-2026#lazy-materializations)


ClickHouse has long relied on layered I/O optimizations such as columnar storage, primary and secondary indexes, projections, and PREWHERE to reduce the amount of data read from disk. Traditionally, once rows passed the WHERE clause, all referenced columns for those rows would be loaded before operations such as sorting, aggregation, or LIMIT were applied. In many analytical queries, especially Top\-N patterns, this meant reading large columns that were ultimately unnecessary for producing the final result.


Lazy materialization, introduced in ClickHouse 25\.4 and enabled by default, changes this behavior. Instead of eagerly loading all selected columns, ClickHouse defers reading columns until they are actually required by the execution plan. For example, when a query performs an `ORDER BY … LIMIT`, the engine can first determine the top rows using only the ordering column, and only then read the remaining columns for those final rows. This reduces I/O, memory usage, and latency, particularly for wide tables or queries returning a small number of rows from very large datasets. If you're curious as to the internals and looking for a deep dive, we recommend the excellent blog post [“ClickHouse gets lazier (and faster): Introducing lazy materialization”](https://clickhouse.com/blog/clickhouse-gets-lazier-and-faster-introducing-lazy-materialization#speed-without-filters-lazy-materialization-in-isolation).


Since this optimization was default since 25\.4, users have been enjoying this for some time. However, this optimization is only applied if the limit is below a specified threshold [`query_plan_max_limit_for_lazy_materialization`](https://clickhouse.com/docs/operations/settings/settings#query_plan_max_limit_for_lazy_materialization). By default, this has a value of 10,000\.


In our own testing against typical ClickStack access patterns for log and trace search, we observed that result sets up to 100,000 rows still benefit significantly from lazy materialization \- in large part to [recent changes which make further optimizations to this feature](https://clickhouse.com/blog/clickhouse-release-25-12#what-changed-in-2512). As a result, in the latest version of ClickStack, we increase this threshold to 100,000 to extend the performance gains to a broader range of real\-world queries.


## Alerts on number charts [\#](/blog/whats-new-in-clickstack-february-2026#alerts-on-number-charts)


We continue to expand alerting capabilities in ClickStack. Last year, we introduced [alerts on saved searches and charts](https://clickhouse.com/docs/use-cases/observability/clickstack/alerts). In the latest release, users can now create alerts directly on number charts as well.


This is ideal for simple, static threshold\-based alerting. For example, if a number tile represents an error rate, request volume, latency, or any other key metric, you can now trigger an alert when it crosses a defined threshold. The workflow is consistent with existing alerting, making it straightforward to apply to existing dashboards.

Loading video...This is a small but practical addition, and part of a broader effort to make alerting more flexible and powerful. Expect more advanced alerting capabilities in upcoming releases.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
