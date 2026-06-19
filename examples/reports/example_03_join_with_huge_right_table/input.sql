SELECT
    e.user_id,
    e.event_time,
    d.segment_name
FROM analytics.events AS e
INNER JOIN dim.user_segments AS d
    ON e.user_id = d.user_id
WHERE e.event_date >= toDate('2026-05-01')
  AND d.is_active = 1;
