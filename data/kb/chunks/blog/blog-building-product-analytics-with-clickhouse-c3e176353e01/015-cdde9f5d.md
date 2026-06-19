---
source: blog
url: https://clickhouse.com/resources/engineering/what-is-time-series-database
topic: building-a-product-analytics-solution-with-clickhouse
ch_version_introduced: '0.25'
last_updated: '2026-06-12'
chunk_index: 15
total_chunks_in_doc: 19
---

represents successful retention. Once churned users can be identified (or, better, those at risk of churning), we can correlate this with other statistics and identify issues in the product \- potentially using other tools such as session replays.

In our case, we measure churn as a customer's spend was above a threshold X in one month but fell below Y (can be the same as X) the following month. The value of X and Y here depends on usage profiles and can be adapted to looking at different customer sizes.

This analysis is an example of one that requires an external dataset \- specifically our billing data. This table is available in our warehouse as `dbt_marts_general.usage_history` and is periodically synced from M3ter. We use this table below with [conditionals](https://clickhouse.com/docs/en/sql-reference/functions/conditional-functions) to compute customer spend for the current and previous months.

```
  
```
1WITH 100 as previous_spend, 100 as new_spend
2SELECT organization__id AS organization__id,
3      max(organization__created_at) AS "Organization Created At",
4      argMax(organization__billing_model, timestamp_hour) AS "Current Billing Model",
5      argMax(organization__marketplace_name, timestamp_hour) AS "Marketplace",
6      argMax(organization__email_domain, timestamp_hour) AS "Email Domain",
7      argMax(account__name, timestamp_hour) AS "Account",
8      argMax(organization__owner_name, timestamp_hour) AS "Owner",
9      sumIf(organization__dollar_usage, toStartOfMonth(timestamp_hour) = toStartOfMonth(now('UTC') - INTERVAL 2 MONTH)) AS "2 Months Ago - MRR",
10      sumIf(organization__dollar_usage, toStartOfMonth(timestamp_hour) = toStartOfMonth(now('UTC') - INTERVAL 1 MONTH)) AS "Last Month - MRR"
11FROM dbt_marts_general.usage_history
12WHERE timestamp_hour >= toDateTime('2023-01-01 00:00:00')
13 AND timestamp_hour < toDateTime('2024-11-28 13:00:00')
14 AND (organization__email_domain NOT IN ('clickhouse.com', 'clickhouse.cloud', 'clickhouse.com_deleted'))
15GROUP BY organization__id
16HAVING ("2 Months Ago - MRR" > previous_spend AND "Last Month - MRR" < new_spend) AND ("Current Billing Model" = 'PAYG' OR "Current Billing Model" = 'Other')
17ORDER BY "2 Months Ago - MRR" DESC
```


```

### Relating to top of funnel activities [\#](/blog/building-product-analytics-with-clickhouse#relating-to-top-of-funnel-activities)

The above analytics focus on in\-product analytics. As mentioned above, like many companies we aim to correlate product behaviour with top of funnel activities performed prior to usage of the service. For this we need to correlate product accounts (organizations in our case) with website traffic.
