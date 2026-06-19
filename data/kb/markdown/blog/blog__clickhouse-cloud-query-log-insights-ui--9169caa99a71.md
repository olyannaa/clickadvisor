# Building a UI for Query Insights


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Building a UI for Query Insights

![](/_next/image?url=%2Fuploads%2FBucky_Schwarz_90b6dcc55f.png&w=96&q=75)Bucky SchwarzJul 1, 2024 · 7 minutes readWe recently released an initial implementation of Query Insights, which gives ClickHouse Cloud users a turnkey way to view and interpret the query log. This feature is available to all ClickHouse Cloud users, and this post discusses what it does and how we built it.


### Why build a query log UI? [\#](/blog/clickhouse-cloud-query-log-insights-ui#why-build-a-query-log-ui)


The system.query\_log table in a ClickHouse instance contains valuable data that can help users understand things like:


- Query performance and anomalies;
- Errors and related heuristics (exception codes, messages, settings, profile events, etc.); and
- Time\-series query metrics (read/write throughput, volume, and latency over time)


Collecting this information does, however, pose a problem—system.query\_log currently contains more than 70 fields (full list [here](https://clickhouse.com/docs/en/operations/system-tables/query_log)) and two or more records are produced for each query. Interpreting query log data can therefore be difficult, especially for users who are less familiar with ClickHouse.


To illustrate this point, let’s take a look at the output of a simple `select * from system.query_log` in the CLI:


![query_insights_ui_01.png](/uploads/query_insights_ui_01_9fcf7c7c28.png)
The SQL console in ClickHouse Cloud slightly improves upon this (at least visually), but unless you already know exactly what information you’re looking for, the experience is still not very intuitive:


![query_insights_ui_02.png](/uploads/query_insights_ui_02_271c05ebb5.png)
Adding slightly more complexity, every ClickHouse Cloud service contains at least two replicas, each with its own replica\-specific version of the query log, meaning that simply running `select * from system.query_log` will only return results from the replica assigned to this query. As a result, each time a ClickHouse Cloud user (or broadly any ClickHouse user running a multi\-replica deployment) wants to inspect the query log, it is necessary to use the `clusterAllReplicas()` function, which is similarly unintuitive for less\-experienced users. This leads us to our first (and most obvious) top\-level goal for a query log UI:


- **Goal \#1** — make query log data more interpretable and accessible


As previously mentioned, the query log is a key source of information for query optimization, debugging, and monitoring overall cluster health and performance. Beyond simply improving the accessibility of query log data, considering how (and when) the query log is useful informed our other top\-level goals for this new feature:


- **Goal \#2** — expose important top\-level query metrics
- **Goal \#3** — simplify query debugging and optimization workflows that utilize the query log
- **Goal \#4** — expose context\-based ‘intelligent’ suggestions and insights from the query log, further simplifying query debugging and optimization


### Taking an iterative approach [\#](/blog/clickhouse-cloud-query-log-insights-ui#taking-an-iterative-approach)


When we began scoping out work for this feature, we determined that the first two goals stated above could be accomplished rather quickly and would serve to address substantial points of friction for our users. On the other hand, the latter two goals were (and are) still amorphous, requiring additional research and a deeper understanding of how and when different query log metrics/indicators are important. As a result, we decided to release an initial version as quickly as possible that addresses goals \#1 and \#2 and lays the groundwork for incremental improvements towards goals \#3 and \#4\. **Importantly, future iterative work will be premised upon user feedback. If you’re reading this, please try out our new Query Insights UI and give us feedback!**


### Query Insights V1 [\#](/blog/clickhouse-cloud-query-log-insights-ui#query-insights-v1)


After selecting a service, the monitoring navigation item in the left sidebar should expand to reveal a new ‘Query insights’ sub\-item. Clicking on this option opens the new Query insights page:


![query_insights_ui_03.png](/uploads/query_insights_ui_03_898f130541.png)
#### Top\-level metrics [\#](/blog/clickhouse-cloud-query-log-insights-ui#top-level-metrics)


The stat boxes at the top represent some basic top\-level query metrics over the selected period of time. Beneath it, we’ve exposed three time\-series charts representing query volume, latency, and error rate broken down by query kind (select, insert, other) over a selected time window. The latency chart can be further adjusted to display p50, p90, and p99 latencies:


![query_insights_ui_04.png](/uploads/query_insights_ui_04_c8ecc7d6fa.png)
#### Recent queries [\#](/blog/clickhouse-cloud-query-log-insights-ui#recent-queries)


Beneath the top\-level metrics, a table displays query log entries (grouped by normalized query hash and user) over the selected time window:


![query_insights_ui_05.png](/uploads/query_insights_ui_05_b27dd0d9ac.png)
Recent queries can be filtered and sorted by any available field, and the table can be configured to display/hide additional fields (tables, p90 and p99 latencies).


#### Query drill\-down [\#](/blog/clickhouse-cloud-query-log-insights-ui#query-drill-down)


Selecting a query from the recent queries table will open a flyout containing metrics and information specific to the selected query:


![query_insights_ui_06.png](/uploads/query_insights_ui_06_1047015bf1.png)
As we can see from the flyout, this particular query has been run more than 3000 times in the last 24 hours. All metrics in the ‘query info’ tab are aggregate, but we can also view metrics from individual runs by selecting the ‘Query history’ tab:


![query_insights_ui_07.png](/uploads/query_insights_ui_07_d6845c13ad.png)
### A peek behind the curtain [\#](/blog/clickhouse-cloud-query-log-insights-ui#a-peek-behind-the-curtain)


Query insights was the first real project I had the opportunity to work on after joining ClickHouse in late February. I'd spent the first few weeks doing small tasks and bug fixes to get familiar with the codebase and processes before being asked to work on this feature. It speaks to the trust and confidence my team has in me, and in our hiring process \- high standards in hiring allow us to know that people who get hired are capable of the work they're given and will be able to hit the ground running.


The feature and what it was supposed to accomplish was fairly well specified and designed, but the details and implementation were left to me. I was working from a Figma design showing a fairly generic chart and affordances for displaying different types of data (like All Queries, Errors, and Slow queries). Implementation primarily comprised separating the queries from the visualization code with some well\-defined interfaces. These interfaces allowed the data passed into the queries (things like time ranges and whether we're querying for latency or errors) to change without affecting the chart rendering code.


By this point in my career, I've learned that mocking up a feature and seeing it in action are two different things, and that our collective understanding of what software needs will change over time. With this in mind, I approached this project by trying to make the initial draft as narrowly\-scoped as possible (yet still usable), and then demoing the feature to various internal and external users—a pretty standard way of developing web applications. This allowed any changes that were going to occur to be fairly easy to implement. I mentioned Slow queries earlier; after some usage by early stakeholders, we decided the idea of slow queries didn't make much sense so we nixed it and replaced it with p99, p90, and p50 latency. We also realized that the flyout that displays when clicking on a table doesn't work very well, and so that was almost completely redesigned. None of this was a big deal because this was developed expecting things to change, and so abstractions and interfaces were put in place to allow this to happen painlessly.


### Try it yourself! [\#](/blog/clickhouse-cloud-query-log-insights-ui#try-it-yourself)


This feature is now available to all existing ClickHouse Cloud users under Monitoring \>\> Query Insights. If you are not yet using ClickHouse Cloud, you can try it today by signing up for a 30\-day trial with $300 free credits [here](https://clickhouse.cloud/signUp).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
