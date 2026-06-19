# ADR-010: Version-Aware Rule Filtering

## Status

Accepted

## Context

ClickHouse evolves quickly. In practical terms, that means the product cannot
assume that a recommendation validated against one server generation will remain
equally useful, equally safe, or even semantically correct against another.
ClickHouse ships on an aggressive release cadence, and features around query
planning, projections, aggregate implementations, JOIN execution, settings, and
storage behavior keep changing. A recommendation that made sense in `23.x` may
be less relevant in `24.x`, and a recommendation that was once a strong
optimization may become neutral or actively misleading in `25.x`.

This is not a theoretical concern. It has already appeared in customer
development conversations with real DBA. The same broad complaint surfaced more
than once: generic LLM tools often give advice that sounds plausible but is
quietly out of date for the actual ClickHouse version in use. The tool may
recommend an older workaround after the engine has improved a planner path, or
it may miss a newer feature because its training data or retrieval context lags
behind the release stream. In both cases, the user receives something that is
linguistically confident but operationally weak.

That failure mode is especially damaging for ClickAdvisor because version drift
cuts directly against the product’s trust model. The core promise is not just
that the tool can say interesting things about SQL, but that it can say them in
a way that is more grounded than a generic model. If ClickAdvisor were to show
rules without regard to the user’s ClickHouse version, it would recreate the
exact class of problem it is meant to solve: recommendations detached from
actual engine reality.

The existing rule catalog already moves in the right direction by carrying
version metadata fields such as `ch_version.introduced` and
`ch_version.last_validated`. However, those fields do not help unless they are
treated as executable policy rather than passive documentation. Version metadata
must influence rule selection in the runtime pipeline, not merely appear in
YAML for future readers.

There is also a UX consideration. Users should not be expected to manually
screen every recommendation against their own server version. That would impose
precisely the verification overhead the product is supposed to remove. The
system should determine the version once, then use that information to narrow
the rule universe before findings are emitted.

## Decision

ClickAdvisor becomes version-aware by default.

When the tool is connected to a live ClickHouse instance, it determines the
server version through `SELECT version()` early in the analysis pipeline. When a
live connection is not available, the user may provide an explicit CLI override
through `--ch-version`. One of these two inputs becomes the canonical version
context for the current run.

Rule filtering is then applied against the version metadata stored in the rule
catalog. Each rule card must include, at minimum:

- `ch_version.introduced`
- `ch_version.last_validated`

At runtime:

- a rule is not shown if `ch_version.introduced` is greater than the user’s
  ClickHouse version
- a rule remains eligible if it was introduced on or before the user’s version
- `ch_version.last_validated` is used as a trust and maintenance signal for the
  team, and may be surfaced in reports or diagnostics when relevant

This design makes version detection a mandatory stage of the analysis pipeline,
not an optional refinement. The product is allowed to operate without a live
connection, but it is not allowed to operate without a version assumption. If
the system cannot detect the version automatically, it must require or infer an
explicit version input before emitting version-sensitive findings.

The decision applies to deterministic rules, cost-based rules, and any future
LLM-assisted recommendation path that draws from the same catalog. Version-aware
filtering is therefore a core property of the recommendation engine rather than
an isolated guardrail on one subsystem.

## Consequences

The immediate consequence is stronger recommendation hygiene. Users will no
longer be shown rules that clearly postdate their installed ClickHouse version,
which removes one of the most visible sources of low-trust advice. This aligns
the product with its positioning: the system is not merely “aware of
ClickHouse,” but aware of the user’s actual ClickHouse.

Another consequence is catalog discipline. From this point forward, version
fields are no longer optional bookkeeping. Every rule card is required to carry
filled `ch_version` metadata, because missing version metadata would make the
runtime filtering model incomplete. This raises authoring overhead slightly, but
it is a worthwhile cost because it turns vague temporal assumptions into
explicit contract data.

The pipeline also gains a new mandatory concern: version detection. That means
CLI flows, offline analysis flows, and future integrations such as MCP must all
carry version context through the same interface. In practice, this is healthy.
It forces consistency between local, connected, and automated usage modes.

There is an implementation burden around version comparison and normalization.
ClickHouse version strings are not always simple semver values; they may include
suffixes such as LTS markers or patch qualifiers. The product therefore needs a
single internal comparison strategy so that catalog filtering behaves
predictably. That burden is accepted because the alternative is silent
misclassification of rule applicability.

This decision also improves LLM safety indirectly. If the LLM path uses the same
catalog and the same version gates, the generated guidance inherits a stronger
time-awareness boundary. That does not make LLM output self-trusting, but it
reduces the chance that retrieval and generation will drift into obviously
inapplicable recommendations.

## Alternatives Considered

### Show all rules with a disclaimer

This was rejected because it reproduces the exact failure mode the product is
trying to fix. A disclaimer does not meaningfully reduce the cognitive load on
the user; it simply shifts version-screening responsibility back onto them while
preserving noisy output. That is effectively the generic GPT experience, just
wrapped in a different interface.

### Track version compatibility only in documentation

This was rejected because passive documentation does not influence runtime
behavior. The system would still emit inappropriate rules unless the user or the
developer manually cross-checked each finding. The project needs version
metadata to be operational, not decorative.

### Detect version only for Tier 2 and Tier 3

This was rejected because even formally safe or ClickHouse-specific Tier 1
rules can have introduction boundaries tied to engine features or function
availability. Version awareness must apply to the whole catalog to keep the
trust model coherent.
