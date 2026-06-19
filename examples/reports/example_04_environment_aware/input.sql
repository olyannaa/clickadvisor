SELECT
    user_id,
    sum(revenue) AS total_revenue
FROM analytics.fact_sales
WHERE sale_date >= toDate('2026-05-01')
GROUP BY user_id
ORDER BY total_revenue DESC
LIMIT 1000;
