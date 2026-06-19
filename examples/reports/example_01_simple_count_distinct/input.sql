SELECT
    count(DISTINCT user_id) AS distinct_users
FROM analytics.events
WHERE event_date = toDate('2026-05-01');
