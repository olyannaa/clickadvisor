SELECT
    user_id,
    event_time,
    payload
FROM analytics.events
WHERE event_type = 'purchase'
  AND event_date >= toDate('2026-05-01')
ORDER BY event_time DESC
LIMIT 100;
