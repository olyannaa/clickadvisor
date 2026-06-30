# Rule Catalog

`docs/rules/` is the documentation source of truth for the ClickAdvisor rule
catalog.

The runtime code in `clickadvisor/rules/` and the rule cards in
`docs/rules/cards/` are intentionally separate:

- documentation cards capture scope, assumptions, validation status, and future
  proof notes
- runtime classes implement executable behavior
- catalog validation ensures metadata consistency before implementation lands

## Tier model

Rule tiers follow the contract defined in ADR-003 and specified in
`docs/rules/TIERS.md`.

- `1A`: formal equivalence from relational algebra
- `1B`: formal equivalence with ClickHouse-specific invariants
- `1C`: formal equivalence with statically verifiable preconditions
- `2`: cost-based recommendation
- `detector`: non-rewrite diagnostic signal
- `3`: speculative advisory recommendation that requires verification
- `env`: environment or deployment adjustment rule

The tier is not presentation-only metadata. It governs proof expectations,
automatic application policy, and validation requirements.

## Tier 2 rules

Tier `2` cards represent cost-based recommendations. They are expected to carry
strong evidence from plans, metadata, or storage context, but they are not
formal equivalence claims. Typical examples include design suggestions for
ordering keys, projections, join strategy, and storage-layout adjustments.

These rules should:

- explain the cost signal they depend on
- avoid theorem-like equivalence language
- describe expected impact conservatively

## Detector rules

Tier `detector` cards represent diagnostic findings that identify a likely
problem shape without necessarily prescribing a single canonical rewrite. They
are useful when the primary value is surfacing risk, waste, or anti-patterns
rather than transforming SQL directly.

These rules should:

- describe the signal being detected
- keep recommendations lightweight unless backed by a separate rule
- avoid pretending they are formal rewrite rules

## Environment rules

Tier `env` cards represent environment-aware findings and adjustments. They do
not rewrite SQL directly; instead they adapt guidance according to hardware,
settings, caching, concurrency, storage, or cluster topology.

These rules should:

- document the environment scope clearly
- separate deployment advice from query-semantic advice
- preserve the distinction between operator tuning and SQL rewrites

## Directory layout

- `SCHEMA.yaml`: JSON Schema for rule card structure
- `TEMPLATE.md`: authoring template and section guidance
- `TIERS.md`: detailed tier definitions and criteria
- `cards/`: YAML rule cards, one file per rule

## Adding a new rule

1. Copy the structure from `TEMPLATE.md`.
2. Create a new YAML card in `docs/rules/cards/`.
3. Fill metadata conservatively. Leave unknown proof details as TODOs rather
   than inventing them.
4. Validate the catalog before opening a PR.
5. Add runtime implementation later in `clickadvisor/rules/` only after the
   card is sufficiently validated.

## Validation

Run the catalog validator locally:

```bash
python scripts/rules/validate_catalog.py
```

The validator checks:

- schema compliance
- duplicate rule IDs
- cross-field constraints such as `tier=1A` with `opt_in=true`
- proof/risk requirements for more mature statuses

## Authoring policy

- Do not fabricate proofs or semantic guarantees.
- If a proof is not yet reviewed, keep the rule in `proposed`.
- Prefer explicit placeholders over vague prose.
- Use references to connect cards to ADRs, docs, and benchmark cases.
