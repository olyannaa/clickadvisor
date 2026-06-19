# GitHub Issues Case Staging

This folder is reserved for manually curated benchmark cases derived from
`github.com/ClickHouse/ClickHouse/issues`, especially performance-oriented
reports.

No automatic ingestion is performed here in this stage because issue triage and
problem extraction require manual filtering and expert interpretation.

Recommended future workflow:

1. identify a performance-relevant issue
2. extract or reconstruct the minimal SQL shape
3. create a YAML case using `benchmark/TEMPLATE.yaml`
4. attach notes linking back to the source issue
5. leave expert labels empty until reviewed
