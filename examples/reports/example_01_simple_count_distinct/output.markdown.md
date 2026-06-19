## ClickAdvisor Report

- Statement: `main`
- LLM mode: `none`
- Findings: `1`

### Finding F-001

- Type: `rule_match`
- Tier: `1A`
- Rule: `R-001 count_distinct_to_uniqExact`
- Title: Use a specialized exact distinct aggregate
- Confidence: `0.98`

**Before**

```sql
SELECT count(DISTINCT user_id) AS distinct_users
FROM analytics.events
WHERE event_date = toDate('2026-05-01');
```

**After**

```sql
SELECT uniqExact(user_id) AS distinct_users
FROM analytics.events
WHERE event_date = toDate('2026-05-01');
```

Notes:

- Tier 1A rule match
- Estimated impact: low to medium
