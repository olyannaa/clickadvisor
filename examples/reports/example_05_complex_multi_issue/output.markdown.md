## ClickAdvisor Report

- Findings total: `6`
- Tier mix: `1A x5`, `3 x1`
- Estimated impact: `high`

### Formal findings

- `R-010`: collapse OR chain into `IN`
- `R-015`: remove `DISTINCT` after `GROUP BY`
- `R-009`: replace singleton `IN` with equality
- `R-001`: replace `count(DISTINCT ...)` with `uniqExact(...)`
- `R-005`: rewrite `toDate(DateTime)` filter into a range predicate

### Advisory finding

- Evaluate whether a projection or PREWHERE-friendly query shape would reduce
  read pressure. This remains `Tier 3` and requires review.
