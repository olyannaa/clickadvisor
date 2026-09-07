---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Building
topic: building-a-ui-for-query-insights-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 3
total_chunks_in_doc: 5
---

incremental improvements towards goals \#3 and \#4\. **Importantly, future iterative work will be premised upon user feedback. If you’re reading this, please try out our new Query Insights UI and give us feedback!** ### Query Insights V1 \#

After selecting a service, the monitoring navigation item in the left sidebar should expand to reveal a new ‘Query insights’ sub\-item. Clicking on this option opens the new Query insights page:

![query_insights_ui_03.png](/_next/image?url=%2Fuploads%2Fquery_insights_ui_03_898f130541.png&w=2048&q=75)

#### Top\-level metrics \#

The stat boxes at the top represent some basic top\-level query metrics over the selected period of time. Beneath it, we’ve exposed three time\-series charts representing query volume, latency, and error rate broken down by query kind (select, insert, other) over a selected time window. The latency chart can be further adjusted to display p50, p90, and p99 latencies:

![query_insights_ui_04.png](/_next/image?url=%2Fuploads%2Fquery_insights_ui_04_c8ecc7d6fa.png&w=2048&q=75)

#### Recent queries \#

Beneath the top\-level metrics, a table displays query log entries (grouped by normalized query hash and user) over the selected time window:

![query_insights_ui_05.png](/_next/image?url=%2Fuploads%2Fquery_insights_ui_05_b27dd0d9ac.png&w=2048&q=75)

Recent queries can be filtered and sorted by any available field, and the table can be configured to display/hide additional fields (tables, p90 and p99 latencies).

#### Query drill\-down \#

Selecting a query from the recent queries table will open a flyout containing metrics and information specific to the selected query:

![query_insights_ui_06.png](/_next/image?url=%2Fuploads%2Fquery_insights_ui_06_1047015bf1.png&w=2048&q=75)

As we can see from the flyout, this particular query has been run more than 3000 times in the last 24 hours. All metrics in the ‘query info’ tab are aggregate, but we can also view metrics from individual runs by selecting the ‘Query history’ tab:

![query_insights_ui_07.png](/_next/image?url=%2Fuploads%2Fquery_insights_ui_07_d6845c13ad.png&w=2048&q=75)

### A peek behind the curtain \#

Query insights was the first real project I had the opportunity to work on after joining ClickHouse in late February. I'd spent the first few weeks doing small tasks and bug fixes to get familiar with the codebase and processes before being asked to work on this feature. It speaks to the trust and confidence my team has in me, and in our hiring process \- high standards in hiring allow us to know that people who get hired are capable of the work they're given and will be able to hit the ground running.
