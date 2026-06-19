## ClickAdvisor Report

### Finding F-001

- Type: `rule_match`
- Tier: `2`
- Title: Right-side JOIN input is disproportionately large
- Severity: `high`

The plan suggests that the right side of the JOIN is expensive to build relative
to the filtered left side. The tool does not emit a forced rewrite here because
the best fix depends on schema and workload patterns.

### Finding F-002

- Type: `advisory`
- Tier: `3`
- Verification required: `true`

Possible follow-up directions include dictionary-style lookups or earlier
dimension filtering, but this remains advisory pending operator review.
