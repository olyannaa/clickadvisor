# ADR-011: MCP Server as Secondary Interface

## Status

Accepted

## Context

The primary ClickAdvisor interaction model remains the CLI. That is still the
best fit for DBA workflows, local-first operation, reproducible CI runs, and
batch-style usage. However, another reality has now emerged from customer
development: many technically sophisticated users are already experimenting with
LLM tooling through the Model Context Protocol (MCP). For this audience, MCP is
not a novelty layer. It is becoming a practical integration point for invoking
specialized tools from within assistant-driven workflows.

This matters because friction is cumulative. If a DBA already uses an assistant
that can call MCP tools, asking them to context-switch into a separate wrapper
or to manually shuttle SQL back and forth into a standalone binary introduces
avoidable friction. The core analysis engine may still be strong, but its
adoption surface becomes narrower than necessary. In contrast, exposing the same
analysis capability as an MCP tool allows ClickAdvisor to participate naturally
in the workflows users already have.

At the same time, the project should not overreact and make MCP the new center
of gravity. That would create new risks. MCP alone does not replace the CLI
need for CI/CD pipelines, scriptability, shell-first DBA operation, or explicit
local execution patterns. It also risks turning the product into “something you
need an LLM shell to access,” which conflicts with the architecture’s
autonomous-tool posture.

The right question is therefore not whether MCP is useful. It clearly is. The
question is how to add it without creating duplicate business logic, diverging
behavior between interfaces, or confusion about which interface is primary. The
project needs one core analysis engine that can be reached from more than one
surface, not two partially overlapping implementations.

## Decision

ClickAdvisor adds an MCP server as a second interface layered on top of the same
core analysis engine.

The CLI remains the primary interface. MCP is explicitly secondary and is added
to reduce integration friction for users who already operate in LLM+tooling
environments.

The architectural split is:

- `clickadvisor/core/` — all analysis logic, rule evaluation, reporting, and
  core orchestration
- `clickadvisor/cli/` — the primary command-line interface
- `clickadvisor/mcp_server/` — a thin MCP interface that wraps the same core
  entrypoint, expected to remain small and interface-focused

The MCP module is responsible for protocol adaptation only. Its role is to
translate an MCP tool call into the existing `core.analyze()` flow, collect the
result, and return it in a shape appropriate for MCP clients. It must not
contain duplicate rule logic, duplicate planner logic, or a second report
construction pathway.

This interface is scheduled for the final week of the initial development
window. That sequencing is intentional. The team first stabilizes the core
engine and the CLI contract, then adds MCP as a thin wrapper once the analysis
surface is sufficiently mature.

## Consequences

The biggest positive consequence is interface reuse without logic duplication.
Users gain a second access path that fits emerging assistant-driven workflows,
while the engineering team preserves a single source of truth for analysis. This
should improve adoption among power users without weakening the product’s
architectural clarity.

The decision also sharpens code organization. If MCP is forced to remain thin,
then any temptation to place business logic in interface code becomes easier to
spot and reject. That is valuable not only for MCP itself, but also for the
overall maintainability of the project. The same discipline that keeps the MCP
layer small also helps keep the CLI honest.

There is some added packaging and operational overhead. The project now has two
interface surfaces to document, test, and support. That includes argument
mapping, output-shape expectations, and possible interface-specific error
handling. The project accepts this cost because the alternative would be forcing
users into workflows that do not match how they already consume tooling.

Another consequence is that result design needs to be interface-portable. The
core output must be structured enough that both CLI and MCP can present it
cleanly without either interface inventing its own interpretation. This is
generally a healthy pressure: it encourages well-defined report contracts rather
than ad hoc string formatting.

The timing consequence also matters. By pushing MCP implementation to the last
week of the initial cycle, the team protects the MVP from becoming an interface
project before the engine has earned it. MCP is added because the core is worth
exposing, not as a substitute for completing the core.

## Alternatives Considered

### Make MCP the only interface

This was rejected because it would abandon core CLI use cases that matter to the
target audience: CI/CD integration, shell-first workflows, explicit scripting,
and local autonomy. It would also make adoption depend on an external assistant
or MCP-capable host, which is too restrictive for the product’s main operating
mode.

### Build separate logic paths for CLI and MCP

This was rejected because duplicated logic would inevitably drift. Different
interfaces would begin to show different recommendations, different evidence, or
different bugs for the same SQL input. That is unacceptable in a trust-sensitive
advisor product.

### Postpone MCP indefinitely

This was rejected because customer development already shows real demand among
DBA who use LLM tooling with MCP. Ignoring that integration surface entirely
would preserve conceptual purity at the expense of adoption friction. A thin MCP
wrapper is a better balance.
