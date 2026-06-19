# Rule Card Template

Use this template when authoring a new rule card in `docs/rules/cards/`.

Important:

- Do not invent proofs.
- Leave sections incomplete rather than filling them with uncertain claims.
- Tier classification must match `docs/rules/TIERS.md`.

```yaml
id: "R-XXX"
name: "descriptive_rule_name"
tier: "1A"
category: "predicate_canonicalization"
status: "proposed"

statement: >
  TODO: one-paragraph description of the transformation or recommendation in
  precise language. State what changes and under what general conditions.

preconditions:
  syntactic:
    - "TODO: AST-level or syntax pattern requirements"
  semantic:
    - "TODO: semantic assumptions that must hold"
  data:
    - "TODO: data- or schema-dependent assumptions, if any"

proof:
  status: "TODO"
  notes: >
    TODO: add proof sketch, derivation reference, or explicit note that proof is
    pending expert validation. Do not fabricate equivalence arguments.

ch_version:
  introduced: null
  deprecated: null
  last_validated: null

example_before: |
  -- TODO: query before rewrite

example_after: |
  -- TODO: query after rewrite

expected_speedup:
  estimate: null
  measurement_method: null

risks:
  - "TODO: semantic, operational, or observability caveat"

opt_in: false

references:
  - "TODO: doc, ADR, issue, or benchmark reference"
```

## Section guidance

### `id`

Stable identifier in `R-###` format. Never recycle an old ID for a different
rule.

### `name`

Machine-friendly snake_case name used across docs and implementation.

### `tier`

Choose from `1A`, `1B`, `1C`, `2`, `3`, or `env`. Use `docs/rules/TIERS.md` as
the authority.

### `category`

Broad thematic grouping such as `sargable`, `subquery`, or
`predicate_canonicalization`.

### `status`

- `proposed`: idea exists but is not validated
- `validated`: logic is reviewed and accepted
- `implemented`: backed by runtime code
- `deprecated`: retained for history but not active

### `statement`

Describe the rule in plain but precise language. Avoid proof language here;
reserve proof claims for the `proof` section.

### `preconditions`

Split assumptions into:

- `syntactic`: pattern shape in the AST or SQL surface
- `semantic`: conditions needed for correctness
- `data`: schema, engine, or workload-dependent requirements

### `proof`

For Tier 1 rules, this section is mandatory before `validated` or
`implemented`. For other tiers, use it to explain the reasoning basis or to mark
that no formal proof is expected.

### `ch_version`

Track introduction, deprecation, and last validation against ClickHouse
versions. Leave `null` until confirmed.

### `example_before` / `example_after`

Use compact examples that isolate the transformation. Avoid production-scale
queries.

### `expected_speedup`

Keep this estimate-focused. Do not imply benchmark truth if the rule is not
backed by repeatable evidence.

### `risks`

Record operator-facing caveats, ambiguity, observability tradeoffs, or rollout
concerns.

### `opt_in`

Use `true` only when the rule should never run automatically. Tier `1A` rules
must not be marked `opt_in: true`.

### `references`

Link supporting docs, ADRs, issues, benchmark cases, or review notes.
