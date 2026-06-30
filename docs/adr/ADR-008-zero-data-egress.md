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

The MVP does not include remote generative LLM calls. AI-agent usage is handled through MCP: an external agent can call ClickAdvisor as a local tool, but ClickAdvisor itself does not send SQL or metadata to an LLM provider.

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

MCP-based AI-agent usage stays compatible with the zero-data-egress model because ClickAdvisor runs locally and returns deterministic findings to the calling agent. If a user chooses to paste those findings into an external tool, that is outside the analyzer runtime rather than hidden product behavior.

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

### Hidden remote inference

This was rejected because raw SQL can contain sensitive literals and business identifiers. Any hidden outbound inference path would conflict with the security model and weaken the local-first product claim.
