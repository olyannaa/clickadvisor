WITH base AS (
    SELECT
        user_id,
        event_time,
        event_type,
        payload,
        toDate(event_time) AS event_day
    FROM analytics.events
    WHERE toDate(event_time) = toDate('2026-05-01')
       OR toDate(event_time) = toDate('2026-05-02')
)
SELECT DISTINCT
    user_id,
    count(DISTINCT session_id) AS sessions,
    sumIf(revenue, event_type = 'purchase') AS revenue_sum
FROM base
GROUP BY user_id
HAVING user_id IN (42)
ORDER BY user_id;
