## ClickAdvisor Report

- Statement: `main`
- Findings: `1`

### Finding F-001

- Tier: `2`
- Title: Potential PREWHERE optimization
- Confidence: `0.74`

The query reads a wide payload column while filtering on columns that are likely
better evaluated earlier. This is reported as a cost-based recommendation rather
than a guaranteed rewrite.

Signals:

- `ReadFromMergeTree`
- wide row shape
- selective predicates on `event_type` and `event_date`
