# Tier Specification

This document expands the tier model introduced in ADR-003 into operational
criteria for rule authoring and implementation.

## Overview

Each rule belongs to exactly one primary tier:

- `1A`
- `1B`
- `1C`
- `2`
- `detector`
- `3`
- `env`

The tier determines:

- what kind of evidence is required
- whether formal proof is expected
- whether automatic application may be allowed
- how output must be presented to the user

## `1A`: formal equivalence from relational algebra

Use `1A` for transformations whose correctness follows from general relational
algebra or universally valid query semantics under explicitly stated
assumptions.

Criteria:

- the rewrite is semantically equivalent, not merely beneficial
- the proof does not depend on ClickHouse-only execution quirks
- the main justification can be expressed independently of workload cost
- the rule is safe for automatic application once validated

Implications:

- proof is mandatory before `validated` or `implemented`
- `opt_in` must be `false`
- examples should isolate the algebraic transformation clearly

## `1B`: formal equivalence with ClickHouse-specific invariants

Use `1B` when correctness remains high-confidence but depends on documented
ClickHouse invariants, semantics, or function-specific behavior rather than pure
engine-agnostic algebra.

Criteria:

- the rewrite is still positioned as correctness-preserving
- the reasoning depends on ClickHouse behavior or guarantees
- the rule must cite those invariants explicitly in future proof work

Implications:

- proof is mandatory before maturity
- references to ClickHouse semantics are expected
- rollout may still be automatic, but only after expert review

## `1C`: formal equivalence with statically verifiable preconditions

Use `1C` when equivalence depends on preconditions that must be checked from the
query, schema, config, or known metadata before the rule can fire.

Criteria:

- equivalence is conditional, not unconditional
- preconditions are statically checkable in principle
- if the preconditions cannot be established, the rule must not apply as Tier 1

Implications:

- proof must describe the conditional nature of the rule
- implementation must encode precondition checks explicitly
- `opt_in` may be used if rollout policy is intentionally conservative

## `2`: cost-based recommendation

Use `2` for recommendations that are not formal semantic rewrites but are
supported by cost-model signals such as `EXPLAIN ESTIMATE`, `system.parts`, or
storage-layout evidence.

Criteria:

- benefit is estimated rather than proven
- semantics may remain unchanged, but the recommendation is justified by cost
  evidence
- output should discuss estimate quality and assumptions

Implications:

- proof is not expected in the formal sense
- expected speedup and measurement method fields matter more
- automatic application should be conservative and policy-driven

## `3`: advisory or LLM-assisted rule

Use `3` for suggestions that depend on advisory reasoning, hypothesis
generation, or LLM assistance and cannot stand as self-justifying optimization
rules.

Criteria:

- recommendation is not self-authenticating
- manual review or mandatory verification is required
- ambiguity and caveats must be explicit

Implications:

- risks must be documented before mature statuses
- implementation should preserve provenance of the advisory source
- auto-apply is generally inappropriate

## `detector`: diagnostic signal without canonical rewrite

Use `detector` for rules that identify an important anti-pattern, safety risk,
or inefficiency signal but do not inherently encode a single formal rewrite or
cost-model intervention.

Criteria:

- the main value is detection, not transformation
- the output may point to follow-up investigation or downstream rule families
- the finding can be useful even when no automatic rewrite is emitted

Examples of detector-style intent:

- full scan risk
- cross join danger
- wide-table `SELECT *`
- missing `LIMIT` on unbounded result shape

Implications:

- proofs are generally not algebraic
- the card should document the detection condition precisely
- recommendations should remain careful and not over-claim a single fix
- detectors may feed prioritization or routing for richer rule execution later

## `env`: environment adjustment rule

Use `env` for rules that alter ranking, visibility, rollout, or wording based on
deployment environment rather than rewriting SQL directly.

Criteria:

- the rule acts on context such as hardware, settings, topology, or deployment
  constraints
- it adjusts applicability or presentation of other rules
- it may suppress or re-rank advice instead of changing the query

Implications:

- proofs are usually not algebraic
- references should document the environment assumption
- implementation often lives near orchestration rather than AST rewrite logic

## Classification checklist

Ask these questions before assigning a tier:

1. Is the transformation semantically equivalent?
2. If yes, is the proof algebraic, ClickHouse-specific, or conditional on
   statically checkable preconditions?
3. If no, is the recommendation driven by cost evidence or by advisory
   reasoning?
4. Does the rule rewrite SQL directly, or only adjust rule applicability based
   on environment?

If a rule cannot clearly answer these questions, keep it in `proposed` until the
classification is reviewed.
