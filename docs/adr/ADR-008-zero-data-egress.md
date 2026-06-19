# ADR-008: Security Model and Zero Data Egress

## Status

Accepted

## Context

ClickAdvisor is intended for environments where query text, schema details, and
operational metadata may already be sensitive. In many of the teams likely to
use the tool, the main blocker for adopting external AI systems is not
theoretical model quality but practical data governance: who can access SQL,
what is allowed to leave the environment, what permissions the runtime needs,
and whether any component might accidentally execute a destructive operation.

Because the product’s goal is advisory analysis rather than data processing, it
would be architecturally wasteful and commercially risky to request more access
than necessary. If the utility needed to read table rows, execute mutating SQL,
or ingest broad operational telemetry by default, it would become much harder to
deploy in regulated or security-conscious settings. The product would also be
harder to reason about internally because the analysis surface would mix logical
query reasoning with direct data access patterns.

The project already has a cleaner boundary available. For the intended analysis
workflow, it is sufficient to operate on SQL text, planner outputs without
`ANALYZE`, schema definitions, metadata such as `system.parts`, relevant
configuration, and hardware characteristics. None of these require reading table
contents. That means the product can keep a hard separation between reasoning
about query behavior and touching the actual data being queried.

Remote LLM usage introduces an additional concern. Even if the product does not
read table rows, query text itself can contain literals, identifiers, or other
fragments that reveal sensitive information. If remote inference is supported at
all, a structured redaction step is required before any content leaves the
host. A best-effort string scrub is not enough; redaction has to be syntax-aware
so that the resulting prompt preserves query structure while stripping sensitive
values where possible.

## Decision

ClickAdvisor adopts a zero-data-egress security posture for its core workflow.

The utility does not read table data and does not require access to table
contents. Its analysis inputs are restricted to:

- SQL text
- `EXPLAIN` outputs without `ANALYZE`
- schemas and DDL context
- metadata such as `system.parts`
- database configuration and settings
- hardware specifications relevant to analysis

The runtime connection model is read-only. The utility does not execute `ALTER`,
`INSERT`, `UPDATE`, `DELETE`, `DROP`, or any other mutating statements as part
of normal operation. In practice, the product should be run with a read-only
database role sufficient to fetch the required metadata and plan information.

When `--llm=remote` is enabled, all outbound prompt content derived from SQL
must first pass through PII- and literal-redaction logic implemented using
`sqlglot` parsing. The intent is to preserve enough structural information for
advisory reasoning while minimizing exposure of sensitive values and query
payload details.

This security model is part of the product contract, not an optional deployment
recommendation.

## Consequences

The clearest consequence is a stronger adoption story for regulated and
security-conscious environments. Because the utility does not require table-data
access and can operate with read-only permissions, security review becomes
simpler and the deployment footprint remains easier to justify.

The decision also creates a healthy architectural boundary. Analysis logic must
be derived from plans, metadata, schemas, and configuration instead of relying
on shortcuts that inspect data directly. That is consistent with the product’s
cost-model orientation and prevents accidental dependence on data access that
would later be hard to remove.

Remote LLM support becomes more constrained, but in a productive way. Any
feature that depends on remote inference has to be designed around a redacted
representation of SQL, which naturally limits leakage and keeps the remote path
secondary to the deterministic core. This also makes the distinction between
local and remote LLM modes concrete rather than merely operational.

There are tradeoffs. Some classes of advice that might benefit from direct data
inspection or mutation-based validation are intentionally out of scope. The
product accepts that limitation because the trust and deployability gains are
more important than squeezing extra signal from data access.

Another consequence is that connection and permission guidance must be explicit
in documentation and CLI behavior. The tool should make it clear what it reads,
what it never touches, and what permissions are expected. That clarity is part
of the security promise.

## Alternatives Considered

### Allow table-data access for richer analysis

This was rejected because it would materially complicate compliance, broaden the
attack surface, and undermine the product’s zero-data-egress posture. It would
also make adoption harder in exactly the environments the product aims to serve.

### Permit mutating database access

This was rejected because ClickAdvisor is an advisory utility, not an execution
or migration tool. Granting mutation privileges would be disproportionate to the
problem being solved and would make the runtime significantly riskier.

### Remote LLM without structured redaction

This was rejected because raw SQL can contain sensitive literals and business
identifiers. Sending that content unredacted would conflict with the security
model and would make remote mode difficult to justify operationally.
