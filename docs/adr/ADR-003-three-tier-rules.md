# ADR-003: Three-Tier Rule System

## Status

Accepted

## Context

Not all optimization advice has the same epistemic status. Some SQL rewrites can
be justified by algebraic equivalence under explicit assumptions. Some
recommendations are not pure equivalence transformations but still have strong
cost-based grounding in metadata, planner estimates, and storage layout. Others
may originate as plausible suggestions from a language model or a heuristic idea
generator and require separate verification before they can be trusted. Treating
all of these outputs as if they were equivalent would produce a misleading user
experience and would undermine the project’s core differentiation.

In SQL advisory tools, one common failure mode is confidence collapse. A system
that mixes proven rewrites, rough heuristics, and speculative suggestions into a
single recommendation list implicitly overstates the reliability of the weakest
items. That is especially dangerous here because the product is intended for DBA
who need to understand not only what the tool suggests, but also why it thinks
that suggestion is safe. If a user cannot distinguish a theorem-like rewrite
from a plausible idea, the tool teaches the wrong trust habit.

The opposite failure mode also exists. If the system labels all recommendations
as merely advisory, then formally safe and reusable rewrites lose their value.
The user is forced to treat a mathematically equivalent transformation with the
same suspicion as an unverified speculative hint. That flattens the trust model
and makes the product appear less rigorous than it actually is.

ClickAdvisor therefore needs a rule taxonomy that preserves differences in
validation burden. The taxonomy must be simple enough to explain in the CLI and
docs, yet expressive enough to capture the real distinction between proof,
estimation, and advisory generation. It must also guide implementation. A rule’s
tier is not just a label for the UI; it determines what evidence the engine
needs, what outputs it may emit, and what verification must happen before the
advice is shown.

Within the highest-confidence class, there is additional nuance. Some Tier 1
rules are direct relational-algebra equivalences. Others depend on explicitly
checkable ClickHouse invariants or schema/settings preconditions. Without a
finer subdivision, Tier 1 can become too vague for internal rule design even if
it remains acceptable as a user-facing top-level label.

## Decision

ClickAdvisor organizes optimization logic into three top-level tiers of
confidence.

### Tier 1: formally equivalent

Tier 1 is reserved for rewrites that are semantically equivalent under explicit,
documented assumptions. These transformations are grounded in relational algebra
or in ClickHouse invariants that can be checked statically from available
context. Tier 1 is the highest-confidence output class and represents the most
trustworthy form of automated rewrite in the system.

Tier 1 is internally subdivided into three subcategories:

- Tier 1A: pure relational-algebra equivalences. These are rewrites whose
  validity follows from general query algebra under stated assumptions, such as
  predicate simplification, projection normalization, or safe operator
  reordering where semantic equivalence is algebraically provable.
- Tier 1B: equivalences that depend on ClickHouse-specific invariants. These are
  still treated as formally safe, but their proof relies on documented engine
  behavior or storage semantics that must be explicitly referenced rather than
  assumed to hold across SQL engines.
- Tier 1C: equivalences gated by statically verifiable preconditions from schema
  or settings context. These are accepted as Tier 1 only when the required
  preconditions can be checked from available metadata, configuration, or parse
  context. If those preconditions cannot be verified, the rule does not fire as
  Tier 1.

### Tier 2: cost-based

Tier 2 contains recommendations that are not purely algebraic equivalence
transformations but are justified by cost-oriented evidence. The main sources of
evidence are `EXPLAIN ESTIMATE`, `system.parts`, schema metadata, storage layout
signals, and environment characteristics. Tier 2 recommendations are presented
as evidence-based optimization advice rather than semantic theorems.

### Tier 3: LLM advisory

Tier 3 contains ideas, explanations, and candidate rewrites produced through LLM
assistance or similarly speculative mechanisms. Tier 3 outputs are never treated
as self-justifying. Any materially actionable Tier 3 recommendation requires
verification before it can be surfaced as trusted advice. The tier label must
remain visible to the user.

## Consequences

This decision creates a clear trust contract for users. When ClickAdvisor
surfaces an optimization recommendation, the tier communicates what kind of
claim is being made. Tier 1 means “the system is asserting formal equivalence
under explicit assumptions.” Tier 2 means “the system is making a grounded cost
argument.” Tier 3 means “the system is offering an advisory suggestion that is
not self-authenticating.” That is much easier for a DBA to work with than a
single confidence score that tries to compress different kinds of evidence into
one number.

Implementation also becomes more disciplined. Rule authors must decide which
kind of evidence a rule depends on before adding it to the catalog. A rewrite
that feels attractive but lacks formal proof cannot be quietly placed beside
algebraic equivalences. Likewise, a useful cost-based recommendation is not
forced into a weaker-looking advisory bucket simply because it is not a theorem.

The Tier 1A/1B/1C subdivision helps internally without overloading the top-level
mental model. It gives the team a structured way to separate general algebraic
equivalence from ClickHouse-specific equivalence and from equivalence that
depends on verified preconditions. This should improve documentation quality and
rule review because each Tier 1 rule can explain exactly what it relies on.

There is some extra authoring burden. Every recommendation path must preserve
tier provenance and, for Tier 1C and Tier 2 especially, record the assumptions
and evidence it used. That is a deliberate cost, because the alternative is to
hide ambiguity and push verification burden onto users.

The decision also constrains UI and report design. Output formatting must not
collapse tiers into a generic recommendation list. The product has to make room
for tier labels, caveats, and evidence references. This may make reports more
structured and slightly less minimal, but it directly supports trust.

## Alternatives Considered

### Single undifferentiated rule layer

This was rejected because it would mix proofs, heuristics, and speculative
advice into one bucket. That design would either overstate the reliability of
Tier 3-style suggestions or understate the value of formally safe rewrites. In
either case, the user would lose the distinction that makes the system
differentiated.

### Two tiers only: deterministic vs heuristic

This was rejected because it still compresses importantly different cases. A
cost-based recommendation supported by `EXPLAIN ESTIMATE` and `system.parts` is
meaningfully stronger than a raw LLM suggestion, even if neither is a pure
algebraic proof. Collapsing them together would weaken the product’s reasoning
model and make verification workflows less precise.
